"""Summarize results.jsonl of run 2026-10-10-claude-b.6-solver-nd-check into summary.json.

Usage (repository root):
  ~/agent-work/venv/bin/python runs/2026-10-10-claude-b.6-solver-nd-check/summarize.py
"""
import json
import os
import datetime

RUN_ID = "2026-10-10-claude-b.6-solver-nd-check"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.expanduser("~"), "analytical-nl-discovery-data", RUN_ID)
recs = [json.loads(l) for l in open(os.path.join(RAW, "results.jsonl")) if l.strip()]

FN = ("best_binary_bins", "best_interval_bins")


def sig6(x):
    """6 significant digits as a string that keeps trailing zeros."""
    return None if x is None else format(x, "#.6g")


def pick(stage, key, fname, mirror=False, label=None, Nt=None, nsteps=None,
         omega0T0=None, weights="solver"):
    out = []
    for r in recs:
        if r["stage"] != stage or r.get("key") != key or r.get("filter") != fname:
            continue
        if r.get("mirror") != mirror or r.get("weights") != weights:
            continue
        if label is not None and r["label"] != label:
            continue
        if Nt is not None and r["Nt"] != Nt:
            continue
        if nsteps is not None and r["nsteps"] != nsteps:
            continue
        if omega0T0 is not None and abs(r["omega0T0"] / omega0T0 - 1) > 1e-9:
            continue
        out.append(r)
    if not out:
        return None
    return out[-1]  # latest if repeated


def F(r):
    return None if r is None else r["F"]


def diff(a, b):
    return None if (a is None or b is None) else a - b


summary = {"run_id": RUN_ID,
           "written": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "conventions": {
               "bins": "filter bin k is Omega T0 = k 2pi/40 on the solver's centered frequency axis "
                       "(window 40 T0); Omega = omega - omega0 is the physical detuning "
                       "(solver convention A(t) = sum_k A_k exp(-i Omega_k t), positive Omega = higher "
                       "optical frequency). 'mirror' uses bins -k.",
               "F": "Var(N_T)/<N_T>, linearized vacuum noise of the coherent input; "
                    "Var = sum |dN_T/dconj(B(0))|^2 from solve_adjoint(...; adjoint_mode=:discrete_rk4ip)",
               "case_A_s_to_0": "F_s0 = mean of the filter and mirrored-filter values at omega0 T0 = 1e9 "
                                "(parity maps (T, s) to (-T, -s), so the mean is F(s=0) + O(s^2))",
           }}

# ---------------- case A ----------------
A = {}
for key in ("N10_zr0.7", "N20_zr0.3"):
    A[key] = {}
    for fname in FN:
        d = {}
        base = pick("A", key, fname, False, "A", 512, 4000, 1e6)
        basem = pick("A", key, fname, True, "A", 512, 4000, 1e6)
        d["Nmean_photons_omega0T0_1e6"] = base["Nmean"] if base else None
        d["n_bins"] = base["n_bins"] if base else None
        d["F_omega0T0_1e6"] = F(base)
        d["F_mirror_omega0T0_1e6"] = F(basem)
        ws = {}
        for w0 in (1e7, 1e8, 1e9):
            r = pick("A_w0", key, fname, False, "A", 512, 4000, w0)
            rm = pick("A_w0", key, fname, True, "A", 512, 4000, w0)
            ws[f"{w0:.0e}"] = {"F": F(r), "F_mirror": F(rm),
                               "mirror_minus_F": diff(F(rm), F(r))}
        d["omega0T0_scan"] = ws
        r9 = pick("A_w0", key, fname, False, "A", 512, 4000, 1e9)
        r9m = pick("A_w0", key, fname, True, "A", 512, 4000, 1e9)
        if r9 is not None and r9m is not None:
            Fs0 = 0.5 * (r9["F"] + r9m["F"])
            d["F_s0"] = Fs0
            d["F_s0_6sig"] = sig6(Fs0)
            d["parity_mean_omega0T0_1e6"] = (0.5 * (base["F"] + basem["F"])
                                             if base and basem else None)
        conv = {}
        for st, kw in (("A_conv_n1000", dict(nsteps=1000)), ("A_conv_n2000", dict(nsteps=2000)),
                       ("A_conv_n8000", dict(nsteps=8000)), ("A_conv_n16000", dict(nsteps=16000)),
                       ("A_conv_Nt1024", dict(Nt=1024, nsteps=4000)),
                       ("A_conv_Nt2048", dict(Nt=2048, nsteps=4000)),
                       ("A_conv_w0T0_1e7", dict(nsteps=4000))):
            Nt = kw.get("Nt", 512)
            ns = kw.get("nsteps")
            w0 = 1e7 if st.endswith("1e7") else 1e6
            r = pick(st, key, fname, False, "A", Nt, ns, w0)
            conv[st.replace("A_conv_", "")] = diff(F(r), F(base))
        d["convergence_dF_vs_production(Nt512,n4000,omega0T0=1e6)"] = conv
        A[key][fname] = d
summary["case_A"] = A

# ---------------- case B ----------------
B = {}
key = "N10_zr0.7"
for fname in FN:
    d = {}
    for lab, w, wl in (("B_ss", 512, "solver"), ("B_noss", 512, "solver"),
                       ("B_noss", 512, "physical_1550nm")):
        r = pick("B", key, fname, False, lab, w, 4000, None, wl)
        rm = pick("B", key, fname, True, lab, w, 4000, None, wl)
        name = lab + ("" if wl == "solver" else "_physical_photon_weights")
        d[name] = {"F": F(r), "F_6sig": sig6(F(r)) if r else None,
                   "F_mirror": F(rm), "F_mirror_6sig": sig6(F(rm)) if rm else None,
                   "Nmean": r["Nmean"] if r else None,
                   "Nmean_mirror": rm["Nmean"] if rm else None,
                   "omega0T0": r["omega0T0"] if r else None,
                   "diag": {k: v for k, v in r.items() if k.startswith("diag_")} if r else None}
    d["SS_effect_total(B_ss - B_noss)"] = {
        "filter": diff(d["B_ss"]["F"], d["B_noss"]["F"]),
        "mirror": diff(d["B_ss"]["F_mirror"], d["B_noss"]["F_mirror"])}
    d["photon_weight_part(B_noss_physw - B_noss)"] = {
        "filter": diff(d["B_noss_physical_photon_weights"]["F"], d["B_noss"]["F"]),
        "mirror": diff(d["B_noss_physical_photon_weights"]["F_mirror"], d["B_noss"]["F_mirror"])}
    d["SS_dynamics_part(B_ss - B_noss_physw)"] = {
        "filter": diff(d["B_ss"]["F"], d["B_noss_physical_photon_weights"]["F"]),
        "mirror": diff(d["B_ss"]["F_mirror"], d["B_noss_physical_photon_weights"]["F_mirror"])}
    base = pick("B", key, fname, False, "B_ss", 512, 4000)
    conv = {}
    for st, Nt, ns in (("B_conv_n8000", 512, 8000), ("B_conv_Nt1024", 1024, 4000),
                       ("B_conv_Nt2048", 2048, 4000)):
        r = pick(st, key, fname, False, "B_ss", Nt, ns)
        rm = pick(st, key, fname, True, "B_ss", Nt, ns)
        basem = pick("B", key, fname, True, "B_ss", 512, 4000)
        conv[st.replace("B_conv_", "")] = {"dF": diff(F(r), F(base)),
                                            "dF_mirror": diff(F(rm), F(basem))}
    d["convergence_B_ss_dF_vs_production(Nt512,n4000)"] = conv
    # consistency with case A (same dimensionless problem when SS is suppressed)
    a = pick("A", key, fname, False, "A", 512, 4000, 1e6)
    am = pick("A", key, fname, True, "A", 512, 4000, 1e6)
    d["B_noss_minus_A(omega0T0=1e6)"] = {"filter": diff(d["B_noss"]["F"], F(a)),
                                         "mirror": diff(d["B_noss"]["F_mirror"], F(am))}
    B[fname] = d
summary["case_B"] = B

# ---------------- case C ----------------
C = {}
for fname in FN:
    d = {}
    for mirror in (False, True):
        r = pick("C", key, fname, mirror, "C_ss_raman", 2048, 4000)
        if r is None:
            continue
        e = {"Nmean": r["Nmean"],
             "F_C1_input_vacuum_only": r["F"], "F_C1_6sig": sig6(r["F"]),
             "var_input_vacuum": r["var_input_vacuum"]}
        for k, v in r.items():
            if k.startswith("varR_") or k.startswith("F_total_"):
                e[k] = v
        for k, v in r.items():
            if k.startswith("varR_"):
                e[k.replace("varR_", "varR_over_N_")] = v / r["Nmean"]
        e["F_C2_coth300_notebook_trap_6sig"] = sig6(r["F_total_coth300_notebook_trap"])
        e["F_C2_coth300_ssweight_trap_6sig"] = sig6(r["F_total_coth300_ssweight_trap"])
        # reference without Raman on the same grid (B_ss at Nt = 2048)
        b = pick("B_conv_Nt2048", key, fname, mirror, "B_ss", 2048, 4000)
        e["F_noRaman_same_grid(B_ss,Nt2048)"] = F(b)
        e["deterministic_Raman_effect(F_C1 - F_noRaman)"] = diff(r["F"], F(b))
        e["diag"] = {k: v for k, v in r.items() if k.startswith("diag_")}
        e["nz_saved"] = r.get("nz_saved")
        # dt^2 (Richardson) extrapolation of the Raman-kernel sampling error
        r4 = pick("C_conv_Nt4096", key, fname, mirror, "C_ss_raman", 4096, 4000)
        r8 = pick("C_conv_Nt8192", key, fname, mirror, "C_ss_raman", 8192, 2000)
        qty = {"F_C1": lambda x: x["F"],
               "varR_over_N_coth300_notebook_trap":
                   lambda x: x["varR_coth300_notebook_trap"] / x["Nmean"],
               "varR_over_N_coth300_ssweight_trap":
                   lambda x: x["varR_coth300_ssweight_trap"] / x["Nmean"],
               "F_C2_coth300_notebook_trap": lambda x: x["F_total_coth300_notebook_trap"],
               "F_C2_coth300_ssweight_trap": lambda x: x["F_total_coth300_ssweight_trap"]}
        ext = {}
        for qn, fq in qty.items():
            v2, v4 = fq(r), (fq(r4) if r4 else None)
            v8 = fq(r8) if r8 else None
            row = {"Nt2048": v2, "Nt4096": v4, "Nt8192": v8}
            if v4 is not None:
                row["richardson_dt2_from_2048_4096"] = v4 + (v4 - v2) / 3
            if v4 is not None and v8 is not None:
                row["richardson_dt2_from_4096_8192"] = v8 + (v8 - v4) / 3
                row["ratio_(F2048-F4096)/(F4096-F8192)"] = ((v2 - v4) / (v4 - v8)
                                                          if v4 != v8 else None)
                row["best_6sig"] = sig6(row["richardson_dt2_from_4096_8192"])
            ext[qn] = row
        e["dt_extrapolation"] = ext
        conv = {}
        for st, Nt, ns in (("C_conv_n2000", 2048, 2000), ("C_conv_n8000", 2048, 8000),
                           ("C_conv_Nt1024", 1024, 4000), ("C_conv_Nt4096", 4096, 4000),
                           ("C_conv_Nt8192", 8192, 2000)):
            rc = pick(st, key, fname, mirror, "C_ss_raman", Nt, ns)
            if rc is None:
                conv[st.replace("C_conv_", "")] = None
                continue
            conv[st.replace("C_conv_", "")] = {
                "dF_C1": rc["F"] - r["F"],
                "dvarR_over_N_coth300_notebook_trap":
                    rc["varR_coth300_notebook_trap"] / rc["Nmean"]
                    - r["varR_coth300_notebook_trap"] / r["Nmean"],
                "dvarR_over_N_coth300_ssweight_trap":
                    rc["varR_coth300_ssweight_trap"] / rc["Nmean"]
                    - r["varR_coth300_ssweight_trap"] / r["Nmean"],
                "dF_C2_coth300_ssweight_trap":
                    rc["F_total_coth300_ssweight_trap"] - r["F_total_coth300_ssweight_trap"]}
        e["convergence_dF_vs_production(Nt2048,n4000)"] = conv
        d["mirror" if mirror else "filter"] = e
    C[fname] = d
summary["case_C"] = C


def g(d, *path):
    for p in path:
        if d is None:
            return None
        d = d.get(p)
    return d


head = {"note": "F to 6 significant digits; 'filter' = bins k as given (Omega = +k 2pi/40 T0, "
                "physical detuning), 'mirror' = bins -k. Full-precision values and checks below."}
head["A_Kerr_only_s0"] = {k: {f: g(A, k, f, "F_s0_6sig") for f in FN} for k in A}
head["A_at_omega0T0_1e6_filter_as_given"] = {k: {f: sig6(g(A, k, f, "F_omega0T0_1e6")) for f in FN}
                                             for k in A}
head["B_selfsteepening_on"] = {f: {"filter": g(B, f, "B_ss", "F_6sig"),
                                   "mirror": g(B, f, "B_ss", "F_mirror_6sig")} for f in FN}
head["B_selfsteepening_suppressed"] = {f: {"filter": g(B, f, "B_noss", "F_6sig"),
                                           "mirror": g(B, f, "B_noss", "F_mirror_6sig")}
                                       for f in FN}
head["B_noSS_dynamics_physical_photon_counting"] = {
    f: {"filter": g(B, f, "B_noss_physical_photon_weights", "F_6sig"),
        "mirror": g(B, f, "B_noss_physical_photon_weights", "F_mirror_6sig")} for f in FN}
for lab, q in (("C1_F_Kerr_SS_detRaman", "F_C1"),
               ("C2_varR_over_N_coth300_notebook", "varR_over_N_coth300_notebook_trap"),
               ("C2_varR_over_N_coth300_ssweight", "varR_over_N_coth300_ssweight_trap"),
               ("C2_F_total_coth300_notebook", "F_C2_coth300_notebook_trap"),
               ("C2_F_total_coth300_ssweight", "F_C2_coth300_ssweight_trap")):
    head[lab] = {}
    for f in FN:
        for side in ("filter", "mirror"):
            row = g(C, f, side, "dt_extrapolation", q)
            if row is None:
                continue
            head[lab][f"{f}/{side}"] = {
                "Nt2048": sig6(row["Nt2048"]),
                "Nt4096": sig6(row["Nt4096"]) if row.get("Nt4096") is not None else None,
                "Nt8192": sig6(row["Nt8192"]) if row.get("Nt8192") is not None else None,
                "dt_to_0": row.get("best_6sig")}
summary["headline"] = head

summary["fd_check"] = [{k: r[k] for k in ("tag", "label", "Nt", "nsteps", "omega0T0", "raman",
                                          "direction", "eps_photon", "dN_fd", "dN_adjoint",
                                          "rel_diff")}
                       for r in recs if r["stage"] == "fd_check"]
summary["all_points"] = recs

order = ["run_id", "written", "conventions", "headline", "case_A", "case_B", "case_C",
         "fd_check", "all_points"]
summary = {k: summary[k] for k in order}
with open(os.path.join(HERE, "summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
print("wrote summary.json with", len(recs), "records")
