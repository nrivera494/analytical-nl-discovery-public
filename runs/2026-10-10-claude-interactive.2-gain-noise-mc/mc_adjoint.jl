# Route (ii) on exactly the Monte Carlo configuration of mc.jl (same grid, step and seed), Kerr on and off.
# Writes (I_in, I_ase) for photon number, Tc and Wc; variance = I_in + (2 n_sp - 1) I_ase.
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-simval-lib", "simlib.jl"))
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-moment-noise", "jsonio.jl"))
outjson = ARGS[1]
const EPS0 = 0.1; const GAM = sqrt(18); const GL = 4.0; const NT = 1024; const WIN = 16.0; const NSTEPS = 2000
simpson(z, f) = (n = length(z) - 1; h = (z[end] - z[1]) / n; h / 3 * (f[1] + f[end] + 4sum(f[2:2:end-1]) + 2sum(f[3:2:end-2])))
res = Dict{String,Any}()
for kerr in (true, false)
    S = mkparams(eps0=EPS0, Gamma=GAM, gL=GL, Nt=NT, window=WIN)
    if !kerr
        P = MMGNLSEParameters(S.domain; length=S.L, gain=S.g, beta=TaylorBeta([0.0, 0.0, S.b2]), S=1.0, n2=0.0, omega0=S.omega0)
        S = merge(S, (; params=P))
    end
    A0 = seed_parabola(S; delta=0.5 * S.eps0^(2/3))
    dz = S.L / NSTEPS
    zf = collect(range(0, S.L; length=401))
    sol = solve_mmgnlse(A0, S.params, dz; saveat=zf)
    AL = get_temporal_field(sol; z=:final)[:, 1, 1]
    fs = Dict("N" => grad_N(AL, S), "Tc" => grad_Tc(AL, S), "Wc" => grad_Wc(AL, S))
    tr = Dict{String,Any}()
    for (k, gt) in fs
        adj = solve_adjoint(lam_from_time_grad(gt), S.params, dz; forward_solution=sol, adjoint_mode=:discrete_rk4ip,
                            units=:photon, saveat=zf)
        tr[k] = get_spectral_field(adj; z=:all, units=:photon)[:, 1, 1, :]
    end
    d = Dict{String,Any}("N0" => photons(S, A0), "NL" => photons(S, AL), "G" => exp(S.g * S.L))
    for (a, b) in (("N", "N"), ("Tc", "Tc"), ("Wc", "Wc"), ("Tc", "Wc"))
        ov = [real(sum(conj.(tr[a][:, k]) .* tr[b][:, k])) for k in 1:401]
        d["$(a)_$(b)"] = [ov[1], S.g * simpson(zf, ov)]
    end
    m = moments(AL, S)
    d["mean_Tc"] = m.Tc; d["mean_Wc"] = m.Wc
    res[kerr ? "kerr" : "lin"] = d
end
open(outjson, "w") do io; json(io, res); println(io); end
println("done")
