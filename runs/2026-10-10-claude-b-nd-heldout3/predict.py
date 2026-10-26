"""Held-out set 3 (claude-b, T-20261010-claude-interactive-05), frozen before computing: N = 18, z/z_wb = 0.9 (Nt 1024,
40 T0). Predictions from the reduced curve curve_N200.json (formula), the centroid closed form, and the parity-bracket
pattern seen on the grid:
  P1 lambda_min = Lambda(Z)/N^2 (1 - c/Phi^2), 0 <= c <= 2
  P2 F_centroid = 1/(1 + 2 N^2 K(Z)) within 1 %, lambda_gen within 1 dB below it
  P3 F_par (parity bound of C-20261010-claude-a-03) >= lambda_gen * 10^0.7  (>= 7 dB)
  P4 2 dB <= 10 log10(F_bin / F_par) <= 6.5 dB  (best binary from the stage-1 search plus refine_binary.refine)
Writes predictions.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-semiclassical")
cr = sorted(json.load(open(os.path.join(SC, "curve_N200.json")))["rows"], key=lambda r: r["Z"])
cZ = np.array([r["Z"] for r in cr]); fL = np.array([4 * r["Z"] ** 2 * r["Lambda_red"] for r in cr])
fK = np.array([(np.sqrt(np.pi / 2) - r["int_rho2"]) / np.sqrt(np.pi) / r["Z"] ** 2 for r in cr])
N, zr = 18, 0.9
Z = zr * N / np.sqrt(4 * N ** 2 * np.exp(-1.5) - 1)
Lam = np.interp(Z, cZ, fL) / (4 * Z ** 2); K = np.interp(Z, cZ, fK) * Z ** 2
pred = dict(N=N, zr=zr, Z=Z, Phi=N * Z, lam_min_formula=Lam / N ** 2, lam_min_lo=Lam / N ** 2 * (1 - 2 / (N * Z) ** 2),
            F_centroid=1 / (1 + 2 * N ** 2 * K), F_centroid_rel_tol=0.01, lam_gen_max_dB_below_centroid=1.0,
            Fpar_min_dB_over_gen=7.0, bin_over_Fpar_dB_range=[2.0, 6.5], frozen_note="committed before computing")
json.dump(pred, open(os.path.join(HERE, "predictions.json"), "w"), indent=1)
json.dump([dict(tag="N18_zr0.9", N=18, zr=0.9, Nt=1024, TW=40.0)], open(os.path.join(HERE, "cases.json"), "w"), indent=1)
print(json.dumps(pred, indent=1))
