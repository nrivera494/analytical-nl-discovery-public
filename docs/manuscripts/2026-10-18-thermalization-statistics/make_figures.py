#!/usr/bin/env python3
"""Figures for the manuscript "Statistics of Kerr-thermalized light in multimode fibre".

agent: claude-interactive.11; model: claude-opus-5-5; family: claude.

Reads only numbers already committed in run folders under runs/; it runs no
simulation. Every plotted value comes from one of these runs:

  Fig. 1  runs/2026-10-17-gpt-b-dirichlet           (summary.json, mc_summary.json)
  Fig. 2a runs/2026-10-18-gpt-b-grin-squeezing      (summary.json)
          runs/2026-10-18-gpt-b-kerr-exact          (summary.json, curvature_gate)
  Fig. 2b runs/2026-10-18-gpt-b-condensate-squeezing (refinement_summary.json)
  Fig. 3  runs/2026-10-18-gpt-b-kerr-exact          (exact_summary.json)
          runs/2026-10-18-gpt-b-condensate-squeezing (extracted_stage.json)

The plotted numbers are also written to figures/figure_data.json.
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

# Colour roles (validated: categorical slots 1-3 pass all-pairs CVD checks;
# the nu ramp is a single-hue ordinal ramp). Marker shape doubles every colour.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
E_STYLE = {0.3: (BLUE, "o"), 0.6: (ORANGE, "s"), 0.9: (AQUA, "^")}
NU_RAMP = {1: "#86b6ef", 3: "#3987e5", 10: "#1c5cab", 30: "#0d366b"}
W1 = 3.375  # revtex single-column width, inches

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


def panel_label(ax, s):
    ax.text(0.03, 0.97, s, transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
            fontweight="bold", color=INK)


def save(fig, stem):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{stem}.pdf", metadata={"Author": "claude-interactive.11 (claude-opus-5-5)", "CreationDate": None})
    fig.savefig(OUT / f"{stem}.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 1
def fig_dirichlet():
    run = "2026-10-17-gpt-b-dirichlet"
    s, mc = load(run, "summary.json"), load(run, "mc_summary.json")
    fig, (a, b) = plt.subplots(1, 2, figsize=(W1, 1.52), layout="constrained")

    # (a) excited-mode g2 against mode number
    M = np.linspace(4.5, 40, 200)
    a.plot(M, 2 - 2 / M, color=INK, lw=1.0, label=r"Dirichlet $2-2/M$", zorder=1)
    a.axhline(2.0, color=INK2, ls=":", lw=0.8, label="thermal, 2", zorder=1)
    rows = [(r["M"], float(np.mean(r["g2"][1:])), r["mean_g2_se"]) for r in mc["rows"]]
    DATA["fig1a_simplex"] = [dict(M=m, g2=g, se=e) for m, g, e in rows]
    a.plot([r[0] for r in rows], [r[1] for r in rows], "x", color=INK2, ms=3.2, mew=0.7,
           label="simplex sampling", zorder=2)
    dyn = []
    for E, off in [(0.3, -0.55), (0.6, 0.0), (0.9, 0.55)]:
        r = next(g for g in s["groups"] if g["K"] == 5 and g["sigma"] == 0.3 and g["E"] == E
                 and g["dt"] == 0.04 and g["end"] == 8000)
        col, mk = E_STYLE[E]
        a.errorbar(r["M"] + off, r["pooled"][2], yerr=r["se"][2], fmt=mk, color=col, ms=3.2,
                   mew=0.6, elinewidth=0.6, zorder=3)
        dyn.append(dict(K=5, M=r["M"], E=E, g2=r["pooled"][2], se=r["se"][2], pred=r["prediction"][2]))
    held = [g for g in s["groups"] if g["held_out"] and g["dt"] == 0.04]
    for r in held:
        a.errorbar(r["M"] + 0.7, r["pooled"][2], yerr=r["se"][2], fmt="D", mfc="white", mec=INK2,
                   color=INK2, ms=3.0, mew=0.7, elinewidth=0.6, zorder=3)
        dyn.append(dict(K=r["K"], M=r["M"], E=r["E"], g2=r["pooled"][2], se=r["se"][2],
                        pred=r["prediction"][2], held_out=True))
    a.plot([], [], "D", mfc="white", mec=INK2, ms=3.0, mew=0.7, label="held out")
    fresh = next(p for p in s["phase_followup"]["rows"] if p["tag"] == "fresh_heldout")
    a.errorbar(21 + 1.6, fresh["pooled"][2], yerr=fresh["se"][2], fmt="v", mfc="white", mec=INK,
               color=INK, ms=3.4, mew=0.7, elinewidth=0.6, zorder=4, label="400-launch holdout")
    dyn.append(dict(K=6, M=21, E=fresh["E"], g2=fresh["pooled"][2], se=fresh["se"][2],
                    pred=fresh["prediction"][2], tag="fresh_heldout"))
    DATA["fig1a_dynamics"] = dyn
    a.plot([], [], "o", color=INK2, ms=3.2, label="dynamics, $K=5$")
    a.set(xlabel=r"number of modes $M$", ylabel=r"excited-mode $g^{(2)}$", xlim=(4, 40),
          ylim=(1.62, 2.06))
    a.legend(loc="lower right", fontsize=5.4, ncol=1, handletextpad=0.4, borderaxespad=0.2)
    panel_label(a, "(a)")

    # (b) condensate-mode covariance, rescaled so the Dirichlet law is the line S1*q - D
    D, S1 = 14, 4 + (1 + 1 / 2 + 1 / 3 + 1 / 4)
    q = np.linspace(0.7, 4.3, 50)
    b.axhline(0, color=GRID, lw=0.6, zorder=0)
    b.plot(q, S1 * q - D, color=INK, lw=1.0, zorder=1, label=r"Dirichlet: $S_1\varepsilon_q-D$")
    b.axvline(D / S1, color=INK2, ls=":", lw=0.8, zorder=1)
    b.text(D / S1 + 0.07, 10.0, r"$D/S_1$", color=INK2, fontsize=6.5, va="center")
    cov = []
    for E, off in [(0.3, -0.1), (0.6, 0.0), (0.9, 0.1)]:
        r = next(g for g in s["groups"] if g["K"] == 5 and g["sigma"] == 0.3 and g["E"] == E
                 and g["dt"] == 0.04 and g["end"] == 8000)
        k = r["metric_order"].index("group_covariances")
        # pooled vector: 4 scalars, 14 per-mode g2 values, then 4 group covariances
        c, e = np.array(r["pooled"][4 + D:]), np.array(r["se"][4 + D:])
        qq = np.arange(1, 5)
        scale = qq ** 2 * D ** 2 * (D + 1) / E ** 2
        col, mk = E_STYLE[E]
        b.errorbar(qq + off, c * scale, yerr=e * scale, fmt=mk, color=col, ms=3.2, mew=0.6,
                   elinewidth=0.6, zorder=3, label=fr"$E'/\kappa N={E}$")
        cov.append(dict(E=E, q=qq.tolist(), cov=c.tolist(), se=e.tolist(),
                        scaled=(c * scale).tolist(), metric_index=k))
    DATA["fig1b_covariance_K5"] = dict(D=D, S1=S1, rows=cov)
    b.set(xlabel=r"mode-group energy $\varepsilon_q/\kappa$", xlim=(0.6, 4.4), ylim=(-12, 13),
          xticks=[1, 2, 3, 4])
    b.set_ylabel(r"$\varepsilon_q^2\,\mathrm{Cov}(I_0,I_q)/c$", labelpad=1)
    b.legend(loc="lower right", fontsize=5.6, handletextpad=0.3, handlelength=1.0, borderaxespad=0.15)
    panel_label(b, "(b)")
    save(fig, "fig1_dirichlet")


# ---------------------------------------------------------------- Figure 2
def fig_squeezing():
    fig, (a, b) = plt.subplots(1, 2, figsize=(W1, 1.56), layout="constrained")

    # (a) curvature excess of the fixed tangent direction against R = sigma_max^6 / n0
    g = load("2026-10-18-gpt-b-grin-squeezing", "summary.json")
    coef = g["core_quad_scaling"]["relative_curvature_coefficient"]
    pts = []
    for c in g["cases"]:
        if not (c["K"] == 5 and c["sigma"] == 0.3 and c["launch"] == 4201 and c["dt"] == 0.02
                and c["shots"] == 2048 and c["alpha"] == 0 and c["weyl"]):
            continue
        for r in c["checkpoints"]:
            if r["z"] not in (5, 10, 20):
                continue
            y = r["quad_fixed_control"]["mean"] / r["linear_quad"] - 1
            se = r["quad_fixed_control"]["se"] / r["linear_quad"]
            pts.append(dict(E=c["E"], n=c["n"], z=r["z"], R=r["ratio"], f0=r["f0"],
                            excess=y, se=se, plotted=bool(y > 2 * se)))
    DATA["fig2a_curvature"] = dict(coefficient=coef, points=pts)
    a.axvspan(1e-4, 0.8, color="#eeeeec", lw=0, zorder=0)
    xx = np.geomspace(1e-3, 3e4, 50)
    l1, = a.plot(xx, xx / 8, color=INK2, ls="--", lw=0.9, zorder=1, label=r"one mode, exact: $R/8$")
    l2, = a.plot(xx, coef["mean"] * xx, color=INK, lw=1.0, zorder=1,
                 label=fr"15 modes, fit: ${coef['mean']:.3f}\,R$")
    a.add_artist(a.legend(handles=[l1, l2], loc="upper left", bbox_to_anchor=(0.0, 0.88),
                          fontsize=5.4, handletextpad=0.4, borderaxespad=0.2))
    for E in (0.3, 0.6, 0.9):
        col, mk = E_STYLE[E]
        sel = [p for p in pts if p["E"] == E and p["plotted"]]
        a.errorbar([p["R"] for p in sel], [p["excess"] for p in sel], yerr=[p["se"] for p in sel],
                   fmt=mk, color=col, ms=3.0, mew=0.6, elinewidth=0.6, zorder=3,
                   mfc=col if E != 0.9 else "white", label=fr"$E'/\kappa N={E}$")
    gate = load("2026-10-18-gpt-b-kerr-exact", "summary.json")["curvature_gate"]
    DATA["fig2a_single_mode_exact"] = gate
    a.text(0.75, 3e-4, r"$R\leq0.8$", color=INK2, fontsize=6.3, ha="right")
    a.set(xscale="log", yscale="log", xlim=(1e-3, 3e4), ylim=(1e-4, 3e3),
          xlabel=r"$R=\sigma_{\max}^6/n_0$")
    a.set_ylabel(r"$V_{\rm fixed}/\lambda_{\rm lin}-1$", labelpad=1)
    a.set_xticks([1e-2, 1, 1e2, 1e4])
    a.set_yticks([1e-3, 1e-1, 1e1, 1e3])
    hs, ls_ = a.get_legend_handles_labels()
    keep = [(h, l) for h, l in zip(hs, ls_) if l.startswith("$E'")]
    a.legend([h for h, _ in keep], [l for _, l in keep], loc="lower right", fontsize=5.4,
             handletextpad=0.4, borderaxespad=0.2)
    panel_label(a, "(a)")

    # (b) the condensate's own squeezing and the pure-state value 1/V_P at the same V_P
    rs = load("2026-10-18-gpt-b-condensate-squeezing", "refinement_summary.json")
    paths = [r for r in rs["records"] if r["sigma"] == 0.3 and r["dt"] == 0.0025 and r["E"] == 0.3]
    zs = [5.0, 10.0, 20.0, 50.0]
    lam, pure, rows = {z: [] for z in zs}, {z: [] for z in zs}, []
    for p in paths:
        for r in p["rows"]:
            if r["z"] in zs:
                lam[r["z"]].append(10 * np.log10(r["lambda_own"]))
                pure[r["z"]].append(10 * np.log10(1 / r["own"][1][1]))
                rows.append(dict(disorder=p["disorder"], z=r["z"], f0=r["f0"], nu=r["nu"],
                                 lambda_own=r["lambda_own"], detV_over_VP=r["own_approx"],
                                 VX=r["own"][0][0], C=r["own"][0][1], VP=r["own"][1][1]))
    stats = {z: dict(lam_mean=float(np.mean(lam[z])), lam_sd=float(np.std(lam[z], ddof=1)),
                     pure_mean=float(np.mean(pure[z])), pure_sd=float(np.std(pure[z], ddof=1)),
                     members=len(lam[z])) for z in zs}
    DATA["fig2b_condensate"] = dict(paths=len(paths), stats=stats, rows=rows)
    b.axvspan(5 / 1.15, 20 * 1.15, color="#eeeeec", lw=0, zorder=0)
    rng = np.random.default_rng(1)
    for z in zs:
        jit = z * np.exp(rng.uniform(-0.06, 0.06, len(lam[z])))
        b.plot(jit, lam[z], ".", color=BLUE, ms=1.6, alpha=0.45, zorder=2)
        b.plot(jit, pure[z], ".", color=ORANGE, ms=1.6, alpha=0.45, zorder=2)
    for key, col, mk, lab in [("lam", BLUE, "o", r"$\lambda_-$"),
                              ("pure", ORANGE, "s", r"$1/V_P$ (pure, same $V_P$)")]:
        for z in zs:
            st = stats[z]
            b.errorbar(z, st[f"{key}_mean"], yerr=st[f"{key}_sd"], fmt=mk, color=col, ms=3.2,
                       mew=0.7, elinewidth=0.7, zorder=4, mfc=col if z <= 20 else "white")
        b.plot([], [], mk, color=col, ms=3.2, label=lab)
    zc = 10.0
    b.annotate("", xy=(zc * 1.32, stats[zc]["lam_mean"]), xytext=(zc * 1.32, stats[zc]["pure_mean"]),
               arrowprops=dict(arrowstyle="<->", lw=0.6, color=INK2, shrinkA=0, shrinkB=0))
    b.text(zc * 1.4, 0.5 * (stats[zc]["lam_mean"] + stats[zc]["pure_mean"]), r"$\det V$",
           fontsize=6.5, color=INK2, va="center")
    b.set(xscale="log", xlim=(3.6, 70), ylim=(-43, 0), xlabel=r"$z/L_{\rm NL}$")
    b.set_ylabel(r"variance (dB rel. vacuum)", labelpad=1)
    b.set_xticks([5, 10, 20, 50])
    b.set_xticklabels(["5", "10", "20", "50"])
    b.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    b.legend(loc="lower left", fontsize=5.6, handletextpad=0.3, borderaxespad=0.2)
    panel_label(b, "(b)")
    save(fig, "fig2_squeezing")


# ---------------------------------------------------------------- Figure 3
def fig_squeezability():
    ex = load("2026-10-18-gpt-b-kerr-exact", "exact_summary.json")
    pref = 3 / (2 * 4 ** (1 / 3))
    fig, (a, b) = plt.subplots(1, 2, figsize=(W1, 1.52), layout="constrained")
    rows = []
    for nu in (1, 3, 10, 30):
        rr = sorted([r for r in ex["rows"] if r["nu"] == nu and r["n"] >= 1e4], key=lambda r: r["n"])
        n = np.array([r["n"] for r in rr])
        lam = np.array([r["exact"]["lambda"] for r in rr])
        held = np.array([r["held_out"] for r in rr])
        col = NU_RAMP[nu]
        nn = np.geomspace(1e4, 1e12, 50)
        a.plot(nn, 10 * np.log10(pref * (nu ** 4 / nn) ** (1 / 3)), color=col, lw=0.9, zorder=1)
        for x, y, h in zip(n, lam, held):
            a.plot(x, 10 * np.log10(y), "o", color=col, mfc="white" if h else col, ms=3.0, mew=0.7, zorder=3)
            b.plot(x, y * x ** (1 / 3) / nu ** (4 / 3), "o", color=col, mfc="white" if h else col,
                   ms=3.0, mew=0.7, zorder=3)
        b.plot(n, lam * n ** (1 / 3) / nu ** (4 / 3), color=col, lw=0.7, zorder=2)
        a.plot([], [], "o-", color=col, ms=3.0, lw=0.9, label=fr"$\nu={nu}$")
        rows += [dict(nu=nu, n_d=float(x), lambda_exact=float(y), held_out=bool(h)) for x, y, h in zip(n, lam, held)]
    DATA["fig3_exact_displaced_thermal"] = dict(prefactor=pref, rows=rows)
    a.set(xscale="log", xlim=(5e3, 2e12), ylim=(-44, 15), xlabel=r"displacement photons $n_d$",
          xticks=[1e4, 1e6, 1e8, 1e10, 1e12])
    a.set_ylabel(r"best variance $\lambda_*$ (dB)", labelpad=1)
    a.legend(loc="upper right", fontsize=5.6, handletextpad=0.4, ncol=1)
    panel_label(a, "(a)")

    ext = load("2026-10-18-gpt-b-condensate-squeezing", "extracted_stage.json")["rows"]
    xs = np.array([r["n0"] for r in ext])
    ys = np.array([r["mean"] * r["n0"] ** (1 / 3) / r["nu"] ** (4 / 3) for r in ext])
    es = np.array([r["se"] * r["n0"] ** (1 / 3) / r["nu"] ** (4 / 3) for r in ext])
    DATA["fig3b_extracted_condensate"] = [dict(E=r["E"], sigma=r["sigma"], z=r["z"], n=r["n"], n0=r["n0"],
                                               nu=r["nu"], measured=r["mean"], se=r["se"],
                                               prediction=r["prediction"],
                                               diff_dB=float(10 * np.log10(r["mean"] / r["prediction"])))
                                          for r in ext]
    b.axhline(pref, color=INK, lw=1.0, zorder=1, label=r"$3/(2\cdot4^{1/3})$")
    jit = np.exp(np.linspace(-0.25, 0.25, len(xs)))
    b.errorbar(xs * jit, ys, yerr=es, fmt="*", color=INK2, ms=4.2, mew=0.4, elinewidth=0.6,
               zorder=4, label="GRIN condensate")
    b.set(xscale="log", xlim=(5e3, 2e12), ylim=(0.88, 1.03), xlabel=r"$n_d$",
          xticks=[1e4, 1e6, 1e8, 1e10, 1e12])
    b.set_ylabel(r"$\lambda_*\,n_d^{1/3}/\nu^{4/3}$", labelpad=1)
    b.legend(loc="upper right", fontsize=5.6, handletextpad=0.3, borderaxespad=0.2)
    panel_label(b, "(b)")
    save(fig, "fig3_squeezability")


if __name__ == "__main__":
    fig_dirichlet()
    fig_squeezing()
    fig_squeezability()
    (OUT / "figure_data.json").write_text(json.dumps(
        {"generated_by": "make_figures.py (claude-interactive.11, claude-opus-5-5, claude)",
         "runs": ["2026-10-17-gpt-b-dirichlet", "2026-10-18-gpt-b-grin-squeezing",
                  "2026-10-18-gpt-b-kerr-exact", "2026-10-18-gpt-b-condensate-squeezing"],
         **DATA}, indent=1) + "\n")
    print("wrote", sorted(p.name for p in OUT.iterdir()))
