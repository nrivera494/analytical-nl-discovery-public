"""Post-hoc (not frozen) scaling of the third-order corrections (run 2026-10-08-claude-b-thirdorder, claude-b,
T-20261008-claude-b-01). Added after the held-out cases H1-H5 missed several frozen tolerances.

A. Off-diagonal defect C12 = 1 - x (C22 = 1), p2 = 0.2 and 0.3, zeta = 2 and 5, x = 0.025 .. 1/3:
   ratio(x) = Delta F / (K0 ||q||^2) with K0 from run 2026-10-08-claude-b-kw-map (built from C22 = 1/2 only).
   Universality at second order requires ratio -> 1 as x -> 0; a third-order correction gives ratio - 1 ~ x.
B. Diagonal defect C22 = 1 - eps (C12 = 1), p2 = 0.3, eps = 1/16, 1/8, 1/4: ratio(eps), expected ratio - 1 ~ eps p2.
C. Cross term at zeta = 2, p2 = 0.3, delta = 0.3: X(eps) = DF(eps, delta) - DF(eps, 0) - DF(0, delta) for eps = 1/8, 1/4, 1/2;
   the second-order form has no cross term, so X is third order, expected ~ eps delta^2.
Filters: the LP01-optimal hard band at each zeta (kmax 5 at zeta = 2, 4 at zeta = 5) and kmax = 3..7.
Writes summary.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2, r2

RID, KW = "2026-10-08-claude-b-thirdorder", "2026-10-08-claude-b-kw-map"
out = {}
for z, kopt in ((2.0, 5), (5.0, 4)):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(RID, f"{zt}_scalar")
    kwr = {k: load(KW, f"{zt}_{k}")[1:3] for k in ("K_p2_0.1", "K_p2_0.2")}
    res = {}
    for km in (3, 4, 5, 6, 7):
        T = (np.abs(g.k) <= km).astype(float)
        Fs = tc.fano(T, Cs, ns)
        K0 = 2 * (tc.fano(T, *kwr["K_p2_0.1"]) - Fs) / q2(0.1, 1, 0.5) - (tc.fano(T, *kwr["K_p2_0.2"]) - Fs) / q2(0.2, 1, 0.5)
        rowsA = {}
        for p2 in (0.2, 0.3):
            rr = []
            for x in (0.025, 0.05, 0.1, 0.2, 1 / 3):
                _, Ct, nt, _ = load(RID, f"{zt}_C12_{1 - x:.4f}_p2_{p2:g}")
                dF = tc.fano(T, Ct, nt) - Fs
                Q = q2(p2, 1 - x, 1.0)
                rr.append(dict(x=x, dF=dF, q2=Q, ratio=dF / (K0 * Q)))
            for a, b in zip(rr[:-1], rr[1:]):
                b["exponent_of_ratio_minus_1"] = float(np.log(abs(b["ratio"] - 1) / abs(a["ratio"] - 1)) / np.log(b["x"] / a["x"]))
            rowsA[f"p2_{p2:g}"] = rr
        rowsB = []
        for e in (0.0625, 0.125, 0.25):
            _, Ct, nt, _ = load(RID, f"{zt}_C22_{1 - e:g}_p2_0.3")
            dF = tc.fano(T, Ct, nt) - Fs
            Q = q2(0.3, 1.0, 1 - e)
            rowsB.append(dict(eps=e, dF=dF, q2=Q, ratio=dF / (K0 * Q)))
        for a, b in zip(rowsB[:-1], rowsB[1:]):
            b["exponent_of_ratio_minus_1"] = float(np.log(abs(b["ratio"] - 1) / abs(a["ratio"] - 1)) / np.log(b["eps"] / a["eps"]))
        res[f"kmax{km}"] = dict(F_s=Fs, K0=K0, A_offdiagonal=rowsA, B_diagonal=rowsB)
    if z == 2.0:
        cross = {}
        for km in (3, 4, 5, 6, 7):
            T = (np.abs(g.k) <= km).astype(float)
            Fs = tc.fano(T, Cs, ns)
            d0 = tc.fano(T, *load(RID, "z2_cross_eps_0_d0.3")[1:3]) - Fs
            rows = []
            for e in (0.125, 0.25, 0.5):
                dboth = tc.fano(T, *load(RID, f"z2_cross_eps_{e:g}_d0.3")[1:3]) - Fs
                de = tc.fano(T, *load(RID, f"z2_cross_eps_{e:g}_d0")[1:3]) - Fs
                rows.append(dict(eps=e, dF_both=dboth, dF_eps=de, dF_delta=d0, cross=dboth - de - d0,
                                 cross_over_W_term=(dboth - de - d0) / d0))
            for a, b in zip(rows[:-1], rows[1:]):
                b["exponent_of_cross"] = float(np.log(abs(b["cross"] / a["cross"])) / np.log(b["eps"] / a["eps"]))
            cross[f"kmax{km}"] = rows
        res["cross_term"] = cross
    res["lp01_opt_kmax"] = kopt
    out[zt] = res
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
for zt, res in out.items():
    k = f"kmax{res['lp01_opt_kmax']}"
    r = res[k]
    print(zt, k, "K0", round(r["K0"], 4))
    for p, rows in r["A_offdiagonal"].items():
        print("  A", p, [(round(x["x"], 3), round(x["ratio"], 4), round(x.get("exponent_of_ratio_minus_1", 0), 2)) for x in rows])
    print("  B", [(x["eps"], round(x["ratio"], 4), round(x.get("exponent_of_ratio_minus_1", 0), 2)) for x in r["B_diagonal"]])
    if "cross_term" in res:
        print("  C", [(x["eps"], f"{x['cross']:+.3e}", round(x["cross_over_W_term"], 3), round(x.get("exponent_of_cross", 0), 2)) for x in res["cross_term"][k]])
