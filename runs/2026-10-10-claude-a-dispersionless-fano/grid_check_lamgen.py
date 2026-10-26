#!/usr/bin/env python3
"""Grid convergence of lambda_gen and of the grid momentum-weight value at large Phi (Kerr, Gaussian, dispersionless):
dt in {0.04, 0.02, 0.0133, 0.01} T0 at Phi = 10, 20; pad 8 (and pad 4 at the finest); threshold 1e-6 (and 1e-9).
Usage: python grid_check_lamgen.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "grid_check_lamgen.json"
rows = []
for Phi in (10.0, 20.0):
    for dt, pad, thr in ((0.04, 8, 1e-6), (0.02, 8, 1e-6), (0.02, 8, 1e-9), (0.0133333, 4, 1e-6), (0.01, 4, 1e-6)):
        t0 = time.time()
        t = np.arange(-7, 7, dt); p = gaussian_p(t)
        m = build_model(p, dt, Phi); V = covariance(m)
        nb, Va, idx, w = spectral(m, V, pad=pad, thr=thr)
        y = w * np.sqrt(nb); lmom = float(y @ Va @ y / (y @ y))
        lg = float(np.linalg.eigvalsh(Va)[0])
        lP = 1 / (1 + 4 * Phi**2 / (3 * np.sqrt(3)))
        rows.append({"Phi": Phi, "dt": dt, "pad": pad, "thr": thr, "n_bins": int(len(nb)), "lam_gen": lg, "lam_mom_grid": lmom,
                     "lam_P": lP, "mom_over_P": lmom / lP, "gen_over_P": lg / lP, "gen_over_mom": lg / lmom,
                     "wall_s": round(time.time() - t0, 1)})
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
