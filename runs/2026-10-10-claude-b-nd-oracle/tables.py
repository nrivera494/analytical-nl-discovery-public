"""Markdown tables for the note, the log and the claims from summary.json (claude-b, T-20261010-claude-interactive-05).
Usage: python tables.py"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "summary.json")))
P = {p["tag"]: p for p in S["points"]}
print("reduced curve:", S["curve"])
sel = ["N10_zr0.7", "N20_zr0.7", "N40_zr0.7", "N40_zr1", "N20_zr1.5", "N10_zr2", "N10_zr3", "N10_zr5", "N10_zr9"]
print("\n| point | $\\Phi$ | $N^2\\lambda_{\\min}$ | $\\Lambda(Z)$ | err | $N^2\\lambda_{\\rm pass}$ | $\\Pi(Z)$ | $N^2\\lambda_{\\rm gen}$ | $N^2F_{\\rm cen}$ | best binary (photon fraction) |")
print("|---|---|---|---|---|---|---|---|---|---|")
for t in sel:
    if t not in P:
        continue
    p = P[t]
    N2 = p["N"] ** 2
    fr = p["F_bin_photon_fraction"]
    print(f"| N{p['N']}, {p['zr']:g}{' (held out)' if p['heldout'] else ''}{'' if p['resolved'] else ' (under-resolved)'} | {p['N']*p['Z']:.1f} | {N2*p['lam_min']:.4f} | {N2*p['formula']:.4f} | {100*p['err_formula']:+.2f}% | "
          f"{N2*p['lam_pass']:.3f} | {N2*p['formula_pass']:.3f} | {N2*p['lam_gen']:.3f} | {N2*p['F_centroid']:.3f} | {p['F_bin']:.4f} ({'n/a' if fr is None else format(fr, '.2f')}) |")
print("\nc = (1 - N^2 lam_min / Lambda) Phi^2 by z/z_wb:")
for zr in sorted({p["zr"] for p in S["points"] if p["s"] == 0}):
    Q = [p for p in S["points"] if p["zr"] == zr and p["s"] == 0]
    print(zr, ", ".join(f"N{q['N']}:{-q['err_formula']*(q['N']*q['Z'])**2:.2f}{'' if q['resolved'] else '*'}" for q in sorted(Q, key=lambda q: q["N"])))
print("\nexponents:")
for zr, r in S["by_zr"].items():
    print(zr, {k: round(v, 2) for k, v in r.items() if "exponent" in k and v is not None})
print("\n| point | vs formula | vs lambda_gen | vs lambda_min | vs lambda_pass | centroid over lambda_gen |")
for t in sel:
    if t in P:
        p = P[t]
        print(f"| {t} | {p['gap_dB_bin_vs_formula']:.1f} | {p['gap_dB_bin_vs_gen']:.1f} | {p['gap_dB_bin_vs_min']:.1f} | {p['gap_dB_bin_vs_pass']:.1f} | {p['gap_dB_centroid_vs_gen']:.2f} |")
R = [p for p in S["points"] if p["s"] == 0 and p["resolved"]]
g = [p["gap_dB_centroid_vs_gen"] for p in R]
print("\ncentroid over lambda_gen, resolved points: %.2f .. %.2f dB (n = %d)" % (min(g), max(g), len(R)))
