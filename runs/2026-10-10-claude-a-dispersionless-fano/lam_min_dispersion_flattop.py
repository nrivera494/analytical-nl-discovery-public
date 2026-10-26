#!/usr/bin/env python3
"""Held-out test (frozen in HELDOUT.md, commit 326c335) of the mechanism behind the lambda_min dispersion law:
flat-top pulse p = exp(-t^4) (p''(0) = 0) -> quartic-oscillator prediction
    lambda_min/V_min(Phi) - 1 = 0.64226 Phi/sqrt(1+Phi^2) y^(2/3),  y = Phi beta2 L / T0^2.
Same restricted-input method as lam_min_dispersion.py. Usage: python lam_min_dispersion_flattop.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import vmin_kerr
from lin_ssfm import propagate_cols
out = sys.argv[1] if len(sys.argv) > 1 else "lam_min_dispersion_flattop.json"
rows = []
for Phi in (10.0, 3.0):
    for dt in (0.01, 0.005):
        for y in (1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 1e-2):
            if dt == 0.005 and y not in (1e-6, 1e-4):
                continue
            t = np.arange(-6.0, 6.0 + dt / 2, dt); t = t - t[np.argmin(np.abs(t))]
            p = np.exp(-t**4)
            cols = np.where(np.abs(t) <= 1.2)[0]
            t0 = time.time()
            A, S = propagate_cols(p, dt, Phi, y / Phi, 200, cols)
            lam = float(np.linalg.svd(S, compute_uv=False)[-1] ** 2)
            v0 = float(vmin_kerr(Phi))
            pred = 0.6422685968257819 * Phi / np.sqrt(1 + Phi**2) * y ** (2 / 3)
            r = {"pulse": "flattop exp(-t^4)", "Phi": Phi, "dt": dt, "y_PhiL_over_LD": y, "lam_min": lam, "Vmin_Phi": v0,
                 "excess": lam / v0 - 1, "pred_excess": float(pred), "ratio": (lam / v0 - 1) / pred,
                 "in_frozen_window": bool(0.95 <= (lam / v0 - 1) / pred <= 1.08) if y <= 1e-3 else None,
                 "wall_s": round(time.time() - t0, 1)}
            rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
            json.dump({"rows": rows}, open(out, "w"), indent=1)
