"""Print the markdown tables used in explorations/2026-10-04-claude-b-manakov-deviation.md from the summary_*.json files
of this run, and check that the kmax = 5 rows reproduce run 2026-10-04-claude-b-manakov-deviation-scan."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-scan", "summary.json")

runs = {z: json.load(open(os.path.join(HERE, f"summary_zeta{z}.json"))) for z in (2, 5)}
edges = sorted({round(c["edge"], 3) for c in runs[2]["cases"]})
print("| $\\zeta$ | $\\delta$ | " + " | ".join(f"{e:.3f}" for e in edges) + " |")
print("|---|---|" + "---|" * len(edges))
for z in (2, 5):
    for d in (0.0, 0.942):
        row = []
        for e in edges:
            c = [c for c in runs[z]["cases"] if round(c["edge"], 3) == e and abs(c["delta"] - d) < 1e-2][0]
            row.append(f"{c['Ftot_dB_minus_Fs_dB']:+.3f}")
        print(f"| {z} | {d:g} | " + " | ".join(row) + " |")
print()
print("| $\\zeta$ | $F_s$ (LP01) at each edge |")
print("|---|---|")
for z in (2, 5):
    fs = []
    for e in edges:
        c = [c for c in runs[z]["cases"] if round(c["edge"], 3) == e][0]
        fs.append(f"{c['Fs_LP01']:.4f}")
    print(f"| {z} | " + ", ".join(fs) + " |")
print()
scan = json.load(open(SCAN))
for z in (2, 5):
    for d in (0.0, 0.942):
        a = [c for c in runs[z]["cases"] if c["kmax"] == 5 and abs(c["delta"] - d) < 1e-2][0]
        b = [c for c in scan["cases"] if c["zeta"] == z and c["p2"] == 0.3 and abs(c["delta"] - d) < 1e-2][0]
        print(f"reproduction zeta={z} delta={d}: edge scan {a['Ftot_dB_minus_Fs_dB']:+.6f} dB, scan {b['Ftot_dB_minus_Fs_dB']:+.6f} dB, "
              f"|dFtot|/Ftot = {abs(a['computed']['Ftot'] - b['computed']['Ftot']) / b['computed']['Ftot']:.1e}")

print()
# extra cases: zeta = 5, delta = 0.942 readouts (p2 = 0.3), and p2 = 0.15 fixed band
fixed5 = {round(c["edge"], 3): c["Ftot_dB_minus_Fs_dB"] for c in runs[5]["cases"] if c["delta"] > 0.9}
fixed2 = {round(c["edge"], 3): c["Ftot_dB_minus_Fs_dB"] for c in runs[2]["cases"] if c["delta"] > 0.9}
sh5 = {round(c["edge"], 3): c["Ftot_dB_minus_Fs_dB"] for c in json.load(open(os.path.join(HERE, "summary_shifted_zeta5.json")))["cases"]}
sh2 = {round(c["edge"], 3): c["Ftot_dB_minus_Fs_dB"] for c in json.load(open(os.path.join(HERE, "summary_shifted_zeta2.json")))["cases"]}
tr5 = {round(c["half_width"], 3): c["Ftot_dB_minus_Fs_dB"] for c in json.load(open(os.path.join(HERE, "summary_trapped_zeta5.json")))["cases"]}
print("| readout ($p_2=0.3$, $\\delta=0.94$) | $\\zeta$ | " + " | ".join(f"{e:.3f}" for e in edges) + " |")
print("|---|---|" + "---|" * len(edges))
print("| common band at 0 (readout (a)) | 5 | " + " | ".join(f"{fixed5[e]:+.3f}" for e in edges) + " |")
print("| LP01 band at 0, LP02 band at $-\\delta$ | 5 | " + " | ".join(f"{sh5[e]:+.3f}" for e in edges) + " |")
print("| bands at the trapped carriers ($+0.31$, $-0.63$) | 5 | " + " | ".join(f"{tr5[e]:+.3f}" for e in edges) + " |")
print("| common band at 0 (readout (a)) | 2 | " + " | ".join(f"{fixed2[e]:+.3f}" for e in edges) + " |")
print("| LP01 band at 0, LP02 band at $-\\delta$ | 2 | " + " | ".join(f"{sh2[e]:+.3f}" for e in edges) + " |")
print()
p15 = json.load(open(os.path.join(HERE, "summary_p2_0.15_zeta5.json")))["cases"]
print("| $p_2=0.15$, $\\zeta=5$, $\\delta$ | " + " | ".join(f"{e:.3f}" for e in edges) + " |")
print("|---|" + "---|" * len(edges))
for d in (0.0, 0.942):
    row = {round(c["edge"], 3): c["Ftot_dB_minus_Fs_dB"] for c in p15 if abs(c["delta"] - d) < 1e-2}
    print(f"| {d:g} | " + " | ".join(f"{row[e]:+.3f}" for e in edges) + " |")
tc = json.load(open(os.path.join(HERE, "trapping_check.json")))
for c in tc["cases"]:
    print(f"trapping zeta={c['zeta']}: LP01 centroid {c['LP01']['centroid']:+.3f}, LP02 centroid {c['LP02']['centroid']:+.3f}, "
          f"separation {c['LP01']['centroid'] - c['LP02']['centroid']:.3f} (delta {tc['delta']:.3f}; p2*delta {tc['p2'] * tc['delta']:+.3f}, -p1*delta {-(1 - tc['p2']) * tc['delta']:+.3f})")

print()
# best band: minimum over the scanned edges of F_tot (common band at 0) against the minimum over edges of F_s
import math
def best(cases):
    c = min(cases, key=lambda c: c["computed"]["Ftot"])
    return c["computed"]["Ftot"], c["edge"]
print("| $\\zeta$ | $p_2$ | $\\delta$ | best $F_{\\rm tot}$ (edge) | best $F_s$ (edge) | dB |")
print("|---|---|---|---|---|---|")
sets = [(2, 0.3, runs[2]["cases"]), (5, 0.3, runs[5]["cases"]), (5, 0.15, p15)]
for z, p2, cases in sets:
    fs_min = min((c["Fs_LP01"], c["edge"]) for c in cases)
    for d in (0.0, 0.942):
        sel = [c for c in cases if abs(c["delta"] - d) < 1e-2]
        F, e = best(sel)
        print(f"| {z} | {p2} | {d:g} | {F:.4f} ({e:.3f}) | {fs_min[0]:.4f} ({fs_min[1]:.3f}) | {10 * math.log10(F / fs_min[0]):+.3f} |")
