"""Summarize results.jsonl of run 2026-10-10-claude-b.6-solver-grid into summary.json.

Usage (repository root):
  ~/agent-work/venv/bin/python runs/2026-10-10-claude-b.6-solver-grid/summarize_grid.py
"""
import datetime
import json
import os

RUN_ID = "2026-10-10-claude-b.6-solver-grid"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.expanduser("~"), "analytical-nl-discovery-data", RUN_ID)
recs = [json.loads(l) for l in open(os.path.join(RAW, "results.jsonl")) if l.strip()]
ORDER = ["N5_zr0.3", "N5_zr0.7", "N5_zr1", "N5_zr1.5", "N10_zr0.3", "N10_zr0.7", "N10_zr1",
         "N10_zr1.5", "N20_zr0.3", "N20_zr0.7", "N20_zr1", "N20_zr1.5"]
Q = ("F_w_centroid", "F_w_lambda_gen_eigvec", "F_w_best_binary", "bandwidth_ratio_var_in_over_out",
     "F_centroid_full_grid")


def pick(stage, key):
    out = [r for r in recs if r["stage"] == stage and r["key"] == key]
    return out[-1] if out else None


def s6(x):
    return None if x is None else format(x, "#.6g")


table = {}
for key in ORDER:
    r = pick("base", key)
    if r is None:
        continue
    e = {"N": r["N"], "zr": r["zr"], "xi": r["xi"], "Nt": r["Nt"], "nsteps": r["nsteps"],
         "dz_LD": r["dz_LD"]}
    for q in Q:
        e[q] = r[q]
        e[q + "_6sig"] = s6(r[q])
    e["F_centroid_full_over_ratio_minus_1"] = r["F_full_over_ratio_minus_1"]
    e["F_centroid_given_bins_over_ratio_minus_1"] = r["F_w_centroid"] / r["bandwidth_ratio_var_in_over_out"] - 1
    e["var_in"] = r["var_in"]
    e["var_out"] = r["var_out"]
    e["out_frac_above_0.8_nyquist"] = r["out_frac_above_0.8_nyquist"]
    e["out_frac_above_0.5_nyquist"] = r["out_frac_above_0.5_nyquist"]
    e["photon_rel_change"] = r["photon_rel_change"]
    d = pick("Nt_double", key) or (pick("conv_Nt_double", key) if key == "N20_zr1.5" else None)
    if d is not None:
        e["Nt_doubled"] = {q: d[q] for q in Q}
        e["Nt_doubled_minus_base"] = {q: d[q] - r[q] for q in Q}
        e["Nt_doubled_full_over_ratio_minus_1"] = d["F_full_over_ratio_minus_1"]
    table[key] = e

conv = {}
b = pick("base", "N20_zr1.5")
for st in ("conv_steps_half", "conv_steps_double", "conv_Nt_double"):
    c = pick(st, "N20_zr1.5")
    if c is None or b is None:
        continue
    conv[st] = {"Nt": c["Nt"], "nsteps": c["nsteps"],
                "minus_base": {q: c[q] - b[q] for q in Q},
                "values": {q: c[q] for q in Q},
                "full_over_ratio_minus_1": c["F_full_over_ratio_minus_1"]}

summary = {"run_id": RUN_ID,
           "written": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "conventions": {
               "model": "Kerr-only NLSE i u_xi - u_tautau/2 + N^2|u|^2 u = 0, u0 = exp(-tau^2/2), xi from "
                        "weights_grid_for_solver.json; solver realization T0 = 1 ps, beta2 = 1 ps^2/m, "
                        "gamma = 1 /W/m, omega0 T0 = 1e9 (s = 1e-9), NoRaman()",
               "grid": "claude-b's grid: Nt over a 40 T0 window (512 for N = 5, 10; 1024 for N = 20); "
                       "steps nsteps = max(4000, N^2 xi / 0.002 rounded up to 1000)",
               "weights": "claude-b bin k on solver bin -k (mirror); F_w = Var(N_w) / sum_k w_k^2 nbar_k, "
                          "Var from solve_adjoint(...; adjoint_mode=:discrete_rk4ip)",
               "bandwidth_ratio": "var_in/var_out of the photon-number spectrum over the whole grid, "
                                  "(Omega T0)^2 about each spectrum's own mean",
               "F_centroid_full_grid": "centroid weight extended to every grid bin, w = -(Omega T0) + offset "
                                       "(offset = mean of w_centroid - k 2pi/40 over the given bins)"},
           "table": table,
           "convergence_N20_zr1.5": conv,
           "all_points": recs}
with open(os.path.join(HERE, "summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
print("wrote summary.json with", len(recs), "records")
