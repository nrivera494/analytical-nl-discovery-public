"""Figure for the clamp test: (a) lam = 0 group fractions against RJ; (b) lam-odd centroid offset; (c) lam-even E_0."""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

tag = sys.argv[1] if len(sys.argv) > 1 else "main"
d = json.load(open("results/summary_%s.json" % tag))
z = np.array(d["z_m"]) / 0.1
fig, ax = plt.subplots(1, 3, figsize=(12, 3.3))
fr = np.array(d["lam0_group_fractions_mean"])
cfg = json.load(open("config.json")); cc = dict(cfg["main"]); cc.update(cfg.get(tag, {}))
for g, rj in zip(range(fr.shape[1]), cc["rj_target"]):
    ax[0].plot(z, fr[:, g], label="group %d" % g)
    ax[0].axhline(rj, ls=":", lw=0.8, color="C%d" % g)
ax[0].set_xlabel(r"$z/L_{\rm NL}$"); ax[0].set_ylabel("group fraction ($\\lambda=0$)")
ax[0].set_title("Kerr + disorder relaxation (dotted: RJ)", fontsize=9); ax[0].legend(fontsize=7, frameon=False)
if "Lkin_m" in d and d["Lkin_m"]:
    for a in ax:
        a.axvline(d["Lkin_m"] / 0.1, color="k", lw=0.6, ls="--")
if "dc01_odd_mean" in d:
    m_, s_ = np.array(d["dc01_odd_mean"]), np.array(d["dc01_odd_se"])
    ax[1].errorbar(z, m_, yerr=s_, marker="o", ms=3, capsize=2, label="field")
    ax[1].plot(z, np.array(d["langmuir_dc01_noKerr"]), "k:", label="Langmuir, no Kerr")
    ax[1].set_xlabel(r"$z/L_{\rm NL}$"); ax[1].set_ylabel(r"$\Delta c_{01}$, $\lambda$-odd (rad/ps)")
    ax[1].set_title("inter-group centroid offset", fontsize=9); ax[1].legend(fontsize=7, frameon=False)
if "even_mean" in d:
    e, se = np.array(d["even_mean"])[:, 0], np.array(d["even_se"])[:, 0]
    ax[2].errorbar(z, e, yerr=se, marker="o", ms=3, capsize=2, label="field")
    ax[2].plot(z, np.array(d["langmuir_even_noKerr"])[:, 0], "k:", label="Langmuir, no Kerr")
    ax[2].set_xlabel(r"$z/L_{\rm NL}$"); ax[2].set_ylabel(r"$E_0$ (W)")
    ax[2].set_title("Raman$^2$ change of the fundamental", fontsize=9); ax[2].legend(fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig("fig_clamp_%s.png" % tag, dpi=130)
print("saved")
