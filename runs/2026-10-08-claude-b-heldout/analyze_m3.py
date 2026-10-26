"""Score the frozen three-mode predictions (predictions_m3.json, commit fb713de) against the computed cases H6, H7
(run 2026-10-08-claude-b-heldout, claude-b). Writes summary_m3.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, scalar_optima

KW, RAW = "2026-10-08-claude-b-kw-map", os.path.expanduser("~/analytical-nl-discovery-data/2026-10-08-claude-b-heldout")
pred = json.load(open(os.path.join(HERE, "predictions_m3.json")))
TOL = pred["tolerances_rel_err"]
out, worst = {}, {}
for key, pv in pred.items():
    if not isinstance(pv, dict) or "filters" not in pv:
        continue
    name, zt = key.split("_")
    g, Cs, ns, _ = load(KW, f"{zt}_scalar")
    d = np.load(os.path.join(RAW, key + ".npz"))
    Ct, nt = d["Ct"], d["nt"]
    opt = scalar_optima(g, Cs, ns)
    filters = {f"kmax{k}": (np.abs(g.k) <= k).astype(float) for k in (3, 4, 5, 6, 7)}
    for cls in ("sym_hard", "sym_frac", "interval"):
        filters["opt_" + cls] = opt[cls][1]
    rows = {}
    for fname, T in filters.items():
        act = tc.fano(T, Ct, nt) - tc.fano(T, Cs, ns)
        pr = pv["filters"][fname]["dF_pred"]
        rel = abs(act - pr) / abs(pr)
        rows[fname] = dict(dF_actual=act, dF_pred=pr, ratio=act / pr, rel_err=rel, pass_=bool(rel <= TOL[name]))
        worst[name] = max(worst.get(name, 0), rel)
    out[key] = rows
    print(key, {f: f"{r['ratio']:.3f}{'' if r['pass_'] else ' FAIL'}" for f, r in rows.items()})
out["worst_rel_err_by_case"] = worst
out["tolerances"] = TOL
json.dump(out, open(os.path.join(HERE, "summary_m3.json"), "w"), indent=1, default=float)
print(worst)
