# agent: gpt-b; model: gpt-6-astra; family: gpt; 2026-10-17.
# Independent full HG tensor, constant temporal field, pinned agents' solver.
# No adjoint is used. The direct C/DOP853 reference uses the same sign convention.
using PulsePropagation, NPZ, FFTW, LinearAlgebra
const PP=PulsePropagation
BLAS.set_num_threads(1);FFTW.set_num_threads(1)
raw=ARGS[1]
input=npzread(joinpath(raw,"solver_input.npz"))
tensor=Float64.(input["tensor"]);a=ComplexF64.(input["initial"]);q=Float64.(input["groups"])
m=length(a);out=Dict{String,Any}()
for kappa in (10.,40.), h in (.002,.001)
    sim=PP.Simulation{Float64}(lambda0=1.064e-6,dz=h,include_Raman=false,pulse_centering=false)
    fiber=PP.Fiber{Float64}(betas=zeros(3,m),sr=tensor,L0=4.,fr=0.)
    sr=PP.calc_srsk(fiber,sim,m)
    d=repeat(reshape(-1im*kappa.*q,1,m),2,1)
    aw=ifft(repeat(reshape(a,1,m),2,1),1);cache=nothing
    for _ in 1:round(Int,4/h)
        aw,cache,ok=PP.step_rk4ip_nogain(aw,sim,fill(-1.0im,2),sr,d,
            ComplexF64[],ComplexF64[],nothing,cache)
        ok || error("Fixed-step RK4IP rejected step")
    end
    out["k$(Int(kappa))_h$(h)"]=vec(fft(aw,1)[1,:])
end
npzwrite(joinpath(raw,"solver_output.npz"),out)
println("Pinned-solver full-tensor cross-check completed")
