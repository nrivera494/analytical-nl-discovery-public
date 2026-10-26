#!/usr/bin/env python3
"""Does the local-symbol picture explain the next-order coefficient c2 of the lambda_min dispersion law?
Model: lambda(t, W)/V_min(Phi) with the exact CW sideband squeezing lambda_CW(Phi p(t), a = beta2 W^2/2) (exact 2x2
generator, all orders in a) and the exact local V_min(Phi p(t)); ordering H = S (I + K) S - I, S = diag(sqrt(1 + U(t))),
U(t) = V_min(Phi p)/V_min(Phi) - 1, K = F^dag diag(lambda_CW(Phi, W)/V_min(Phi) - 1) F. Ground-state energy vs the
propagated values in lam_min_dispersion.json (Gaussian). Usage: python c2_symbol_model.py out.json"""
import json, sys
import numpy as np
from numpy.fft import fftfreq
from dlfano import vmin_kerr
out = sys.argv[1] if len(sys.argv) > 1 else "c2_symbol_model.json"

def lam_cw(g, a):
    k2 = a * (a + 2 * g)
    k = np.sqrt(np.abs(k2) + 0j)
    c = np.where(k2 >= 0, np.cos(np.sqrt(np.maximum(k2, 0))), np.cosh(np.sqrt(np.maximum(-k2, 0))))
    s_over_k = np.where(np.abs(k2) < 1e-14, 1.0, np.where(k2 >= 0, np.sin(np.sqrt(np.maximum(k2, 1e-300))) / np.sqrt(np.maximum(k2, 1e-300)),
                                                          np.sinh(np.sqrt(np.maximum(-k2, 1e-300))) / np.sqrt(np.maximum(-k2, 1e-300))))
    tr = 2 * c**2 + (a**2 + (a + 2 * g) ** 2) * s_over_k**2
    return (tr - np.sqrt(tr**2 - 4)) / 2

meas = {(r["Phi"], r["y_PhiL_over_LD"]): r["excess"] for r in json.load(open("lam_min_dispersion.json"))["rows"]
        if r["dt"] == 0.01 and r["sign_beta2"] == 1 and r["tcut"] == 1.0 and r["nz"] == 200}
rows = []
for Phi in (5.0, 10.0, 20.0):
    v0 = vmin_kerr(Phi)
    for y in (1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
        beta2 = y / Phi
        tau = (y / 24) ** 0.25
        L = 16 * tau; n = 400
        t = (np.arange(n) - n // 2) * (L / n)
        W = 2 * np.pi * fftfreq(n, L / n)
        p = np.exp(-t**2)
        U = vmin_kerr(Phi * p) / v0 - 1
        Kd = lam_cw(Phi, beta2 * W**2 / 2) / v0 - 1
        F = np.exp(-1j * np.outer(W, t)) / np.sqrt(n)
        Km = (F.conj().T @ (Kd[:, None] * F)).real
        S = np.sqrt(1 + U)
        H = S[:, None] * (np.eye(n) + Km) * S[None, :] - np.eye(n)
        E = float(np.linalg.eigvalsh(0.5 * (H + H.T))[0])
        lead = np.sqrt(2 / 3) * Phi / np.sqrt(1 + Phi**2) * np.sqrt(y)
        m = meas.get((Phi, y))
        rows.append({"Phi": Phi, "y": y, "E_model": E, "leading": lead, "model_over_leading": E / lead,
                     "measured": m, "measured_over_leading": (m / lead) if m else None})
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
