# R2, R5: deterministic linear response of the shape modes, by paired +/- perturbation runs of the full NLSE
# (FastDifferentiableMMNLO facade, RK4IP) on the asymptotic seed (Gamma = sqrt 18, chirp q = 1/3).
# Usage: julia --project=solver shapemodes.jl <eps0> <gL> <eta> <outjson> [nsteps_factor] [case]
# Launches: for l = 0..4, "ph" (phase eta*P_l(xi)) and "int" (relative intensity eta*P_l(xi)), signs +/-.
# Readouts (n_l, p_l), l = 0..4, of the central difference delta A = (A+ - A-)/2 at 61 planes.
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-simval-lib", "simlib.jl"))
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-moment-noise", "jsonio.jl"))

eps0 = parse(Float64, ARGS[1]); gL = parse(Float64, ARGS[2]); eta = parse(Float64, ARGS[3]); outjson = ARGS[4]
nfac = length(ARGS) >= 5 ? parse(Float64, ARGS[5]) : 1.0
case = length(ARGS) >= 6 ? ARGS[6] : "asym"
Gamma, q = case == "asym" ? (sqrt(18), 1 / 3) : case == "main" ? (sqrt(18), 0.0) : error("case")

zs_h, as_h, aps_h = hydro_width(1.0, q * Gamma, Gamma, gL / Gamma; n=100000)
amax = maximum(as_h); apmax = maximum(abs.(aps_h))
thetaL = sum(exp.(Gamma .* zs_h[1:end-1]) ./ as_h[1:end-1] .* diff(zs_h))
window = 2 * ceil(1.45 * amax + 5)
Nt = nextpow(2, window / (π / (2.4 * apmax / eps0)))
S = mkparams(eps0=eps0, Gamma=Gamma, gL=gL, Nt=Nt, window=window)
A0 = vec(seed_parabola(S; q=q, delta=0.5 * eps0^(2/3)))
nsteps = max(3000, round(Int, 2 * ceil(15 * nfac * thetaL / eps0)))
dz = S.L / nsteps
nz = 61
zf = collect(range(0, S.L; length=nz))

Pl(l, x) = l == 0 ? 1.0 : l == 1 ? x : l == 2 ? (3x^2 - 1) / 2 : l == 3 ? (5x^3 - 3x) / 2 : (35x^4 - 30x^2 + 3) / 8
dPl(l, x) = l == 0 ? 0.0 : l == 1 ? 1.0 : l == 2 ? 3x : l == 3 ? (15x^2 - 3) / 2 : (140x^3 - 60x) / 8

run(A) = get_temporal_field(solve_mmgnlse(reshape(A, :, 1, 1), S.params, dz; saveat=zf); z=:all)[:, 1, 1, :]
t0 = time()
Aref = run(A0)
tref = time() - t0
mref = [moments(Aref[:, k], S) for k in 1:nz]

m0 = mref[1]; Tp0 = sqrt(5m0.varT)
xi0 = (S.t .- m0.Tc) ./ Tp0
cut = exp.(-(max.(abs.(xi0) .- 1.3, 0.0) ./ 0.1) .^ 2)

curr(A) = S.b2 .* real.(conj.(A) .* iddt(A, S.w))
function readouts(Ap, Am, k)
    m = mref[k]; Ab = Aref[:, k]
    Tp = sqrt(5m.varT); Tpp = sqrt(5) * S.b2 * m.cov / sqrt(m.varT)
    x = S.t .- m.Tc; xi = x ./ Tp
    drho = (abs2.(Ap) .- abs2.(Am)) ./ 2
    dj = (curr(Ap) .- curr(Am)) ./ 2
    dA = (Ap .- Am) ./ 2
    n = [((2l + 1) / 2) * (4 / (3m.E)) * sum(Pl.(l, xi) .* drho) * S.dt for l in 0:4]
    p = zeros(5)
    for l in 1:4
        p[l+1] = ((2l + 1) / (2S.b2 * l * (l + 1))) * (4Tp / (3m.E)) *
                 ((Tpp / Tp) * sum(dPl.(l, xi) .* x .* drho) * S.dt - sum(dPl.(l, xi) .* dj) * S.dt)
    end
    p[1] = sum(imag.(conj.(Ab) .* dA)) * S.dt / m.E + p[3] / 5
    return vcat(p, n)
end

launches = String[]
data = Dict{String,Any}()
for l in 0:4, typ in ("ph", "int")
    pert(s) = typ == "ph" ? A0 .* cis.(s * eta .* Pl.(l, xi0) .* cut) : A0 .* sqrt.(1 .+ s * eta .* Pl.(l, xi0) .* cut)
    Ap = run(pert(1.0)); Am = run(pert(-1.0))
    key = "$(typ)$(l)"
    push!(launches, key)
    data[key] = [readouts(Ap[:, k], Am[:, k], k) for k in 1:nz]
    @printf("launch %s done (%.0fs)\n", key, time() - t0); flush(stdout)
end
ref = Dict("z" => zf, "tau" => S.g .* zf, "E" => [m.E for m in mref], "varT" => [m.varT for m in mref],
           "cov" => [m.cov for m in mref], "varW" => [m.varW for m in mref], "Tc" => [m.Tc for m in mref])
ef = edge_fractions(Aref[:, end], S)
out = Dict{String,Any}("case" => case, "eps0" => eps0, "gL" => gL, "eta" => eta, "Nt" => Nt, "window" => window,
    "nsteps" => nsteps, "t_ref_s" => tref, "t_total_s" => time() - t0, "edge_time" => ef.et, "edge_freq" => ef.ew,
    "energy_balance_rel_err" => mref[end].E / (mref[1].E * exp(S.g * S.L)) - 1,
    "params" => Dict("g" => S.g, "L" => S.L, "b2" => S.b2, "gam" => S.gam, "P0" => S.P0, "T0" => S.T0,
                     "dt" => S.dt, "Gamma" => Gamma, "q" => q),
    "ref" => ref, "launches" => launches, "readouts_p0to4_n0to4" => data)
open(outjson, "w") do io; json(io, out); println(io); end
@printf("done eps0=%.3g Nt=%d nsteps=%d total %.0fs energy_err=%.1e edges=(%.1e,%.1e)\n", eps0, Nt, nsteps,
        time() - t0, out["energy_balance_rel_err"], ef.et, ef.ew)
