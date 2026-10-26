"""Exact single-mode Kerr squeezing of a coherent state, H = (Lambda/2) a+ a+ a a, to find how the best quadrature variance scales with
the photon number n (curvature of the Kerr crescent). c_n(t) = e^{-n/2} alpha^m/sqrt(m!) e^{-i Lambda m(m-1) t/2}; Var_min over the
quadrature angle = 1 + 2(<a+a> - |<a>|^2) - 2|<a^2> - <a>^2| (vacuum = 1). Scan the nonlinear phase Phi = Lambda n t.
Also a displaced-thermal input (Gaussian noise nu around the mean field) via the linearized-plus-curvature estimate, for comparison."""
import numpy as np, json
from scipy.special import gammaln
out = []
for nbar in [1e2, 1e3, 1e4, 1e5, 1e6]:
    m = np.arange(int(max(0, nbar - 12*np.sqrt(nbar))), int(nbar + 12*np.sqrt(nbar)) + 1)
    la = 0.5*(m*np.log(nbar) - gammaln(m + 1) - nbar)
    amp = np.exp(la - la.max()); amp /= np.sqrt(np.sum(amp**2))
    best = (np.inf, None)
    for Phi in np.logspace(-1, np.log10(5*nbar**(1/3)) + 0.3, 400):
        lt = Phi/nbar
        c = amp*np.exp(-0.5j*lt*m*(m - 1))
        a1 = np.sum(np.conj(c[:-1])*c[1:]*np.sqrt(m[1:]))
        a2 = np.sum(np.conj(c[:-2])*c[2:]*np.sqrt(m[2:]*(m[2:] - 1)))
        nm = np.sum(np.abs(c)**2*m)
        v = 1 + 2*(nm - abs(a1)**2) - 2*abs(a2 - a1**2)
        if v < best[0]: best = (float(v.real), float(Phi))
    out.append(dict(nbar=nbar, best_var=best[0], best_dB=float(10*np.log10(best[0])), Phi_opt=best[1],
                    estimate_n13=float(0.945*nbar**(-1/3)), Phi_estimate=float((nbar/16)**(1/6))))
    print(f"n = {nbar:.0e}: best Var {best[0]:.3e} ({10*np.log10(best[0]):.1f} dB) at Phi = {best[1]:.2f}; estimate 0.945 n^(-1/3) = {0.945*nbar**(-1/3):.3e} at Phi = {(nbar/16)**(1/6):.2f}", flush=True)
ns = np.array([o['nbar'] for o in out]); vs = np.array([o['best_var'] for o in out])
slope = float(np.polyfit(np.log(ns), np.log(vs), 1)[0])
print('log-log slope of the best variance against n:', round(slope, 3))
json.dump(dict(results=out, slope=slope), open('kerr_curvature.json', 'w'), indent=1)
