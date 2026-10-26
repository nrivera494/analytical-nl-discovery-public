#!/usr/bin/env python3
"""Ellipticity scan with the validated vector-Raman propagation (vector_raman_prop.py): T0 = 200 fs, Phi = 10,
300 K, split A, chi in {0.1, 0.2, 0.3, 0.5, 0.6, 0.7} rad (0 = linear, pi/4 = circular; pi/8 = 0.3927 is in
vector_raman_prop.json). Polarization-insensitive bins. Usage: python vector_raman_chiscan.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import gaussian_p, binary_search4
from vector_raman_prop import kernels, propagate, bins_insensitive
out = sys.argv[1] if len(sys.argv) > 1 else "vector_raman_chiscan.json"
Phi, T0, TK, fR = 10.0, 200.0, 300.0, 0.245
dt = min(0.8 / Phi, 0.04) * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0); n = len(p)
Rm, Hm = kernels(n, dt, TK, "A", fR)
rows = []
for chi in (0.1, 0.2, 0.3, 0.5, 0.6, 0.7):
    t0 = time.time()
    Ax, Ay, V = propagate(p, dt, Phi, fR, chi, Rm, Hm, nz=400)
    nb, Va, w, nb2, Va2, f2 = bins_insensitive(Ax, Ay, V, dt)
    lg_ins = float(np.linalg.eigvalsh(Va2)[0])
    rb = binary_search4(nb2, Va2, f2)
    P0 = np.abs(Ax) ** 2 + np.abs(Ay) ** 2; Ap = (Ax - 1j * Ay) / np.sqrt(2); k0 = np.argmin(np.abs(t))
    row = {"chi": chi, "T0_fs": T0, "T_K": TK, "Phi": Phi, "split": "A", "lam_min": float(np.linalg.eigvalsh(V)[0]),
           "lam_gen_insensitive": lg_ins, "binary_insensitive": rb["F"],
           "peak_circ_fraction_plus_in": float((np.cos(chi) + np.sin(chi)) ** 2 / 2),
           "peak_circ_fraction_plus_out": float(np.abs(Ap[k0]) ** 2 / P0[k0]), "wall_s": round(time.time() - t0, 1)}
    rows.append(row); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
