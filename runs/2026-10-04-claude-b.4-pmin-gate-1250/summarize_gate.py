"""Summarize run 2026-10-04-claude-b.4-pmin-gate-1250: compare with the archive point by point and fit P_min.

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-gate-1250/summarize_gate.py
Reads the raw point TOMLs from ~/analytical-nl-discovery-data/<run-id>/points/ and the archive TOMLs (read-only),
writes summary.json next to this script.
"""
import glob
import json
import math
import os
import sys
try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pminfit import fit_min, interp_at  # noqa: E402

RUN_ID = "2026-10-04-claude-b.4-pmin-gate-1250"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}/points")
ARCH = "~/Desktop/fall2026_research/ai driven lab work/research_runs"

cfg = tomllib.load(open(os.path.join(HERE, "config.toml"), "rb"))
out = {"run_id": RUN_ID, "task": "T-20261004-claude-interactive-03", "agent": "claude-b.4",
       "fit_method": "local quadratic in ln P: 3-point exact (primary) and 5-point least squares (check)",
       "gate_tolerance_relative_P_min": 0.02, "sweeps": {}}
for sw in cfg["sweeps"]:
    tag = sw["tag"]
    rows = []
    for P in sw["powers_mw"]:
        f = os.path.join(RAW, f"{tag}_{sw['kind']}_P{P:.2f}.toml")
        if not os.path.exists(f):
            continue
        d = tomllib.load(open(f, "rb"))
        ap = os.path.join(ARCH, sw["archive_glob"].replace("{P}", str(int(P))).replace("{P:.1f}", f"{P:.1f}"))
        a = tomllib.load(open(ap, "rb")) if os.path.exists(ap) else None
        aF = None if a is None else a.get("F_total", a.get("F_intrinsic"))
        aFR = None if a is None else a.get("F_Raman", a.get("raman_F_increment"))
        row = {"P_mw": P, "F": d["F_total"], "F_bright": d["F_bright"], "F_shape": d["F_shape"],
               "F_phase": d["F_phase"], "F_partition": d["F_partition"], "F_Raman": d["F_Raman"],
               "G": d["transfer_slope_G"], "c": d["bright_amplitude_c"], "T_N": d["T_N"],
               "P_out_selected_mw": d["selected_output_power_mw"], "photon_drift": d["photon_drift"],
               "temporal_edge_fraction": d["temporal_edge_fraction"],
               "spectral_edge_fraction": d["spectral_edge_fraction"],
               "archive_file": None if a is None else os.path.relpath(ap, ARCH),
               "archive_F": aF, "archive_F_Raman": aFR,
               "archive_P_out_selected_mw": None if a is None else a["selected_output_power_mw"],
               "archive_F_bright": None if a is None else a.get("F_common_amplitude")}
        if aF is not None:
            row["dF_rel"] = (d["F_total"] - aF) / aF
            row["dPout_rel"] = (d["selected_output_power_mw"] - a["selected_output_power_mw"]) / a["selected_output_power_mw"]
        rows.append(row)
    if not rows:
        continue
    P = [r["P_mw"] for r in rows]
    mine3 = fit_min(P, [r["F"] for r in rows], 3)
    mine5 = fit_min(P, [r["F"] for r in rows], 5)
    res = {"length_m": sw["length_m"], "kind": sw["kind"], "grid": {k: sw[k] for k in ("nt", "window_ps", "dz_m", "raman_z_spacing_m")},
           "points": rows, "fit_mine_3pt": mine3, "fit_mine_5pt": mine5}
    if all(r["archive_F"] is not None for r in rows):
        arch3 = fit_min(P, [r["archive_F"] for r in rows], 3)
        arch5 = fit_min(P, [r["archive_F"] for r in rows], 5)
        res["fit_archive_3pt"] = arch3
        res["fit_archive_5pt"] = arch5
        res["max_abs_dF_rel"] = max(abs(r["dF_rel"]) for r in rows)
        res["max_abs_dPout_rel"] = max(abs(r["dPout_rel"]) for r in rows)
        if mine3["ok"] and arch3["ok"]:
            res["P_min_rel_diff_3pt"] = mine3["P_min_mw"] / arch3["P_min_mw"] - 1
            res["gate_pass"] = abs(res["P_min_rel_diff_3pt"]) <= 0.02
    if mine3.get("ok"):
        Pm = mine3["P_min_mw"]
        res["decomposition_at_P_min"] = {k: interp_at(P, [r[k] for r in rows], Pm) for k in
                                         ("F_bright", "F_shape", "F_phase", "F_partition", "F_Raman", "G", "T_N")}
        # Dimensionless groups at P_min. T0 (spectral rms), L_D, C and Omega_e T0 do not depend on P or L;
        # N^2 and phi scale linearly with P (checked: ratios in the point files are exact to rounding).
        ref = tomllib.load(open(os.path.join(RAW, f"{tag}_{sw['kind']}_P{rows[0]['P_mw']:.2f}.toml"), "rb"))
        s = Pm / ref["pin_mw"]
        T0, LD, b2 = ref["T0_spectral_rms_ps"], ref["L_D_m"], ref["beta2_ps2_m"]
        Tc = ref["input_fwhm_ps"] / (2 * math.sqrt(math.log(2)))  # chirped 1/e half-width (Gaussian convention)
        N2TL, N2pk = ref["N2_TL"] * s, ref["N2_chirped_peak"] * s
        LDc = Tc ** 2 / b2
        N2c = ref["gamma_W_m"] * ref["input_peak_W"] * s * Tc ** 2 / b2
        Lm = sw["length_m"]
        res["groups_at_P_min"] = {
            "T0_spectral_rms_ps": T0, "L_D_m": LD, "zeta": Lm / LD, "C_chirp": ref["C_chirp"],
            "Omega_e_T0_red": ref["Omega_e_T0_red"], "Omega_e_T0_blue": ref["Omega_e_T0_blue"],
            "N2_TL": N2TL, "N2_chirped_peak": N2pk, "phi_NL_chirped_peak": ref["phi_NL_chirped_peak"] * s,
            "phi_NL_TL_peak": ref["gamma_W_m"] * ref["P_peak_transform_limited_W"] * s * Lm,
            "L_WB_over_kappa_TL_m": LD / math.sqrt(N2TL), "L_WB_over_kappa_chirpedpeak_m": LD / math.sqrt(N2pk),
            "T_chirped_ps": Tc, "L_D_chirped_m": LDc, "N2_chirped_duration_and_peak": N2c,
            "L_WB_over_kappa_chirped_duration_m": LDc / math.sqrt(N2c)}
        # Crude plateau estimate for the frozen note only: extrapolate G linearly from the two highest powers.
        hi2 = sorted(rows, key=lambda r: r["P_mw"])[-2:]
        slope = (hi2[1]["G"] - hi2[0]["G"]) / (hi2[1]["P_mw"] - hi2[0]["P_mw"])
        if slope < 0:
            res["P_G0_linear_extrapolation_mw"] = hi2[1]["P_mw"] - hi2[1]["G"] / slope
            res["P_min_over_P_G0_extrapolated"] = Pm / res["P_G0_linear_extrapolation_mw"]
    out["sweeps"][tag] = res
    print(tag, "mine", mine3, "\n   archive", res.get("fit_archive_3pt"), "\n   maxdF", res.get("max_abs_dF_rel"),
          "gate", res.get("gate_pass"))
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print("wrote", os.path.join(HERE, "summary.json"))
