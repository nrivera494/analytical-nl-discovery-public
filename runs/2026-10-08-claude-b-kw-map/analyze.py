"""K(zeta; T) and W(zeta; T) at the LP01-optimal filters (run 2026-10-08-claude-b-kw-map, claude-b, T-20261008-claude-b-01).

For each zeta:
- LP01 (scalar) optimum in four filter classes applied to all modes: A hard symmetric band |k| <= kmax; A' symmetric band
  with a fractional edge bin (continuous edge); B any hard interval [k1, k2]; C any transmission T(omega) in [0, 1]
  (projected gradient, best of several starts; a local optimum).
- K at that filter from the GRIN runs (C22 = 1/2, p2 = 0.1, 0.2, delta = 0): K(p2) = Delta F / ||q||^2, with the
  linear extrapolation K0 = 2 K(0.1) - K(0.2) to p2 -> 0.
- W at that filter from the walk-off runs (Manakov overlaps, p2 = 0.5, delta = 0.1, 0.2): W(delta) = Delta F / ||r||^2,
  extrapolated as W0 = (4 W(0.1) - W(0.2)) / 3 (even in delta).
- Direct finite-parameter check of the optimum inequality: min over the class of F_GRIN minus min over the class of F_s
  (each optimized separately) for the p2 = 0.2 GRIN run and the delta = 0.2 walk-off run, compared with the second-order
  prediction ||q||^2 K(T*) (envelope argument) and ||r||^2 W(T*).
- K over the hard symmetric bands kmax = 2..10 (where Delta F < 0 at a fixed filter).
Writes summary.json and kw_vs_zeta.png.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2, r2, scalar_optima

RID = "2026-10-08-claude-b-kw-map"
ZETAS = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0)
out = {"zetas": ZETAS, "rows": []}


def class_min(cls, g, Ct, nt, T_start):
    if cls == "sym_hard":
        A = tc.class_sym_hard(g, Ct, nt, range(0, 20))
        return min(A.values())
    if cls == "sym_frac":
        return tc.class_sym_frac(g, Ct, nt, range(0, 20))[0]["F"]
    if cls == "interval":
        return tc.class_interval(g, Ct, nt)["F"]
    starts = [T_start, (np.abs(g.k) <= 5).astype(float), 0.5 * np.ones(g.N), np.ones(g.N)]
    return tc.class_any(g, Ct, nt, starts)[0]["F"]


for z in ZETAS:
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(RID, f"{zt}_scalar")
    opt = scalar_optima(g, Cs, ns)
    runs = {key: load(RID, f"{zt}_{key}")[1:3] for key in ("K_p2_0.1", "K_p2_0.2", "W_delta_0.1", "W_delta_0.2")}
    row = {"zeta": z, "classes": {}}
    for cls, (Fs, T, info) in opt.items():
        def dF(key):
            Ct, nt = runs[key]
            return tc.fano(T, Ct, nt) - Fs
        K1, K2 = dF("K_p2_0.1") / q2(0.1, 1, 0.5), dF("K_p2_0.2") / q2(0.2, 1, 0.5)
        W1, W2 = dF("W_delta_0.1") / r2(0.5, 0.1), dF("W_delta_0.2") / r2(0.5, 0.2)
        # direct optimum comparison at finite parameters (each launch optimized within the class)
        Ct, nt = runs["K_p2_0.2"]
        dmin_K = class_min(cls, g, Ct, nt, T) - Fs
        Ct, nt = runs["W_delta_0.2"]
        dmin_W = class_min(cls, g, Ct, nt, T) - Fs
        info_clean = {k: v for k, v in info.items() if not isinstance(v, np.ndarray)}
        row["classes"][cls] = dict(F_s_opt=Fs, filter=info_clean, T_opt_nonzero_bins=int(np.sum(T > 1e-6)),
                                   K_p2_0p1=K1, K_p2_0p2=K2, K0=2 * K1 - K2, W_delta_0p1=W1, W_delta_0p2=W2,
                                   W0=(4 * W1 - W2) / 3,
                                   min_F_grin_minus_min_F_s_p2_0p2=dmin_K, envelope_prediction_p2_0p2=q2(0.2, 1, 0.5) * K2,
                                   min_F_walk_minus_min_F_s_delta_0p2=dmin_W, envelope_prediction_delta_0p2=r2(0.5, 0.2) * W2)
        if cls == "any":
            row["classes"][cls]["T_opt"] = [float(x) for x in T[g.order]]
    kband = {}
    for km in range(2, 11):
        T = (np.abs(g.k) <= km).astype(float)
        Fs_k = tc.fano(T, Cs, ns)
        Ct, nt = runs["K_p2_0.1"]
        K1 = (tc.fano(T, Ct, nt) - Fs_k) / q2(0.1, 1, 0.5)
        Ct, nt = runs["K_p2_0.2"]
        K2 = (tc.fano(T, Ct, nt) - Fs_k) / q2(0.2, 1, 0.5)
        Ct, nt = runs["W_delta_0.1"]
        W1 = (tc.fano(T, Ct, nt) - Fs_k) / r2(0.5, 0.1)
        kband[km] = dict(edge=(km + 0.5) * g.dw, F_s=Fs_k, K0=2 * K1 - K2, W_delta_0p1=W1)
    row["sym_hard_bands"] = kband
    out["rows"].append(row)
    c = row["classes"]
    print(f"zeta={z}: " + " | ".join(f"{k}: Fs*={v['F_s_opt']:.4f} K0={v['K0']:+.3f} W0={v['W0']:+.3f} "
                                       f"dmin(p2=.2)={v['min_F_grin_minus_min_F_s_p2_0p2']:+.2e} (env {v['envelope_prediction_p2_0p2']:+.2e})"
                                       for k, v in c.items()), flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
for cls, mk in (("sym_hard", "o"), ("sym_frac", "s"), ("interval", "^"), ("any", "x")):
    ax[0].plot(ZETAS, [r["classes"][cls]["K0"] for r in out["rows"]], mk + "-", label=cls)
    ax[1].plot(ZETAS, [r["classes"][cls]["W0"] for r in out["rows"]], mk + "-", label=cls)
for a, lab in ((ax[0], "K at the LP01-optimal filter"), (ax[1], "W at the LP01-optimal filter")):
    a.axhline(0, color="k", lw=0.8)
    a.set_xlabel(r"$\zeta$")
    a.set_title(lab, fontsize=10)
ax[0].legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "kw_vs_zeta.png"), dpi=130)
