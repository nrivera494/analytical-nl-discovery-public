#!/usr/bin/env python3
"""Deficit 1 - lambda_gen/lambda_P at large Phi on converged bins (threshold 1e-9, padding 4, dt = 0.4/Phi), Kerr Gaussian,
Phi = 20..80. Usage: python lamgen_deficit.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "lamgen_deficit.json"
rows = []
for Phi in (20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0):
    t0 = time.time()
    dt = min(0.04, 0.4 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=4, thr=1e-9)
    lg = float(np.linalg.eigvalsh(Va)[0]); lP = 1 / (1 + 4 * Phi**2 / (3 * np.sqrt(3)))
    y = w * np.sqrt(nb); mom = float(y @ Va @ y / (y @ y))
    rows.append({"Phi": Phi, "lam_gen": lg, "lam_P": lP, "ratio": lg / lP, "deficit": 1 - lg / lP, "mom_over_P": mom / lP,
                 "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)})
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
P = np.array([r["Phi"] for r in rows]); d = np.array([r["deficit"] for r in rows])
print("deficit slope (all):", float(np.polyfit(np.log(P), np.log(d), 1)[0]))
