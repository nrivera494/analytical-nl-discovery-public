#!/usr/bin/env python3
"""Breakdown of the dispersionless theory: linearized SSFM (lin_ssfm.py) with small beta2 of both signs.
Grid of Phi and x = Phi^2 L/L_D; reports lam_min, lam_gen, best binary (nested tabu) and their ratio to the
dispersionless (beta2 = 0) values. Usage: python scan_dispersion.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import binary_search4, lam_gen, gaussian_p
from lin_ssfm import propagate, spectral_from_S
out = sys.argv[1]
rows = []
for Phi in (5.0, 10.0, 20.0):
    dt = min(0.04, 0.8 / Phi); t = np.arange(-8, 8, dt); p = gaussian_p(t)
    nz = int(max(200, 25 * Phi))
    base = None
    for x in (0.0, 1e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0):
        for sgn in ((1,) if x == 0 else (1, -1)):
            t0 = time.time()
            delta = sgn * x / Phi**2          # beta2 L / T0^2 (signed)
            A, S = propagate(p, dt, Phi, delta, nz=nz)
            V = S @ S.T
            lm = float(np.linalg.eigvalsh(V)[0])
            nb, Va, w = spectral_from_S(A, S, dt, pad=4, thr=1e-6)
            lg = lam_gen(Va)
            r = binary_search4(nb, Va, w)
            row = {"Phi": Phi, "x_Phi2L_over_LD": x, "sign_beta2": sgn, "beta2L_over_T0sq": delta, "nz": nz,
                   "lam_min": lm, "lam_gen": lg, "binary_F": r["F"], "n_bins": int(len(nb)),
                   "wall_s": round(time.time() - t0, 1)}
            if x == 0:
                base = row
            row["ratio_to_dispersionless"] = {k: row[k] / base[k] for k in ("lam_min", "lam_gen", "binary_F")}
            rows.append(row)
            print(json.dumps(row), flush=True)
            json.dump({"rows": rows}, open(out, "w"), indent=1)
