#!/usr/bin/env python3
"""Sixth held-out (HELDOUT.md, commit 0475fdd): momentum-bound tightness for the flat-top p = exp(-t^4), dispersionless
Kerr, Phi = 5, 15, padding 8, bin threshold 1e-9: lambda_gen <= lambda_P and lambda_gen/lambda_P in [0.80, 1.00].
Usage: python heldout_flattop_lamgen.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral
out = sys.argv[1] if len(sys.argv) > 1 else "heldout_flattop_lamgen.json"
lP = {5.0: 0.064008, 15.0: 0.007541}
rows = []
for Phi in (5.0, 15.0):
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = np.exp(-t**4)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-9)
    lg = float(np.linalg.eigvalsh(Va)[0]); y = w * np.sqrt(nb); lmom = float(y @ Va @ y / (y @ y))
    r = {"pulse": "flattop exp(-t^4)", "Phi": Phi, "lam_gen": lg, "lam_P_frozen": lP[Phi], "ratio": lg / lP[Phi],
         "in_window": bool(0.8 <= lg / lP[Phi] <= 1.0), "lam_mom_grid": lmom, "mom_over_P": lmom / lP[Phi],
         "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
