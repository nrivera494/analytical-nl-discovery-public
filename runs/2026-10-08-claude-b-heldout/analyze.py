"""Score the frozen predictions (predictions.json, committed before the held-out cases were computed) against the
held-out runs (run 2026-10-08-claude-b-heldout, claude-b, T-20261008-claude-b-01).
For every case and filter: Delta F actual = F_case(T) - F_s(T) (F_s from run 2026-10-08-claude-b-kw-map at the same zeta),
predicted Delta F, ratio and relative error, and pass/fail against the frozen tolerance (as frozen in predictions.json: 25% for H2, 20% for H4, 15% otherwise, on
|actual - predicted| / |predicted|). Writes summary.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, scalar_optima

KW, RID = "2026-10-08-claude-b-kw-map", "2026-10-08-claude-b-heldout"
pred = json.load(open(os.path.join(HERE, "predictions.json")))
TOL = pred["tolerances_rel_err"]
out, worst = {}, {}
for key, pv in pred.items():
    if not isinstance(pv, dict) or "filters" not in pv:
        continue
    name, zt = key.split("_")
    g, Cs, ns, _ = load(KW, f"{zt}_scalar")
    _, Ct, nt, _ = load(RID, key)
    opt = scalar_optima(g, Cs, ns)
    filters = {f"kmax{k}": (np.abs(g.k) <= k).astype(float) for k in (3, 4, 5, 6, 7)}
    for cls in ("sym_hard", "sym_frac", "interval"):
        filters["opt_" + cls] = opt[cls][1]
    rows = {}
    for fname, T in filters.items():
        Fs = tc.fano(T, Cs, ns)
        act = tc.fano(T, Ct, nt) - Fs
        pr = pv["filters"][fname]["dF_pred"]
        rel = abs(act - pr) / abs(pr)
        rows[fname] = dict(dF_actual=act, dF_pred=pr, ratio=act / pr, rel_err=rel, pass_=bool(rel <= TOL[name]))
        worst[name] = max(worst.get(name, 0), rel)
    out[key] = rows
    print(key, {f: f"{r['ratio']:.3f}{'' if r['pass_'] else ' FAIL'}" for f, r in rows.items()})
out["worst_rel_err_by_case"] = worst
out["tolerances"] = TOL
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
