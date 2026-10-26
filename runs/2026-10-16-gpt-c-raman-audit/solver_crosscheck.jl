# Independent library invocation. agent gpt-c; model gpt-6-astra; family gpt.
using PulsePropagation, FFTW, LinearAlgebra, DelimitedFiles
LinearAlgebra.BLAS.set_num_threads(1)
FFTW.set_num_threads(2)
raw="~/analytical-nl-discovery-data/2026-10-16-gpt-c-raman-audit"
mkpath(raw)
N=4.0; T0=0.2; n=16384; width=96.0
grid=TimeGrid(n,width*T0)
domain=MMGNLSEDomain(degrees_of_freedom(:time);time_grid=grid)
t=time_axis(grid)
b2=-0.0217; gamma=0.0013; LD=T0^2/abs(b2)
c=2.99792458e-4; omega0=2pi*c/1550e-9; n2=2.6e-20
q=N ./ cosh.(t./T0)
A=reshape(ComplexF64.(q .* sqrt(abs(b2)/gamma/T0^2)),n,1,1)
p=MMGNLSEParameters(domain;length=3LD/N,alpha=0.0,gain=0.0,
    beta=TaylorBeta([0.0,0.0,b2]),S=gamma*c/(n2*omega0),n2=n2,omega0=omega0,
    raman=AgarwalRaman(fraction=.18,tau1=.0122,tau2=.032))
elapsed=@elapsed sol=solve_mmgnlse(A,p,LD*1e-4;method=RK4IP(),saveat=nothing)
out=vec(get_temporal_field(sol))./sqrt(abs(b2)/gamma/T0^2)
writedlm(joinpath(raw,"library_N4_T200_zN3.csv"),hcat(t./T0,real.(out),imag.(out)),',')
open(joinpath(raw,"library_crosscheck.txt"),"w") do io
    println(io,"agent=gpt-c model=gpt-6-astra family=gpt")
    println(io,"elapsed_seconds=",elapsed," norm_ratio=",sum(abs2,out)/sum(abs2,q))
    println(io,"peak_rss_bytes=",Sys.maxrss())
    println(io,"solver_commit=b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa n=",n," width=",width," step_LD=0.0001")
end
println("completed library forward in ",elapsed," seconds")
