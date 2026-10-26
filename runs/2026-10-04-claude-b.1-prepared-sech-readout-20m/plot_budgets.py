"""Figure for the LP01 baseline note: Fano-factor budget of the three registered baselines.

Reads only the committed summary.json files of the three claude-b.1 runs (no raw data) and writes budget.png here.
Usage: ~/agent-work/venv/bin/python plot_budgets.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent
c1 = json.loads((RUNS / "2026-10-04-claude-b.1-ideal-sech-kerr-20m" / "summary.json").read_text())
c2 = json.loads((HERE / "summary.json").read_text())
c3 = json.loads((RUNS / "2026-10-04-claude-b.1-bandpass-1546-1553-20m" / "summary.json").read_text())

rows = []  # (label, input vacuum, Raman, added readout vacuum)
g = c1["grids"]["nominal"]
rows.append(("Ideal sech, Kerr only, reference readout\n(case 1, ideal-sech-kerr-20m)",
             g["F_signal"][0], 0.0, g["F_reference_vacuum"][0]))
for kind, name in (("agarwal", "oscillator"), ("anisotropic", "anisotropic")):
    r = c2["results"][f"{kind}_tight"]
    rows.append((f"Prepared sech, reference readout, {name} Raman\n(case 2, prepared-sech-readout-20m)",
                 r["F_signal_input"], r["F_Raman"], r["F_reference_vacuum"]))
for kind, name in (("agarwal", "oscillator"), ("anisotropic", "anisotropic")):
    r = c3["results"].get(f"{kind}_nominal_edge0.5")
    if r is None:
        continue
    N = r["mean_photons_after_filter"]
    rows.append((f"1.23 ps pulse, 1546.5-1553.5 nm band, {name} Raman\n(case 3, bandpass-1546-1553-20m)",
                 r["initial_variance"] / N, r["raman_F_increment"], r["filter_vacuum_variance"] / N))

SURFACE = "#fcfcfb"
TEXT, TEXT2 = "#0b0b0b", "#52514e"
COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]  # categorical slots 1-3, validated (light mode)
NAMES = ["Input vacuum carried through the fiber",
         "Raman reservoir (300 K)",
         "Vacuum added at the readout (reference port, or band-edge partition)"]

groups = [("Coherent-reference readout (all wavelengths)", [r for r in rows if "band" not in r[0]], 0.06),
          ("Direct detection after the 1546.5-1553.5 nm bandpass", [r for r in rows if "band" in r[0]], 0.45)]
fig, axes = plt.subplots(2, 1, figsize=(8.6, 5.2), dpi=150,
                         gridspec_kw={"height_ratios": [len(groups[0][1]), len(groups[1][1]) + 0.6]})
fig.patch.set_facecolor(SURFACE)
for ax, (gtitle, grows, xmax) in zip(axes, groups):
    ax.set_facecolor(SURFACE)
    y = list(range(len(grows)))[::-1]
    for yi, (label, a, b, c) in zip(y, grows):
        left = 0.0
        for val, col in zip((a, b, c), COLORS):
            if val > 0:
                ax.barh(yi, val, left=left, height=0.5, color=col, edgecolor=SURFACE, linewidth=1.5)
            left += val
        ax.text(left + xmax * 0.012, yi, f"F = {left:.4f}", va="center", ha="left", fontsize=8.5, color=TEXT)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in grows], fontsize=7.5, color=TEXT)
    ax.set_xlim(0, xmax)
    ax.set_ylim(-0.6, len(grows) - 0.4)
    ax.tick_params(axis="x", colors=TEXT2, labelsize=8)
    ax.tick_params(axis="y", length=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(TEXT2)
    ax.grid(axis="x", color="#e4e3df", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_title(gtitle, fontsize=9, color=TEXT, loc="left")
axes[-1].set_xlabel("Fano factor F of the counted photon number (shot noise = 1); note the different x ranges",
                    fontsize=8.5, color=TEXT)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COLORS]
fig.legend(handles, NAMES, loc="upper left", bbox_to_anchor=(0.005, 0.955), ncol=2, fontsize=7.5, frameon=False,
           labelcolor=TEXT)
fig.suptitle("Noise budgets of the registered LP01 baselines, 20 m GIF625 at 1550 nm", x=0.01, y=0.99,
             ha="left", fontsize=10, color=TEXT)
fig.tight_layout(rect=(0, 0, 1, 0.89))
fig.savefig(HERE / "budget.png", facecolor=SURFACE)
print("wrote", HERE / "budget.png", [(r[0].split("\n")[0], round(sum(r[1:]), 6)) for r in rows])
