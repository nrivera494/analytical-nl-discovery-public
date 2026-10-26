"""Dispersionless slot model of the matched-LO covariance with complete ASE and gain growth of the Kerr rate
(derived in the audit report, Part 4). k = gamma P/g in each time slot, kbar = <k>_P, k2 = <k^2>_P; G = e^tau.
  C11 = 2nG - (2n-1)
  C12 = 2 kbar G [(G-1) + (2n-1)(G-1-ln G)]
  C22 = G + 4 k2 G (G-1)^2 + (2n-1)[(G-1) + 4 k2 G (G^2 - 2 G ln G - 1)]
claude-interactive.13."""
import json, numpy as np
from scipy.optimize import brentq

def C(tau, kbar, k2, n):
    G = np.exp(tau); L = tau
    c11 = 2 * n * G - (2 * n - 1)
    c12 = 2 * kbar * G * ((G - 1) + (2 * n - 1) * (G - 1 - L))
    c22 = G + 4 * k2 * G * (G - 1) ** 2 + (2 * n - 1) * ((G - 1) + 4 * k2 * G * (G**2 - 2 * G * L - 1))
    return c11, c12, c22

def lam_min(tau, kbar, k2, n):
    a, b, c = C(tau, kbar, k2, n)
    tr, det = a + c, a * c - b * b
    return 2 * det / (tr + np.sqrt(tr**2 - 4 * det))

def min_over_tau(R, v, n, taus=np.linspace(1e-4, 4, 40001)):
    kbar = n * R; k2 = kbar**2 * (1 + v)       # v = Var_P(P)/<P>_P^2
    l = lam_min(taus, kbar, k2, n)
    i = np.argmin(l)
    return l[i], taus[i]

out = {}
for name, v in (("gaussian", 1 / np.sqrt(3) / 0.5 - 1), ("parabola", (24 / 35) / 0.64 - 1)):
    for n in (1.0, 2.0):
        f = lambda R: min_over_tau(R, v, n)[0] - 1
        Rmin = brentq(f, 1e-3, 1.0, xtol=1e-10)
        rows = {str(R): dict(zip(("min_lam", "tau_at_min"), map(float, min_over_tau(R, v, n)))) for R in (0.3, 0.5, 0.7, 0.9, 1.0, 1.1)}
        out[f"{name}_nsp{int(n)}"] = dict(var_over_mean2=v, R_min_for_squeezing_at_some_length=Rmin, rows=rows)
        print(name, int(n), "v=%.4f  R_min=%.5f" % (v, Rmin), {k: (round(r["min_lam"], 4), round(r["tau_at_min"], 3)) for k, r in rows.items()})
json.dump(out, open("slot_model_summary.json", "w"), indent=1)
