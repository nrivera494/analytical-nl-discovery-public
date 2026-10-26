#!/usr/bin/env python3
"""Test of the open prediction in C-20261010-claude-a-03 (registered at commit cb7ad63): dispersionless Kerr Gaussian,
40 < Phi <= 100, bins nbar >= 1e-6 max (padding 8): lambda_even >= 0.05, hence F_par >= 0.025.
Grid as scan_kerr (dt = min(0.04, 0.8/Phi), |t| < 7). Usage: python open_prediction_lameven.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "open_prediction_lameven.json"
rows = []
for Phi in (70.0, 85.0, 100.0):
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
    key = {round(x, 9): i for i, x in enumerate(w)}
    P = np.zeros((len(w), len(w)))
    for i, x in enumerate(w):
        j = key.get(round(-x, 9)); P[i, j if j is not None else i] = 1.0
    ev, U = np.linalg.eigh(P)
    lo = float(np.linalg.eigvalsh(U[:, ev < 0].T @ Va @ U[:, ev < 0])[0]); le = float(np.linalg.eigvalsh(U[:, ev > 0].T @ Va @ U[:, ev > 0])[0])
    Fp = (lo + le) / 2 if lo <= le else le
    r = {"Phi": Phi, "n_bins": int(len(nb)), "lam_odd": lo, "lam_even": le, "parity_bound": Fp,
         "prediction_holds": bool(le >= 0.05), "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps(r), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
