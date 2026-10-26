"""Parity check for claim C-20261008-claude-b-01, item 1 (run 2026-10-08-claude-b-exponents, claude-b, T-20261008-claude-b-01).
F(delta; T(omega)) = F(-delta; T(-omega)). Computes the Manakov-overlap, p2 = 0.5, zeta = 2 case at delta = -0.2 (the +0.2
case is stored in this run) and compares symmetric bands kmax = 3..7 and asymmetric intervals [k1, k2] with their mirror
images. Writes parity_check.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load

g, Cp, npl, _ = load("2026-10-08-claude-b-exponents", "z2_delta_0.2_p2_0.5_C22_1")
a0, b0, _ = tc.launch(g, 0.5, [[1, 1], [1, 1]])
nb, Cov = tc.bin_covariance(g, a0, b0, 2.0, 2e-3, [[1, 1], [1, 1]], -0.2)
Cm, nm = tc.totals(nb, Cov, g.N)
rows = []
for km in (3, 4, 5, 6, 7):
    T = (np.abs(g.k) <= km).astype(float)
    rows.append(dict(filter=f"|k|<={km}", F_plus=tc.fano(T, Cp, npl), F_minus=tc.fano(T, Cm, nm)))
for k1, k2 in ((-6, 3), (-4, 6), (-2, 8), (0, 7)):
    T = ((g.k >= k1) & (g.k <= k2)).astype(float)
    Tm = ((g.k >= -k2) & (g.k <= -k1)).astype(float)
    rows.append(dict(filter=f"[{k1},{k2}] at +delta vs mirror at -delta", F_plus=tc.fano(T, Cp, npl), F_minus=tc.fano(Tm, Cm, nm),
                     F_minus_same_filter=tc.fano(T, Cm, nm)))
for r in rows:
    r["rel_diff"] = abs(r["F_plus"] / r["F_minus"] - 1)
out = dict(rows=rows, max_rel_diff=max(r["rel_diff"] for r in rows))
json.dump(out, open(os.path.join(HERE, "parity_check.json"), "w"), indent=1, default=float)
for r in rows:
    print(r)
print("max rel diff", out["max_rel_diff"])
