#!/usr/bin/env python3
"""Figures for the manuscript "Quantum noise of the amplifier similariton".

agent: claude-interactive.20; model: claude-opus-5-5; family: claude.

Reads only numbers already committed in run folders under runs/; it runs no
simulation. Every plotted value comes from one of these runs:

  Fig. 1  runs/2026-10-19-gpt-e-similariton (reduced-main.json)
          runs/2026-10-18-pi-chatgpt-independent-verification
              (archive/similariton/analysis_summary.json)
          runs/2026-10-11-gpt-a-highlights-audit-c2 (closed.json)
  Fig. 2  runs/2026-10-19-claude-interactive.13-similariton-lo-verification
              (slopes_summary.json, curve_summary.json)
          runs/2026-10-19-gpt-e-similariton (fullfield-short.json, fullfield-main.json)
          runs/2026-10-18-pi-chatgpt-independent-verification (summary.json)
  Fig. 3  runs/2026-10-19-claude-interactive.13-similariton-lo-verification
              (reduced_summary.json, source_seed_summary.json)
          runs/2026-10-19-gpt-e-similariton (reduced-main.json, fullfield-main.json)

Derived values (ratios, compensated variances, the matched-mode minimum from
C_AA, C_PP and 1-r^2) are computed here from the committed numbers and written,
with every plotted number, to figures/figure_data.json.
Usage: python make_figures.py   (from any directory)
"""
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNS = ROOT / "runs"
OUT = HERE / "figures"

R_E = "2026-10-19-gpt-e-similariton"
R_P = "2026-10-18-pi-chatgpt-independent-verification"
R_A = "2026-10-11-gpt-a-highlights-audit-c2"
R_V = "2026-10-19-claude-interactive.13-similariton-lo-verification"

# Colour roles as in docs/manuscripts/2026-10-18-thermalization-statistics (categorical slots 1-3
# validated for colour-vision deficiency; every colour is doubled by a marker shape).
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
SHADE = "#eeeeec"
W1 = 3.375  # revtex single-column width, inches
SQ18 = np.sqrt(18.0)

plt.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 6.3, "legend.frameon": False, "legend.handlelength": 1.4,
    "legend.borderaxespad": 0.3, "legend.labelspacing": 0.25,
    "axes.linewidth": 0.6, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK,
    "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.minor.width": 0.4,
    "ytick.minor.width": 0.4, "xtick.major.size": 3, "ytick.major.size": 3,
    "xtick.minor.size": 1.6, "ytick.minor.size": 1.6,
    "lines.linewidth": 1.0, "lines.markersize": 3.6, "errorbar.capsize": 1.4,
    "savefig.dpi": 300, "pdf.fonttype": 42,
})

DATA = {}


def load(run, name):
    return json.loads((RUNS / run / name).read_text())


def panel_label(ax, s, x=0.03, y=0.97):
    ax.text(x, y, s, transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
            fontweight="bold", color=INK)


def save(fig, stem):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{stem}.pdf", metadata={"Author": "claude-interactive.20 (claude-opus-5-5)",
                                               "CreationDate": None})
    fig.savefig(OUT / f"{stem}.png", dpi=200)
    plt.close(fig)


def gpte_case(Gamma, nsp, launch):
    for e in load(R_E, "reduced-main.json"):
        if abs(e["Gamma"] - Gamma) < 1e-6 and e["nsp"] == nsp and e["launch"] == launch:
            return e
    raise KeyError((Gamma, nsp, launch))


def lo_minimum(CAA, CPP, deficit):
    """Smaller eigenvalue of [[CAA, CAP], [CAP, CPP]] from det = CAA CPP (1 - r^2), without cancellation."""
    det = CAA * CPP * deficit
    tr = CAA + CPP
    return det / (0.5 * (tr + np.sqrt(tr * tr - 4 * det)))


# ---------------------------------------------------------------- Figure 1
def fig_shape():
    e = gpte_case(SQ18, 1.0, "asymptotic")
    eps = e["epsilon"]
    rows = e["rows"]
    tau = np.array([r["tau"] for r in rows])
    nI = np.array([r["photon_intensity_variances"] for r in rows])          # N_out Var n_l, l = 2, 3, 4
    nP = np.array([r["photon_phase_variances"] for r in rows]) * eps ** 2  # eps0^2 N_out Var p_l
    spec = np.array([r["spectral_ratio"] for r in rows])
    defi = np.array([r["phase_energy_deficit"] for r in rows])
    per = load(R_P, "archive/similariton/analysis_summary.json")["period_matched_l2"]["rows"]
    gpta = [s for s in load(R_A, "closed.json")["shape"]]
    DATA["fig1_gpte_reduced"] = dict(run=R_E, Gamma=e["Gamma"], nsp=e["nsp"], launch=e["launch"],
                                     epsilon=eps, tau=tau.tolist(), NVar_n_l234=nI.tolist(),
                                     eps2NVar_p_l234=nP.tolist(), spectral_ratio=spec.tolist(),
                                     one_minus_r2=defi.tolist(),
                                     late_normalized_min=e["late_normalized_min"],
                                     late_normalized_max=e["late_normalized_max"])
    DATA["fig1_gpt6pro_period_rows"] = dict(run=R_P, rows=[
        {k: p[k] for k in ("tau", "density_photon_variance", "phase_photon_variance_eps2",
                           "spectral_ratio", "phase_energy_deficit")} for p in per])
    DATA["fig1_gpta_reduced"] = dict(run=R_A, rows=[
        dict(gL=s["gL"], eigenvalue_ratio=s["eigenvalue_ratio"], phase_residual=s["phase_residual"])
        for s in gpta])

    fig, (a, b) = plt.subplots(1, 2, figsize=(W1, 1.62), layout="constrained")
    # (a) photon-normalized shape variances against ln G
    tt = np.linspace(0, 32, 50)
    i12 = int(np.argmin(abs(tau - 12)))
    for l, mk in zip((2, 3, 4), ("o", "s", "^")):
        k = l - 2
        a.plot(tau, nI[:, k], mk, color=BLUE, ms=2.9, mew=0.6, mfc=BLUE if l == 2 else "white", zorder=3)
        a.plot(tau, nP[:, k], mk, color=ORANGE, ms=2.9, mew=0.6, mfc=ORANGE if l == 2 else "white", zorder=3)
    for q, ref in ((1 / 3, nI[i12, 0]), (5 / 3, nP[i12, 0])):
        a.plot(tt, ref * np.exp(q * (tt - 12)), color=INK, ls="--", lw=0.8, zorder=1)
    a.plot(tt, nI[0, 0] * np.exp(tt - tau[0]), color=INK2, ls=":", lw=0.8, zorder=1)
    a.text(27.5, 5e6, r"$\propto G$", color=INK2, fontsize=6.5, ha="right")
    a.text(24, 3e5, r"$G^{1/3}$", color=INK, fontsize=6.5, ha="right")
    a.text(22.0, 5e18, r"$G^{5/3}$", color=INK, fontsize=6.5, ha="right")
    a.plot([p["tau"] for p in per], [p["density_photon_variance"] for p in per], "D", mfc="none",
           mec=INK, ms=3.6, mew=0.7, zorder=4)
    a.plot([p["tau"] for p in per], [p["phase_photon_variance_eps2"] for p in per], "D", mfc="none",
           mec=INK, ms=3.6, mew=0.7, zorder=4)
    h1, = a.plot([], [], "o", color=BLUE, ms=2.9, label=r"$N_{\rm out}{\rm Var}\,n_\ell$")
    h2, = a.plot([], [], "o", color=ORANGE, ms=2.9, label=r"$\varepsilon_0^2N_{\rm out}{\rm Var}\,p_\ell$")
    h3, = a.plot([], [], "D", mfc="none", mec=INK, ms=3.4, mew=0.7, label=r"GPT 6 Pro, $\ell=2$")
    a.legend(handles=[h2, h1, h3], loc="upper left", bbox_to_anchor=(0.0, 0.9), fontsize=5.4,
             handletextpad=0.3, borderaxespad=0.2)
    a.text(0.97, 0.05, r"filled: $\ell=2$; open: $\ell=3,4$", transform=a.transAxes, ha="right",
           va="bottom", fontsize=5.6, color=INK2)
    a.set(yscale="log", xlim=(0, 32), ylim=(3e-2, 1e24), xlabel=r"$\tau=\ln G$",
          yticks=[1e0, 1e6, 1e12, 1e18, 1e24], xticks=[0, 10, 20, 30])
    a.set_ylabel("photon-normalized variance", labelpad=1)
    panel_label(a, "(a)")

    # (b) five-component spectral ratio and phase-energy deficit
    a_, = b.plot(tau, spec, "o-", color=BLUE, ms=2.9, lw=0.7, mew=0.6, zorder=3, label=r"$\mu_2/\mu_1$")
    b_, = b.plot(tau, defi, "s-", color=ORANGE, ms=2.9, lw=0.7, mew=0.6, zorder=3, label=r"$1-r^2$")
    for ref, col in ((spec[i12], BLUE), (defi[i12], ORANGE)):
        b.plot(tt, ref * np.exp(-2 / 3 * (tt - 12)), color=INK, ls="--", lw=0.8, zorder=1)
    b.text(29, 3e-6, r"$G^{-2/3}$", color=INK, fontsize=6.5, ha="right")
    c_, = b.plot([p["tau"] for p in per], [p["spectral_ratio"] for p in per], "D", mfc="none", mec=INK,
                 ms=3.6, mew=0.7, zorder=4, label="GPT 6 Pro")
    b.plot([p["tau"] for p in per], [p["phase_energy_deficit"] for p in per], "D", mfc="none", mec=INK,
           ms=3.6, mew=0.7, zorder=4)
    d_, = b.plot([s["gL"] for s in gpta], [s["eigenvalue_ratio"] for s in gpta], "v", mfc="none", mec=AQUA,
                 ms=3.6, mew=0.7, zorder=4, label="gpt-a")
    b.plot([s["gL"] for s in gpta], [s["phase_residual"] for s in gpta], "v", mfc="none", mec=AQUA,
           ms=3.6, mew=0.7, zorder=4)
    b.legend(handles=[a_, b_, c_, d_], loc="lower left", fontsize=5.4, handletextpad=0.3,
             borderaxespad=0.2)
    b.set(yscale="log", xlim=(0, 32), ylim=(1e-11, 3), xlabel=r"$\tau=\ln G$", xticks=[0, 10, 20, 30],
          yticks=[1e-10, 1e-7, 1e-4, 1e-1])
    panel_label(b, "(b)", x=0.85)
    save(fig, "fig1_shape")


# ---------------------------------------------------------------- Figure 2
def fig_short():
    sl = load(R_V, "slopes_summary.json")
    styles = {
        "parabola_d0.05_unchirped_nsp1": (BLUE, "o", True, "parabola"),
        "parabola_d0.05_unchirped_nsp2": (BLUE, "o", False, None),
        "parabola_d0.05_asymchirp_nsp1": (AQUA, "^", True, "chirped parabola"),
        "parabola_d0.05_asymchirp_nsp2": (AQUA, "^", False, None),
        "gaussian_unchirped_nsp1": (ORANGE, "s", True, "Gaussian"),
        "gaussian_unchirped_nsp2": (ORANGE, "s", False, None),
    }
    fig, (a, b) = plt.subplots(1, 2, figsize=(W1, 1.62), layout="constrained")
    a.axvspan(1.0, 2.2, color=SHADE, lw=0, zorder=0)
    RR = np.linspace(0.35, 2.15, 10)
    a.plot(RR, 1 - RR, color=INK, lw=0.9, zorder=1, label=r"$1-R$")
    a.axhline(0, color=GRID, lw=0.6, zorder=0)
    pts = []
    for key, (col, mk, filled, lab) in styles.items():
        nsp = 2.0 if key.endswith("nsp2") else 1.0
        rows = sl["cases"][key]["rows"]
        x = [r["R"] for r in rows]
        y = [r["slope"] / (2 * nsp) for r in rows]
        a.plot(x, y, mk, color=col, mfc=col if filled else "white", ms=3.0, mew=0.7, zorder=3,
               label=lab)
        pts += [dict(case=key, nsp=nsp, R=r["R"], slope_per_tau=r["slope"],
                     slope_over_2nsp=r["slope"] / (2 * nsp), theory=r["slope_theory"] / (2 * nsp))
                for r in rows]
    DATA["fig2a_initial_slopes"] = dict(run=R_V, note="slope is d lambda_LO/d tau at tau=0+; "
                                        "open symbols n_sp=2 (held out)", points=pts,
                                        max_abs_slope_err={k: sl["cases"][k]["max_abs_slope_err"]
                                                           for k in styles})
    a.text(1.6, 0.30, "squeezed at\nshort length", fontsize=5.8, color=INK2, ha="center", va="center")
    a.plot([], [], "o", mfc="white", mec=INK2, ms=3.0, mew=0.7, label=r"open: $n_{sp}=2$")
    a.set(xlim=(0.35, 2.15), ylim=(-1.2, 0.75), xlabel=r"$R=\gamma\langle P\rangle_P/(n_{sp}g)$")
    a.set_ylabel(r"$\lambda_{\rm LO}'(0^+)/(2n_{sp}g)$", labelpad=1)
    a.legend(loc="lower left", fontsize=5.4, handletextpad=0.3, borderaxespad=0.2)
    panel_label(a, "(a)", x=0.85)

    # (b) matched-mode minimum variance at short and moderate length, full field
    cs = load(R_V, "curve_summary.json")["curve"]
    out = {}
    for key, col, mk, lab in (("0.05", BLUE, "o", r"$\varepsilon_0=0.05$"),
                              ("0.025", ORANGE, "s", r"$\varepsilon_0=0.025$")):
        t = np.array([r["tau"] for r in cs[key]])
        lam = np.array([r["lam_min"] for r in cs[key]])
        b.plot(t, lam, mk + "-", color=col, ms=2.7, lw=0.7, mew=0.6, zorder=3, label=lab)
        out[key] = dict(tau=t.tolist(), lambda_LO=lam.tolist())
    eps0 = 0.05
    # R = gamma<P>_P/(n_sp g) = kappa gamma P0/g = kappa/(Gamma eps0), with kappa = <P>_P/P0 of the
    # delta = 0.05 smoothed parabola used for these curves (curve.py of the run), taken from slopes_summary.json
    kappa = sl["cases"]["parabola_d0.05_asymchirp_nsp1"]["kappa"]
    Rsrc = kappa / (SQ18 * eps0)
    ts = np.geomspace(0.008, 0.12, 20)
    b.plot(ts, 1 + 2 * (1 - Rsrc) * ts, color=INK2, ls="--", lw=0.8, zorder=2)
    b.text(0.0092, 0.12, r"$1+2(1-R)\tau$", fontsize=5.6, color=INK2)
    b.axhline(1.0, color=INK2, ls=":", lw=0.8, zorder=1)
    b.text(0.25, 1.06, "vacuum", fontsize=5.8, color=INK2)
    short = load(R_E, "fullfield-short.json")[0]
    ffm = [r for r in load(R_E, "fullfield-main.json") if r["epsilon"] == 0.05 and r["chirped"]
           and r["smoothing"] == 0.0]
    ge_t = [short["tau"]] + [r["tau"] for r in ffm]
    ge_l = [short["full"]["lambda_LO"]] + [r["full"]["lambda_LO"] for r in ffm]
    b.plot(ge_t, ge_l, "v", mfc="none", mec=AQUA, ms=3.8, mew=0.8, zorder=4, label="gpt-e")
    src = load(R_P, "summary.json")["similariton"]["short_gain_counterexample"][0]
    b.plot([src["tau"]], [src["matched_LO_min"]], "D", mfc="none", mec=INK, ms=3.8, mew=0.8, zorder=4,
           label="GPT 6 Pro")
    DATA["fig2b_lambda_LO"] = dict(run=R_V, Gamma=SQ18, nsp=1, curves=out,
                                   launch="parabola smoothed at delta=0.05, asymptotic chirp sqrt(2) (curve.py)",
                                   tangent_kappa=kappa, tangent_R=Rsrc,
                                   gpte=dict(run=R_E, tau=ge_t, lambda_LO=ge_l, eps0=0.05, chirped=True),
                                   gpt6pro=dict(run=R_P, tau=src["tau"], lambda_LO=src["matched_LO_min"]))
    b.set(xscale="log", xlim=(0.008, 5), ylim=(0, 3.5), xlabel=r"$\tau=gz$")
    b.set_ylabel(r"$\lambda_{\rm LO}$ (vacuum $=1$)", labelpad=1)
    b.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88), fontsize=5.4, handletextpad=0.3,
             borderaxespad=0.2)
    panel_label(b, "(b)")
    save(fig, "fig2_short")


# ---------------------------------------------------------------- Figure 3
def fig_large():
    red = load(R_V, "reduced_summary.json")["cases"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W1, 1.62), layout="constrained")
    # (a) error of the C_PP prefactor
    tt = np.linspace(0, 80, 50)
    store = {}
    for key, col, mk, lab in (("G18_asym", BLUE, "o", r"$\Gamma=\sqrt{18}$"),
                              ("G1_unchirped", ORANGE, "s", r"$\Gamma=1$")):
        env = red[key]["nsp1"]["ratio_err_envelope"]
        a.plot(env["tau"], env["abs_err"], mk, color=col, ms=3.0, mew=0.6, zorder=3, label=lab)
        store[key] = dict(run=R_V, envelope=env, ratio_at=red[key]["nsp1"]["ratio_i_at"])
        ref = env["abs_err"][0]
        a.plot(tt, ref * np.exp(-(tt - env["tau"][0]) / 3), color=col, ls="--", lw=0.7, zorder=1)
    ge = {}
    for (G, launch), col, mk in (((SQ18, "asymptotic"), BLUE, "o"), ((1.0, "unchirped"), ORANGE, "s")):
        e = gpte_case(G, 1.0, launch)
        t = np.array([r["tau"] for r in e["rows"]])
        ratio = np.array([r["CPP"] / ((32 / 9) * np.exp(r["tau"]) * r["Phi_NL"] ** 2) for r in e["rows"]])
        a.plot(t, abs(ratio - 1), mk, mfc="none", mec=col, ms=3.0, mew=0.6, zorder=2)
        ge[f"Gamma={G:.4g},{launch}"] = dict(run=R_E, tau=t.tolist(), ratio=ratio.tolist())
    a.plot([], [], "o", mfc="none", mec=INK2, ms=3.0, mew=0.6, label="gpt-e (samples)")
    a.text(60, 2e-6, r"$\propto G^{-1/3}$", fontsize=6.3, color=INK, ha="center")
    a.set(yscale="log", xlim=(0, 80), ylim=(1e-12, 1), xlabel=r"$\tau=\ln G$", xticks=[0, 20, 40, 60, 80],
          yticks=[1e-12, 1e-8, 1e-4, 1])
    a.set_ylabel(r"$|C_{PP}/(\frac{32n_{sp}}{9}G\Phi_{NL}^2)-1|$", labelpad=1)
    a.legend(loc="lower left", fontsize=5.4, handletextpad=0.3, borderaxespad=0.2)
    panel_label(a, "(a)", x=0.85)
    DATA["fig3a_CPP_prefactor"] = dict(claude_interactive_13=store, gpte=ge)

    # (b) compensated minimum variance of the matched mode
    v18 = red["G18_asym"]["nsp1"]
    b.fill_between([12, 26], *v18["Gm13_lam_lead_range_12_26"], color=SHADE, lw=0, zorder=0)
    b.fill_between([26, 80], *v18["Gm13_lam_lead_range_26_80"], color=SHADE, lw=0, zorder=0)
    lam_at = v18["lam_lead_at"]
    tv = np.array([float(k) for k in lam_at])
    lv = np.array([lam_at[k] for k in lam_at]) * np.exp(-tv / 3)
    b.plot(tv, lv, "o", color=BLUE, ms=3.0, mew=0.6, zorder=3, label=r"$\Gamma=\sqrt{18}$, $n_{sp}=1$")
    gb = {}
    for (G, launch, nsp), col, mk, fill, lab in (((SQ18, "asymptotic", 1.0), BLUE, "o", False, None),
                                                 ((SQ18, "asymptotic", 2.0), AQUA, "^", False,
                                                  r"$\Gamma=\sqrt{18}$, $n_{sp}=2$"),
                                                 ((1.0, "unchirped", 1.0), ORANGE, "s", False,
                                                  r"$\Gamma=1$, $n_{sp}=1$")):
        e = gpte_case(G, nsp, launch)
        t = np.array([r["tau"] for r in e["rows"]])
        lm = np.array([lo_minimum(r["CAA"], r["CPP"], r["phase_energy_deficit"]) for r in e["rows"]])
        y = lm * np.exp(-t / 3)
        b.plot(t, y, mk + "-", color=col, mfc="white", ms=2.9, lw=0.5, mew=0.6, zorder=2, label=lab)
        gb[f"Gamma={G:.4g},{launch},nsp={nsp}"] = dict(run=R_E, tau=t.tolist(), lambda_min=lm.tolist(),
                                                       compensated=y.tolist())
    src = load(R_V, "source_seed_summary.json")["eps0.05_tau4.0_N4096_L16.0_steps20000"]["lam_min"]
    ffm = [r for r in load(R_E, "fullfield-main.json") if r["epsilon"] == 0.05 and r["chirped"]
           and r["smoothing"] == 0.0 and r["tau"] == 4.0][0]["full"]["lambda_LO"]
    b.plot([4.0], [src * np.exp(-4 / 3)], "*", color=INK, ms=4.6, mew=0.4, zorder=4,
           label=r"full field, $\tau=4$")
    b.plot([4.0], [ffm * np.exp(-4 / 3)], "*", mfc="none", mec=INK, ms=4.6, mew=0.5, zorder=4)
    b.text(53, 0.13, "range, reduced\n" r"$\Gamma=\sqrt{18}$, $n_{sp}=1$", fontsize=5.2, color=INK2,
           ha="center")
    DATA["fig3b_lambda_min"] = dict(claude_interactive_13=dict(
        run=R_V, lam_lead_at=lam_at, range_12_26=v18["Gm13_lam_lead_range_12_26"],
        range_26_80=v18["Gm13_lam_lead_range_26_80"], fullfield_tau4_source_launch=src), gpte=gb,
        gpte_fullfield_tau4=dict(run=R_E, lambda_LO=ffm))
    b.set(xlim=(0, 80), ylim=(0, 2.65), xlabel=r"$\tau=\ln G$", xticks=[0, 20, 40, 60, 80])
    b.set_ylabel(r"$G^{-1/3}\lambda_{\min}(C_{\rm LO})$", labelpad=1)
    b.legend(loc="upper right", fontsize=5.2, handletextpad=0.3, borderaxespad=0.2, ncol=1)
    panel_label(b, "(b)", x=0.04)
    save(fig, "fig3_large")


if __name__ == "__main__":
    fig_shape()
    fig_short()
    fig_large()
    (OUT / "figure_data.json").write_text(json.dumps(
        {"generated_by": "make_figures.py (claude-interactive.20, claude-opus-5-5, claude)",
         "runs": [R_E, R_P, R_A, R_V], **DATA}, indent=1) + "\n")
    print("wrote", sorted(p.name for p in OUT.iterdir()))
