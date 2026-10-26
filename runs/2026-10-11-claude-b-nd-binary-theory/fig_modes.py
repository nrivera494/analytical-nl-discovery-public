"""Figure: mean spectrum and the optimal even and odd weights at N40 z/z_wb = 0.7 and 1.0 (claude-b,
T-20261010-claude-interactive-05, continuation). Writes fig_modes.png."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mode_anatomy import sectors
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-heldout")
fig, axs = plt.subplots(3, 2, figsize=(11, 7), sharex="col")
for col, tag in enumerate(("N40_zr0.7", "N40_zr1")):
    d = np.load(os.path.join(RAW, tag + ".npz"))
    kk = np.rint(d["w"][d["keep"]] / (2 * np.pi / 40)).astype(int)
    C, nb, kk, A, (le, Ve), (lo, Vo) = sectors(d["C"], d["nbar"], kk)
    order = np.argsort(kk); kk, nb = kk[order], nb[order]; Ve, Vo = Ve[order], Vo[order]
    v = kk * (2 * np.pi / 40) / 40
    axs[0, col].semilogy(v, nb / nb.max(), "k-", lw=0.7); axs[0, col].set_ylim(1e-6, 2); axs[0, col].set_title(tag + ": mean spectrum")
    we = Ve[:, 0] / np.sqrt(nb); wo = Vo[:, 0] / np.sqrt(nb)
    axs[1, col].plot(v, Ve[:, 0], "g-", lw=0.7); axs[1, col].set_title(f"even mode y = w sqrt(nbar), lambda_even = {le[0]:.3f}")
    axs[2, col].plot(v, Vo[:, 0], "b-", lw=0.7); axs[2, col].set_title(f"odd mode, lambda_odd = {lo[0]:.4f}")
    axs[2, col].set_xlabel("v = omega / N")
    for r in range(3):
        axs[r, col].set_xlim(-1.0, 1.0)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_modes.png"), dpi=100)
print("ok")
