"""Fill the {{...}} placeholders of the exploration note from the run summaries (prints the values; --write substitutes)."""
import os, sys, json, math, re
import numpy as np

RUNS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = os.path.join(os.path.dirname(RUNS), "explorations", "2026-10-10-claude-interactive.2-similariton-validation.md")


def J(run):
    return json.load(open(os.path.join(RUNS, run, "summary.json")))


def pc(x, d=1):
    return f"{100*x:.{d}f}%"


def rng(vals, d=1):
    vals = [abs(v) for v in vals if v is not None]
    return pc(max(vals), d) if vals else "n/a"


def main():
    N = J("2026-10-10-claude-interactive.2-moment-noise"); R = N["runs"]
    A = J("2026-10-10-claude-interactive.2-attraction")
    S = J("2026-10-10-claude-interactive.2-shape-modes")
    M = J("2026-10-10-claude-interactive.2-gain-noise-mc")
    v = {}
    base = {k: r for k, r in R.items() if not k.startswith(("conv_", "gbw_", "core_")) and r["delta_mode"] == "e23"}
    _full = {(r["case"], r["eps0"], r["gL"]) for k, r in base.items() if k.endswith("_all")}
    base = {k: r for k, r in base.items() if not (k.endswith("_TW") and (r["case"], r["eps0"], r["gL"]) in _full)}
    # R7
    asym = {k: r for k, r in base.items() if r["case"] == "asym"}
    e01 = [d for r in asym.values() if r["eps0"] == 0.1 for q in r["R7_rel_dev"] for d in [r["R7_rel_dev"][q][1]]]
    v["R7_ase_e01"] = rng(e01)
    emin = min(r["eps0"] for r in asym.values())
    esm = [r["R7_rel_dev"][q][1] for r in asym.values() if r["eps0"] == emin for q in r["R7_rel_dev"]]
    v["R7_ase_small"] = rng(esm) + f" ($\\varepsilon_0={emin}$)"
    _sm = {}
    for g in sorted({r["gL"] for r in asym.values() if r["gL"] <= 6}):
        e = min(r["eps0"] for r in asym.values() if r["gL"] == g)
        _sm[g] = (e, [r for r in asym.values() if r["gL"] == g and r["eps0"] == e])
    for q, key in (("VarWc", "R7_W_small"), ("VarTc", "R7_T_small"), ("VarTcomp", "R7_Tc_small")):
        v[key] = ", ".join(f"{rng([r['R7_rel_dev'][q][1] for r in rs], 2)} ($gL={g:.0f}$, $\\varepsilon_0={e}$)" for g, (e, rs) in _sm.items())
    v["R7_ase_small"] = ", ".join(f"{rng([r['R7_rel_dev'][q][1] for r in rs for q in r['R7_rel_dev']], 2)} ($gL={g:.0f}$, $\\varepsilon_0={e}$)" for g, (e, rs) in _sm.items())
    E0 = N["error_exponents"]
    sl7 = [(k, E0[k]["slope"]) for k in sorted(E0) if k.startswith("asym_g") and k.endswith("_ase") and E0[k]["slope"] is not None]
    _lab = {"VarWc": "$\\Omega_c$", "VarTc": "$T_c$", "VarTcomp": "$T_{\\rm comp}$"}
    _g = {}
    for k, x in sl7:
        _g.setdefault(k.split("_")[1][1:], []).append((k.split("_")[2], x))
    v["R7_ase_slope"] = "; ".join(f"$gL={g}$: " + ", ".join(f"{_lab[q]} {x:.2f}" for q, x in sorted(_g[g], key=lambda t: ["VarWc", "VarTc", "VarTcomp"].index(t[0])))
                                  for g in sorted(_g, key=float)) or "n/a"
    xs7 = [x for k, x in sl7]
    v["R7_slope_rng"] = f"{min(xs7):.2f} to {max(xs7):.2f}" if xs7 else "n/a"
    v["R7_slope_cmp"] = ("All are below the effective slope 1.66 of the claim's $\\varepsilon_0^2\\ln(1/\\varepsilon_0)$ over this range."
                         if xs7 and max(xs7) < 1.66 else "They are not uniformly below the effective slope 1.66 of $\\varepsilon_0^2\\ln(1/\\varepsilon_0)$.")
    def _sq(q):
        return ", ".join(f"{x:.2f} ($gL={k.split('_')[1][1:]}$)" for k, x in sl7 if k.split("_")[2] == q)
    v["R7_slope_W"] = _sq("VarWc"); v["R7_slope_T"] = _sq("VarTc"); v["R7_slope_Tcomp"] = _sq("VarTcomp")
    tl = sorted({r["eps0"]: r["R7_sim"]["VarWc"][0] - 1 for r in asym.values() if abs(r["gL"] - 4) < 1e-6}.items())
    if len(tl) >= 2:
        sl = np.polyfit(np.log([t[0] for t in tl]), np.log([abs(t[1]) for t in tl]), 1)[0]
        v["R7_tl"] = ", ".join(f"{t[1]:.4f} ($\\varepsilon_0={t[0]}$)" for t in tl[::-1]) + f"; slope {sl:.2f}"
    # C-01 tables: largest ASE deviation at the smallest eps0 run, per gL
    for case, key in (("main", "P3"), ("heldout", "P5")):
        rs = [r for r in base.values() if r["case"] == case and "C01_table_rel_dev" in r]
        parts = []
        for g in sorted({r["gL"] for r in rs}):
            e = min(r["eps0"] for r in rs if r["gL"] == g)
            devs = [r["C01_table_rel_dev"][q][1] for r in rs if r["gL"] == g and r["eps0"] == e for q in ("VarTc", "VarTcomp", "VarWc", "Cov")]
            parts.append(f"{rng(devs)} ($gL={g:.0f}$, $\\varepsilon_0={e}$)")
        v[f"{key}_ase_0025"] = ", ".join(parts) if parts else "n/a"
    E = N["error_exponents"]
    for case, key in (("main", "P3"), ("heldout", "P5")):
        sa = [E[k]["slope"] for k in E if k.startswith(case + "_g") and k.endswith("_ase") and E[k]["slope"] is not None and len(E[k]["eps0"]) >= 3]
        si = [E[k]["slope"] for k in E if k.startswith(case + "_g") and k.endswith("_in") and E[k]["slope"] is not None and len(E[k]["eps0"]) >= 3 and "VarWc" not in k]
        v[f"{key}_slopes_ase"] = f"{min(sa):.2f} to {max(sa):.2f} (median {np.median(sa):.2f})" if sa else "n/a"
        v[f"{key}_slopes_in"] = f"{min(si):.2f} to {max(si):.2f} (median {np.median(si):.2f})" if si else "n/a"
        rs = [r for r in base.values() if r["case"] == case and "C01_table_rel_dev" in r]
        parts = []
        for g in sorted({r["gL"] for r in rs}):
            e = min(r["eps0"] for r in rs if r["gL"] == g)
            devs = [r["C01_table_rel_dev"][q][0] for r in rs if r["gL"] == g and r["eps0"] == e for q in ("VarTc", "VarTcomp")]
            parts.append(f"{rng(devs)} ($gL={g:.0f}$, $\\varepsilon_0={e}$)")
        v[f"{key}_in_small"] = ", ".join(parts) if parts else "n/a"
    d1 = {k: r for k, r in R.items() if r["delta_mode"] == "e1"}
    dk = sorted(k for k in E if k.startswith("asym-d1_") and k.endswith("_ase") and E[k]["slope"] is not None and len(E[k]["eps0"]) >= 3)
    if dk:
        xs = [E[k]["slope"] for k in dk]
        v["D1_rng"] = f"{min(xs):.2f} to {max(xs):.2f}"
        for q, key in (("VarWc", "D1_W"), ("VarTc", "D1_T"), ("VarTcomp", "D1_Tc")):
            v[key] = ", ".join(f"{E[k]['slope']:.2f} ($gL={k.split('_')[1][1:]}$)" for k in dk if k.split("_")[2] == q)
    else:
        v["D1_rng"] = v["D1_W"] = v["D1_T"] = v["D1_Tc"] = "n/a"
    mk = sorted(k for k in E if k.startswith("main-d1_") and E[k]["slope"] is not None and len(E[k]["eps0"]) >= 3)
    if mk:
        xs = [E[k]["slope"] for k in mk]
        v["D1_main_rng"] = f"{min(xs):.2f} to {max(xs):.2f}"
        k = "main-d1_g4_VarTc_in"
        v["D1_main_tc01"] = (f"{100*E[k]['rel_dev'][E[k]['eps0'].index(0.1)]:+.1f}%" if k in E and 0.1 in E[k]["eps0"] else "n/a")
    else:
        v["D1_main_rng"] = v["D1_main_tc01"] = "n/a"
    if d1:
        parts = []
        for key, lab in (("main-d1_g4_VarTcomp_in", "main case, $gL=4$, $\\mathrm{Var}(T_{\\rm comp})$ input part"),
                         ("main-d1_g4_VarTc_in", "main case, $gL=4$, $\\mathrm{Var}(T_c)$ input part"),
                         ("asym-d1_g2_VarWc_ase", "asymptotic seed, $gL=2$, $\\Omega_c$ ASE part"),
                         ("asym-d1_g2_VarTcomp_ase", "asymptotic seed, $gL=2$, $T_{\\rm comp}$ ASE part"),
                         ("asym-d1_g4_VarWc_ase", "asymptotic seed, $gL=4$, $\\Omega_c$ ASE part"),
                         ("asym-d1_g4_VarTcomp_ase", "asymptotic seed, $gL=4$, $T_{\\rm comp}$ ASE part")):
            if key in E and E[key]["slope"] is not None:
                parts.append(f"{lab}: deviations {', '.join(f'{100*x:+.2f}%' for x in E[key]['rel_dev'])} at $\\varepsilon_0$ = "
                             f"{', '.join(str(e) for e in E[key]['eps0'])}, slope {E[key]['slope']:.2f}")
        v["D1_result"] = "; ".join(parts) if parts else "not available"
    else:
        v["D1_result"] = "not completed in the session"
    # R8
    W = sorted((r["gL"], r["eps0"], r["R8_vacuum_share_nsp1"]["Wc"], r["R8_pred_finiteG_nsp1"]["Wc"]) for r in asym.values())
    T = sorted((r["gL"], r["eps0"], r["R8_vacuum_share_nsp1"]["Tcomp"], r["R8_pred_finiteG_nsp1"]["Tcomp"]) for r in asym.values())
    v["R8_W"] = "; ".join(f"$gL={g:.0f}$, $\\varepsilon_0={e}$: {s:.3f} (closed form {p:.3f})" for g, e, s, p in W if e == min(x[1] for x in W if x[0] == g))
    v["R8_T"] = "; ".join(f"$gL={g:.0f}$: {s:.3f} (closed form {p:.3f})" for g, e, s, p in T if e == min(x[1] for x in T if x[0] == g))
    n2 = sorted((r["gL"], r["eps0"], r["R8_vacuum_share_nsp1"].get("n2")) for r in asym.values() if "n2" in r["R8_vacuum_share_nsp1"])
    v["R8_n2"] = ", ".join(f"{s:.2f} ($gL={g:.0f}$, $\\varepsilon_0={e}$)" for g, e, s in n2)
    # R9/R10
    a9 = sorted((r["gL"], r["lambda2_over_lambda1_L2"]) for r in asym.values() if r["eps0"] == 0.1 and "lambda2_over_lambda1_L2" in r)
    v["R9_asym"] = ", ".join(f"{x:.3g}" for g, x in a9)
    a10 = sorted((r["gL"], r["one_minus_r2"]) for r in asym.values() if r["eps0"] == 0.1 and "one_minus_r2" in r)
    v["R10_asym"] = ", ".join(f"{x:.3g}" for g, x in a10)
    rows = sorted((r["gL"], np.array(r["N0Var_s_in"]) + np.array(r["N0Var_s_ase"])) for r in asym.values() if r["eps0"] == 0.1 and "N0Var_s_in" in r)
    if len(rows) >= 3:
        U = np.array([x[0] for x in rows]); Rr = np.array([x[1][1:] / x[1][0] for x in rows]); sel = U >= 4
        v["R9_ratios"] = ", ".join(f"$l={l+1}$: {np.polyfit(U[sel], np.log(Rr[sel, l]), 1)[0]:.2f}" for l in range(4))
    m2 = sorted((r["eps0"], r["lambda2_over_lambda1_L2"]) for r in base.values() if r["case"] == "main" and abs(r["gL"] - 2) < 1e-6 and "lambda2_over_lambda1_L2" in r)
    cs = N.get("core_sensitivity", {})
    v["R9_core"] = ("; ".join(f"{k.split('_e')[0].replace('core_', '')}, $gL=2$, $\\varepsilon_0=0.05$: {d['ratio_chirp_core']:.3f} (rms-edge core {d['ratio_rms_core']:.3f})"
                              for k, d in sorted(cs.items())) or "not completed")
    if cs:
        mxc = max(abs(d["ratio_chirp_core"] / d["ratio_rms_core"] - 1) for d in cs.values())
        v["R9_core_concl"] = (f"Moving the cut changes the ratio by at most {pc(mxc)}, so the cut does not explain the gap." if mxc < 0.05 else
                              f"Moving the cut changes the ratio by up to {pc(mxc)}; the $gL=2$ comparison is sensitive to the cut.")
    else:
        v["R9_core_concl"] = ""
    h2 = sorted((r["eps0"], r["lambda2_over_lambda1_L2"]) for r in base.values() if r["case"] == "heldout" and abs(r["gL"] - 2) < 1e-6 and "lambda2_over_lambda1_L2" in r)
    v["R9_g2"] = ("At $gL=2$ the main-case ratio is " + ", ".join(f"{x:.3f} ($\\varepsilon_0={e}$)" for e, x in m2[::-1]) + " against 0.987. "
                  "The held-out (C-02 P5) $gL=2$ ratio is " + ", ".join(f"{x:.3f} ($\\varepsilon_0={e}$)" for e, x in h2[::-1]) + " against 0.4257.")
    # main case, gL = 2: convergence of lambda2/lambda1 and of the N0 Var(s_l) entries toward C-02 P3
    g2r = sorted(((r["eps0"], r) for r in base.values() if r["case"] == "main" and abs(r["gL"] - 2) < 1e-6 and "N0Var_s_in" in r), key=lambda t: t[0])
    if len(g2r) >= 2:
        es2 = [e for e, _ in g2r]; tab = g2r[0][1]["C02_P3_table"]
        dr = [r["lambda2_over_lambda1_L2"] / tab["ratio"] - 1 for _, r in g2r]
        slr = float(np.polyfit(np.log(es2), np.log(np.abs(dr)), 1)[0])
        ent = []
        for l in range(5):
            for i, part in ((0, "in"), (1, "ase")):
                t = tab["s"][l][i]
                if t == 0:
                    continue
                d = [r["N0Var_s_" + part][l] / t - 1 for _, r in g2r]
                ent.append((l, part, d, float(np.polyfit(np.log(es2), np.log(np.abs(d)), 1)[0])))
        worst = max(ent, key=lambda x: abs(x[2][0]))
        v["R9_g2_detail"] = (f"$\\lambda_2/\\lambda_1$ deviates by " + ", ".join(f"{100*x:+.1f}%" for x in dr) + f" at $\\varepsilon_0$ = "
                             + ", ".join(str(e) for e in es2) + f" (slope {slr:.2f}). The 9 nonzero $N_0\\mathrm{{Var}}(s_l)$ entries deviate by at most "
                             f"{100*abs(worst[2][0]):.0f}% at $\\varepsilon_0={es2[0]}$ ($s_{worst[0]}$, {worst[1]}), with slopes {min(x[3] for x in ent):.2f} to {max(x[3] for x in ent):.2f}")
        v["R9_g2_lam"] = f"{100*dr[0]:+.1f}% at $\\varepsilon_0={es2[0]}$, slope {slr:.2f}"
        v["R9_g2_maxent"] = f"{100*abs(worst[2][0]):.0f}%"
    if len(h2) >= 2:
        hd = [x / 0.4257 - 1 for e, x in h2[::-1]]
        v["R9_h2_dev"] = ", ".join(f"{100*x:+.1f}%" for x in hd) + " at $\\varepsilon_0$ = " + ", ".join(str(e) for e, x in h2[::-1])
        e_hi, e_lo = h2[-1][0], h2[0][0]
        v["R9_h2_exp"] = (f"{math.log(abs(hd[0]) / abs(hd[-1])) / math.log(e_hi / e_lo):.2f} over a factor {e_hi / e_lo:.0f} in $\\varepsilon_0$")
    # C-02 P3 entries at the smallest eps0 run per gL: entries off by more than 10%
    mrs = [r for r in base.values() if r["case"] == "main" and "N0Var_s_in" in r]
    parts = []
    for g in sorted({r["gL"] for r in mrs}):
        e = min(r["eps0"] for r in mrs if r["gL"] == g)
        r = [x for x in mrs if x["gL"] == g and x["eps0"] == e][0]
        t = r["C02_P3_table"]["s"]
        bad = [f"$s_{l}$ {part} {100*(r['N0Var_s_' + part][l]/t[l][i]-1):+.0f}%" for l in range(5) for i, part in ((0, "in"), (1, "ase"))
               if t[l][i] != 0 and abs(r["N0Var_s_" + part][l] / t[l][i] - 1) > 0.10]
        parts.append(f"$gL={g:.0f}$, $\\varepsilon_0={e}$: " + (", ".join(bad) if bad else "none"))
    v["P3_entries_bad"] = "; ".join(parts)
    lam = []
    for case, tk in (("main", "C02_P3_table"), ("heldout", "C02_P5_table")):
        rs = [r for r in base.values() if r["case"] == case and "lambda2_over_lambda1_L2" in r]
        pp = []
        for g in sorted({r["gL"] for r in rs}):
            e = min(r["eps0"] for r in rs if r["gL"] == g)
            r = [x for x in rs if x["gL"] == g and x["eps0"] == e][0]
            pp.append(f"{100*(r['lambda2_over_lambda1_L2']/r[tk]['ratio']-1):+.1f}% ($gL={g:.0f}$, $\\varepsilon_0={e}$)")
        lam.append(("main" if case == "main" else "held out") + ": " + ", ".join(pp))
    v["R9_lam_small"] = "; ".join(lam)
    om = sorted((r["gL"], r["eps0"], r["one_minus_r2"], r["C02_P4_table"]["omr2"]) for r in base.values() if r["case"] == "main" and "one_minus_r2" in r)
    _om = {}
    for g, e, x, t in om:
        if g not in _om or e < _om[g][0]:
            _om[g] = (e, x, t)
    v["R10_omr2_short"] = ", ".join(f"{100*(x/t-1):+.1f}% ($gL={g:.0f}$, $\\varepsilon_0={e}$)" for g, (e, x, t) in sorted(_om.items()))
    v["R10_omr2"] = "; ".join(f"$gL={g:.0f}$, $\\varepsilon_0={e}$: {x:.4g} (table {t:.4g}, {pc(x/t-1)})" for g, e, x, t in om)
    # R1
    r1 = A["R1_runs"]
    for e, key in ((0.1, "R1_err01"), (0.05, "R1_err005"), (0.025, "R1_err0025")):
        xs = [r["err_s_rel"] for r in r1 if r["eps0"] == e]
        v[key] = ((f"{min(xs):.1e} to {max(xs):.1e} ({len(xs)} launches)" if len(xs) > 1 else f"{xs[0]:.1e} (1 launch)") if xs else "not run")
    from collections import Counter
    cnt = Counter(r["eps0"] for r in r1)
    v["R1_cov"] = ", ".join(f"{n} at {e}" for e, n in sorted(cnt.items(), reverse=True))
    sl = [x["slope_s"] for x in A["R1_error_exponents"].values() if x["slope_s"] is not None]
    v["R1_slopes"] = f"{min(sl):.2f} to {max(sl):.2f} (median {np.median(sl):.2f})" if sl else "n/a"
    ch = {e: [r["err_chirp_rel"] for r in r1 if r["eps0"] == e] for e in (0.1, 0.05, 0.025, 0.0125)}
    v["R1_chirp"] = ", ".join(f"max {max(x):.1e} at $\\varepsilon_0={e}$" for e, x in ch.items() if x)
    lg = A.get("R1_long", {})
    if lg:
        v["R1_long"] = ("Runs to $gL=10$ ($\\varepsilon_0=0.1$): " + "; ".join(
            f"{k.split('_G')[1].replace('_g10','')}: $s$ = " + ", ".join(f"{x:.3f}" for x in d["s"]) + f" at $\\tau$ = 0, 2, ..., 10 (ODE end {d['s_ode'][-1]:.3f})"
            for k, d in lg.items()) + ".")
    else:
        v["R1_long"] = ""
    # R3, R4
    r3 = A["R3"]
    # shape-mode reference runs (asymptotic seed, eta = 1e-4) give the same moments; used for the slopes of eps_eff and the TL share
    import glob as _g
    sref = {}
    for pth in _g.glob(os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_asym_e*_eta1e-4.json")):
        d = json.load(open(pth)); rf = d["ref"]; tau = np.array(rf["tau"])
        vT, vW, cv, E = (np.array(rf[k]) for k in ("varT", "varW", "cov", "E"))
        f = 1 - cv ** 2 / (vT * vW); Tp = np.sqrt(5 * vT); pk = 3 * E / (4 * Tp)
        ee = np.sqrt(d["params"]["b2"] / (d["params"]["gam"] * pk * Tp ** 2)); sel = tau >= 2
        sref[d["eps0"]] = dict(slope_ftl=float(np.polyfit(tau[sel], np.log(f[sel]), 1)[0]),
                               slope_eeff=float(np.polyfit(tau[sel], np.log(ee[sel]), 1)[0]),
                               growth=float((f[-1] / ee[-1] ** 2) / (f[int(np.argmin(np.abs(tau - 2)))] / ee[int(np.argmin(np.abs(tau - 2)))] ** 2)))
    if sref:
        v["R3_ftl_ref"] = ", ".join(f"{d['slope_ftl']:.2f} ($\\varepsilon_0={e}$)" for e, d in sorted(sref.items(), reverse=True))
        v["R3_eeff_ref"] = ", ".join(f"{d['slope_eeff']:.3f} ($\\varepsilon_0={e}$)" for e, d in sorted(sref.items(), reverse=True))
        v["R3_growth"] = ", ".join(f"{d['growth']:.1f} ($\\varepsilon_0={e}$)" for e, d in sorted(sref.items(), reverse=True))
    if not r3 and sref:
        v["R3_eeff"] = v["R3_eeff_ref"]; v["R3_ftl"] = v["R3_ftl_ref"]; v["R3_edge"] = "not measured (attraction runs on the asymptotic seed not completed)"
    if sref:
        v["R3_eeff"] = v["R3_eeff_ref"]; v["R3_ftl"] = v["R3_ftl_ref"]
    if r3:
        if not sref:
            v["R3_eeff"] = ", ".join(f"{d['slope_eeff']:.3f} ($\\varepsilon_0={e}$)" for e, d in sorted(r3.items(), key=lambda t: -float(t[0])))
            v["R3_ftl"] = ", ".join(f"{d['slope_ftl']:.2f} ($\\varepsilon_0={e}$)" for e, d in sorted(r3.items(), key=lambda t: -float(t[0])))
        v["R3_edge"] = ", ".join(f"{d['slope_edge']:.2f} ($\\varepsilon_0={e}$)" for e, d in sorted(r3.items(), key=lambda t: -float(t[0])))
        emin3 = min(r3, key=float)
        v["R3_edge_dev"] = f"{100*abs(r3[emin3]['slope_edge']/(-4/9)-1):.0f}%"
        v["R3_edge_emin"] = str(emin3)
    r4 = A["R4"]
    if r4:
        emn = min(r4, key=float)
        d = r4[emn]
        v["R4_tau6"] = (f"$(d\\ln T_p,\\,d\\ln P_{{\\rm pk}},\\,d\\ln\\sigma_\\omega,\\,d\\ln\\kappa)/d\\ln E_0$ = "
                        f"({d['dlnTp'][-1]:.3f}, {d['dlnPk'][-1]:.3f}, {d['dlnBW'][-1]:.3f}, {d['dlnChirp'][-1]:.3f}) at $\\varepsilon_0={emn}$")
        v["R4_asym"] = "; ".join(f"$\\varepsilon_0={e}$: ({x['asymptote_fit']['dlnTp']:.3f}, {x['asymptote_fit']['dlnPk']:.3f}, "
                                 f"{x['asymptote_fit']['dlnBW']:.3f}, {x['asymptote_fit']['dlnChirp']:.4f})"
                                 for e, x in sorted(r4.items(), key=lambda t: -float(t[0])))
        v["R4_chirp"] = ", ".join(f"{abs(x['chirp_over_g3b2'][-1]-1):.1e} ($\\varepsilon_0={e}$)" for e, x in sorted(r4.items(), key=lambda t: -float(t[0])))
    # R2/R5 smallest eps0
    es = sorted(S["asym"], key=float)
    if es:
        e = es[0]; b = S["asym"][e]["blocks"]
        g = lambda l: b[str(l)]["generator_tau3to6"]["sim"] if str(l) in b else b[l]["generator_tau3to6"]["sim"]
        v["R2_smallest"] = (f"At $\\varepsilon_0={e}$ (window $\\tau\\in[3,{S['asym'][e]['tau_end']:.0f}]$): decays "
                            + ", ".join(f"{g(l)['decay']:.4f}" for l in (2, 3, 4)) + "; frequencies "
                            + ", ".join(f"{g(l)['omega']:.4f}" for l in (2, 3, 4)) + ".")
        def _re(ee, ls=(2, 3, 4)):
            return max(max(abs(x) for x in S["asym"][ee]["blocks"][str(l)]["generator_tau3to6"]["sim"]["eig"][:2]) for l in ls)
        v["GEN_RE"] = ", ".join(f"{_re(ee):.1e} ($\\varepsilon_0={ee}$)" for ee in sorted(S["asym"], key=lambda t: -float(t)))
        small = [ee for ee in S["asym"] if float(ee) <= 0.05]
        v["GEN_RE_SMALL"] = f"{max(_re(ee) for ee in small):.1e}" if small else "n/a"
        v["GEN_RE_PCT"] = f"{100*3*max(_re(ee) for ee in small):.2f}%" if small else "n/a"
        mx = {ee: S["asym"][ee]["mixing_max"] for ee in S["asym"]}
        v["R2_mixing"] = ", ".join(f"{pc(m)} ($\\varepsilon_0={ee}$)" for ee, m in sorted(mx.items(), key=lambda t: -float(t[0])))
        dets = {ee: [S["asym"][ee]["blocks"][str(l)]["det_sim_end"] for l in (2, 3, 4)] for ee in S["asym"]}
        v["R5_det"] = "Across $\\varepsilon_0$: " + "; ".join(f"{ee}: " + ", ".join(f"{x:.4f}" for x in dd) for ee, dd in sorted(dets.items(), key=lambda t: -float(t[0]))) + " ($l=2,3,4$)."
    # convergence
    C = N.get("convergence", {})
    for k, key in (("conv_main_e0.05_g4_all_n2", "CONV_n2"), ("conv_main_e0.05_g4_all_grid1.5", "CONV_grid")):
        if k in C:
            mxv = max(C[k]["max_rel_change"].values())
            v[key] = f"{mxv:.1e} (largest over the covariance entries, $\\lambda_2/\\lambda_1$ and $1-r^2$)"
        else:
            v[key] = "not completed"
    sc = S.get("convergence", {})
    if sc:
        k = list(sc)[0]
        base_e = str(sc[k]["eps0"])
        bb = S["asym"].get(base_e)
        if bb:
            dd = max(float(np.linalg.norm(np.array(sc[k]["blocks"][str(l)]["M_sim_end"]) - np.array(bb["blocks"][str(l)]["M_sim_end"])) /
                           np.linalg.norm(np.array(bb["blocks"][str(l)]["M_sim_end"]))) for l in range(5))
            v["CONV_sm"] = f"doubling the steps changes the block maps by at most {dd:.1e} (asymptotic seed, $\\varepsilon_0={base_e}$, $gL=6$)"
    else:
        v["CONV_sm"] = "the step-doubling run was not completed in the session"
    # gain bandwidth
    gb = N.get("gain_bandwidth", {})
    if gb:
        parts = []
        for k, d in sorted(gb.items()):
            t = (f"$gL(\\omega_{{\\rm edge}}/\\Omega_g)^2={k.split('_b')[-1]}$: $\\mathrm{{Var}}(\\Omega_c)$ ratio {d['VarWc_ratio_total']:.4f}, "
                 f"$\\mathrm{{Var}}(T_{{\\rm comp}})$ ratio {d['VarTcomp_ratio_total']:.4f}")
            if "lambda2_over_lambda1_L2_ratio" in d:
                t += f", $\\lambda_2/\\lambda_1$ ratio {d['lambda2_over_lambda1_L2_ratio']:.3f}, $1-r^2$ ratio {d['one_minus_r2_ratio']:.3f}"
            parts.append(t)
        v["GBW_full"] = ("Parabolic gain $g(1-\\omega^2/\\Omega_g^2)$ on the asymptotic seed ($\\varepsilon_0=0.1$, $gL=6$, $n_{sp}=1$, noise weight $\\lvert g(\\omega)\\rvert$), relative to flat gain: "
                         + "; ".join(parts) + ". C-01's regime statement says gain filtering at the bound 0.05 damps the centre-frequency noise by roughly 10%; "
                         "the claim's own drift formula integrated on the asymptote gives about 0.9%.")
        b5 = [d for k, d in gb.items() if k.endswith("b0.05")]
        if b5:
            d = b5[0]
            v["GBW_pct"] = pc(1 - d["VarWc_ratio_total"])
            v["GBW_full"] += (f" At the bound the full NLSE reduces $\\mathrm{{Var}}(\\Omega_c)$ by {pc(1-d['VarWc_ratio_total'])} "
                              f"(input part {pc(1-d['VarWc_in_ratio'])}, ASE part {pc(1-d['VarWc_ase_ratio'])}); the output energy is {pc(-d['energy_rel_to_flat_gain'], 2)} below the flat-gain value. "
                              + ("This is the size of the drift estimate, about an order of magnitude below \"roughly 10%\"; the claim's gain-flatness bound is conservative."
                                 if 1 - d["VarWc_ratio_total"] < 0.03 else "This is closer to the claim's estimate than to the drift formula."))
        v["GBW"] = "parabolic gain at the claim's bound, asymptotic seed at $\\varepsilon_0=0.1$, $gL=6$"
        b5 = [d for k, d in gb.items() if k.endswith("b0.05")]
        v["GBW_short"] = (f"at the claim's bound ($gL(\\omega_{{\\rm edge}}/\\Omega_g)^2=0.05$, asymptotic seed, $\\varepsilon_0=0.1$, $gL=6$), $\\mathrm{{Var}}(\\Omega_c)$ falls by "
                          f"{pc(1-b5[0]['VarWc_ratio_total'])} relative to flat gain (claim: roughly 10%; the claim's own drift formula gives about 0.9%)") if b5 else "not completed"
    else:
        v["GBW_full"] = "not completed"; v["GBW"] = "not completed"; v["GBW_short"] = "not completed"
    # numpy cross-check
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("xc", os.path.join(RUNS, "2026-10-10-claude-interactive.2-shape-modes", "xcheck_compare.py"))
        xc = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.join(RUNS, "2026-10-10-claude-interactive.2-shape-modes")); spec.loader.exec_module(xc)
        x = xc.main()
        if x:
            n = max(x, key=int); d = x[n]
            v["XCHECK"] = (f"rms width, bandwidth and $T$-$\\omega$ covariance at all 61 planes within {d['varT_max_rel_diff']:.1e}, {d['varW_max_rel_diff']:.1e} and "
                           f"{d['cov_max_rel_diff']:.1e}, and the $l=2$ block map within {d['M2_max_rel_diff']:.1e} ({n} steps)")
        else:
            v["XCHECK"] = "not completed"
    except Exception as ex:
        v["XCHECK"] = f"not completed ({ex})"
    # shape-mode exponents and C-02 P1 (main case)
    ex = S.get("block_error_exponents_tau4", {})
    v["SM_slopes"] = ", ".join(f"$l={k[1:]}$: {x['slope']:.2f} (errors {', '.join(f'{e:.1e}' for e in x['err'][::-1])} at $\\varepsilon_0$ = {', '.join(str(e) for e in x['eps0'][::-1])})"
                               for k, x in sorted(ex.items()) if x["slope"] is not None) or "n/a"
    p1 = S.get("C02_P1_comparison", {})
    if p1:
        parts = []
        for e in sorted(p1, key=float, reverse=True):
            rows = p1[e]
            parts.append(f"$\\varepsilon_0={e}$: " + ", ".join(f"{k.replace('_', ' ')} {pc(x['rel_err'])}" for k, x in rows.items()))
        v["P1_main"] = "relative (Frobenius) deviation from the frozen matrices: " + "; ".join(parts)
        es1 = sorted(p1, key=float)
        v["P1_max"] = ", ".join(f"{pc(max(x['rel_err'] for x in p1[e].values()))} at $\\varepsilon_0={e}$" for e in es1[::-1])
        if len(es1) >= 2:
            sl1 = [float(np.polyfit(np.log([float(e) for e in es1]), np.log([p1[e][k]["rel_err"] for e in es1]), 1)[0]) for k in p1[es1[0]]]
            v["P1_slopes"] = f"{min(sl1):.2f} to {max(sl1):.2f}"
        else:
            v["P1_slopes"] = "n/a (one $\\varepsilon_0$)"
    else:
        v["P1_main"] = "not completed"
    ho = [(r["gL"], r["eps0"], r["N0Var_s_in"][0], r["N0Var_s_ase"][0], r["N0Var_s_in"][2], r["N0Var_s_ase"][2], r["lambda2_over_lambda1_L2"], r["one_minus_r2"], r["C02_P5_table"])
          for r in base.values() if r["case"] == "heldout" and "N0Var_s_in" in r]
    v["P5_c02"] = "; ".join(f"$gL={g:.0f}$, $\\varepsilon_0={e}$: $\\lambda_2/\\lambda_1$ {rt:.3f} (table {t['ratio']}), $1-r^2$ {om:.4g} (table {t['omr2']}), $s_0$ ({a:.3f}, {b:.3f}) (table {tuple(t['s0'])})"
                        for g, e, a, b, c2, d2, rt, om, t in sorted(ho))
    _em = min([r["eps0"] for r in R.values() if r["case"] in ("main", "heldout", "asym")] + [r["eps0"] for r in A["R1_runs"]] + [float(e) for e in S["asym"]])
    _gm = sorted({r["gL"] for r in R.values() if r["case"] in ("main", "heldout", "asym") and r["eps0"] == _em})
    _am = any(r["eps0"] == _em for r in A["R1_runs"])
    v["EPS_MIN"] = (f"{_em}" + (f" (noise runs at $gL$ = {', '.join(f'{g:.0f}' for g in _gm)} only" + ("; one attraction launch)" if _am else ")") if _em < 0.025 else ""))
    def sci(x):
        e = int(math.floor(math.log10(x))); return f"{x/10**e:.1f}\\times10^{{{e}}}"
    allr = [r for k, r in R.items() if not k.startswith("gbw_")]
    allr_att = A["R1_runs"]
    v["EDGE_T"] = sci(max([r["edge_time"] for r in allr] + [r["edge_t"] for r in allr_att] + [1e-300]))
    v["EDGE_W"] = sci(max([r["edge_freq"] for r in allr] + [r["edge_w"] for r in allr_att] + [1e-300]))
    en = [abs(r["energy_err"]) for k, r in R.items() if not k.startswith("gbw_") and not (r["case"] == "asym" and abs(r["gL"] - 8) < 1e-6)]
    v["ENERGY_MAX"] = sci(max(en + [abs(r["energy_err"]) for r in allr_att]))
    m6 = N["max_R6b_dev_flat_gain_no_selfsteepening"]
    ex6 = int(math.floor(math.log10(m6))); v["R6B_MAX"] = f"{m6/10**ex6:.1f}\\times10^{{{ex6}}}"
    fd = N.get("adjoint_fd_check")
    v["FD"] = (f"{max(max(x) for x in fd.values()):.1e} or better (relative)" if fd else "not completed")
    # Monte Carlo markers
    c = M["cases"]
    jf = M["joint_fit_scale_factors"]
    v["MC_b"] = (f"{jf['VarTc']['b_ase']:.3f} $\\pm$ {jf['VarTc']['b_err']:.3f} ($T_c$), {jf['VarWc']['b_ase']:.3f} $\\pm$ {jf['VarWc']['b_err']:.3f} ($\\Omega_c$)")
    v["MC_chi"] = f"{jf['VarWc']['chi2']:.1f} for {jf['VarWc']['dof']} degrees of freedom"
    def rr(x):
        return f"{x['ratio']:.3f} $\\pm$ {x['ratio_err']:.3f}"
    mcf = []
    for k in ("kerr_ns0.5", "kerr_ns1.0"):
        if k in c:
            mcf.append(f"$n_s={c[k]['n_s']}$ ($n_{{sp}}={c[k]['n_sp']}$, {c[k]['ntraj']} trajectories): $N_0\\mathrm{{Var}}(N)/\\langle N\\rangle^2$ = "
                       f"{c[k]['F'][0]:.3f} $\\pm$ {c[k]['F'][1]:.3f} against {c[k]['F_pred_exact']:.4f}")
    v["MARK:MCF"] = "; ".join(mcf)
    rows = ["", "| case | trajectories | energy (exact law) | Var $T_c$ | Var $\\Omega_c$ | Cov |", "|---|---|---|---|---|---|"]
    for k in ("kerr_ns0.5", "kerr_ns1.0", "kerr_vac", "kerr_ase"):
        if k in c:
            x = c[k]
            rows.append(f"| {k} | {x['ntraj']} | {x['F_ratio']:.3f} $\\pm$ {x['F_ratio_err']:.3f} | {rr(x['VarTc'])} | {rr(x['VarWc'])} | {rr(x['CovTW'])} |")
    v["MARK:MCTAB"] = "\n".join(rows) + "\n"
    sp = [f"{k}: energy {c[k]['F_ratio']:.3f} $\\pm$ {c[k]['F_ratio_err']:.3f}, Var $\\Omega_c$ {rr(c[k]['VarWc'])}" for k in ("kerr_vac", "kerr_ase") if k in c]
    v["MARK:MCSPLIT"] = "; ".join(sp) + " (ratios to the adjoint's separate input and ASE parts)."
    return v


if __name__ == "__main__":
    v = main()
    for k, x in v.items():
        print(k, "=>", x)
    if "--write" in sys.argv:
        LOG = os.path.join(os.path.dirname(RUNS), "log", "2026-10-10_claude-interactive.2_T-20261010-claude-interactive.2-01.md")
        for path in (NOTE, LOG):
            s = open(path).read()
            for k, x in v.items():
                if k.startswith("MARK:"):
                    s = s.replace("<!-- " + k[5:] + " -->", x)
                else:
                    s = s.replace("{{" + k + "}}", x)
            open(path, "w").write(s)
            print(os.path.basename(path), "remaining:", sorted(set(re.findall(r"{{([A-Za-z0-9_]+)}}", s))))
