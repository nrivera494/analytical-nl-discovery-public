#!/usr/bin/env python3
"""Kerr-only dispersionless scan: lambda_min(V), lambda_pass, lambda_gen, best binary filter (nested tabu search),
over Phi_peak, for the Gaussian pulse; bin-resolution convergence (pad 4 and 8) and the momentum-weight value.
Usage: python scan_kerr.py out.json [pulse=gaussian|sech] [Phis comma-separated]"""
import json
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from dlfano import (build_model, covariance, lam_min, lam_pass, spectral, lam_gen, binary_search4,
                    gaussian_p, sech_p, vmin_kerr, symplectic_check)

out = sys.argv[1]
pulse = sys.argv[2] if len(sys.argv) > 2 else "gaussian"
Phis = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [1, 2, 3, 5, 7, 10, 15, 20, 30]
rows = []
for Phi in Phis:
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi)
    tmax = 7.0 if pulse == "gaussian" else 14.0
    t = np.arange(-tmax, tmax, dt)
    p = gaussian_p(t) if pulse == "gaussian" else sech_p(t, 0.9445)
    m = build_model(p, dt, Phi)
    V = covariance(m)
    row = {"Phi": Phi, "dt": dt, "tmax": tmax, "N_t": len(t), "lam_min": lam_min(V), "anchor": float(vmin_kerr(Phi)),
           "lam_pass": lam_pass(V, p), "symplectic_min": symplectic_check(V) if len(t) <= 600 else None}
    for pad in (4, 8):
        nb, Va, idx, w = spectral(m, V, pad=pad, thr=1e-6)
        s = np.sqrt(nb)
        y = w * s
        r = binary_search4(nb, Va, w)
        row[f"pad{pad}"] = {"n_bins": int(len(nb)), "lam_gen": lam_gen(Va),
                            "lam_momentum": float(y @ Va @ y / (y @ y)),
                            "binary_F": r["F"], "binary_selected": int(r["T"].sum())}
    row["wall_s"] = round(time.time() - t0, 1)
    rows.append(row)
    print(json.dumps({k: v for k, v in row.items()}), flush=True)
    with open(out, "w") as f:
        json.dump({"pulse": pulse, "rows": rows}, f, indent=1)
