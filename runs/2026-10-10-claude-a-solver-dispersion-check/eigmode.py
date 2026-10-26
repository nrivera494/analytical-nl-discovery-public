"""Where does the most-squeezed mode of V live? Spectral and temporal moments of the
eigenvector of the smallest eigenvalue of V (z = X + iY, N-point DFT).

Usage: ~/agent-work/venv/bin/python runs/2026-10-10-claude-a-solver-dispersion-check/eigmode.py case ...
Writes <raw>/eigmode_<case>.json.
"""
import json
import os
import sys

import numpy as np

RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-a-solver-dispersion-check")

for case in sys.argv[1:]:
    d = np.load(os.path.join(RAW, case + ".npz"))
    S = d["S"]
    t = d["t_ps"]
    N = len(t)
    dt = float(t[1] - t[0])
    V = S @ S.T
    w, U = np.linalg.eigh(0.5 * (V + V.T))
    v = U[:, 0]
    z = v[:N] + 1j * v[N:]
    zw = np.fft.fft(z)
    om = 2 * np.pi * np.fft.fftfreq(N, d=dt)
    p = np.abs(zw) ** 2
    p /= p.sum()
    tw = np.abs(z) ** 2
    tw /= tw.sum()
    tc = float((tw * t).sum())
    res = {
        "case": case,
        "lambda_min_full_V": float(w[0]),
        "min_mode_peak_abs_omega_rad_per_ps": float(abs(om[np.argmax(p)])),
        "min_mode_rms_abs_omega_rad_per_ps": float(np.sqrt((p * om ** 2).sum())),
        "min_mode_time_centroid_ps": tc,
        "min_mode_rms_width_ps": float(np.sqrt((tw * (t - tc) ** 2).sum())),
    }
    with open(os.path.join(RAW, f"eigmode_{case}.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res))
