"""Extra checks (claude-interactive.8): (1) the sech-ansatz time kernel of arXiv:2603.21734 Eq. (2), as transcribed by
subagent claude-interactive.8.1, B(u) = (15/8) csch^4 u [4u + 2u cosh 2u - 3 sinh 2u] (per tau0), equals (15/4)(-q'(u)),
q = (u coth u - 1)/sinh^2 u the claim's autocorrelation density; (2) the closed form at extreme r = 0.01, 20."""
import json, mpmath as mp
from ramanlib import rho_closed, rho_spectral, q_diff
mp.mp.dps = 40
out = {"kernel": [], "extreme_r": []}
for u in [mp.mpf("0.05"), mp.mpf("0.5"), mp.mpf(1), mp.mpf(3), mp.mpf(8)]:
    B = mp.mpf(15) / 8 / mp.sinh(u) ** 4 * (4 * u + 2 * u * mp.cosh(2 * u) - 3 * mp.sinh(2 * u))
    mqp = -mp.diff(q_diff, u)
    out["kernel"].append({"u": float(u), "B": float(B), "15/4*(-q')": float(15 * mqp / 4), "rel": float(abs(B - 15 * mqp / 4) / abs(B))})
for r in [0.01, 20.0]:
    for x in [0.01, 1.0, 100.0]:
        rc, rs = rho_closed(r, x), rho_spectral(r, x)
        out["extreme_r"].append({"r": r, "x": x, "rho_closed": float(rc), "rho_spectral": float(rs), "rel": float(abs(rc - rs) / rc)})
out["kernel_max_rel"] = max(k["rel"] for k in out["kernel"])
out["extreme_r_max_rel"] = max(k["rel"] for k in out["extreme_r"])
json.dump(out, open("summary_extra.json", "w"), indent=1)
print(json.dumps(out, indent=1))
