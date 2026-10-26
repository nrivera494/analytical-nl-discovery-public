#!/usr/bin/env python3
"""Summary figure: (a) lambda_min, lambda_gen, lambda_P, parity bound, best binary vs Phi (Kerr, Gaussian, dispersionless);
(b) best box-relaxed weight density d(w) and nbar(w) at Phi = 20; (c) lambda_min excess vs y = Phi L/L_D with the
harmonic-oscillator law. Usage: python make_figure.py"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = "~/analytical-nl-discovery-data/2026-10-10-claude-a-dispersionless-fano"
k = json.load(open("scan_kerr_gaussian.json"))["rows"]
par = {r["Phi"]: r for r in json.load(open("parity_bound.json"))["rows"]}
rel = {r["Phi"]: r["best_F"] for r in json.load(open("binary_relax_gaussian.json"))["rows"] if "best_F" in r}
for r in json.load(open("binary_relax2_gaussian.json"))["rows"]:
    if "best_F" in r:
        rel[r["Phi"]] = min(rel.get(r["Phi"], 9), r["best_F"])   # best over all searches (pad 8), as in summary.json
cont = {12.5: 0.4971, 25: 0.4323}
fig, ax = plt.subplots(1, 4, figsize=(17, 4))  # panel (d): polarization with vector Raman
Ph = np.array([r["Phi"] for r in k])
a = ax[0]
PP = np.linspace(1, 50, 300)
a.loglog(PP, 1 + 2 * PP**2 - 2 * PP * np.sqrt(1 + PP**2), "k-", lw=1, label=r"$V_{\min}(\Phi)=\lambda_{\min}(V)$")
a.loglog(PP, 1 / (1 + 4 * PP**2 / (3 * np.sqrt(3))), "b--", lw=1, label=r"$\lambda_P$ (momentum bound)")
a.loglog(Ph, [r["pad8"]["lam_gen"] for r in k], "bo", ms=4, label=r"$\lambda_{\rm gen}$")
pk = sorted(par)
a.loglog(pk, [par[p]["parity_bound"] for p in pk], "gs-", ms=4, lw=0.8, label=r"parity bound $F_{\rm par}$")
tabu = {r["Phi"]: min(r["pad8"]["binary_F"], r["pad4"]["binary_F"]) for r in k}
tabu.update({p: min(tabu.get(p, 9), v) for p, v in cont.items()})
allp = sorted(set(tabu) | set(rel))
best = [min(tabu.get(p, 9), rel.get(p, 9)) for p in allp]
a.loglog(allp, best, "r^-", ms=5, lw=0.8, label="best binary found")
a.set_xlabel(r"$\Phi=\gamma P_0L$"); a.set_ylabel("Fano factor / variance"); a.legend(fontsize=7); a.set_title("(a) Kerr, Gaussian, $L/L_D=0$", fontsize=9)
a = ax[1]
try:
    z = np.load(f"{RAW}/binary_relax_gaussian_Phi20.npz")
    o = np.argsort(z["w"])
    a.plot(z["w"][o] / 20, z["nbar"][o] / z["nbar"].max(), "0.6", lw=0.8, label=r"$\bar n(\omega)$ (norm.)")
    a.plot(z["w"][o] / 20, z["d"][o], "r-", lw=0.8, label=r"box-relaxed local optimum $d(\omega)$")
    a.set_xlabel(r"$\omega T_0/\Phi$"); a.legend(fontsize=7)
except Exception as e:
    a.text(0.1, 0.5, str(e), fontsize=6)
a.set_title(r"(b) best relaxed weight density (local optimum), $\Phi=20$", fontsize=9)
a = ax[2]
L = json.load(open("lam_min_dispersion.json"))["rows"]
for Phi, c in ((2.0, "c"), (5.0, "b"), (10.0, "k"), (20.0, "m"), (40.0, "r")):
    s = sorted([r for r in L if r["Phi"] == Phi and r["dt"] == 0.01 and r["sign_beta2"] == 1 and r["tcut"] == 1.0 and r["nz"] == 200], key=lambda r: r["y_PhiL_over_LD"])
    if s:
        y = np.array([r["y_PhiL_over_LD"] for r in s]); e = np.array([r["excess"] for r in s])
        a.loglog(y, e, "o", color=c, ms=3, label=fr"$\Phi={Phi:g}$")
        a.loglog(y, np.sqrt(2 / 3) * Phi / np.sqrt(1 + Phi**2) * np.sqrt(y), "-", color=c, lw=0.6)
try:
    F = [r for r in json.load(open("lam_min_dispersion_flattop.json"))["rows"] if r["Phi"] == 10.0 and r["dt"] == 0.01]
    F.sort(key=lambda r: r["y_PhiL_over_LD"])
    yf = np.array([r["y_PhiL_over_LD"] for r in F]); ef = np.array([r["excess"] for r in F])
    a.loglog(yf, ef, "ks", mfc="none", ms=5, label=r"flat-top $e^{-t^4}$, $\Phi=10$ (held-out)")
    a.loglog(yf, 0.64226 * 10 / np.sqrt(101) * yf ** (2 / 3), "k--", lw=0.8, label=r"$0.642\,\Phi(1+\Phi^2)^{-1/2}y^{2/3}$")
except Exception as e:
    pass
a.set_xlabel(r"$y=\Phi L/L_D$ ($\beta_2>0$)"); a.set_ylabel(r"$\lambda_{\min}/V_{\min}(\Phi)-1$")
a.legend(fontsize=7); a.set_title(r"(c) lines: $\sqrt{2/3}\,\Phi(1+\Phi^2)^{-1/2}\sqrt{y}$", fontsize=9)
a = ax[3]
try:
    ex = {r["config"]: r for r in json.load(open("vector_raman_exact.json"))["rows"] if r["T0_fs"] == 200.0 and r["T_K"] == 300.0}
    sc = json.load(open("vector_raman_chiscan.json"))["rows"]
    pr = [r for r in json.load(open("vector_raman_prop.json"))["rows"] if r["split"] == "A" and r["T_K"] == 300.0 and abs(r["chi"] - np.pi / 8) < 1e-6]
    pts = [(0.0, ex["linear (a+b, both splits)"]["lam_gen"], ex["linear (a+b, both splits)"]["binary_F"])]
    pts += [(r["chi"], r["lam_gen_insensitive"], r["binary_insensitive"]) for r in sc]
    pts += [(r["chi"], r["lam_gen_insensitive"], r["binary_insensitive"]) for r in pr]
    pts += [(np.pi / 4, ex["circular, split A"]["lam_gen"], ex["circular, split A"]["binary_F"])]
    pts.sort()
    c = [x[0] for x in pts]
    a.plot(c, [x[1] for x in pts], "bo-", ms=4, label=r"$\lambda_{\rm gen}$ (insensitive)")
    a2 = a.twinx(); a2.plot(c, [x[2] for x in pts], "r^-", ms=4, label="best binary")
    a.set_xlabel(r"ellipticity angle $\chi$ (rad)"); a.set_ylabel(r"$\lambda_{\rm gen}$", color="b"); a2.set_ylabel("best binary", color="r")
except Exception as e:
    a.text(0.1, 0.5, str(e), fontsize=6)
a.set_title(r"(d) vector Raman, $T_0=200$ fs, 300 K, $\Phi=10$", fontsize=9)
fig.tight_layout(); fig.savefig("summary.png", dpi=110)
print("ok")
