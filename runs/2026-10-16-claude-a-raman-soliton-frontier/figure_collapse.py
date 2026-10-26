#!/usr/bin/env python3
"""Collapse figure for C-20261016-claude-a-02: leading-soliton content f1 * sqrt(N) against y = N^2 tau1 / T0 for all N and
the Raman responses tested (four single-oscillator ones and Lin-Agrawal) (Blow-Wood; tau1 = 10 and 16 fs at the same T_R; As2S3-like f_R = 0.10).
Clean rows only (as in h3_analysis.clean), last clean L of each propagation. Usage: python figure_collapse.py -> h3_collapse.png"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

tab = json.load(open("h3_summary.json"))["table"]
pts = {}
for t in tab:
    if t.get("eps") is None:
        continue
    pts.setdefault(("Blow-Wood", t["N"]), []).append((t["N"] ** 2 * 12.2 / t["T0_fs"], t["f1"] * np.sqrt(t["N"])))


def clean(r):
    return abs(r["zeta1_re"]) < 0.05 and not r["window_limited"] and abs(r["photon_drift"]) < 1e-4


for f, name in (("h3_rshape.log", None), ("h3_as2s3.log", "As2S3-like"), ("h3_as2s3fine.log", "As2S3-like"), ("h3_lin.log", "Lin-Agrawal")):
    last = {}
    for l in open(f):
        if l.startswith("{"):
            r = json.loads(l)
            if clean(r):
                last[(r["tau1"], r["N"], r["T0_fs"])] = r
    for (t1, N, T0), r in last.items():
        lab = name or f"tau1={t1:g} fs (same T_R)"
        pts.setdefault((lab, N), []).append((N**2 * t1 / T0, r["f1_output_ZS"] * np.sqrt(N)))
fig, ax = plt.subplots(figsize=(6.4, 4.2))
mk = {"Blow-Wood": "o", "tau1=10 fs (same T_R)": "s", "tau1=16 fs (same T_R)": "^", "As2S3-like": "D", "Lin-Agrawal": "v"}
for (lab, N), v in sorted(pts.items(), key=lambda kv: (kv[0][0], kv[0][1])):
    v = sorted(v)
    x, y = zip(*v)
    ax.semilogx(x, y, marker=mk.get(lab, "o"), ms=3.5, lw=0.8, label=f"{lab}, N={N:g}" if lab != "Blow-Wood" or N in (2, 4, 6, 8) else None)
ax.axvspan(0.78, 1.30, color="0.85", zorder=0)
ax.axhline(1.29, color="k", lw=0.6, ls=":")
ax.set_xlabel(r"$y=N^2\tau_1/T_0$  (compressed-soliton bandwidth / Raman gain-peak frequency)")
ax.set_ylabel(r"$f_1\sqrt{N}$")
ax.set_title("Leading-soliton content after fission, all N and Raman responses", fontsize=9)
ax.legend(fontsize=5.5, ncol=2)
fig.tight_layout(); fig.savefig("h3_collapse.png", dpi=120)
print("points:", sum(len(v) for v in pts.values()))
