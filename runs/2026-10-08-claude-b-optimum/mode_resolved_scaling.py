"""Scaling and length dependence of the mode-resolved gain (exploration within T-20261008-claude-b-01; claude-b).
Uses best_mode_resolved() of mode_resolved.py on stored covariances of run 2026-10-08-claude-b-exponents:
(1) zeta = 2, p2 = 0.2, C22 = 1 -+ e (e = 1/8, 1/4, 1/2): gain = min R - min F_s (LP01, hard symmetric band);
    the Manakov control in mode_resolved.json gives zero gain, so the gain should be even and quadratic in e;
(2) zeta = 5, GRIN p2 = 0.2 and 0.4 (where the common-filter difference is positive).
Writes mode_resolved_scaling.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load
from mode_resolved import best_mode_resolved, blocks

RAW = os.path.expanduser("~/analytical-nl-discovery-data")
E = "2026-10-08-claude-b-exponents"
res = {}
g, Cs, ns, _ = load(E, "z2_scalar")
Fs = min(tc.class_sym_hard(g, Cs, ns, range(1, 15)).values())
rows = []
for C22 in (0.875, 0.75, 0.5, 1.125, 1.25, 1.5):
    nbar, Caa, Cab, Cbb = blocks(os.path.join(RAW, E, f"z2_eps_C22_{C22:g}_p2_0.2.npz"))
    b = best_mode_resolved(g, nbar, Caa, Cab, Cbb)
    rows.append(dict(eps=1 - C22, R=b["R"], gain=b["R"] - Fs, w_b=b["w"][1], kmax_a=b["kmax_a"], kmax_b=b["kmax_b"]))
    print("z2 eps", round(1 - C22, 3), "R", round(b["R"], 6), "gain", f"{b['R'] - Fs:+.3e}", "w_b", round(b["w"][1], 4),
          "bands", b["kmax_a"], b["kmax_b"], flush=True)
res["z2_eps_scan_p2_0.2"] = dict(F_s_best=Fs, rows=rows)
g, Cs, ns, _ = load(E, "z5_scalar")
Fs5 = min(tc.class_sym_hard(g, Cs, ns, range(1, 15)).values())
for tag, p2 in (("z5_eps_C22_0.5_p2_0.2", 0.2), ("z5_p2_0.4_C22_0.5", 0.4)):
    nbar, Caa, Cab, Cbb = blocks(os.path.join(RAW, E, tag + ".npz"))
    b = best_mode_resolved(g, nbar, Caa, Cab, Cbb)
    res[f"z5_p2_{p2:g}"] = dict(F_s_best=Fs5, gain=b["R"] - Fs5, gain_dB=10 * np.log10(b["R"] / Fs5), **b)
    print("z5 p2", p2, "R", round(b["R"], 6), "LP01", round(Fs5, 6), "gain", f"{b['R'] - Fs5:+.3e}",
          f"({10 * np.log10(b['R'] / Fs5):+.3f} dB)", "w_b", round(b["w"][1], 4), "bands", b["kmax_a"], b["kmax_b"], flush=True)
json.dump(res, open(os.path.join(HERE, "mode_resolved_scaling.json"), "w"), indent=1, default=float)
