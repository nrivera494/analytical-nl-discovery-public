"""Summarize run 2026-10-16-claude-b.7-solver-masks into summary.json (from results_v2.jsonl)."""
import json
import os

RUN_ID = "2026-10-16-claude-b.7-solver-masks"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}")
HERE = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(l) for l in open(os.path.join(RAW, "results_v2.jsonl")) if l.strip()]


def get(mask, tag, n=None, mode="exact"):
    for r in recs:
        if r["mask"] == mask and r["tag"] == tag and r["mode"] == mode and (n is None or r["nsteps"] == n):
            return r
    return None


def rel(a, b):
    return a / b - 1


out = {"run_id": RUN_ID,
       "definition": ("N = 3, delta3 = 0.05, xi = 2, laser exp(-tau^2/2), model M0. eta_B: band w >= 10/3 "
                      "energy / laser energy; eta_G: same after the gate g = 1 - 0.5[tanh(tau+15) - tanh(tau-15)]. "
                      "Primary grid = claude-b's: TW = 70, Nt = 1024, mask applied on the exact bins. "
                      "*_fracedge: band sums with the bin straddling w_z weighted by its fraction above w_z. "
                      "Window checks W140/W280 use the TW = 70 masked input zero-padded in time (identical "
                      "field); W140interp applies the mask linearly interpolated in w on 2pi/140 bins "
                      "(a different input field)."),
       "masks": {}}
for m in ("TL", "phase", "passive"):
    r2, r4, r8 = get(m, "R", 2000), get(m, "R", 4000), get(m, "R", 8000)
    f, w1, w2 = get(m, "Ftau"), get(m, "W140"), get(m, "W280")
    wi = get(m, "W140interp", mode="interp")
    e = {"primary_TW70_Nt1024_n8000": {k: r8[k] for k in ("eta_B", "eta_G", "eta_B_fracedge", "eta_G_fracedge",
                                                         "E_in_over_E_laser", "input_peak_power_ratio",
                                                         "E_rel_drift", "P_abs_drift", "H_rel_drift",
                                                         "output_edge_power_ratio")},
         "claude-b_step_h0.001_n2000": {k: r2[k] for k in ("eta_B", "eta_G")},
         "relchange_n2000_vs_n8000": {k: rel(r2[k], r8[k]) for k in ("eta_B", "eta_G")},
         "relchange_n4000_vs_n8000": {k: rel(r4[k], r8[k]) for k in ("eta_B", "eta_G")},
         "relchange_Nt1024_vs_Nt2048_TW70": {k: rel(r8[k], f[k]) for k in ("eta_B", "eta_G")},
         "window": {
             "TW140": {k: w1[k] for k in ("eta_B", "eta_G", "eta_B_fracedge", "eta_G_fracedge")},
             "TW280": {k: w2[k] for k in ("eta_B", "eta_G", "eta_B_fracedge", "eta_G_fracedge")},
             "relchange_TW70_vs_TW140": {k: rel(r8[k], w1[k]) for k in ("eta_B", "eta_G", "eta_B_fracedge", "eta_G_fracedge")},
             "relchange_TW140_vs_TW280": {k: rel(w1[k], w2[k]) for k in ("eta_B", "eta_G", "eta_B_fracedge", "eta_G_fracedge")}}}
    if wi is not None:
        e["mask_linear_interp_TW140"] = {k: wi[k] for k in ("eta_B", "eta_G", "eta_B_fracedge", "eta_G_fracedge",
                                                             "E_in_over_E_laser", "input_edge_power_ratio")}
        e["relchange_interp_vs_zeropad_TW140"] = {k: rel(wi[k], w1[k]) for k in ("eta_B", "eta_G")}
    out["masks"][m] = e
with open(os.path.join(HERE, "summary.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote summary.json")
