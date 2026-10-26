#!/usr/bin/env python3
"""Parity bound for non-negative spectral weights (binary filters included), symmetric pulse, Kerr (dispersionless).
For a parity-symmetric problem (V^amp commutes with w -> -w), any weight vector y = T sqrt(nbar) >= 0 has
|y_even|^2 >= |y_odd|^2, so  F[T] >= (lam_odd + lam_even)/2,  lam_odd/even = lowest eigenvalue of V^amp in each sector.
Also reports the low part of each sector's spectrum. Usage: python parity_bound.py out.json [Phis]"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p, sech_p

out = sys.argv[1] if len(sys.argv) > 1 else "parity_bound.json"
Phis = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [1, 2, 3, 5, 7, 10, 15, 20, 30]
pulse = sys.argv[3] if len(sys.argv) > 3 else "gaussian"
rows = []
for Phi in Phis:
    t0 = time.time()
    if pulse == "gaussian":
        dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    else:
        dt = min(0.04, 0.8 / Phi); t = np.arange(-14, 14, dt); p = sech_p(t, 0.9445)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
    # parity pairing on the kept bins
    key = {round(x, 9): i for i, x in enumerate(w)}
    P = np.zeros((len(w), len(w)))
    unpaired = 0
    for i, x in enumerate(w):
        j = key.get(round(-x, 9))
        if j is None:
            unpaired += 1; P[i, i] = 1.0
        else:
            P[i, j] = 1.0
    comm = float(np.abs(P @ Va - Va @ P).max())
    ev, U = np.linalg.eigh(P)                       # +1 even, -1 odd
    Ue, Uo = U[:, ev > 0], U[:, ev < 0]
    le = np.linalg.eigvalsh(Ue.T @ Va @ Ue); lo = np.linalg.eigvalsh(Uo.T @ Va @ Uo)
    r = {"pulse": pulse, "Phi": Phi, "n_bins": int(len(nb)), "unpaired_bins": unpaired, "parity_commutator_max": comm,
         "lam_odd": float(lo[0]), "lam_even": float(le[0]), "parity_bound": float((lo[0] + le[0]) / 2),
         "odd_low5": [float(x) for x in lo[:5]], "even_low5": [float(x) for x in le[:5]],
         "n_even_below1": int((le < 1).sum()), "n_odd_below1": int((lo < 1).sum()), "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps(r), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
