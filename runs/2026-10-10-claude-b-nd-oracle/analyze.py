"""Scoring of the oracle grid against the semiclassical formulas (claude-b, T-20261010-claude-interactive-05).

Inputs: rows.jsonl and the stored arrays of runs 2026-10-10-claude-b-nd-oracle and 2026-10-10-claude-b-nd-heldout;
binary_transfer.json (final binary search stage); the reduced curves of run 2026-10-10-claude-b-nd-semiclassical
(curve_N200.json if present, else curve_N100.json, else curve_N50.json).

Per point (pure Kerr, s = 0):
  formula      Lambda(Z)/N^2, Lambda = 1/sigma_1(C_Z)^2   (leading order of lambda_min)
  formula_pass Pi(Z)/N^2,     Pi = 1/sigma_2(C_Z)^2       (leading order of lambda_pass, odd sector)
  F_centroid   <dw^2>_in/<dw^2>_out from the output mean spectrum (exact Fano of the spectral-centroid readout,
               an upper bound on lambda_gen); centroid_check = Fano of w = omega - mean computed from the stored count
               covariance divided by F_centroid (1 when the grid conserves momentum; used as a resolution flag)
  F_bin        best binary filter found (three search stages), with its photon fraction
  gaps in dB   10 log10(F_bin / x) for x = formula, lambda_gen, lambda_min, lambda_pass; and 10 log10(F_centroid / lambda_gen)
Per z/z_wb: relative error of lambda_min against the formula and its exponent in N (log-log slope over resolved N >= 10),
same for lambda_pass; exponent of F_bin in N.
Writes summary.json and fig_bounds.png.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
SC = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-semiclassical")
RHO0SQ, RHO0 = np.sqrt(np.pi / 2), np.sqrt(np.pi)

for name in ("curve_N200.json", "curve_N100.json", "curve_N50.json"):
    if os.path.exists(os.path.join(SC, name)):
        curve = json.load(open(os.path.join(SC, name)))
        break
cr = sorted(curve["rows"], key=lambda r: r["Z"])
# beyond the primary curve (Z > 3.3) use the long N = 50 curve (curve_N50_long.json, 80 T0 window) if present
if os.path.exists(os.path.join(SC, "curve_N50_long.json")):
    zmax = cr[-1]["Z"]
    cr += sorted([r for r in json.load(open(os.path.join(SC, "curve_N50_long.json")))["rows"] if r["Z"] > zmax + 1e-9],
                 key=lambda r: r["Z"])
cZ = np.array([r["Z"] for r in cr])
fL = np.array([4 * r["Z"] ** 2 * r["Lambda_red"] for r in cr])
fP = np.array([4 * r["Z"] ** 2 / r["sigma2_C"] ** 2 for r in cr])
fK = np.array([(RHO0SQ - r["int_rho2"]) / RHO0 / r["Z"] ** 2 for r in cr])


def Lam(Z):
    return float(np.interp(Z, cZ, fL)) / (4 * Z ** 2)


def Pi(Z):
    return float(np.interp(Z, cZ, fP)) / (4 * Z ** 2)


def K(Z):
    return float(np.interp(Z, cZ, fK)) * Z ** 2


def dB(x):
    return float(10 * np.log10(x))


fin = json.load(open(os.path.join(HERE, "binary_transfer.json")))
pts = []
for run in ("2026-10-10-claude-b-nd-oracle", "2026-10-10-claude-b-nd-heldout"):
    for l in open(os.path.join(RAW, run, "rows.jsonl")):
        r = json.loads(l)
        tag = r["tag"]
        d = np.load(os.path.join(RAW, run, tag + ".npz"))
        al, w = d["alpha"], d["w"]
        n = np.abs(al) ** 2
        wb = (n * w).sum() / n.sum()
        om2 = (n * (w - wb) ** 2).sum() / n.sum()
        F_centroid = 0.5 / om2
        wc = w[d["keep"]] - wb
        F_c_cov = float(wc @ d["C"] @ wc / (wc @ (d["nbar"] * wc)))
        N, Z = r["N"], r["N"] * r["xi"]
        fb = fin.get(tag, {})
        F_bin = fb.get("F_binary_final", r["F_best"])
        if Z > cZ[-1] + 1e-9:
            print("skipping", tag, "(Z beyond the reduced curve)")
            continue
        p = dict(tag=tag, run=run, heldout=run.endswith("heldout"), N=N, zr=r["zr"], s=r["s"], Z=Z, Phi_peak=r["Phi_peak"],
                 Nt=r["Nt"], TW=r["TW"], lam_min=r["lam_min"], lam_pass=r["lam_pass"], lam_gen=r["lam_gen"],
                 F_bin=F_bin, F_bin_photon_fraction=fb.get("photon_fraction_on_final"), F_interval=r["F_interval"],
                 F_symband=r["F_symband"], F_nonneg_heuristic=fb.get("F_nonneg_heuristic"),
                 F_centroid=F_centroid, centroid_check=F_c_cov / F_centroid,
                 resolved=bool(abs(F_c_cov / F_centroid - 1) < 1e-3) if r["s"] == 0 else None,
                 formula=Lam(Z) / N ** 2, formula_pass=Pi(Z) / N ** 2,
                 F_centroid_largeN=1 / (1 + 2 * N ** 2 * K(Z)))
        p["err_formula"] = p["lam_min"] / p["formula"] - 1
        p["err_formula_pass"] = p["lam_pass"] / p["formula_pass"] - 1
        p["gap_dB_bin_vs_formula"] = dB(F_bin / p["formula"])
        p["gap_dB_bin_vs_gen"] = dB(F_bin / p["lam_gen"])
        p["gap_dB_bin_vs_min"] = dB(F_bin / p["lam_min"])
        p["gap_dB_bin_vs_pass"] = dB(F_bin / p["lam_pass"])
        p["gap_dB_centroid_vs_gen"] = dB(F_centroid / p["lam_gen"])
        p["gap_dB_gen_vs_min"] = dB(p["lam_gen"] / p["lam_min"])
        pts.append(p)
pts.sort(key=lambda p: (p["s"], p["zr"], p["N"]))
by = {}
for zr in sorted({p["zr"] for p in pts if p["s"] == 0}):
    P = [p for p in pts if p["zr"] == zr and p["s"] == 0]
    res = {"N": [p["N"] for p in P], "Z": [p["Z"] for p in P], "resolved": [p["resolved"] for p in P]}
    for key in ("err_formula", "err_formula_pass"):
        Q = [p for p in P if p["resolved"] and p["N"] >= 10 and abs(p[key]) > 0]
        if len(Q) >= 2:
            res[key + "_exponent"] = float(np.polyfit(np.log([q["N"] for q in Q]), np.log([abs(q[key]) for q in Q]), 1)[0])
            res[key + "_fit_N"] = [q["N"] for q in Q]
    Q = [p for p in P if p["resolved"] and p["N"] >= 10]
    if len(Q) >= 2:
        res["F_bin_exponent"] = float(np.polyfit(np.log([q["N"] for q in Q]), np.log([q["F_bin"] for q in Q]), 1)[0])
        res["F_nonneg_exponent"] = float(np.polyfit(np.log([q["N"] for q in Q]), np.log([q["F_nonneg_heuristic"] for q in Q]), 1)[0])
    by[str(zr)] = res
json.dump(dict(curve=dict(N=curve["N"], Nt=curve["Nt"], M=curve["M"], Zmax=float(cZ[-1])), points=pts, by_zr=by),
          open(os.path.join(HERE, "summary.json"), "w"), indent=1)

print("tag                 N   Z     res  N2lmin  N2form  err%    N2lpass N2Pi  err%   N2lgen N2Fcen  |  F_bin  frac  | gaps dB: form  gen   min  pass | cen-gen gen-min")
for p in pts:
    N2 = p["N"] ** 2
    print(f"{p['tag']:19s} {p['N']:2d} {p['Z']:5.3f} {str(p['resolved'])[0]} {N2*p['lam_min']:7.4f} {N2*p['formula']:7.4f} {100*p['err_formula']:+6.2f} "
          f"{N2*p['lam_pass']:7.4f} {N2*p['formula_pass']:6.4f} {100*p['err_formula_pass']:+6.2f} {N2*p['lam_gen']:7.3f} {N2*p['F_centroid']:7.3f} | "
          f"{p['F_bin']:.4f} {p['F_bin_photon_fraction'] if p['F_bin_photon_fraction'] is not None else float('nan'):.3f} | "
          f"{p['gap_dB_bin_vs_formula']:5.1f} {p['gap_dB_bin_vs_gen']:5.1f} {p['gap_dB_bin_vs_min']:5.1f} {p['gap_dB_bin_vs_pass']:5.1f} | "
          f"{p['gap_dB_centroid_vs_gen']:5.2f} {p['gap_dB_gen_vs_min']:5.2f}{' H' if p['heldout'] else ''}")
for zr, r in by.items():
    print(zr, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if "exponent" in k or k.endswith("fit_N")})

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
Zg = np.exp(np.linspace(np.log(0.1), np.log(cZ[-1]), 400))   # the reduced curve is basis-truncated below Z = 0.1
ax[0].plot(Zg, [Lam(z) for z in Zg], "k-", label=r"$\Lambda(Z)=\sigma_1(C_Z)^{-2}$")
ax[0].plot(Zg, [Pi(z) for z in Zg], "b-", label=r"$\Pi(Z)=\sigma_2(C_Z)^{-2}$")
ax[0].plot(Zg, [1 / (2 * K(z)) for z in Zg], "r-", label=r"$1/(2K(Z))$ (centroid)")
ax[0].plot(Zg, (1 + 2 / np.sqrt(6) * Zg) / (4 * Zg ** 2), "k:", label=r"$(1+0.816Z)/(4Z^2)$")
for p in pts:
    if p["s"] != 0 or not p["resolved"]:
        continue
    N2 = p["N"] ** 2
    a = min(1, 0.25 + p["N"] / 40)
    ax[0].plot(p["Z"], N2 * p["lam_min"], "ko", ms=3, alpha=a)
    ax[0].plot(p["Z"], N2 * p["lam_pass"], "bs", ms=3, alpha=a)
    ax[0].plot(p["Z"], N2 * p["lam_gen"], "r^", ms=3, alpha=a)
ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel(r"$Z=z/\sqrt{L_DL_{NL}}$"); ax[0].set_ylabel(r"$N^2\lambda$")
ax[0].axvline(1.25, color="gray", lw=0.8, ls="--"); ax[0].legend(fontsize=7); ax[0].set_title("bounds x N^2 (points: oracle N=5..40)")
for zr, c in ((0.3, "C0"), (0.7, "C1"), (1.0, "C2"), (1.5, "C3")):
    P = [p for p in pts if p["zr"] == zr and p["s"] == 0]
    ax[1].plot([p["N"] for p in P], [p["F_bin"] for p in P], "o-", color=c, label=f"best binary, z/z_wb={zr}")
    ax[1].plot([p["N"] for p in P], [p["lam_gen"] for p in P], "^--", color=c, ms=3)
    ax[1].plot([p["N"] for p in P], [p["formula"] for p in P], ":", color=c)
ax[1].set_xscale("log"); ax[1].set_yscale("log"); ax[1].set_xlabel("N"); ax[1].set_ylabel("F")
ax[1].set_title("best binary (o), lambda_gen (^), Lambda/N^2 (dotted)"); ax[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_bounds.png"), dpi=110)
