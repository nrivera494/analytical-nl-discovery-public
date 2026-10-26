#!/usr/bin/env python3
"""Held-out test (HELDOUT.md, commit 98430d6) of the momentum bound with third-order dispersion (parity broken):
lambda_gen <= lambda_P = <w^2>_in / <w^2>_out (c = 0; also min over c), Kerr + beta2 + beta3, Gaussian.
Linearized split-step as lin_ssfm.propagate with linear factor exp(i(beta2/2 w^2 - beta3/6 w^3) dz)
(d_z A = -(i/2) beta2 A_tt + (beta3/6) A_ttt + i gamma |A|^2 A). Bins: pad 8, threshold 1e-9.
Usage: python momentum_beta3.py out.json"""
import json, sys, time, warnings
import numpy as np
from numpy.fft import fft, ifft, fftfreq
warnings.filterwarnings("ignore")
from dlfano import gaussian_p
from lin_ssfm import spectral_from_S

def propagate3(p, dt, Phi, beta2, beta3, nz):
    n = len(p); w = 2 * np.pi * fftfreq(n, dt); dz = 1.0 / nz
    lin_half = np.exp(1j * (0.5 * beta2 * w**2 - beta3 / 6 * w**3) * dz / 2)
    A = np.sqrt(p).astype(complex)
    P = np.zeros((n, 2 * n), complex)
    P[np.arange(n), np.arange(n)] = 0.5; P[np.arange(n), n + np.arange(n)] = 0.5j
    for _ in range(nz):
        A = ifft(lin_half * fft(A)); P = ifft(lin_half[:, None] * fft(P, axis=0), axis=0)
        I = np.abs(A) ** 2; th = np.angle(A)
        b = np.exp(-1j * th)[:, None] * P
        b = b + 2j * Phi * (I / nz)[:, None] * b.real
        A = A * np.exp(1j * Phi * I / nz)
        P = np.exp(1j * (th + Phi * I / nz))[:, None] * b
        A = ifft(lin_half * fft(A)); P = ifft(lin_half[:, None] * fft(P, axis=0), axis=0)
    return A, np.vstack([2 * P.real, 2 * P.imag]), w

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "momentum_beta3.json"
    rows = []
    for Phi in (5.0, 10.0):
        dt = 0.04 if Phi <= 5 else 0.03; t = np.arange(-8, 8, dt); p = gaussian_p(t)
        for b2 in (0.0, 0.1 / Phi**2):
            for d3 in (0.01, -0.01, 0.05, -0.05):
                t0 = time.time()
                A, S, w = propagate3(p, dt, Phi, b2, d3, nz=int(max(300, 30 * Phi)))
                nb, Va, wb = spectral_from_S(A, S, dt, pad=8, thr=1e-9)
                lg = float(np.linalg.eigvalsh(Va)[0])
                sin = np.abs(fft(np.sqrt(p))) ** 2; sout = np.abs(fft(A)) ** 2
                m2 = lambda s, c: float(((w - c) ** 2 * s).sum() / s.sum())
                lP0 = m2(sin, 0.0) / m2(sout, 0.0)
                cs = np.linspace(-2, 2, 401); lPc = min(m2(sin, c) / m2(sout, c) for c in cs)
                cent_out = float((w * sout).sum() / sout.sum())
                y = wb * np.sqrt(nb); lmom = float(y @ Va @ y / (y @ y))
                r = {"Phi": Phi, "beta2L_T0sq": b2, "delta3": d3, "lam_gen": lg, "lam_P_c0": lP0, "lam_P_minc": lPc,
                     "lam_mom_grid": lmom, "gen_over_P": lg / lP0, "bound_holds": bool(lg <= lP0 * (1 + 1e-9)),
                     "in_frozen_window": bool(0.75 <= lg / lP0 <= 1.0), "output_centroid": cent_out,
                     "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)}
                rows.append(r); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
                json.dump({"rows": rows}, open(out, "w"), indent=1)
