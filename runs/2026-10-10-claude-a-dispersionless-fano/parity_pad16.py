#!/usr/bin/env python3
"""Parity bound at padding 16 (bins nbar >= 1e-6 max), Kerr Gaussian Phi = 20, 30; compare with the best binary at
padding 16 (binary_relax_pad16.json, binary_relax2_pad16.json). Usage: python parity_pad16.py out.json"""
import json, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "parity_pad16.json"
best = {}
for f in ("binary_relax_pad16.json", "binary_relax2_pad16.json"):
    for r in json.load(open(f))["rows"]:
        if "best_F" in r:
            best[r["Phi"]] = min(best.get(r["Phi"], 9), r["best_F"])
rows = []
for Phi in (20.0, 30.0):
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=16, thr=1e-6)
    key = {round(x, 9): i for i, x in enumerate(w)}
    P = np.zeros((len(w), len(w)))
    for i, x in enumerate(w):
        j = key.get(round(-x, 9)); P[i, j if j is not None else i] = 1.0
    ev, U = np.linalg.eigh(P)
    lo = float(np.linalg.eigvalsh(U[:, ev < 0].T @ Va @ U[:, ev < 0])[0]); le = float(np.linalg.eigvalsh(U[:, ev > 0].T @ Va @ U[:, ev > 0])[0])
    Fp = (lo + le) / 2 if lo <= le else le
    r = {"Phi": Phi, "pad": 16, "n_bins": int(len(nb)), "lam_odd": lo, "lam_even": le, "parity_bound": Fp,
         "best_binary_pad16": best.get(Phi), "bound_respected": bool(best.get(Phi, 9) >= Fp),
         "gap_dB": float(10 * np.log10(best[Phi] / Fp)) if Phi in best else None}
    rows.append(r); print(json.dumps(r), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
