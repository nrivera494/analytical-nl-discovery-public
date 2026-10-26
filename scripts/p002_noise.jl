# agent: gpt-a; model: gpt-6-astra; family: gpt
# Coherent-input linearized photon-count covariance, including the matched
# symmetric 300 K Raman reservoir. Constant photon weight matches no shock.
include(joinpath(@__DIR__,"p002_common.jl"))

function bath_spectrum(p;temperature=300.)
    p.response=="none" && return zeros(p.nt)
    kernels=PP._mmgnlse_raman_kernels(p.pars)
    h=kernels.fraction.*(kernels.ha.+kernels.hb)
    omega=PP._mmgnlse_raw_omega(p.pars).*1e12
    kb=1.380649e-23
    C=[iszero(w) ? 0. : HBAR*W0*1e12/KAPPA*abs(imag(h[j]))/tanh(HBAR*abs(w)/(2kb*temperature)) for (j,w) in enumerate(omega)]
    rr=p.pars.raman.base
    slope=rr.fraction*2rr.tau1^2*rr.tau2/(rr.tau1^2+rr.tau2^2)
    rr isa AnisotropicRaman && (slope*=rr.fa+rr.fc)
    C[1]=2W0*kb*temperature*slope/KAPPA
    C
end

function noise_case(out,label;r=.01,delta=0.,response="none",nt=4096,window=320.,dz=.01,zspacing=.2,zeta=20.)
    p=setup(;r,delta,response,nt,window,zeta)
    started=time()
    sol=solve_mmgnlse(p.a,p.pars,dz*LD;saveat=zspacing*LD)
    aw=reshape(get_spectral_field(sol),nt,p.nm)
    weight=nt*p.grid.dt*1e-12/(HBAR*W0*1e12)
    omega=frequency_axis(p.grid).*T0
    masks=[Float64.(abs.(omega).<=1),Float64.(omega.>=0),ones(nt)]
    labels=["band_01","band_02","edge_01","edge_02","all_01","all_02","total"]
    channels=[(1,1),(1,2),(2,1),(2,2),(3,1),(3,2),(3,0)]
    nobs=length(channels)
    means=zeros(nobs);gradients=zeros(ComplexF64,nt*p.nm,nobs)
    pairs=[(m,n) for n in 1:p.nm for m in 1:p.nm]
    G=[n-m==q-v ? ARR["S"][m,n,v,q] : 0. for (m,n) in pairs,(v,q) in pairs]
    ge=eigen(Symmetric(G));groot=ge.vectors*Diagonal(sqrt.(max.(ge.values,0.)))
    C=bath_spectrum(p);nz=length(sol.z)
    zw=zeros(nz);zw[1:end-1].+=diff(sol.z)./2;zw[2:end].+=diff(sol.z)./2
    at=reshape(sol.fields,nt,p.nm,nz)
    # Store reservoir vectors on disk and accumulate one channel at a time.
    # nt*4*nz*7 ComplexF64 is modest at the prescribed grid.
    reservoir=response=="none" ? zeros(ComplexF64,0,nobs) : zeros(ComplexF64,nt*p.nm^2*nz,nobs)
    # At most two Julia worker threads; each adjoint has its own replay cache.
    # Columns are independent and written by exactly one worker.
    Threads.nthreads()<=2 || error("This task permits at most two Julia threads")
    Threads.@threads :static for j in eachindex(channels)
        fi,mi=channels[j]
        mask=zeros(nt,p.nm)
        mi==0 ? (mask.=masks[fi]) : (mask[:,mi].=masks[fi])
        means[j]=weight*sum(mask.*abs2.(aw))
        terminal=reshape(weight.*mask.*aw./sqrt(means[j]),nt,p.nm,1)
        adj=solve_adjoint(terminal,p.pars,dz*LD;forward_solution=sol,units=:power,
            saveat=zspacing*LD,adjoint_mode=:discrete_rk4ip,checkpoint_stride=20)
        gradients[:,j].=vec(get_spectral_field(adj;units=:power))./sqrt(weight)
        if response!="none"
            @assert maximum(abs.(adj.z.-sol.z))<1e-9
            lt=reshape(get_temporal_field(adj;z=:all,units=:power),nt,p.nm,nz)
            B=zeros(ComplexF64,nt,p.nm^2)
            for iz in 1:nz
                for (a,(m,n)) in enumerate(pairs)
                    B[:,a].=im.*(conj.(lt[:,m,iz]).*at[:,n,iz].-lt[:,n,iz].*conj.(at[:,m,iz]))./nt
                end
                Bw=fft(B,1)*groot
                weights=sqrt.(C.*(KAPPA^2/(nt*p.grid.dt)*1e12*zw[iz]))
                reservoir[(iz-1)*nt*p.nm^2+1:iz*nt*p.nm^2,j].=vec(Bw.*weights)
            end
        end
        @printf("ADJOINT %s %s %.1fs\n",label,labels[j],time()-started);flush(stdout)
    end
    optical=real.(gradients'*gradients);bath=real.(reservoir'*reservoir);Q=optical+bath
    rows=Dict{String,Any}[]
    for (f,i,j) in (("band",1,2),("edge",3,4),("all",5,6))
        push!(rows,Dict("filter"=>f,"F01"=>Q[i,i],"F02"=>Q[j,j],"rho"=>Q[i,j]/sqrt(Q[i,i]*Q[j,j]),
           "F01_optical"=>optical[i,i],"F02_optical"=>optical[j,j],"cov_optical_normalized"=>optical[i,j],
           "F01_Raman"=>bath[i,i],"F02_Raman"=>bath[j,j],"cov_Raman_normalized"=>bath[i,j],
           "mean_photons_01"=>means[i],"mean_photons_02"=>means[j]))
    end
    d=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt","label"=>label,
        "r"=>r,"delta"=>delta,"response"=>response,"nt"=>nt,"window_tau"=>window,
        "dzeta"=>dz,"zspacing"=>zspacing,"zeta"=>zeta,"rows"=>rows,"elapsed_seconds"=>time()-started,
        "total_count_F"=>Q[7,7],"total_count_Raman_F"=>bath[7,7],
        "min_optical_covariance_eigenvalue"=>minimum(eigvals(Symmetric(optical))),
        "min_Raman_covariance_eigenvalue"=>minimum(eigvals(Symmetric(bath))),
        "min_pair_Gram_eigenvalue"=>minimum(ge.values),"carrier_photon_weight"=>weight,
        "mean_diagnostics"=>fieldstats(sol.fields[:,:,:,end],p))
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,d);end
    npzwrite(joinpath(out,label*".npz"),Dict("tau"=>p.tau,"zeta"=>sol.z./LD,"fields"=>sol.fields,
        "optical_covariance"=>optical,"Raman_covariance"=>bath,"input_gradients"=>gradients,
        "mean_photons"=>means,"bath_spectrum"=>C))
    @printf("NOISE %s F2band=%.8g rho=%.8g total=%.9g seconds=%.1f\n",label,Q[2,2],Q[1,2]/sqrt(Q[1,1]*Q[2,2]),Q[7,7],time()-started);flush(stdout)
    GC.gc();d
end

if abspath(PROGRAM_FILE)==@__FILE__
    out=ARGS[1];mode=length(ARGS)>1 ? ARGS[2] : "main";mkpath(out)
    if mode in ("main","main_resume")
        for response in ("none","agarwal","anisotropic"), (j,d) in enumerate((0.,MAT["delta_physical"])), r in (.003,.01,.03)
            label="$(response)_d$(j)_r$(r)"
            if mode=="main_resume" && isfile(joinpath(out,label*".toml")) && isfile(joinpath(out,label*".npz"))
                npzread(joinpath(out,label*".npz")) # refuse a corrupt/incomplete checkpoint
                println("REUSE_COMPLETE ",label);flush(stdout)
            else
                noise_case(out,label;r,delta=d,response)
            end
        end
    elseif mode=="convergence"
        for response in ("none","agarwal","anisotropic")
            noise_case(out,"$(response)_halfstep";r=.003,delta=MAT["delta_physical"],response,dz=.005,zspacing=.1)
            noise_case(out,"$(response)_doublewindow";r=.003,delta=MAT["delta_physical"],response,window=640.,nt=8192)
            noise_case(out,"$(response)_resolution";r=.003,delta=MAT["delta_physical"],response,nt=8192)
        end
    elseif mode=="small"
        for response in ("none","agarwal","anisotropic"),(j,d) in enumerate((0.,MAT["delta_physical"])),r in (.0001,)
            noise_case(out,"$(response)_d$(j)_r$(r)";r,delta=d,response)
        end
    else
        error("Unknown mode $mode")
    end
end
