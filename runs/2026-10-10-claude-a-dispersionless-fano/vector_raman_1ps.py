#!/usr/bin/env python3
"""Elliptical input (chi = pi/8) with vector Raman at T0 = 1 ps, Phi = 10, 0 and 300 K, split A (validated propagation
of vector_raman_prop.py); compare with linear/circular exact reductions at 1 ps (vector_raman_exact.json).
Usage: python vector_raman_1ps.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import gaussian_p, binary_search4
from vector_raman_prop import kernels, propagate, bins_insensitive
out = sys.argv[1] if len(sys.argv) > 1 else "vector_raman_1ps.json"
Phi, T0, fR, chi = 10.0, 1000.0, 0.245, np.pi / 8
dt = min(0.8 / Phi, 0.04) * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0); n = len(p)
rows = []
for TK in (0.0, 300.0):
    t0 = time.time()
    Rm, Hm = kernels(n, dt, TK, "A", fR)
    Ax, Ay, V = propagate(p, dt, Phi, fR, chi, Rm, Hm, nz=400)
    nb, Va, w, nb2, Va2, f2 = bins_insensitive(Ax, Ay, V, dt)
    lg = float(np.linalg.eigvalsh(Va2)[0]); rb = binary_search4(nb2, Va2, f2)
    P0 = np.abs(Ax) ** 2 + np.abs(Ay) ** 2; Ap = (Ax - 1j * Ay) / np.sqrt(2); k0 = np.argmin(np.abs(t))
    r = {"T0_fs": T0, "T_K": TK, "chi": chi, "Phi": Phi, "split": "A", "lam_gen_insensitive": lg, "binary_insensitive": rb["F"],
         "sigma_plus_peak_in": float((np.cos(chi) + np.sin(chi)) ** 2 / 2), "sigma_plus_peak_out": float(np.abs(Ap[k0]) ** 2 / P0[k0]),
         "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
