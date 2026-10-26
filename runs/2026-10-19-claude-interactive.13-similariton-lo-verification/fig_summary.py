"""Summary figure for the verification of C-20261019-pi-chatgpt-02 (claude-interactive.13)."""
import json, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-19-claude-interactive.13-similariton-lo-verification")
BLUE, ORANGE, GRAY, INK, INK2 = "#2a78d6", "#eb6834", "#8a8984", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8})
fig, ax = plt.subplots(1, 3, figsize=(12.0, 3.7))
# (a) initial slope vs R
s = json.load(open("slopes_summary.json"))["cases"]
R = np.linspace(0.4, 2.1, 50)
ax[0].plot(R, 1 - R, color=GRAY, lw=1.5, zorder=1, label=r"claim: $1-R$")
for key, col, mk, lab in (("parabola_d0.05_unchirped", BLUE, "o", "smoothed parabola"), ("gaussian_unchirped", ORANGE, "s", "Gaussian")):
    for nsp, fill in ((1, True), (2, False)):
        rows = s[f"{key}_nsp{nsp}"]["rows"]
        x = [r["R"] for r in rows]; y = [r["slope"] / (2 * nsp) for r in rows]
        ax[0].plot(x, y, mk, ms=6.5 if nsp == 1 else 8.5, mfc=col if fill else "none", mec=col, mew=1.4, ls="none", zorder=3 if fill else 2,
                   label=f"{lab}, $n_{{sp}}={nsp}$" + ("" if fill else " (held out)"))
ax[0].axhline(0, color=GRAY, lw=0.6, ls=":"); ax[0].axvline(1, color=GRAY, lw=0.6, ls=":")
ax[0].set_xlabel(r"$R=\gamma\int P^2dt\,/\,(n_{sp}\,g\int P\,dt)$")
ax[0].set_ylabel(r"$\frac{1}{2n_{sp}}\,d\lambda_{\rm LO}/d(gz)\,|_{0^+}$ (full field)")
ax[0].set_title("(ii) initial slope; squeezed iff R > 1", fontsize=9, color=INK, loc="left")
ax[0].legend(fontsize=7, frameon=False, loc="lower left")
# (b) prefactor ratio of (i)
for name, col, ls, lab in (("G18_asym", BLUE, "-", r"$\Gamma=\sqrt{18}$, asymptotic seed"), ("G1_unchirped", ORANGE, "--", r"$\Gamma=1$, unchirped (held out)")):
    d = np.load(os.path.join(RAW, f"reduced_{name}_nsp1_lo.npz"))
    m = d["tau"] <= 40
    ax[1].plot(d["tau"][m], d["ratio_i"][m], color=col, ls=ls, lw=1.6, label=lab)
ax[1].axhline(1, color=GRAY, lw=0.8, ls=":")
ax[1].axvspan(12, 26, color=GRAY, alpha=0.12, lw=0)
ax[1].text(19, 1.12, "fit window 12–26", ha="center", fontsize=7, color=INK2)
ax[1].set_ylim(0.55, 1.15); ax[1].set_xlim(0, 40)
ax[1].set_xlabel(r"log gain $\tau=gz=\ln G$"); ax[1].set_ylabel(r"$C_{PP}\,/\,[(32n_{sp}/9)\,G\,\Phi_{NL}^2]$ (reduced)")
ax[1].set_title(r"(i) $C_{PP}\to(32n_{sp}/9)G\Phi_{NL}^2$, $n_{sp}=1$", fontsize=9, color=INK, loc="left")
ax[1].legend(fontsize=7, frameon=False, loc="lower right")
# (c) G^{-1/3} lambda_min
for name, col, ls, lab in (("G18_asym", BLUE, "-", r"reduced, $\Gamma=\sqrt{18}$ asymptotic"), ("G1_unchirped", ORANGE, "--", r"reduced, $\Gamma=1$ unchirped (held out)")):
    d = np.load(os.path.join(RAW, f"reduced_{name}_nsp1_lo.npz"))
    m = (d["tau"] >= 1.0) & (d["tau"] <= 40)
    ax[2].plot(d["tau"][m], d["lam_lead"][m] * np.exp(-d["tau"][m] / 3), color=col, ls=ls, lw=1.6, label=lab)
c = json.load(open("curve_summary.json"))["curve"]
for eps0, fill in (("0.05", True), ("0.025", False)):
    t = np.array([r["tau"] for r in c[eps0]]); l = np.array([r["lam_min"] for r in c[eps0]])
    ax[2].plot(t, l * np.exp(-t / 3), "o", ms=4.5, mfc=BLUE if fill else "none", mec=BLUE, mew=1.1, ls="none",
               label=rf"full field, $\Gamma=\sqrt{{18}}$, $\varepsilon_0={eps0}$")
ax[2].axvspan(12, 26, color=GRAY, alpha=0.12, lw=0)
ax[2].set_xlim(0, 40); ax[2].set_ylim(0, 1.6)
ax[2].set_xlabel(r"log gain $\tau=\ln G$"); ax[2].set_ylabel(r"$G^{-1/3}\,\lambda_{\min}(C_{\rm LO})$, $n_{sp}=1$")
ax[2].set_title(r"(iii) $\lambda_{\min}=\Theta(G^{1/3})$", fontsize=9, color=INK, loc="left")
ax[2].legend(fontsize=6.5, frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig("fig_summary.png", dpi=110)
print(os.path.getsize("fig_summary.png"))
