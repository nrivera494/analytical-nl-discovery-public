# Independent API-only energy/photon cross-check. gpt-d / gpt-6-astra / gpt.
using PulsePropagation, FFTW, NPZ, TOML, LinearAlgebra
BLAS.set_num_threads(1);FFTW.set_num_threads(2)
raw=ARGS[1];d=npzread(joinpath(raw,"inputs.npz"));scalar(k)=Float64(d[k])
A=ComplexF64.(d["A"]);nt=length(A);grid=TimeGrid(nt,scalar("window"));om=vec(d["Om"])
domain=MMGNLSEDomain(degrees_of_freedom(:time);time_grid=grid)
params=MMGNLSEParameters(domain;length=scalar("L"),alpha=vec(d["alpha"]),gain=0.,beta=SampledBeta(om,vec(d["beta"])),S=1/scalar("Aeff"),n2=scalar("n2"),omega0=scalar("omega0"),raman=AgarwalRaman(fraction=scalar("fR"),tau1=scalar("t1"),tau2=scalar("t2")))
t0=time();sol=solve_mmgnlse(reshape(A,nt,1,1),params,scalar("h");method=RK4IP(),precision=:float64,saveat=.01)
omega=scalar("omega0").+om;iw=map(w->w>0 ? 1/(1.054571817e-10*w) : 0.,omega);factor=scalar("dt")*nt
N0=factor*sum(abs2.(fftshift(ifft(A))).*iw);E0=factor*sum(abs2.(fftshift(ifft(A))))
aa=1/scalar("t2");bb=1/scalar("t1");H=(aa^2+bb^2)./(aa^2+bb^2 .-om.^2 .-2im*aa.*om);pref=scalar("kappa")/(.5*(aa^2+bb^2))
rows=Dict{String,Any}[]
for z in sol.z
 Q=vec(get_spectral_field(sol;z=z,units=:power));p=abs2.(Q);N=factor*sum(p.*iw);E=factor*sum(p)
 I=abs2.(fft(ifftshift(Q)));Fi=fftshift(ifft(I));rate=-pref*factor*sum(om.*imag.(H).*abs2.(Fi))
 push!(rows,Dict("z"=>Float64(z),"E_pJ"=>E,"N_ratio"=>N/N0,"retention"=>E/E0,"retention_bound"=>1/(1+scalar("kappa")*E0*z),"ideal_identity_rate"=>rate,"rate_over_bound"=>-rate/(scalar("kappa")*E^2)))
end
Q=vec(get_spectral_field(sol;units=:power));npzwrite(joinpath(raw,"final.npz"),Dict("Q"=>Q,"omega"=>omega))
out=Dict("agent"=>"gpt-d","model"=>"gpt-6-astra","family"=>"gpt","solver_commit"=>"b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa","wall_s"=>time()-t0,"records"=>rows,"qualification"=>"Rate is the ideal identity evaluated on Julia fields, not Julia's exact RHS; its blue window may modify the identity.")
open(joinpath(raw,"metrics.toml"),"w") do io;TOML.print(io,out);end
println(rows[end])
