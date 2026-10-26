"""Figure and post-hoc numbers for C-20261017-gpt-d-01 (claude-interactive.8).

fig_summary.png: GNLSE launch-plane rho (nonlinear RHS) for sech launches vs the closed form.
Also: sech-tracking of propagated N=1 solitons (A1, A2 raw data of run ...-concentration):
rho(z) vs rho_closed(T_eff(z)), T_eff = 1/(3 Q(z)) (exact for a sech intensity).
"""
import json, os
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ramanlib import rho_closed

HERE = os.path.dirname(os.path.abspath(__file__))
snap = json.load(open(os.path.join(HERE, "summary_snapshots.json")))
BLUE, ORANGE, INK, GRAY = "#2a78d6", "#eb6834", "#0b0b0b", "#8a8984"

# ---------------------------------------------------------------- sech tracking (post-hoc)
RAW2 = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration")
track = {}
for case, tau1, tau2 in [("A1", 12.2e-15, 32e-15), ("A2", 12.2e-15, 32e-15)]:
    d = np.load(os.path.join(RAW2, case + ".npz"))
    idx = np.unique(np.linspace(0, len(d["z"]) - 1, 81).astype(int))
    rat = []
    for i in idx:
        Teff = 1 / (3 * d["Q"][i])
        rat.append(d["rho_rhs"][i] / float(rho_closed(tau1 / tau2, Teff / tau1)))
    rat = np.array(rat)
    track[case] = {"planes": int(len(idx)), "ratio_launch": float(rat[0]), "ratio_min": float(rat.min()),
                   "ratio_max": float(rat.max()), "ratio_end": float(rat[-1]),
                   "Teff_launch_fs": float(1 / (3 * d["Q"][0]) / 1e-15),
                   "Teff_end_fs": float(1 / (3 * d["Q"][-1]) / 1e-15)}
json.dump(track, open(os.path.join(HERE, "summary_tracking.json"), "w"), indent=1)
print(track)

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(figsize=(6.0, 4.3), dpi=100)
x = np.geomspace(0.15, 30, 300)
for r, col, lab in [(12.2 / 32, BLUE, r"SMF-28 surrogate, $r=0.381$"), (9.1 / 40, ORANGE, r"fluoride surrogate, $r=0.228$")]:
    ax.loglog(x, [float(rho_closed(r, xx)) for xx in x], color=col, lw=2, label=f"closed form, {lab}")
r = 12.2 / 32
xl = np.geomspace(3, 30, 50)
ax.loglog(xl, 16 * r / (15 * (1 + r * r) ** 2) * xl ** -3.0, ls="--", color=GRAY, lw=1.5,
          label=r"$\frac{16r}{15(1+r^2)^2}x^{-3}$ and $1-2rx$ ($r=0.381$)")
xs = np.geomspace(0.15, 0.6, 30)
ax.loglog(xs, 1 - 2 * r * xs, ls="--", color=GRAY, lw=1.5)
for mat, col in [("A", BLUE), ("B", ORANGE)]:
    for held in [False, True]:
        pts = [s for s in snap["snapshots"] if s["material"] == mat and s["kernel"] == "analytic" and s["held_out"] == held]
        if not pts:
            continue
        ax.plot([s["x"] for s in pts], [s["rho_rhs"] for s in pts], "o", ms=8, mec=col, mew=1.6,
                mfc=("white" if held else col), ls="none",
                label=("GNLSE launch plane, held out" if held else "GNLSE launch plane") + (" (SMF-28)" if mat == "A" else " (fluoride)"))
ax.set_xlabel(r"$x=T/\tau_1$  (sech width over inverse Raman frequency)", fontsize=11)
ax.set_ylabel(r"$\rho=|dE/dz|/(\kappa_U E^2)$", fontsize=11)
ax.set_ylim(1e-5, 1.5)
ax.grid(True, which="major", color="#e6e5e0", lw=0.8)
ax.tick_params(labelsize=10)
for s in ax.spines.values():
    s.set_color("#bdbcb6")
ax.legend(fontsize=7.6, loc="lower left", frameon=False)
fig.tight_layout()
out = os.path.join(HERE, "fig_summary.png")
fig.savefig(out, dpi=100)
print("saved", out, os.path.getsize(out), "bytes")
