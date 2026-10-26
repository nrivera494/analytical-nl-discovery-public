"""Frozen predictions for the held-out cases of claim C-20261008-claude-b-01 (claude-b, T-20261008-claude-b-01).

Run BEFORE the held-out cases are computed. Uses only run 2026-10-08-claude-b-kw-map (built from the C22 = 1/2 GRIN
matrix at delta = 0 and from Manakov overlaps with walk-off). Prediction: Delta F(T) = K(zeta; T) ||q||^2 + W(zeta; T) ||r||^2
with K = K0 and W = W0 (the p2 -> 0 and delta -> 0 extrapolations), for the hard symmetric bands kmax = 3..7 and for the
LP01-optimal filter of each class (A, A', B; class C excluded because its optimizer is a local search).
Held-out cases (none share an overlap structure with the K/W runs, except H4 which combines both):
  H1: C12 = 0.9, C22 = 1, p2 = 0.3, delta = 0     -> ||q||^2 = p1 p2 (0.1 (p1 - p2))^2
  H2: C12 = 2/3, C22 = 1, p2 = 0.2, delta = 0     (cross-phase-only polarization pair in a PM fiber)
  H3: C12 = 1, C22 = 3/4, p2 = 0.3, delta = 0     (ideal GRIN LP01 + LP11a)
  H4: C12 = 1, C22 = 1/2, p2 = 0.3, delta = 0.3   (GRIN LP02 with walk-off; tests additivity, no cross term)
  H5: C12 = 1, C22 = 3/4, p2 = 0.3, delta = 0.588 (GIF625 LP01 + LP11a at T0 = 0.227 ps, 1550 nm; large delta)
at zeta = 2 and 5. Writes predictions.json and cases.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2, r2, scalar_optima

KW = "2026-10-08-claude-b-kw-map"
CASES = [dict(name="H1", C12=0.9, C22=1.0, p2=0.3, delta=0.0),
         dict(name="H2", C12=2.0 / 3.0, C22=1.0, p2=0.2, delta=0.0),
         dict(name="H3", C12=1.0, C22=0.75, p2=0.3, delta=0.0),
         dict(name="H4", C12=1.0, C22=0.5, p2=0.3, delta=0.3),
         dict(name="H5", C12=1.0, C22=0.75, p2=0.3, delta=0.588)]
pred, cases = {}, []
for z in (2.0, 5.0):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(KW, f"{zt}_scalar")
    runs = {k: load(KW, f"{zt}_{k}")[1:3] for k in ("K_p2_0.1", "K_p2_0.2", "W_delta_0.1", "W_delta_0.2")}
    opt = scalar_optima(g, Cs, ns)
    filters = {f"kmax{k}": (np.abs(g.k) <= k).astype(float) for k in (3, 4, 5, 6, 7)}
    for cls in ("sym_hard", "sym_frac", "interval"):
        filters["opt_" + cls] = opt[cls][1]
    KWv = {}
    for name, T in filters.items():
        Fs = tc.fano(T, Cs, ns)
        d = {k: tc.fano(T, *runs[k]) - Fs for k in runs}
        K1, K2 = d["K_p2_0.1"] / q2(0.1, 1, 0.5), d["K_p2_0.2"] / q2(0.2, 1, 0.5)
        W1, W2 = d["W_delta_0.1"] / r2(0.5, 0.1), d["W_delta_0.2"] / r2(0.5, 0.2)
        KWv[name] = dict(F_s=Fs, K0=2 * K1 - K2, W0=(4 * W1 - W2) / 3, K_spread=abs(K1 - K2), W_spread=abs(W1 - W2))
    for c in CASES:
        Q, R = q2(c["p2"], c["C12"], c["C22"]), r2(c["p2"], c["delta"])
        rows = {}
        for name, v in KWv.items():
            dF = v["K0"] * Q + v["W0"] * R
            rows[name] = dict(F_s=v["F_s"], q2=Q, r2=R, dF_pred=dF, F_pred=v["F_s"] + dF)
        pred[f"{c['name']}_{zt}"] = dict(case=c, zeta=z, filters=rows)
        cases.append(dict(tag=f"{c['name']}_{zt}", zeta=z, p2=c["p2"], C22=c["C22"], C12=c["C12"], delta=c["delta"]))
pred["tolerances_rel_err"] = {"H1": 0.15, "H2": 0.25, "H3": 0.15, "H4": 0.20, "H5": 0.20}
pred["frozen_note"] = "Committed before the held-out cases were computed; a case passes when |actual - predicted| <= tolerance * |predicted| for every filter listed."
json.dump(pred, open(os.path.join(HERE, "predictions.json"), "w"), indent=1, default=float)
json.dump(cases, open(os.path.join(HERE, "cases.json"), "w"), indent=1)
for k, v in pred.items():
    if not isinstance(v, dict) or "filters" not in v:
        continue
    print(k, {n: f"{r['dF_pred']:+.3e}" for n, r in v["filters"].items()})
