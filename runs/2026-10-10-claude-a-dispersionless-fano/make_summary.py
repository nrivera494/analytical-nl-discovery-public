#!/usr/bin/env python3
"""Collect the numbers quoted in the claims, the exploration note and the log into summary.json, with dB gaps.
Usage: python make_summary.py"""
import json, os
import numpy as np
db = lambda a, b: float(10 * np.log10(a / b))
J = lambda f: json.load(open(f)) if os.path.exists(f) else {"rows": []}
S = {"run_id": "2026-10-10-claude-a-dispersionless-fano", "notes": "gaps in dB are 10 log10(best binary / quantity)"}

# Kerr, Gaussian, dispersionless
k = J("scan_kerr_gaussian.json")["rows"]
par = {r["Phi"]: r for r in J("parity_bound.json")["rows"]}
rel = {r["Phi"]: r["best_F"] for r in J("binary_relax_gaussian.json")["rows"] if "best_F" in r}
for r in J("binary_relax2_gaussian.json")["rows"]:
    if "best_F" in r:
        rel[r["Phi"]] = min(rel.get(r["Phi"], 9), r["best_F"])
cont = {12.5: 0.4971, 17.5: 0.5428, 25: 0.4323}
kerr = []
phis = sorted(set([r["Phi"] for r in k]) | set(rel) | set(par))
kd = {r["Phi"]: r for r in k}
for Phi in phis:
    lP = 1 / (1 + 4 * Phi**2 / (3 * np.sqrt(3)))
    vmin = 1 + 2 * Phi**2 - 2 * Phi * np.sqrt(1 + Phi**2)
    r = kd.get(Phi)
    tabu = min(r["pad8"]["binary_F"], r["pad4"]["binary_F"]) if r else cont.get(Phi)
    cands = [x for x in (tabu, rel.get(Phi)) if x is not None]
    best = min(cands) if cands else None
    lg = r["pad8"]["lam_gen"] if r else (par[Phi]["lam_odd"] if Phi in par else None)
    row = {"Phi": Phi, "lam_min": r["lam_min"] if r else vmin, "lam_min_source": "grid" if r else "V_min(Phi) (exact, item 2)",
           "lam_pass": r["lam_pass"] if r else None, "lam_gen": lg, "lam_P_formula": lP,
           "parity_bound": par[Phi]["parity_bound"] if Phi in par else None,
           "lam_even": par[Phi]["lam_even"] if Phi in par else None,
           "binary_tabu": tabu, "binary_relax": rel.get(Phi), "best_binary": best}
    if best:
        row["gap_dB_lamP_vs_binary"] = db(best, lP)
        if lg: row["gap_dB_lamgen_vs_binary"] = db(best, lg)
        row["gap_dB_lammin_vs_binary"] = db(best, row["lam_min"])
        if row["parity_bound"]: row["gap_dB_parity_vs_binary"] = db(best, row["parity_bound"])
        if lg: row["waste_lamgen_over_lammin"] = lg / row["lam_min"]
        row["waste_binary_over_lammin"] = best / row["lam_min"]
    kerr.append(row)
S["kerr_gaussian"] = kerr
# exponent of the best binary vs Phi (Phi >= 10)
pp = [(r["Phi"], r["best_binary"]) for r in kerr if r["best_binary"] and r["Phi"] >= 10]
if len(pp) >= 3:
    x, y = np.log([a for a, b in pp]), np.log([b for a, b in pp])
    S["binary_exponent_Phi_ge_10"] = {"slope": float(np.polyfit(x, y, 1)[0]), "points": pp}

# held-out
relR = {}
for r in J("binary_relax_raman.json")["rows"]:
    relR[(r["pulse"], r["T0_or_Ts_fs"], r["Phi"], r["T_K"])] = r["binary_relax"]
h = J("heldout_results.json")["rows"]
relS = {r["Phi"]: r["best_F"] for r in J("binary_relax_sech.json")["rows"] if "best_F" in r}
parS = {r["Phi"]: r for r in J("parity_bound_sech.json")["rows"]}
fro = {("kerr", 5.0): 0.04192, ("kerr", 15.0): 0.004838, ("raman300", 5.0): 0.08197, ("raman300", 15.0): 0.01941}
ho = []
for r in h:
    key = (r["case"], r["Phi"])
    best = min([x for x in (r["binary_F"], relS.get(r["Phi"]) if r["case"] == "kerr" else relR.get(("sech", 188.9, r["Phi"], 300.0))) if x is not None])
    o = dict(r); o["formula_lam_P"] = fro[key]; o["best_binary_all_methods"] = best
    o["gap_dB_formula_vs_binary"] = db(best, fro[key]); o["gap_dB_lamgen_vs_binary"] = db(best, r["lam_gen"])
    o["gap_dB_lammin_vs_binary"] = db(best, r["lam_min"])
    if r["case"] == "kerr" and r["Phi"] in parS:
        o["parity_bound"] = parS[r["Phi"]]["parity_bound"]; o["gap_dB_parity_vs_binary"] = db(best, o["parity_bound"])
    ho.append(o)
S["heldout_sech"] = ho
# Raman
S["raman_gaussian"] = J("raman_momentum_compare.json")["rows"]
for r in S["raman_gaussian"]:
    rv = relR.get(("gaussian", r["T0_fs"], r["Phi"], r["T_K"]))
    r["binary_tabu"] = r["binary_F"]
    if rv is not None:
        r["binary_relax"] = rv; r["binary_F"] = min(r["binary_F"], rv)
    r["gap_dB_formula_vs_binary"] = db(r["binary_F"], r["lam_P_R_formula"])
    r["gap_dB_lamgen_vs_binary"] = db(r["binary_F"], r["lam_gen"])
    r["gap_dB_lammin_band_vs_binary"] = db(r["binary_F"], r["lam_min_band"])
# dispersion: lambda_min law
L = J("lam_min_dispersion.json")["rows"]
law = {}
for Phi in (2.0, 5.0, 10.0, 20.0, 40.0):
    s = [r for r in L if r["Phi"] == Phi and r["dt"] == 0.01 and r["sign_beta2"] == 1 and r["tcut"] == 1.0 and r["nz"] == 200]
    sel = [r for r in s if 1e-6 <= r["y_PhiL_over_LD"] <= 1e-4]
    if len(sel) >= 3:
        law[str(Phi)] = {"exponent_1e-6_1e-4": float(np.polyfit(np.log([r["y_PhiL_over_LD"] for r in sel]), np.log([r["excess"] for r in sel]), 1)[0]),
                         "ratio_to_leading": {f'{r["y_PhiL_over_LD"]:g}': r["excess"] / r["pred_excess_leading"] for r in s}}
S["lam_min_dispersion_law"] = law
S["lam_min_dispersion_sech_heldout"] = [{"dt": r["dt"], "y": r["y_PhiL_over_LD"], "ratio": r["ratio"], "in_window": r["in_frozen_window"]} for r in J("lam_min_dispersion_sech.json")["rows"]]
S["c2_symbol_model"] = J("c2_symbol_model.json")["rows"]
S["c2_reshaping_check"] = J("c2_reshaping_check.json")["rows"]
S["lam_min_anomalous_grid_dependence"] = [{"dt": r["dt"], "lam_min": r["lam_min"]} for r in L if r["sign_beta2"] == -1]
# dispersion: filter quantities and momentum bound
S["dispersion_filter"] = J("scan_dispersion.json")["rows"]
S["dispersion_filter_phi20_rest"] = J("scan_dispersion_phi20_rest.json")["rows"]
S["binary_vs_dispersion"] = J("binary_vs_dispersion.json")["rows"]
S["binary_vs_beta3"] = J("binary_vs_beta3.json")["rows"]
S["momentum_bound_with_dispersion"] = J("momentum_dispersion.json")["rows"]
S["selfsteep"] = J("scan_selfsteep.json")
S["polarization"] = J("polarization.json")["rows"]
S["dither_formula_Phi10"] = [r for r in J("dither_ramp.json")["rows"] if "F_pred" in r]
S["binary_pad_check"] = {f"pad{p}": [r for r in J(f"binary_relax_pad{p}.json")["rows"] if "best_F" in r] for p in (4, 16)}
S["lam_gen_dense_thr1e-6"] = J("lam_gen_dense.json")["rows"]
S["grid_check_threshold_dt"] = J("grid_check_lamgen.json")["rows"] + J("grid_check2.json")["rows"]
S["birefringence_lam_min"] = J("birefringence_lammin.json")["rows"]
S["lam_min_dispersion_flattop_heldout"] = J("lam_min_dispersion_flattop.json")["rows"]
S["raman_temperature_T0_1ps_Phi10"] = J("scan_raman_temperature.json")["rows"]
S["momentum_bound_beta3_heldout"] = J("momentum_beta3.json")["rows"]
S["binary_structure"] = J("binary_structure.json")["rows"]
S["vector_raman_exact_linear_circular"] = J("vector_raman_exact.json")["rows"]
S["vector_raman_propagated"] = J("vector_raman_prop.json")["rows"]
S["vector_raman_chi_scan"] = J("vector_raman_chiscan.json")["rows"]
S["vector_raman_elliptical_1ps"] = J("vector_raman_1ps.json")["rows"]
S["heldout_thermal_T0_500fs_Phi15"] = J("heldout_thermal.json")["rows"]
S["raman_dt_convergence"] = J("raman_dt_convergence.json")["rows"]
S["open_prediction_phi50"] = J("open_prediction_phi50.json")["rows"]
S["parity_pad16"] = J("parity_pad16.json")["rows"]
S["open_prediction_lameven"] = J("open_prediction_lameven.json")["rows"]
S["heldout_flattop_lamgen"] = J("heldout_flattop_lamgen.json")["rows"]
S["lamgen_deficit_converged"] = J("lamgen_deficit.json")["rows"]
S["open_prediction_5ps_REFUTED"] = J("open_prediction_5ps.json")["rows"]
S["band_cost_check"] = J("band_cost_check.json")["rows"]
S["binary_relax_raman"] = J("binary_relax_raman.json")["rows"]
S["binary_relax2_pad16"] = [r for r in J("binary_relax2_pad16.json")["rows"] + J("binary_relax2_pad16_phi40.json")["rows"] + J("binary_relax2_pad32_phi20.json")["rows"] if "best_F" in r]
S["birefringence_Phi10_45deg"] = J("birefringence_Phi10_45deg.json")["rows"]
json.dump(S, open("summary.json", "w"), indent=1)
print(json.dumps({"kerr": [(r["Phi"], round(r["best_binary"], 4) if r["best_binary"] else None, round(r.get("gap_dB_lamgen_vs_binary", np.nan), 2), round(r.get("gap_dB_parity_vs_binary", np.nan), 2)) for r in kerr],
                  "exp": S.get("binary_exponent_Phi_ge_10", {}).get("slope")}, indent=0))
