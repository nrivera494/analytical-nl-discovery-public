# Route (ii): linearized output covariances by discrete-RK4IP adjoint contraction (FastDifferentiableMMNLO facade).
# Usage: julia --project=solver contract.jl <case> <eps0> <gL> <funcset> <outjson> [nsteps_factor] [grid_factor]
#   case    = main (Gamma=sqrt18, q=0) | heldout (Gamma=1, q=0) | asym (Gamma=sqrt18, q=1/3)
#             | p8 | p8_lin | p8_ss  (realistic Gaussian seed of C-20261008-claude-a-01 P8; ss = self-steepening on)
#   funcset = TW (centroids) | all (centroids, photon number, matched-LO phase quadrature, spectral s_0..s_4, n_2)
# Output: JSON with (I_in, I_ase) covariance blocks (variance = I_in + (2 n_sp - 1) I_ase), mean-field moments,
# W(z)-moment-formula values (R6b) and diagnostics.
include(joinpath(@__DIR__, "..", "2026-10-10-claude-interactive.2-simval-lib", "simlib.jl"))

case = ARGS[1]; eps0 = parse(Float64, ARGS[2]); gL = parse(Float64, ARGS[3]); funcset = ARGS[4]; outjson = ARGS[5]
nfac = length(ARGS) >= 6 ? parse(Float64, ARGS[6]) : 1.0
gfac = length(ARGS) >= 7 ? parse(Float64, ARGS[7]) : 1.0
# optional seed-edge softening: "e23" (default) delta = 0.5 eps0^(2/3); "e1" delta = 0.5 eps0
dmode = length(ARGS) >= 8 ? ARGS[8] : "e23"
# optional finite gain bandwidth (relaxed assumption): gbw = gL (omega_edge(L)/Omega_g)^2, g(omega) = g (1 - (omega/Omega_g)^2)
gbw = length(ARGS) >= 9 ? parse(Float64, ARGS[9]) : 0.0
# optional spectral-core edge: "rms" (default) omega_e = sqrt(5 varW); "chirp" omega_e = sqrt(5) |cov| / sigma_T (chirp part only)
coremode = length(ARGS) >= 10 ? ARGS[10] : "rms"
gw = nothing

function json(io, x::AbstractDict, ind="")
    println(io, "{"); ks = collect(keys(x))
    for (i, k) in enumerate(ks)
        print(io, ind, "  \"", k, "\": "); json(io, x[k], ind * "  "); println(io, i < length(ks) ? "," : "")
    end
    print(io, ind, "}")
end
json(io, x::AbstractVector, ind="") = (print(io, "["); for (i, v) in enumerate(x); json(io, v, ind); i < length(x) && print(io, ", "); end; print(io, "]"))
json(io, x::AbstractMatrix, ind="") = json(io, [x[i, :] for i in 1:size(x, 1)], ind)
json(io, x::Real, ind="") = print(io, isfinite(x) ? repr(Float64(x)) : "null")
json(io, x::AbstractString, ind="") = print(io, "\"", x, "\"")
json(io, x::Bool, ind="") = print(io, x ? "true" : "false")

simpson(z, f) = begin
    n = length(z) - 1; @assert iseven(n); h = (z[end] - z[1]) / n
    @assert maximum(abs.(diff(z) .- h)) < 1e-9 * h
    h / 3 * (f[1] + f[end] + 4 * sum(f[2:2:end-1]) + 2 * sum(f[3:2:end-2]))
end

# ---------------- setup ----------------
if startswith(case, "p8")
    # physical units: ps, m, W
    b2 = 0.025; gam = 0.005; g = 1.9; L = 3.2
    T0g = 0.25 / (2 * sqrt(log(2)))                  # Gaussian 1/e half-width of intensity^(1/2): A = sqrt(P0) exp(-t^2/(2 T0^2))
    Ein = 10.0                                        # pJ = W ps
    P0 = Ein / (sqrt(π) * T0g)
    omega0 = case == "p8_ss" ? 2π * CLIGHT / 1030e-9 : OMEGA0_BIG
    Nt = round(Int, 2048 * gfac); window = 12.0
    grid = TimeGrid(Nt, window); domain = MMGNLSEDomain(degrees_of_freedom(:time), grid)
    gam_eff = case == "p8_lin" ? 0.0 : gam
    params = MMGNLSEParameters(domain; length=L, gain=g, beta=TaylorBeta([0.0, 0.0, b2]), S=1.0,
                               n2=gam_eff * CLIGHT / omega0, omega0=omega0)
    t = collect(time_axis(grid)); dt = grid.dt
    S = (; params, grid, domain, t, dt, w=PulsePropagation.ifft_frequency_grid(Nt, dt), Nt, window,
         eps0=NaN, Gamma=NaN, gL=g * L, gam=gam_eff, b2, T0=T0g, P0, g, L, sq=NaN, omega0)
    A0 = reshape(ComplexF64.(sqrt(P0) .* exp.(-t .^ 2 ./ (2T0g^2))), :, 1, 1)
    nsteps = round(Int, 4000 * nfac)
    hyd = nothing
else
    Gamma, q = case == "main" ? (sqrt(18), 0.0) : case == "heldout" ? (1.0, 0.0) : case == "asym" ? (sqrt(18), 1 / 3) : error("case")
    # hydrodynamic background for grid sizing and normalizers (sharp parabola, E0 = 4/3 P0 T0)
    ap0 = q * Gamma            # a'(0) in zeta units: chirp v = q g T  ->  da/dzeta = q Gamma a
    zs_h, as_h, aps_h = hydro_width(1.0, ap0, Gamma, gL / Gamma; n=100000)
    aL = as_h[end]; apL = aps_h[end]
    thetaL = simpson(zs_h[1:2:end], exp.(Gamma .* zs_h[1:2:end]) ./ as_h[1:2:end])
    window = 2 * ceil(1.45 * aL + 5)
    wedge = apL / eps0
    dt_req = π / (2.4 * wedge * gfac)
    Nt = nextpow(2, window / dt_req)
    S = mkparams(eps0=eps0, Gamma=Gamma, gL=gL, Nt=Nt, window=window)
    if gbw > 0
        Omg = (apL / eps0) * sqrt(gL / gbw)
        wc0 = fftshift(S.w)
        gprof = S.g .* (1 .- (wc0 ./ Omg) .^ 2)
        P = MMGNLSEParameters(S.domain; length=S.L, gain=reshape(gprof, :, 1, 1, 1), beta=TaylorBeta([0.0, 0.0, S.b2]),
                              S=1.0, n2=S.gam * CLIGHT / S.omega0, omega0=S.omega0)
        S = merge(S, (; params=P))
        global gw = abs.(gprof) ./ S.g       # per-bin noise weight (n_sp = 1: |g(omega)|/2 symmetric noise)
    end
    A0 = seed_parabola(S; q=q, delta=(dmode == "e1" ? 0.5 * eps0 : 0.5 * eps0^(2/3)))
    nsteps = max(3000, round(Int, 2 * ceil(15 * nfac * thetaL / eps0)))
    hyd = Dict("aL" => aL, "apL" => apL, "thetaL" => thetaL)
end
N0 = photons(S, A0)
dz = S.L / nsteps
nz = 401
zf = collect(range(0, S.L; length=nz))
t0 = time()
sol = solve_mmgnlse(A0, S.params, dz; saveat=zf)
tfwd = time() - t0
At = get_temporal_field(sol; z=:all)
AL = At[:, 1, 1, end]
mz = [moments(At[:, 1, 1, k], S) for k in 1:nz]
Nz = [photons(S, At[:, 1, 1, k]) for k in 1:nz]
mL = mz[end]; NL = Nz[end]
ef = edge_fractions(AL, S)
energy_err = Nz[end] / (Nz[1] * exp(S.g * S.L)) - 1

# ---------------- functionals (time-domain gradients unless noted) ----------------
cph = S.dt * 1e-12 / (HBAR * S.omega0 * 1e12)        # photons per (W ps) per bin factor
Tp = sqrt(5 * mL.varT)
funcs = Dict{String,Any}()
funcs["Tc"] = lam_from_time_grad(grad_Tc(AL, S))
funcs["Wc"] = lam_from_time_grad(grad_Wc(AL, S))
if funcset == "all"
    funcs["N"] = lam_from_time_grad(grad_N(AL, S))
    funcs["XP"] = lam_from_time_grad((im / 2) .* AL .* cph ./ sqrt(NL))      # matched-LO phase quadrature
    # n_2 readout: (5/2)(4/(3E)) int P2(T/Tp) delta rho dT, delta rho = 2 Re(conj(Abar) dA)
    P2 = x -> (3x^2 - 1) / 2
    funcs["n2"] = lam_from_time_grad((5 / 2) * (4 / (3 * mL.E)) .* P2.(S.t ./ Tp) .* AL .* S.dt)
    # spectral Legendre components over the core |omega| <= omega_e (centered spectral convention)
    Aw = fftshift(ifft(AL)); wc = fftshift(S.w); dw = abs(wc[2] - wc[1])
    we = coremode == "chirp" ? sqrt(5) * abs(mL.cov) / sqrt(mL.varT) : sqrt(5 * mL.varW)
    core = abs.(wc .- mL.Wc) .<= we
    S0 = 0.75 * sum(abs2.(Aw)) * dw / we
    Pl = [x -> 1.0, x -> x, x -> (3x^2 - 1) / 2, x -> (5x^3 - 3x) / 2, x -> (35x^4 - 30x^2 + 3) / 8]
    for l in 0:4
        lam = zeros(ComplexF64, S.Nt)
        xi = (wc .- mL.Wc) ./ we
        lam[core] .= ((2l + 1) / 2) .* Pl[l+1].(xi[core]) .* Aw[core] .* (dw / (we * S0))
        funcs["s$l"] = reshape(lam, :, 1, 1)
    end
end

names = collect(keys(funcs))
order = ["N", "Tc", "Wc", "XP", "n2", "s0", "s1", "s2", "s3", "s4"]
names = [n for n in order if n in names]
traj = Dict{String,Any}()
tadj = Dict{String,Float64}()
for nm in names
    t1 = time()
    adj = solve_adjoint(funcs[nm], S.params, dz; forward_solution=sol, adjoint_mode=:discrete_rk4ip,
                        units=:photon, saveat=zf)
    tadj[nm] = time() - t1
    @assert adj.z[1] == 0 && length(adj.z) == nz
    traj[nm] = get_spectral_field(adj; z=:all, units=:photon)[:, 1, 1, :]
end
K = length(names)
Cin = zeros(K, K); Case = zeros(K, K)
for i in 1:K, j in i:K
    ov = gw === nothing ? [real(sum(conj.(traj[names[i]][:, k]) .* traj[names[j]][:, k])) for k in 1:nz] :
                          [real(sum(gw .* conj.(traj[names[i]][:, k]) .* traj[names[j]][:, k])) for k in 1:nz]
    Cin[i, j] = Cin[j, i] = ov[1]
    Case[i, j] = Case[j, i] = S.g * simpson(zf, ov)
end
# R6b exact moment formula with W(z) of the noise-free run
z = zf; Lz = S.L; b2v = S.b2
fT = [(mz[k].varT + 2b2v * (Lz - z[k]) * mz[k].cov + b2v^2 * (Lz - z[k])^2 * mz[k].varW) / Nz[k] for k in 1:nz]
fW = [mz[k].varW / Nz[k] for k in 1:nz]
fC = [(mz[k].cov + b2v * (Lz - z[k]) * mz[k].varW) / Nz[k] for k in 1:nz]
mom = Dict("VarTc" => [fT[1], S.g * simpson(z, fT)], "VarWc" => [fW[1], S.g * simpson(z, fW)],
           "Cov" => [fC[1], S.g * simpson(z, fC)])

out = Dict{String,Any}()
out["case"] = case; out["delta_mode"] = dmode; out["gbw"] = gbw; out["core_mode"] = coremode; out["eps0"] = eps0; out["gL"] = S.g * S.L; out["Nt"] = S.Nt; out["window"] = S.window
out["nsteps"] = nsteps; out["nz_saved"] = nz; out["omega0"] = S.omega0; out["N0"] = N0; out["NL"] = NL
out["t_forward_s"] = tfwd; out["t_adjoint_s"] = [tadj[n] for n in names]
out["energy_balance_rel_err"] = energy_err; out["edge_time"] = ef.et; out["edge_freq"] = ef.ew
out["names"] = names; out["C_in"] = Cin; out["C_ase"] = Case
out["moment_formula"] = mom
out["seed"] = Dict("varT" => mz[1].varT, "varW" => mz[1].varW, "cov" => mz[1].cov, "E" => mz[1].E)
out["output"] = Dict("varT" => mL.varT, "varW" => mL.varW, "cov" => mL.cov, "E" => mL.E, "Tp" => Tp)
out["z"] = zf[1:20:end]; out["varT_z"] = [m.varT for m in mz[1:20:end]]; out["varW_z"] = [m.varW for m in mz[1:20:end]]
out["cov_z"] = [m.cov for m in mz[1:20:end]]
hyd === nothing || (out["hydro"] = hyd)
out["params"] = Dict("g" => S.g, "L" => S.L, "b2" => S.b2, "gam" => S.gam, "P0" => S.P0, "T0" => S.T0, "dt" => S.dt)
open(outjson, "w") do io
    json(io, out); println(io)
end
@printf("done %s eps0=%.4g gL=%.3g Nt=%d nsteps=%d fwd=%.1fs adj=%s energy_err=%.2e edges=(%.1e,%.1e)\n",
        case, eps0, S.g * S.L, S.Nt, nsteps, tfwd, string(round.([tadj[n] for n in names]; digits=1)), energy_err, ef.et, ef.ew)
