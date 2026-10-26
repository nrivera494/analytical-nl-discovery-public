#!/usr/bin/env python3
"""Completes scan_dispersion.json at Phi = 20 (rows lost when that scan was stopped): x = 0.3 (anomalous), 1, 3
(both signs). Same propagator and grid as scan_dispersion.py (lin_ssfm.propagate, dt = 0.04, |t| < 8, nz = 500, pad 4,
threshold 1e-6). Reports lambda_min, lambda_gen, lambda_P(beta2) = <w^2>_in/<w^2>_out, and the best binary from the
box-relaxation search (binary_relax_raman.relax_search). Usage: python scan_dispersion_phi20_rest.py out.json"""
import json, sys, time, warnings
import numpy as np
from numpy.fft import fft, fftfreq
warnings.filterwarnings("ignore")
from dlfano import lam_gen, gaussian_p
from lin_ssfm import propagate, spectral_from_S
from binary_relax_raman import relax_search
out = sys.argv[1] if len(sys.argv) > 1 else "scan_dispersion_phi20_rest.json"
Phi = 20.0; dt = 0.04; t = np.arange(-8, 8, dt); p = gaussian_p(t); nz = 500
rng = np.random.default_rng(13)
w = 2 * np.pi * fftfreq(len(t), dt)
w2 = lambda A: float((w**2 * np.abs(fft(A)) ** 2).sum() / (np.abs(fft(A)) ** 2).sum())
rows = []
for x, sgn in ((0.3, -1), (1.0, 1), (1.0, -1), (3.0, 1), (3.0, -1)):
    t0 = time.time()
    A, S = propagate(p, dt, Phi, sgn * x / Phi**2, nz=nz)
    V = S @ S.T
    nb, Va, wb = spectral_from_S(A, S, dt, pad=4, thr=1e-6)
    lg = lam_gen(Va)
    lP = w2(np.sqrt(p).astype(complex)) / w2(A)
    Fb = relax_search(nb, Va, wb, rng)
    r = {"Phi": Phi, "x_Phi2L_over_LD": x, "sign_beta2": sgn, "lam_min": float(np.linalg.eigvalsh(V)[0]), "lam_gen": lg,
         "lam_P_beta2": lP, "gen_over_P": lg / lP, "bound_holds": bool(lg <= lP), "binary_relax": Fb,
         "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
