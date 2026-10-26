#!/usr/bin/env python3
"""Dense Phi scan (Kerr, Gaussian, dispersionless): lambda_gen / lambda_P and the parity-sector eigenvalues
lambda_odd, lambda_even (no binary search). Purpose: error order of lambda_gen ~ lambda_P and the oscillation of
lambda_even. Grid as scan_kerr (dt = min(0.04, 0.8/Phi), |t| < 7, pad 8). Usage: python lam_gen_dense.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "lam_gen_dense.json"
Phis = list(np.arange(2, 30.5, 1.0)) + list(np.arange(32, 61, 2.0))
rows = []
for Phi in Phis:
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
    key = {round(x, 9): i for i, x in enumerate(w)}
    P = np.zeros((len(w), len(w)))
    for i, x in enumerate(w):
        j = key.get(round(-x, 9)); P[i, j if j is not None else i] = 1.0
    ev, U = np.linalg.eigh(P)
    lo = np.linalg.eigvalsh(U[:, ev < 0].T @ Va @ U[:, ev < 0]); le = np.linalg.eigvalsh(U[:, ev > 0].T @ Va @ U[:, ev > 0])
    lP = 1 / (1 + 4 * Phi**2 / (3 * np.sqrt(3)))
    y = w * np.sqrt(nb); lmom = float(y @ Va @ y / (y @ y))
    rows.append({"Phi": float(Phi), "lam_gen": float(min(lo[0], le[0])), "lam_odd": float(lo[0]), "lam_even": float(le[0]),
                 "odd2": float(lo[1]), "even2": float(le[1]), "lam_P": lP, "lam_momentum_grid": lmom,
                 "ratio_gen_P": float(min(lo[0], le[0]) / lP), "parity_bound": float((lo[0] + le[0]) / 2),
                 "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)})
    print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
