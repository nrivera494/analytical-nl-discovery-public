#!/usr/bin/env python3
"""lambda_min(V) only, two-polarization Kerr with linear birefringence of strength b = Delta-beta/(gamma P0)
(= 2 pi L_NL/L_B), 45-degree linear input, Gaussian; tests whether Phi_eff(b)/Phi collapses in b for Phi = 5, 10, 20.
Phi_eff is defined by lambda_min = V_min(Phi_eff). Usage: python birefringence_lammin.py out.json"""
import json, sys, time, warnings
import numpy as np
from scipy.optimize import brentq
warnings.filterwarnings("ignore")
from birefringence import propagate
from dlfano import gaussian_p, vmin_kerr
out = sys.argv[1] if len(sys.argv) > 1 else "birefringence_lammin.json"
dt = 0.04; t = np.arange(-7, 7, dt); p = gaussian_p(t)
rows = []
for Phi in (5.0, 10.0, 20.0):
    for b in (0, 0.03, 0.1, 0.2, 0.3, 0.5, 0.667, 1, 1.5, 2, 3, 5, 10, 30, 100):
        t0 = time.time()
        nz = int(max(400, 60 * b * Phi / (2 * np.pi), 40 * Phi))
        Ax, Ay, M = propagate(p, Phi, b, 0.5, nz)
        V = np.einsum("tij,tkj->tik", M, M)
        lm = np.linalg.eigvalsh(V)[:, 0]
        lmin = float(lm.min())
        Pe = brentq(lambda x: vmin_kerr(x) - lmin, 1e-6, 10 * Phi)
        rows.append({"Phi": Phi, "b": b, "nz": nz, "lam_min": lmin, "t_at_min": float(t[np.argmin(lm)]),
                     "Phi_eff_over_Phi": Pe / Phi, "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
