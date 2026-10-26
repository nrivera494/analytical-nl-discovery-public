"""Figure for run 2026-10-08-claude-a-gain-noise-benchmark.

Reads summary.json (this folder) and the per-case .npz files in the raw folder.
Run: ~/agent-work/venv/bin/python runs/2026-10-08-claude-a-gain-noise-benchmark/plot.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-08-claude-a-gain-noise-benchmark")
F0 = 2.99792458e-4 / 1550e-9  # THz

d = json.load(open(os.path.join(HERE, "summary.json")))
cases = d["cases"] + [c for c in d["supplementary"] if "F_ratio" in c]

fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))

# left: per-bin output Wigner variance / prediction vs detuning
for name, col in [("G1_nsp1", "C0"), ("G3_nsp1", "C1"), ("G2_nsp2", "C2")]:
    z = np.load(os.path.join(RAW, name + ".npz"))
    c = next(c for c in cases if c["name"] == name)
    df = z["f_abs_THz_unshifted"] - F0
    o = np.argsort(df)
    ax[0].plot(df[o], z["s_k"][o] / c["s_pred"], ".", ms=2, color=col,
               label=f'{name}: G={c["G"]:.2f}, ns={c["gain_langevin_noise_scale"]:.3f}')
n = 20000
ax[0].axhspan(1 - 1 / np.sqrt(n), 1 + 1 / np.sqrt(n), color="0.85", zorder=0, label=r"$\pm 1/\sqrt{n_{traj}}$")
ax[0].axhline(1, color="k", lw=0.8)
ax[0].set_xlabel("detuning from carrier (THz)")
ax[0].set_ylabel(r"$\langle|\delta B_k|^2\rangle / s_{pred}$")
ax[0].legend(fontsize=6, loc="lower left")
ax[0].set_title("per-bin output variance (photon units)", fontsize=9)

# right: Fano-type ratio per case
x = np.arange(len(cases))
r = np.array([c["F_ratio"] for c in cases])
e = np.array([c["F_ratio_se"] for c in cases])
ax[1].errorbar(x, r, yerr=e, fmt="o", ms=3, capsize=2)
ax[1].axhline(1, color="k", lw=0.8)
ax[1].set_xticks(x)
ax[1].set_xticklabels([c["name"] for c in cases], rotation=75, fontsize=6)
ax[1].set_ylabel(r"$F_{meas}/F_{pred}$")
ax[1].set_title(r"$F=[\mathrm{Var}(N_W)-Ms^2]/(GN_0)$ vs $2s_{pred}$", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "gain_noise.png"), dpi=110)
print("wrote gain_noise.png")
