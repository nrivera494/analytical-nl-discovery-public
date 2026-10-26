"""Zero crossing of K* between zeta = 2.5 and 3 (run 2026-10-08-claude-b-kw-map, cases_crossing.json; claude-b,
T-20261008-claude-b-01). Same estimators as analyze.py (K0 = 2 K(0.1) - K(0.2), W0 = (4 W(0.1) - W(0.2)) / 3) at the
LP01-optimal filter of the hard-band, fractional-edge and interval classes, for zeta = 2.5, 2.6, 2.7, 2.8, 2.9, 3.
Linear interpolation of K0 gives zeta_c. Writes crossing.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2, r2, scalar_optima

RID = "2026-10-08-claude-b-kw-map"
rows = []
for z in (2.5, 2.6, 2.7, 2.8, 2.9, 3.0):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(RID, f"{zt}_scalar")
    opt = scalar_optima(g, Cs, ns)
    runs = {k: load(RID, f"{zt}_{k}")[1:3] for k in ("K_p2_0.1", "K_p2_0.2", "W_delta_0.1", "W_delta_0.2")}
    row = dict(zeta=z)
    for cls in ("sym_hard", "sym_frac", "interval"):
        Fs, T, info = opt[cls]
        d = {k: tc.fano(T, *runs[k]) - Fs for k in runs}
        K0 = 2 * d["K_p2_0.1"] / q2(0.1, 1, 0.5) - d["K_p2_0.2"] / q2(0.2, 1, 0.5)
        W0 = (4 * d["W_delta_0.1"] / r2(0.5, 0.1) - d["W_delta_0.2"] / r2(0.5, 0.2)) / 3
        row[cls] = dict(F_s=Fs, K0=K0, W0=W0, filter={k: v for k, v in info.items() if not isinstance(v, np.ndarray)})
    rows.append(row)
    print(z, {c: (round(row[c]["F_s"], 4), round(row[c]["K0"], 3), round(row[c]["W0"], 3)) for c in ("sym_hard", "sym_frac", "interval")})
out = {"rows": rows}
for cls in ("sym_hard", "sym_frac", "interval"):
    zs = [r["zeta"] for r in rows]
    ks = [r[cls]["K0"] for r in rows]
    zc = None
    for (z0, k0), (z1, k1) in zip(zip(zs, ks), zip(zs[1:], ks[1:])):
        if k0 < 0 <= k1:
            zc = z0 + (0 - k0) * (z1 - z0) / (k1 - k0)
            break
    out[f"zeta_c_{cls}"] = zc
json.dump(out, open(os.path.join(HERE, "crossing.json"), "w"), indent=1, default=float)
print({k: v for k, v in out.items() if k.startswith("zeta_c")})
