"""Summarize run 2026-10-04-claude-b.4-pmin-convergence.

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-convergence/summarize_convergence.py
For every case and grid variant: F, its parts and G at each power; the refitted P_min and F_min (exact parabola in ln P
through the three powers) where all three powers exist; and the changes relative to the base grid.
"""
import glob
import json
import math
import os
import re

import numpy as np

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_ID = "2026-10-04-claude-b.4-pmin-convergence"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}/points")
cfg = tomllib.load(open(os.path.join(HERE, "config.toml"), "rb"))
out = {"run_id": RUN_ID, "task": "T-20261004-claude-interactive-03", "agent": "claude-b.4", "cases": {}}
for case in cfg["cases"]:
    tag = case["tag"]
    res = {"length_m": case["length_m"], "variants": {}}
    for f in sorted(glob.glob(os.path.join(RAW, f"{tag}_agarwal_L*_P*_*.toml"))):
        d = tomllib.load(open(f, "rb"))
        v = d["variant"]
        res["variants"].setdefault(v, {})[f"{d['pin_mw']:.3f}"] = {
            "P_mw": d["pin_mw"], "F": d["F_total"], "F_bright": d["F_bright"], "F_shape": d["F_shape"],
            "F_Raman": d["F_Raman"], "G": d["transfer_slope_G"], "c": d["bright_amplitude_c"],
            "P_out_selected_mw": d["selected_output_power_mw"], "nt": d["nt"], "window_ps": d["window_ps"],
            "dz_m": d["dz_m"], "raman_z_spacing_m": d["raman_z_spacing_m"],
            "temporal_edge_fraction": d["temporal_edge_fraction"], "spectral_edge_fraction": d["spectral_edge_fraction"],
            "photon_drift": d["photon_drift"], "seconds": d["forward_seconds"] + d["adjoint_and_reservoir_seconds"]}
    base = res["variants"].get("base", {})
    for v, pts in res["variants"].items():
        P = sorted(pts, key=float)
        if v != "base":
            dF = [pts[p]["F"] - base[p]["F"] for p in P if p in base]
            dG = [pts[p]["G"] - base[p]["G"] for p in P if p in base]
            res.setdefault("changes_vs_base", {})[v] = {
                "max_abs_dF": max(map(abs, dF)) if dF else None, "max_abs_dG": max(map(abs, dG)) if dG else None,
                "dF_by_power": {p: pts[p]["F"] - base[p]["F"] for p in P if p in base}}
        if len(P) >= 3 and "dip" in tag:
            x = np.log([pts[p]["P_mw"] for p in P[:3]])
            y = [pts[p]["F"] for p in P[:3]]
            a, b, c = np.polyfit(x, y, 2)
            xv = -b / (2 * a)
            res.setdefault("refit", {})[v] = {"P_min_mw": float(math.exp(xv)), "F_min": float(np.polyval([a, b, c], xv))}
    if "refit" in res and "base" in res["refit"]:
        b0 = res["refit"]["base"]
        for v, r in res["refit"].items():
            r["dP_min_rel"] = r["P_min_mw"] / b0["P_min_mw"] - 1
            r["dF_min"] = r["F_min"] - b0["F_min"]
    if tag.startswith("L0.25"):
        # plateau bracket: P_G0 by linear interpolation of c in ln P between the two bracket powers, per variant
        for v, pts in res["variants"].items():
            if "1044.879" in pts and "1201.611" in pts:
                c1, c2 = pts["1044.879"]["c"], pts["1201.611"]["c"]
                x1, x2 = math.log(1044.879), math.log(1201.611)
                res.setdefault("P_G0_by_variant", {})[v] = math.exp(x1 + (x2 - x1) * c1 / (c1 - c2)) if c1 > 0 > c2 else None
    out["cases"][tag] = res
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
for tag, res in out["cases"].items():
    print(tag)
    for v, ch in res.get("changes_vs_base", {}).items():
        print(f"   {v:8s} max|dF|={ch['max_abs_dF']:.2e} max|dG|={ch['max_abs_dG']:.2e}")
    for v, r in res.get("refit", {}).items():
        print(f"   refit {v:8s} P_min={r['P_min_mw']:.3f} F_min={r['F_min']:.6f} dP/P={r.get('dP_min_rel', 0):+.2e} dF={r.get('dF_min', 0):+.2e}")
    if "P_G0_by_variant" in res:
        print("   P_G0", res["P_G0_by_variant"])
    for v, pts in res["variants"].items():
        print("   ", v, {p: round(q["F"], 6) for p, q in pts.items()})
