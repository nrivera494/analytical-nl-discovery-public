#!/usr/bin/env python3
"""Why the 5 ps open prediction failed: band-limited lambda_min / slice value vs band width at T0 = 5 ps, Phi = 10,
300 K (Blow-Wood, fR = 0.18). If the excess is the cost of the band cutoff, it should scale ~ (Omega_b T0)^-2.
Usage: python band_cost_check.py out.json"""
import json, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, lam_min_band, lag_kernels, gaussian_p
out = sys.argv[1] if len(sys.argv) > 1 else "band_cost_check.json"
T0, Phi, fR, TK = 5000.0, 10.0, 0.18, 300.0
M = np.array([[1, 2 * Phi], [2 * Phi, 1 + 4 * Phi**2 + 2 * Phi * fR * 1.276]]); ls = float(np.linalg.eigvalsh(M)[0])
dt = 0.02 * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
m = build_model(p, dt, Phi, fR=fR, temp_K=TK, kern=lag_kernels(len(t), dt, fR, TK)); V = covariance(m)
rows = []
for bf, ex in ((1.2, 3.0), (1.8, 4.5), (2.4, 6.0), (3.6, 9.0), (4.8, 12.0)):
    lb, Wb, nsel = lam_min_band(m, V, band_factor=bf, extra=ex)
    r = {"band_factor": bf, "extra": ex, "Omega_b_T0": float(Wb * T0), "n_modes": nsel, "lam_min_band": lb, "slice": ls, "excess": lb / ls - 1}
    rows.append(r); print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
x = np.log([r["Omega_b_T0"] for r in rows]); y = np.log([r["excess"] for r in rows])
print("slope of log(excess) vs log(Omega_b T0):", float(np.polyfit(x, y, 1)[0]))
json.dump({"rows": rows}, open(out, "w"), indent=1)
