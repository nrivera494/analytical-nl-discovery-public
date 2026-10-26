#!/usr/bin/env python3
"""Build the similariton verification figure from supplied data only."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
fv = json.loads((root / "results_fv.json").read_text())
rows = fv["dense"]["rows"]
t = np.array([r["tau"] for r in rows])
vn = np.array([r["density_photon_variance"] for r in rows])
vp = np.array([r["phase_photon_variance_eps2"] for r in rows])
ratio = np.array([r["spectral_ratio"] for r in rows])
deficit = np.array([r["phase_energy_deficit"] for r in rows])
full = json.loads((root / "results_nlse_extended.json").read_text())
case = next(r for r in full["cases"]
            if r["tau"] == 6 and r["ngrid"] == 4096)
tf = np.array([r["tau"] for r in case["samples"]])
nf = np.array([r["n_from_unit_eps_phase"][0] for r in case["samples"]])
nu = np.sqrt(2) / 3
core = -6 / (np.sqrt(18) * nu) * np.exp(-tf / 3) * np.sin(nu * tf)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.titlesize": 12, "axes.labelsize": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "savefig.facecolor": "white",
})
fig, ax = plt.subplots(2, 2, figsize=(11.8, 7.8))
blue = "#185a9d"
orange = "#c25c12"
green = "#167f6d"
purple = "#7b4198"

ax[0, 0].plot(t, vn * np.exp(-t/3), color=blue, lw=2)
ax[0, 0].set_title("(a) Density variance: bounded oscillatory prefactor",
                   loc="left", pad=10)
ax[0, 0].set_ylabel(r"$G^{-1/3}N_{\rm out}\,{\rm Var}(\widehat n_2)$")
ax[0, 0].set_xlim(0, 26)
ax[0, 0].set_ylim(bottom=0)
ax[0, 0].text(.03, .94, r"Predicted variance power: $1/3$",
              transform=ax[0, 0].transAxes, va="top",
              bbox=dict(facecolor="white", edgecolor="none", alpha=.85))

ax[0, 1].plot(t, vp * np.exp(-5*t/3), color=orange, lw=2)
ax[0, 1].set_title("(b) Phase variance: bounded oscillatory prefactor",
                   loc="left", pad=10)
ax[0, 1].set_ylabel(r"$G^{-5/3}\epsilon^2N_{\rm out}\,{\rm Var}(\widehat p_2)$")
ax[0, 1].set_xlim(0, 26)
ax[0, 1].set_ylim(bottom=0)
ax[0, 1].text(.03, .94, r"Predicted variance power: $5/3$",
              transform=ax[0, 1].transAxes, va="top",
              bbox=dict(facecolor="white", edgecolor="none", alpha=.85))

mask = (t >= 4) & np.isfinite(deficit)
ax[1, 0].semilogy(t[mask], ratio[mask], color=green, lw=2,
                  label=r"Spectral $\lambda_2/\lambda_1$")
ax[1, 0].semilogy(t[mask], deficit[mask], color=purple, lw=2,
                  label=r"Phase–energy $1-r^2$")
ax[1, 0].semilogy(t[mask], .04*np.exp(-2*(t[mask]-6)/3),
                  color="#68727d", lw=1.5, ls="--",
                  label=r"Reference $G^{-2/3}$")
ax[1, 0].set_xlim(4, 26)
ax[1, 0].set_ylim(2e-9, 1)
ax[1, 0].set_ylabel("Dimensionless covariance ratio")
ax[1, 0].set_title("(c) Finite core covariance and energy locking",
                   loc="left", pad=10)
ax[1, 0].legend(loc="upper right", frameon=True, framealpha=.94,
                edgecolor="none", fontsize=9)

ax[1, 1].plot(tf, nf, color=blue, lw=2.2, label="Full NLSE, smooth seed")
ax[1, 1].plot(tf, core, color=orange, lw=1.6, ls="--",
              label="Leading parabolic core")
ax[1, 1].axhline(0, color="#a8afb5", lw=.7)
ax[1, 1].set_xlim(0, 6)
ax[1, 1].set_ylabel(r"$n_2$ for $\epsilon p_2(0)=1$")
ax[1, 1].set_title("(d) Independent full-field shape response",
                   loc="left", pad=10)
ax[1, 1].legend(loc="lower right", frameon=True, framealpha=.94,
                edgecolor="none", fontsize=9)
ax[1, 1].text(.04, .95,
              "Full fit: decay 0.333825, frequency 0.470401\n"
              "Core: decay 0.333333, frequency 0.471405",
              transform=ax[1, 1].transAxes, va="top", ha="left",
              fontsize=9,
              bbox=dict(facecolor="white", edgecolor="none", alpha=.90))

for panel in ax.flat:
    panel.set_xlabel(r"Logarithmic power gain $\tau=\ln G$")
    panel.grid(True, which="major", color="#d9dfe5", lw=.6, alpha=.75)
    panel.set_axisbelow(True)

fig.suptitle("Independent amplifier-similariton verification",
             fontsize=16, fontweight="bold", y=.985)
fig.text(.5, .944,
         r"$\Gamma=\sqrt{18}$, $n_{\rm sp}=1$; asymptotic core chirp",
         ha="center", fontsize=11, color="#3c4955")
fig.text(.05, .027,
         "(a–c) Real-space finite volumes, 512 cells and 8 orthonormal modes; "
         "leading density vacuum and ASE.\n"
         "(d) Full NLSE with all second derivatives; "
         r"$\epsilon=0.05$, 4096 points, $\Delta\tau=0.001$; rounded parabolic launch.",
         fontsize=9, color="#3c4955", va="bottom", linespacing=1.7)
fig.subplots_adjust(left=.085, right=.985, bottom=.14, top=.885,
                    hspace=.40, wspace=.28)
for ext in ("pdf", "png"):
    dest = root / ("similariton_verification." + ext)
    fig.savefig(dest, dpi=220)
    print(dest)
