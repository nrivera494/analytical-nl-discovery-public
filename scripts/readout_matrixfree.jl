# agent: gpt-a; model: gpt-6-astra; family: gpt
# Exact tangent of the same scalar no-shock RK4IP map, paired with the public
# discrete adjoint. It permits whole-grid covariance eigenvalues without
# reconstructing every covariance entry on a long temporal window.
include(joinpath(@__DIR__,"readout_covariance.jl"))
using Random

struct ReadoutCovarianceOperator{P,S,C}
    p::P
    sol::S
    cache::C
    stage_a::Array{ComplexF64,3}
    stage_r::Array{Float64,3}
    half1::Matrix{ComplexF64}
    half2::Matrix{ComplexF64}
    phase::Vector{ComplexF64}
    nbar::Vector{Float64}
    bath_indices::Vector{Int}
    bath_z::Vector{Float64}
    bath_weight::Vector{Float64}
    bath_spectrum::Vector{Float64}
    dz::Float64
end

function make_operator(c)
    get(c,"public_model",false) && error("Matrix-free adapter is no-shock only")
    p=readout_setup(c);n=p.n;dz=c["length_m"]/c["steps"]
    sol=solve_mmgnlse(p.a,p.pars,dz;saveat=:steps)
    cache=PP._mmgnlse_solver_cache(p.pars); ns=length(sol.z)-1
    aa=zeros(ComplexF64,n,4,ns);rr=zeros(n,4,ns)
    h1=zeros(ComplexF64,n,ns);h2=similar(h1)
    frac=cache.raman.fraction
    kernel=iszero(frac) ? zeros(ComplexF64,n) : cache.raman.ha.+cache.raman.hb
    for j in 1:ns
        z0,z1=sol.z[j],sol.z[j+1];h=z1-z0;mid=(z0+z1)/2
        H1=PP._mmgnlse_linear_propagator(p.pars,z0,mid,cache)
        H2=PP._mmgnlse_linear_propagator(p.pars,mid,z1,cache)
        h1[:,j].=vec(H1);h2[:,j].=vec(H2)
        w0=ifft(@view(sol.fields[:,:,:,j]),1)
        base=H1.*w0
        k1=H1.*PP._mmgnlse_nonlinear_spectral(w0,p.pars,cache)
        w2=base.+h/2 .*k1
        k2=PP._mmgnlse_nonlinear_spectral(w2,p.pars,cache)
        w3=base.+h/2 .*k2
        k3=PP._mmgnlse_nonlinear_spectral(w3,p.pars,cache)
        w4=H2.*(base.+h.*k3)
        for (k,w) in enumerate((w0,w2,w3,w4))
            a=vec(fft(w,1));intensity=abs2.(a)
            aa[:,k,j].=a
            rr[:,k,j].=(1-frac).*intensity
            if !iszero(frac)
                rr[:,k,j].+=frac.*real.(fft(kernel.*ifft(intensity)))
            end
        end
    end
    aw=vec(get_spectral_field(sol));phase=exp.(1im.*angle.(aw));nbar=p.weight.*abs2.(aw)
    bath=get(c,"raman",false)
    wanted=Int(get(c,"bath_intervals",32))
    indices=bath ? unique(round.(Int,range(1,length(sol.z);length=min(wanted+1,length(sol.z))))) : Int[]
    zs=sol.z[indices];weights=zeros(length(zs))
    if bath
        weights[1:end-1].+=diff(zs)./2;weights[2:end].+=diff(zs)./2
    end
    Cw=bath ? raman_langevin_spectrum_coth(n,p.grid.dt,p.omega0/(2pi),p.gamma;temperature_K=300.0) : zeros(n)
    ReadoutCovarianceOperator(p,sol,cache,aa,rr,h1,h2,phase,nbar,indices,zs,weights,Cw,dz)
end

function stage_jvp(op,j,k,dw)
    a=@view op.stage_a[:,k,j];r=@view op.stage_r[:,k,j]
    da=fft(dw);di=2 .*real.(conj.(a).*da)
    f=op.cache.raman.fraction
    dr=(1-f).*di
    if !iszero(f)
        dr.+=f.*real.(fft((op.cache.raman.ha.+op.cache.raman.hb).*ifft(di)))
    end
    1im*op.p.gamma.*ifft(da.*r.+a.*dr)
end

function step_jvp(op,j,dw)
    h=op.sol.z[j+1]-op.sol.z[j]
    h1=@view op.half1[:,j];h2=@view op.half2[:,j]
    mid=h1.*dw
    k1=h1.*stage_jvp(op,j,1,dw)
    k2=stage_jvp(op,j,2,mid.+h/2 .*k1)
    k3=stage_jvp(op,j,3,mid.+h/2 .*k2)
    k4=stage_jvp(op,j,4,h2.*(mid.+h.*k3))
    h2.*(mid.+h/6 .*(k1.+2 .*k2.+2 .*k3)).+h/6 .*k4
end

function covariance_product(op,x)
    p=op.p;n=p.n
    q=complex.(@view(x[1:n]),@view(x[n+1:2n]))
    terminal=reshape(sqrt.(p.weight).*op.phase.*q,n,1,1)
    bath=!isempty(op.bath_indices)
    adj=solve_adjoint(terminal,p.pars,op.dz;forward_solution=op.sol,units=:power,
        saveat=bath ? op.bath_z : [0.0,p.pars.length],adjoint_mode=:discrete_rk4ip,checkpoint_stride=32)
    dw=ifftshift(vec(get_spectral_field(adj;units=:power))./p.weight)
    kicks=zeros(ComplexF64,n,length(op.bath_indices))
    if bath
        lt=reshape(get_temporal_field(adj;z=:all,units=:power),n,:)
        for k in eachindex(op.bath_indices)
            at=vec(@view op.sol.fields[:,:,:,op.bath_indices[k]])
            b=-2 .*imag.(at.*conj.(@view lt[:,k]))./n
            cb=real.(ifft(op.bath_spectrum.*fft(b)))
            kicks[:,k].=(2p.gamma^2/(p.grid.dt*1e-12)*op.bath_weight[k]).*ifft(1im.*at.*cb)
        end
    end
    cursor=1
    if bath && first(op.bath_indices)==1
        dw.+=@view kicks[:,1];cursor+=1
    end
    for j in 1:length(op.sol.z)-1
        dw=step_jvp(op,j,dw)
        if bath && cursor<=length(op.bath_indices) && op.bath_indices[cursor]==j+1
            dw.+=@view kicks[:,cursor];cursor+=1
        end
    end
    result=conj.(op.phase).*sqrt.(p.weight).*fftshift(dw)
    vcat(real.(result),imag.(result))
end

function lanczos_lowest(apply,n;count=1,maxiter=120,tol=1e-8,seed=20261010,label="eigen")
    rng=MersenneTwister(seed);q=randn(rng,n);q./=norm(q)
    Q=zeros(n,maxiter);diag=Float64[];off=Float64[]
    previous=zeros(n);beta=0.0;started=time()
    result=nothing
    for j in 1:maxiter
        Q[:,j].=q
        w=apply(q).-beta.*previous
        alpha=dot(q,w);w.-=alpha.*q
        for _ in 1:2
            basis=@view Q[:,1:j]
            w.-=basis*(basis'*w)
        end
        beta_new=norm(w);push!(diag,alpha)
        E=eigen(SymTridiagonal(diag,off))
        used=min(count,j);res=beta_new.*abs.(E.vectors[end,1:used])
        result=(values=E.values[1:used],vectors=Q[:,1:j]*E.vectors[:,1:used],
            residuals=res,iterations=j,seconds=time()-started,
            converged=used==count && maximum(res)<tol)
        if j%20==0
            @printf("KRYLOV %s iter=%d min=%.9g residual=%.3g %.1fs\n",label,j,E.values[1],res[1],time()-started);flush(stdout)
        end
        (j>=min(20,n) && result.converged || beta_new<1e-14 || j==n) && break
        j==maxiter && break
        push!(off,beta_new);previous=q;q=w./beta_new;beta=beta_new
    end
    result
end

function amplitude_product(op,x)
    n=op.p.n
    covariance_product(op,vcat(x,zeros(n)))[1:n]
end

function selected_amplitude_covariance(op,indices;label="core",include_phase=false)
    p=op.p;n=p.n;m=length(indices);bath=!isempty(op.bath_indices)
    columns=include_phase ? 2m : m
    G=zeros(ComplexF64,n,columns)
    B=zeros(ComplexF64,bath ? n*length(op.bath_z) : 0,columns)
    started=time();complete=Threads.Atomic{Int}(0)
    function fill_one(j)
        local bin,terminal,adj,lt,at,response,done
        bin=indices[mod1(j,m)];terminal=zeros(ComplexF64,n,1,1)
        terminal[bin]=sqrt(p.weight[bin])*op.phase[bin]*(j>m ? 1im : 1.0)
        adj=solve_adjoint(terminal,p.pars,op.dz;forward_solution=op.sol,units=:power,
            saveat=bath ? op.bath_z : [0.0,p.pars.length],adjoint_mode=:discrete_rk4ip,checkpoint_stride=32)
        G[:,j].=vec(get_spectral_field(adj;units=:power))./sqrt.(p.weight)
        if bath
            lt=reshape(get_temporal_field(adj;z=:all,units=:power),n,:)
            for k in eachindex(op.bath_indices)
                at=vec(@view op.sol.fields[:,:,:,op.bath_indices[k]])
                response=-2 .*imag.(at.*conj.(@view lt[:,k]))./n
                B[(k-1)*n+1:k*n,j].=fft(response).*sqrt.(op.bath_spectrum.*(p.gamma^2/(n*p.grid.dt*1e-12)*op.bath_weight[k]))
            end
        end
        done=Threads.atomic_add!(complete,1)+1
        if done%16==0 || done==columns
            @printf("CORE %s %d/%d %.1fs\n",label,done,columns,time()-started);flush(stdout)
        end
    end
    Threads.@threads :static for j in 1:columns
        fill_one(j)
    end
    vacuum=real.(G'*G);reservoir=real.(B'*B)
    (;A=(vacuum+reservoir)[1:m,1:m],vacuum=vacuum[1:m,1:m],reservoir=reservoir[1:m,1:m],
      V=vacuum+reservoir,Vvac=vacuum,Vbath=reservoir)
end

eigen_record(e) = Dict{String,Any}("values"=>e.values,"residuals"=>e.residuals,
    "iterations"=>e.iterations,"seconds"=>e.seconds,"converged"=>e.converged)

function matrixfree_case(c,out)
    label=c["label"];file=joinpath(out,label);started=time()
    if isfile(file*".toml") && get(TOML.parsefile(file*".toml"),"complete",false)
        return println("REUSE ",label)
    end
    op=make_operator(c);n=op.p.n
    maxiter=Int(get(c,"eig_maxiter",120));tol=get(c,"eig_tol",1e-7)
    active=findall(op.nbar.>maximum(op.nbar)*get(c,"core_relative_power",1e-12))
    padding=Int(get(c,"core_padding_bins",4))
    indices=collect(max(1,first(active)-padding):min(n,last(active)+padding))
    core=selected_amplitude_covariance(op,indices;label,include_phase=get(c,"counting_core",true))
    npzwrite(file*".core.npz",Dict("A"=>core.A,"vacuum"=>core.vacuum,"reservoir"=>core.reservoir,
        "nbar"=>op.nbar[indices],"nbar_full"=>op.nbar,"indices"=>indices.-1,
        "omega_rad_ps"=>frequency_axis(op.p.grid)[indices],"mean_spectral_full"=>vec(get_spectral_field(op.sol)),
        "V"=>core.V,"Vvac"=>core.Vvac,"Vbath"=>core.Vbath))
    python="~/analytical-nl-discovery-data/venv-gpt-a/bin/python"
    run(`$python $(joinpath(@__DIR__,"readout_matrixfree_score.py")) $(file*".core.npz")`)
    scored=npzread(file*".core.score.npz");k=Array(scored["dual_K"])
    mask=vec(scored["mask"]);Fbest=only(scored["best_binary_F"])
    fullmask=zeros(n);fullmask[indices].=mask
    report=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "config"=>c,"method"=>"matrix-free exact discrete RK4IP tangent plus public discrete adjoint",
        "complete"=>false,"core_bins"=>length(indices),"full_bins"=>n,
        "core_omitted_mean_fraction"=>1-sum(op.nbar[indices])/sum(op.nbar),
        "best_binary_F"=>Fbest,"dt_fs"=>op.p.grid.dt*1e3,
        "temporal_edge_fraction"=>sum(abs2.(vec(op.sol.fields[:,:,:,end]))[abs.(op.p.t).>0.45c["window_ps"]])/sum(abs2,op.sol.fields[:,:,:,end]),
        "spectral_edge_fraction"=>sum(op.nbar[abs.(frequency_axis(op.p.grid)).>0.85maximum(abs,frequency_axis(op.p.grid))])/sum(op.nbar))
    kernels=PP._mmgnlse_raman_kernels(op.p.pars)
    report["sampled_raman_integral"]=get(c,"raman",false) ? real(kernels.ha[1]+kernels.hb[1]) : 0.0
    write_report()=open(file*".toml","w") do io;TOML.print(io,report);end
    write_report()
    field=lanczos_lowest(x->covariance_product(op,x),2n;count=2,maxiter,tol,label=label*"_field")
    report["field_eigen"]=eigen_record(field);report["lambda_min"]=field.values[1];write_report()
    amp=lanczos_lowest(x->amplitude_product(op,x),n;count=2,maxiter,tol,label=label*"_amp")
    report["amplitude_eigen"]=eigen_record(amp);report["lambda_gen"]=amp.values[1];write_report()
    g=vcat(zeros(n),sqrt.(op.nbar./sum(op.nbar)))
    function passive_product(x)
        gx=dot(g,x);px=x.-gx.*g
        y=covariance_product(op,px)
        y.-dot(g,y).*g.+(Fbest+1).*gx.*g
    end
    passive=lanczos_lowest(passive_product,2n;count=1,maxiter,tol,label=label*"_passive")
    report["passive_eigen"]=eigen_record(passive);report["lambda_pass"]=passive.values[1]
    report["passive_minimizer_port_photons"]=dot(sqrt.(op.nbar),passive.vectors[1:n,1])^2
    write_report()
    duals=Dict{String,Any}[];bestdual=amp.values[1];bestscale=0.0
    # Scaling a valid nonnegative combination remains a valid combination.
    # These are numerical Ritz estimates, with residuals recorded explicitly.
    for scale in get(c,"dual_scales",[1.0])
        function dual_product(x)
            y=amplitude_product(op,x)
            y[indices].-=scale.*(k*x[indices])
            y
        end
        dual=lanczos_lowest(dual_product,n;count=1,maxiter,tol,label=label*"_dual$(scale)")
        record=eigen_record(dual);record["scale"]=scale;push!(duals,record)
        if dual.values[1]>bestdual
            bestdual=dual.values[1];bestscale=scale
        end
    end
    report["dual_eigen"]=duals;report["moment_bound_ritz"]=bestdual;report["dual_scale"]=bestscale
    report["eigensolver_caveat"]="Ritz values and residuals are numerical convergence evidence, not rigorous global eigenvalue enclosures."
    report["elapsed_seconds"]=time()-started;report["complete"]=true;write_report()
    npzwrite(file*".eigen.npz",Dict("field_vectors"=>field.vectors,"amplitude_vectors"=>amp.vectors,
        "passive_vector"=>passive.vectors,"nbar_full"=>op.nbar,"full_mask"=>fullmask,
        "omega_rad_ps"=>frequency_axis(op.p.grid),"time_ps"=>op.p.t,
        "mean_temporal"=>vec(op.sol.fields[:,:,:,end])))
    @printf("MATRIXFREE DONE %s min=%.8g gen=%.8g binary=%.8g %.1fs\n",label,
        field.values[1],amp.values[1],Fbest,time()-started);flush(stdout)
    GC.gc()
end

function operator_checks(out)
    config=TOML.parsefile(joinpath(@__DIR__,"..","runs","2026-10-10-gpt-a-readout-reference","config-pilot.toml"))
    rows=Dict{String,Any}[]
    for c in config["cases"]
        op=make_operator(c);d=npzread(joinpath(out,c["label"]*".npz"));n=op.p.n
        rng=MersenneTwister(20261010);x=randn(rng,2n);x./=norm(x);y=randn(rng,2n);y./=norm(y)
        vx=covariance_product(op,x);vy=covariance_product(op,y)
        product_error=norm(vx-d["V"]*x)/norm(vx);symmetry=abs(dot(x,vy)-dot(y,vx))
        product_error<2e-9 || error("Matrix-free / dense covariance gate failed")
        symmetry<2e-9 || error("Covariance product symmetry gate failed")
        eig=lanczos_lowest(v->covariance_product(op,v),2n;count=2,maxiter=160,label=c["label"])
        dense=sort(eigvals(Symmetric(d["V"])))
        push!(rows,Dict("label"=>c["label"],"product_relative_error"=>product_error,"symmetry_error"=>symmetry,
            "eigenvalues"=>eig.values,"dense_eigenvalues"=>dense[1:2],"residuals"=>eig.residuals,
            "converged"=>eig.converged,"iterations"=>eig.iterations,"seconds"=>eig.seconds))
        GC.gc()
    end
    open(joinpath(out,"matrixfree-gates.toml"),"w") do io
        TOML.print(io,Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt","checks"=>rows))
    end
end

function fixed_filter_step_audit(out)
    file=joinpath(out,"fixed-filter-step-audit.toml")
    isfile(file) && get(TOML.parsefile(file),"complete",false) && return
    baseline=TOML.parsefile(joinpath(out,"anom_N1_z0.75_R.toml"))["config"]
    dark=Float64.(npzread(joinpath(out,"anom_N1_z0.75_R.bounds.npz"))["best_mask"])
    bright=vec(npzread(joinpath(out,"anom_N1_z0.75_R_mf_base.eigen.npz"))["full_mask"])
    rows=Dict{String,Any}[]
    for steps in (96,192,384,1536,6144,12288,24576)
        c=deepcopy(baseline);c["steps"]=steps
        started=time();op=make_operator(c)
        row=Dict{String,Any}("steps"=>steps,"step_m"=>op.dz)
        for (name,mask) in (("dark",dark),("bright",bright))
            photons=dot(mask,op.nbar);q=sqrt.(op.nbar).*mask./sqrt(photons)
            row[name*"_F"]=dot(q,amplitude_product(op,q))
            row[name*"_coherent_photons"]=photons
        end
        row["seconds"]=time()-started;push!(rows,row)
        open(file,"w") do io
            TOML.print(io,Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
                "config"=>baseline,"fixed_masks_source"=>"baseline formal optimum and pilot bright-core optimum",
                "complete"=>steps==24576,"rows"=>rows))
        end
        @printf("FIXED FILTER steps=%d dark=%.12g bright=%.12g %.1fs\n",steps,row["dark_F"],row["bright_F"],row["seconds"]);flush(stdout)
        op=nothing
        GC.gc()
    end
end

if abspath(PROGRAM_FILE)==@__FILE__
    out=ARGS[1];include(joinpath(out,"raman_bath_spectrum.jl"))
    if length(ARGS)==1
        operator_checks(out)
    else
        config=TOML.parsefile(ARGS[2])
        get(config,"run_operator_gates",true) && operator_checks(out)
        get(config,"fixed_filter_step_audit",false) && fixed_filter_step_audit(out)
        for c in config["cases"]
            matrixfree_case(c,out)
        end
    end
end
