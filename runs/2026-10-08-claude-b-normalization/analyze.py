"""Equal photon number instead of the gamma_eff energy (run 2026-10-08-claude-b-normalization, claude-b, T-20261008-claude-b-01).

zeta = 2, GRIN LP01/LP02 (C22 = 1/2), delta = 0, p2 = 0.3 and 0.75, launched with the LP01 soliton's photon number
(amplitudes sqrt(p_m) sech, no 1/sqrt(Sigma)). By the argument of claim C-20261008-claude-b-01 the soliton direction
then has soliton order N^2 = Sigma, so the expected first-order behaviour is F_GRIN,photon ~ F_LP01(N^2 = Sigma) + O(q^2).
Compares, for the hard symmetric bands and each launch's own best band: F_GRIN,photon, F_s(N^2 = Sigma) and F_s(N = 1).
Writes summary.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load

RID = "2026-10-08-claude-b-normalization"
g, Cs, ns, _ = load(RID, "z2_scalar")
A1 = tc.class_sym_hard(g, Cs, ns, range(1, 15))
out = {"scalar_N1_best": dict(F=min(A1.values()), kmax=min(A1, key=A1.get))}
for p2 in (0.3, 0.75):
    S = (1 - p2) ** 2 + 2 * (1 - p2) * p2 + 0.5 * p2 ** 2
    _, Cg, ng, _ = load(RID, f"z2_photon_p2_{p2:g}")
    _, Cn, nn, _ = load(RID, f"z2_scalar_N2_{S:.5f}")
    Ag = tc.class_sym_hard(g, Cg, ng, range(1, 15))
    An = tc.class_sym_hard(g, Cn, nn, range(1, 15))
    rows = {}
    for km in range(3, 9):
        rows[km] = dict(F_grin_photon=Ag[km], F_s_N2_Sigma=An[km], F_s_N1=A1[km],
                        grin_minus_sN1=Ag[km] - A1[km], grin_minus_sSigma=Ag[km] - An[km])
    out[f"p2_{p2:g}"] = dict(Sigma=S, bands=rows,
                             best=dict(F_grin_photon=min(Ag.values()), kmax_grin=min(Ag, key=Ag.get),
                                       F_s_N2_Sigma=min(An.values()), kmax_sSigma=min(An, key=An.get),
                                       F_s_N1=out["scalar_N1_best"]["F"],
                                       grin_minus_sN1=min(Ag.values()) - out["scalar_N1_best"]["F"],
                                       grin_minus_sSigma=min(Ag.values()) - min(An.values())))
    b = out[f"p2_{p2:g}"]["best"]
    print(f"p2={p2} Sigma={S:.4f}: best F_GRIN(photon)={b['F_grin_photon']:.5f} (k{b['kmax_grin']}), "
          f"F_s(N^2=Sigma)={b['F_s_N2_Sigma']:.5f} (k{b['kmax_sSigma']}), F_s(N=1)={b['F_s_N1']:.5f}; "
          f"GRIN-LP01 = {b['grin_minus_sN1']:+.4e}, GRIN - scalar(N^2=Sigma) = {b['grin_minus_sSigma']:+.4e}")
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
