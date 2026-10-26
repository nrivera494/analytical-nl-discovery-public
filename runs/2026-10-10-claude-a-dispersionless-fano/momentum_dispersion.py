#!/usr/bin/env python3
"""Mean-field-only check of the momentum bound with dispersion: lambda_P(beta2) = <w^2>_in / <w^2>_out(beta2),
an upper bound on lambda_gen for any number- and momentum-conserving dynamics (Kerr + any linear dispersion).
Compares with lambda_gen from scan_dispersion.json (same grid, same propagator). Usage: python momentum_dispersion.py"""
import json
import numpy as np
from numpy.fft import fft, ifft, fftfreq
from dlfano import gaussian_p

def field_out(p, dt, Phi, beta2, nz):
    n = len(p); w = 2 * np.pi * fftfreq(n, dt); dz = 1.0 / nz
    lin_half = np.exp(1j * 0.5 * beta2 * w**2 * dz / 2)
    A = np.sqrt(p).astype(complex)
    for _ in range(nz):
        A = ifft(lin_half * fft(A)); A = A * np.exp(1j * Phi * np.abs(A)**2 * dz); A = ifft(lin_half * fft(A))
    return A, w

def w2(A, w):
    s = np.abs(fft(A))**2
    return float((w**2 * s).sum() / s.sum())

rows = json.load(open("scan_dispersion.json"))["rows"]
out = []
for r in rows:
    Phi = r["Phi"]; dt = min(0.04, 0.8 / Phi); t = np.arange(-8, 8, dt); p = gaussian_p(t)
    A, w = field_out(p, dt, Phi, r["beta2L_over_T0sq"], r["nz"])
    w2in = w2(np.sqrt(p).astype(complex), w); w2out = w2(A, w)
    lamP = w2in / w2out
    out.append({"Phi": Phi, "x": r["x_Phi2L_over_LD"], "sign": r["sign_beta2"], "w2_in": w2in, "w2_out": w2out,
                "lam_P_beta2": lamP, "lam_gen": r["lam_gen"], "lam_gen_over_lam_P": r["lam_gen"] / lamP,
                "bound_holds": bool(r["lam_gen"] <= lamP * (1 + 1e-9))})
    print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in out[-1].items()}))
json.dump({"rows": out}, open("momentum_dispersion.json", "w"), indent=1)
