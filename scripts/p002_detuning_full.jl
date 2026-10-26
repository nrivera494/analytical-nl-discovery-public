# agent: gpt-a; model: gpt-6-astra; family: gpt
# Supplemental held-out detuning check of the zero-walk-off spectral corollary.
include(joinpath(@__DIR__,"p002_common.jl"))
out=ARGS[1];mkpath(out)
for (j,mu) in enumerate((-.7,-7.,-47.)),r in (.0002,.0006,.002)
    label="mu$(j)_r$(r)";p=setup(;r,delta=0.,nm=3,nt=4096,window=320.,zeta=17.)
    beta=copy(p.beta);beta[1,3]=mu/LD
    pars=MMGNLSEParameters(p.pars.domain;length=17LD,beta=TaylorBeta(beta),
        S=p.S,n2=MAT["n2_m2_W"],omega0=W0,raman=Round1Response(NoRaman()))
    dz=abs(mu)>20 ? .0025 : .005;zs=[0.,5.,11.,17.]
    elapsed=@elapsed sol=solve_mmgnlse(p.a,pars,dz*LD;saveat=zs.*LD)
    rows=Dict{String,Any}[]
    for (k,z) in enumerate(sol.z)
        row=fieldstats(sol.fields[:,:,:,k],p);row["zeta"]=z/LD;push!(rows,row)
    end
    info=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "label"=>label,"mu"=>mu,"r"=>r,"nt"=>4096,"window_tau"=>320.,
        "dzeta"=>dz,"elapsed_seconds"=>elapsed,"rows"=>rows)
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,info);end
    npzwrite(joinpath(out,label*".npz"),Dict("tau"=>p.tau,"zeta"=>sol.z./LD,"fields"=>sol.fields))
    @printf("DETUNING %s K=%.9g seconds=%.2f\n",label,last(rows)["energies"][3]/r^2,elapsed);flush(stdout)
    GC.gc()
end
