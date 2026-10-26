# gpt-b / gpt-6-astra / gpt; independent tensor, read-only pinned solver.
# Float64 fixed-step forward RK4IP. No adjoint or stochastic Raman is used.
using PulsePropagation, NPZ, FFTW, LinearAlgebra
const PP=PulsePropagation
BLAS.set_num_threads(1);FFTW.set_num_threads(1)
raw=ARGS[1];input=npzread(joinpath(raw,"squeezing_solver_input.npz"));out=Dict{String,Any}()
for single in (false,true),h in (.01,.005)
    tensor=single ? ones(Float64,1,1,1,1) : Float64.(get(input,"tensor_solver",input["tensor"]))
    initial=single ? reshape(ComplexF64.(input["initial1"]),:,1) : ComplexF64.(input["initial"])
    m=size(initial,2);final=similar(initial)
    sim=PP.Simulation{Float64}(lambda0=1.064e-6,dz=h,include_Raman=false,pulse_centering=false)
    fiber=PP.Fiber{Float64}(betas=zeros(3,m),sr=tensor,L0=5.,fr=0.);sr=PP.calc_srsk(fiber,sim,m)
    for b in axes(initial,1)
        a=initial[b,:];aw=ifft(repeat(reshape(a,1,m),2,1),1);cache=nothing
        for _ in 1:round(Int,5/h)
            aw,cache,ok=PP.step_rk4ip_nogain(aw,sim,fill(-1.0im,2),sr,zeros(ComplexF64,2,m),ComplexF64[],ComplexF64[],nothing,cache)
            ok || error("Fixed RK4IP step rejected")
        end
        final[b,:]=vec(fft(aw,1)[1,:])
    end
    out[(single ? "single_h" : "h")*string(h)]=single ? vec(final) : final
    println("solver completed single=",single," h=",h);flush(stdout)
end
npzwrite(joinpath(raw,"squeezing_solver_output.npz"),out)
