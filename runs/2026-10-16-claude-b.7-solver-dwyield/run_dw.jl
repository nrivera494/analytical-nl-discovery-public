# Driver for run 2026-10-16-claude-b.7-solver-dwyield (agent claude-b.7, task
# T-20261016-claude-interactive-03, problem P-20261016-claude-interactive-01).
#
# Usage (repository root):
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-16-claude-b.7-solver-dwyield/run_dw.jl <stage> [<stage> ...]
#
# Every saved plane of every case is appended as one JSON object per line to
#   ~/analytical-nl-discovery-data/2026-10-16-claude-b.7-solver-dwyield/results_<stage>.jsonl
# summarize.py turns those files into summary.json.
#
# Grids (tau in T0 units, w = Omega T0):
#   G1: window 160, Nt 4096  (dtau 0.0391, w_max 80.4)
#   G2: window 256, Nt 16384 (dtau 0.0156, w_max 201.1)
#   G3: window 384, Nt 32768 (dtau 0.0117, w_max 268.1)   (grid refinement)
# Steps: fixed-step Float64 RK4IP; convergence by halving the step.

include(joinpath(@__DIR__, "dw_lib.jl"))

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-16-claude-b.7-solver-dwyield"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(RAW)
results_file(stage) = joinpath(RAW, "results_" * stage * ".jsonl")

const G1 = (window_T0=160.0, Nt=4096)
const G2 = (window_T0=256.0, Nt=16384)
const G3 = (window_T0=384.0, Nt=32768)

function say(stage, recs)
    for r in recs
        @printf("%-10s %-22s xi=%.3f nst=%6d Nt=%5d  etaB=%.6e etaDW=%.6e etaDWs=%.6e  pk=%.2fdB(in) %.2fdB(out) w=%.3f edge=%s loc=%.2fdB w=%.3f  dE=%.2e dP=%.2e dH=%.2e  t=%.1fs\n",
                stage, r["label"], r["xi"], r["nsteps"], r["Nt"], r["eta_B"], r["eta_DW"],
                r["eta_DW_smoothgate"], r["peak_band_max_dB_rel_input_max"],
                r["peak_band_max_dB_rel_output_max"], r["peak_band_max_w"],
                r["peak_band_max_at_band_edge"], r["peak_local_dB_rel_input_max"],
                r["peak_local_w"], r["E_rel_drift"], r["P_abs_drift"], r["H_rel_drift"],
                r["t_wall_s"])
    end
    flush(stdout)
end

function go(c::DWCase, stage; save_raw=true, only_last=false)
    recs, _, _ = run_case(c; stage, results=results_file(stage), rawdir=RAW, save_raw)
    say(stage, only_last ? recs[end:end] : recs)
    return recs
end

# ---------------- linear convention test ----------------
"""
gamma = 0 (n2 = 0). Checks (a) a field exp(-tau^2/(2 s^2) - i w1 tau) peaks at
+w1 on the solver's frequency axis, (b) A_k(xi)/A_k(0) = exp(i D(w_k) xi) with
D = delta3 w^3 - w^2/2 (against three alternatives), (c) a packet centred at
w1 is delayed by D'(w1) xi = (3 delta3 w1^2 - w1) xi (positive = trailing).
"""
function stage_lin()
    stage = "lin"
    c = DWCase(; label="lin", pulse=:gauss, N=1.0, delta3=0.05, xi=0.05,
               window_T0=160.0, Nt=4096, nsteps=10)
    s = build(c; linear=true)
    out = Dict{String,Any}("stage" => stage, "label" => "lin_phase", "delta3" => c.delta3,
                           "xi" => c.xi, "Nt" => c.Nt, "window_T0" => c.window_T0)
    # (b) phase law on a broadband input (s = 0.15)
    init = zeros(ComplexF64, c.Nt, 1, 1)
    init[:, 1, 1] .= exp.(-s.tau .^ 2 ./ (2 * 0.15^2))
    sol = solve_mmgnlse(init, s.params, dz(c))
    A0 = spec(sol.fields[:, 1, 1, 1])
    A1 = spec(sol.fields[:, 1, 1, end])
    sig = abs2.(A0) .> 1e-20 * maximum(abs2.(A0))
    w = s.w
    r = A1[sig] ./ A0[sig]
    hyp = Dict(
        "D_task(+d3w3-w2/2)" => c.delta3 .* w .^ 3 .- w .^ 2 ./ 2,
        "D_flipped_axis(-d3w3-w2/2)" => -c.delta3 .* w .^ 3 .- w .^ 2 ./ 2,
        "minus_D(-d3w3+w2/2)" => -(c.delta3 .* w .^ 3 .- w .^ 2 ./ 2),
        "D_no_1/6(+6d3w3-w2/2)" => 6 .* c.delta3 .* w .^ 3 .- w .^ 2 ./ 2)
    for (name, D) in hyp
        out["maxabs_err_" * name] = maximum(abs.(r .- exp.(1im .* D[sig] .* c.xi)))
    end
    out["n_bins_tested"] = count(sig)
    out["w_range_tested"] = [minimum(w[sig]), maximum(w[sig])]
    out["max_phase_D_xi_tested"] = maximum(abs.((c.delta3 .* w[sig] .^ 3 .- w[sig] .^ 2 ./ 2) .* c.xi))
    # (a) axis sign: carrier offset w1 = +5 written as exp(-i w1 tau)
    w1 = 5.0
    a = exp.(-s.tau .^ 2 ./ 2 .- 1im .* w1 .* s.tau)
    out["axis_test_input_exp(-i*5*tau)_peak_w"] = w[argmax(abs2.(spec(a)))]
    # (c) group delay of a packet at w1 = 10 after xi = 2, delta3 = 0.05
    c2 = DWCase(; label="lin_gd", pulse=:gauss, N=1.0, delta3=0.05, xi=2.0,
                window_T0=160.0, Nt=4096, nsteps=10)
    s2 = build(c2; linear=true)
    w1 = 10.0
    init2 = zeros(ComplexF64, c2.Nt, 1, 1)
    init2[:, 1, 1] .= exp.(-s2.tau .^ 2 ./ (2 * 3.0^2) .- 1im .* w1 .* s2.tau)
    sol2 = solve_mmgnlse(init2, s2.params, dz(c2))
    P = abs2.(sol2.fields[:, 1, 1, end])
    out["gd_packet_w1"] = w1
    out["gd_centroid_tau"] = sum(s2.tau .* P) / sum(P)
    out["gd_predicted_tau(3d3w1^2-w1)xi"] = (3 * c2.delta3 * w1^2 - w1) * c2.xi
    open(results_file(stage), "a") do io
        println(io, jsonval(out))
    end
    for (k, v) in sort(collect(out); by=first)
        println(rpad(k, 40), " ", v)
    end
end

# ---------------- timing ----------------
function stage_timing()
    for (g, n) in ((G1, 200), (G2, 200))
        c = DWCase(; label="timing", N=2.0, delta3=0.02, xi=0.2, nsteps=n, g...)
        s = build(c)
        solve_mmgnlse(s.initial, s.params, dz(c))   # compile
        t0 = time()
        solve_mmgnlse(s.initial, s.params, dz(c))
        @printf("timing Nt=%d: %.2f ms/step\n", c.Nt, (time() - t0) / n * 1e3)
    end
    c = DWCase(; label="timing", N=2.0, delta3=0.02, xi=0.2, nsteps=200, raman=true, T0=0.05, G1...)
    s = build(c)
    solve_mmgnlse(s.initial, s.params, dz(c))
    t0 = time()
    solve_mmgnlse(s.initial, s.params, dz(c))
    @printf("timing Raman Nt=%d: %.2f ms/step\n", c.Nt, (time() - t0) / 200 * 1e3)
    flush(stdout)
end

# ---------------- item 1: Roy check, sech N=2, xi=4 ----------------
const D3_ITEM1 = (0.02, 0.03, 0.04, 0.06, 0.10)
item1(d3; nsteps=4000, g=G1, tag="G1") =
    DWCase(; label=@sprintf("sechN2_d%.3f_%s_n%d", d3, tag, nsteps), pulse=:sech, N=2.0,
           delta3=d3, xi=4.0, nsteps=nsteps, g...)

stage_item1() = for d3 in D3_ITEM1; go(item1(d3), "item1"); end
stage_item1_conv() = for d3 in D3_ITEM1; go(item1(d3; nsteps=8000), "item1_conv"; save_raw=false); end

# ---------------- item 2: gated yield law, sech N=2, xi=4 ----------------
const D3_ITEM2 = (0.010, 0.012, 0.014, 0.016, 0.020, 0.025, 0.030)
item2(d3; nsteps=4000, g=G2, tag="G2") =
    DWCase(; label=@sprintf("sechN2_d%.3f_%s_n%d", d3, tag, nsteps), pulse=:sech, N=2.0,
           delta3=d3, xi=4.0, nsteps=nsteps, g...)

stage_item2() = for d3 in D3_ITEM2; go(item2(d3), "item2"); end
stage_item2_conv() = for d3 in D3_ITEM2; go(item2(d3; nsteps=8000), "item2_conv"; save_raw=false); end
stage_item2_grid() = go(item2(0.010; nsteps=8000, g=G3, tag="G3"), "item2_grid")

"""
Floor/reference: delta3 = 0 (pure NLSE, integrable N=2 breather, no DW), same grid
and step; observables evaluated with each item-2 band edge w_z = 1/(6 delta3).
"""
function stage_item2_ref()
    stage = "item2_ref"
    for nst in (4000, 8000)
        c0 = DWCase(; label="ref", pulse=:sech, N=2.0, delta3=0.0, xi=4.0, nsteps=nst, G2...)
        s = build(c0)
        t0 = time()
        sol = solve_mmgnlse(s.initial, s.params, dz(c0))
        tw = time() - t0
        At0 = sol.fields[:, 1, 1, 1]
        for d3 in D3_ITEM2
            c = DWCase(; label=@sprintf("sechN2_d0_band%.3f_G2_n%d", d3, nst), pulse=:sech,
                       N=2.0, delta3=0.0, band_delta3=d3, xi=4.0, nsteps=nst, G2...)
            for jz in (1, length(sol.z))
                At = sol.fields[:, 1, 1, jz]
                rec = case_record(c)
                rec["stage"] = stage
                rec["xi"] = sol.z[jz]
                rec["nsteps_actual"] = length(sol.cache.integration_z) - 1
                rec["t_wall_s"] = tw
                merge!(rec, observables(c, s, At0, At))
                inv0 = invariants(c, At0)
                inv = invariants(c, At)
                rec["E_rel_drift"] = inv.E / inv0.E - 1
                rec["P_abs_drift"] = inv.P - inv0.P
                rec["H_rel_drift"] = inv.H / inv0.H - 1
                open(results_file(stage), "a") do io
                    println(io, jsonval(rec))
                end
                say(stage, [rec])
            end
        end
    end
end

# ---------------- item 3: TL Gaussian card regime ----------------
const ITEM3 = ((3.0, 0.02, 4000), (3.0, 0.05, 4000), (6.0, 0.03, 8000),
               (8.0, 0.05, 16000), (10.0, 0.05, 20000))
item3(N, d3, nst; g=G2, tag="G2") =
    DWCase(; label=@sprintf("gaussN%g_d%.3f_%s_n%d", N, d3, tag, nst), pulse=:gauss, N=N,
           delta3=d3, xi=2.0, nsteps=nst, save_xi=[0.5, 1.0, 1.5, 2.0], g...)

stage_item3() = for (N, d3, nst) in ITEM3; go(item3(N, d3, nst), "item3"); end
stage_item3_conv() = for (N, d3, nst) in ITEM3; go(item3(N, d3, 2nst), "item3_conv"; save_raw=false); end
stage_item3_grid() = go(item3(10.0, 0.05, 40000; g=G3, tag="G3"), "item3_grid")

# ---------------- item 4: Raman (M1), T0 = 50 fs ----------------
const D3_ITEM4 = (0.02, 0.03, 0.04)
item4(d3; nsteps=4000, g=G1, tag="G1") =
    DWCase(; label=@sprintf("sechN2_d%.3f_raman_T50fs_%s_n%d", d3, tag, nsteps), pulse=:sech,
           N=2.0, delta3=d3, xi=4.0, T0=0.05, raman=true, nsteps=nsteps, g...)

stage_item4() = for d3 in D3_ITEM4; go(item4(d3), "item4"); end
stage_item4_conv() = for d3 in D3_ITEM4; go(item4(d3; nsteps=8000), "item4_conv"; save_raw=false); end
stage_item4_grid() = go(item4(0.02; nsteps=8000, g=(window_T0=160.0, Nt=8192), tag="G1x2"), "item4_grid")

# grid check for the item-1 points not covered by item 2 (G2, nsteps 8000)
stage_item1_grid() = for d3 in (0.04, 0.06, 0.10)
    go(item1(d3; nsteps=8000, g=G2, tag="G2"), "item1_grid"; save_raw=false)
end

"""
Residual self-steepening check: the momentum and Hamiltonian drifts at omega0 T0 = 1e6
should scale as s = 1/(omega0 T0) if they come from the suppressed self-steepening.
"""
stage_ss() = for w0 in (1.0e7, 1.0e8)
    c = item1(0.04; nsteps=8000)
    c2 = DWCase(; label=@sprintf("sechN2_d0.040_G1_n8000_w0T0_%.0e", w0), pulse=:sech, N=2.0,
                delta3=0.04, xi=4.0, nsteps=8000, omega0T0=w0, G1...)
    go(c2, "ss"; save_raw=false)
end

# xi-resolved yields (diagnostic for the gate timing relative to the N=2 compressions)
stage_item2_xi() = for d3 in (0.012, 0.016, 0.020)
    c = DWCase(; label=@sprintf("sechN2_d%.3f_G2_n4000_xires", d3), pulse=:sech, N=2.0,
               delta3=d3, xi=4.0, nsteps=4000, save_xi=collect(0.05:0.05:4.0), G2...)
    go(c, "item2_xi"; save_raw=false, only_last=true)
end

# Raman kernel / time-step refinement: dt = 0.98 fs and 0.49 fs (window 160 T0, nsteps 8000)
function stage_item4_grid2()
    for d3 in (0.03, 0.04)
        go(item4(d3; nsteps=8000, g=(window_T0=160.0, Nt=8192), tag="G1x2"), "item4_grid2"; save_raw=false)
    end
    for d3 in (0.02, 0.03, 0.04)
        go(item4(d3; nsteps=8000, g=(window_T0=160.0, Nt=16384), tag="G1x4"), "item4_grid2"; save_raw=false)
    end
end

# time-window check for item 3 (field at the G2 window edge up to 1.6e-3 of the peak at N = 8):
# same dtau as G2, window doubled to 512 T0 (Nt 32768), base step
stage_item3_win() = for (N, d3, nst) in ((8.0, 0.05, 16000), (6.0, 0.03, 8000))
    go(item3(N, d3, nst; g=(window_T0=512.0, Nt=32768), tag="W512"), "item3_win"; save_raw=false)
end

# N = 10 time-window check: G2 -> G3 changed eta_DW(2) by 2.3 % (DW content at w >= 32 has group
# delay >= 243 T0 over xi = 2 and wraps into the gate on the 256 T0 window); window 1024 T0, dtau as G2
stage_item3_win10() = go(item3(10.0, 0.05, 20000; g=(window_T0=1024.0, Nt=65536), tag="W1024"),
                         "item3_win10"; save_raw=false)

const STAGES = Dict(
    "lin" => stage_lin, "timing" => stage_timing,
    "item1" => stage_item1, "item1_conv" => stage_item1_conv,
    "item2" => stage_item2, "item2_conv" => stage_item2_conv,
    "item2_grid" => stage_item2_grid, "item2_ref" => stage_item2_ref,
    "item3" => stage_item3, "item3_conv" => stage_item3_conv, "item3_grid" => stage_item3_grid,
    "item4" => stage_item4, "item4_conv" => stage_item4_conv, "item4_grid" => stage_item4_grid,
    "item1_grid" => stage_item1_grid, "ss" => stage_ss,
    "item2_xi" => stage_item2_xi, "item4_grid2" => stage_item4_grid2,
    "item3_win" => stage_item3_win, "item3_win10" => stage_item3_win10)

for st in ARGS
    haskey(STAGES, st) || error("unknown stage $st")
    t0 = time()
    println("=== stage $st start ", time())
    STAGES[st]()
    @printf("=== stage %s done in %.1f s\n", st, time() - t0)
    flush(stdout)
end
