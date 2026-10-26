#!/usr/bin/env python3
"""Hypothesis for the remaining half of c2: normal dispersion reshapes the mean field and lowers the peak intensity at
O(y), so the peak sees Phi_eff = Phi * <p(0, z)>_z. Prediction: lambda_min ~ V_min(Phi_eff) * (1 + E_model), with E_model
from c2_symbol_model.json. Compared with lam_min_dispersion.json (Gaussian). Usage: python c2_reshaping_check.py out.json"""
import json, sys
import numpy as np
from numpy.fft import fft, ifft, fftfreq
from dlfano import vmin_kerr, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "c2_reshaping_check.json"
model = {(r["Phi"], r["y"]): r["E_model"] for r in json.load(open("c2_symbol_model.json"))["rows"]}
meas = {(r["Phi"], r["y_PhiL_over_LD"]): r["lam_min"] for r in json.load(open("lam_min_dispersion.json"))["rows"]
        if r["dt"] == 0.01 and r["sign_beta2"] == 1 and r["tcut"] == 1.0 and r["nz"] == 200}
rows = []
for Phi in (5.0, 10.0, 20.0):
    dt = 0.01; t = np.arange(-6, 6 + dt / 2, dt); t = t - t[np.argmin(np.abs(t))]; p = gaussian_p(t); k0 = np.argmin(np.abs(t))
    w = 2 * np.pi * fftfreq(len(t), dt)
    for y in (1e-5, 1e-4, 1e-3, 1e-2):
        beta2 = y / Phi; nz = 400; dz = 1.0 / nz
        lin_half = np.exp(1j * 0.5 * beta2 * w**2 * dz / 2)
        A = np.sqrt(p).astype(complex); peaks = []
        for _ in range(nz):
            A = ifft(lin_half * fft(A)); A = A * np.exp(1j * Phi * np.abs(A) ** 2 * dz); A = ifft(lin_half * fft(A))
            peaks.append(np.abs(A[k0]) ** 2)
        pbar = float(np.mean(peaks))
        Phi_eff = Phi * pbar
        pred = vmin_kerr(Phi_eff) * (1 + model[(Phi, y)])
        m = meas.get((Phi, y))
        rows.append({"Phi": Phi, "y": y, "mean_peak_p": pbar, "pred_symbol_plus_reshaping": float(pred), "measured": m,
                     "pred_over_measured": float(pred / m) if m else None,
                     "symbol_only_over_measured": float(vmin_kerr(Phi) * (1 + model[(Phi, y)]) / m) if m else None})
        print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
