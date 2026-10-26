#!/usr/bin/env python3
"""Held-out evaluation (frozen in HELDOUT.md before computing): sech pulse, Kerr and Raman 300 K (T_s = 188.9 fs)."""
import json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import (build_model, covariance, lam_min, lam_pass, spectral, lam_gen, binary_search4, sech_p,
                    lag_kernels, vmin_kerr)
rows = []
for case, fR, TK in (("kerr", 0.0, 300.0), ("raman300", 0.18, 300.0)):
    for Phi in (5.0, 15.0):
        t0 = time.time()
        T0 = 200.0                                   # fs reference; Ts = 0.9445 T0
        Ts = 0.9445 * T0
        dt = min(0.8 / Phi, 0.04) * T0
        t = np.arange(-14 * T0, 14 * T0, dt)
        p = sech_p(t, Ts)
        kern = lag_kernels(len(t), dt, fR, TK) if fR > 0 else None
        m = build_model(p, dt, Phi, fR=fR, temp_K=TK, kern=kern)
        V = covariance(m)
        nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
        r = binary_search4(nb, Va, w)
        row = {"case": case, "Phi": Phi, "lam_min": lam_min(V), "lam_pass": lam_pass(V, p), "lam_gen": lam_gen(Va),
               "binary_F": r["F"], "n_bins": int(len(nb)), "N_t": len(t), "wall_s": round(time.time() - t0, 1)}
        rows.append(row); print(json.dumps(row), flush=True)
        json.dump({"rows": rows}, open("heldout_results.json", "w"), indent=1)
