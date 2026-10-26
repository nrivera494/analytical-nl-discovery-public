#!/usr/bin/env python3
"""Does third-order dispersion (parity broken) help binary filters? Kerr + beta3 only (beta2 = 0), Gaussian,
Phi = 10, 20, delta3 = beta3 L/T0^3 in {0, 0.01, 0.03, 0.1, 0.2}; lambda_gen, bandwidth bound, best binary from the
relaxation search. Propagator as momentum_beta3.py. Usage: python binary_vs_beta3.py out.json"""
import json, sys, time, warnings
import numpy as np
from numpy.fft import fft
warnings.filterwarnings("ignore")
from dlfano import gaussian_p
from lin_ssfm import spectral_from_S
from momentum_beta3 import propagate3
from binary_relax_raman import relax_search
out = sys.argv[1] if len(sys.argv) > 1 else "binary_vs_beta3.json"
rng = np.random.default_rng(21)
rows = []
for Phi in (10.0, 20.0):
    dt = 0.03 if Phi <= 10 else 0.02; t = np.arange(-8, 8, dt); p = gaussian_p(t)
    for d3 in (0.0, 0.01, 0.03, 0.1, 0.2):
        t0 = time.time()
        A, S, w = propagate3(p, dt, Phi, 0.0, d3, nz=int(max(300, 30 * Phi)))
        nb, Va, wb = spectral_from_S(A, S, dt, pad=4, thr=1e-6)
        lg = float(np.linalg.eigvalsh(Va)[0])
        sin = np.abs(fft(np.sqrt(p))) ** 2; sout = np.abs(fft(A)) ** 2
        lP = float((w**2 * sin).sum() / sin.sum()) / float((w**2 * sout).sum() / sout.sum())
        r = {"Phi": Phi, "delta3": d3, "lam_gen": lg, "lam_P": lP, "binary_relax": relax_search(nb, Va, wb, rng),
             "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)}
        rows.append(r); print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
