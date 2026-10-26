"""Figures for the amplifier-similariton validation (claude-interactive.2). Reads raw outputs, writes PNGs into run folders."""
import os, sys, glob, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUNS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/")
sys.path.insert(0, os.path.join(RUNS, "2026-10-10-claude-interactive.2-attraction"))
sys.path.insert(0, os.path.join(RUNS, "2026-10-10-claude-interactive.2-shape-modes"))
sys.path.insert(0, os.path.join(RUNS, "2026-10-10-claude-interactive.2-moment-noise"))
sys.path.insert(0, os.path.join(RUNS, "2026-10-10-claude-interactive.2-gain-noise-mc"))

INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SER = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]   # categorical slots 1, 2, 3, 7 (fixed order)
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "lines.linewidth": 1.6})
EPS_ORDER = [0.1, 0.05, 0.025, 0.0125]
ECOL = {e: c for e, c in zip(EPS_ORDER, SER)}


def save(fig, run, name):
    p = os.path.join(RUNS, run, name)
    fig.savefig(p, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote", p)


def fig_attraction():
    import analyze_attraction as A
    D = RAW + "2026-10-10-claude-interactive.2-attraction/"
    launches = [(1.0, 0.0), (1.0, 1.0), (4.243, -0.5), (4.243, 1.0), (10.0, -0.5), (10.0, 1.0)]
    cols = {(1.0, 0.0): SER[0], (1.0, 1.0): SER[1], (4.243, -0.5): SER[2], (4.243, 1.0): SER[3], (10.0, -0.5): INK2, (10.0, 1.0): "#a8a7a2"}
    lab = lambda G, q: f"w={((G*G/18)**(1/3)):.2f}, q={q:g}"
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.5))
    for (G, q) in launches:
        p = None
        for e in ("0.0125", "0.025", "0.05", "0.1"):
            cand = D + f"att_e{e}_G{G:.3f}_q{q:.3f}.json"
            if os.path.exists(cand):
                p = cand; break
        if p is None:
            continue
        c = A.compare(A.load(p))
        ax[0].plot(c["tau"], c["s"], color=cols[(G, q)], lw=1.6, label=lab(G, q))
        ax[0].plot(c["tau"], c["s_ode"], color=INK, ls=":", lw=1.0)
    ax[0].axhline(1, color=INK2, lw=0.8)
    ax[0].set_xlabel(r"$\tau=gz$"); ax[0].set_ylabel(r"$s=T_p/(c\,e^{\tau/3})$ (rms-derived)")
    ax[0].set_title("Full NLSE (solid) vs width ODE (dotted), smallest $\\varepsilon_0$ run", fontsize=8.5)
    ax[0].legend(fontsize=7, ncol=2)
    rows = {}
    for p in glob.glob(D + "att_e*.json"):
        d = A.load(p); c = A.compare(d)
        rows.setdefault((round(d["Gamma"], 3), round(d["q"], 3)), []).append((d["eps0"], c["err_s_rel"]))
    for k, v in sorted(rows.items()):
        v = sorted(v)
        if len(v) < 2:
            continue
        e, er = zip(*v)
        ax[1].loglog(e, er, marker="o", ms=4, lw=1.0, color=cols.get(k, "#c9c8c3"), label=lab(*k) if k in cols else None)
    ee = np.array([0.0125, 0.1])
    ax[1].loglog(ee, 0.5 * ee ** 2, color=INK, ls="--", lw=0.8, label=r"$\propto\varepsilon_0^2$")
    ax[1].set_xticks([0.0125, 0.025, 0.05, 0.1]); ax[1].set_xticklabels(["0.0125", "0.025", "0.05", "0.1"])
    ax[1].minorticks_off()
    ax[1].set_xlabel(r"$\varepsilon_0$"); ax[1].set_ylabel(r"max$_{\tau\leq 6}|s/s_{\rm ODE}-1|$")
    ax[1].set_title("R1: deviation from the width ODE (grey: other launches)", fontsize=8.5)
    ax[1].legend(fontsize=6.5, ncol=2)
    save(fig, "2026-10-10-claude-interactive.2-attraction", "r1_width_ode.png")


def fig_shape():
    import run_analysis as S
    import analyze_shape as A
    D = RAW + "2026-10-10-claude-interactive.2-shape-modes/"
    files = {}
    for p in glob.glob(D + "sm_asym_e*_eta1e-4.json"):
        d = json.load(open(p)); files[d["eps0"]] = p
    if not files:
        return
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    summ = {e: S.summarize(files[e]) for e in sorted(files)}
    for l, col in zip((1, 2, 3, 4), SER):
        v = sorted((e, summ[e]["blocks"][l]["err_at_tau4"]) for e in summ)
        e, er = zip(*v)
        ax[0].loglog(e, er, marker="o", ms=4, color=col, label=f"l={l}")
    ax[0].set_xlabel(r"$\varepsilon_0$"); ax[0].set_ylabel(r"max$_{\tau\leq 4}\|M_l-M_l^{\rm ODE}\|/\|M_l^{\rm ODE}\|$")
    ax[0].set_title("Block maps vs reduced block ODE", fontsize=9); ax[0].legend(fontsize=8)
    for l, col in zip((2, 3, 4), SER[1:]):
        pts = sorted((e, summ[e]["blocks"][l]["generator_tau3to6"]["sim"], summ[e]["blocks"][l]["pred_omega"]) for e in summ)
        e = [p[0] for p in pts]
        ax[1].loglog(e, [abs(p[1]["omega"] / p[2] - 1) for p in pts], marker="o", ms=4, color=col, label=f"l={l}, frequency")
        ax[1].loglog(e, [abs(3 * p[1]["decay"] - 1) for p in pts], marker="s", ms=4, color=col, ls="--", mfc="none", label=f"l={l}, decay")
    ax[1].set_xlabel(r"$\varepsilon_0$"); ax[1].set_ylabel("relative deviation from prediction")
    ax[1].set_title(r"Rates on $\tau\in[3,\tau_{\rm end}]$ vs $\frac{g}{3}$, $\frac{g}{3}\sqrt{l(l+1)/2-1}$", fontsize=9)
    ax[1].legend(fontsize=6.5, ncol=2)
    for a in ax[:2]:
        a.set_xticks(sorted(summ)); a.set_xticklabels([str(x) for x in sorted(summ)]); a.minorticks_off()
    emin = min(files)
    d = A.load(files[emin]); zeta, maps, X0 = A.sim_maps(d)
    tau = np.array(d["ref"]["tau"])
    for l, col in zip((2, 3, 4), SER[1:]):
        Mo, a = A.ode_maps(d, zeta, l)
        ax[2].plot(tau, maps[l][:, 1, 0], color=col, label=f"l={l} NLSE")
        ax[2].plot(tau, Mo[:, 1, 0], color=INK, ls=":", lw=1.0)
    ax[2].set_xlabel(r"$\tau=gz$"); ax[2].set_ylabel(r"$\partial(n_l/\varepsilon_0)/\partial p_l(0)$")
    ax[2].set_title(rf"Phase-launch response, $\varepsilon_0={emin}$ (dotted: ODE)", fontsize=9); ax[2].legend(fontsize=8)
    save(fig, "2026-10-10-claude-interactive.2-shape-modes", "r2_block_maps.png")


NONBASE = ("conv_", "gbw_", "core_")  # convergence, gain-bandwidth and core-cut variants are not production points


def fig_noise():
    S = json.load(open(os.path.join(RUNS, "2026-10-10-claude-interactive.2-moment-noise", "summary.json")))
    runs = S["runs"]
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.3))
    Us = np.linspace(0.01, 8.2, 200)
    G3 = np.exp(-Us / 3)
    closed = dict(VarWc=(np.ones_like(Us), 3 * (1 - G3)), VarTc=((1 + Us / 3) ** 2, 3 + Us ** 2 / 3 - 3 * G3),
                  VarTcomp=(Us ** 2 / 9, Us ** 2 / 3 - 2 * Us + 6 * (1 - G3)))
    titles = dict(VarWc=r"$N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2$", VarTc=r"$N_0\mathrm{Var}(T_c)/\sigma_{T0}^2$",
                  VarTcomp=r"$N_0\mathrm{Var}(T_{\rm comp})/\sigma_{T0}^2$")
    for j, q in enumerate(("VarWc", "VarTc", "VarTcomp")):
        a = ax[j]
        a.plot(Us, closed[q][0], color=INK2, ls="--", lw=1.0, label="closed form, input")
        a.plot(Us, closed[q][1], color=INK, ls="-", lw=1.0, label="closed form, ASE")
        for e in EPS_ORDER:
            pts = sorted((r["gL"], r["R7_sim"][q]) for kk, r in runs.items() if r["case"] == "asym" and r["eps0"] == e and r["delta_mode"] == "e23" and not kk.startswith(NONBASE))
            if not pts:
                continue
            U, v = zip(*pts); v = np.array(v)
            a.plot(U, v[:, 0], "o", ms=4, mfc="none", color=ECOL[e])
            a.plot(U, v[:, 1], "s", ms=4, color=ECOL[e], label=rf"$\varepsilon_0={e}$")
        a.set_xlabel(r"$gL$"); a.set_title(titles[q], fontsize=9)
    ax[0].legend(fontsize=7)
    ax[1].text(0.3, 0.9, "open: input part\nfilled: ASE part", transform=ax[1].transAxes, fontsize=7, color=INK2, va="top")
    save(fig, "2026-10-10-claude-interactive.2-moment-noise", "r7_closed_forms.png")

    # error scaling: max |relative deviation| over the quantities, separately for input and ASE parts
    E = S["error_exponents"]
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    for j, (case, title) in enumerate((("asym", "R7 closed forms, asymptotic seed"), ("main", "C-01 P3 table, main case"),
                                       ("heldout", "C-01 P5 table, held out"))):
        a = ax[j]; k = 0
        for U in (2, 4, 6):
            for part, mk in (("in", "o"), ("ase", "s")):
                keys = [kk for kk in E if kk.startswith(f"{case}_g{U}_") and kk.endswith("_" + part) and "VarWc_in" not in kk]
                if not keys:
                    continue
                eps = sorted(set(e for kk in keys for e in E[kk]["eps0"]))
                mx = []
                for e in eps:
                    vals = [abs(E[kk]["rel_dev"][E[kk]["eps0"].index(e)]) for kk in keys if e in E[kk]["eps0"]]
                    mx.append(max(vals))
                col = {2: SER[0], 4: SER[1], 6: SER[2]}[U]
                a.loglog(eps, mx, marker=mk, ms=4, lw=1.2, color=col, ls="-" if part == "ase" else "--",
                         mfc=col if part == "ase" else "none", label=f"gL={U}, {part}")
        ee = np.array([0.0125, 0.1])
        a.loglog(ee, 3 * ee ** 2, color=INK, ls=":", lw=0.9, label=r"$\propto\varepsilon_0^2$")
        a.loglog(ee, 0.6 * ee ** (4 / 3), color=INK2, ls="-.", lw=0.9, label=r"$\propto\varepsilon_0^{4/3}$")
        a.set_xticks([0.0125, 0.025, 0.05, 0.1]); a.set_xticklabels(["0.0125", "0.025", "0.05", "0.1"]); a.minorticks_off()
        a.set_xlabel(r"$\varepsilon_0$"); a.set_title(title, fontsize=8.5)
    ax[0].set_ylabel("max relative deviation (entries of the table)")
    h, l = ax[1].get_legend_handles_labels()
    fig.legend(h, l, fontsize=7, ncol=8, loc="lower center", bbox_to_anchor=(0.5, -0.06))
    save(fig, "2026-10-10-claude-interactive.2-moment-noise", "noise_error_scaling.png")


def fig_mc():
    S = json.load(open(os.path.join(RUNS, "2026-10-10-claude-interactive.2-gain-noise-mc", "summary.json")))
    cases = [c for c in ("kerr_ns0.5", "kerr_ns1.0", "kerr_vac", "kerr_ase") if c in S["cases"]]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    for i, c in enumerate(cases):
        r = S["cases"][c]
        ax[0].errorbar(i, r["F_ratio"], yerr=2 * r["F_ratio_err"], fmt="o", color=SER[0], ms=4, capsize=2)
        for j, q in enumerate(("VarTc", "VarWc")):
            ax[1].errorbar(i + 0.15 * (j - 0.5), r[q]["ratio"], yerr=2 * r[q]["ratio_err"], fmt="o" if j == 0 else "s",
                           color=SER[1 + j], ms=4, capsize=2, label=(r"Var $T_c$" if j == 0 else r"Var $\Omega_c$") if i == 0 else None)
    labels = [f"{c}\n({S['cases'][c]['ntraj']})" for c in cases]
    for a in ax:
        a.axhline(1, color=INK2, lw=0.8); a.set_xticks(range(len(cases))); a.set_xticklabels(labels, fontsize=7)
    ax[0].set_ylabel(r"MC / $[1+(2n_{sp}-1)(1-1/G)]$"); ax[0].set_title("R6a: energy noise, MC (2 s.e.) vs exact law", fontsize=9)
    ax[1].set_ylabel("MC / adjoint"); ax[1].set_title("R6b: centroid variances, MC (2 s.e.) vs adjoint", fontsize=9); ax[1].legend(fontsize=8)
    save(fig, "2026-10-10-claude-interactive.2-gain-noise-mc", "mc_vs_exact.png")


def fig_spectral():
    S = json.load(open(os.path.join(RUNS, "2026-10-10-claude-interactive.2-moment-noise", "summary.json")))
    runs = S["runs"]
    import tables as tb
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    for j, (key, tkey, title) in enumerate((("lambda2_over_lambda1_L2", "ratio", r"R9: $\lambda_2/\lambda_1$ ($l\leq 4$, $L^2$)"),
                                            ("one_minus_r2", "omr2", r"R10: $1-r^2$ (matched LO)"))):
        a = ax[j]
        for case, mk in (("main", "o"), ("asym", "s")):
            for e in EPS_ORDER:
                pts = sorted((r["gL"], r[key]) for kk, r in runs.items() if r["case"] == case and r["eps0"] == e and key in r and not kk.startswith(NONBASE) and r["delta_mode"] == "e23")
                if not pts:
                    continue
                U, v = zip(*pts)
                a.semilogy(U, v, marker=mk, ms=4, lw=1.0, color=ECOL[e], ls="-" if case == "main" else "--",
                           label=rf"{case}, $\varepsilon_0={e}$")
        tab = tb.C02_P3 if j == 0 else tb.C02_P4
        U = sorted(tab); a.semilogy(U, [tab[u][tkey] for u in U], "x", color=INK, ms=7, label="C-02 table (main)")
        apts = sorted((r["gL"], r[key]) for kk, r in runs.items() if r["case"] == "asym" and r["eps0"] == 0.1 and key in r and not kk.startswith(NONBASE))
        if apts:
            U8, y8 = apts[-1]
            Ug = np.array([3.0, U8]); a.semilogy(Ug, y8 * np.exp(-2 * (Ug - U8) / 3), color=INK2, ls=":", lw=1.2,
                                                 label=r"slope of $G^{-2/3}$ (through asym, $gL=8$)")
        a.set_xlabel(r"$gL$"); a.set_title(title, fontsize=9); a.legend(fontsize=6)
    save(fig, "2026-10-10-claude-interactive.2-moment-noise", "r9_r10_trends.png")


def fig_r3():
    import analyze_attraction as A
    D = RAW + "2026-10-10-claude-interactive.2-attraction/"
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    DS = RAW + "2026-10-10-claude-interactive.2-shape-modes/"
    for e in EPS_ORDER:
        ps = DS + f"sm_asym_e{e}_g6_eta1e-4.json"
        if os.path.exists(ps):
            r = json.load(open(ps))["ref"]
            tau = np.array(r["tau"]); vT = np.array(r["varT"]); vW = np.array(r["varW"]); cv = np.array(r["cov"])
            ax[0].semilogy(tau, 1 - cv ** 2 / (vT * vW), color=ECOL[e], label=rf"$\varepsilon_0={e}$")
        p = D + f"att_e{e}_G4.243_q0.333.json"
        if os.path.exists(p):
            r = A.load(p)["rows"]
            ax[1].semilogy(np.array(r["tau"]), np.array(r["edge_rho"]), color=ECOL[e], label=rf"$\varepsilon_0={e}$")
    tt = np.linspace(2, 6, 10)
    ax[0].semilogy(tt, 2e-2 * np.exp(-4 * (tt - 2) / 3), color=INK, ls="--", lw=0.9, label=r"$\propto e^{-4\tau/3}$")
    ax[1].semilogy(tt, 3e-2 * np.exp(-4 * (tt - 2) / 9), color=INK, ls="--", lw=0.9, label=r"$\propto e^{-4\tau/9}$")
    ax[0].set_xlabel(r"$\tau=gz$"); ax[0].set_ylabel(r"$1-C_{T\omega}^2/(\sigma_T^2\sigma_\omega^2)$")
    ax[0].set_title("R3: transform-limited share of the bandwidth", fontsize=9); ax[0].legend(fontsize=7)
    ax[1].set_xlabel(r"$\tau=gz$"); ax[1].set_ylabel(r"$\rho(T_{\rm fit})/\rho_{\rm pk}$")
    ax[1].set_title("R3: intensity at the fitted parabola edge", fontsize=9); ax[1].legend(fontsize=7)
    save(fig, "2026-10-10-claude-interactive.2-attraction", "r3_eps_eff.png")


if __name__ == "__main__":
    which = sys.argv[1:] or ["attraction", "r3", "shape", "noise", "mc", "spectral"]
    for w in which:
        try:
            globals()["fig_" + w]()
        except Exception as ex:
            print("figure", w, "failed:", repr(ex))
