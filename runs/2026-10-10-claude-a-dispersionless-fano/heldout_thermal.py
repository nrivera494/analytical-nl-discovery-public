#!/usr/bin/env python3
"""Fifth held-out (HELDOUT.md, commits 7398320 and its correction): Blow-Wood fR = 0.18, Gaussian T0 = 500 fs,
Phi = 15, 150 K and 300 K. Scores lambda_gen / lambda_th and band-limited lambda_min / slice value.
Usage: python heldout_thermal.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, lam_gen, lam_min_band, lag_kernels, gaussian_p, momentum_formula, symplectic_check
out = sys.argv[1] if len(sys.argv) > 1 else "heldout_thermal.json"
sq = np.sqrt(np.pi); I1, I2, Ip2 = sq / 2, 2 * sq / 3**1.5, sq / np.sqrt(2)
T0, Phi, fR = 500.0, 15.0, 0.18
dt = min(0.8 / Phi, 0.04) * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
rows = []
for TK in (150.0, 300.0):
    t0 = time.time()
    m = build_model(p, dt, Phi, fR=fR, temp_K=TK, kern=lag_kernels(len(t), dt, fR, TK))
    V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
    lg = lam_gen(Va); lb = lam_min_band(m, V)[0]
    H0 = 1.276 * TK / 300
    lth = (I1 + 0.5 * Phi * fR * H0 * Ip2) / (I1 + Phi**2 * I2)
    M = np.array([[1, 2 * Phi], [2 * Phi, 1 + 4 * Phi**2 + 2 * Phi * fR * H0]]); ls = float(np.linalg.eigvalsh(M)[0])
    lPR = momentum_formula(lambda tt: gaussian_p(tt, T0), T0, Phi, fR=fR, temp_K=TK, dtf=0.25)["lam_P"]
    r = {"T0_fs": T0, "Phi": Phi, "T_K": TK, "lam_gen": lg, "lam_th": lth, "lam_P_R": lPR, "gen_over_th": lg / lth,
         "bound_holds": bool(lg <= lPR), "gen_window_ok": bool(0.88 <= lg / lth <= 1.0),
         "lam_min_band": lb, "slice": ls, "band_over_slice": lb / ls, "band_window_ok": bool(1.0 <= lb / ls <= 1.15),
         "symplectic_min": symplectic_check(V), "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
