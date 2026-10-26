"""Summarize run 2026-10-04-claude-b.4-pmin-length-map.

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-length-map/summarize_map.py [kind]
Reads the per-point TOMLs from ~/analytical-nl-discovery-data/<run-id>/points/ and writes summary.json (or
summary_<kind>.json for a kind other than agarwal) next to this script.

F(P) can have more than one dip below shot noise at one length (found at 5 m in the first pass). Every interior local
minimum of the sampled F(P) with F < 1, below the plateau power P_G0 and with prominence >= 0.003 is fitted by the exact
parabola in ln P through it and its two neighbours. "first" is the lowest-power dip, "global" the deepest.
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
from pminfit import interp_at, zero_crossing  # noqa: E402

RUN_ID = "2026-10-04-claude-b.4-pmin-length-map"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}/points")
KIND = sys.argv[1] if len(sys.argv) > 1 else "agarwal"
TERMS = ("F_bright", "F_shape", "F_phase", "F_partition", "F_Raman")

pts = {}
for f in glob.glob(os.path.join(RAW, f"{KIND}_L*_P*.toml")):
    m = re.search(r"_L([0-9.]+)_P([0-9.]+)\.toml$", f)
    L, P = float(m.group(1)), float(m.group(2))
    pts.setdefault(L, {})[P] = tomllib.load(open(f, "rb"))


def groups(x0, Pm, L):
    s = Pm / x0["pin_mw"]
    LD, b2 = x0["L_D_m"], x0["beta2_ps2_m"]
    N2TL, N2pk = x0["N2_TL"] * s, x0["N2_chirped_peak"] * s
    Tc = x0["input_fwhm_ps"] / (2 * math.sqrt(math.log(2)))
    N2c = x0["gamma_W_m"] * x0["input_peak_W"] * s * Tc ** 2 / b2
    return {"zeta": L / LD, "N2_TL": N2TL, "N2_chirped_peak": N2pk,
            "phi_NL_chirped_peak": x0["gamma_W_m"] * x0["input_peak_W"] * s * L,
            "L_over_LWB_TL_kappa1": L * math.sqrt(N2TL) / LD,
            "L_over_LWB_chirpedpeak_kappa1": L * math.sqrt(N2pk) / LD,
            "L_over_LWB_chirpedduration_kappa1": L * math.sqrt(N2c) / (Tc ** 2 / b2)}


def fit_dip(P, F, rows, i, x0, L, PG0):
    x = np.log(P[i - 1:i + 2])
    a, b, c = np.polyfit(x, F[i - 1:i + 2], 2)
    xv = -b / (2 * a)
    Pm = float(math.exp(xv))
    dip = {"P_min_mw": Pm, "F_min": float(np.polyval([a, b, c], xv)), "curvature_d2F_dlnP2": float(2 * a),
           "points_used_mw": [float(p) for p in P[i - 1:i + 2]], "F_sampled_min": float(F[i]),
           "max_relative_spacing": float(max(P[i] / P[i - 1], P[i + 1] / P[i]) - 1)}
    # flatness: the ln P half-width over which the fitted parabola stays within 0.002 of F_min
    dip["lnP_halfwidth_dF_0.002"] = float(math.sqrt(2 * 0.002 / (2 * a))) if a > 0 else None
    dip["decomposition"] = {k: interp_at(P, [r[k] for r in rows], Pm) for k in TERMS + ("G", "T_N")}
    # output rms spectral width at the dip (rad/ps) and relative to the red filter-edge offset Omega_e
    sw = interp_at(P, [r["output_sigma_omega_rad_ps"] for r in rows], Pm)
    dip["output_sigma_omega_rad_ps"] = sw
    dip["output_sigma_omega_over_Omega_e_red"] = sw / abs(x0["Omega_red_edge_rad_ps"])
    slopes = {}
    for k in TERMS:
        o = np.argsort(np.abs(np.log(P) - math.log(1.05 * Pm)))[:3]
        co = np.polyfit(np.log(P[o]) - math.log(1.05 * Pm), [rows[j][k] for j in o], 2)
        slopes[k] = float(co[1])
    dip["dterm_dlnP_at_1.05_P_min"] = slopes
    rising = {k: v for k, v in slopes.items() if v > 0}
    dip["term_ending_minimum"] = max(rising, key=rising.get) if rising else None
    tot = sum(rising.values())
    dip["Raman_share_of_rising_slope"] = slopes["F_Raman"] / tot if tot > 0 else None
    dip["groups"] = groups(x0, Pm, L)
    dip["P_min_times_L_mw_m"] = Pm * L
    if PG0:
        dip["P_min_over_P_G0"] = Pm / PG0
    return dip


out = {"run_id": RUN_ID, "task": "T-20261004-claude-interactive-03", "agent": "claude-b.4", "kind": KIND,
       "fit_method": "every interior local minimum of the sampled F(P) with F<1, below P_G0, prominence >= 0.003: exact "
                     "parabola in ln P through the sampled minimum and its two neighbours; decomposition interpolated "
                     "to P_min by a local quadratic in ln P. P_G0: first + to - sign change of the bright amplitude c, "
                     "linear in ln P.",
       "lengths": {}}
for L in sorted(pts):
    d = pts[L]
    P = np.array(sorted(d))
    F = np.array([d[p]["F_total"] for p in P])
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
    res = {"length_m": L, "n_points": int(len(P)), "P_range_mw": [float(P.min()), float(P.max())]}
    zc = zero_crossing(P, [r["c"] for r in rows])
    PG0 = zc["P_G0_mw"] if zc else None
    res["plateau"] = zc if zc else {"P_G0_mw": None, "note": f"no + to - sign change of c up to {P.max():.1f} mW"}
    # plateau onset, a less fragile measure than the first zero of G: first power where G falls below 0.25
    Gs = [r["G"] for r in rows]
    k = next((k for k in range(1, len(P)) if Gs[k - 1] >= 0.25 > Gs[k]), None)
    if k is not None:
        x0, x1 = math.log(P[k - 1]), math.log(P[k])
        res["plateau"]["P_G025_mw"] = float(math.exp(x0 + (x1 - x0) * (Gs[k - 1] - 0.25) / (Gs[k - 1] - Gs[k])))
    for key in ("P_G0_mw", "P_G025_mw"):
        if res["plateau"].get(key):
            sw = interp_at(P, [r["output_sigma_omega_rad_ps"] for r in rows], res["plateau"][key])
            res["plateau"][key.replace("_mw", "_output_sigma_omega_rad_ps")] = sw
    top = len(P) if PG0 is None else int(np.searchsorted(P, PG0))
    ok = [r["spectral_edge_fraction"] <= 1e-8 and r["temporal_edge_fraction"] <= 1e-4 for r in rows]
    res["max_spectral_edge_fraction_below_P_G0"] = max(r["spectral_edge_fraction"] for r in rows[:max(top, 1)])
    res["max_abs_photon_drift_below_P_G0"] = max(abs(r["photon_drift"]) for r in rows[:max(top, 1)])
    dips = []
    for i in range(1, min(top, len(P) - 1)):
        if F[i] < F[i - 1] and F[i] < F[i + 1] and F[i] < 1.0 and ok[i - 1] and ok[i] and ok[i + 1]:
            prom = min(F[:i].max(), F[i + 1:max(top, i + 2)].max()) - F[i]
            if prom >= 0.003:
                dd = fit_dip(P, F, rows, i, d[P[0]], L, PG0)
                dd["prominence"] = float(prom)
                dips.append(dd)
    res["dips"] = dips
    for q in dips:
        if res["plateau"].get("P_G025_mw"):
            q["P_min_over_P_G025"] = q["P_min_mw"] / res["plateau"]["P_G025_mw"]
    if dips:
        res["first"] = dips[0]
        res["global"] = min(dips, key=lambda q: q["F_min"])
    res["F_min_sampled_below_P_G0"] = float(F[:max(top, 1)].min())
    res["P_at_F_min_sampled_mw"] = float(P[:max(top, 1)][np.argmin(F[:max(top, 1)])])
    # Finite-difference check of the adjoint transfer slope: G_fd = dln n / dln N between neighbours (<= 6% apart)
    gchk = []
    for a, b in zip(rows[:-1], rows[1:]):
        if b["P_mw"] / a["P_mw"] - 1 > 0.06 or (PG0 and b["P_mw"] > PG0):
            continue
        gfd = math.log(b["n_selected"] / a["n_selected"]) / math.log(b["N_input"] / a["N_input"])
        gchk.append({"P_pair_mw": [a["P_mw"], b["P_mw"]], "G_fd": gfd, "G_adjoint_mean": 0.5 * (a["G"] + b["G"]),
                     "diff": gfd - 0.5 * (a["G"] + b["G"])})
    res["G_finite_difference_check"] = gchk
    res["G_fd_max_abs_diff"] = max((abs(g["diff"]) for g in gchk), default=None)
    res["points"] = rows
    out["lengths"][f"{L:g}"] = res


def alpha_series(key):
    Ls = [L for L in sorted(pts) if key in out["lengths"][f"{L:g}"]]
    al = []
    for a, b in zip(Ls[:-1], Ls[1:]):
        pa = out["lengths"][f"{a:g}"][key]["P_min_mw"]
        pb = out["lengths"][f"{b:g}"][key]["P_min_mw"]
        al.append({"L_pair_m": [a, b], "L_geometric_mean_m": math.sqrt(a * b),
                   "alpha": -math.log(pb / pa) / math.log(b / a)})
    return al


out["alpha_first_dip"] = alpha_series("first")
out["alpha_global_min"] = alpha_series("global")
LsG = [L for L in sorted(pts) if out["lengths"][f"{L:g}"]["plateau"].get("P_G0_mw")]
LsG25 = [L for L in sorted(pts) if out["lengths"][f"{L:g}"]["plateau"].get("P_G025_mw")]
out["alpha_P_G025"] = [{"L_pair_m": [a, b], "L_geometric_mean_m": math.sqrt(a * b),
                        "alpha": -math.log(out["lengths"][f"{b:g}"]["plateau"]["P_G025_mw"] /
                                           out["lengths"][f"{a:g}"]["plateau"]["P_G025_mw"]) / math.log(b / a)}
                       for a, b in zip(LsG25[:-1], LsG25[1:])]
out["alpha_P_G0"] = [{"L_pair_m": [a, b], "L_geometric_mean_m": math.sqrt(a * b),
                      "alpha": -math.log(out["lengths"][f"{b:g}"]["plateau"]["P_G0_mw"] /
                                         out["lengths"][f"{a:g}"]["plateau"]["P_G0_mw"]) / math.log(b / a)}
                     for a, b in zip(LsG[:-1], LsG[1:])]
name = "summary.json" if KIND == "agarwal" else f"summary_{KIND}.json"
json.dump(out, open(os.path.join(HERE, name), "w"), indent=1)
print("wrote", name)
for L in sorted(pts):
    r = out["lengths"][f"{L:g}"]
    pg = r["plateau"].get("P_G0_mw")
    print(f"L={L:5.2f} n={r['n_points']:3d} range={r['P_range_mw'][0]:.0f}-{r['P_range_mw'][1]:.0f} "
          f"PG0={pg if pg is None else round(pg, 1)} PG025={r['plateau'].get('P_G025_mw')} Fmin_sampled={r['F_min_sampled_below_P_G0']:.4f} "
          f"at {r['P_at_F_min_sampled_mw']:.1f} Gfd={r['G_fd_max_abs_diff']}")
    for q in r["dips"]:
        print(f"     dip P={q['P_min_mw']:8.2f} F={q['F_min']:.4f} sp={q['max_relative_spacing']:.3f} "
              f"prom={q['prominence']:.3f} bright={q['decomposition']['F_bright']:.3f} "
              f"shape={q['decomposition']['F_shape']:.3f} R={q['decomposition']['F_Raman']:.4f} "
              f"G={q['decomposition']['G']:.3f} ratio={q.get('P_min_over_P_G0')} ends={q['term_ending_minimum']} "
              f"sw={q['output_sigma_omega_rad_ps']:.2f} TN={q['decomposition']['T_N']:.4f} r25={q.get('P_min_over_P_G025')} "
              f"Rshare={q['Raman_share_of_rising_slope']} hw={q['lnP_halfwidth_dF_0.002']} L/LWBpk={q['groups']['L_over_LWB_chirpedpeak_kappa1']:.2f} "
              f"phi={q['groups']['phi_NL_chirped_peak']:.2f}")
for k in ("alpha_first_dip", "alpha_global_min", "alpha_P_G0", "alpha_P_G025"):
    print(k, [(round(e["L_geometric_mean_m"], 3), round(e["alpha"], 3)) for e in out[k]])
