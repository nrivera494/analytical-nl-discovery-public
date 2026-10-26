#!/usr/bin/env python3
"""Threshold and time-step convergence of lambda_gen, the momentum readout and the parity eigenvalues at large Phi
(Kerr, Gaussian, dispersionless). thr in {1e-6, 1e-9, 1e-12}; dt in {0.8/Phi, 0.4/Phi} (capped at 0.04). pad 8.
Usage: python grid_check2.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "grid_check2.json"
rows = []
for Phi in (20.0, 30.0, 40.0, 60.0):
    for fdt, thr in ((0.8, 1e-6), (0.8, 1e-9), (0.8, 1e-12), (0.4, 1e-9)):
        t0 = time.time()
        dt = min(0.04, fdt / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
        m = build_model(p, dt, Phi); V = covariance(m)
        nb, Va, idx, w = spectral(m, V, pad=8, thr=thr)
        y = w * np.sqrt(nb); lmom = float(y @ Va @ y / (y @ y))
        key = {round(x, 9): i for i, x in enumerate(w)}
        P = np.zeros((len(w), len(w)))
        for i, x in enumerate(w):
            j = key.get(round(-x, 9)); P[i, j if j is not None else i] = 1.0
        ev, U = np.linalg.eigh(P)
        lo = float(np.linalg.eigvalsh(U[:, ev < 0].T @ Va @ U[:, ev < 0])[0]); le = float(np.linalg.eigvalsh(U[:, ev > 0].T @ Va @ U[:, ev > 0])[0])
        lP = 1 / (1 + 4 * Phi**2 / (3 * np.sqrt(3)))
        rows.append({"Phi": Phi, "dt": dt, "thr": thr, "n_bins": int(len(nb)), "lam_gen": min(lo, le), "lam_odd": lo, "lam_even": le,
                     "lam_mom_grid": lmom, "lam_P": lP, "gen_over_P": min(lo, le) / lP, "mom_over_P": lmom / lP,
                     "parity_bound": (lo + le) / 2 if lo <= le else le, "wall_s": round(time.time() - t0, 1)})
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
