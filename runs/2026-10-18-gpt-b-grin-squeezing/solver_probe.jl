# gpt-b / gpt-6-astra / gpt. Black-box contraction-index diagnosis.
# No solver source is read or modified, preserving the clean-context boundary.
using PulsePropagation, NPZ, FFTW, LinearAlgebra
const PP=PulsePropagation
BLAS.set_num_threads(1);FFTW.set_num_threads(1)
raw=ARGS[1];input=npzread(joinpath(raw,"squeezing_solver_input.npz"));out=Dict{String,Any}()
a=ComplexF64.(input["initial"])[1,:];base=Float64.(input["tensor"]);m=length(a)
for (label,order) in [("conj_second",(1,2,3,4)),("conj_third",(1,3,2,4)),("conj_fourth",(1,3,4,2))]
    h=1e-5;tensor=permutedims(base,order)
    sim=PP.Simulation{Float64}(lambda0=1.064e-6,dz=h,include_Raman=false,pulse_centering=false)
    fiber=PP.Fiber{Float64}(betas=zeros(3,m),sr=tensor,L0=h,fr=0.);sr=PP.calc_srsk(fiber,sim,m)
    aw=ifft(repeat(reshape(a,1,m),2,1),1)
    aw,_,ok=PP.step_rk4ip_nogain(aw,sim,fill(-1.0im,2),sr,zeros(ComplexF64,2,m),ComplexF64[],ComplexF64[],nothing,nothing)
    ok || error("One-step interface probe rejected")
    out[label]=(vec(fft(aw,1)[1,:])-a)/h
end
npzwrite(joinpath(raw,"squeezing_solver_probe.npz"),out)
