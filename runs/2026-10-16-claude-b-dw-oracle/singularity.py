"""Analyticity-strip width d(xi) of the unperturbed (delta3 = 0) NLSE solution, from the exponential decay of its
spectral tail: ln|uhat(w)| = a + b ln w - d w fitted where the tail lies between 10^lo and 10^hi of the peak.
Validated on the exact N = 2 breather: d(xi) = (1/2) arccos(sqrt(3)|sin 2xi| - 1)."""
import numpy as np, json, sys
from dw_lib import *

def strip_width(u, w, lo=-9.5, hi=-2.5, side=+1):
    """Fit ln|uhat| = a + b ln w - d w on side*w > 2 where 10^lo < |uhat|/max < 10^hi. The numerical floor (median
    level over the outer 20% of |w|) must lie at least 2 decades below 10^lo, and the fitted points must span at
    least 5 decades; otherwise nan."""
    A = np.abs(fft(u))
    A = A / A.max()
    LA = np.log10(A + 1e-300)
    outer = np.abs(w) > 0.8 * np.abs(w).max()
    floor = np.median(LA[outer])
    if floor > lo - 2:
        return np.nan, 0
    m = (side * w > 2) & (LA < hi) & (LA > lo)
    ww = np.abs(w[m]); y = np.log(A[m])
    if len(ww) < 20 or (y.max() - y.min()) < 5 * np.log(10):
        return np.nan, 0
    X = np.vstack([np.ones_like(ww), np.log(ww), -ww]).T
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    return c[2], len(ww)

def dcurve(u0, N, xis, Nt, TW, h=1e-3):
    p = Prop(Nt, TW, N, 0.0, max(xis), h, 4)
    _, _, snaps = p.run(u0, record=list(xis))
    res = []
    for x in xis:
        d, n = strip_width(snaps[x], p.w)
        res.append((x, d, n))
    return res

if __name__ == '__main__':
    out = {}
    # validation: sech N=2
    Nt, TW = 4096, 40.0
    tau, dt, w = grid(Nt, TW)
    xis = list(np.round(np.linspace(0.3, 1.2, 19), 6))
    r = dcurve(1/np.cosh(tau) + 0j, 2.0, xis, Nt, TW, h=5e-4)
    exact = lambda x: 0.5*np.arccos(np.sqrt(3)*abs(np.sin(2*x)) - 1)
    print('sech N=2: xi, d_fit, d_exact, npts')
    for x, d, n in r:
        print(f'{x:.3f} {d:.5f} {exact(x):.5f} {n}')
    out['sech2'] = [dict(xi=x, d_fit=d, d_exact=exact(x), npts=n) for x, d, n in r]
    json.dump(out, open('singularity_validation.json', 'w'), indent=1, default=float)
