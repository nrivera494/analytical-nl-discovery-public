#!/usr/bin/env python3
"""H1c counterexample check: Lorentzian A/(1+t^2), window convergence (width 60, 120, 240) at fixed dt.
Usage: python h1c_lorentz_window.py out.json"""
import json, sys, time
import numpy as np
from zs import Grid, leading_fast, eta_wkb
rows = []
for A in (1.0, 2.0, 3.0):
    for width, n in ((60.0, 768), (120.0, 1536), (240.0, 3072)):
        t0 = time.time()
        g = Grid(n, width); q = (A / (1 + g.t**2)).astype(complex)
        z, v, w = leading_fast(g, q, sigma=1j * (A + 0.3))
        # WKB on an untruncated fine grid (tails below eta do not contribute)
        tt = np.linspace(-50, 50, 400001); ew = eta_wkb(A / (1 + tt**2), tt[1] - tt[0])
        rows.append({"A": A, "width": width, "n": n, "eta_max": float(z.imag), "eta_wkb_exact_profile": ew, "eta_minus_wkb": float(z.imag) - ew, "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
json.dump({"rows": rows}, open(sys.argv[1] if len(sys.argv) > 1 else "h1c_lorentz_window.json", "w"), indent=1)
