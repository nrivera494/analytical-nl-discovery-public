"""Recompute the frozen tables P3 and P5 of C-20261008-claude-a-01 from the claim's own formulas (b):
a'' = 2 e^{Gamma zeta}/a^2, X = a + a'(zeta_L - zeta), h = X - a' a_L / a'_L, and the stated integrals.
Independent ODE solve and quadrature; output: recompute_tables.json next to this script."""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
import tables as tb


def table(Gamma, U):
    zL = U / Gamma
    sol = solve_ivp(lambda z, y: [y[1], 2 * np.exp(Gamma * z) / y[0] ** 2], [0, zL], [1.0, 0.0], rtol=1e-12, atol=1e-14,
                    dense_output=True)
    z = np.linspace(0, zL, 200001); a, ap = sol.sol(z)
    aL, apL = a[-1], ap[-1]
    X = a + ap * (zL - z); h = X - ap * aL / apL
    w = Gamma * np.exp(-Gamma * z)
    I = lambda f: float(np.trapezoid(w * f, z))
    sTL2 = aL ** 2 / 5; sWL2 = apL ** 2 / 5
    return dict(aL=float(aL), apL=float(apL), VarTc=[X[0] ** 2 / 5 / sTL2, I(X ** 2) / 5 / sTL2],
                VarTcomp=[h[0] ** 2 / 5, I(h ** 2) / 5], VarWc=[ap[0] ** 2 / 5 / sWL2, I(ap ** 2) / 5 / sWL2])


out = {}
for name, G, tab in (("P3_main", math.sqrt(18), tb.C01_P3), ("P5_heldout", 1.0, tb.C01_P5)):
    for U in (2, 4, 6):
        r = table(G, U)
        t = tab[U]
        r["max_abs_rel_diff_vs_frozen"] = max(abs(r[k][i] / t[k][i] - 1) for k in ("VarTc", "VarTcomp", "VarWc") for i in (0, 1) if t[k][i] != 0)
        r["aL_apL_rel_diff"] = max(abs(r["aL"] / t["aL"] - 1), abs(r["apL"] / t["apL"] - 1))
        out[f"{name}_gL{U}"] = r
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "recompute_tables.json"), "w"), indent=1)
print(json.dumps({k: (round(v["max_abs_rel_diff_vs_frozen"], 6), round(v["aL_apL_rel_diff"], 6)) for k, v in out.items()}))
