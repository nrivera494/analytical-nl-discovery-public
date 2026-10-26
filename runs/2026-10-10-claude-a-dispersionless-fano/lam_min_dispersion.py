#!/usr/bin/env python3
"""lambda_min(V) with weak dispersion: test of the harmonic-oscillator prediction
    lambda_min / V_min(Phi) - 1 = sqrt(2/3) * Phi/sqrt(1+Phi^2) * sqrt(y),   y = Phi L/L_D = gamma P0 beta2 L^2/T0^2 (beta2 > 0),
for a Gaussian pulse (intensity exp(-t^2/T0^2)). lambda_min is computed as sigma_min(S restricted to input slices with
|t| <= tcut)^2 (an upper bound on the full lambda_min, tight when the optimal input mode lies inside the cut; checked
against tcut and against the full-matrix values in scan_dispersion.json). Grid convergence: dt in {0.04, 0.02, 0.01}.
Usage: python lam_min_dispersion.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import gaussian_p, vmin_kerr
from lin_ssfm import propagate_cols

out = sys.argv[1] if len(sys.argv) > 1 else "lam_min_dispersion.json"
rows = []

def one(Phi, y, sgn, dt, tcut=0.6, nz=200, tmax=6.0):
    t = np.arange(-tmax, tmax + dt / 2, dt)
    t = t - t[np.argmin(np.abs(t))]           # put a grid point exactly at the peak
    p = gaussian_p(t)
    cols = np.where(np.abs(t) <= tcut)[0]
    beta2 = sgn * y / Phi                     # beta2 L / T0^2
    t0 = time.time()
    A, S = propagate_cols(p, dt, Phi, beta2, nz, cols)
    s = np.linalg.svd(S, compute_uv=False)
    lam = float(s[-1] ** 2)
    v0 = float(vmin_kerr(Phi))
    pred = np.sqrt(2 / 3) * Phi / np.sqrt(1 + Phi**2) * np.sqrt(y) if sgn > 0 else None
    return {"Phi": Phi, "y_PhiL_over_LD": y, "x_Phi2L_over_LD": y * Phi, "sign_beta2": sgn, "dt": dt, "tcut": tcut,
            "nz": nz, "lam_min": lam, "Vmin_Phi": v0, "excess": lam / v0 - 1, "pred_excess_leading": pred,
            "wall_s": round(time.time() - t0, 1)}

if __name__ == "__main__":
    import os
    if os.path.exists(out):                     # resume: keep finished rows
        rows.extend(json.load(open(out))["rows"])
    done = {(r["Phi"], r["y_PhiL_over_LD"], r["sign_beta2"], r["dt"], r["tcut"], r["nz"]) for r in rows}
    jobs = []
    ys = (1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1)
    for dt in (0.04, 0.02, 0.01):
        for y in ys:
            jobs.append((10.0, y, 1, dt, 1.0))
    for y in (1e-6, 1e-5, 1e-4, 1e-3):          # finest grid, convergence
        jobs.append((10.0, y, 1, 0.005, 1.0))
    for Phi in (2.0, 5.0, 20.0, 40.0):
        for y in ys:
            jobs.append((Phi, y, 1, 0.01, 1.0))
    for dt in (0.04, 0.02, 0.01, 0.005):       # anomalous sign: grid dependence (MI of dark sidebands)
        jobs.append((10.0, 1e-3, -1, dt, 1.0))
    for tc in (0.6, 2.0):                        # input-cut check
        jobs.append((10.0, 1e-2, 1, 0.01, tc))
    jobs.append((10.0, 1e-3, 1, 0.01, 1.0, 400))  # nz check
    for j in jobs:
        nz = j[5] if len(j) > 5 else 200
        if (j[0], j[1], j[2], j[3], j[4], nz) in done:
            continue
        r = one(*j[:4], tcut=j[4], nz=nz)
        rows.append(r)
        print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
