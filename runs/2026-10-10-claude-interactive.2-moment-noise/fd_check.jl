# Central-difference check of the discrete-RK4IP adjoint gradient used in contract.jl (main case, eps0 = 0.05, gL = 6).
# Usage: julia --project=solver fd_check.jl <outjson>
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-simval-lib", "simlib.jl"))
include(joinpath(@__DIR__, "jsonio.jl"))
outjson = ARGS[1]
S = mkparams(eps0=0.05, Gamma=sqrt(18), gL=6.0, Nt=2^13, window=32.0)
A0 = seed_parabola(S; delta=0.5 * S.eps0^(2/3))
dz = S.L / 16000
sol = solve_mmgnlse(A0, S.params, dz)
AL = get_temporal_field(sol; z=:final)[:, 1, 1]
res = Dict{String,Any}()
for (name, gfun, J) in (("Tc", grad_Tc, A -> moments(A, S).Tc), ("Wc", grad_Wc, A -> moments(A, S).Wc))
    lam = lam_from_time_grad(gfun(AL, S))
    adj = solve_adjoint(lam, S.params, dz; forward_solution=sol, adjoint_mode=:discrete_rk4ip, units=:power)
    lam0 = vec(get_spectral_field(adj; z=:initial, units=:power))
    out = Float64[]
    for seed in 1:3
        rng = MersenneTwister(seed)
        d = reshape(ComplexF64.(randn(rng, S.Nt) .+ im .* randn(rng, S.Nt)) .* sqrt.(abs2.(vec(A0)) .+ 1e-6 * S.P0) .* 1e-6, :, 1, 1)
        Jp = J(get_temporal_field(solve_mmgnlse(A0 .+ d, S.params, dz))[:, 1, 1])
        Jm = J(get_temporal_field(solve_mmgnlse(A0 .- d, S.params, dz))[:, 1, 1])
        pred = 2 * real(sum(conj.(lam0) .* fftshift(ifft(vec(d)))))
        push!(out, abs((Jp - Jm) / 2 - pred) / abs(pred))
    end
    res[name] = out
end
open(outjson, "w") do io; json(io, res); println(io); end
println("fd check rel errors: ", res)
