#!/usr/bin/env python3
"""H1c' (frozen in HYPOTHESES.md, sixth freeze): eta_max <= eta_WKB[|q|] + 1e-3 for single-humped q with at least
exponential tails, on shapes not used before; plus two algebraic-tail shapes. Leading eigenvalue by shift-invert on two
grids (leading_fast); WKB integral on a fine (n = 2^18) sampling of the exact profile. Usage: python h1c_narrow.py out.json"""
import json, sys, time
import numpy as np
from zs import Grid, leading_fast, eta_wkb

out = sys.argv[1] if len(sys.argv) > 1 else "h1c_narrow.json"
shapes = {
    "sech_half": (lambda t: 1 / np.sqrt(np.cosh(t)), 80.0),
    "sech_cubed": (lambda t: 1 / np.cosh(t) ** 3, 24.0),
    "exp_abs_1.5": (lambda t: np.exp(-np.abs(t) ** 1.5), 24.0),
    "asym_sech": (lambda t: np.exp(0.4 * np.tanh(t)) / np.cosh(t), 30.0),
    "alg_inv_1pt2_sq": (lambda t: 1 / (1 + t**2) ** 2, 60.0),
    "alg_inv_1pt4": (lambda t: 1 / (1 + t**4), 60.0),
}
rows = []
for name, (f, width) in shapes.items():
    tt = np.linspace(-width / 2, width / 2, 2**18, endpoint=False)
    prof = f(tt); peak = prof.max()
    for A in (1.0, 2.0, 3.0, 4.0):
        t0 = time.time()
        zs_ = []
        for n in (768, 1152):
            g = Grid(n, width)
            q = (A * f(g.t) / peak).astype(complex)
            z, _, _ = leading_fast(g, q, sigma=1j * (A + 0.3))
            zs_.append(z)
        ew = eta_wkb(A * prof / peak, tt[1] - tt[0])
        eta = float(zs_[1].imag)
        rows.append({"shape": name, "A": A, "eta_max": eta, "two_grid_err": float(abs(zs_[1] - zs_[0])), "eta_wkb": ew,
                     "wkb_minus_eta": ew - eta, "exp_tail": not name.startswith("alg"), "violates": bool(ew - eta < -1e-3),
                     "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
