"""Exponent tests (run 2026-10-08-claude-b-exponents, claude-b, T-20261008-claude-b-01).

Filters: the LP01-optimal hard symmetric band at each zeta (class A), plus kmax = 3..7 for reference.
1. First-order null in epsilon = 1 - C22 (C12 = 1, delta = 0, p2 = 0.2): even and odd parts of
   Delta F(e) = F(C22 = 1 - e) - F_s over e = +-0.125, +-0.25, +-0.5. Prediction: even ~ e^2, odd ~ e^3 (no e^1 term).
2. p2 scaling (C22 = 1/2, delta = 0): Delta F / (eps^2 p1 p2^3) -> constant K as p2 -> 0; local exponent of Delta F -> 3.
3. delta scaling (Manakov overlaps, p2 = 0.5): Delta F / (delta^2 p1 p2) -> constant W; local exponent -> 2.
4. p1 p2 scaling of the walk-off term (delta = 0.2, p2 = 0.1, 0.3, 0.5).
Writes summary.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2, r2

RID = "2026-10-08-claude-b-exponents"
out = {}
for z in (2.0, 5.0):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(RID, f"{zt}_scalar")
    A = tc.class_sym_hard(g, Cs, ns, range(0, 15))
    kA = min(A, key=A.get)
    filters = {f"kmax{k}": (np.abs(g.k) <= k).astype(float) for k in (3, 4, 5, 6, 7)}
    res = {"lp01_class_A_optimum_kmax": kA, "F_s": {name: tc.fano(T, Cs, ns) for name, T in filters.items()}}

    def dF(tag, T):
        g2, Ct, nt, _ = load(RID, tag)
        return tc.fano(T, Ct, nt) - tc.fano(T, Cs, ns)

    # 1. epsilon parity
    eps_rows = {}
    for name, T in filters.items():
        rows = []
        for e in (0.125, 0.25, 0.5):
            dp = dF(f"{zt}_eps_C22_{1 - e:g}_p2_0.2", T)     # C22 = 1 - e  (epsilon = +e)
            dm = dF(f"{zt}_eps_C22_{1 + e:g}_p2_0.2", T)     # C22 = 1 + e  (epsilon = -e)
            rows.append(dict(e=e, dF_plus=dp, dF_minus=dm, even=(dp + dm) / 2, odd=(dp - dm) / 2))
        for r0, r1 in zip(rows[:-1], rows[1:]):
            r1["even_exponent"] = float(np.log(abs(r1["even"] / r0["even"])) / np.log(r1["e"] / r0["e"]))
            r1["odd_exponent"] = float(np.log(abs(r1["odd"] / r0["odd"])) / np.log(r1["e"] / r0["e"]))
        eps_rows[name] = rows
    res["epsilon_parity"] = eps_rows

    # 2. p2 scaling at C22 = 1/2
    p2_rows = {}
    for name, T in filters.items():
        rows = []
        for p2 in (0.025, 0.05, 0.1, 0.2, 0.4):
            tag = f"{zt}_eps_C22_0.5_p2_0.2" if p2 == 0.2 else f"{zt}_p2_{p2:g}_C22_0.5"
            d = dF(tag, T)
            rows.append(dict(p2=p2, dF=d, q2=q2(p2, 1.0, 0.5), K_eff=d / q2(p2, 1.0, 0.5)))
        for r0, r1 in zip(rows[:-1], rows[1:]):
            r1["dF_exponent_vs_p2"] = float(np.log(abs(r1["dF"] / r0["dF"])) / np.log(r1["p2"] / r0["p2"]))
        p2_rows[name] = rows
    res["p2_scaling"] = p2_rows

    # 3. delta scaling at Manakov overlaps, p2 = 0.5
    d_rows = {}
    for name, T in filters.items():
        rows = []
        for dl in (0.05, 0.1, 0.2, 0.4):
            d = dF(f"{zt}_delta_{dl:g}_p2_0.5_C22_1", T)
            rows.append(dict(delta=dl, dF=d, r2=r2(0.5, dl), W_eff=d / r2(0.5, dl)))
        for r0, r1 in zip(rows[:-1], rows[1:]):
            r1["dF_exponent_vs_delta"] = float(np.log(abs(r1["dF"] / r0["dF"])) / np.log(r1["delta"] / r0["delta"]))
        d_rows[name] = rows
    res["delta_scaling"] = d_rows

    # 4. p1 p2 scaling of the walk-off term at delta = 0.2
    w_rows = {}
    for name, T in filters.items():
        rows = []
        for p2 in (0.1, 0.3, 0.5):
            tag = f"{zt}_delta_0.2_p2_0.5_C22_1" if p2 == 0.5 else f"{zt}_delta_0.2_p2_{p2:g}_C22_1"
            d = dF(tag, T)
            rows.append(dict(p2=p2, dF=d, r2=r2(p2, 0.2), W_eff=d / r2(p2, 0.2)))
        w_rows[name] = rows
    res["walkoff_p2_scaling"] = w_rows
    out[zt] = res
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
for zt, res in out.items():
    k = f"kmax{res['lp01_class_A_optimum_kmax']}" if f"kmax{res['lp01_class_A_optimum_kmax']}" in res["F_s"] else "kmax5"
    print(zt, "LP01 class-A optimum kmax", res["lp01_class_A_optimum_kmax"], "| reporting filter", k)
    for r in res["epsilon_parity"][k]:
        print("  eps", r)
    for r in res["p2_scaling"][k]:
        print("  p2 ", r)
    for r in res["delta_scaling"][k]:
        print("  dl ", r)
    for r in res["walkoff_p2_scaling"][k]:
        print("  wp2", r)
