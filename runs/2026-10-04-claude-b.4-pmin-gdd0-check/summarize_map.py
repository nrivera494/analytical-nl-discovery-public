"""Summarize run 2026-10-04-claude-b.4-pmin-length-map.

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-length-map/summarize_map.py [kind]
Reads the per-point TOMLs from ~/analytical-nl-discovery-data/<run-id>/points/ and writes summary.json (or
summary_<kind>.json for a kind other than agarwal) next to this script.
"""
import glob
import json
import math
import os
import re
import sys

import numpy as np

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pminfit import fit_min, interp_at, zero_crossing  # noqa: E402

RUN_ID = "2026-10-04-claude-b.4-pmin-gdd0-check"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}/points")
KIND = sys.argv[1] if len(sys.argv) > 1 else "agarwal"

pts = {}
for f in glob.glob(os.path.join(RAW, f"{KIND}_L*_P*.toml")):
    m = re.search(r"_L([0-9.]+)_P([0-9.]+)\.toml$", f)
    L, P = float(m.group(1)), float(m.group(2))
    pts.setdefault(L, {})[P] = tomllib.load(open(f, "rb"))

TERMS = ("F_bright", "F_shape", "F_phase", "F_partition", "F_Raman")
out = {"run_id": RUN_ID, "task": "T-20261004-claude-interactive-03", "agent": "claude-b.4", "kind": KIND,
       "fit_method": "P_min, F_min: 3-point exact quadratic in ln P through the lowest sampled point and its neighbours "
                     "(primary); 5-point least squares (check). Decomposition interpolated to P_min by a local quadratic "
                     "in ln P. P_G0: first + to - sign change of the bright amplitude c, linear in ln P.",
       "lengths": {}}
for L in sorted(pts):
    d = pts[L]
    P = np.array(sorted(d))
    F = np.array([d[p]["F_total"] for p in P])
    f3 = fit_min(P, F, 3)
    f5 = fit_min(P, F, 5)
    res = {"length_m": L, "n_points": int(len(P)), "fit_3pt": f3, "fit_5pt": f5}
    rows = []
    for p in P:
        x = d[p]
        rows.append({"P_mw": float(p), "F": x["F_total"], **{k: x[k] for k in TERMS},
                     "G": x["transfer_slope_G"], "c": x["bright_amplitude_c"], "T_N": x["T_N"],
                     "n_selected": x["mean_photons_selected"], "N_input": x["input_photons"],
                     "P_out_selected_mw": x["selected_output_power_mw"],
                     "P_out_fiber_mw": x["fiber_output_power_mw"],
                     "noise_dB": 10 * math.log10(x["F_total"]),
                     "temporal_edge_fraction": x["temporal_edge_fraction"],
                     "spectral_edge_fraction": x["spectral_edge_fraction"], "photon_drift": x["photon_drift"],
                     "fiber_output_peak_W": x["fiber_output_peak_W"],
                     "output_sigma_omega_rad_ps": x["output_sigma_omega_rad_ps"],
                     "raman_z_spacing_m": x["raman_z_spacing_m"], "dz_m": x["dz_m"], "nt": x["nt"],
                     "window_ps": x["window_ps"]})
    res["points"] = rows
    res["max_temporal_edge_fraction"] = max(r["temporal_edge_fraction"] for r in rows)
    res["max_spectral_edge_fraction"] = max(r["spectral_edge_fraction"] for r in rows)
    res["max_abs_photon_drift"] = max(abs(r["photon_drift"]) for r in rows)
    # Finite-difference check of the adjoint transfer slope: G_fd = dln n / dln N between neighbours
    gchk = []
    for a, b in zip(rows[:-1], rows[1:]):
        if b["P_mw"] / a["P_mw"] - 1 > 0.1:
            continue
        gfd = math.log(b["n_selected"] / a["n_selected"]) / math.log(b["N_input"] / a["N_input"])
        gmid = 0.5 * (a["G"] + b["G"])
        gchk.append({"P_pair_mw": [a["P_mw"], b["P_mw"]], "G_fd": gfd, "G_adjoint_mean": gmid, "diff": gfd - gmid})
    res["G_finite_difference_check"] = gchk
    if f3.get("ok"):
        Pm = f3["P_min_mw"]
        dec = {k: interp_at(P, [r[k] for r in rows], Pm) for k in TERMS + ("G", "T_N")}
        res["decomposition_at_P_min"] = dec
        # Which term ends the minimum: slopes dX/dlnP from a local quadratic at 1.05 P_min (just above the minimum)
        slopes = {}
        for k in TERMS:
            o = np.argsort(np.abs(np.log(P) - math.log(1.05 * Pm)))[:3]
            co = np.polyfit(np.log(P[o]) - math.log(1.05 * Pm), [rows[i][k] for i in o], 2)
            slopes[k] = float(co[1])
        res["dterm_dlnP_at_1.05_P_min"] = slopes
        rising = {k: v for k, v in slopes.items() if v > 0}
        res["term_ending_minimum"] = max(rising, key=rising.get) if rising else None
        tot = sum(v for v in rising.values())
        res["Raman_share_of_rising_slope"] = slopes["F_Raman"] / tot if tot > 0 else None
        x0 = d[P[0]]
        s = Pm / x0["pin_mw"]
        LD, T0, b2 = x0["L_D_m"], x0["T0_spectral_rms_ps"], x0["beta2_ps2_m"]
        N2TL, N2pk = x0["N2_TL"] * s, x0["N2_chirped_peak"] * s
        Tc = x0["input_fwhm_ps"] / (2 * math.sqrt(math.log(2)))
        N2c = x0["gamma_W_m"] * x0["input_peak_W"] * s * Tc ** 2 / b2
        res["groups_at_P_min"] = {
            "T0_spectral_rms_ps": T0, "L_D_m": LD, "zeta": L / LD, "C_chirp": x0["C_chirp"],
            "Omega_e_T0_red": x0["Omega_e_T0_red"], "N2_TL": N2TL, "N2_chirped_peak": N2pk,
            "phi_NL_chirped_peak": x0["gamma_W_m"] * x0["input_peak_W"] * s * L,
            "L_over_LWB_TL_kappa1": L * math.sqrt(N2TL) / LD,
            "L_over_LWB_chirpedpeak_kappa1": L * math.sqrt(N2pk) / LD,
            "L_over_LWB_chirpedduration_kappa1": L * math.sqrt(N2c) / (Tc ** 2 / b2)}
        res["P_min_times_L_mw_m"] = Pm * L
    zc = zero_crossing(P, [r["c"] for r in rows])
    res["plateau"] = zc if zc else {"P_G0_mw": None, "note": f"no + to - sign change of c up to {P.max():.1f} mW",
                                    "G_at_highest_power": rows[-1]["G"], "highest_power_mw": float(P.max())}
    if zc and f3.get("ok"):
        res["P_min_over_P_G0"] = f3["P_min_mw"] / zc["P_G0_mw"]
    out["lengths"][f"{L:g}"] = res

# Local exponent alpha between neighbouring lengths
Ls = [L for L in sorted(pts) if out["lengths"][f"{L:g}"]["fit_3pt"].get("ok")]
alpha = []
for a, b in zip(Ls[:-1], Ls[1:]):
    pa = out["lengths"][f"{a:g}"]["fit_3pt"]["P_min_mw"]
    pb = out["lengths"][f"{b:g}"]["fit_3pt"]["P_min_mw"]
    pa5 = out["lengths"][f"{a:g}"]["fit_5pt"].get("P_min_mw")
    pb5 = out["lengths"][f"{b:g}"]["fit_5pt"].get("P_min_mw")
    e = {"L_pair_m": [a, b], "L_geometric_mean_m": math.sqrt(a * b),
         "alpha_3pt": -math.log(pb / pa) / math.log(b / a)}
    if pa5 and pb5:
        e["alpha_5pt"] = -math.log(pb5 / pa5) / math.log(b / a)
    ga = out["lengths"][f"{a:g}"].get("plateau", {}).get("P_G0_mw")
    gb = out["lengths"][f"{b:g}"].get("plateau", {}).get("P_G0_mw")
    if ga and gb:
        e["alpha_P_G0"] = -math.log(gb / ga) / math.log(b / a)
    alpha.append(e)
out["alpha"] = alpha
if len(Ls) >= 2:
    x = np.log(Ls)
    y = np.log([out["lengths"][f"{L:g}"]["fit_3pt"]["P_min_mw"] for L in Ls])
    out["global_power_law_fit"] = {"exponent": float(-np.polyfit(x, y, 1)[0]),
                                   "note": "least-squares slope of ln P_min against ln L over all lengths; a summary, "
                                           "not a model"}
name = "summary.json" if KIND == "agarwal" else f"summary_{KIND}.json"
json.dump(out, open(os.path.join(HERE, name), "w"), indent=1)
print("wrote", name)
for L in Ls:
    r = out["lengths"][f"{L:g}"]
    print(f"L={L:5.2f} Pmin3={r['fit_3pt']['P_min_mw']:8.2f} Pmin5={r['fit_5pt'].get('P_min_mw', float('nan')):8.2f} "
          f"Fmin={r['fit_3pt']['F_min']:.4f} bright={r['decomposition_at_P_min']['F_bright']:.3f} "
          f"shape={r['decomposition_at_P_min']['F_shape']:.3f} R={r['decomposition_at_P_min']['F_Raman']:.4f} "
          f"G={r['decomposition_at_P_min']['G']:.3f} PG0={r['plateau'].get('P_G0_mw')} "
          f"ratio={r.get('P_min_over_P_G0')} ends={r['term_ending_minimum']} Rshare={r['Raman_share_of_rising_slope']:.3f} "
          f"L/LWB(pk)={r['groups_at_P_min']['L_over_LWB_chirpedpeak_kappa1']:.2f} phi={r['groups_at_P_min']['phi_NL_chirped_peak']:.2f} "
          f"n={r['n_points']}")
for e in alpha:
    print("alpha", e)
print("global", out.get("global_power_law_fit"))
