"""Largest GRIN advantage at the optimal filter inside the physical domain of the two-mode cross-phase model in ideal
GIF625 at 1550 nm (claude-b, T-20261008-claude-b-01; second-order formula, coefficients from this run's summary.json).

min F_GRIN - min F_s ~ K*(zeta) eps^2 p1 p2^3 + W*(zeta) delta^2 p1 p2 (hard-band class), with delta at its smallest value
inside the model's domain, |dbeta| L_D >= 10 (run 2026-10-08-claude-b-gif625-fwm-mismatch): delta_LP02 >= 0.562 (eps = 1/2),
delta_LP11 >= 0.543 (eps = 1/4). Scans p2 in (0, 1) and the map's zeta values; reports the most negative value, absolute
and relative to F_s*. Second-order formula only: third-order terms are of relative size ~|Delta| (see the claim).
Writes domain_bound.json.
"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
s = json.load(open(os.path.join(HERE, "summary.json")))
p2 = np.linspace(0.001, 0.999, 999)
p1 = 1 - p2
out = {}
for mode, eps, dmin in (("LP02", 0.5, 0.5622), ("LP11", 0.25, 0.5429)):
    best = None
    for r in s["rows"]:
        c = r["classes"]["sym_hard"]
        if r["zeta"] > 5:          # outside the asserted coefficient domain
            continue
        val = c["K0"] * eps ** 2 * p1 * p2 ** 3 + c["W0"] * dmin ** 2 * p1 * p2
        i = int(np.argmin(val))
        rel = val[i] / c["F_s_opt"]
        if best is None or rel < best["rel"]:
            best = dict(zeta=r["zeta"], p2=float(p2[i]), dF=float(val[i]), rel=float(rel), F_s_opt=c["F_s_opt"], delta=dmin, eps=eps)
    out[mode] = best
json.dump(out, open(os.path.join(HERE, "domain_bound.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
