"""Build summary.json for run 2026-10-10-claude-interactive.2-moment-noise from the raw contract.jl outputs."""
import os, glob, json, math
import numpy as np
import analyze_lib as a
import tables as tb

RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/")
HERE = os.path.dirname(os.path.abspath(__file__))


def rel(x, y):
    return float(x / y - 1) if y != 0 else None


def slope(eps, dev):
    eps = np.array(eps, float); dev = np.abs(np.array(dev, float))
    ok = dev > 0
    if ok.sum() < 2:
        return None
    return float(np.polyfit(np.log(eps[ok]), np.log(dev[ok]), 1)[0])


def main():
    runs = {}
    for p in sorted(glob.glob(RAW + "*.json")):
        if os.path.basename(p).startswith("fd_check"):
            continue
        d = a.load(p)
        key = os.path.basename(p)[:-5]
        r = dict(case=d["case"], eps0=d["eps0"], gL=d["gL"], Nt=d["Nt"], window=d["window"], nsteps=d["nsteps"],
                 delta_mode=d.get("delta_mode", "e23"), energy_err=d["energy_balance_rel_err"],
                 edge_time=d["edge_time"], edge_freq=d["edge_freq"], N0=d["N0"])
        c = a.collective(d)
        r["N0Var_Tc"] = c["VarTc"].tolist(); r["N0Var_Wc"] = c["VarWc"].tolist(); r["N0Cov"] = c["Cov"].tolist()
        r["N0Var_Tcomp"] = c["VarTcomp"].tolist(); r["Dc"] = c["Dc"]
        # R6b: adjoint vs W(z) moment formula (exact identity)
        mf = d["moment_formula"]; N0 = d["N0"]
        dev = []
        for k, kk in (("VarTc", "N0Var_Tc"), ("VarWc", "N0Var_Wc"), ("Cov", "N0Cov")):
            scale = (abs(mf[k][0]) + abs(mf[k][1])) * N0
            for i in (0, 1):
                dev.append(abs(r[kk][i] - mf[k][i] * N0) / scale)
        r["R6b_max_rel_dev_adjoint_vs_moment_formula"] = float(max(dev))  # |adjoint - formula| / (|in| + |ase|)
        U = d["gL"]; G = math.exp(U)
        if "N" in d["names"]:
            e = a.energy(d); r["energy_N0Var_over_N2"] = e.tolist(); r["energy_pred"] = [1.0, 1 - 1 / G]
            lo = a.matched_lo(d)
            r["CAA"] = lo["CAA"].tolist(); r["CAA_pred"] = [G, G - 1]
            r["eps0sq_CPP_over_G"] = (d["eps0"] ** 2 * lo["CPP"] / G).tolist() if d["eps0"] == d["eps0"] else None
            r["one_minus_r2"] = lo["one_minus_r2"]
            sp = a.spectral(d); spE = a.spectral(d, "euclid")
            r["N0Var_s_in"] = sp["var_in"].tolist(); r["N0Var_s_ase"] = sp["var_ase"].tolist()
            r["lambda2_over_lambda1_L2"] = sp["ratio"]; r["lambda2_over_lambda1_euclid"] = spE["ratio"]
            NN = a.block(d, "N", "N"); n2 = a.block(d, "n2", "n2"); WW = a.block(d, "Wc", "Wc")
            TT = a.block(d, "Tc", "Tc"); TW = a.block(d, "Tc", "Wc")
            comp = TT + 2 * c["Dc"] * TW + c["Dc"] ** 2 * WW
            sh = lambda x: float(x[0] / (x[0] + x[1]))
            r["R8_vacuum_share_nsp1"] = dict(energy=sh(NN), Wc=sh(WW), Tcomp=sh(comp), n2=sh(n2))
        if "R8_vacuum_share_nsp1" not in r:
            WW = a.block(d, "Wc", "Wc"); TT = a.block(d, "Tc", "Tc"); TW = a.block(d, "Tc", "Wc")
            comp = TT + 2 * c["Dc"] * TW + c["Dc"] ** 2 * WW
            r["R8_vacuum_share_nsp1"] = dict(Wc=float(WW[0] / WW.sum()), Tcomp=float(comp[0] / comp.sum()))
        if d["case"] == "asym":
            s = a.r7_sim(d); cf = a.r7_closed(U)
            r["R7_sim"] = {k: v.tolist() for k, v in s.items()}
            r["R7_closed"] = {k: list(v) for k, v in cf.items()}
            r["R7_rel_dev"] = {k: [rel(s[k][i], cf[k][i]) for i in (0, 1)] for k in cf}
            G3 = math.exp(-U / 3)
            comp_closed = (U * U / 9, U * U / 3 - 2 * U + 6 * (1 - G3))
            r["R8_pred_finiteG_nsp1"] = dict(energy=1 / (1 + (1 - 1 / G)), Wc=1 / (1 + 3 * (1 - G3)),
                                             Tcomp=comp_closed[0] / sum(comp_closed), asymptotic=0.25)
        if d["case"] in ("main", "heldout"):
            Ui = int(round(U))
            tab = (tb.C01_P3 if d["case"] == "main" else tb.C01_P5)[Ui]
            e0 = d["eps0"]
            sTL2 = tab["aL"] ** 2 / 5; sWL2 = tab["apL"] ** 2 / (5 * e0 * e0)
            simv = dict(VarTc=c["VarTc"] / sTL2, VarTcomp=c["VarTcomp"], VarWc=c["VarWc"] / sWL2, Cov=e0 * c["Cov"])
            r["C01_table_sim"] = {k: v.tolist() for k, v in simv.items()}
            r["C01_table"] = {k: list(tab[k]) for k in ("VarTc", "VarTcomp", "VarWc", "Cov")}
            r["C01_table_rel_dev"] = {k: [rel(simv[k][i], tab[k][i]) if tab[k][i] != 0 else None for i in (0, 1)]
                                      for k in ("VarTc", "VarTcomp", "VarWc", "Cov")}
            r["hydro_aL_apL"] = [d["hydro"]["aL"], d["hydro"]["apL"]]
            if "N" in d["names"] and d["case"] == "main":
                t3 = tb.C02_P3[Ui]; t4 = tb.C02_P4[Ui]
                r["C02_P3_table"] = dict(s=t3["s"], ratio=t3["ratio"]); r["C02_P4_table"] = dict(CPP=t4["CPP"], omr2=t4["omr2"])
            if "N" in d["names"] and d["case"] == "heldout":
                r["C02_P5_table"] = tb.C02_P5[Ui]
        runs[key] = r
    # error exponents at fixed (case, gL, quantity) over eps0
    expo = {}
    for case, dm in (("main", "e23"), ("heldout", "e23"), ("asym", "e23"), ("main", "e1"), ("asym", "e1")):
        for U in (2, 4, 6):
            sel = [(k, r) for k, r in runs.items() if r["case"] == case and abs(r["gL"] - U) < 1e-6
                   and r["delta_mode"] == dm and not k.startswith(("conv_", "gbw_", "core_"))]
            case_lbl = case if dm == "e23" else case + "-d1"
            if case == "asym":
                for q in ("VarWc", "VarTc", "VarTcomp"):
                    for i, part in ((0, "in"), (1, "ase")):
                        pts = sorted({r["eps0"]: r["R7_rel_dev"][q][i] for k, r in sel}.items())
                        if len(pts) >= 2 and all(v is not None for _, v in pts):
                            expo[f"{case_lbl}_g{U}_{q}_{part}"] = dict(eps0=[p[0] for p in pts], rel_dev=[p[1] for p in pts],
                                                                   slope=slope([p[0] for p in pts], [p[1] for p in pts]))
            else:
                for q in ("VarTc", "VarTcomp", "VarWc", "Cov"):
                    for i, part in ((0, "in"), (1, "ase")):
                        pts = sorted({r["eps0"]: r["C01_table_rel_dev"][q][i] for k, r in sel}.items())
                        if len(pts) >= 2 and all(v is not None for _, v in pts):
                            expo[f"{case_lbl}_g{U}_{q}_{part}"] = dict(eps0=[p[0] for p in pts], rel_dev=[p[1] for p in pts],
                                                                   slope=slope([p[0] for p in pts], [p[1] for p in pts]))
    # step and grid convergence: conv_* runs against their base run
    conv = {}
    for k, r in runs.items():
        if not k.startswith("conv_"):
            continue
        base = [b for bk, b in runs.items() if not bk.startswith(("conv_", "gbw_", "core_")) and b["case"] == r["case"] and b["eps0"] == r["eps0"]
                and abs(b["gL"] - r["gL"]) < 1e-6 and b["delta_mode"] == r["delta_mode"] and "N0Var_s_in" in b]
        if not base:
            continue
        b = base[0]; dev = {}
        for q in ("N0Var_Tc", "N0Var_Wc", "N0Cov", "N0Var_Tcomp", "N0Var_s_in", "N0Var_s_ase"):
            if q in r and q in b:
                x = np.array(r[q], float); y = np.array(b[q], float)
                dev[q] = float(np.max(np.abs(x - y) / np.maximum(np.abs(y), 1e-300)))
        for q in ("one_minus_r2", "lambda2_over_lambda1_L2"):
            if q in r and q in b:
                dev[q] = abs(r[q] / b[q] - 1)
        conv[k] = dict(Nt=r["Nt"], base_Nt=b["Nt"], nsteps=r["nsteps"], base_nsteps=b["nsteps"], max_rel_change=dev)
    # finite gain bandwidth (relaxed assumption): Var(Omega_c) with gain filtering vs the flat-gain base run (n_sp = 1)
    gb = {}
    for k, r in runs.items():
        if not k.startswith("gbw_"):
            continue
        base = [b for bk, b in runs.items() if not bk.startswith(("gbw_", "conv_", "core_")) and b["case"] == r["case"]
                and b["eps0"] == r["eps0"] and abs(b["gL"] - r["gL"]) < 1e-6 and b["delta_mode"] == r["delta_mode"]]
        if base:
            b = base[0]
            gb[k] = dict(VarWc_ratio_total=sum(r["N0Var_Wc"]) / sum(b["N0Var_Wc"]),
                         VarWc_ase_ratio=r["N0Var_Wc"][1] / b["N0Var_Wc"][1],
                         VarWc_in_ratio=r["N0Var_Wc"][0] / b["N0Var_Wc"][0], energy_rel_to_flat_gain=r["energy_err"],
                         VarTcomp_ratio_total=sum(r["N0Var_Tcomp"]) / sum(b["N0Var_Tcomp"]))
            for q in ("lambda2_over_lambda1_L2", "one_minus_r2"):
                if q in r and q in b:
                    gb[k][q + "_ratio"] = r[q] / b[q]
    fdp = RAW + "fd_check.json"
    fd = json.load(open(fdp)) if os.path.exists(fdp) else None
    core = {}
    for k, r in runs.items():
        if not k.startswith("core_"):
            continue
        base = [b for bk, b in runs.items() if not bk.startswith(("gbw_", "conv_", "core_")) and b["case"] == r["case"]
                and b["eps0"] == r["eps0"] and abs(b["gL"] - r["gL"]) < 1e-6 and "lambda2_over_lambda1_L2" in b]
        if base and "lambda2_over_lambda1_L2" in r:
            core[k] = dict(ratio_chirp_core=r["lambda2_over_lambda1_L2"], ratio_rms_core=base[0]["lambda2_over_lambda1_L2"])
    out = dict(adjoint_fd_check=fd, core_sensitivity=core, convergence=conv, gain_bandwidth=gb, run_id="2026-10-10-claude-interactive.2-moment-noise", runs=runs, error_exponents=expo,
               max_R6b_dev_flat_gain_no_selfsteepening=max(r["R6b_max_rel_dev_adjoint_vs_moment_formula"] for k, r in runs.items()
                                                            if not k.startswith("gbw_") and r["case"] != "p8_ss"))
    with open(os.path.join(HERE, "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    o = main()
    print("runs:", len(o["runs"]), "max R6b dev:", o["max_R6b_dev_flat_gain_no_selfsteepening"])
    for k, v in sorted(o["error_exponents"].items()):
        print("%-28s eps0=%s dev=%s slope=%s" % (k, v["eps0"], np.round(v["rel_dev"], 4), None if v["slope"] is None else round(v["slope"], 2)))
