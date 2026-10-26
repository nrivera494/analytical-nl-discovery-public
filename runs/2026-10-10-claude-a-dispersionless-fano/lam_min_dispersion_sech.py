#!/usr/bin/env python3
"""Held-out check (frozen in HELDOUT.md, commit 3a46f26) of the lambda_min dispersion law for a sech pulse,
p = sech^2(t/T_s), Phi = 10, beta2 > 0, y = Phi beta2 L / T_s^2. Same restricted-input method as lam_min_dispersion.py.
Usage: python lam_min_dispersion_sech.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import vmin_kerr
from lin_ssfm import propagate_cols

out = sys.argv[1] if len(sys.argv) > 1 else "lam_min_dispersion_sech.json"
rows = []
Phi = 10.0
for dt in (0.01, 0.005):
    for y in (1e-5, 3e-5, 1e-4, 3e-4, 1e-3):
        tmax = 12.0
        t = np.arange(-tmax, tmax + dt / 2, dt); t = t - t[np.argmin(np.abs(t))]
        p = 1 / np.cosh(t) ** 2                        # T_s = 1
        cols = np.where(np.abs(t) <= 1.0)[0]
        t0 = time.time()
        A, S = propagate_cols(p, dt, Phi, y / Phi, 200, cols)
        lam = float(np.linalg.svd(S, compute_uv=False)[-1] ** 2)
        v0 = float(vmin_kerr(Phi))
        pred = Phi**1.5 / np.sqrt(1 + Phi**2) * np.sqrt(2.0 * (y / Phi) / 3)   # |p''(0)| = 2/T_s^2, beta2 L = y/Phi
        r = {"pulse": "sech", "Phi": Phi, "y_PhiL_over_LD": y, "dt": dt, "lam_min": lam, "Vmin_Phi": v0,
             "excess": lam / v0 - 1, "pred_excess_leading": float(pred), "ratio": (lam / v0 - 1) / pred,
             "in_frozen_window": bool(0.97 <= (lam / v0 - 1) / pred <= 1.06), "wall_s": round(time.time() - t0, 1)}
        rows.append(r); print(json.dumps(r), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
