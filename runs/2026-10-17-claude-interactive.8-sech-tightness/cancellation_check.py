"""Near-cancellation of the short-pulse x^2 coefficient (r = 1/sqrt3) and the finite-window slope at r = 0.6
(the proposer's retained failure), claude-interactive.8. Uses the closed form, verified to 1e-25 in check_exact.py."""
import json, numpy as np, mpmath as mp
from ramanlib import rho_closed
mp.mp.dps = 40
def slope(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(np.abs(np.asarray(ys, float))), 1)[0])
out = []
for r in [0.6, float(1 / mp.sqrt(3)), 0.45]:
    for lo, hi in [(1e-4, 1e-2), (2e-3, 1.6e-2), (2.5e-4, 2e-3), (1e-5, 1e-4)]:
        xs = np.geomspace(lo, hi, 8)
        g = [float((1 - rho_closed(r, x)) / (2 * mp.mpf(r) * x) - 1) for x in xs]
        out.append({"r": r, "x_window": [lo, hi], "gap_ratio_slope": slope(xs, g)})
        print(out[-1])
json.dump(out, open("summary_cancellation.json", "w"), indent=1)
