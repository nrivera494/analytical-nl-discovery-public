# agent: gpt-b; model: gpt-6-astra; family: gpt
# Exact ordinary-centroid readout versus the closed collective timing mode.
# This is a deterministic adjoint calculation, not stochastic propagation.
include("mm_soliton_covariance_solver.jl")

function timing_check(profile,out;dz=.01,zeta=4.,zspacing=.05)
    data=npzread(profile);mkpath(out);started=time()
    t=vec(data["t"]);nt=length(t);dt=t[2]-t[1];nm=2
    f=data["f"];b=vec(data["b"]);d=vec(data["d"]);lam=vec(data["lam"])
    domain=MMGNLSEDomain(degrees_of_freedom(:time,:space),TimeGrid(nt,nt*dt))
    beta=zeros(3,nm);beta[2,:].=d;beta[3,:].=-b;w0=1215.2590756831312
    pars=MMGNLSEParameters(domain;length=zeta,beta=TaylorBeta(beta),S=xpm_tensor(data["C"]),
        n2=2.99792458e-4/w0,omega0=w0,raman=CovarianceResponse(0.,.5))
    gauge=exp.(-im .* t .* transpose(d ./ b));rate=lam .+ d.^2 ./ (2b)
    initial=reshape(f.*gauge,nt,nm,1)
    sol=solve_mmgnlse(initial,pars,dz;method=RK4IP(),saveat=zspacing)
    gy=zeros(ComplexF64,nt,nm,7)
    gy[:,:,1:6].=reshape(reshape(data["g"],nt*nm,6)*transpose(data["readout"]),nt,nm,6)
    gy[:,:,7].=2 .* t .* f ./sum(data["N"])
    adjoints=zeros(ComplexF64,nt,nm,length(sol.z),7)
    for j in 1:7
        gt=gy[:,:,j].*gauge.*transpose(exp.(im.*rate*zeta))
        terminal=reshape(nt*dt.*fftshift(ifft(gt,1),1),nt,nm,1)
        adj=solve_adjoint(terminal,pars,dz;forward_solution=sol,units=:power,
            saveat=zspacing,adjoint_mode=:discrete_rk4ip,checkpoint_stride=25)
        adjoints[:,:,:,j].=reshape(get_temporal_field(adj;z=:all),nt,nm,length(adj.z))./(nt*dt)
    end
    label=splitext(basename(profile))[1]*"_ordinary_timing"
    npzwrite(joinpath(out,label*".npz"),Dict("z"=>sol.z,"t"=>t,"fields"=>sol.fields,"adjoints"=>adjoints))
    summary=Dict("agent"=>"gpt-b","model"=>"gpt-6-astra","family"=>"gpt",
        "profile"=>profile,"zeta"=>zeta,"dzeta"=>dz,"zspacing"=>zspacing,"raman_mean"=>false,
        "coordinates"=>["E","theta","T_weighted","V","p2","phi","T_ordinary"],
        "readout"=>"Exact ordinary energy-centroid gradient at a stationary two-mode mean",
        "elapsed_seconds"=>time()-started)
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,summary);end
    TOML.print(stdout,summary);flush(stdout)
end

for pair in ("grin02","grin11","step11")
    timing_check(joinpath(ARGS[1],pair*"_p0.2_physical.npz"),ARGS[2])
end
