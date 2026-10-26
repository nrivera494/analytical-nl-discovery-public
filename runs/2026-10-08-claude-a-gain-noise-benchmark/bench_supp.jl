# Supplementary high-statistics check of the per-bin output variance, run after bench.jl.
# Motivation: in bench.jl the pooled per-bin variance ratio s_meas/s_pred averaged 0.99968 +- 0.00010
# over the 10 cases (about -3 sigma). This script checks whether that deficit is real.
#   JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-08-claude-a-gain-noise-benchmark/bench_supp.jl
include(joinpath(@__DIR__, "bench.jl"))   # defines make_problem, run_case, _js, constants (does not run main)

const SUPP_CASES = [
    (name="S1_G3_nsp1_onestep_200k",    lnG=3.0, ns=0.5, ns0=NS0, N0=1e6, nsteps=1, ntraj=200000, seed_init=3101, seed_drive=4101),
    (name="S2_G2_vacuum_off_onestep_200k", lnG=2.0, ns=0.5, ns0=0.0, N0=1e6, nsteps=1, ntraj=200000, seed_init=3102, seed_drive=4102),
]

# S3: initial ShotNoise ensemble only (no propagation): E|dB|^2 should be 2*0.5^2 = 0.5 per bin
function generator_check(; ntraj=200000, batch=10000, seed=3103)
    problem = make_problem(; lnG=1.0, N0=1e6, nsteps=1)
    objs = PP.backend_objects(problem)
    w = PP.photon_bin_weights(NT, objs.ic.dt, objs.sim.f0; shifted=false)
    mean_uw = ifft(objs.ic.fields[:, 1, 1])
    rng = MersenneTwister(seed)
    per_traj = zeros(ntraj)
    q0 = 0
    while q0 < ntraj
        nb = min(batch, ntraj - q0)
        ens = PP.stochastic_ensemble(problem; noise=PP.ShotNoise(; noise_scale=0.5), ntraj=nb, rng=rng)
        dB = sqrt.(w) .* (ens.uω[:, 1, :] .- mean_uw)
        per_traj[(q0 + 1):(q0 + nb)] = vec(sum(abs2, dB; dims=1))
        q0 += nb
    end
    M = count(>(0), w)
    m = mean(per_traj) / M
    se = std(per_traj) / sqrt(ntraj) / M
    return Dict("name" => "S3_shotnoise_generator_only", "ntraj" => ntraj, "M_bins" => M, "seed" => seed,
                "E_abs2_dB_meas" => m, "E_abs2_dB_se" => se, "E_abs2_dB_pred" => 0.5,
                "ratio" => m / 0.5, "ratio_se" => se / 0.5)
end

function supp_main()
    t0 = time()
    out = Dict{String,Any}[]
    for c in SUPP_CASES
        r = run_case(c)
        push!(out, r)
        @printf("%-30s s ratio %.5f±%.5f | F ratio %.4f±%.4f | mean-added %.4f±%.4f | chi2/bin %.3f | %.1fs\n",
                c.name, r["s_ratio"], r["s_ratio_se"], r["F_ratio"], r["F_ratio_se"],
                r["mean_added_ratio"], r["mean_added_ratio_se"], r["flatness"]["chi2_per_bin"], r["wall_time_s"])
        flush(stdout)
    end
    g = generator_check()
    @printf("%-30s E|dB|^2 ratio %.5f±%.5f\n", g["name"], g["ratio"], g["ratio_se"])
    push!(out, g)
    open(joinpath(OUTDIR, "summary_supp.tmp.json"), "w") do io
        write(io, _js(Dict{String,Any}("supplementary" => out, "supp_wall_time_s" => time() - t0)) * "\n")
    end
    println("supp wall time ", time() - t0, " s")
end

supp_main()
