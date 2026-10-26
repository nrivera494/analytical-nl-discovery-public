"""Collect the numbers quoted in the audit report into summary.json (claude-interactive.13)."""
import json
L = lambda f: json.load(open(f))
red = L("reduced_summary.json")["cases"]; sl = L("slopes_summary.json")["cases"]; ex = L("explicit_summary.json")
cu = L("curve_summary.json"); ed = L("eps_delta_summary.json"); bc = L("boundary_curvature.json"); cm = L("commutator_summary.json"); ft = L("ff_tests.json")
S = {"run_id": "2026-10-19-claude-interactive.13-similariton-lo-verification", "claim": "C-20261019-pi-chatgpt-02"}
S["i_reduced"] = {c: {n: {k: red[c][n][k] for k in ("power_ls_12_26", "power_ls_26_40", "power_ls_40_60", "power_equal_phase_12_26",
                                                   "power_equal_phase_40_80", "local_power_range_12_26", "ratio_i_at", "ratio_i_range_12_26",
                                                   "ratio_i_range_40_80", "CAA_exact_check_maxrelerr", "e2CPP_at", "PhiNL2_eps005_at")}
                      | {"ratio_err_exponent_vs_G": red[c][n]["ratio_err_envelope"]["fitted_exponent_vs_G"]}
                      for n in ("nsp1", "nsp2")} for c in red}
S["iii_reduced"] = {c: {n: {k: red[c][n][k] for k in ("Gm13_lam_lead_range_12_26", "Gm13_lam_lead_range_26_80", "Gm13_lam_eps005_range_12_26",
                                                     "lam_lead_at", "one_m_r2_at", "one_m_r2_power_ls_12_26")} for n in ("nsp1", "nsp2")} for c in red}
S["ii_slopes"] = {k: {"kappa": v["kappa"], "threshold_gammaP0_over_g": v["threshold_gammaP0_over_g_smoothed"], "root_R": v["root_R"],
                      "slope_at_R1": v["slope_at_R1"], "max_abs_slope_err": v["max_abs_slope_err"],
                      "max_comm_err": max(r["max_comm_err"] for r in v["rows"])} for k, v in sl.items()}
S["ii_smoothing_limit"] = {"kappa_and_thresholds": ex["smoothing_limit"], "exponent_of_0.8_minus_kappa_vs_delta": ex["smoothing_limit_exponent"],
                           "delta0.01_nsp2_scan": ex["delta0.01_nsp2_scan"], "slope_convergence_R0.9_nsp2": ex["slope_convergence_R0.9_nsp2"]}
S["ii_explicit_tau0.02"] = {k: {kk: v[kk] for kk in ("lam_min", "comm_minus_1") if kk in v} for k, v in ex["explicit_tau0.02"].items()}
S["ii_commutator_without_reservoir"] = cm
S["ii_boundary_R1_curvature"] = bc
S["fullfield_tests"] = {k: {kk: v[kk] for kk in v if kk in ("maxdev", "comm", "comm_minus_1", "lam_min", "det")} for k, v in ft.items()}
S["fullfield_curve_Gamma_sqrt18_nsp1"] = {e0: [{k: r[k] for k in ("tau", "lam_min", "CAA", "CAA_exact", "e2CPP_over_G", "comm_minus_1", "det")} for r in rows]
                                          for e0, rows in cu["curve"].items()}
S["fullfield_tau4_convergence"] = {k: {"lam_min": v["lam_min"], "comm_minus_1": v["comm_minus_1"]} for k, v in cu["tau4_convergence_eps0.05"].items()}
S["reduced_same_taus"] = cu["reduced_same_taus"]
S["fullfield_vs_reduced_eps_delta"] = ed

S["ii_truncated_wigner"] = {k: {kk: v[kk] for kk in ("lam_min", "lam_err", "lam_linearized", "M", "lo_mismatch")} for k, v in L("twa_summary.json")["cases"].items()}
S["ii_truncated_wigner_mode_dependence"] = {k: {kk: v[kk] for kk in ("lam_min", "lam_err", "lam_linearized", "M", "grid_modes")} for k, v in L("twa_modes_summary.json").items()}
S["source_launch_fullfield"] = {k: {"lam_min": v["lam_min"], "det": v["det"], "comm_minus_1": v["comm_minus_1"]} for k, v in L("source_seed_summary.json").items()}
S["source_values_quoted"] = {"lam_tau0.02_eps0.05": 0.8964864655, "lam_tau4_eps0.05": 3.159235825, "lam_tau4_eps0.1": 3.410751835, "lam_tau4_eps0.025": 3.074149802,
                             "power_e2CPP_12_26": 2.3335053304851803, "note": "from archive/similariton/TECHNICAL_NOTES.md and analysis_summary.json of run 2026-10-18-pi-chatgpt-independent-verification, read after commit 4ff455f"}
S["beyond_claim_finite_length_slot_model"] = L("slot_model_summary.json")
S["beyond_claim_slot_model_vs_fullfield_eps0.005"] = {k: {"lam_full": v["lam_full"], "lam_slot": v["lam_slot"]} for k, v in L("slot_model_check.json").items()}
S["beyond_claim_finite_length_fullfield_eps0.05"] = {k: {"Gamma": v["Gamma"], "min_lam": v["min_lam"], "tau_at_min": v["tau_at_min"]} for k, v in L("finite_length_summary.json").items()}
S["i_iii_reduced_other_Gamma"] = L("reduced_gamma_scan.json")
json.dump(S, open("summary.json", "w"), indent=1)
print("ok", len(json.dumps(S)))
