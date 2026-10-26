"""Post-freeze comparison with claude-b's numpy values for item 7 (read after summary.json was hashed).

Source: runs/2026-10-16-claude-b-dw-oracle/summary.json, keys m1_gauss3_heldout (eta_DW at claude-b's
finer step 'h2', per-delta3 Nt / window / Raman kernel step) and m1_gauss3_fit4 (c, p, d).
Writes comparison.json next to this script.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-b.7-solver-m1gauss")
cb = json.load(open(os.path.join(HERE, "..", "2026-10-16-claude-b-dw-oracle", "summary.json")))
mine = json.load(open(os.path.join(HERE, "summary.json")))
D3 = (0.0055, 0.006, 0.0066, 0.0073)


def recs(stage):
    fn = os.path.join(RAW, f"results_{stage}.jsonl")
    return [json.loads(l) for l in open(fn)] if os.path.exists(fn) else []


def at(stage, d3, xi=2.0):
    for r in recs(stage):
        if abs(r["delta3"] - d3) < 1e-12 and abs(r["xi"] - xi) < 1e-9:
            return r
    return None


out = {"source": "runs/2026-10-16-claude-b-dw-oracle/summary.json (m1_gauss3_heldout, m1_gauss3_fit4)",
       "convention": "reldiff = claude-b / solver - 1", "by_delta3": {}}
cbv = {round(e["d3"], 6): e for e in cb["m1_gauss3_heldout"]}
cmp = {}
for d3 in D3:
    e = cbv[round(d3, 6)]
    m32 = mine["by_delta3"][f"{d3:.4f}"]["convergence"]["eta_G_n32000"]
    b8 = at("base", d3)["eta_G"]
    t8 = at("dt", d3)["eta_G"]
    # second-order dt model fitted to the solver's own two kernel steps (0.390625 and 0.1953125 fs)
    h1, h2 = 0.390625, 0.1953125
    eta0_8 = t8 + (t8 - b8) / 3.0                      # dt -> 0 at 8000 steps
    k = (t8 - b8) / (eta0_8 * (h1 ** 2 - h2 ** 2))      # eta(dt) = eta0 (1 - k dt^2)
    eta0 = m32 * eta0_8 / b8                            # 32000 steps, dt -> 0
    pred_cb = eta0 * (1 - k * e["kernel_dt_fs"] ** 2)   # what the solver would give at claude-b's kernel step
    d = {"claude-b_eta_DW": e["eta_DW"], "claude-b_kernel_dt_fs": e["kernel_dt_fs"],
         "solver_n32000_dt0.39fs": m32, "reldiff_vs_solver_n32000": e["eta_DW"] / m32 - 1,
         "solver_dt_to_0_estimate": eta0, "reldiff_vs_solver_dt0": e["eta_DW"] / eta0 - 1,
         "solver_k_per_fs2": k,
         "solver_value_at_claude-b_kernel_dt": pred_cb,
         "reldiff_vs_solver_at_same_kernel_dt": e["eta_DW"] / pred_cb - 1}
    ss = at("ss", d3)
    if ss is not None:
        d["solver_w0T0_1e8_n8000"] = ss["eta_G"]
        d["relchange_w0T0_1e6_vs_1e8_n8000"] = b8 / ss["eta_G"] - 1
    out["by_delta3"][f"{d3:.4f}"] = d
    cmp[d3] = d

fit_cb = cb["m1_gauss3_fit4"]
fit_me = mine["fit_primary"]
sens = np.array(fit_me["dd_dln_eta"])
eps = np.array([cmp[d3]["reldiff_vs_solver_n32000"] for d3 in D3])
out["fit"] = {"claude-b": fit_cb, "solver_n32000": {k: fit_me[k] for k in ("c", "p", "d")},
              "d_diff_claude-b_minus_solver": fit_cb["d"] - fit_me["d"],
              "d_diff_predicted_from_eta_diffs_linear": float(sens @ eps)}
json.dump(out, open(os.path.join(HERE, "comparison.json"), "w"), indent=1)
for d3, d in cmp.items():
    print(f"{d3:.4f}", {k: (f"{v:.4e}" if isinstance(v, float) else v) for k, v in d.items()})
print(out["fit"])


# --- d from (i) claude-b's values corrected to kernel dt -> 0 with the solver's measured k, and
# --- (ii) the solver's 32000-step values corrected to dt -> 0 and to s = 1/(omega0 T0) -> 0 (s-effect
# --- measured at delta3 = 0.0055 and 0.0073, interpolated linearly in 1/delta3 for the middle two)
def fit3(etas):
    d = np.array(sorted(etas))
    y = np.log(np.array([etas[x] for x in d]))
    A = np.column_stack([np.ones_like(d), np.log(d), -1.0 / d])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return {"c": float(coef[0]), "p": float(coef[1]), "d": float(coef[2]),
            "rms_residual": float(np.sqrt(np.mean((y - A @ coef) ** 2)))}


cb_dt0 = {d3: cmp[d3]["claude-b_eta_DW"] / (1 - cmp[d3]["solver_k_per_fs2"] * cmp[d3]["claude-b_kernel_dt_fs"] ** 2)
          for d3 in D3}
x = np.array([1 / 0.0055, 1 / 0.0073])
yv = np.array([cmp[0.0055]["relchange_w0T0_1e6_vs_1e8_n8000"], cmp[0.0073]["relchange_w0T0_1e6_vs_1e8_n8000"]])
slope = (yv[0] - yv[1]) / (x[0] - x[1])
s_eff = {d3: float(yv[1] + slope * (1 / d3 - x[1])) for d3 in D3}
me_best = {d3: cmp[d3]["solver_dt_to_0_estimate"] / (1 + s_eff[d3]) for d3 in D3}
out["fit"]["claude-b_values_corrected_to_kernel_dt0_with_solver_k"] = fit3(cb_dt0)
out["fit"]["solver_dt0_s0_estimate"] = fit3(me_best)
out["solver_dt0_s0_eta"] = {f"{d3:.4f}": me_best[d3] for d3 in D3}
out["selfsteepening_effect_interpolated"] = {f"{d3:.4f}": s_eff[d3] for d3 in D3}
out["reldiff_claude-b_dt0_vs_solver_dt0_s0"] = {f"{d3:.4f}": cb_dt0[d3] / me_best[d3] - 1 for d3 in D3}
json.dump(out, open(os.path.join(HERE, "comparison.json"), "w"), indent=1)
print("cb dt0 fit", out["fit"]["claude-b_values_corrected_to_kernel_dt0_with_solver_k"])
print("solver dt0 s0 fit", out["fit"]["solver_dt0_s0_estimate"])
print("reldiff after corrections", out["reldiff_claude-b_dt0_vs_solver_dt0_s0"])
print("solver best eta", out["solver_dt0_s0_eta"])
