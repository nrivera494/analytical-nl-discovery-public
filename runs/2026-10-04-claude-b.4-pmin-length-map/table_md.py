"""Print the Markdown tables used in explorations/2026-10-04-claude-b.4-pmin-length.md from summary.json.

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-length-map/table_md.py [anisotropic]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "summary.json" if len(sys.argv) < 2 else f"summary_{sys.argv[1]}.json"
S = json.load(open(os.path.join(HERE, NAME)))
print("| $L$ (m) | $\\zeta$ | dips: $P_{\\min}$ (mW), $F_{\\min}$ | bright | shape | Raman | $G$ | $T_N$ | "
      "$\\sigma_{\\omega,\\rm out}$ (rad/ps) | $P_{G0}$ (mW) | $P_{\\min}/P_{G0}$ | $P_{G025}$ (mW) | "
      "$P_{\\min}/P_{G025}$ | ends the dip (Raman share) | points |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(S["lengths"], key=float):
    r = S["lengths"][k]
    pg = r["plateau"].get("P_G0_mw")
    pg25 = r["plateau"].get("P_G025_mw")
    zeta = r["length_m"] / 3.343290600272917
    if not r.get("dips"):
        pgs = f"{pg:.0f}" if pg else "-"
        pg25s = f"{pg25:.0f}" if pg25 else "-"
        wk = "; weak-power dip only" if r["F_min_sampled_below_P_G0"] < 1 else ""
        print(f"| {r['length_m']:g} | {zeta:.3f} | no dip of prominence ≥ 0.003{wk} (lowest sampled $F$ = {r['F_min_sampled_below_P_G0']:.4f} "
              f"at {r['P_at_F_min_sampled_mw']:.0f} mW) | | | | | | | {pgs} | | {pg25s} | | | {r['n_points']} |")
        continue
    for j, q in enumerate(r["dips"]):
        d = q["decomposition"]
        rs = q["Raman_share_of_rising_slope"]
        lab = q["term_ending_minimum"].replace("F_", "") if q["term_ending_minimum"] else "-"
        print(f"| {r['length_m']:g}{'' if j == 0 else ' (2nd)'} | {zeta:.3f} | {q['P_min_mw']:.1f}, {q['F_min']:.4f} | "
              f"{d['F_bright']:.3f} | {d['F_shape']:.3f} | {d['F_Raman']:.4f} | {d['G']:.3f} | {d['T_N']:.4f} | "
              f"{q['output_sigma_omega_rad_ps']:.2f} | {pg if pg is None else round(pg)} | {q.get('P_min_over_P_G0', float('nan')):.3f} | "
              f"{pg25 if pg25 is None else round(pg25)} | {q.get('P_min_over_P_G025', float('nan')):.3f} | {lab} ({rs:.2f}) | "
              f"{r['n_points'] if j == 0 else ''} |")
print()
for key in ("alpha_first_dip", "alpha_P_G0", "alpha_P_G025"):
    print(key + ": " + ", ".join(f"{e['L_pair_m'][0]:g}-{e['L_pair_m'][1]:g} m: {e['alpha']:.2f}" for e in S[key]))
print()
for k in sorted(S["lengths"], key=float):
    r = S["lengths"][k]
    print(k, "G_fd max diff", r["G_fd_max_abs_diff"], "max spectral edge below PG0", r["max_spectral_edge_fraction_below_P_G0"],
          "max |drift| below PG0", r["max_abs_photon_drift_below_P_G0"],
          "dip halfwidths", [round(q["lnP_halfwidth_dF_0.002"], 3) for q in r.get("dips", [])],
          "spacing", [round(q["max_relative_spacing"], 3) for q in r.get("dips", [])],
          "groups", [(round(q["groups"]["phi_NL_chirped_peak"], 2), round(q["groups"]["N2_chirped_peak"], 1),
                      round(q["groups"]["L_over_LWB_chirpedpeak_kappa1"], 2)) for q in r.get("dips", [])])
