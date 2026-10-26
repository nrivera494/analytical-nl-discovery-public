#!/usr/bin/env python3
"""Kerr + Raman (Blow-Wood, symmetrized coth reservoir) dispersionless scan over T0, temperature and Phi:
lambda_min(V), lambda_pass, lambda_gen, momentum-weight value, best binary filter (nested tabu search).
Usage: python scan_raman.py out.json [pulse] [T0 list fs] [temps K] [Phis] [fR]"""
import json
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from dlfano import (build_model, covariance, lam_min, lam_pass, spectral, lam_gen, binary_search4,
                    gaussian_p, sech_p, lag_kernels, symplectic_check, lam_min_band, vmin_kerr)

out = sys.argv[1]
pulse = sys.argv[2] if len(sys.argv) > 2 else "gaussian"
T0s = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [50, 100, 200, 500, 1000]
temps = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [0.0, 300.0]
Phis = [float(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else [2, 5, 10, 20]
fR = float(sys.argv[6]) if len(sys.argv) > 6 else 0.18
pad = 8
rows = []
for T0 in T0s:
    for Phi in Phis:
        dt = min(0.8 / Phi, 0.04) * T0               # resolves the SPM band; Raman kernels are bin-averaged
        tmax = (7.0 if pulse == "gaussian" else 14.0) * T0
        t = np.arange(-tmax, tmax, dt)
        Ts = 0.9445 * T0
        p = gaussian_p(t, T0) if pulse == "gaussian" else sech_p(t, Ts)
        for TK in temps:
            t0 = time.time()
            kern = lag_kernels(len(t), dt, fR, TK)
            m = build_model(p, dt, Phi, fR=fR, temp_K=TK, kern=kern)
            V = covariance(m)
            nb, Va, idx, w = spectral(m, V, pad=pad, thr=1e-6)
            s = np.sqrt(nb)
            y = w * s
            r = binary_search4(nb, Va, w)
            row = {"pulse": pulse, "T0_fs": T0, "Phi": Phi, "T_K": TK, "fR": fR, "dt_fs": dt, "N_t": len(t), "pad": pad,
                   "n_bins": int(len(nb)), "lam_min": lam_min(V), "lam_min_band": lam_min_band(m, V)[0], "Vmin_instKerr": float(vmin_kerr((1 - fR) * Phi)), "lam_pass": lam_pass(V, p), "lam_gen": lam_gen(Va),
                   "lam_momentum": float(y @ Va @ y / (y @ y)), "binary_F": r["F"],
                   "binary_selected": int(r["T"].sum()),
                   "symplectic_min": symplectic_check(V) if len(t) <= 500 else None,
                   "wall_s": round(time.time() - t0, 1)}
            rows.append(row)
            print(json.dumps(row), flush=True)
            with open(out, "w") as f:
                json.dump({"rows": rows}, f, indent=1)
