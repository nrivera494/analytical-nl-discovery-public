"""Best quadrature squeezing of the condensate after a subsequent single-mode Kerr stage, including the curvature of the Kerr crescent.
For each checkpoint of cond_kerr.json (condensate covariance V in its own amplitude/phase frame, vacuum = 1), minimize over the stage's
nonlinear phase Phi:  lambda(Phi) = lambda_min[K(Phi) V K(Phi)^T] + V'(Phi)^2/(8 n0),  V'(Phi) = V_P + 4 Phi C + 4 Phi^2 V_X,
where the second term is the variance of the crescent's sagitta for a Gaussian phase spread V' on a circle of radius 2 sqrt(n0)
(checked against exact single-mode Kerr in kerr_curvature.py: best 0.945 n^(-1/3), slope -0.337). Closed form when the existing
phase spread is below the optimum: lambda_best ~ 0.945 (nu^4/n0)^(1/3). n0 = condensate photons per cell. Output: best_squeezing.txt."""
import json, numpy as np
from scipy.optimize import minimize_scalar
d = json.load(open('cond_kerr.json'))
lines = []
def lam(V, Phi, n0):
    K = np.array([[1.0, 0.0], [2*Phi, 1.0]]); W = K @ V @ K.T
    return np.linalg.eigvalsh(W)[0] + W[1, 1]**2/(8*n0)
for case in d['cases']:
    for n0 in [1e8, 1e10, 1e12]:
        row = []
        for r in case['records']:
            V = np.array([[r['V_X'], r['C']], [r['C'], r['V_P']]])
            grid = np.concatenate([[0.0], np.logspace(-2, 4, 600)])
            vals = [lam(V, p, n0) for p in grid]; i = int(np.argmin(vals))
            lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
            res = minimize_scalar(lambda p: lam(V, p, n0), bounds=(lo, hi), method='bounded') if hi > lo else None
            best = min(vals[i], res.fun if res is not None else np.inf); Phi = res.x if (res is not None and res.fun < vals[i]) else grid[i]
            closed = 0.945*(r['nu']**4/n0)**(1/3)
            row.append((r['z'], 10*np.log10(best), Phi, 10*np.log10(closed)))
        lines.append(f"E'={case['Eprime']} sigma={case['sigma']} n0={n0:.0e}: " + "; ".join(f"z={z:.0f}: {db:.1f} dB at Phi={p:.3g} (closed form {cdb:.1f})" for z, db, p, cdb in row))
coh = [f"n0={n0:.0e}: coherent state {10*np.log10(0.945*n0**(-1/3)):.1f} dB" for n0 in [1e8, 1e10, 1e12]]
lines.append('reference, pure coherent state of the same photon number: ' + '; '.join(coh))
open('best_squeezing.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
