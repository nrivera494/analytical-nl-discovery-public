"""Optimized-filter comparison at finite parameters (run 2026-10-08-claude-b-optimum, claude-b, T-20261008-claude-b-01).

zeta = 2, GRIN LP01/LP02 overlaps (C22 = 1/2), delta = 0, p2 = 0.3, 0.5, 0.75, 0.9. For each filter class (applied to all
modes): min over the class of F_GRIN and of F_s, each optimized separately; their difference, in absolute value and dB;
and F_GRIN at the LP01 optimum. Convergence of the p2 = 0.75 case: half step (dz = 1e-3), finer sampling (N = 512 over
40 T0: same frequency bins), doubled window (N = 512 over 80 T0: frequency spacing halved, so classes A and B are finer;
compare the continuous-edge class A' and class C). Writes summary.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2, scalar_optima

RID = "2026-10-08-claude-b-optimum"


def class_min_all(g, Ct, nt, T_hint):
    A = tc.class_sym_hard(g, Ct, nt, range(0, g.N // 8))
    Ap, _ = tc.class_sym_frac(g, Ct, nt, range(0, g.N // 8))
    B = tc.class_interval(g, Ct, nt)
    kA = min(A, key=A.get)
    starts = [T_hint, (np.abs(g.k) <= kA).astype(float), 0.5 * np.ones(g.N), np.ones(g.N),
              (np.abs(g.k) <= Ap["kmax"]).astype(float) + Ap["f"] * (np.abs(g.k) == Ap["kmax"] + 1)]
    Cr, _ = tc.class_any(g, Ct, nt, starts)
    return {"sym_hard": (A[kA], dict(kmax=kA, edge=(kA + 0.5) * g.dw)), "sym_frac": (Ap["F"], Ap), "interval": (B["F"], B), "any": (Cr["F"], {})}


out = {}
for variant in ("", "_halfdz", "_N512", "_TW80"):
    g, Cs, ns, _ = load(RID, "z2_scalar" + variant)
    opt = scalar_optima(g, Cs, ns, kmax_max=g.N // 8)
    p2s = (0.3, 0.5, 0.75, 0.9) if variant == "" else (0.75,)
    res = {"scalar_optima": {k: dict(F=v[0], filter={kk: vv for kk, vv in v[2].items() if not isinstance(vv, np.ndarray)}) for k, v in opt.items()}}
    for p2 in p2s:
        _, Ct, nt, _ = load(RID, f"z2_p2_{p2:g}" + variant)
        mins = class_min_all(g, Ct, nt, opt["any"][1])
        rows = {}
        for cls in ("sym_hard", "sym_frac", "interval", "any"):
            Fs = opt[cls][0]
            Fg = mins[cls][0]
            rows[cls] = dict(min_F_s=Fs, min_F_grin=Fg, diff=Fg - Fs, diff_dB=10 * np.log10(Fg / Fs),
                             F_grin_at_lp01_opt=tc.fano(opt[cls][1], Ct, nt),
                             grin_filter={k: v for k, v in mins[cls][1].items() if not isinstance(v, np.ndarray)},
                             q2=q2(p2, 1, 0.5))
        res[f"p2_{p2:g}"] = rows
    out[variant or "base"] = res
    print(variant or "base", {k: {c: f"{v['diff']:+.3e}" for c, v in r.items()} for k, r in res.items() if k.startswith("p2")}, flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
