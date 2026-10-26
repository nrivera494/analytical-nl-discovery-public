#!/usr/bin/env python3
"""H1a (eta <= ||q||_inf) and H1c (eta_max <= eta_WKB[|q|]) tests, frozen in HYPOTHESES.md (commit 3af8dfa).
Shapes at transform-limited peak A: Gaussian exp(-t^2/2), sech^2, Lorentzian 1/(1+t^2), super-Gaussian exp(-t^4/2);
linearly chirped Gaussians A exp(-(1+iC) t^2/2); random smooth spectral-phase masks on a Gaussian spectrum.
Leading eigenvalue by shift-invert above ||q||_inf, on two grids. Usage: python h1_tests.py out.json"""
import json, sys, time
import numpy as np
from numpy.polynomial import legendre
from zs import Grid, leading, eta_wkb

out = sys.argv[1] if len(sys.argv) > 1 else "h1_tests.json"
rng = np.random.default_rng(2026)

def lead_eta(q_of_t, width, n, A):
    res = []
    for nn in (n, int(1.5 * n) // 2 * 2):
        g = Grid(nn, width)
        q = q_of_t(g)
        try:
            z, v, w = leading(g, q, sigma=1j * (np.abs(q).max() + 0.3), k=3)
        except Exception:
            z = np.nan
        res.append((z, g, q))
    z1, g1, q1 = res[0]; z2 = res[1][0]
    return z1, abs(z1 - z2), g1, q1

shapes = {
    "gaussian": lambda t, A: A * np.exp(-t**2 / 2),
    "sech2": lambda t, A: A / np.cosh(t) ** 2,
    "lorentzian": lambda t, A: A / (1 + t**2),
    "supergauss2": lambda t, A: A * np.exp(-t**4 / 2),
}
rows = []
for name, f in shapes.items():
    for A in (1.0, 2.0, 3.0, 4.0, 6.0):
        t0 = time.time()
        width = 60.0 if name == "lorentzian" else 24.0
        n = 768 if A <= 3 else 1024
        z, err, g, q = lead_eta(lambda gg: f(gg.t, A).astype(complex), width, n, A)
        ew = eta_wkb(np.abs(q), g.dt)
        rows.append({"case": name, "A": A, "chirp": 0.0, "eta_max": float(z.imag), "two_grid_err": float(err),
                     "q_inf": float(np.abs(q).max()), "eta_over_qinf": float(z.imag / np.abs(q).max()),
                     "eta_wkb": ew, "wkb_minus_eta": ew - float(z.imag), "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
for A in (2.0, 3.0, 6.0):
    for C in (0.5, 1.0, 2.0, 4.0):
        t0 = time.time()
        n = 768 if A <= 3 else 1024
        z, err, g, q = lead_eta(lambda gg: A * np.exp(-(1 + 1j * C) * gg.t**2 / 2), 24.0, n, A)
        ew = eta_wkb(np.abs(q), g.dt)
        rows.append({"case": "chirped_gaussian", "A": A, "chirp": C, "eta_max": float(z.imag), "two_grid_err": float(err),
                     "q_inf": float(np.abs(q).max()), "eta_over_qinf": float(z.imag / np.abs(q).max()),
                     "eta_wkb": ew, "wkb_minus_eta": ew - float(z.imag), "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
# random smooth phase masks on a Gaussian spectrum (TL peak A)
for A in (3.0, 6.0):
    n = 768 if A <= 3 else 1024
    for trial in range(15):
        t0 = time.time()
        coef = rng.normal(0, 1, 7) * np.array([0, 0, 2.0, 1.5, 1.0, 0.7, 0.5])
        def qf(gg, A=A, coef=coef):
            w = gg.k
            Q = np.fft.fft(np.fft.ifftshift(A * np.exp(-gg.t**2 / 2)))
            x = np.clip(w / 4.0, -1, 1)
            phi = legendre.legval(x, coef)
            return np.fft.fftshift(np.fft.ifft(Q * np.exp(1j * phi)))
        z, err, g, q = lead_eta(qf, 40.0, int(n * 40 / 24) // 2 * 2, A)
        ew = eta_wkb(np.abs(q), g.dt)
        rows.append({"case": "random_phase_gaussian", "A": A, "trial": trial, "eta_max": float(z.imag) if np.isfinite(z) else None,
                     "two_grid_err": float(err) if np.isfinite(err) else None, "q_inf": float(np.abs(q).max()),
                     "eta_over_qinf": float(z.imag / np.abs(q).max()) if np.isfinite(z) else None,
                     "eta_over_TLpeak": float(z.imag / A) if np.isfinite(z) else None,
                     "eta_wkb": ew, "wkb_minus_eta": (ew - float(z.imag)) if np.isfinite(z) else None, "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
