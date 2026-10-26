"""Summarize results.jsonl of run 2026-10-10-claude-b.6-solver-weighted-raman into summary.json.

Usage (repository root):
  ~/agent-work/venv/bin/python runs/2026-10-10-claude-b.6-solver-weighted-raman/summarize_wr.py
"""
import datetime
import json
import os

RUN_ID = "2026-10-10-claude-b.6-solver-weighted-raman"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.expanduser("~"), "analytical-nl-discovery-data", RUN_ID)
recs = [json.loads(l) for l in open(os.path.join(RAW, "results.jsonl")) if l.strip()]
W = ("w_centroid", "w_lambda_gen_eigvec", "w_best_binary")


def s6(x):
    return None if x is None else format(x, "#.6g")


def pick(stage, key, wname, mirror):
    out = [r for r in recs if r["stage"] == stage and r["key"] == key
           and r["weight"] == wname and r["mirror"] == mirror]
    return out[-1] if out else None  # latest if a stage was repeated


def kerr_block(key):
    d = {}
    for side, mirror in (("mirror", True), ("given", False)):
        e = {}
        for w in W:
            r = pick("1_kerr", key, w, mirror)
            if r is None:
                continue
            e[w] = {"F_w": r["F_det"], "F_w_6sig": s6(r["F_det"]),
                    "Nw_mean": r["Nw_mean"], "sum_w2_nbar": r["denominator_sum_w2_nbar"]}
            if "conserved_prediction_sum_w2_nin_over_sum_w2_nout" in r:
                e[w]["conserved_prediction_same_bins"] = r["conserved_prediction_sum_w2_nin_over_sum_w2_nout"]
                e[w]["out_var_share_outside_weight_bins"] = r.get("out_var_share_outside_weight_bins")
        r = pick("1_kerr", key, "w_centroid", mirror)
        if r is not None:
            e["bandwidth_ratio_var_in_over_var_out"] = r["bw_ratio_var_in_over_out"]
            e["var_in_OmegaT0^2"] = r["bw_var_in"]
            e["var_out_OmegaT0^2"] = r["bw_var_out"]
            e["mean_in_OmegaT0"] = r["bw_mean_in"]
            e["mean_out_OmegaT0"] = r["bw_mean_out"]
            e["F_centroid_minus_ratio"] = r["F_det"] - r["bw_ratio_var_in_over_out"]
            e["F_centroid_over_ratio_minus_1"] = r["F_det"] / r["bw_ratio_var_in_over_out"] - 1
        d[side] = e
    conv = {}
    for st in ("1_conv_n2000", "1_conv_Nt1024"):
        conv[st] = {w: (pick(st, key, w, True)["F_det"] - pick("1_kerr", key, w, True)["F_det"])
                    if pick(st, key, w, True) and pick("1_kerr", key, w, True) else None for w in W}
    d["convergence_dF_mirror(vs Nt512,n4000)"] = conv
    return d


def raman_block(base, key, conv_prefix):
    d = {}
    for side, mirror in (("mirror", True), ("given", False)):
        e = {}
        for w in W:
            r = pick(base, key, w, mirror)
            if r is None:
                continue
            e[w] = {"F_det": r["F_det"], "F_det_6sig": s6(r["F_det"]),
                    "sum_w2_nbar": r["denominator_sum_w2_nbar"], "Nw_mean": r["Nw_mean"]}
            for k in ("F_R_notebook", "F_R_ssweight", "F_total_notebook", "F_total_ssweight"):
                if k in r:
                    e[w][k] = r[k]
                    e[w][k + "_6sig"] = s6(r[k])
            if "conserved_prediction_sum_w2_nin_over_sum_w2_nout" in r:
                e[w]["conserved_prediction_same_bins"] = r["conserved_prediction_sum_w2_nin_over_sum_w2_nout"]
            # dt^2 extrapolation (mirror only)
            if mirror:
                r4 = pick(conv_prefix + "_conv_Nt4096", key, w, True)
                r8 = pick(conv_prefix + "_conv_Nt8192", key, w, True)
                r2n = pick(conv_prefix + "_conv_n2000", key, w, True)
                ext = {}
                for q in ("F_det", "F_R_notebook", "F_R_ssweight", "F_total_notebook", "F_total_ssweight"):
                    if q not in r:
                        continue
                    row = {"Nt2048": r[q], "Nt4096": r4[q] if r4 else None,
                           "Nt8192": r8[q] if r8 else None,
                           "dz_n2000_minus_n4000": (r2n[q] - r[q]) if r2n else None}
                    if r4:
                        row["richardson_dt2_2048_4096"] = r4[q] + (r4[q] - r[q]) / 3
                    if r4 and r8:
                        row["richardson_dt2_4096_8192"] = r8[q] + (r8[q] - r4[q]) / 3
                        row["ratio_successive_differences"] = ((r[q] - r4[q]) / (r4[q] - r8[q])
                                                               if r4[q] != r8[q] else None)
                    best = row.get("richardson_dt2_4096_8192", row.get("richardson_dt2_2048_4096"))
                    row["dt_to_0_6sig"] = s6(best)
                    ext[q] = row
                e[w]["dt_extrapolation_and_dz"] = ext
        r = pick(base, key, "w_centroid", mirror)
        if r is not None:
            e["bandwidth_ratio_var_in_over_var_out(photon-number spectra)"] = r["bw_ratio_var_in_over_out"]
            e["var_in_OmegaT0^2"] = r["bw_var_in"]
            e["var_out_OmegaT0^2"] = r["bw_var_out"]
            e["mean_in_OmegaT0"] = r["bw_mean_in"]
            e["mean_out_OmegaT0"] = r["bw_mean_out"]
            e["diag"] = {k: v for k, v in r.items() if k.startswith("diag_")}
            e["setup"] = {k: r[k] for k in ("N_soliton", "zr", "xi_L", "T0_ps", "beta2", "gamma",
                                            "P0_W", "length_m", "omega0T0", "raman", "Nt",
                                            "dt_fs", "nsteps", "counting")}
        d[side] = e
    return d


summary = {"run_id": RUN_ID,
           "written": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "conventions": {
               "weights": "weights_for_solver.json (claude-b), bins_k in claude-b's numpy convention; "
                          "'mirror' puts w_k on solver bin -k (claude-b's bins as claude-b applies them), "
                          "'given' on solver bin +k",
               "F_w": "Var(N_w) / sum_k w_k^2 nbar_k; Var from the discrete RK4IP adjoint (input vacuum); "
                      "F_R = Raman Langevin variance (coth 300 K, trapezoid in z) / sum_k w_k^2 nbar_k",
               "bandwidth_ratio": "var_in/var_out of the photon-number spectra over the whole grid, "
                                  "Omega T0 units, each about its own photon-weighted mean",
               "case1": "Kerr only, T0 = 1 ps, beta2 = 1 ps^2/m, gamma = 1/W/m, omega0 T0 = 1e9 (s = 1e-9), Nt 512, 4000 steps",
               "case2a": "physical fibre, self-steepening suppressed (omega0 T0 = 1e6, as B_noss), no Raman, Nt 512; "
                         "photons counted uniformly at hbar*omega0(1550 nm)",
               "case2b": "physical fibre, self-steepening suppressed (omega0 T0 = 1e9), AgarwalRaman, Nt 2048; photons "
                         "counted uniformly at hbar*omega0(1550 nm) and the reservoir prefactor hbar*omega0/gamma at 1550 nm",
               "case2c": "physical fibre, self-steepening on (1550 nm), AgarwalRaman, Nt 2048; physical photon counting 1/(hbar(omega0+Omega))",
               "case3": "as 2c at N = 20, z = 0.3 z_wb, N20_zr0.3 weights",
               "F_R_variants": "notebook = noise injected as i gamma A m; ssweight = through the solver's (1+Omega/omega0)*damped_freq_window",
           }}
summary["case1_kerr"] = {k: kerr_block(k) for k in ("N10_zr0.7", "N20_zr0.3")}
summary["case1_identity_diagnostic"] = [
    {k: r[k] for k in ("stage", "key", "weight", "Nt", "nsteps", "omega0T0", "F_det",
                       "conserved_prediction", "bw_ratio_var_in_over_out",
                       "F_over_ratio_minus_1", "F_over_prediction_minus_1", "offset")}
    for r in recs if r["stage"].startswith("1_identity_")]
summary["case2a_noss_noRaman"] = raman_block("2a", "N10_zr0.7", "2a")
summary["case2b_noss_Raman"] = raman_block("2b", "N10_zr0.7", "2b")
summary["case2c_ss_Raman"] = raman_block("2c", "N10_zr0.7", "2c")
summary["case3_N20_ss_Raman"] = raman_block("3", "N20_zr0.3", "3")
summary["all_points"] = recs
with open(os.path.join(HERE, "summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
print("wrote summary.json with", len(recs), "records")
