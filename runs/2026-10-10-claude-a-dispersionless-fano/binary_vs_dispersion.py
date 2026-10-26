#!/usr/bin/env python3
"""Onset of the dispersion effect on the best binary filter (box-relaxation search), Phi = 10 and 20,
x = Phi^2 L/L_D in {0, 0.01, 0.03, 0.1, 0.3, 1}, both signs (anomalous only to x = 0.3, converged there).
Same propagator and grid as scan_dispersion.py. Usage: python binary_vs_dispersion.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import lam_gen, gaussian_p
from lin_ssfm import propagate, spectral_from_S
from binary_relax_raman import relax_search
out = sys.argv[1] if len(sys.argv) > 1 else "binary_vs_dispersion.json"
rng = np.random.default_rng(17)
rows = []
for Phi in (10.0, 20.0):
    dt = 0.04; t = np.arange(-8, 8, dt); p = gaussian_p(t); nz = int(max(200, 25 * Phi))
    for x, sgn in ((0.0, 1), (0.01, 1), (0.03, 1), (0.1, 1), (0.3, 1), (1.0, 1), (0.01, -1), (0.03, -1), (0.1, -1), (0.3, -1)):
        t0 = time.time()
        A, S = propagate(p, dt, Phi, sgn * x / Phi**2, nz=nz)
        nb, Va, wb = spectral_from_S(A, S, dt, pad=4, thr=1e-6)
        r = {"Phi": Phi, "x": x, "sign_beta2": sgn, "lam_gen": lam_gen(Va), "binary_relax": relax_search(nb, Va, wb, rng),
             "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)}
        rows.append(r); print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
