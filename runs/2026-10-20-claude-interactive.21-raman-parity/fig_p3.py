"""Figure for P3: lam-even and lam-odd parts of the fundamental's photon number against z."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

d = json.load(open("summary.json"))
z = np.array(d["z_m"]) / 0.1          # in units of L_NL = 0.1 m
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
for key, lab, ls in (("s0_lam1", r"$\lambda=1$", "-"), ("s0_lam0.5", r"$\lambda=0.5$ (x4)", "--")):
    e = np.array(d["P3"][key]["even_pair_mean"])[:, 0]
    se = np.array(d["P3"][key]["even_pair_se"])[:, 0]
    f = 4 if "0.5" in key else 1
    ax[0].errorbar(z, f * e, yerr=f * se, ls=ls, marker="o", ms=3, capsize=2, label="field, " + lab)
lang = np.array(d["langmuir_exactkernel_s0_even_W"])[:, 0]
ax[0].plot(z, lang, "k:", label="Langmuir, no Kerr (post hoc)")
ax[0].set_xlabel(r"$z/L_{\rm NL}$")
ax[0].set_ylabel(r"even part $E_0$ of $\tilde N_0$ (W)")
ax[0].set_title("Raman$^2$: fundamental gains (s = 0)", fontsize=9)
ax[0].legend(fontsize=7, frameon=False)
for key, lab in (("s1_lam1", "s = 1"), ("s0.5_lam1", "s = 0.5 (x2)")):
    o = np.array(d["P3"][key]["odd_pair_mean"])[:, 0]
    se = np.array(d["P3"][key]["odd_pair_se"])[:, 0]
    f = 2 if "0.5" in key else 1
    ax[1].errorbar(z, f * o, yerr=f * se, marker="o", ms=3, capsize=2, label=lab)
o0 = np.array(d["P3"]["s0_lam1"]["odd_pair_mean"])[:, 0]
ax[1].plot(z, o0, "k-", lw=0.8, label="s = 0 (zero to 1e-16)")
ax[1].set_xlabel(r"$z/L_{\rm NL}$")
ax[1].set_ylabel(r"$\lambda$-odd part $O_0$ (W)")
ax[1].set_title("shock x Raman cross term", fontsize=9)
ax[1].legend(fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig("fig_p3.png", dpi=130)
print("saved")
