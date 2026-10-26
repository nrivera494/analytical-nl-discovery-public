# Agents' solver cross-check, gpt-c / gpt-6-astra / gpt.
# No solver repository files are modified. Custom response is local to this run.
using PulsePropagation, FFTW, LinearAlgebra, DelimitedFiles
LinearAlgebra.BLAS.set_num_threads(1)
FFTW.set_num_threads(1)
struct MeasuredZBLAN <: PulsePropagation.AbstractRamanResponse
    fraction::Float64
end
function PulsePropagation.raman_response(r::MeasuredZBLAN,t::AbstractVector{<:Real})
    # Yan Table 1 and HC linewidth convention; t is ps, table calculation fs.
    table=[54.43 8.48 58.67 23.46;102.91 17.12 82.40 32.96;
           169.95 51.78 115.27 46.11;275.91 155.69 160.76 64.30;
           377.35 62.12 137.90 55.16;504.77 107.05 184.62 73.85;
           576.43 27.69 38.50 15.40;648.44 17.83 135.84 54.34]
    c=pi*2.99792458e-5;tf=1000 .* t;h=zeros(Float64,length(t))
    for k in axes(table,1)
        p,A,g,l=table[k,:]
        h .+= A .* exp.(-c*l .* tf .- (c*g .* tf).^2 ./4) .* sin.(2c*p .* tf)
    end
    h[t .< 0] .= 0
    h ./= sum(h)*(t[2]-t[1])
    return (ha=h,hb=zeros(Float64,length(t)))
end
raw="~/analytical-nl-discovery-data/2026-10-17-gpt-c-zblan-transfer"
mkpath(raw)
N=4.;T0=.2;n=8192;width=96.
grid=TimeGrid(n,width*T0)
domain=MMGNLSEDomain(degrees_of_freedom(:time);time_grid=grid)
t=time_axis(grid);b2=-.0189;b3=.000112;gamma=.0021;LD=T0^2/abs(b2)
c=2.99792458e-4;omega0=2pi*c/1940e-9;n2=2.1e-20
q=N ./cosh.(t./T0);normalization=sqrt(abs(b2)/gamma/T0^2)
A=reshape(ComplexF64.(q .* normalization),n,1,1)
p=MMGNLSEParameters(domain;length=2LD/N,alpha=50log(10)/10000,gain=0.,
    beta=TaylorBeta([0.,0.,b2,b3]),S=gamma*c/(n2*omega0),n2=n2,omega0=omega0,
    raman=MeasuredZBLAN(.24))
elapsed=@elapsed sol=solve_mmgnlse(A,p,LD*1e-4;method=RK4IP(),saveat=nothing)
out=vec(get_temporal_field(sol))./normalization
writedlm(joinpath(raw,"library_zblan_N4_T200_zN2.csv"),hcat(t./T0,real.(out),imag.(out)),',')
open(joinpath(raw,"library_crosscheck.txt"),"w") do io
    println(io,"agent=gpt-c model=gpt-6-astra family=gpt")
    println(io,"elapsed_seconds=",elapsed," norm_ratio=",sum(abs2,out)/sum(abs2,q))
    println(io,"peak_rss_bytes=",Sys.maxrss())
    println(io,"solver_commit=b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa n=",n," width=",width," step_LD=0.0001")
    println(io,"Float64 fixed-step RK4IP forward; no adjoint or noise.")
end
println("completed measured-response library forward in ",elapsed," seconds")
