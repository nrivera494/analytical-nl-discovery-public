#!/usr/bin/env python3
"""Test of the open prediction in C-20261010-claude-a-02 (registered before computing): dispersionless Kerr, Gaussian,
Phi = 50, bin threshold 1e-9, time step <= 0.4/Phi: lambda_gen/lambda_P in [0.9, 1]. Also dt = 0.3/Phi and thr 1e-12.
Usage: python open_prediction_phi50.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "open_prediction_phi50.json"
rows = []
Phi = 50.0
lP = 1 / (1 + 4 * Phi**2 / (3 * np.sqrt(3)))
for fdt, thr in ((0.4, 1e-9), (0.3, 1e-9), (0.4, 1e-12)):
    t0 = time.time()
    dt = fdt / Phi; t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=4, thr=thr)
    lg = float(np.linalg.eigvalsh(Va)[0])
    y = w * np.sqrt(nb); lmom = float(y @ Va @ y / (y @ y))
    r = {"Phi": Phi, "dt": dt, "pad": 4, "thr": thr, "n_bins": int(len(nb)), "lam_gen": lg, "lam_P": lP,
         "ratio": lg / lP, "in_window": bool(0.9 <= lg / lP <= 1.0), "mom_over_P": lmom / lP, "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
