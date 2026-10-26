# agent: gpt-a; model: gpt-6-astra; family: gpt
# Full finite-admixture comparisons, separate from the response evaluator.
include(joinpath(@__DIR__,"p002_common.jl"))

function next_parameters(delta=0.;kind="ideal")
    q=Dict("delta"=>Float64(delta),"delta3"=>2delta,"b2"=>1.,"b3"=>1.,"mu"=>0.,
        "sigma"=>1.,"sigma13"=>.75,"kappa"=>.25,"alpha2"=>.5)
    if kind=="perturbed"
        merge!(q,Dict("delta3"=>2.1delta,"b2"=>1.015,"b3"=>1.03,"mu"=>-10.,"sigma"=>.98))
    elseif kind=="physical"
        b=ARR["beta"]
        merge!(q,Dict("delta"=>MAT["delta_physical"],"delta3"=>(b[2,3]-b[2,1])*T0/abs(b[3,1]),
            "b2"=>b[3,2]/b[3,1],"b3"=>b[3,3]/b[3,1],"mu"=>(b[1,3]-2b[1,2]+b[1,1])*LD))
    elseif kind!="ideal"
        error("Unknown condition")
    end
    q
end

function next_full(out,label,q;r=.002,nm=3,nt=4096,window=320.,dz=.005,
        zs=[0.,7.,13.,19.],phase=0.,third=0.,thirdphase=0.,resume=false)
    if resume && isfile(joinpath(out,label*".toml")) && isfile(joinpath(out,label*".npz"))
        println("Retained completed case ",label);flush(stdout)
        return TOML.parsefile(joinpath(out,label*".toml"))
    end
    phase=Float64(phase);thirdphase=Float64(thirdphase)
    p=setup(;r,delta=q["delta"],nm,nt,window,zeta=last(zs),phase,third,thirdphase)
    S=copy(p.S);beta=copy(p.beta)
    for a in 1:nm,b in 1:nm,c in 1:nm,d in 1:nm
        if sort([a,b,c,d])==[1,1,2,2] && b+c==a+d
            S[a,b,c,d]=q["sigma"]*S[1,1,1,1]/2
        end
    end
    beta[2,2]=q["delta"]*T0/LD;beta[2,3]=q["delta3"]*T0/LD
    beta[3,2]=beta[3,1]*q["b2"];beta[3,3]=beta[3,1]*q["b3"]
    beta[1,3]=q["mu"]/LD
    pars=MMGNLSEParameters(p.pars.domain;length=last(zs)*LD,beta=TaylorBeta(beta),
        S,n2=MAT["n2_m2_W"],omega0=W0,raman=Round1Response(NoRaman()))
    p=merge(p,(;pars,S,beta))
    elapsed=@elapsed sol=solve_mmgnlse(p.a,pars,dz*LD;saveat=zs.*LD)
    nu=(sqrt(1+8q["sigma"]/q["b2"])-1)/2
    psi=exp.(-im*q["delta"].*p.tau./q["b2"])./cosh.(p.tau).^nu
    dt=p.grid.dt/T0;psi./=sqrt(sum(abs2,psi)*dt)
    rows=Dict{String,Any}[]
    for (j,z) in enumerate(sol.z)
        aa=sol.fields[:,:,:,j];de=fieldstats(aa,p);de["zeta"]=z/LD
        de["reference_projection"]=abs2(dot(psi,aa[:,2,1]./sqrt(P0))*dt)/(2r)
        push!(rows,de)
    end
    info=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt","label"=>label,
        "parameters"=>q,"r"=>r,"p2_total"=>r/(1+r+third),"nm"=>nm,"nt"=>nt,
        "window_tau"=>window,"dzeta"=>dz,"phase02"=>phase,"third_ratio"=>third,
        "phase03"=>thirdphase,"elapsed_seconds"=>elapsed,"rows"=>rows)
    mkpath(out)
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,info);end
    npzwrite(joinpath(out,label*".npz"),Dict("tau"=>p.tau,"zeta"=>sol.z./LD,"fields"=>sol.fields))
    @printf("NEXT %s r=%.5g B=%.10g seconds=%.2f\n",label,r,last(rows)["reference_projection"],elapsed);flush(stdout)
    GC.gc();info
end

if abspath(PROGRAM_FILE)==@__FILE__
out=ARGS[1];mode=ARGS[2]
if mode=="main"
    cases=[("ideal_d$j",next_parameters(d)) for (j,d) in enumerate((0.,.35,.85,1.35))]
    append!(cases,[("perturbed",next_parameters(.85;kind="perturbed")),("physical",next_parameters(;kind="physical"))])
    for (label,q) in cases,r in (.0002,.0006,.002)
        next_full(out,"$(label)_r$(r)",q;r,dz=label=="physical" ? .0025 : .005)
    end
elseif mode=="boundary"
    frozen=TOML.parsefile(joinpath(@__DIR__,"..","runs","2026-10-04-gpt-a-nextorder-prediction","boundary.toml"))
    for r in (.0002,.0006,.002)
        delta=frozen["delta_half_zeroth"]+r*frozen["delta_half_slope_r"]
        next_full(out,"half_r$(r)",next_parameters(delta);r,zs=[0.,13.])
    end
elseif mode=="convergence"
    q=next_parameters(.85)
    next_full(out,"halfstep",q;dz=.0025)
    next_full(out,"doublewindow",q;nt=8192,window=640.)
    next_full(out,"resolution",q;nt=8192)
    next_full(out,"four_modes",q;nm=4)
    next_full(out,"physical_halfstep",next_parameters(;kind="physical");dz=.00125)
elseif mode in ("phase","phase-resume")
    q=next_parameters(.85)
    resume=mode=="phase-resume"
    for (j,phase) in enumerate((0.,pi/2,pi,3pi/2))
        next_full(out,"null_p$j",q;r=.01,phase,resume,zs=[0.,1.,7.,13.])
        for r in (.003,.01)
            next_full(out,"seed_r$(r)_p$j",q;r,third=r^2,thirdphase=phase,resume,zs=[0.,.05,1.,7.,13.])
        end
    end
    for (label,qq) in (("ideal",q),("physical",next_parameters(;kind="physical"))),(j,phase) in enumerate((pi/2,3pi/2))
        next_full(out,"flux_$(label)_p$j",qq;r=.01,third=.01^2,thirdphase=phase,
            resume,dz=.00005,zs=[0.,.0005,.001,.002,.004])
    end
else
    error("Unknown mode $mode")
end
end
