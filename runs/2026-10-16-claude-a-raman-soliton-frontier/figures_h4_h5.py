#!/usr/bin/env python3
"""Small summary figures: H4 headroom by case (best real gain over TL, with the integrable-limit conjecture bound) and H5
leading-soliton timing-jitter ratios versus N. Numbers are read from the run files (no hand-typed values).
Usage: python figures_h4_h5.py  -> h4_headroom.png, h5_jitter_ratios.png"""
import json, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

cases = []
for f, lab in (("h4_N2_T100_d0_phi.json", "N=2\n100 fs"), ("h4_N3_T100_d0_phi.json", "N=3\n100 fs"),
               ("h4_N4_T100_d0_phi.json", "N=4\n100 fs"), ("h4_N4_T200_d0_phi.json", "N=4\n200 fs")):
    d = json.load(open(f)); cases.append((lab, d["headroom"] - 1, d["integrable_bound_factor"]))
for f, lab in (("h4grad_N3_T100.json", "N=3 100 fs\n11-par grad"), ("h4grad_N3_T140.json", "N=3 140 fs\n11-par grad"), ("h4grad_N4_T100.json", "N=4 100 fs\n11-par grad"), ("h4grad_N5_T280.json", "N=5 280 fs\n7-par grad")):
    try:
        d = json.load(open(f)); cases.append((lab, d["headroom"] - 1, 6 / 5))
    except FileNotFoundError:
        pass
try:
    am = json.load(open("h4_adjoint_measure_N4_T200.json"))["rows"]
    cases.append(("N=4 200 fs\n15-par adjoint", max(r["f1_ZS"] for r in am[1:]) / am[0]["f1_ZS"] - 1, 8 / 7))
except (FileNotFoundError, IndexError):
    pass
try:
    s6 = json.load(open("h4_scan6_T100.json"))["rows"]
    cases.append(("N=6\n100 fs (scan)", max(r["ratio_to_TL"] for r in s6) - 1, 12 / 11))
except FileNotFoundError:
    pass
rc = {}
for f in ("h4_recheck.json", "h4_recheck_N4d005.json"):
    try:
        for r in json.load(open(f))["rows"]:
            if r["d3"] > 0:
                rc[(r["N"], r["mask"])] = r["f1_ZS_local"]
    except FileNotFoundError:
        pass
for N in (3.0, 4.0):
    if (N, "TL") in rc and (N, "best") in rc:
        cases.append((f"N={int(N)} 100 fs\nd3=0.05 (local ZS)", rc[(N, "best")] / rc[(N, "TL")] - 1, 2 * N / (2 * N - 1)))
fig, ax = plt.subplots(figsize=(8, 3.2))
x = np.arange(len(cases))
ax.bar(x, [100 * c[1] for c in cases], color="tab:blue")
ax.set_xticks(x); ax.set_xticklabels([c[0] for c in cases], fontsize=7)
ax.set_ylabel("best gain over TL (%)"); ax.axhline(5, color="k", ls=":", lw=0.8)
ax.text(len(cases) - 0.5, 5.2, "frozen 5% line", fontsize=7, ha="right")
ax.set_title("H4: best phase-shaping gain found (achievable lower bounds; card's conjecture bound: 48-68%)", fontsize=9)
fig.tight_layout(); fig.savefig("h4_headroom.png", dpi=110)

pat = re.compile(r"^N=(\d) T0=100 fs .*ratios vac ([\d.]+) ram ([\d.]+) total ([\d.]+)")
patF = re.compile(r"FIXEDSHIFT N=(\d) T0=100 fs.*ratios vac ([\d.]+) ram ([\d.]+) total ([\d.]+)")
rows = {}
for f in ("h5_jitter.log", "h5_jitter_N45.log"):
    try:
        for line in open(f):
            m = pat.search(line)
            if m:
                rows[int(m.group(1))] = tuple(float(m.group(i)) for i in (2, 3, 4))
    except FileNotFoundError:
        pass
rowsF = {}
for line in open("h5_jitter_fixedshift.log"):
    m = patF.search(line)
    if m:
        rowsF[int(m.group(1))] = tuple(float(m.group(i)) for i in (2, 3, 4))
Ns = sorted(rows)
fig, ax = plt.subplots(figsize=(4.6, 3.4))
for k, lab in enumerate(("vacuum", "Raman bath", "total")):
    ax.semilogy(Ns, [rows[n][k] for n in Ns], "o-", label=lab + " (same length)")
for k, lab in enumerate(("vacuum", "Raman bath", "total")):
    NF = sorted(rowsF)
    ax.semilogy(NF, [rowsF[n][k] for n in NF], "s--", label=lab + " (fixed shift)")
ax.axhline(1, color="k", lw=0.6)
ax.set_xlabel("N (TL sech, T0 = 100 fs, L = 4 L_D/N)"); ax.set_ylabel("variance ratio: leading / isolated")
ax.set_title("H5: timing jitter of the leading soliton", fontsize=9); ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig("h5_jitter_ratios.png", dpi=110)
print("cases", [(c[0].replace("\n", " "), round(100 * c[1], 2)) for c in cases]); print("H5", rows)
