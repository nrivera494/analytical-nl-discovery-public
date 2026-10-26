"""Summarize run 2026-10-04-claude-b.1-ideal-sech-kerr-20m into summary.json.

Reads the raw TOML output under ~/analytical-nl-discovery-data/<run-id>/<tag>/full_control.toml, recomputes the
archive's analytical soliton-continuum prediction with the byte-identical archive script
(soliton_copy_analytic_archive.py, no propagation), and compares both with the archive values in config.toml.
Usage: ~/agent-work/venv/bin/python summarize.py
"""
import json
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11 (the repo venv is 3.9)
    import tomli as tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
RUN_ID = HERE.name
RAW = Path.home() / "analytical-nl-discovery-data" / RUN_ID

import sys
sys.path.insert(0, str(HERE))
import soliton_copy_analytic_archive as an  # noqa: E402

cfg = tomllib.loads((HERE / "config.toml").read_text())
arch = cfg["archive"]
fz = cfg["frozen_control_parameters"]
offsets = cfg["readout"]["phase_offsets_rad"]


def rel(a, b):
    return (a - b) / abs(b)


# Analytical prediction (archive script, default quadrature grid dx=0.04, nx=16384, and a 2x finer grid).
zeta = fz["length_m"] / an.LD_M
analytic = {}
for label, grid in (("default_dx0.04_nx16384", {}), ("fine_dx0.02_nx32768", {"dx": 0.02, "nx": 32768})):
    Q = an.optical_covariance(zeta, **grid)
    rows = []
    for off in offsets:
        r = an.readout(Q, fz["length_m"], psi=an.PSI + off)
        rows.append({"phase_offset_rad": off, **r})
    analytic[label] = {"Q_optical": Q.tolist(), "readout": rows}
an_def = analytic["default_dx0.04_nx16384"]

runs = {}
for tag in [g["tag"] for g in cfg["grids"]]:
    f = RAW / tag / "full_control.toml"
    if f.exists():
        runs[tag] = tomllib.loads(f.read_text())

summary = {
    "run_id": RUN_ID,
    "task": "T-20261004-claude-interactive-06",
    "problem": "P-20261004-root-03",
    "agent": "claude-b.1",
    "case": "1: pure-Kerr ideal-sech soliton, coherent input-copy readout, 20 m (zeta = %.9f)" % zeta,
    "raw_location": str(RAW),
    "zeta": zeta,
    "LD_m_analytic_script": an.LD_M,
    "analytic_recomputed": analytic,
    "grids": {},
    "comparison_nominal": {},
    "convergence_vs_nominal": {},
}
for tag, d in runs.items():
    summary["grids"][tag] = {
        "nt": d["nt"], "window_ps": d["window_ps"], "dz_m": d["dz_m"], "dt_ps": d["dt_ps"],
        "phase_offsets_rad": [row["phase_offset_rad"] for row in d["readout"]],
        "F_total": [row["F_total"] for row in d["readout"]],
        "F_signal": [row["F_signal"] for row in d["readout"]],
        "F_reference_vacuum": [row["F_reference_vacuum"] for row in d["readout"]],
        "output_power_mw": [row["output_power_mw"] for row in d["readout"]],
        "Q_optical": d["Q_optical"],
        "exact_soliton_mean_relative_field_error": d["exact_soliton_mean_relative_field_error"],
        "photon_drift": d["photon_drift"],
        "input_power_mw": d["input_power_mw"],
        "forward_plus_4_adjoints_seconds": d["forward_plus_4_adjoints_seconds"],
    }

if "nominal" in runs:
    d = runs["nominal"]
    c = {}
    for i, off in enumerate(offsets):
        key = "offset0" if i == 0 else "offsetpi"
        F = d["readout"][i]["F_total"]
        P = d["readout"][i]["output_power_mw"]
        Fa = an_def["readout"][i]["F"]
        Pa = an_def["readout"][i]["output_mW_exact_sech"]
        c["F_" + key] = {
            "this_run": F,
            "archive_solver": arch["F_solver_" + key],
            "rel_diff_vs_archive_solver": rel(F, arch["F_solver_" + key]),
            "analytic_recomputed": Fa,
            "archive_analytic": arch["F_analytic_" + key],
            "rel_diff_analytic_recomputed_vs_archive_analytic": rel(Fa, arch["F_analytic_" + key]),
            "abs_diff_this_run_vs_analytic": F - Fa,
            "rel_diff_this_run_vs_analytic": rel(F, Fa),
        }
        c["Pout_mW_" + key] = {
            "this_run": P,
            "archive_solver": arch["Pout_mW_solver_" + key],
            "rel_diff_vs_archive_solver": rel(P, arch["Pout_mW_solver_" + key]),
            "analytic_recomputed_exact_sech": Pa,
            "rel_diff_this_run_vs_analytic": rel(P, Pa),
        }
    Q = np.array(d["Q_optical"])
    c["Q_optical"] = {
        "this_run": Q.tolist(),
        "max_abs_diff_vs_archive_solver": float(np.max(np.abs(Q - np.array(arch["Q_solver"])))),
        "max_abs_diff_vs_analytic_recomputed": float(np.max(np.abs(Q - np.array(an_def["Q_optical"])))),
    }
    c["exact_soliton_mean_relative_field_error"] = {
        "this_run": d["exact_soliton_mean_relative_field_error"],
        "archive": arch["exact_soliton_mean_relative_field_error"]}
    c["photon_drift"] = {"this_run": d["photon_drift"], "archive": arch["photon_drift"]}
    summary["comparison_nominal"] = c
    for tag, e in runs.items():
        if tag == "nominal":
            continue
        summary["convergence_vs_nominal"][tag] = {
            "F_offset0_rel_change": rel(e["readout"][0]["F_total"], d["readout"][0]["F_total"]),
            "F_offsetpi_rel_change": rel(e["readout"][1]["F_total"], d["readout"][1]["F_total"]),
            "F_offset0_abs_change": e["readout"][0]["F_total"] - d["readout"][0]["F_total"],
            "F_offsetpi_abs_change": e["readout"][1]["F_total"] - d["readout"][1]["F_total"],
            "Pout_offset0_rel_change": rel(e["readout"][0]["output_power_mw"], d["readout"][0]["output_power_mw"]),
            "Q_max_abs_change": float(np.max(np.abs(np.array(e["Q_optical"]) - np.array(d["Q_optical"])))),
            "F_offset0_abs_diff_vs_analytic": e["readout"][0]["F_total"] - an_def["readout"][0]["F"],
        }

    # Error against the analytic Green function on the nominal and fine grids (fine halves dz and dt).
    # RK4IP is fourth order in dz, so the error should fall by about 2^4 = 16 if dz dominates.
    if "fine" in runs:
        e = runs["fine"]
        Qa = np.array(an_def["Q_optical"]); Qa_f = np.array(analytic["fine_dx0.02_nx32768"]["Q_optical"])
        err = {}
        for name, nom, fin, ref, ref_alt in (
                ("Q_YY", d["Q_optical"][1][1], e["Q_optical"][1][1], Qa[1, 1], Qa_f[1, 1]),
                ("Q_XY", d["Q_optical"][0][1], e["Q_optical"][0][1], Qa[0, 1], Qa_f[0, 1]),
                ("F_offsetpi", d["readout"][1]["F_total"], e["readout"][1]["F_total"],
                 an_def["readout"][1]["F"], analytic["fine_dx0.02_nx32768"]["readout"][1]["F"]),
                ("F_offset0", d["readout"][0]["F_total"], e["readout"][0]["F_total"],
                 an_def["readout"][0]["F"], analytic["fine_dx0.02_nx32768"]["readout"][0]["F"])):
            en, ef = nom - ref, fin - ref
            err[name] = {"nominal_minus_analytic": en, "fine_minus_analytic": ef,
                         "ratio": en / ef if ef else None,
                         "exponent_log2_ratio": float(np.log2(abs(en / ef))) if ef else None,
                         "analytic_quadrature_change_dx0.04_to_0.02": ref_alt - ref}
        summary["error_vs_analytic_by_grid"] = err

(HERE / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
print(json.dumps(summary["comparison_nominal"], indent=1))
print(json.dumps(summary["convergence_vs_nominal"], indent=1))
