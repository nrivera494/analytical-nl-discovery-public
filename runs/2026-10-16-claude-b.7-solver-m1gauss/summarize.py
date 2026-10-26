"""Summarize run 2026-10-16-claude-b.7-solver-m1gauss into summary.json.

Values: base runs (window 256 T0, Nt 32768, 8000 steps over xi = 2). Fit (claude-b's form):
ln eta_G = c + p ln delta3 - d / delta3, least squares on the four delta3 values (3 parameters).
"""
import glob
import json
import math
import os

import numpy as np

RUN_ID = "2026-10-16-claude-b.7-solver-m1gauss"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}")
HERE = os.path.dirname(os.path.abspath(__file__))
D3 = (0.0055, 0.006, 0.0066, 0.0073)

recs = {}
for fn in sorted(glob.glob(os.path.join(RAW, "results_*.jsonl"))):
    st = os.path.basename(fn)[len("results_"):-len(".jsonl")]
    recs[st] = [json.loads(l) for l in open(fn) if l.strip()]


def find(stage, d3, xi, band=None, nsteps=None):
    for r in recs.get(stage, []):
        if abs(r["delta3"] - d3) > 1e-12 or abs(r["xi"] - xi) > 1e-9:
            continue
        if band is not None and abs(r["band_delta3"] - band) > 1e-12:
            continue
        if nsteps is not None and r["nsteps"] != nsteps:
            continue
        return r
    return None


KEYS = ["eta_G", "eta_B", "eta_G_DWwindow_0.8_1.2", "eta_G_band_below_0.8wDW", "eta_G_above_1.2wDW",
        "eta_B_DWwindow_0.8_1.2", "eta_B_band_below_0.8wDW", "gated_band_max_w", "gated_band_max_at_edge",
        "gated_band_max_dB_rel_input_max", "gated_local_peak_w", "gated_local_peak_dB_rel_input_max",
        "band_max_w", "band_max_at_edge", "band_max_dB_rel_input_max", "energy_frac_inside_abs_tau_lt_15",
        "t_peak_T0", "peak_power_ratio", "output_max_w", "mean_w", "time_edge_power_ratio",
        "spec_max_dB_above_0.8nyq_rel_max", "E_rel_drift", "P_abs_drift", "H_rel_drift", "w_z", "w_DW_est",
        "Nt", "window_T0", "dtau", "dt_fs", "w_max", "nsteps", "dxi", "t_wall_s"]


def pick(r):
    return None if r is None else {k: r.get(k) for k in KEYS}


def rel(a, b):
    return None if (a is None or b is None or b == 0) else a / b - 1


out = {"run_id": RUN_ID,
       "definition": ("M1 (AgarwalRaman 0.18/12.2 fs/32 fs, T0 = 50 fs, omega0 T0 = 1e6), TL Gaussian, N = 3, "
                      "xi = 2. eta_G: band (w >= 1/(6 delta3)) energy after g = 1 - 0.5[tanh(tau+15) - "
                      "tanh(tau-15)], over input energy; eta_B without the gate. Values: window 256 T0, Nt 32768 "
                      "(dt 0.39 fs, w_max 402), 8000 steps. relchange_A_vs_B = X(A)/X(B) - 1."),
       "by_delta3": {}}
vals = {}
for d3 in D3:
    b = find("base", d3, 2.0)
    b0 = find("base", d3, 0.0)
    e = {"value": pick(b),
         "xi_resolved": {f"{xi:.1f}": (lambda r: None if r is None else
                                       {"eta_G": r["eta_G"], "eta_B": r["eta_B"], "t_peak_T0": r["t_peak_T0"],
                                        "mean_w": r["mean_w"], "peak_power_ratio": r["peak_power_ratio"]})(
                             find("base", d3, xi)) for xi in (0.5, 1.0, 1.5)},
         "floor_xi0": None if b0 is None else {"eta_G": b0["eta_G"], "eta_B": b0["eta_B"]}}
    ref = find("ref", 0.0, 2.0, band=d3)
    ref0 = find("ref", 0.0, 0.0, band=d3)
    if ref is not None:
        e["reference_delta3_0_same_band_xi2"] = {k: ref[k] for k in ("eta_G", "eta_B", "eta_G_DWwindow_0.8_1.2",
                                                                     "eta_G_band_below_0.8wDW", "t_peak_T0",
                                                                     "mean_w")}
        e["reference_delta3_0_same_band_xi0"] = None if ref0 is None else {"eta_G": ref0["eta_G"], "eta_B": ref0["eta_B"]}
    c = find("coarse", d3, 2.0)
    h = find("halve", d3, 2.0)
    q = find("q32k", d3, 2.0)
    wnd = find("window", d3, 2.0)
    conv = {}
    if q is not None:
        if h is not None:
            conv["relchange_eta_G_n16000_vs_n32000"] = rel(h["eta_G"], q["eta_G"])
            conv["relchange_eta_B_n16000_vs_n32000"] = rel(h["eta_B"], q["eta_B"])
        conv["eta_G_n32000"] = q["eta_G"]
        conv["eta_B_n32000"] = q["eta_B"]
        conv["relchange_eta_G_n8000_vs_n32000"] = rel(b["eta_G"], q["eta_G"]) if b is not None else None
        conv["relchange_eta_B_n8000_vs_n32000"] = rel(b["eta_B"], q["eta_B"]) if b is not None else None
    if c is not None:
        conv["eta_G_n4000"] = c["eta_G"]
    dtr = find("dt", d3, 2.0)
    if dtr is not None and b is not None:
        conv["eta_G_dt0.195fs_n8000"] = dtr["eta_G"]
        conv["relchange_eta_G_dt0.39fs_vs_dt0.195fs"] = rel(b["eta_G"], dtr["eta_G"])
        conv["relchange_eta_B_dt0.39fs_vs_dt0.195fs"] = rel(b["eta_B"], dtr["eta_B"])
    if c is not None and b is not None:
        conv["relchange_eta_G_n4000_vs_n8000"] = rel(c["eta_G"], b["eta_G"])
        conv["relchange_eta_B_n4000_vs_n8000"] = rel(c["eta_B"], b["eta_B"])
    if h is not None and b is not None:
        conv["relchange_eta_G_n8000_vs_n16000"] = rel(b["eta_G"], h["eta_G"])
        conv["relchange_eta_B_n8000_vs_n16000"] = rel(b["eta_B"], h["eta_B"])
        conv["eta_G_n16000"] = h["eta_G"]
        conv["eta_B_n16000"] = h["eta_B"]
    if wnd is not None and b is not None:
        conv["relchange_eta_G_W256_vs_W512"] = rel(b["eta_G"], wnd["eta_G"])
        conv["relchange_eta_B_W256_vs_W512"] = rel(b["eta_B"], wnd["eta_B"])
        conv["eta_G_W512"] = wnd["eta_G"]
    e["convergence"] = conv
    out["by_delta3"][f"{d3:.4f}"] = e
    if b is not None:
        vals[d3] = b


def fit3(etas):
    d = np.array(sorted(etas))
    y = np.log(np.array([etas[x] for x in d]))
    A = np.column_stack([np.ones_like(d), np.log(d), -1.0 / d])
    coef, res, rank, sv = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    # sensitivity of d to each ln(eta_i): row 3 of the pseudo-inverse
    pinv = np.linalg.pinv(A)
    dof = len(y) - 3
    s2 = float(resid @ resid) / dof if dof > 0 else float("nan")
    cov = s2 * np.linalg.inv(A.T @ A)
    se = np.sqrt(np.diag(cov))
    corr_pd = cov[1, 2] / (se[1] * se[2])
    return {"c": coef[0], "p": coef[1], "d": coef[2], "se_c": se[0], "se_p": se[1], "se_d": se[2],
            "corr_p_d": corr_pd, "dof": dof, "residuals_ln_eta": resid.tolist(),
            "rms_residual": float(np.sqrt(np.mean(resid ** 2))), "cond_design": float(sv[0] / sv[-1]),
            "dd_dln_eta": pinv[2].tolist(), "delta3": d.tolist(), "ln_eta": y.tolist()}


def fit2(etas):
    d = np.array(sorted(etas))
    y = np.log(np.array([etas[x] for x in d]))
    A = np.column_stack([np.ones_like(d), -1.0 / d])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    return {"c": coef[0], "d": coef[1], "rms_residual": float(np.sqrt(np.mean(resid ** 2)))}


levels = {4000: "coarse", 8000: "base", 16000: "halve", 32000: "q32k"}
by_level = {}
for n, st in levels.items():
    got = {d3: find(st, d3, 2.0, nsteps=n) for d3 in D3}
    by_level[n] = {d3: r for d3, r in got.items() if r is not None}
out["eta_G_by_nsteps"] = {str(n): {f"{d3:.4f}": r["eta_G"] for d3, r in lv.items()} for n, lv in by_level.items()}
out["eta_B_by_nsteps"] = {str(n): {f"{d3:.4f}": r["eta_B"] for d3, r in lv.items()} for n, lv in by_level.items()}
fits = {}
for n, lv in by_level.items():
    if len(lv) == 4:
        fits[str(n)] = {"eta_G_3param": fit3({d3: lv[d3]["eta_G"] for d3 in D3}),
                        "eta_G_2param_p0": fit2({d3: lv[d3]["eta_G"] for d3 in D3}),
                        "eta_B_3param": fit3({d3: lv[d3]["eta_B"] for d3 in D3})}
out["fits_by_nsteps"] = fits
# Raman kernel / time-step refinement (window 256, Nt 65536, dt 0.195 fs, 8000 steps)
dtv = {d3: find("dt", d3, 2.0) for d3 in D3}
if all(v is not None for v in dtv.values()) and len(by_level[8000]) == 4:
    fits["dt0.195fs_n8000"] = {"eta_G_3param": fit3({d3: dtv[d3]["eta_G"] for d3 in D3})}
    if len(by_level[32000]) == 4:
        # combined estimate: n32000 values times the dt-refinement factor measured at n8000,
        # and the same with second-order (dt^2) Richardson extrapolation of that factor to dt -> 0
        comb = {d3: by_level[32000][d3]["eta_G"] * dtv[d3]["eta_G"] / by_level[8000][d3]["eta_G"] for d3 in D3}
        rich = {d3: by_level[32000][d3]["eta_G"] * (1 + (dtv[d3]["eta_G"] / by_level[8000][d3]["eta_G"] - 1) * 4 / 3)
                for d3 in D3}
        fits["n32000_x_dtfactor"] = {"eta_G_3param": fit3(comb),
                                     "eta_G_values": {f"{d3:.4f}": comb[d3] for d3 in D3}}
        fits["n32000_x_dtfactor_richardson"] = {"eta_G_3param": fit3(rich),
                                                "eta_G_values": {f"{d3:.4f}": rich[d3] for d3 in D3}}
complete = sorted(int(k) for k in fits if k.isdigit())
if complete:
    nbest = complete[-1]
    out["fit_primary"] = {"nsteps": nbest, **fits[str(nbest)]["eta_G_3param"]}
    if len(complete) > 1:
        out["fit_primary"]["d_change_vs_coarser_levels"] = {
            str(n): fits[str(n)]["eta_G_3param"]["d"] - fits[str(nbest)]["eta_G_3param"]["d"] for n in complete[:-1]}
    for k in ("dt0.195fs_n8000", "n32000_x_dtfactor", "n32000_x_dtfactor_richardson"):
        if k in fits:
            out["fit_primary"][f"d_{k}_minus_primary"] = fits[k]["eta_G_3param"]["d"] - fits[str(nbest)]["eta_G_3param"]["d"]


def clean(x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list):
        return [clean(v) for v in x]
    if isinstance(x, (np.floating,)):
        return clean(float(x))
    return x


json.dump(clean(out), open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print("wrote summary.json; stages:", {k: len(v) for k, v in recs.items()})
