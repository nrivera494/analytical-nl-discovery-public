#!/usr/bin/env python3
"""Figure for run 2026-10-08-claude-a-amp-sim-checks: compressed-pulse timing and shape-noise suppression vs gL."""
import json, math, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.argv = [sys.argv[0], "."]
exec(open("numeric.py").read().split("# ---------------------------------------------------------------- checks")[0])
gls = np.linspace(0.5, 12, 47)
rows = {"main (Gam=sqrt18, unchirped)": (math.sqrt(18), 0.0), "held-out (Gam=1, unchirped)": (1.0, 0.0),
        "asymptotic seed": (math.sqrt(18), math.sqrt(18) / 3)}
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
for lab, (Gm, ad0) in rows.items():
    ct, rat = [], []
    for gl in gls:
        c = collective(Gm, ad0, gl, 1201)
        ct.append(c["comp_timing_in"] + c["comp_timing_ase"])         # n_sp = 1
        Sin, Sase = block_noise(c, Gm)
        aL, adL = c["a_L"], c["ad"][-1]
        Cs = np.zeros((LMAX + 1, LMAX + 1))
        for l in range(LMAX + 1):
            vl = np.array([-l * (l + 1) / (aL * adL), 1.0])
            for m in range(LMAX + 1):
                vm = np.array([-m * (m + 1) / (aL * adL), 1.0])
                Cs[l, m] = vl @ (Sin[l, m] + Sase[l, m]) @ vm
        Gh = np.diag(np.sqrt(2 / (2 * np.arange(LMAX + 1) + 1)))
        ev = np.sort(np.linalg.eigvalsh(Gh @ Cs @ Gh))[::-1]
        rat.append(ev[1] / ev[0])
    ax[0].plot(gls, ct, label=lab)
    ax[1].semilogy(gls, rat, label=lab)
ax[0].plot(gls, 0.2 * (1 + (1 - np.exp(-gls))), "k--", label="linear amplifier (same seed)")
ax[0].set_xlabel("gL"); ax[0].set_ylabel(r"$N_0\,\mathrm{Var}(T_{comp})/T_0^2$  ($n_{sp}=1$)")
ax[1].semilogy(gls, 3 * np.exp(-2 * gls / 3), "k:", label=r"$\propto G^{-2/3}$")
ax[1].set_xlabel("gL"); ax[1].set_ylabel(r"spectral covariance $\lambda_2/\lambda_1$ ($l\leq4$, $n_{sp}=1$)")
for a_ in ax: a_.legend(fontsize=7)
fig.tight_layout(); fig.savefig("amp_sim_noise.png", dpi=120)
print("saved")
