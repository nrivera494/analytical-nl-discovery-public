# Gain-Langevin noise normalization benchmark (linear amplifier, Kerr off).
# Run from the repository root:
#   JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-08-claude-a-gain-noise-benchmark/bench.jl
#
# Uses only the public stochastic API of the solver:
#   PassiveFiber(; n2=0.0, raman_fraction=0.0, ...), RK4IPSolver(; linear_gain=LinearGain(g)),
#   stochastic_ensemble(problem; noise=ShotNoise(; noise_scale), ntraj, rng),
#   stochastic_solve(problem, ensemble; drives=[GainLangevin(; noise_scale)], rng).
# Per-trajectory scalars and per-bin moments go to ~/analytical-nl-discovery-data/<run-id>/.

using PulsePropagation
using Random, Statistics, FFTW, LinearAlgebra, NPZ, Printf
const PP = PulsePropagation

const RUN_ID = "2026-10-08-claude-a-gain-noise-benchmark"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const OUTDIR = @__DIR__
mkpath(RAW)

# ---------------- fixed parameters (mirrored in config.yaml) ----------------
const NT = 512
const WINDOW_PS = 40.0
const LAMBDA0 = 1550e-9          # m
const LFIB = 1.0                 # m
const BETA2 = -0.02              # ps^2/m
const FWHM_PS = 1.0              # Gaussian intensity FWHM
const NS0 = 0.5                  # ShotNoise noise_scale for all noisy cases (unless overridden)
const BATCH = 500
const HBAR = 1.054571817e-34

# name, ln G, GainLangevin noise_scale, ShotNoise noise_scale, N0, nsteps, ntraj, seed_init, seed_drive
const CASES = [
    (name="G1_nsp1",        lnG=1.0, ns=0.5,       ns0=NS0, N0=1e6, nsteps=10, ntraj=20000, seed_init=1101, seed_drive=2101),
    (name="G2_nsp1",        lnG=2.0, ns=0.5,       ns0=NS0, N0=1e6, nsteps=10, ntraj=20000, seed_init=1102, seed_drive=2102),
    (name="G3_nsp1",        lnG=3.0, ns=0.5,       ns0=NS0, N0=1e6, nsteps=10, ntraj=20000, seed_init=1103, seed_drive=2103),
    (name="G3_nsp1_dz_half",lnG=3.0, ns=0.5,       ns0=NS0, N0=1e6, nsteps=20, ntraj=20000, seed_init=1104, seed_drive=2104),
    (name="G3_nsp1_onestep",lnG=3.0, ns=0.5,       ns0=NS0, N0=1e6, nsteps=1,  ntraj=20000, seed_init=1105, seed_drive=2105),
    (name="G2_nsp2",        lnG=2.0, ns=sqrt(0.75),ns0=NS0, N0=1e6, nsteps=10, ntraj=20000, seed_init=1106, seed_drive=2106),
    (name="G2_nsp2_dz_half",lnG=2.0, ns=sqrt(0.75),ns0=NS0, N0=1e6, nsteps=20, ntraj=20000, seed_init=1107, seed_drive=2107),
    (name="G2_nsp1_N0_1e8", lnG=2.0, ns=0.5,       ns0=NS0, N0=1e8, nsteps=10, ntraj=20000, seed_init=1108, seed_drive=2108),
    (name="G2_langevin_off",lnG=2.0, ns=0.0,       ns0=NS0, N0=1e6, nsteps=10, ntraj=20000, seed_init=1109, seed_drive=2109),
    (name="G2_vacuum_off",  lnG=2.0, ns=0.5,       ns0=0.0, N0=1e6, nsteps=10, ntraj=20000, seed_init=1110, seed_drive=2110),
]

function make_problem(; lnG, N0, nsteps)
    grid = TimeGrid(NT, WINDOW_PS)
    t = PP.time_axis(grid)
    f0 = 2.99792458e-4 / LAMBDA0                      # THz
    tau = FWHM_PS / (2 * sqrt(log(2)))                # field exp(-t^2/(2 tau^2))
    A = exp.(-t .^ 2 ./ (2 * tau^2))
    E_target_pJ = N0 * HBAR * 2pi * f0 * 1e12 * 1e12  # carrier-photon energy, pJ
    A .*= sqrt(E_target_pJ / (sum(abs2, A) * grid.dt))
    system = PP.PassiveFiber(; length=LFIB, lambda0=LAMBDA0,
                             betas=reshape([0.0, 0.0, BETA2], :, 1),
                             n2=0.0, raman_fraction=0.0)
    g = lnG / LFIB                                     # power gain coefficient, 1/m
    dz = LFIB / nsteps
    solver = PP.RK4IPSolver(; stepping=PP.FixedStep(; dz=dz),
                            saveat=PP.SaveAt(collect(range(0.0, LFIB; length=nsteps + 1))),
                            linear_gain=PP.LinearGain(g))
    return PP.PulsePropagationProblem(; grid=grid, system=system,
                                      fields=reshape(ComplexF64.(A), NT, 1),
                                      solver=solver)
end

# standard error of a sample variance using the empirical 4th central moment
function var_and_se(x)
    n = length(x)
    m = mean(x)
    d = x .- m
    v = sum(abs2, d) / (n - 1)
    m4 = mean(d .^ 4)
    se = sqrt(max(m4 - v^2 * (n - 3) / (n - 1), 0.0) / n)
    return v, se
end

function run_case(c)
    t0 = time()
    problem = make_problem(; lnG=c.lnG, N0=c.N0, nsteps=c.nsteps)
    objs = PP.backend_objects(problem)
    dt = objs.ic.dt
    f0 = objs.sim.f0
    w = PP.photon_bin_weights(NT, dt, f0; shifted=false)   # unshifted order
    pos = w .> 0
    M = count(pos)
    G = exp(c.lnG)

    # input coherent amplitude in photon units
    B0 = sqrt.(w) .* ifft(objs.ic.fields[:, 1, 1])
    N0 = sum(abs2, B0)

    # noise-free output through the same stochastic RK4IP path (exact mean for a linear system)
    ens0 = PP.stochastic_ensemble(problem; noise=PP.ShotNoise(; noise_scale=0.0), ntraj=1,
                                  rng=MersenneTwister(0))
    st0 = PP.stochastic_solve(problem, ens0; drives=[PP.GainLangevin(; noise_scale=0.0)],
                              rng=MersenneTwister(0))
    Bbar = sqrt.(w) .* ifft(st0.fields[:, 1, end, 1])
    Nbar = sum(abs2, Bbar)
    # independent deterministic solve (ODE path with linear_gain) as a cross-check
    sol = PP.solve(problem)
    Bdet = sqrt.(w) .* ifft(sol.output.fields[:, 1, end])
    Ndet = sum(abs2, Bdet)
    u = Bbar ./ sqrt(Nbar)                                   # signal-mode unit vector

    n = c.ntraj
    NW = zeros(n); Eeta = zeros(n); X = zeros(n); Y = zeros(n)
    s1 = zeros(ComplexF64, NT); s2 = zeros(NT); s4 = zeros(NT)
    rng_i = MersenneTwister(c.seed_init)
    rng_d = MersenneTwister(c.seed_drive)
    obs = PP.SpectralPhotonNumber(; filter=ones(NT), modes=:all)
    max_obs_diff = 0.0
    q0 = 0
    while q0 < n
        nb = min(BATCH, n - q0)
        ens = PP.stochastic_ensemble(problem; noise=PP.ShotNoise(; noise_scale=c.ns0),
                                     ntraj=nb, rng=rng_i)
        st = PP.stochastic_solve(problem, ens; drives=[PP.GainLangevin(; noise_scale=c.ns)],
                                 rng=rng_d)
        B = sqrt.(w) .* ifft(st.fields[:, 1, end, :], 1)    # NT x nb, photon units
        eta = B .- Bbar
        idx = (q0 + 1):(q0 + nb)
        NW[idx] = vec(sum(abs2, B; dims=1))
        Eeta[idx] = vec(sum(abs2, eta; dims=1))
        proj = vec(sum(conj.(u) .* eta; dims=1))
        X[idx] = real.(proj); Y[idx] = imag.(proj)
        a2 = abs2.(eta)
        s1 .+= vec(sum(eta; dims=2)); s2 .+= vec(sum(a2; dims=2)); s4 .+= vec(sum(a2 .^ 2; dims=2))
        if q0 == 0   # public observable cross-check on the first batch
            nobs = PP.stochastic_values(obs, st)
            max_obs_diff = maximum(abs.(nobs .- NW[idx]) ./ NW[idx])
        end
        q0 += nb
    end

    # ---------------- predictions ----------------
    sigma0 = 2 * c.ns0^2                       # input per-bin Wigner variance
    added = 2 * c.ns^2                         # = n_sp - 1/2 in the symmetric-ordering map
    s_pred = G * sigma0 + added * (G - 1)      # output per-bin Wigner variance
    nsp_equiv = added + 0.5
    F_pred = 2 * s_pred                        # = 1 + 2 n_sp (G-1) when sigma0 = 1/2

    # ---------------- estimators ----------------
    s_k = s2 ./ n
    s_k_se = sqrt.(max.(s4 ./ n .- s_k .^ 2, 0.0) ./ n)
    s_meas = mean(Eeta) / M
    s_meas_se = std(Eeta) / sqrt(n) / M
    mean_bias_chi2 = sum(abs2.(s1[pos] ./ n) ./ (s_pred / n)) / M   # E ~ 1 if unbiased

    VN, VN_se = var_and_se(NW)
    F_meas = (VN - M * s_meas^2) / Nbar
    F_meas_se = VN_se / Nbar
    VX, VX_se = var_and_se(X); VY, VY_se = var_and_se(Y)

    mean_added = mean(NW) - Nbar
    mean_added_se = std(NW) / sqrt(n)

    # flatness over bins with positive photon weight
    sk = s_k[pos]; skse = s_k_se[pos]
    z = (sk .- s_pred) ./ skse
    fabs = PP.absolute_frequency_grid_THz(NT, dt, f0; shifted=false)
    dfrel = abs.(fabs .- f0)[pos]
    inner = dfrel .<= quantile(dfrel, 0.5)
    flat = Dict(
        "mean_over_bins_ratio" => mean(sk) / s_pred,
        "std_over_bins_rel" => std(sk) / s_pred,
        "expected_std_rel_from_statistics" => mean(skse) / s_pred,
        "chi2_per_bin" => mean(z .^ 2),
        "max_abs_z" => maximum(abs.(z)),
        "inner_half_band_mean_ratio" => mean(sk[inner]) / s_pred,
        "outer_half_band_mean_ratio" => mean(sk[.!inner]) / s_pred,
        "min_ratio" => minimum(sk) / s_pred,
        "max_ratio" => maximum(sk) / s_pred,
    )

    res = Dict(
        "name" => c.name, "G" => G, "lnG" => c.lnG,
        "gain_langevin_noise_scale" => c.ns, "shot_noise_scale" => c.ns0,
        "n_sp_equivalent" => nsp_equiv,
        "N0_target" => c.N0, "N0_photon_units" => N0, "nsteps" => c.nsteps,
        "dz_m" => LFIB / c.nsteps, "ntraj" => n, "M_bins" => M,
        "deterministic_gain_stochastic_path" => Nbar / N0,
        "deterministic_gain_ode_solve" => Ndet / N0,
        "max_rel_diff_mean_fields_rk4ip_vs_ode" => maximum(abs.(Bdet .- Bbar)) / maximum(abs.(Bbar)),
        "max_rel_diff_public_observable_vs_manual" => max_obs_diff,
        "s_pred" => s_pred, "s_meas_pooled" => s_meas, "s_meas_pooled_se" => s_meas_se,
        "s_ratio" => s_meas / s_pred, "s_ratio_se" => s_meas_se / s_pred,
        "F_pred" => F_pred, "F_meas" => F_meas, "F_meas_se" => F_meas_se,
        "F_ratio" => F_meas / F_pred, "F_ratio_se" => F_meas_se / F_pred,
        "F_raw_varNW_over_GN0" => VN / Nbar,
        "M_s2_over_varNW" => M * s_meas^2 / VN,
        "var_X_inphase_ratio_to_s_over_2" => VX / (s_pred / 2), "var_X_se_ratio" => VX_se / (s_pred / 2),
        "var_Y_quadrature_ratio_to_s_over_2" => VY / (s_pred / 2), "var_Y_se_ratio" => VY_se / (s_pred / 2),
        "mean_added_wigner_photons_meas" => mean_added, "mean_added_wigner_photons_se" => mean_added_se,
        "mean_added_wigner_photons_pred" => M * s_pred,
        "mean_added_ratio" => mean_added / (M * s_pred), "mean_added_ratio_se" => mean_added_se / (M * s_pred),
        "mean_added_normal_ordered_meas" => mean_added - M / 2,
        "mean_added_normal_ordered_pred" => M * (s_pred - 0.5),
        "mean_field_bias_chi2_per_bin" => mean_bias_chi2,
        "flatness" => flat,
        "seed_init" => c.seed_init, "seed_drive" => c.seed_drive,
        "wall_time_s" => time() - t0,
    )

    npzwrite(joinpath(RAW, c.name * ".npz"), Dict(
        "N_W" => NW, "E_noise" => Eeta, "X_inphase" => X, "Y_quadrature" => Y,
        "s_k" => s_k, "s_k_se" => s_k_se, "mean_eta_re" => real.(s1 ./ n), "mean_eta_im" => imag.(s1 ./ n),
        "Bbar_re" => real.(Bbar), "Bbar_im" => imag.(Bbar), "f_abs_THz_unshifted" => fabs,
        "photon_weight" => w))
    return res
end

# ---------------- minimal JSON writer ----------------
_js(x::AbstractString) = "\"" * replace(x, "\\" => "\\\\", "\"" => "\\\"") * "\""
_js(x::Bool) = x ? "true" : "false"
_js(x::Integer) = string(x)
_js(x::Real) = isfinite(x) ? repr(Float64(x)) : "null"
_js(x::Nothing) = "null"
_js(x::AbstractVector) = "[" * join(_js.(x), ", ") * "]"
function _js(d::AbstractDict, ind=0)
    pad = " "^(ind + 2)
    items = [pad * _js(string(k)) * ": " * (v isa AbstractDict ? _js(v, ind + 2) : _js(v)) for (k, v) in sort(collect(d); by=first)]
    return "{\n" * join(items, ",\n") * "\n" * " "^ind * "}"
end

function main()
    tstart = time()
    results = Dict{String,Any}[]
    # BENCH_QUICK=1: smoke test only (2 cases, 1000 trajectories, no summary written)
    quick = get(ENV, "BENCH_QUICK", "0") == "1"
    cases = quick ? [merge(c, (ntraj=1000,)) for c in CASES[[1, 9]]] : CASES
    for c in cases
        r = run_case(c)
        push!(results, r)
        @printf("%-17s G=%6.3f ns=%.4f ns0=%.2f nsteps=%2d n=%d  F=%.4f±%.4f pred %.4f ratio %.4f±%.4f | s ratio %.5f±%.5f | mean-added ratio %.3f±%.3f | flat chi2/bin %.3f maxz %.2f | Gdet %.12f | %.1fs\n",
                c.name, r["G"], c.ns, c.ns0, c.nsteps, c.ntraj, r["F_meas"], r["F_meas_se"], r["F_pred"],
                r["F_ratio"], r["F_ratio_se"], r["s_ratio"], r["s_ratio_se"], r["mean_added_ratio"],
                r["mean_added_ratio_se"], r["flatness"]["chi2_per_bin"], r["flatness"]["max_abs_z"],
                r["deterministic_gain_stochastic_path"] / r["G"], r["wall_time_s"])
        flush(stdout)
    end
    summary = Dict{String,Any}(
        "run_id" => RUN_ID,
        "conventions" => Dict(
            "photon_units" => "B_k = sqrt(photon_bin_weights_k) * ifft(A_t)_k; N_W = sum_k |B_k|^2 over bins with positive weight",
            "s_pred" => "G*2*ns0^2 + 2*ns^2*(G-1)",
            "F_pred" => "2*s_pred = 1 + 2 n_sp (G-1) with n_sp = 2 ns^2 + 1/2 when ns0 = 1/2",
            "F_meas" => "(Var(N_W) - M s_meas^2)/(G N0), with G N0 the noise-free output photon number",
            "errors" => "one standard error; variance SE from the empirical fourth central moment"),
        "cases" => results,
        "total_wall_time_s" => time() - tstart,
        "julia_threads" => Threads.nthreads(),
        "julia_version" => string(VERSION),
    )
    quick && return
    open(joinpath(OUTDIR, "summary.json"), "w") do io
        write(io, _js(summary) * "\n")
    end
    println("total wall time ", time() - tstart, " s")
end

# run only when executed as a program (bench_supp.jl includes this file)
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
