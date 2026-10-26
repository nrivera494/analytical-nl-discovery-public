"""Build summary.json from the per-case JSON files in the raw folder
(<case>.json from run_check.jl, bandlimited_<case>.json from bandlimited.py,
ideal_compare_<case>.json from ideal_b0_compare.py).

Usage: ~/agent-work/venv/bin/python runs/2026-10-10-claude-a-solver-dispersion-check/make_summary.py
"""
import json
import os

RUN_ID = "2026-10-10-claude-a-solver-dispersion-check"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}")
HERE = os.path.dirname(os.path.abspath(__file__))

MAIN = ["b0", "p0.1", "m0.1", "p1", "m1"]
DZ_PAIRS = [("m1", "m1_dzhalf"), ("m0.1", "m0.1_dzhalf"), ("b0", "b0_dzhalf")]
DIAG = ["b0_selfsteep", "m0.1_nt400", "b0_nt400"]
WB_HEADLINE = 40.0

KEEP = ["beta2_ps2_per_m", "x", "nt", "dt_ps", "dz_m", "nsteps", "omega0_rad_per_ps",
        "lambda_min", "lambda_min_from_svd_of_S", "lambda_gen", "n_bins_kept",
        "lambda_max", "lambda_gen_max", "path", "fd_check_max_rel_err",
        "symplectic_defect_max_abs", "nonlocal_fraction_of_S", "energy_drift",
        "edge_energy_fraction_5pct", "peak_phase_check_rad", "wall_s", "role"]


def load(name, prefix=""):
    path = os.path.join(RAW, prefix + name + ".json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def band_value(bl, wb):
    if bl is None or wb not in bl["omega_B_rad_per_ps"]:
        return None
    return bl["lambda_min_band"][bl["omega_B_rad_per_ps"].index(wb)]


def rel(a, b):
    if a is None or b is None:
        return None
    return abs(a - b) / abs(b)


cases = {}
for name in MAIN + [p[1] for p in DZ_PAIRS] + DIAG:
    d = load(name)
    if d is None:
        continue
    c = {k: d[k] for k in KEEP if k in d}
    c["lambda_min_full_V"] = c["lambda_min"]
    affected = c["beta2_ps2_per_m"] == 0.0
    c["lambda_min_window_affected"] = affected
    c["lambda_min_note"] = (
        "lambda_min = smallest eigenvalue of the full 2N x 2N V, as requested. " +
        ("NOT usable at beta2 = 0: the exact time-local map gives 0.0098049; the solver's smaller value comes from "
         "a mode at the edge of the frequency band created by the solver's nonlinear anti-alias window "
         "(see min_mode_of_full_V, ideal_time_local_map_same_grid); use lambda_min_band_<wB> inside the flat band."
         if affected else
         "The minimizing mode lies inside the flat part of the window (see min_mode_of_full_V and "
         "lambda_min_band), so the window does not set it."))
    bl = load(name, "bandlimited_")
    if bl is not None:
        c["lambda_min_band"] = {f"{wb:g}": v for wb, v in zip(bl["omega_B_rad_per_ps"], bl["lambda_min_band"])}
        c[f"lambda_min_band_{WB_HEADLINE:g}"] = band_value(bl, WB_HEADLINE)
        c["lambda_min_band_60"] = band_value(bl, 60.0)
        c["lambda_gen_rel_change_if_output_outside_60_rad_per_ps_replaced_by_vacuum"] = \
            bl["lambda_gen_rel_change_out_of_band_vacuum"]
        c["window_rolloff_start_rad_per_ps"] = bl["window_rolloff_start_rad_per_ps"]
        if "ideal_lambda_min_band" in bl:
            c["ideal_time_local_map_same_grid"] = {
                "lambda_min_full_V": bl["ideal_lambda_min_full"],
                "lambda_min_band": {f"{wb:g}": v for wb, v in
                                    zip(bl["omega_B_rad_per_ps"], bl["ideal_lambda_min_band"])},
            }
    em = load(name, "eigmode_")
    if em is not None:
        c["min_mode_of_full_V"] = {k: v for k, v in em.items() if k.startswith("min_mode")}
    ic = load(name, "ideal_compare_")
    if ic is not None:
        c.setdefault("ideal_time_local_map_same_grid", {})
        c["ideal_time_local_map_same_grid"].update({
            "lambda_gen": ic["ideal_lambda_gen"],
            "rel_diff_lambda_gen_solver_vs_ideal": ic["rel_diff_lambda_gen_solver_vs_ideal"],
            "rel_diff_lambda_min_full_solver_vs_ideal": ic["rel_diff_lambda_min_solver_vs_ideal"],
            "rel_fro_S_minus_ideal": ic["rel_fro_S_minus_ideal"],
            "max_abs_Abar_minus_ideal_over_peak": ic["max_abs_Abar_minus_ideal_over_peak"],
        })
    cases[name] = c

dz_checks = []
for base, half in DZ_PAIRS:
    if base not in cases or half not in cases:
        continue
    a, b = cases[base], cases[half]
    entry = {"case": base, "compared_with": half, "dz_m": [a["dz_m"], b["dz_m"]]}
    for key in ("lambda_min_full_V", f"lambda_min_band_{WB_HEADLINE:g}", "lambda_min_band_60", "lambda_gen"):
        entry[key] = [a.get(key), b.get(key)]
        entry["rel_change_" + key] = rel(a.get(key), b.get(key))
    vals = [v for k, v in entry.items() if k.startswith("rel_change_") and v is not None]
    entry["max_rel_change"] = max(vals)
    entry["passes_1e-3"] = max(vals) < 1e-3
    dz_checks.append(entry)
    cases[base]["dz_convergence"] = {k: v for k, v in entry.items() if k.startswith("rel_change_") or k in ("compared_with", "max_rel_change", "passes_1e-3")}

summary = {
    "run_id": RUN_ID,
    "agent": "claude-a.1",
    "task": "T-20261010-claude-interactive-04",
    "physics": "scalar NLSE (Agrawal sign convention), Kerr only, Gaussian A=sqrt(P0)exp(-T^2/2T0^2), T0=1 ps, "
               "Phi=gamma P0 L=5, L=1 m, x=Phi^2 L |beta2|/T0^2, coherent input; self-steepening suppressed by "
               "omega0=2pi*193.4e3 rad/ps (except b0_selfsteep, physical omega0)",
    "Phi": 5.0,
    "exact_dispersionless_lambda_min_(sqrt(1+Phi^2)-Phi)^2": (26 ** 0.5 - 5) ** 2,
    "definitions": {
        "lambda_min_full_V": "smallest eigenvalue of V = S S^T over all 2N time-bin quadratures (shot noise 1)",
        "lambda_min_band_<wB>": "smallest eigenvalue of V compressed to output quadratures with |omega| <= wB "
                                "rad/ps (N-point DFT bins); input keeps all 2N vacuum modes",
        "lambda_gen": "smallest eigenvalue of the spectral amplitude-quadrature covariance V_amp "
                      "(4x zero padding, bins with |Abar_k|^2 >= 1e-6 max, padded samples vacuum)",
    },
    "window_artifact": (
        "solve_mmgnlse multiplies the nonlinear term by damped_freq_window(nt) (src/backend/fft_utils.jl): "
        "1 for negative detuning, rolling off above 0.34 nt domega on the positive side (68 rad/ps for nt=512, "
        "53 rad/ps for nt=400; ~0.013 at the positive Nyquist). Single-time-bin quadratures have flat spectra, so "
        "the full-V lambda_min is corrupted: at beta2=0 the solver gives 0.0048058 against 0.0098049 for the exact "
        "time-local map on the same grid, the map is not symplectic (max|S J S^T - J| = 2.0). Output modes inside "
        "|omega| <= 60 rad/ps (nt=512) are unaffected: lambda_min_band agrees with the exact map to ~1e-8 relative. "
        "lambda_gen agrees with the exact map to 3e-9 and changes by 3e-11 if all output modes outside 60 rad/ps "
        "are replaced by vacuum."),
    "minimizing_mode_note": (
        "beta2 > 0: the most-squeezed mode of the full V sits near omega = 0 at T = 0 (rms width 0.17 ps at x=0.1, "
        "0.35 ps at x=1). beta2 < 0: it is a modulation-instability sideband pair at +-49.5 rad/ps (x=0.1) and "
        "+-17.3 rad/ps (x=1), near sqrt(2 gamma P0/|beta2|) = sqrt(2 Phi^3/x)/T0, with lambda_min ~ 5e-5, close to "
        "exp(-2 Phi) = 4.5e-5. beta2 = 0: a band-edge mode (|omega| ~ 95 rad/ps) created by the anti-alias window."),
    "dz_convergence_note": (
        "Halving dz checked on m1 (largest |beta2|, MI-dominated): all quantities change by < 2e-7 relative. "
        "b0_dzhalf and m0.1_dzhalf were not run (time budget); for b0 the comparison with the exact time-local map "
        "(lambda_gen 3e-9, lambda_min_band_60 1e-8 relative) bounds the step error."),
    "self_steepening_note": (
        "b0_selfsteep (physical omega0 = 2 pi 193.4 rad/ps, s = 1/(omega0 T0) = 8.2e-4): lambda_gen changes by "
        "+5.7e-6 relative, lambda_min_band_60 by +0.18%, mean output field by 2.3% of peak, against the shock-free map."),
    "not_run": ["m0.1_nt400", "b0_nt400", "b0_dzhalf", "m0.1_dzhalf"],
    "main_cases": MAIN,
    "cases": cases,
    "dz_convergence_checks": dz_checks,
}
with open(os.path.join(HERE, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
for k, v in cases.items():
    print(k, v.get("beta2_ps2_per_m"), v.get("x"), "full", v.get("lambda_min_full_V"),
          "band40", v.get(f"lambda_min_band_{WB_HEADLINE:g}"), "band60", v.get("lambda_min_band_60"),
          "gen", v.get("lambda_gen"), "kept", v.get("n_bins_kept"))
print(json.dumps(dz_checks, indent=1))
