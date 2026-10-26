#!/usr/bin/env python3
"""Structure of the best binary filters found (Kerr, Gaussian, dispersionless, pad 8, thr 1e-6): photon fraction on
w > 0, odd-sector weight fraction f_odd = |y_odd|^2/|y|^2 (<= 1/2 for any non-negative filter), the contributions of
the odd and even sectors to F, overlap with the momentum mode, and number of contiguous selected blocks.
Usage: python binary_structure.py out.json"""
import glob, json, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p, fano_of
RAW = "~/analytical-nl-discovery-data/2026-10-10-claude-a-dispersionless-fano"
out = sys.argv[1] if len(sys.argv) > 1 else "binary_structure.json"
rows = []
for Phi in (7.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0):
    cands = []
    for f in glob.glob(f"{RAW}/binary_relax*_gaussian_Phi{Phi:g}.npz"):
        z = np.load(f); cands.append(z)
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
    best = None
    for z in cands:
        if len(z["w"]) != len(w) or np.abs(z["w"] - w).max() > 1e-9:
            continue
        F = fano_of(z["T"], nb, Va)
        if best is None or F < best[0]:
            best = (F, z["T"])
    if best is None:
        continue
    F, T = best
    y = T * np.sqrt(nb)
    key = {round(x, 9): i for i, x in enumerate(w)}
    mir = np.array([key.get(round(-x, 9), i) for i, x in enumerate(w)])
    ye, yo = (y + y[mir]) / 2, (y - y[mir]) / 2
    n2 = y @ y
    Fe, Fo = ye @ Va @ ye / n2, yo @ Va @ yo / n2
    mom = w * np.sqrt(nb); mom /= np.linalg.norm(mom)
    o = np.argsort(w); Ts = T[o]
    blocks = int(((Ts[1:] == 1) & (Ts[:-1] == 0)).sum() + (Ts[0] == 1))
    rows.append({"Phi": Phi, "F": float(F), "frac_photons_w_pos": float((T * nb * (w > 0)).sum() / (T * nb).sum()),
                 "f_odd": float(yo @ yo / n2), "F_from_even": float(Fe), "F_from_odd": float(Fo),
                 "overlap2_momentum": float((mom @ y) ** 2 / n2), "n_selected": int(T.sum()), "n_bins": int(len(nb)),
                 "selected_blocks": blocks})
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
