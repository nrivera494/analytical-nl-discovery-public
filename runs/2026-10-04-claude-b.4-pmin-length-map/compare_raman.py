"""Compare the oscillator and anisotropic Raman maps of run 2026-10-04-claude-b.4-pmin-length-map.

Usage: ~/agent-work/venv/bin/python runs/2026-10-04-claude-b.4-pmin-length-map/compare_raman.py
Reads summary.json (oscillator) and summary_anisotropic.json; prints a Markdown table of the dips and plateau powers of
both responses at every length, and the local exponents of the anisotropic first dip.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "summary.json")))
B = json.load(open(os.path.join(HERE, "summary_anisotropic.json")))


def dips(r):
    return ", ".join(f"{q['P_min_mw']:.1f} mW / {q['F_min']:.4f}" for q in r.get("dips", [])) or "none"


print("| $L$ (m) | oscillator dips ($P_{\\min}$ / $F_{\\min}$) | anisotropic dips | first-dip $\\Delta P_{\\min}/P_{\\min}$ | "
      "first-dip $\\Delta F_{\\min}$ | $P_{G0}$ osc. / aniso. (mW) | aniso. $P_{\\min}/P_{G025}$ | aniso. Raman share |")
print("|---|---|---|---|---|---|---|---|")
for k in sorted(set(A["lengths"]) | set(B["lengths"]), key=float):
    ra, rb = A["lengths"].get(k, {}), B["lengths"].get(k, {})
    dp = df = r25 = rs = ""
    if ra.get("first") and rb.get("first"):
        dp = f"{rb['first']['P_min_mw'] / ra['first']['P_min_mw'] - 1:+.3f}"
        df = f"{rb['first']['F_min'] - ra['first']['F_min']:+.4f}"
    if rb.get("first"):
        r25 = f"{rb['first'].get('P_min_over_P_G025', float('nan')):.3f}"
        rs = f"{rb['first']['Raman_share_of_rising_slope']:.2f}"
    pa = ra.get("plateau", {}).get("P_G0_mw")
    pb = rb.get("plateau", {}).get("P_G0_mw")
    print(f"| {float(k):g} | {dips(ra)} | {dips(rb)} | {dp} | {df} | {pa if pa is None else round(pa)} / "
          f"{pb if pb is None else round(pb)} | {r25} | {rs} |")
print()
print("anisotropic alpha_first_dip: " + ", ".join(f"{e['L_pair_m'][0]:g}-{e['L_pair_m'][1]:g} m: {e['alpha']:.2f}"
                                                  for e in B["alpha_first_dip"]))
print("anisotropic alpha_P_G025: " + ", ".join(f"{e['L_pair_m'][0]:g}-{e['L_pair_m'][1]:g} m: {e['alpha']:.2f}"
                                                for e in B["alpha_P_G025"]))
