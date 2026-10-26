"""Figures for run 2026-10-04-claude-b.4-pmin-length-map (reads summary.json written by summarize_map.py).

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-length-map/plot_map.py [L ...]
  power_noise_L<L>m.png : scope-doc convention (output power in the band, blue, left axis; noise in dB, red, right
                          axis) against coupled input power at one length, with the bright term alone dashed. The
                          dual axis follows the repository's plotting convention (docs/multimode-squeezing-scope.md).
  pmin_vs_length.png    : P_min(L) of each dip and P_G0(L) on log-log axes with reference slopes; local exponents;
                          F_min of each dip with the parts of the first dip.
"""
import json
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "summary.json")))
conv = sys.argv[1:] or ["1", "5"]
BLUE, RED, AMBER, PURPLE, GRAY = "#1f5fbf", "#c62828", "#b26a00", "#6a3d9a", "#6b6b6b"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False})

# ---- convention figures ------------------------------------------------------------------------------
for Lc in conv:
    r = S["lengths"][Lc]
    pg = r["plateau"].get("P_G0_mw")
    top = 1.15 * pg if pg else max(p["P_mw"] for p in r["points"])
    pts = [p for p in r["points"] if p["P_mw"] <= top]
    P = np.array([p["P_mw"] for p in pts])
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.plot(P, [p["P_out_selected_mw"] for p in pts], "o-", color=BLUE, ms=2.5, lw=1.5)
    ax.set_xlabel("coupled input power (mW)")
    ax.set_ylabel("output power in 1226-1269 nm band (mW)", color=BLUE)
    ax.tick_params(axis="y", colors=BLUE)
    ax.spines["left"].set_color(BLUE)
    ax2 = ax.twinx()
    ax2.plot(P, [10 * math.log10(p["F"]) for p in pts], "s-", color=RED, ms=2.5, lw=1.5, label="noise, full model")
    ax2.plot(P, [10 * math.log10(p["F_bright"]) if p["F_bright"] > 1e-3 else np.nan for p in pts], "--", color=RED,
             lw=1, label="bright term $T_NG^2$ alone")
    ax2.axhline(0, color=GRAY, lw=0.6)
    ax2.set_ylim(-6, 3)
    ax2.set_ylabel("noise relative to shot noise (dB)", color=RED)
    ax2.tick_params(axis="y", colors=RED)
    ax2.spines["right"].set_color(RED)
    for q in r.get("dips", []):
        ax2.axvline(q["P_min_mw"], color=GRAY, ls=":", lw=1)
        ax2.annotate(f"dip {q['P_min_mw']:.0f} mW\nF={q['F_min']:.3f}", (q["P_min_mw"], -5.9), xytext=(3, 2),
                     textcoords="offset points", fontsize=7, color=GRAY)
    if pg:
        ax2.axvline(pg, color=AMBER, ls="-.", lw=1)
        ax2.annotate(f"$P_{{G0}}$={pg:.0f} mW", (pg, 2.6), xytext=(-62, 0), textcoords="offset points", fontsize=7,
                     color=AMBER)
    ax2.legend(loc="upper left", fontsize=7, frameon=False)
    ax.set_title(f"1250 nm LP01, {float(Lc):g} m GIF625, oscillator Raman; run {S['run_id']}", fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"power_noise_L{Lc}m.png"), dpi=150)
    plt.close(fig)

# ---- P_min(L) figure ------------------------------------------------------------------------------------
L1, P1, F1, B1, S1, R1 = [], [], [], [], [], []
L2, P2, F2 = [], [], []
Lg, Pg = [], []
nodip = []
for k, r in S["lengths"].items():
    L = r["length_m"]
    if "first" in r:
        q = r["first"]
        L1.append(L); P1.append(q["P_min_mw"]); F1.append(q["F_min"])
        B1.append(q["decomposition"]["F_bright"]); S1.append(q["decomposition"]["F_shape"])
        R1.append(q["decomposition"]["F_Raman"])
        for q2 in r["dips"][1:]:
            L2.append(L); P2.append(q2["P_min_mw"]); F2.append(q2["F_min"])
    else:
        nodip.append(L)
    if r["plateau"].get("P_G0_mw"):
        Lg.append(L); Pg.append(r["plateau"]["P_G0_mw"])


def srt(*a):
    o = np.argsort(a[0])
    return [np.array(v)[o] for v in a]


L1, P1, F1, B1, S1, R1 = srt(L1, P1, F1, B1, S1, R1)
Lg, Pg = srt(Lg, Pg)
fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
ax = axs[0]
ax.loglog(L1, P1, "o-", color=BLUE, ms=4, lw=1.5, label="first dip $P_{\\min}$")
if L2:
    ax.loglog(L2, P2, "D", color=PURPLE, ms=5, mfc="none", mew=1.5, label="further dip below $P_{G0}$")
ax.loglog(Lg, Pg, "s-", color=AMBER, ms=4, lw=1.5, label="$P_{G0}$ (G = 0)")
if 1.0 in list(L1):
    p1 = P1[list(L1).index(1.0)]
    xx = np.array([0.2, 6.0])
    for a, ls in ((1, "--"), (2, ":"), (0, "-.")):
        ax.loglog(xx, p1 * xx ** (-a), ls, color=GRAY, lw=0.8)
        ax.annotate(f"$L^{{-{a}}}$" if a else "$L^0$", (xx[-1], p1 * xx[-1] ** (-a)), fontsize=7, color=GRAY,
                    xytext=(2, 0), textcoords="offset points")
for L in nodip:
    ax.axvline(L, color=RED, lw=0.8, ls=":")
    ax.annotate("no dip deeper\nthan 0.003", (L, 15), fontsize=7, color=RED, xytext=(3, 0), textcoords="offset points")
ax.set_xlabel("fiber length L (m)")
ax.set_ylabel("coupled input power (mW)")
ax.set_ylim(10, 3000)
ax.legend(fontsize=7, frameon=False, loc="upper right")
ax = axs[1]
for key, col, mk, lab in (("alpha_first_dip", BLUE, "o-", "first dip"), ("alpha_P_G0", AMBER, "s-", "$P_{G0}$")):
    al = S[key]
    ax.semilogx([a["L_geometric_mean_m"] for a in al], [a["alpha"] for a in al], mk, color=col, ms=4, lw=1.5, label=lab)
for y in (0, 1, 2):
    ax.axhline(y, color=GRAY, lw=0.6, ls="--")
ax.set_xlabel("L (m), geometric mean of neighbouring lengths")
ax.set_ylabel("local exponent $-d\\ln P/d\\ln L$")
ax.legend(fontsize=7, frameon=False)
ax = axs[2]
ax.semilogx(L1, F1, "o-", color=RED, ms=4, lw=1.5, label="$F_{\\min}$, first dip")
if L2:
    ax.semilogx(L2, F2, "D", color=PURPLE, ms=5, mfc="none", mew=1.5, label="$F_{\\min}$, further dip")
ax.semilogx(L1, B1, "--", color=RED, lw=1, label="bright part, first dip")
ax.semilogx(L1, S1, ":", color=GRAY, lw=1.2, label="shape part, first dip")
ax.semilogx(L1, 10 * R1, "-.", color=AMBER, lw=1, label="Raman part x10, first dip")
ax.axhline(1, color=GRAY, lw=0.6)
ax.set_xlabel("fiber length L (m)")
ax.set_ylabel("Fano factor and its parts")
ax.legend(fontsize=7, frameon=False)
fig.suptitle(f"1250 nm LP01 GIF625, band 1226-1269 nm, input GDD -0.015 ps$^2$, oscillator Raman; run {S['run_id']}",
             fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "pmin_vs_length.png"), dpi=150)
print("figures written")
