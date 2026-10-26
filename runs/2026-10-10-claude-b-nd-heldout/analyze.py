"""Score the frozen held-out predictions (predictions.json, commit 895cc71) against the N = 40 runs of this run id
(claude-b, T-20261010-claude-interactive-05). Also compares with the reduced semiclassical coefficient Lambda(Z) of run
2026-10-10-claude-b-nd-semiclassical (computed after the freeze; not part of the frozen test). Writes summary.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
pred = json.load(open(os.path.join(HERE, "predictions.json")))
rows = {json.loads(l)["tag"]: json.loads(l) for l in open(os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-heldout/rows.jsonl"))}
tol = pred["tolerances"]
out = {}
for key in ("N40_zr0.7", "N40_zr1"):
    if key not in rows:
        continue
    r, p = rows[key], pred[key]
    res = {}
    for q in ("lam_min", "lam_pass", "lam_gen"):
        rel = abs(r[q] / p[q]["pred"] - 1)
        res[q] = dict(actual=r[q], pred=p[q]["pred"], rel_err=rel, pass_=bool(rel <= tol[q]))
    d = abs(r["F_interval"] - p["F_interval"]["pred"])
    res["F_interval"] = dict(actual=r["F_interval"], pred=p["F_interval"]["pred"], abs_err=d, pass_=bool(d <= tol["F_interval_abs"]))
    res["F_best_found"] = r["F_best"]
    res["Z"] = r["N"] * r["xi"]
    out[key] = res
    print(key, {q: (round(v["actual"], 7), round(v["pred"], 7), "PASS" if v["pass_"] else "FAIL") for q, v in res.items() if isinstance(v, dict)}, "F_best", round(r["F_best"], 4))
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
