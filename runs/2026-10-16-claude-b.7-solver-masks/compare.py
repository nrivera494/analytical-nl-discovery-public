"""Post-freeze comparison with claude-b's numpy values (read only after summary.json was hashed).

Writes comparison.json: claude-b's eta values from
runs/2026-10-16-claude-b-dw-shaping/opt_N3_d0.05_xi2.json against this run's solver values on the
same grid (TW = 70, Nt = 1024), at omega0 T0 = 1e6 (summary.json) and 1e8 (results_ss.jsonl,
run after the freeze to test the self-steepening residual s = 1/(omega0 T0)).
"""
import json
import os

RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-b.7-solver-masks")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "2026-10-16-claude-b-dw-shaping", "opt_N3_d0.05_xi2.json")
cb = json.load(open(SRC))
v2 = [json.loads(l) for l in open(os.path.join(RAW, "results_v2.jsonl")) if l.strip()]
ss = [json.loads(l) for l in open(os.path.join(RAW, "results_ss.jsonl")) if l.strip()]


def get(recs, mask, n, tagprefix="R"):
    for r in recs:
        if r["mask"] == mask and r["nsteps"] == n and r["tag"].startswith(tagprefix) and r["mode"] == "exact" \
                and r["TW"] == 70.0 and r["Nt"] == 1024:
            return r
    raise KeyError((mask, n))


claude_b = {"TL": {"eta_B": cb["eta_TL"], "eta_B_h/2": cb["eta_TL_h2"],
                   "eta_G": cb["best_phase_diag"]["gated_TL"]},
            "phase": {"eta_B": cb["eta_phase"], "eta_G": cb["best_phase_diag"]["gated"]},
            "passive": {"eta_B": cb["passive"]["eta"], "energy_kept": cb["passive"]["energy_kept"]}}
out = {"source": "runs/2026-10-16-claude-b-dw-shaping/opt_N3_d0.05_xi2.json (claude-b numpy, TW 70, Nt 1024, h 0.001)",
       "convention": "relative difference = claude-b / solver - 1", "by_mask": {}}
for m in ("TL", "phase", "passive"):
    e = {"claude-b": claude_b[m]}
    for label, recs, tag in (("solver_w0T0_1e6", v2, "R"), ("solver_w0T0_1e8", ss, "R_w0T0")):
        for n in (2000, 8000):
            r = get(recs, m, n, tag)
            d = {"eta_B": r["eta_B"], "eta_G": r["eta_G"], "E_in_over_E_laser": r["E_in_over_E_laser"]}
            d["reldiff_eta_B"] = claude_b[m]["eta_B"] / r["eta_B"] - 1
            if "eta_G" in claude_b[m]:
                d["reldiff_eta_G"] = claude_b[m]["eta_G"] / r["eta_G"] - 1
            if "energy_kept" in claude_b[m]:
                d["reldiff_energy_kept"] = claude_b[m]["energy_kept"] / r["E_in_over_E_laser"] - 1
            e[f"{label}_n{n}"] = d
    out["by_mask"][m] = e
json.dump(out, open(os.path.join(HERE, "comparison.json"), "w"), indent=1)
for m, e in out["by_mask"].items():
    for k, d in e.items():
        if k == "claude-b":
            print(m, "claude-b", d)
        else:
            print("   ", k, {kk: (f"{vv:.3e}" if kk.startswith("reldiff") else vv) for kk, vv in d.items()})
