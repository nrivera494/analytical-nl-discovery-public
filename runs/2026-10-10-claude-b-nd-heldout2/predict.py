"""Frozen held-out predictions for the semiclassical formulas (claude-b, T-20261010-claude-interactive-05).
Written and committed BEFORE the three cases below are computed.

Cases (Gaussian, pure Kerr, normal dispersion; z/z_wb with z_wb = L_D / sqrt(4 N^2 e^{-3/2} - 1)):
  N16_zr0.5   N = 16, z/z_wb = 0.5   (Z ~ 0.53, before breaking; Z and N not on the scoring grid)
  N24_zr1.25  N = 24, z/z_wb = 1.25  (Z ~ 1.32, at the measured onset of oscillations Z_b ~ 1.25)
  N12_zr2.5   N = 12, z/z_wb = 2.5   (Z ~ 2.66, after breaking)
Predictions use only the reduced curve curve_N50.json of run 2026-10-10-claude-b-nd-semiclassical (no oracle data):
  P1  lambda_min = Lambda(Z)/N^2 (1 - c/Phi^2) with 0 <= c <= 2, Phi = N Z      [leading order + bound on the correction]
  P2  lambda_pass = Pi(Z)/N^2 (1 - e) with 0 <= e <= 0.05                         [leading order, odd sector]
  P3  lambda_pass = lambda_2(V) to relative 1e-6                                   [parity]
  P4  F_centroid = <dw^2>_in/<dw^2>_out = 1/(1 + 2 N^2 K(Z)) within 1 %           [energy identity, K from the curve]
  P5  F_centroid * 10^(-0.1) <= lambda_gen <= F_centroid                           [upper: exact; lower: empirical 1 dB]
  P6  best binary filter found >= lambda_gen * 10^(1.0)                           [binary gap at least 10 dB]
Writes predictions.json.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
curve = json.load(open(os.path.join(HERE, "..", "2026-10-10-claude-b-nd-semiclassical", "curve_N50.json")))
cr = sorted(curve["rows"], key=lambda r: r["Z"])
cZ = np.array([r["Z"] for r in cr])
fL = np.array([4 * r["Z"] ** 2 * r["Lambda_red"] for r in cr])
fP = np.array([4 * r["Z"] ** 2 / r["sigma2_C"] ** 2 for r in cr])
fK = np.array([(np.sqrt(np.pi / 2) - r["int_rho2"]) / np.sqrt(np.pi) / r["Z"] ** 2 for r in cr])


def xi_wb(N):
    return 1.0 / np.sqrt(4 * N ** 2 * np.exp(-1.5) - 1)


cases = [dict(tag="N16_zr0.5", N=16, zr=0.5, Nt=1024, TW=40.0),
         dict(tag="N24_zr1.25", N=24, zr=1.25, Nt=1024, TW=40.0),
         dict(tag="N12_zr2.5", N=12, zr=2.5, Nt=1024, TW=60.0)]
pred = {}
for c in cases:
    N = c["N"]
    Z = c["zr"] * N * xi_wb(N)
    Phi = N * Z
    Lam = np.interp(Z, cZ, fL) / (4 * Z ** 2)
    Pi = np.interp(Z, cZ, fP) / (4 * Z ** 2)
    K = np.interp(Z, cZ, fK) * Z ** 2
    Fc = 1 / (1 + 2 * N ** 2 * K)
    pred[c["tag"]] = dict(N=N, zr=c["zr"], Z=Z, Phi=Phi,
                          lam_min=dict(formula=Lam / N ** 2, lo=Lam / N ** 2 * (1 - 2 / Phi ** 2), hi=Lam / N ** 2),
                          lam_pass=dict(formula=Pi / N ** 2, lo=0.95 * Pi / N ** 2, hi=Pi / N ** 2),
                          lam_pass_equals_lam_2_rel=1e-6,
                          F_centroid=dict(pred=Fc, rel_tol=0.01),
                          lam_gen=dict(lo_factor_of_F_centroid=10 ** -0.1, hi_factor_of_F_centroid=1.0),
                          F_bin_min_gap_dB_over_lam_gen=10.0)
pred["frozen_note"] = "Committed before the three cases were computed; predictions use curve_N50.json only."
json.dump(pred, open(os.path.join(HERE, "predictions.json"), "w"), indent=1)
json.dump(cases, open(os.path.join(HERE, "cases.json"), "w"), indent=1)
print(json.dumps(pred, indent=1))
