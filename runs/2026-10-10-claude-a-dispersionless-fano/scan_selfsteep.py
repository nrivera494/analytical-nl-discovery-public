#!/usr/bin/env python3
"""Self-steepening (dispersionless, Kerr only), Gaussian, Phi = 10: lam_min, lam_gen, best binary vs s = 1/(w0 T0),
both signs (time-reversal check), RK4 tangent propagation. Usage: python scan_selfsteep.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import binary_search4, lam_gen, gaussian_p
from lin_ssfm import propagate_ss, spectral_from_S
out = sys.argv[1]
Phi = 10.0; dt = 0.04; t = np.arange(-7, 7, dt); p = gaussian_p(t)
rows = []
for s in (0.0, 0.005, -0.005, 0.01, -0.01, 0.02, -0.02):
    t0 = time.time()
    A, S = propagate_ss(p, dt, Phi, s, nz=600)
    V = S @ S.T
    nb, Va, w = spectral_from_S(A, S, dt, pad=4)
    r = binary_search4(nb, Va, w)
    row = {"Phi": Phi, "s": s, "Phi_s": Phi * s, "lam_min": float(np.linalg.eigvalsh(V)[0]), "lam_gen": lam_gen(Va),
           "binary_F": r["F"], "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)}
    rows.append(row); print(json.dumps(row), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
