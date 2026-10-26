# Independent solver API cross-check: gpt-d / gpt-6-astra / gpt.
using PulsePropagation, FFTW, NPZ, TOML, LinearAlgebra
BLAS.set_num_threads(1); FFTW.set_num_threads(2)
raw=ARGS[1]; d=npzread(joinpath(raw,"inputs.npz")); scalar(k)=Float64(d[k])
A=ComplexF64.(d["A"]); nt=length(A); grid=TimeGrid(nt,scalar("window"))
domain=MMGNLSEDomain(degrees_of_freedom(:time);time_grid=grid)
@assert maximum(abs.(frequency_axis(grid).-d["Om"])) < 1e-8
params=MMGNLSEParameters(domain;length=scalar("L"),alpha=vec(d["alpha"]),gain=0.,
 beta=SampledBeta(vec(d["Om"]),vec(d["beta"])),S=1/scalar("Aeff"),n2=scalar("n2"),
 omega0=scalar("omega0"),raman=AgarwalRaman(fraction=scalar("fR"),tau1=scalar("t1"),tau2=scalar("t2")))
t0=time(); sol=solve_mmgnlse(reshape(A,nt,1,1),params,scalar("h");method=RK4IP(),precision=:float64,saveat=scalar("L")>100 ? 2. : .5)
omega=scalar("omega0").+vec(d["Om"]); iw=map(w->w>0 ? 1/(1.054571817e-10*w) : 0.,omega)
N0=scalar("dt")*nt*sum(abs2.(fftshift(ifft(A))).*iw)
rows=Dict{String,Any}[]
for z in sol.z
 Q=vec(get_spectral_field(sol;z=z,units=:power)); p=abs2.(Q);N=scalar("dt")*nt*sum(p.*iw);E=scalar("dt")*nt*sum(p)
 cut=omega.<2pi*299.792458/scalar("cutoff"); eta=scalar("dt")*nt*sum((p.*iw)[cut])/N0
 push!(rows,Dict("z"=>Float64(z),"N_ratio"=>N/N0,"lambda_um"=>2pi*299.792458/(E/(1.054571817e-10*N)),"eta"=>eta))
end
Q=vec(get_spectral_field(sol;units=:power)); npzwrite(joinpath(raw,"final.npz"),Dict("Q"=>Q,"omega"=>omega))
out=Dict("agent"=>"gpt-d","model"=>"gpt-6-astra","family"=>"gpt","solver_commit"=>"b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa","wall_s"=>time()-t0,"records"=>rows)
open(joinpath(raw,"metrics.toml"),"w") do io; TOML.print(io,out); end
println(rows[end]); println("Wall seconds: ",out["wall_s"])
