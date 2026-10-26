"""G1 of predictions.md: a single-mode Kerr stage acting on a mixed Gaussian condensate state, by the exact classical Kerr map of Wigner samples
(truncated Wigner; exact up to O(1/n0) for this Hamiltonian). Input covariances (vacuum = 1) from cond_kerr.json (reference realization) and from
three Q-dis members of ensemble_squeezing.jsonl (C = +sqrt(V_X (V_P - V_P|X)), the sign of the fibre's own Kerr shear, checked on the reference).
For each input and n0 in {1e8, 1e10}: best over the Kerr phase Phi of the smallest quadrature variance, against (i) the best_squeezing.py optimum
(exact 2x2 shear + V'^2/(8 n0)) and (ii) the closed form 0.945 (nu^4/n0)^(1/3). Output single_mode_mixed_kerr.json and printed lines."""
import json, numpy as np
from scipy.optimize import minimize_scalar
NS = 200000; rng = np.random.default_rng(17)
g = rng.standard_normal((2, NS))                       # fixed samples for every Phi (smooth objective)
ck = json.load(open('../2026-10-17-claude-interactive.7-condensate-kerr-squeezability/cond_kerr.json'))
ref = [c for c in ck['cases'] if c['Eprime'] == 0.3 and c['sigma'] == 0.3][0]
inputs = [('coherent', 1.0, 0.0, 1.0)]
for r in ref['records']:
    if round(r['z']) in (10, 50, 100): inputs.append((f"ref_z{round(r['z'])}", r['V_X'], r['C'], r['V_P']))
sign_ok = all(r['C'] > 0 for r in ref['records'] if round(r['z']) in (10, 50, 100))
qs = [json.loads(l) for l in open('../2026-10-17-claude-interactive.7-ensemble-squeezing/ensemble_squeezing.jsonl')]
for r in qs:
    if r['ens'] == 'Q-dis' and abs(r['Ep'] - 0.3) < 1e-9 and r['dis_seed'] in (101, 104, 107):
        for x in r['records']:
            if round(x['z']) in (10, 50):
                inputs.append((f"dis{r['dis_seed']}_z{round(x['z'])}", x['V_X'], float(np.sqrt(max(x['V_X']*(x['V_P'] - x['V_P_given_X']), 0))), x['V_P']))
def formula_lam(V, Phi, n0):
    K = np.array([[1.0, 0.0], [2*Phi, 1.0]]); W = K @ V @ K.T
    return np.linalg.eigvalsh(W)[0] + W[1, 1]**2/(8*n0)
def best_formula(V, n0):
    grid = np.concatenate([[0.0], np.logspace(-2, 4, 800)]); vals = [formula_lam(V, p, n0) for p in grid]; i = int(np.argmin(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    res = minimize_scalar(lambda p: formula_lam(V, p, n0), bounds=(lo, hi), method='bounded') if hi > lo else None
    return min(vals[i], res.fun if res is not None else np.inf)
def twa_var(V, Phi, n0):
    L = np.linalg.cholesky(V); xp = L @ g                # vacuum-1 quadratures (x, p): delta a = (x + i p)/2
    a = np.sqrt(n0) + 0.5*(xp[0] + 1j*xp[1])
    a2 = a*np.exp(1j*(Phi/n0)*np.abs(a)**2)
    m = a2.mean(); d = (a2 - m)*np.exp(-1j*np.angle(m))
    W = np.cov(np.vstack([2*d.real, 2*d.imag]))
    return float(np.linalg.eigvalsh(W)[0])
out = []
for name, VX, C, VP in inputs:
    V = np.array([[VX, C], [C, VP]]); nu = float(np.sqrt(np.linalg.det(V)))
    for n0 in (1e8, 1e10):
        grid = np.concatenate([[0.0], np.logspace(-2, 3.3, 260)])
        tv = np.array([twa_var(V, p, n0) for p in grid]); i = int(np.argmin(tv))
        lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
        res = minimize_scalar(lambda p: twa_var(V, p, n0), bounds=(lo, hi), method='bounded', options=dict(xatol=1e-3*max(hi, 1e-3)))
        tbest, tphi = (res.fun, res.x) if res.fun < tv[i] else (tv[i], grid[i])
        fb = best_formula(V, n0); cf = 0.945*(nu**4/n0)**(1/3); Vstar = (4*n0*nu**2)**(1/3)
        rec = dict(input=name, V_X=VX, C=C, V_P=VP, nu=nu, n0=n0, twa_best_dB=float(10*np.log10(tbest)), twa_Phi_opt=float(tphi),
                   formula_best_dB=float(10*np.log10(fb)), closed_form_dB=float(10*np.log10(cf)), VP_below_Vstar=bool(VP < Vstar),
                   twa_minus_formula_dB=float(10*np.log10(tbest/fb)), twa_minus_closed_dB=float(10*np.log10(tbest/cf)))
        out.append(rec)
        print(f"{name:12s} nu={nu:8.3g} n0={n0:.0e}: TWA best {rec['twa_best_dB']:6.1f} dB at Phi {tphi:7.3g} | formula {rec['formula_best_dB']:6.1f} | closed {rec['closed_form_dB']:6.1f} "
              f"(V_P < V*: {rec['VP_below_Vstar']}) | TWA-formula {rec['twa_minus_formula_dB']:+.2f} dB, TWA-closed {rec['twa_minus_closed_dB']:+.2f} dB", flush=True)
json.dump(dict(sign_of_C_positive_on_reference=sign_ok, samples=NS, results=out), open('single_mode_mixed_kerr.json', 'w'), indent=1)
print('reference C > 0 at z = 10, 50, 100:', sign_ok)
