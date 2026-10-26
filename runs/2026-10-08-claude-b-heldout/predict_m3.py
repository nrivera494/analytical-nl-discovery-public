"""Frozen predictions for the three-mode held-out cases H6, H7 of claim C-20261008-claude-b-01 (claude-b).

Run BEFORE the cases are computed. Ideal parabolic-GRIN LP01, LP02, LP11a (exact Laguerre-Gauss overlaps, cross-phase
coefficients 2 Q_mn / Q_0101 off the diagonal and Q_mm / Q_0101 on it):
    C = [[1, 1, 1], [1, 1/2, 1/2], [1, 1/2, 3/4]],  delta = 0.
The dark subspace is two-dimensional, so these test that K does not depend on M and is isotropic in the dark subspace.
Prediction: Delta F(T) = K0(zeta; T) ||q||^2, ||q||^2 = || P_perp diag(sqrt p) (C - J) p ||^2, with K0 from run
2026-10-08-claude-b-kw-map (two modes only), for the hard bands kmax = 3..7 and the LP01 optima of classes A, A', B.
  H6: p = (0.6, 0.2, 0.2);  H7: p = (0.4, 0.3, 0.3);  zeta = 2 and 5.  Tolerance 25% (larger overlap defects than H1-H5).
Writes predictions_m3.json and cases_m3.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
import mmode_cov as mm
from analysis import load, q2, r2, scalar_optima

KW = "2026-10-08-claude-b-kw-map"
C3 = [[1.0, 1.0, 1.0], [1.0, 0.5, 0.5], [1.0, 0.5, 0.75]]
CASES = [dict(name="H6", p=[0.6, 0.2, 0.2]), dict(name="H7", p=[0.4, 0.3, 0.3])]
pred, cases = {}, []
for z in (2.0, 5.0):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(KW, f"{zt}_scalar")
    runs = {k: load(KW, f"{zt}_{k}")[1:3] for k in ("K_p2_0.1", "K_p2_0.2")}
    opt = scalar_optima(g, Cs, ns)
    filters = {f"kmax{k}": (np.abs(g.k) <= k).astype(float) for k in (3, 4, 5, 6, 7)}
    for cls in ("sym_hard", "sym_frac", "interval"):
        filters["opt_" + cls] = opt[cls][1]
    K0 = {}
    for name, T in filters.items():
        Fs = tc.fano(T, Cs, ns)
        K1 = (tc.fano(T, *runs["K_p2_0.1"]) - Fs) / q2(0.1, 1, 0.5)
        K2 = (tc.fano(T, *runs["K_p2_0.2"]) - Fs) / q2(0.2, 1, 0.5)
        K0[name] = (Fs, 2 * K1 - K2)
    for c in CASES:
        Q = mm.q2(c["p"], C3)
        pred[f"{c['name']}_{zt}"] = dict(case=dict(C=C3, **c), zeta=z, q2=Q,
                                         filters={n: dict(F_s=v[0], dF_pred=v[1] * Q) for n, v in K0.items()})
        cases.append(dict(tag=f"{c['name']}_{zt}", zeta=z, p=c["p"], C=C3, delta=[0, 0, 0]))
pred["tolerances_rel_err"] = {"H6": 0.25, "H7": 0.25}
pred["frozen_note"] = "Committed before the three-mode cases were computed."
json.dump(pred, open(os.path.join(HERE, "predictions_m3.json"), "w"), indent=1, default=float)
json.dump(cases, open(os.path.join(HERE, "cases_m3.json"), "w"), indent=1)
for k, v in pred.items():
    if isinstance(v, dict) and "filters" in v:
        print(k, "q2", f"{v['q2']:.4e}", {n: f"{r['dF_pred']:+.3e}" for n, r in v["filters"].items()})
