"""Summarize run 2026-10-16-claude-b.7-solver-dwyield into summary.json.

Reads ~/analytical-nl-discovery-data/2026-10-16-claude-b.7-solver-dwyield/results_*.jsonl
(written by run_dw.jl) and writes summary.json next to this script.
Reported value = finest-step run on the base grid; convergence = relative change
against the run with twice the step (and against a refined grid where available).
"""
import glob
import json
import math
import os

RUN_ID = "2026-10-16-claude-b.7-solver-dwyield"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}")
HERE = os.path.dirname(os.path.abspath(__file__))

recs = {}
for fn in sorted(glob.glob(os.path.join(RAW, "results_*.jsonl"))):
    stage = os.path.basename(fn)[len("results_"):-len(".jsonl")]
    with open(fn) as f:
        recs[stage] = [json.loads(line) for line in f if line.strip()]


def rel(a, b):
    if a is None or b is None:
        return None
    if b == 0:
        return None
    return a / b - 1


def pick(stage, **kw):
    out = []
    for r in recs.get(stage, []):
        ok = True
        for k, v in kw.items():
            rv = r.get(k)
            if isinstance(v, float):
                if rv is None or abs(rv - v) > 1e-9 * max(1.0, abs(v)):
                    ok = False
                    break
            elif rv != v:
                ok = False
                break
        if ok:
            out.append(r)
    return out


def last(stage, **kw):
    rs = pick(stage, **kw)
    if not rs:
        return None
    return max(rs, key=lambda r: r["xi"])


def at_xi(stage, xi, **kw):
    for r in pick(stage, **kw):
        if abs(r["xi"] - xi) < 1e-9:
            return r
    return None


OBS = ["eta_B", "eta_DW", "eta_DW_smoothgate",
       "peak_band_max_dB_rel_input_max", "peak_band_max_dB_rel_output_max",
       "peak_band_max_w", "peak_band_max_dnuT0", "peak_band_max_at_band_edge",
       "peak_local_dB_rel_input_max", "peak_local_dB_rel_output_max",
       "peak_local_w", "peak_local_dnuT0",
       "gated_peak_w", "gated_peak_dB_rel_input_max", "output_max_w",
       "E_rel_drift", "P_abs_drift", "H_rel_drift",
       "spec_frac_above_0.8nyq", "spec_max_dB_above_0.8nyq_rel_max",
       "time_edge_power_ratio", "peak_power_ratio", "t_peak_T0", "w_z"]
CONV = ["eta_B", "eta_DW", "eta_DW_smoothgate"]
DCONV = ["peak_band_max_dB_rel_input_max", "peak_local_dB_rel_input_max",
         "peak_band_max_w", "peak_local_w"]


def obs(r):
    return None if r is None else {k: r.get(k) for k in OBS}


def conv(fine, coarse, tag):
    if fine is None or coarse is None:
        return None
    d = {f"relchange_{k}_{tag}": rel(coarse[k], fine[k]) for k in CONV}
    for k in DCONV:
        a, b = coarse.get(k), fine.get(k)
        d[f"absdiff_{k}_{tag}"] = None if (a is None or b is None) else a - b
    return d


def grid_meta(r):
    if r is None:
        return None
    return {k: r[k] for k in ("Nt", "window_T0", "dtau", "w_max", "nsteps", "dxi",
                              "dt_fs", "t_wall_s")}


summary = {"run_id": RUN_ID,
           "notes": ("All yields are energy fractions relative to the total input energy. "
                     "w = Omega T0 (positive = blue). eta_DW uses the hard gate |tau| >= 8 "
                     "as defined in the task; eta_DW_smoothgate (tanh gate, width 1) is a "
                     "diagnostic only.")}

# conventions
lin = recs.get("lin", [])
summary["convention_test"] = lin[-1] if lin else None

# item 1
item1 = {}
for d3 in (0.02, 0.03, 0.04, 0.06, 0.10):
    c = last("item1", delta3=d3)
    f = last("item1_conv", delta3=d3)
    g8 = last("item2_conv", delta3=d3) or last("item1_grid", delta3=d3)
    e = {"value_source": "item1_conv (G1, nsteps 8000)", "value": obs(f),
         "grid": grid_meta(f), "coarse_step": obs(c),
         "conv_step_halving": conv(f, c, "n4000_vs_n8000")}
    if g8 is not None:
        e["conv_grid_G2_n8000_vs_G1_n8000"] = conv(g8, f, "G1_vs_G2")
        e["grid_G2"] = grid_meta(g8)
    item1[f"{d3:.3f}"] = e
summary["item1_roy_check_sech_N2_xi4"] = item1

# item 2
item2 = {}
for d3 in (0.010, 0.012, 0.014, 0.016, 0.020, 0.025, 0.030):
    c = last("item2", delta3=d3)
    f = last("item2_conv", delta3=d3)
    x0 = at_xi("item2", 0.0, delta3=d3)
    ref8 = last("item2_ref", band_delta3=d3, nsteps=8000)
    ref4 = last("item2_ref", band_delta3=d3, nsteps=4000)
    e = {"value_source": "item2_conv (G2, nsteps 8000)",
         "eta_DW": None if f is None else f["eta_DW"],
         "eta_B": None if f is None else f["eta_B"],
         "eta_DW_smoothgate": None if f is None else f["eta_DW_smoothgate"],
         "value": obs(f), "grid": grid_meta(f),
         "conv_step_halving": conv(f, c, "n4000_vs_n8000"),
         "floor_input_xi0": None if x0 is None else
             {"eta_B_xi0": x0["eta_B"], "eta_DW_xi0": x0["eta_DW"],
              "eta_DW_smoothgate_xi0": x0["eta_DW_smoothgate"]},
         "floor_reference_delta3_0_same_band": None if ref8 is None else
             {"eta_B": ref8["eta_B"], "eta_DW": ref8["eta_DW"],
              "eta_DW_smoothgate": ref8["eta_DW_smoothgate"],
              "eta_B_n4000": None if ref4 is None else ref4["eta_B"],
              "eta_DW_n4000": None if ref4 is None else ref4["eta_DW"],
              "eta_DW_smoothgate_n4000": None if ref4 is None else ref4["eta_DW_smoothgate"]}}
    if d3 == 0.010:
        gr = last("item2_grid", delta3=d3)
        e["grid_G3"] = grid_meta(gr)
        e["conv_grid_G3_vs_G2_n8000"] = conv(gr, f, "G2_vs_G3")
        e["value_G3"] = obs(gr)
    item2[f"{d3:.3f}"] = e
summary["item2_gated_yield_sech_N2_xi4"] = item2

# derived: local slopes d ln(eta) / d(1/delta3) between adjacent item-2 points (nsteps 8000, G2)
keys = sorted(item2, key=float)
slopes = {}
for a, b in zip(keys[:-1], keys[1:]):
    ea, eb = item2[a], item2[b]
    da, db_ = float(a), float(b)
    d = {}
    for q in ("eta_DW", "eta_DW_smoothgate", "eta_B"):
        if ea.get(q) and eb.get(q) and ea[q] > 0 and eb[q] > 0:
            d[q] = (math.log(eb[q]) - math.log(ea[q])) / (1 / db_ - 1 / da)
    slopes[f"{a}-{b}"] = d
summary["item2_local_slopes_dln_eta_d_inv_delta3"] = slopes

# xi-resolved yields (diagnostic stage item2_xi)
xr = {}
for r in recs.get("item2_xi", []):
    k = f"{r['delta3']:.3f}"
    xr.setdefault(k, []).append([round(r["xi"], 6), r["eta_B"], r["eta_DW"], r["eta_DW_smoothgate"],
                                 r["peak_power_ratio"]])
for k in xr:
    xr[k].sort()
summary["item2_xi_resolved"] = {"columns": ["xi", "eta_B", "eta_DW", "eta_DW_smoothgate",
                                            "peak_power/P0"], "by_delta3": xr}

# item 3
item3 = {}
for N, d3, nst in ((3.0, 0.02, 4000), (3.0, 0.05, 4000), (6.0, 0.03, 8000),
                   (8.0, 0.05, 16000), (10.0, 0.05, 20000)):
    e = {"value_source": f"item3_conv (G2, nsteps {2 * nst} over xi = 2)", "by_xi": {}}
    for xi in (0.0, 0.5, 1.0, 1.5, 2.0):
        c = at_xi("item3", xi, N=N, delta3=d3)
        f = at_xi("item3_conv", xi, N=N, delta3=d3)
        e["by_xi"][f"{xi:.1f}"] = {
            "eta_B": None if f is None else f["eta_B"],
            "eta_B_coarse": None if c is None else c["eta_B"],
            "relchange_eta_B_step_halving": None if (c is None or f is None) else rel(c["eta_B"], f["eta_B"]),
            "eta_DW": None if f is None else f["eta_DW"],
            "eta_DW_coarse": None if c is None else c["eta_DW"],
            "eta_DW_smoothgate": None if f is None else f["eta_DW_smoothgate"],
            "E_rel_drift": None if f is None else f["E_rel_drift"],
            "P_abs_drift": None if f is None else f["P_abs_drift"],
            "H_rel_drift": None if f is None else f["H_rel_drift"],
            "H_rel_drift_coarse": None if c is None else c["H_rel_drift"],
            "spec_max_dB_above_0.8nyq_rel_max": None if f is None else f["spec_max_dB_above_0.8nyq_rel_max"],
            "time_edge_power_ratio": None if f is None else f["time_edge_power_ratio"]}
    fl = last("item3_conv", N=N, delta3=d3)
    e["grid"] = grid_meta(fl)
    e["value_xi2"] = obs(fl)
    if N == 10.0:
        gr = last("item3_grid", N=N, delta3=d3)
        e["grid_G3"] = grid_meta(gr)
        e["conv_grid_G3_vs_G2_xi2"] = conv(gr, fl, "G2_vs_G3")
        e["value_G3_xi2"] = obs(gr)
        e["by_xi_G3"] = {f"{xi:.1f}": (lambda r: None if r is None else
                                       {"eta_B": r["eta_B"], "eta_DW": r["eta_DW"]})(
                                           at_xi("item3_grid", xi, N=N, delta3=d3))
                         for xi in (0.5, 1.0, 1.5, 2.0)}
    for wstage, wtag in (("item3_win", "W512"), ("item3_win10", "W1024")):
        wins = pick(wstage, N=N, delta3=d3)
        if not wins:
            continue
        key = f"window_check_{wtag}_vs_G2_same_step"
        e[key] = {}
        for xi in (0.5, 1.0, 1.5, 2.0):
            rw = at_xi(wstage, xi, N=N, delta3=d3)
            rb = at_xi("item3", xi, N=N, delta3=d3)
            if rw is not None and rb is not None:
                e[key][f"{xi:.1f}"] = {
                    f"eta_B_{wtag}": rw["eta_B"], f"eta_DW_{wtag}": rw["eta_DW"],
                    f"eta_DW_smoothgate_{wtag}": rw["eta_DW_smoothgate"],
                    f"relchange_eta_B_G2_vs_{wtag}": rel(rb["eta_B"], rw["eta_B"]),
                    f"relchange_eta_DW_G2_vs_{wtag}": rel(rb["eta_DW"], rw["eta_DW"]),
                    f"time_edge_power_ratio_{wtag}": rw["time_edge_power_ratio"]}
    item3[f"N{N:g}_d{d3:.3f}"] = e
summary["item3_card_regime_gauss_xi2"] = item3

# item 4
item4 = {}
for d3 in (0.02, 0.03, 0.04):
    c = last("item4", delta3=d3)
    f = last("item4_conv", delta3=d3)
    e = {"value_source": "item4_conv (G1, nsteps 8000, dt 1.95 fs)", "value": obs(f),
         "grid": grid_meta(f), "conv_step_halving": conv(f, c, "n4000_vs_n8000")}
    if d3 == 0.02:
        gr = last("item4_grid", delta3=d3)
        e["grid_refined"] = grid_meta(gr)
        e["conv_grid_dt0.98fs_vs_1.95fs_n8000"] = conv(gr, f, "dt1.95_vs_dt0.98")
    item4[f"{d3:.3f}"] = e
for d3 in (0.02, 0.03, 0.04):
    e = item4[f"{d3:.3f}"]
    for nt, tag in ((8192, "dt0.98fs"), (16384, "dt0.49fs")):
        r = last("item4_grid2", delta3=d3, Nt=nt) or (last("item4_grid", delta3=d3) if (nt == 8192 and d3 == 0.02) else None)
        if r is not None:
            e[f"value_{tag}_n8000"] = {k: r[k] for k in ("eta_B", "eta_DW", "eta_DW_smoothgate",
                                                         "peak_band_max_dB_rel_input_max",
                                                         "peak_band_max_dB_rel_output_max",
                                                         "peak_band_max_w", "peak_band_max_dnuT0",
                                                         "t_peak_T0", "output_max_w", "P_mean_w",
                                                         "E_rel_drift")}
            e[f"relchange_eta_B_{tag}_vs_dt1.95fs"] = rel(r["eta_B"], e["value"]["eta_B"]) if e["value"] else None
tau1, tau2, fR = 12.2, 32.0, 0.18
TR = fR * 2 * tau1**2 * tau2 / (tau1**2 + tau2**2)
summary["item4_raman_M1_sech_N2_xi4_T0_50fs"] = item4
summary["item4_raman_model"] = {
    "solver_class": "AgarwalRaman(fraction=0.18, tau1=0.0122 ps, tau2=0.0320 ps)",
    "h_R": "(tau1^2+tau2^2)/(tau1 tau2^2) exp(-t/tau2) sin(t/tau1), t >= 0 (single damped oscillator, Blow-Wood form); int h_R dt = 1",
    "nonlinearity": "(1-f_R)|A|^2 A + f_R A (h_R * |A|^2), circular FFT convolution, kernel sampled at the grid step",
    "T_R_fs_first_moment": TR, "tau_R_over_T0": TR / 50.0,
    "self_steepening": "suppressed with omega0 T0 = 1e6; the Raman time constants are physical (independent of omega0 in this solver)"}

# residual self-steepening check (item-1 point delta3 = 0.04, G1, nsteps 8000)
ss = {}
base = last("item1_conv", delta3=0.04)
if base is not None:
    ss["1e+06"] = {k: base[k] for k in ("eta_B", "eta_DW", "P_abs_drift", "H_rel_drift", "E_rel_drift")}
for r in recs.get("ss", []):
    if r["xi"] > 0:
        ss[f"{r['omega0T0']:.0e}"] = {k: r[k] for k in ("eta_B", "eta_DW", "P_abs_drift", "H_rel_drift", "E_rel_drift")}
summary["selfsteepening_residual_check_d0.040"] = ss


# ---- grid-robust variants from the saved spectra (base runs; step dependence < 1e-5) ----
import numpy as np


def npz_variants(fn, d3, smooth_w=1.0):
    z = np.load(fn)
    w, Sin, S, Sg = z["w"], z["S_in"], z["S_out"], z["S_out_gated"]
    dw = w[1] - w[0]
    E = Sin.sum()
    wz = 1.0 / (6.0 * d3)
    frac = np.clip((w + dw / 2 - wz) / dw, 0.0, 1.0)
    band = w >= wz
    nb = max(1, int(round(smooth_w / dw)))
    if nb % 2 == 0:
        nb += 1
    ker = np.ones(nb) / nb
    Ss = np.convolve(S, ker, mode="same")
    j = np.argmax(np.where(band, Ss, 0.0))
    idx = np.where(band)[0]
    jl, best = -1, -np.inf
    for i in idx[1:-1]:
        if Ss[i] >= Ss[i - 1] and Ss[i] >= Ss[i + 1] and Ss[i] > best:
            jl, best = i, Ss[i]
    return {"file": os.path.basename(fn), "dw": float(dw),
            "smoothed_local_peak_w": float(w[jl]) if jl >= 0 else None,
            "smoothed_local_peak_dB_rel_input_max": float(10 * np.log10(Ss[jl] / Sin.max())) if jl >= 0 else None,
            "smoothed_local_peak_dB_rel_output_max": float(10 * np.log10(Ss[jl] / S.max())) if jl >= 0 else None,
            "eta_B_fracedge": float((frac * S).sum() / E),
            "eta_DW_fracedge": float((frac * Sg).sum() / E),
            "eta_B_plain_check": float(S[band].sum() / E),
            "smoothed_peak_width_w": float(nb * dw),
            "smoothed_peak_w": float(w[j]),
            "smoothed_peak_dB_rel_input_max": float(10 * np.log10(Ss[j] / Sin.max())),
            "smoothed_peak_dB_rel_output_max": float(10 * np.log10(Ss[j] / S.max()))}


variants = {}
for fn in sorted(glob.glob(os.path.join(RAW, "*.npz"))):
    b = os.path.basename(fn)
    if "_d0" not in b:
        continue
    d3 = float(b.split("_d")[1].split("_")[0])
    try:
        variants[b[:-4]] = npz_variants(fn, d3)
    except Exception as e:  # pragma: no cover
        variants[b[:-4]] = {"error": str(e)}
summary["grid_robust_variants_from_saved_spectra"] = {
    "definition": ("eta_*_fracedge: band sum with the bin straddling w_z weighted by its fraction above "
                   "w_z (bins of width dw centred on w_k); smoothed_peak: band maximum of |A_k|^2 after a "
                   "boxcar of width ~1 in w (fringe-averaged NSR level; smoothed_local_peak = largest interior local "
                   "maximum of the smoothed band spectrum, i.e. the DW hump). Computed on the base-step runs."),
    "by_run": variants}


def clean(x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list):
        return [clean(v) for v in x]
    return x


with open(os.path.join(HERE, "summary.json"), "w") as f:
    json.dump(clean(summary), f, indent=1, sort_keys=False)
print("wrote summary.json; stages:", {k: len(v) for k, v in recs.items()})
