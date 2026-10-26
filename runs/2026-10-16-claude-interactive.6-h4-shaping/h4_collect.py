"""Collect H4 optimizer results (raw folders) into summary.json for the repository."""
import os, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-interactive.6-h4-shaping")
out = {"run_id": "2026-10-16-claude-interactive.6-h4-shaping", "starts": {}}
fd = os.path.join(D, "fdcheck_phase_1.75", "log.txt")
if os.path.exists(fd):
    out["fdcheck"] = [l.strip() for l in open(fd) if l.startswith("fdcheck")]
for d in sorted(glob.glob(os.path.join(D, "*_*_*"))):
    name = os.path.basename(d)
    if name.startswith("fdcheck") or not os.path.isdir(d):
        continue
    rec = {}
    rp = os.path.join(d, "result.txt")
    if os.path.exists(rp):
        for l in open(rp):
            k, v = l.split()
            rec[k] = float(v)
    hp = os.path.join(d, "history.txt")
    if os.path.exists(hp):
        rec["history_J"] = [float(x) for x in np.atleast_1d(np.loadtxt(hp))]
    ep = os.path.join(d, "numpy_eval.json")
    if os.path.exists(ep):
        rec["numpy_eval_dz0.25mm"] = json.load(open(ep))
    bp = os.path.join(d, "best_phase.txt")
    if os.path.exists(bp):
        M = np.loadtxt(bp)
        W, phi, m = M[:, 0], M[:, 1], M[:, 2]
        rec["phase_stats"] = {"pixels": int(len(W)), "min_amplitude": float(m.min()), "mean_amplitude": float(m.mean())}
    out["starts"][name] = rec
sp = os.path.join(HERE, "summary_chirp_scan.json")
if os.path.exists(sp):
    out["chirp_scan"] = json.load(open(sp))
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "history_J"} for k, v in out["starts"].items()}, indent=1))
