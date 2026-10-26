# Run 2026-10-16-claude-b.7-solver-m1gauss (agent claude-b.7, task T-20261016-claude-interactive-03,
# problem P-20261016-claude-interactive-01), item 7 requested by claude-b.
#
# Model M1: i u_xi + (1/2) u_tautau + N^2 [(1-f_R)|u|^2 + f_R (h_R * |u|^2)] u = i delta3 u_tautautau,
# AgarwalRaman(fraction 0.18, tau1 12.2 fs, tau2 32 fs) at T0 = 50 fs, self-steepening suppressed
# (omega0 T0 = 1e6). Launch TL Gaussian u0 = exp(-tau^2/2), N = 3, xi_f = 2,
# delta3 in {0.0055, 0.006, 0.0066, 0.0073}.
# Observables at xi (all divided by the input energy sum_k |A_k(0)|^2), band w = Omega T0 >= 1/(6 delta3):
#   eta_B = band energy;  eta_G = band energy after g = 1 - 0.5[tanh(tau+15) - tanh(tau-15)].
# Model mapping and helpers: dw_lib.jl (copy of runs/2026-10-16-claude-b.7-solver-dwyield/dw_lib.jl).
#
# Usage (repository root):
#   JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no \
#       runs/2026-10-16-claude-b.7-solver-m1gauss/run_m1g.jl <stage> [<stage> ...]

include(joinpath(@__DIR__, "dw_lib.jl"))

FFTW.set_num_threads(1)
BLAS.set_num_threads(1)

const RUN_ID = "2026-10-16-claude-b.7-solver-m1gauss"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
mkpath(RAW)
results_file(stage) = joinpath(RAW, "results_" * stage * ".jsonl")

const GB = (window_T0=256.0, Nt=32768)     # dtau 0.0078 (0.39 fs), w_max 402
const GW = (window_T0=512.0, Nt=65536)     # same dtau, window doubled
const D3 = (0.0055, 0.006, 0.0066, 0.0073)

gate15(tau) = 1 .- 0.5 .* (tanh.(tau .+ 15) .- tanh.(tau .- 15))

m1g(d3; nsteps=8000, g=GB, tag="GB", band_delta3=NaN) =
    DWCase(; label=@sprintf("gaussN3_d%.4f_raman_T50fs_%s_n%d", d3, tag, nsteps), pulse=:gauss,
           N=3.0, delta3=d3, xi=2.0, T0=0.05, raman=true, nsteps=nsteps,
           save_xi=[0.5, 1.0, 1.5, 2.0], band_delta3=band_delta3, g...)

function obs7(c::DWCase, s, At0, At)
    w = s.w
    d3b = band_d3(c)
    wzb = 1 / (6 * d3b)
    wdw = 1 / (2 * d3b)
    band = w .>= wzb
    S0 = abs2.(spec(At0))
    Ein = sum(S0)
    S = abs2.(spec(At))
    g = gate15(s.tau)
    Sg = abs2.(spec(At .* g))
    win = (w .>= 0.8 * wdw) .& (w .<= 1.2 * wdw)
    lo = band .& (w .< 0.8 * wdw)
    hi = w .> 1.2 * wdw
    pkg = band_peak(w, Sg, band)
    pk = band_peak(w, S, band)
    P = abs2.(At)
    inside = abs.(s.tau) .< 15
    nedge = max(1, c.Nt ÷ 50)
    nyq = maximum(abs.(w))
    hiw = abs.(w) .> 0.8 * nyq
    return Dict{String,Any}(
        "w_z" => wzb, "w_DW_est" => wdw,
        "eta_B" => sum(S[band]) / Ein, "eta_G" => sum(Sg[band]) / Ein,
        "eta_G_DWwindow_0.8_1.2" => sum(Sg[win]) / Ein,
        "eta_G_band_below_0.8wDW" => sum(Sg[lo]) / Ein,
        "eta_G_above_1.2wDW" => sum(Sg[hi]) / Ein,
        "eta_B_DWwindow_0.8_1.2" => sum(S[win]) / Ein,
        "eta_B_band_below_0.8wDW" => sum(S[lo]) / Ein,
        "gated_band_max_w" => w[pkg.j], "gated_band_max_at_edge" => pkg.at_edge,
        "gated_band_max_dB_rel_input_max" => db(Sg[pkg.j] / maximum(S0)),
        "gated_local_peak_w" => pkg.jl > 0 ? w[pkg.jl] : NaN,
        "gated_local_peak_dB_rel_input_max" => pkg.jl > 0 ? db(Sg[pkg.jl] / maximum(S0)) : NaN,
        "band_max_w" => w[pk.j], "band_max_at_edge" => pk.at_edge,
        "band_max_dB_rel_input_max" => db(S[pk.j] / maximum(S0)),
        "energy_frac_inside_abs_tau_lt_15" => sum(P[inside]) / sum(P),
        "t_peak_T0" => s.tau[argmax(P)], "peak_power_ratio" => maximum(P) / P0(c),
        "output_max_w" => w[argmax(S)], "mean_w" => sum(w .* S) / sum(S),
        "time_edge_power_ratio" => maximum(P[[1:nedge; end-nedge+1:end]]) / maximum(P),
        "spec_max_dB_above_0.8nyq_rel_max" => db(maximum(S[hiw]) / maximum(S)))
end

function run7(c::DWCase, stage; save_raw=true, extra_bands=())
    s = build(c)
    t0 = time()
    sol = solve_mmgnlse(s.initial, s.params, dz(c); saveat=c.save_xi)
    tw = time() - t0
    At0 = sol.fields[:, 1, 1, 1]
    inv0 = invariants(c, At0)
    cases = isempty(extra_bands) ? [c] :
            [DWCase(; label=replace(c.label, "_d0.0000" => @sprintf("_d0_band%.4f", b)), pulse=c.pulse,
                    N=c.N, delta3=c.delta3, xi=c.xi, T0=c.T0, raman=c.raman, nsteps=c.nsteps,
                    save_xi=c.save_xi, band_delta3=b, window_T0=c.window_T0, Nt=c.Nt)
             for b in extra_bands]
    for cc in cases, (jz, z) in enumerate(sol.z)
        At = sol.fields[:, 1, 1, jz]
        rec = case_record(cc)
        rec["stage"] = stage
        rec["xi"] = z
        rec["nsteps_actual"] = length(sol.cache.integration_z) - 1
        rec["t_wall_s"] = tw
        merge!(rec, obs7(cc, s, At0, At))
        inv = invariants(cc, At)
        rec["E_rel_drift"] = inv.E / inv0.E - 1
        rec["P_abs_drift"] = inv.P - inv0.P
        rec["H_rel_drift"] = inv.H / inv0.H - 1
        open(results_file(stage), "a") do io
            println(io, jsonval(rec))
        end
        if z == sol.z[end] || z == 0
            @printf("%-9s %-40s xi=%.2f n=%5d Nt=%5d  etaB=%.6e  etaG=%.6e  win=%.3e lo=%.3e hi=%.3e  gpk=%.2fdB@%.2f(edge=%s) loc=%.2fdB@%.2f  tpk=%.2f <w>=%.3f in15=%.2e dE=%.1e  (%.0fs)\n",
                    stage, cc.label, z, cc.nsteps, cc.Nt, rec["eta_B"], rec["eta_G"],
                    rec["eta_G_DWwindow_0.8_1.2"], rec["eta_G_band_below_0.8wDW"], rec["eta_G_above_1.2wDW"],
                    rec["gated_band_max_dB_rel_input_max"], rec["gated_band_max_w"], rec["gated_band_max_at_edge"],
                    rec["gated_local_peak_dB_rel_input_max"], rec["gated_local_peak_w"],
                    rec["t_peak_T0"], rec["mean_w"], rec["energy_frac_inside_abs_tau_lt_15"],
                    rec["E_rel_drift"], tw)
            flush(stdout)
        end
    end
    if save_raw
        AtL = sol.fields[:, 1, 1, end]
        npzwrite(joinpath(RAW, "$(stage)_$(c.label).npz"),
                 Dict("w" => collect(s.w), "tau" => collect(s.tau),
                      "S_in" => abs2.(spec(At0)), "S_out" => abs2.(spec(AtL)),
                      "S_out_gated" => abs2.(spec(AtL .* gate15(s.tau))), "P_out" => abs2.(AtL)))
    end
end

const STAGES = Dict(
    "baseA" => () -> for d3 in D3[1:2]; run7(m1g(d3), "base"); end,
    "baseB" => () -> for d3 in D3[3:4]; run7(m1g(d3), "base"); end,
    "halve" => () -> run7(m1g(0.0055; nsteps=16000), "halve"; save_raw=false),
    "halve2" => () -> run7(m1g(0.0073; nsteps=16000), "halve"; save_raw=false),
    "coarse" => () -> for d3 in D3; run7(m1g(d3; nsteps=4000), "coarse"; save_raw=false); end,
    # added after the first convergence results: the 4000 -> 8000 -> 16000 changes at delta3 = 0.0055 were
    # +1.25e-4 and +1.53e-4 (not shrinking), so the step is refined further
    "q32k" => () -> run7(m1g(0.0055; nsteps=32000), "q32k"; save_raw=false),
    "q32kb" => () -> run7(m1g(0.0073; nsteps=32000), "q32k"; save_raw=false),
    # 32000 steps at the two middle delta3 so that the fit can use one step size throughout
    "q32kc" => () -> run7(m1g(0.006; nsteps=32000), "q32k"; save_raw=false),
    "q32kd" => () -> run7(m1g(0.0066; nsteps=32000), "q32k"; save_raw=false),
    # Raman kernel / time step 0.39 -> 0.195 fs (window 256 T0, Nt 65536, w_max 804), 8000 steps
    "dtA" => () -> run7(m1g(0.0055; g=(window_T0=256.0, Nt=65536), tag="GBx2"), "dt"; save_raw=false),
    "dtB" => () -> run7(m1g(0.0073; g=(window_T0=256.0, Nt=65536), tag="GBx2"), "dt"; save_raw=false),
    # residual self-steepening check (added after the freeze and after reading claude-b's values):
    # omega0 T0 = 1e8 instead of 1e6, base grid, 8000 steps
    "ssA" => () -> run7(DWCase(; label="gaussN3_d0.0055_raman_T50fs_GB_n8000_w0T0_1e8", pulse=:gauss, N=3.0,
                               delta3=0.0055, xi=2.0, T0=0.05, raman=true, nsteps=8000, omega0T0=1.0e8,
                               save_xi=[0.5, 1.0, 1.5, 2.0], GB...), "ss"; save_raw=false),
    "ssB" => () -> run7(DWCase(; label="gaussN3_d0.0073_raman_T50fs_GB_n8000_w0T0_1e8", pulse=:gauss, N=3.0,
                               delta3=0.0073, xi=2.0, T0=0.05, raman=true, nsteps=8000, omega0T0=1.0e8,
                               save_xi=[0.5, 1.0, 1.5, 2.0], GB...), "ss"; save_raw=false),
    "dtC" => () -> run7(m1g(0.006; g=(window_T0=256.0, Nt=65536), tag="GBx2"), "dt"; save_raw=false),
    "dtD" => () -> run7(m1g(0.0066; g=(window_T0=256.0, Nt=65536), tag="GBx2"), "dt"; save_raw=false),
    "window" => () -> run7(m1g(0.0055; g=GW, tag="GW"), "window"; save_raw=false),
    # delta3 = 0 reference (Raman soliton dynamics without a DW resonance), evaluated at the four band edges
    "ref" => () -> run7(m1g(0.0; nsteps=8000), "ref"; save_raw=false, extra_bands=D3),
)

for st in ARGS
    haskey(STAGES, st) || error("unknown stage $st")
    t0 = time()
    println("=== stage $st start")
    STAGES[st]()
    @printf("=== stage %s done in %.1f s\n", st, time() - t0)
    flush(stdout)
end
