"""Figure 1 of R-0006, redrawn from committed numbers only (no simulation).

Source: runs/2026-10-17-gpt-a-phase-headroom/verification.json (gpt-a, family gpt), key "pairs".
Each pair compares a masked launch with the transform-limited (TL) launch of the same laser
spectrum and energy. H_zs uses the ZS soliton energy of the leading pulse; H_gate uses its
time-gated energy, which gpt-a takes as the primary observable once shock, TOD, loss or a
frequency-dependent dispersion is on.

Run from the repository root:
    ~/agent-work/venv/bin/python results/promising/R-0006-phase-mask-headroom-leading-raman-soliton/repro/make_fig1.py
Writes figures/fig1-witness-headroom.png next to this folder and prints the plotted values.
Author: claude-interactive.15 (claude-opus-5-5, family claude), 2026-10-19.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RUN = ROOT / "runs" / "2026-10-17-gpt-a-phase-headroom"
OUT = HERE.parent / "figures" / "fig1-witness-headroom.png"

pairs = json.loads((RUN / "verification.json").read_text())["pairs"]

# (row label, A2 pair, B pair, readout key)
ROWS = [
    ("Core model (the result)", "core_100_A2", "core_200_B", "H_zs"),
    ("Duration −10%, fixed energy and length", "detuneE_90_A2", "detuneE_180_B", "H_zs"),
    ("Duration +10%, fixed energy and length", "detuneE_110_A2", "detuneE_220_B", "H_zs"),
    ("+ self-steepening", "shock_100_A2", "shock_200_B", "H_gate"),
    ("+ third-order dispersion", "tod_100_A2", "tod_200_B", "H_gate"),
    ("+ loss 0.2 dB/km", "loss_100_A2", "loss_200_B", "H_gate"),
    ("Published SMF-28 dispersion + shock + loss", "published_100_A2", "published_200_B", "H_gate"),
]
# Numerical variants of the core model (step, grid, window, length, smooth mask cutoff)
VARIANTS = ["step0.5", "step0.25", "step2.0", "grid", "window", "length6", "length8", "cutoff_smooth"]

INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
BLUE, ORANGE = "#2a78d6", "#eb6834"  # categorical slots 1-2, validated (light): CVD dE 24.7

print(f"{'row':45s} {'A2':>10s} {'B':>10s}  readout")
for label, a, b, key in ROWS:
    print(f"{label:45s} {pairs[a][key]:10.6f} {pairs[b][key]:10.6f}  {key}")
for mask, T in [("A2", 100), ("B", 200)]:
    vals = [pairs[f"{v}_{T}_{mask}"]["H_zs"] for v in VARIANTS]
    core = pairs[f"core_{T}_{mask}"]["H_zs"]
    print(f"numerical variants {mask}: min {min(vals):.6f} max {max(vals):.6f} "
          f"(core {core:.6f}; largest deviation {max(abs(v - core) for v in vals):.2e})")

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK})
fig, ax = plt.subplots(figsize=(8.2, 3.9), dpi=160, constrained_layout=True)
ys = list(range(len(ROWS)))[::-1]
for y, (label, a, b, key) in zip(ys, ROWS):
    ha, hb = pairs[a][key], pairs[b][key]
    ax.plot([min(ha, hb), max(ha, hb)], [y, y], color=GRID, lw=2, zorder=1, solid_capstyle="round")
    ax.plot(ha, y, "o", ms=8, color=BLUE, mec="white", mew=1.5, zorder=3,
            label="Mask A2, $T_0=100$ fs" if y == ys[0] else None)
    ax.plot(hb, y, "s", ms=7.5, color=ORANGE, mec="white", mew=1.5, zorder=3,
            label="Mask B, $T_0=200$ fs" if y == ys[0] else None)
    if y == ys[0]:  # direct labels on the result row only
        ax.annotate(f"{ha:.4f}", (ha, y), xytext=(0, 9), textcoords="offset points",
                    ha="center", va="bottom", color=INK, fontsize=9)
        ax.annotate(f"{hb:.4f}", (hb, y), xytext=(0, 9), textcoords="offset points",
                    ha="center", va="bottom", color=INK, fontsize=9)
ax.axvline(1.0, color=INK2, lw=1, zorder=0)
ax.text(1.0015, ys[-1] - 0.55, "no gain (TL launch)", color=INK2, fontsize=8.5, va="center")
ax.set_yticks(ys)
ax.set_yticklabels([f"{r[0]}  [{'ZS' if r[3] == 'H_zs' else 'gated'}]" for r in ROWS])
ax.set_ylim(ys[-1] - 0.9, ys[0] + 0.8)
ax.set_xlim(0.995, 1.105)
ax.grid(axis="x", color=GRID, lw=0.6)
ax.set_axisbelow(True)
ax.set_xlabel(r"Headroom $H=f_1(\mathrm{mask})/f_1(\mathrm{TL})$ at $N=4$", color=INK)
ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=2, frameon=False, fontsize=9,
          handletextpad=0.4, columnspacing=1.4)
fig.savefig(OUT, facecolor="white", metadata={"Author": "claude-interactive.15; claude-opus-5-5; claude",
                                              "Source": "runs/2026-10-17-gpt-a-phase-headroom/verification.json"})
print("wrote", OUT.relative_to(ROOT))
