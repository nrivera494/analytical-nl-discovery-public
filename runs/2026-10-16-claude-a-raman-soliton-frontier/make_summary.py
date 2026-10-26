#!/usr/bin/env python3
"""Collect the numbers quoted in the claims (C-20261016-claude-a-01/02/03) and the log into summary.json.
Reads the json/log outputs of this run folder; missing files are reported as pending. Usage: python make_summary.py"""
import json, glob, os
import numpy as np


def jload(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


def logrows(p):
    try:
        return [json.loads(l) for l in open(p) if l.startswith("{")]
    except FileNotFoundError:
        return []


S = {"run_id": "2026-10-16-claude-a-raman-soliton-frontier"}

# H1
h1 = logrows("h1_tests.log")
S["H1"] = {"n_potentials": len(h1), "max_eta_over_qinf": max(r["eta_over_qinf"] for r in h1) if h1 else None,
           "H1c_violations": [{"case": r["case"], "A": r["A"], "wkb_minus_eta": r["wkb_minus_eta"]} for r in h1 if r["wkb_minus_eta"] < -1e-3],
           "max_two_grid_err": max(r["two_grid_err"] for r in h1) if h1 else None}
lw = jload("h1c_lorentz_window.json")
S["H1"]["lorentz_window_check"] = lw
nar = logrows("h1c_narrow.log")
S["H1"]["H1c_prime"] = [{"shape": r["shape"], "A": r["A"], "wkb_minus_eta": r["wkb_minus_eta"], "two_grid_err": r["two_grid_err"],
                          "violates": r["violates"]} for r in nar]

# H2
h2 = {}
for f in ("h2_sech.log", "h2_gauss.log", "h2_A6_sech.log", "h2_A6_gauss.log", "h2b_asym.log", "h2b_flattop.log"):
    for r in logrows(f):
        k = f'{r["laser"]} A={r["A"]} {r["class"]}'
        d = h2.setdefault(k, {"eta_TL": r["eta_TL"], "ratios": [], "q_inf_final": []})
        d["ratios"].append(r["ratio_to_TL"]); d["q_inf_final"].append(r["q_inf_final"])
for k, d in h2.items():
    d["max_ratio"] = max(d["ratios"]); d["n_starts"] = len(d["ratios"])
S["H2"] = {"per_case": h2, "n_optimizations": sum(d["n_starts"] for d in h2.values()),
           "max_ratio_overall": max(d["max_ratio"] for d in h2.values()) if h2 else None}

# H3
hs = jload("h3_summary.json") or {}
S["H3"] = {"peaks": hs.get("peaks"), "small_tauR": hs.get("small_tauR"),
           "n_points": sum(1 for t in hs.get("table", []) if t.get("eps") is not None)}
conv = logrows("h3_conv.log")
S["H3"]["convergence"] = [{"tag": r["tag"], "N": r["N"], "T0_fs": r["T0_fs"], "n": r["n"], "width": r["width"], "h": r["h"],
                           "excess": r["excess"], "window_limited": r["window_limited"]} for r in conv]
convs = logrows("h3_conv_small.log")
S["H3"]["convergence_small_tauR"] = [{"tag": r["tag"], "N": r["N"], "T0_fs": r["T0_fs"], "L_times_N": r["L_times_N"], "h": r["h"],
                                      "excess": r["excess"]} for r in convs]
sc = jload("solver_check.json")
S["H3"]["second_implementation"] = sc["rows"] if sc else None
rel = logrows("h3_relaxed.log")
base = {}
for r in logrows("h3_main.log"):
    if r["raman"] and r["L_times_N"] == 4.0 and r["T0_fs"] == 100.0 and not r["window_limited"]:
        base[r["N"]] = r["f1_output_ZS"]
S["H3"]["self_steepening"] = [{"N": r["N"], "s": r["s"], "d3": r["d3"], "f1": r["f1_output_ZS"],
                               "f1_photon": r["f1_output_ZS"] / (1 - r["s"] * r["red_shift_W"]),
                               "ratio_photon_to_s0": r["f1_output_ZS"] / (1 - r["s"] * r["red_shift_W"]) / base[r["N"]]}
                              for r in rel if r["s"] > 0 and r["d3"] == 0 and r["N"] in base]
b3 = jload("h3_beta3.json")
S["H3"]["beta3"] = b3["rows"] if b3 else None
diag = jload("h3_peaks_N8_T400.json")
S["H3"]["N8_T400_aliasing_diagnostic"] = diag["rows"][0]["peaks_by_redshift"][:3] if diag else None

# H4
h4 = {}
for f in sorted(glob.glob("h4_N*_T*_*.json")):
    d = jload(f)
    if d:
        h4[f] = {"f1_TL": d["f1_TL"], "best_f1": d["best_f1"], "headroom": d["headroom"],
                 "integrable_bound_factor": d["integrable_bound_factor"], "n_evals": d["n_evals"],
                 "starts": [r for r in d["rows"] if r["start"] != "TL"]}
for f in sorted(glob.glob("h4_scan6_*.json")):
    d = jload(f)
    if d:
        h4[f] = {"rows": d["rows"], "max_ratio": max(r["ratio_to_TL"] for r in d["rows"])}
for f in sorted(glob.glob("h4grad_*.json")):
    d = jload(f)
    if d:
        h4[f] = {"f1_TL": d["f1_TL"], "best_f1": d["best_f1"], "headroom": d["headroom"], "n_evals": d["n_evals"],
                 "starts": [{k: v for k, v in r.items() if k != "c_opt"} for r in d["rows"] if r.get("start") != "TL" or "f1_opt" in r]}
for f in ("h4_adjoint_measure_N4_T200.json", "h4_robust.json", "h4_verify_N4_T100.json", "h4_recheck.json", "h4_recheck_N4d005.json"):
    d = jload(f)
    if d:
        h4[f] = {"rows": [{k: v for k, v in r.items() if k != "census"} for r in d["rows"]]}
S["H4"] = h4
h2c = jload("h2c_sharp.json")
if h2c:
    S["H2c_sharp_masks"] = {"n": len(h2c["rows"]), "max_ratio": max(r["eta_ratio"] for r in h2c["rows"])}
import re
pat = re.compile(r"(FIXEDSHIFT )?N=(\d) T0=(\d+) fs.*?ratios vac ([\d.]+) ram ([\d.]+) total ([\d.]+)")
h5 = []
for f in ("h5_jitter.log", "h5_jitter_N45.log", "h5_jitter_fixedshift.log", "h5_jitter_fixedshift_T140.log", "h5_jitter_fixedshift_T200.log"):
    try:
        for line in open(f):
            m = pat.search(line)
            if m:
                h5.append({"baseline": "fixed shift" if m.group(1) else "same length", "N": int(m.group(2)), "T0_fs": float(m.group(3)),
                           "R_vac": float(m.group(4)), "R_ram": float(m.group(5)), "R_tot": float(m.group(6)), "file": f})
    except FileNotFoundError:
        pass
S["H5"] = h5
json.dump(S, open("summary.json", "w"), indent=1, default=float)
print(json.dumps({"H1_max_eta_over_qinf": S["H1"]["max_eta_over_qinf"], "H2_n_opt": S["H2"]["n_optimizations"],
                  "H2_max_ratio": S["H2"]["max_ratio_overall"], "H3_points": S["H3"]["n_points"],
                  "H4": {k: v.get("headroom", v.get("max_ratio")) for k, v in h4.items()}}, indent=1))
