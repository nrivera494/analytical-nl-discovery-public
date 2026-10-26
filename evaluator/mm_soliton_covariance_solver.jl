# agent: gpt-b; model: gpt-6-astra; family: gpt
# T-20261008-gpt-b-01. Unchanged pinned solver, explicit model coefficients.
using PulsePropagation, FFTW, LinearAlgebra, Random, Statistics, NPZ, TOML
const PP = PulsePropagation
BLAS.set_num_threads(1); FFTW.set_num_threads(1)
Threads.nthreads()<=2 || error("At most two Julia threads")

# The abstract Raman type is the solver's extension point. This evaluator
# specifies analytic Fourier kernels and no shock/damping for the stated model.
struct CovarianceResponse <: PP.AbstractRamanResponse
    fraction::Float64
    t0::Float64
end
function PP._mmgnlse_raman_kernels(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:CovarianceResponse}
    nt=p.domain.time_grid.nt; r=p.raman
    iszero(r.fraction) && return (ha=ComplexF64[],hb=ComplexF64[],fraction=0.)
    w=PP._mmgnlse_raw_omega(p)./r.t0; aa=1/.032;bb=1/.0122
    ha=(aa^2+bb^2)./((aa .- im.*w).^2 .+ bb^2)
    iseven(nt) && (ha[nt÷2+1]=real(ha[nt÷2+1]))
    (;ha=ComplexF64.(ha),hb=zeros(ComplexF64,nt),fraction=r.fraction)
end
function PP._mmgnlse_solver_cache(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:CovarianceResponse}
    nt,nm,np=PP._mmgnlse_public_shape(p);omega=PP._mmgnlse_raw_omega(p)
    beta_operator=PP._mmgnlse_beta_array(p.beta,nt,nm,np,omega)
    nonlinear_prefactor=fill(1im*p.n2*p.omega0/2.99792458e-4,nt,1,1)
    nonlinear_active=any(!iszero,nonlinear_prefactor) && !PP._mmgnlse_overlap_iszero(p.S)
    (;omega,beta_operator,nonlinear_prefactor,nonlinear_active,raman=PP._mmgnlse_raman_kernels(p))
end

function xpm_tensor(C)
    nm=size(C,1);S=zeros(nm,nm,nm,nm)
    for m in 1:nm,n in 1:nm
        if m==n
            S[m,m,m,m]=C[m,m]
        else
            S[m,m,n,n]=C[m,n]/2
            S[m,n,m,n]=C[m,n]/2
        end
    end
    S
end

function exact_sparse_cp(S)
    inds=findall(x->abs(x)>1e-12,S);nm=size(S,1);nr=length(inds)
    U=ntuple(_->zeros(nm,nr),4);weights=zeros(nr)
    for (j,idx) in enumerate(inds)
        weights[j]=S[idx]
        for d in 1:4;U[d][idx[d],j]=1.;end
    end
    MMGNLSECPDecomposition(weights,U;layout=:spatial,nmodes=nm,npolarizations=1,relative_error=1e-12)
end

function run_adjoint(profile,out;zeta=4.,dz=.01,zspacing=.05,raman=false)
    data=npzread(profile);mkpath(out);started=time()
    t=vec(data["t"]);nt=length(t);dt=t[2]-t[1];nm=2
    f=data["f"];b=vec(data["b"]);d=vec(data["d"]);lam=vec(data["lam"])
    grid=TimeGrid(nt,nt*dt);domain=MMGNLSEDomain(degrees_of_freedom(:time,:space),grid)
    @assert maximum(abs.(time_axis(grid).-t))<1e-12
    beta=zeros(3,nm);beta[2,:].=d;beta[3,:].=-b
    w0=1215.2590756831312
    pars=MMGNLSEParameters(domain;length=zeta,beta=TaylorBeta(beta),S=xpm_tensor(data["C"]),
        n2=2.99792458e-4/w0,omega0=w0,raman=CovarianceResponse(raman ? .18 : 0.,Float64(get(data,"t0",.5))))
    gauge=exp.(-im .* t .* transpose(d ./ b));rate=lam .+ d.^2 ./ (2b)
    initial=reshape(f.*gauge,nt,nm,1)
    sol=solve_mmgnlse(initial,pars,dz;method=RK4IP(),saveat=zspacing)
    expected=initial.*reshape(exp.(im.*rate*zeta),1,nm,1)
    err=norm(sol.fields[:,:,:,end]-expected)/norm(initial)
    energy=dropdims(sum(abs2,sol.fields;dims=1);dims=(1,3)).*dt
    readout=data["readout"];base=data["g"]
    gy=reshape(reshape(base,nt*nm,6)*transpose(readout),nt,nm,6)
    adjoints=zeros(ComplexF64,nt,nm,length(sol.z),6)
    initial_gradient_error=zeros(6)
    AY=readout*data["A"]/readout
    for j in 1:6
        gt=gy[:,:,j].*gauge.*transpose(exp.(im.*rate*zeta))
        terminal=reshape(nt*dt.*fftshift(ifft(gt,1),1),nt,nm,1)
        adj=solve_adjoint(terminal,pars,dz;forward_solution=sol,units=:power,
            saveat=zspacing,adjoint_mode=:discrete_rk4ip,checkpoint_stride=25)
        @assert maximum(abs.(adj.z.-sol.z))<1e-12
        adjoints[:,:,:,j].=reshape(get_temporal_field(adj;z=:all),nt,nm,length(adj.z))./(nt*dt)
        analytic=reshape(reshape(gy,nt*nm,6)*vec((I+zeta*AY)[j,:]),nt,nm).*gauge
        initial_gradient_error[j]=norm(adjoints[:,:,1,j]-analytic)/norm(analytic)
        println("ADJOINT ",basename(profile)," ",j," ",time()-started);flush(stdout)
    end
    # One directional finite difference independently checks pairing/FFT scaling.
    rng=MersenneTwister(2026100801);v=randn(rng,ComplexF64,size(initial));v./=norm(v)
    h=2e-5; terminalg=gy[:,:,3].*gauge.*transpose(exp.(im.*rate*zeta))
    objective(a)=dt*real(sum(conj.(terminalg).*reshape(solve_mmgnlse(a,pars,dz;method=RK4IP()).fields[:,:,:,end],nt,nm)))
    fd=(objective(initial.+h.*v)-objective(initial.-h.*v))/(2h)
    pred=dt*real(sum(conj.(adjoints[:,:,1,3]).*reshape(v,nt,nm)))
    label=splitext(basename(profile))[1]*"_"*(raman ? "raman" : "kerr")*"_h"*string(dz)
    npzwrite(joinpath(out,label*".npz"),Dict("z"=>sol.z,"t"=>t,"fields"=>sol.fields,
        "adjoints"=>adjoints,"expected_final"=>expected,"energy"=>energy))
    summary=Dict("agent"=>"gpt-b","model"=>"gpt-6-astra","family"=>"gpt",
        "profile"=>profile,"zeta"=>zeta,"dzeta"=>dz,"zspacing"=>zspacing,"raman_mean"=>raman,
        "mean_stationarity_relative"=>err,"modal_energy_relative_change"=>vec(energy[:,end]./energy[:,1].-1),
        "initial_dual_relative_errors"=>initial_gradient_error,
        "directional_fd"=>fd,"directional_adjoint"=>pred,"directional_relative_error"=>abs(fd-pred)/abs(fd),
        "elapsed_seconds"=>time()-started)
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,summary);end
    TOML.print(stdout,summary);flush(stdout)
end

function gain_calibration(out;ntraj=8192)
    mkpath(out);rng=MersenneTwister(2026100802);nt=16;dt=.25;g=.7;L=1.;h=.125;f0=193.4
    sim=PP.Simulation{Float64}(lambda0=1.55e-6,f0=f0,dz=h,include_Raman=false,pulse_centering=false)
    fiber=PP.Fiber{Float64}(betas=zeros(3,1),sr=ones(1,1,1,1),L0=L,n2=0.,fr=0.)
    weights=PP.photon_bin_weights(nt,dt,f0;shifted=false);nphot=1e6
    meanw=zeros(ComplexF64,nt,1);meanw[1]=sqrt(nphot/weights[1]);G=exp(g*L)
    rows=Dict{String,Any}[]
    for inputnoise in (false,true)
        ens=inputnoise ? PP.photon_vacuum_ensemble(meanw,dt,f0,ntraj;rng,noise_scale=.5) : repeat(meanw,1,1,ntraj)
        st=PP.stochastic_solve(fiber,ens,dt,sim;zsave=collect(0:h:L),rng,
            linear_gain=g,linear_gain_noise=true,gain_noise_scale=.5,deterministic_stepper=:rk4ip)
        finalw=ifft(st.fields[:,:,end,:],1)
        delta=vec(finalw[1,1,:]).*sqrt(weights[1]).-sqrt(G*nphot)
        added=2sqrt(G*nphot).*real.(delta)
        target=nphot*(inputnoise ? (2G^2-G) : G*(G-1))
        push!(rows,Dict("input_noise"=>inputnoise,"measured_linear_energy_variance"=>var(added),
            "analytic_variance"=>target,"ratio"=>var(added)/target,"ntraj"=>ntraj,
            "relative_sampling_se"=>sqrt(2/(ntraj-1)),"mean_quadrature"=>mean(real.(delta))))
        npzwrite(joinpath(out,inputnoise ? "gain_total.npz" : "gain_added.npz"),Dict("delta_B"=>delta))
    end
    result=Dict("agent"=>"gpt-b","model"=>"gpt-6-astra","family"=>"gpt",
        "gain_intensity_rate"=>g,"length"=>L,"nsp"=>1.,"gain_power"=>G,"input_photons"=>nphot,
        "rows"=>rows,"seed"=>2026100802,"noise_scale"=>.5)
    open(joinpath(out,"gain.toml"),"w") do io;TOML.print(io,result);end
    TOML.print(stdout,result)
end

function run_relaxed(profile,material,out;pair="grin02",zeta=4.,dz=.002,zspacing=.05,raman=false,adjoint=true,cp=true,
        actual_observables=false)
    data=npzread(profile);mat=npzread(material);mkpath(out);started=time()
    t=vec(data["t"]);nt=length(t);dt=t[2]-t[1];t0=.5
    S=copy(mat["S"]);S./=S[1,1,1,1];beta=mat["beta"]
    nm=size(S,1);selected=pair=="grin11" ? [1,3] : [1,2]
    groups=haskey(mat,"groups") ? Int.(vec(mat["groups"])) : (startswith(pair,"grin") ? [0,2,1,4,2,1] : [0,1,1])
    for a in 1:nm,b in 1:nm,c in 1:nm,d in 1:nm
        groups[b]+groups[c]==groups[a]+groups[d] || (S[a,b,c,d]=0.)
    end
    ld=t0^2/abs(beta[3,1]);b=vec(beta[3,:]./beta[3,1]);d=vec((beta[2,:].-beta[2,1]).*ld./t0)
    gap=startswith(pair,"grin") ? beta[1,3]-beta[1,1] : beta[1,2]-beta[1,1]
    beta0=vec((beta[1,:].-beta[1,1].-gap.*groups).*ld)
    bsim=vcat(transpose(beta0),transpose(d),transpose(-b))
    grid=TimeGrid(nt,nt*dt);domain=MMGNLSEDomain(degrees_of_freedom(:time,:space),grid)
    w0=1215.2590756831312
    overlap=cp ? exact_sparse_cp(S) : S
    pars=MMGNLSEParameters(domain;length=zeta,beta=TaylorBeta(bsim),S=overlap,
        n2=2.99792458e-4/w0,omega0=w0,raman=CovarianceResponse(raman ? .18 : 0.,t0))
    f=zeros(nt,nm);f[:,selected].=data["f"]
    gauge=exp.(-im .* t .* transpose(d ./ b))
    rate=beta0 .+ d.^2 ./ (2b);rate[selected].+=vec(data["lam"])
    initial=reshape(f.*gauge,nt,nm,1)
    sol=solve_mmgnlse(initial,pars,dz;method=RK4IP(),saveat=zspacing)
    energy=dropdims(sum(abs2,sol.fields;dims=1);dims=(1,3)).*dt
    shape_error=Float64[];phase_error=Vector{Float64}[];timing=Float64[]
    for (j,z) in enumerate(sol.z)
        actual=reshape(sol.fields[:,:,:,j],nt,nm)
        target=f.*gauge.*transpose(exp.(im.*rate*z))
        ph=[angle(dot(target[:,m],actual[:,m])) for m in selected]
        target[:,selected].*=transpose(exp.(im.*ph))
        push!(shape_error,norm(actual-target)/norm(initial))
        push!(phase_error,ph)
        push!(timing,dt*sum(t.*vec(sum(abs2,actual;dims=2)))/sum(energy[:,j]))
    end
    gy=zeros(ComplexF64,nt,nm,6)
    gy[:,selected,:].=reshape(reshape(data["g"],nt*2,6)*transpose(data["readout"]),nt,2,6)
    adjoints=zeros(ComplexF64,nt,nm,length(sol.z),adjoint ? 6 : 0)
    terminal=gy.*reshape(gauge,nt,nm,1).*reshape(exp.(im.*rate*zeta),1,nm,1)
    if actual_observables
        # Exact gradients of total norm, weighted centroid, spectral centroid,
        # and occupied-mode fraction at the actual propagated mean. The two
        # phase channels remain the declared nominal adjoint homodyne readouts.
        u=reshape(sol.fields[:,:,:,end],nt,nm);E=sum(energy[:,end])
        mass=sum(energy[:,end]./b)
        Tw=dt*sum(t.*vec(sum(abs2.(u)./transpose(b);dims=2)))/mass
        kk=2pi.*FFTW.fftfreq(nt,1/dt)
        up=ifft(im.*kk.*fft(u,1),1)
        V=dt*imag(sum(conj.(u).*up))/E
        fraction=energy[selected[2],end]/E
        terminal[:,:,1].=2u
        terminal[:,:,3].=2 .* (t.-Tw).*u./transpose(b.*mass)
        terminal[:,:,4].=(-2im.*up.-2V.*u)./E
        weights=fill(-fraction,nm);weights[selected[2]]+=1
        terminal[:,:,5].=2u.*transpose(weights)./E
    end
    if adjoint
        for j in 1:6
            terminal_spectrum=reshape(nt*dt.*fftshift(ifft(terminal[:,:,j],1),1),nt,nm,1)
            adj=solve_adjoint(terminal_spectrum,pars,dz;forward_solution=sol,units=:power,
                saveat=zspacing,adjoint_mode=:discrete_rk4ip,checkpoint_stride=50)
            adjoints[:,:,:,j].=reshape(get_temporal_field(adj;z=:all),nt,nm,length(adj.z))./(nt*dt)
            println("RELAXED ADJOINT ",pair," ",j," ",time()-started);flush(stdout)
        end
    end
    label=pair*"_"*(raman ? "raman" : "kerr")*"_h"*string(dz)*"_M"*string(nm)*(cp ? "_cp" : "")*(actual_observables ? "_actual" : "")
    npzwrite(joinpath(out,label*".npz"),Dict("z"=>sol.z,"t"=>t,"fields"=>sol.fields,
        "adjoints"=>adjoints,"energy"=>energy,"S"=>mat["S"]./mat["S"][1,1,1,1],
        "groups"=>groups,"selected"=>selected,"beta"=>bsim))
    empty=setdiff(collect(1:nm),selected)
    summary=Dict("agent"=>"gpt-b","model"=>"gpt-6-astra","family"=>"gpt",
        "profile"=>profile,"material"=>material,"pair"=>pair,"nm"=>nm,"zeta"=>zeta,
        "dzeta"=>dz,"zspacing"=>zspacing,"raman_mean"=>raman,"group_resonant_tensor"=>true,
        "actual_energy_centroid_frequency_fraction_gradients"=>actual_observables,
        "phase_readout"=>"Fixed nominal adjoint homodyne quadrature",
        "overlap_backend"=>cp ? "exact sparse-term CP" : "dense", "cp_entry_drop_tolerance"=>cp ? 1e-12 : 0.,
        "shape_error_final"=>last(shape_error),"shape_error_max"=>maximum(shape_error),
        "phase_errors_final"=>last(phase_error),"centroid_final"=>last(timing),
        "empty_mode_energy_fraction_max"=>maximum(vec(sum(energy[empty,:];dims=1)))./sum(energy[:,1]),
        "occupied_modal_energy_relative_changes"=>vec(energy[selected,end]./energy[selected,1].-1),
        "dispersion_ratio"=>b,"walkoff"=>d,"beta0_residual"=>beta0,"elapsed_seconds"=>time()-started)
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,summary);end
    TOML.print(stdout,summary);flush(stdout)
end

if abspath(PROGRAM_FILE)==@__FILE__
    mode=ARGS[1]
    if mode=="gain"
        gain_calibration(ARGS[2])
    elseif mode=="adjoint"
        run_adjoint(ARGS[2],ARGS[3];dz=length(ARGS)>3 ? parse(Float64,ARGS[4]) : .01,
            raman=length(ARGS)>4 && ARGS[5]=="raman",zeta=length(ARGS)>5 ? parse(Float64,ARGS[6]) : 4.)
    elseif mode in ("relaxed","actual_relaxed")
        run_relaxed(ARGS[2],ARGS[3],ARGS[4];pair=ARGS[5],dz=length(ARGS)>5 ? parse(Float64,ARGS[6]) : .002,
            raman=length(ARGS)>6 && ARGS[7]=="raman",actual_observables=mode=="actual_relaxed")
    elseif mode=="core_suite"
        profiles=ARGS[2];out=ARGS[3]
        for z in (.5,1.,2.,4.)
            run_adjoint(joinpath(profiles,"grin02_p0.2_equalb.npz"),joinpath(out,"growth_z"*string(z));
                zeta=z,dz=.02,zspacing=.1)
        end
        for dz in (.04,.01)
            run_adjoint(joinpath(profiles,"grin02_p0.2_equalb.npz"),joinpath(out,"convergence_h"*string(dz));
                zeta=4.,dz,zspacing=5dz)
        end
        for pair in ("grin11","step11")
            run_adjoint(joinpath(profiles,pair*"_p0.2_physical.npz"),out;zeta=4.,dz=.01,zspacing=.05)
        end
    elseif mode=="qualification_suite"
        profiles=ARGS[2];material=ARGS[3];out=ARGS[4]
        run_relaxed(joinpath(profiles,"step11_p0.2_physical.npz"),joinpath(material,"step_257.npz"),out;pair="step11",dz=.002)
        for pair in ("grin02","grin11","step11")
            mat=startswith(pair,"grin") ? "grin_257.npz" : "step_257.npz"
            run_relaxed(joinpath(profiles,pair*"_p0.2_physical.npz"),joinpath(material,mat),out;pair,dz=.002,raman=true)
        end
        run_relaxed(joinpath(profiles,"grin02_p0.2_physical.npz"),joinpath(material,"grin_257.npz"),out;pair="grin02",dz=.001)
    elseif mode=="extension_suite"
        profiles=ARGS[2];material=ARGS[3];out=ARGS[4]
        for pair in ("grin02","grin11")
            run_relaxed(joinpath(profiles,pair*"_p0.2_physical.npz"),joinpath(material,"extended","grin_257.npz"),out;pair,dz=.002)
        end
        for pair in ("grin02","grin11","step11")
            mat=startswith(pair,"grin") ? "grin_257.npz" : "step_257.npz"
            run_relaxed(joinpath(profiles,pair*"_p0.2_physical.npz"),joinpath(material,mat),out;pair,dz=.002,raman=true,actual_observables=true)
        end
    else
        error("Unknown mode")
    end
end
