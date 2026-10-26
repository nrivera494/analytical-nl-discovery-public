"""fig_summary.png for C-20261017-gpt-d-02 (claude-interactive.8): every propagation plane (rho, tau2 Q)
against the arctangent ceiling, plus the optimizer's best positive intensities."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration")
BLUE, ORANGE, AQUA, INK, GRAY = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#8a8984"
TAU2 = {"A": 32e-15, "B": 40e-15}
cases = [("A1", "A", False), ("A2", "A", False), ("A3", "A", False), ("A4", "A", True), ("A5", "A", True),
         ("A6", "A", True), ("B1_widewin", "B", True)]
fig, ax = plt.subplots(figsize=(6.0, 4.3), dpi=100)
q = np.geomspace(0.03, 20, 400)
F = 2 / np.pi * np.arctan(np.pi * q / 2)
ax.loglog(q, F, color=INK, lw=2, label=r"bound $F=\frac{2}{\pi}\arctan(\pi\tau_2Q/2)$")
ax.loglog(q, np.minimum(1, q), color=GRAY, lw=1.5, ls="--", label=r"earlier ceilings $\min(1,\tau_2Q)$")
first = {False: True, True: True}
for name, mat, held in cases:
    d = np.load(os.path.join(RAW, name + ".npz"))
    idx = np.unique(np.linspace(0, len(d["z"]) - 1, 60).astype(int))
    col = BLUE if mat == "A" else AQUA
    lab = None
    if mat == "A" and first[held]:
        lab = "GNLSE planes, SMF-28 " + ("held-out launches" if held else "launches")
        first[held] = False
    if mat == "B":
        lab = "GNLSE planes, fluoride held-out launch"
    ax.plot(TAU2[mat] * d["Q"][idx], d["rho_rhs"][idx], "o", ms=5, mec=col, mew=1.0,
            mfc=("white" if held else col), ls="none", alpha=0.9, label=lab)
st = json.load(open(os.path.join(HERE, "summary_static.json")))
best = st["optimizer_best_by_Q"]
ax.plot([b["tau2Q"] for b in best], [b["rho"] for b in best], "D", ms=8, mfc=ORANGE, mec="white", mew=1.0,
        ls="none", label="optimized positive intensity (fixed $Q$)")
ax.set_xlabel(r"$\tau_2 Q$,  $Q=\int I^2dt/E^2$", fontsize=11)
ax.set_ylabel(r"$\rho=|dE/dz|/(\kappa_U E^2)$", fontsize=11)
ax.set_xlim(0.03, 20); ax.set_ylim(5e-5, 1.6)
ax.grid(True, which="major", color="#e6e5e0", lw=0.8)
ax.tick_params(labelsize=10)
for s in ax.spines.values():
    s.set_color("#bdbcb6")
ax.legend(fontsize=7.8, loc="lower right", frameon=False)
fig.tight_layout()
out = os.path.join(HERE, "fig_summary.png")
fig.savefig(out, dpi=100)
print("saved", out, os.path.getsize(out))
