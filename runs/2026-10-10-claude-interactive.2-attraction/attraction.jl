# R1, R3, R4: deterministic full-NLSE runs of near-parabolic launches (FastDifferentiableMMNLO facade, RK4IP).
# Usage: julia --project=solver attraction.jl <eps0> <Gamma> <q> <gL> <energy_scale> <outjson> [nsteps_factor]
# Saves rms moments along z, core-parabola fit and edge diagnostics.
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-simval-lib", "simlib.jl"))
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-moment-noise", "jsonio.jl"))

eps0 = parse(Float64, ARGS[1]); Gamma = parse(Float64, ARGS[2]); q = parse(Float64, ARGS[3])
gL = parse(Float64, ARGS[4]); escale = parse(Float64, ARGS[5]); outjson = ARGS[6]
nfac = length(ARGS) >= 7 ? parse(Float64, ARGS[7]) : 1.0

zs_h, as_h, aps_h = hydro_width(1.0, q * Gamma, Gamma, gL / Gamma; n=100000)
amax = maximum(as_h); apmax = maximum(abs.(aps_h))
thetaL = sum(exp.(Gamma .* zs_h[1:end-1]) ./ as_h[1:end-1] .* diff(zs_h))
window = 2 * ceil(1.45 * amax + 5)
Nt = nextpow(2, window / (π / (2.4 * apmax / eps0)))
S = mkparams(eps0=eps0, Gamma=Gamma, gL=gL, Nt=Nt, window=window)
A0 = seed_parabola(S; q=q, delta=0.5 * eps0^(2/3)) .* sqrt(escale)
nsteps = max(3000, round(Int, 2 * ceil(15 * nfac * thetaL / eps0)))
dz = S.L / nsteps
nz = 241
zf = collect(range(0, S.L; length=nz))
t0 = time()
sol = solve_mmgnlse(A0, S.params, dz; saveat=zf)
tf = time() - t0
At = get_temporal_field(sol; z=:all)

function corefit(A, S)
    # least-squares parabola rho = c0 + c2 T^2 on |T - Tc| < 0.6 Tp (Tp from rms), returns peak, half-width
    m = moments(A, S); Tp = sqrt(5m.varT)
    rho = abs2.(A); x = S.t .- m.Tc
    sel = abs.(x) .< 0.6Tp
    X = hcat(ones(count(sel)), x[sel] .^ 2)
    c = X \ rho[sel]
    pk = c[1]; Tfit = sqrt(-c[1] / c[2])
    resid = sqrt(mean((rho[sel] .- X * c) .^ 2)) / pk
    # intensity at the fitted edge, relative to peak (edge-layer measure ~ (delta/Tp))
    function interp(xq)
        i = searchsortedlast(x, xq); i = clamp(i, 1, length(x) - 1)
        θ = (xq - x[i]) / (x[i+1] - x[i]); (1 - θ) * rho[i] + θ * rho[i+1]
    end
    edge = (interp(Tfit) + interp(-Tfit)) / (2pk)
    return pk, Tfit, resid, edge
end

rows = Dict{String,Any}()
mz = [moments(At[:, 1, 1, k], S) for k in 1:nz]
cf = [corefit(At[:, 1, 1, k], S) for k in 1:nz]
rows["z"] = zf; rows["tau"] = S.g .* zf
rows["E"] = [m.E for m in mz]; rows["varT"] = [m.varT for m in mz]; rows["varW"] = [m.varW for m in mz]
rows["cov"] = [m.cov for m in mz]; rows["Tc"] = [m.Tc for m in mz]; rows["Wc"] = [m.Wc for m in mz]
rows["peak"] = [maximum(abs2.(At[:, 1, 1, k])) for k in 1:nz]
rows["fit_peak"] = [c[1] for c in cf]; rows["fit_Tp"] = [c[2] for c in cf]; rows["fit_resid"] = [c[3] for c in cf]
rows["edge_rho"] = [c[4] for c in cf]
ef = edge_fractions(At[:, 1, 1, end], S)
out = Dict{String,Any}("eps0" => eps0, "Gamma" => Gamma, "q" => q, "gL" => gL, "escale" => escale,
    "Nt" => Nt, "window" => window, "nsteps" => nsteps, "t_forward_s" => tf, "edge_time" => ef.et, "edge_freq" => ef.ew,
    "energy_balance_rel_err" => rows["E"][end] / (rows["E"][1] * exp(S.g * S.L)) - 1,
    "params" => Dict("g" => S.g, "L" => S.L, "b2" => S.b2, "gam" => S.gam, "P0" => S.P0, "T0" => S.T0, "dt" => S.dt),
    "rows" => rows)
open(outjson, "w") do io; json(io, out); println(io); end
@printf("done eps0=%.3g Gamma=%.3g q=%.3g E=%.4g Nt=%d nsteps=%d t=%.1fs energy_err=%.1e edges=(%.1e,%.1e)\n",
        eps0, Gamma, q, escale, Nt, nsteps, tf, out["energy_balance_rel_err"], ef.et, ef.ew)
