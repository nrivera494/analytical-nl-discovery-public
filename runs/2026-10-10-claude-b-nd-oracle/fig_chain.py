"""Summary figure of the bound chain against N at fixed z/z_wb (claude-b, T-20261010-claude-interactive-05):
formula Lambda/N^2, lambda_min, lambda_pass, lambda_gen, centroid readout, parity bound (C-20261010-claude-a-03),
best binary filter found; z/z_wb = 0.7 and 1.0, resolved points only. Writes fig_chain.png."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
S = [p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"] if p["s"] == 0 and p["resolved"]]
PB = json.load(open(os.path.join(HERE, "parity_bound.json")))
fig, axs = plt.subplots(1, 2, figsize=(11, 4.3), sharey=True)
for ax, zr in zip(axs, (0.7, 1.0)):
    P = sorted([p for p in S if p["zr"] == zr], key=lambda p: p["N"])
    N = np.array([p["N"] for p in P])
    get = lambda k: np.array([p[k] for p in P])
    ax.plot(N, get("formula"), "k-", label=r"$\Lambda(Z)/N^2$ (C-01)")
    ax.plot(N, get("lam_min"), "ko", ms=4, label=r"$\lambda_{\min}(V)$")
    ax.plot(N, get("lam_pass"), "bs", ms=4, label=r"$\lambda_{\rm pass}=\lambda_2$")
    ax.plot(N, get("lam_gen"), "r^", ms=5, label=r"$\lambda_{\rm gen}$")
    ax.plot(N, get("F_centroid"), "r--", label=r"centroid $\langle\Delta\omega^2\rangle_{\rm in}/\langle\Delta\omega^2\rangle_{\rm out}$ (C-02)")
    ax.plot(N, [PB[p["tag"]]["F_par"] for p in P], "g-d", ms=5, label="parity bound (C-20261010-claude-a-03)")
    ax.plot(N, get("F_bin"), "mo-", ms=5, label="best binary found")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("N"); ax.set_title(f"z/z_wb = {zr}")
    ax.grid(True, which="both", alpha=0.3)
axs[0].set_ylabel("Fano factor / variance (shot noise = 1)")
axs[0].legend(fontsize=7, loc="lower left")
fig.suptitle("Gaussian in normal dispersion, Kerr only: bound chain vs N (runs 2026-10-10-claude-b-nd-oracle, -heldout)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_chain.png"), dpi=110)
print("ok")
