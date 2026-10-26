"""Markdown tables for the exploration note, generated from the run summaries (so numbers in the note trace to runs)."""
import os, json, math
import numpy as np

RUNS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def J(run):
    return json.load(open(os.path.join(RUNS, run, "summary.json")))


def f(x, n=3):
    if x is None:
        return "n/a"
    if isinstance(x, (list, tuple)):
        return "(" + ", ".join(f(v, n) for v in x) + ")"
    if x == 0:
        return "0"
    a = abs(x)
    if a >= 1e4 or a < 1e-3:
        return f"{x:.{n-1}e}"
    return f"{x:.{n}g}" if a < 1 else f"{x:.{n+1}g}"


def pct(x):
    return "n/a" if x is None else f"{100*x:+.1f}%"


def noise_tables():
    S = J("2026-10-10-claude-interactive.2-moment-noise")
    R = dedupe(S["runs"])
    out = []
    # R7 closed forms, asymptotic seed
    out.append("| $gL$ | $\\varepsilon_0$ | $\\Omega_c$ (in, ase) | dev | $T_c$ (in, ase) | dev | $T_{\\rm comp}$ (in, ase) | dev |")
    out.append("|---|---|---|---|---|---|---|---|")
    for k in sorted(R, key=lambda k: (R[k]["gL"], -R[k]["eps0"])):
        r = R[k]
        if r["case"] != "asym" or r["delta_mode"] != "e23" or k.startswith(("conv_", "gbw_", "core_")):
            continue
        s, d = r["R7_sim"], r["R7_rel_dev"]
        out.append(f"| {r['gL']:.0f} | {r['eps0']} | {f(s['VarWc'])} | {pct(d['VarWc'][0])}, {pct(d['VarWc'][1])} | {f(s['VarTc'])} | "
                   f"{pct(d['VarTc'][0])}, {pct(d['VarTc'][1])} | {f(s['VarTcomp'])} | {pct(d['VarTcomp'][0])}, {pct(d['VarTcomp'][1])} |")
    out.append("")
    # C-01 P3/P5 tables
    for case, lab in (("main", "P3 (main)"), ("heldout", "P5 (held out)")):
        out.append(f"**C-01 {lab}**: relative deviation of (in, ase) from the frozen table.")
        out.append("")
        out.append("| $gL$ | $\\varepsilon_0$ | Var $T_c/\\sigma_{TL}^2$ | Var $T_{\\rm comp}/T_0^2$ | Var $\\Omega_c/\\sigma_{\\omega L}^2$ (ase) | $\\varepsilon_0$Cov (ase) |")
        out.append("|---|---|---|---|---|---|")
        for k in sorted(R, key=lambda k: (R[k]["gL"], -R[k]["eps0"])):
            r = R[k]
            if r["case"] != case or r["delta_mode"] != "e23" or k.startswith(("conv_", "gbw_", "core_")):
                continue
            d = r["C01_table_rel_dev"]
            out.append(f"| {r['gL']:.0f} | {r['eps0']} | {pct(d['VarTc'][0])}, {pct(d['VarTc'][1])} | {pct(d['VarTcomp'][0])}, {pct(d['VarTcomp'][1])} | "
                       f"{pct(d['VarWc'][1])} | {pct(d['Cov'][1])} |")
        out.append("")
    return "\n".join(out)


def dedupe(R):
    """Drop a TW run when an 'all' run with the same case, eps0, gL and seed family exists (identical centroid numbers)."""
    full = {(r["case"], r["eps0"], r["gL"], r["delta_mode"]) for k, r in R.items() if k.endswith("_all")}
    return {k: r for k, r in R.items() if not (k.endswith("_TW") and (r["case"], r["eps0"], r["gL"], r["delta_mode"]) in full)}


def spectral_tables():
    S = J("2026-10-10-claude-interactive.2-moment-noise")
    R = S["runs"]
    out = ["| case | $gL$ | $\\varepsilon_0$ | $\\lambda_2/\\lambda_1$ | table | $1-r^2$ | table | $\\varepsilon_0^2C_{PP}/G$ (in, ase) | table |",
           "|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(R, key=lambda k: (R[k]["case"], R[k]["gL"], -R[k]["eps0"])):
        r = R[k]
        if "lambda2_over_lambda1_L2" not in r or k.startswith(("conv_", "gbw_", "core_")) or r["case"].startswith("p8"):
            continue
        tr = r.get("C02_P3_table", {}).get("ratio") if r["case"] == "main" else (r.get("C02_P5_table", {}).get("ratio") if r["case"] == "heldout" else None)
        to = r.get("C02_P4_table", {}).get("omr2") if r["case"] == "main" else (r.get("C02_P5_table", {}).get("omr2") if r["case"] == "heldout" else None)
        tc = r.get("C02_P4_table", {}).get("CPP") if r["case"] == "main" else None
        cpp = r.get("eps0sq_CPP_over_G")
        out.append(f"| {r['case']} | {r['gL']:.0f} | {r['eps0']} | {f(r['lambda2_over_lambda1_L2'])} | {f(tr)} | {f(r['one_minus_r2'])} | {f(to)} | "
                   f"{f(cpp) if r['case'] != 'p8' else 'n/a'} | {f(tc)} |")
    # entry-level comparison with C-02 P3 (main case): N0 Var(s_l), input and ASE parts
    out += ["", "**C-02 P3 entries (main case)**: relative deviation of $N_0\\mathrm{Var}(s_l)$ (in, ase) from the frozen table; "
            "where the table entry is 0 the simulated value is given.", "",
            "| $gL$ | $\\varepsilon_0$ | $s_0$ | $s_1$ | $s_2$ | $s_3$ | $s_4$ |", "|---|---|---|---|---|---|---|"]
    for k in sorted(R, key=lambda k: (R[k]["gL"], -R[k]["eps0"])):
        r = R[k]
        if r["case"] != "main" or "N0Var_s_in" not in r or k.startswith(("conv_", "gbw_", "core_")):
            continue
        t = r["C02_P3_table"]["s"]
        cells = []
        for l in range(5):
            parts = []
            for i, part in ((0, "in"), (1, "ase")):
                x = r["N0Var_s_" + part][l]
                parts.append(f"{x:.4f}" if t[l][i] == 0 else pct(x / t[l][i] - 1))
            cells.append(", ".join(parts))
        out.append(f"| {r['gL']:.0f} | {r['eps0']} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def shape_tables():
    S = J("2026-10-10-claude-interactive.2-shape-modes")
    out = ["| $\\varepsilon_0$ | $l$ | max rel. error of $M_l$, $\\tau\\le4$ | over $\\tau\\le6$ | det $M_l(6)$ | decay, $\\tau\\in[3,6]$ ($g$) | ang. freq. ($g$) | predicted freq. | gain exponents NLSE | ODE |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for e in sorted(S["asym"], key=float, reverse=True):
        s = S["asym"][e]
        for l in range(5):
            b = s["blocks"][str(l)] if str(l) in s["blocks"] else s["blocks"][l]
            fa = fw = "n/a"; pw = "n/a"
            if "generator_tau3to6" in b:
                gsim = b["generator_tau3to6"]["sim"]
                fa = f"{gsim['decay']:.4f}"
                fw = f"{gsim['omega']:.4f}"
                pw = f"{b['pred_omega']:.4f}"
            out.append(f"| {e} | {l} | {f(b['err_at_tau4'])} | {f(b['max_rel_err'])} | {b['det_sim_end']:.4f} | {fa} | {fw} | {pw} | "
                       f"{f(b['gain_exp_sim'], 4)} | {f(b['gain_exp_ode'], 4)} |")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["noise", "spectral", "shape"]
    for w in which:
        print(globals()[w + "_tables"]())
        print()
