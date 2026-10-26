#!/usr/bin/env python3
"""Compare lambda_gen and the grid momentum-weight value (scan_raman_gaussian.json) with the 1D-integral bound
lambda_P,R (dlfano.momentum_formula) and with its long-pulse thermal limit
    lambda_th = [I1 + (Phi/2) fR H(0) int p'^2] / [I1 + Phi^2 I2]   (Gaussian, T0 = 1 units),
    H(0) = 4 kB T |d_w Im h(0)| / hbar = 1.276 at 300 K (Blow-Wood).  Usage: python raman_momentum_compare.py"""
import json
import numpy as np
from dlfano import momentum_formula, gaussian_p
rows = json.load(open("scan_raman_gaussian.json"))["rows"]
sq = np.sqrt(np.pi)
I1, I2, Ip2 = sq / 2, 2 * sq / 3**1.5, sq / np.sqrt(2)
out = []
for r in rows:
    T0, Phi, TK, fR = r["T0_fs"], r["Phi"], r["T_K"], r["fR"]
    mf = momentum_formula(lambda t: gaussian_p(t, T0), T0, Phi, fR=fR, temp_K=TK, dtf=min(0.25, T0 / 200))
    H0 = 1.276 * TK / 300.0
    lth = (I1 + 0.5 * Phi * fR * H0 * Ip2) / (I1 + Phi**2 * I2)
    o = {"T0_fs": T0, "Phi": Phi, "T_K": TK, "lam_gen": r["lam_gen"], "lam_momentum_grid": r["lam_momentum"],
         "lam_P_R_formula": mf["lam_P"], "lam_thermal_longpulse": lth, "lam_min_band": r["lam_min_band"],
         "binary_F": r["binary_F"], "gen_over_PR": r["lam_gen"] / mf["lam_P"], "grid_over_formula": r["lam_momentum"] / mf["lam_P"],
         "gen_over_min_band": r["lam_gen"] / r["lam_min_band"]}
    out.append(o)
    print(" ".join(f"{k}={v:.5g}" for k, v in o.items()))
json.dump({"rows": out}, open("raman_momentum_compare.json", "w"), indent=1)
