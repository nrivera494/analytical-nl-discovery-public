"""Recompute C-20261008-claude-a-02 P1 (block matrices, main case Gamma = sqrt 18, unchirped sharp parabola) from the
claim's block ODE (a): dp/dzeta = e^{Gamma zeta}/a * m, dm/dzeta = -l(l+1)/a^2 p, a'' = 2 e^{Gamma zeta}/a^2, a(0)=1, a'(0)=0.
Output: recompute_p1.json next to this script."""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from summarize import C02_P1

G = math.sqrt(18)


def M(l, U):
    def f(z, y):
        a, ap, p1, m1, p2, m2 = y
        e = math.exp(G * z)
        return [ap, 2 * e / a ** 2, e / a * m1, -l * (l + 1) / a ** 2 * p1, e / a * m2, -l * (l + 1) / a ** 2 * p2]
    s = solve_ivp(f, [0, U / G], [1, 0, 1, 0, 0, 1], rtol=1e-12, atol=1e-14)
    y = s.y[:, -1]
    return np.array([[y[2], y[4]], [y[3], y[5]]])


out = {}
for U in (2, 4, 6):
    for l, key in ((0, "M0"), (2, "M2"), (3, "M3")):
        m = M(l, U); t = np.array(C02_P1[U][key])
        out[f"gL{U}_{key}"] = dict(recomputed=m.tolist(), frozen=t.tolist(), max_abs_diff=float(np.max(np.abs(m - t))))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "recompute_p1.json"), "w"), indent=1)
print({k: round(v["max_abs_diff"], 5) for k, v in out.items()})
