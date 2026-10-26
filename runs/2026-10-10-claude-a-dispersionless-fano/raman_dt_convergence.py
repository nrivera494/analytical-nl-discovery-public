#!/usr/bin/env python3
"""Time-step convergence of the Raman results (Blow-Wood, fR = 0.18, bin-averaged kernels), Gaussian, Phi = 10, 300 K:
T0 = 200 fs at dt = 8, 4, 2 fs and T0 = 1000 fs at dt = 40, 20, 10 fs. Reports lambda_min (full grid), band-limited
lambda_min, lambda_gen, and the grid momentum readout (no binary search). Usage: python raman_dt_convergence.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, lam_gen, lam_min, lam_min_band, lag_kernels, gaussian_p, symplectic_check
out = sys.argv[1] if len(sys.argv) > 1 else "raman_dt_convergence.json"
rows = []
Phi, fR, TK = 10.0, 0.18, 300.0
for T0, dts in ((200.0, (8.0, 4.0, 2.0)), (1000.0, (40.0, 20.0, 10.0))):
    for dt in dts:
        t0 = time.time()
        t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
        m = build_model(p, dt, Phi, fR=fR, temp_K=TK, kern=lag_kernels(len(t), dt, fR, TK))
        V = covariance(m)
        nb, Va, idx, w = spectral(m, V, pad=8 if len(t) <= 700 else 4, thr=1e-6)
        y = w * np.sqrt(nb)
        r = {"T0_fs": T0, "dt_fs": dt, "N_t": len(t), "lam_min": lam_min(V), "lam_min_band": lam_min_band(m, V)[0],
             "lam_gen": lam_gen(Va), "lam_momentum": float(y @ Va @ y / (y @ y)),
             "symplectic_min": symplectic_check(V) if len(t) <= 1400 else None, "wall_s": round(time.time() - t0, 1)}
        rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
