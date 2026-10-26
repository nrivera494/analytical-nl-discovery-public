#!/usr/bin/env python3
"""Test of the open prediction in C-20261010-claude-a-01 (registered at commit cb7ad63): item 3(b) at T0 = 5 ps,
Phi = 10, 300 K: band-limited lambda_min within 5% of the single-slice value. Blow-Wood, fR = 0.18, Gaussian.
Two grids (dt = 0.04 T0 and 0.02 T0). Usage: python open_prediction_5ps.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, lam_min, lam_min_band, lag_kernels, gaussian_p, spectral, lam_gen
out = sys.argv[1] if len(sys.argv) > 1 else "open_prediction_5ps.json"
T0, Phi, fR, TK = 5000.0, 10.0, 0.18, 300.0
M = np.array([[1, 2 * Phi], [2 * Phi, 1 + 4 * Phi**2 + 2 * Phi * fR * 1.276]]); ls = float(np.linalg.eigvalsh(M)[0])
rows = []
for frac in (0.04, 0.02):
    t0 = time.time()
    dt = frac * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
    m = build_model(p, dt, Phi, fR=fR, temp_K=TK, kern=lag_kernels(len(t), dt, fR, TK))
    V = covariance(m)
    lb = lam_min_band(m, V)[0]
    nb, Va, idx, w = spectral(m, V, pad=4, thr=1e-6)
    r = {"T0_fs": T0, "dt_fs": dt, "Phi": Phi, "T_K": TK, "lam_min_band": lb, "slice": ls, "ratio": lb / ls,
         "within_5pct": bool(abs(lb / ls - 1) <= 0.05), "lam_min_full": lam_min(V), "lam_gen": lam_gen(Va), "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
