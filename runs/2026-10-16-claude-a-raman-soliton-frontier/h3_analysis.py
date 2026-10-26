#!/usr/bin/env python3
"""Assemble the H3 results (Raman-transfer excess of the leading fission soliton) from all scan logs, pick the clean
saturated value per (N, T0), fit the peak position/value and the small-tau_R coefficient, and draw the summary figure.
Clean row: |Re zeta1| < 0.05, not window-limited, photon drift < 1e-4 (s = 0 runs only). Saturated: the clean value at the
largest L changes by < 5% from the previous clean L of the same propagation (or two L values agree when only h3_main has it).
Usage: python h3_analysis.py  (writes h3_summary.json and h3_excess.png)"""
import json, glob
import numpy as np

TR = 1.462   # fs, f_R * int t h(t) dt for Blow-Wood (tau1 = 12.2 fs, tau2 = 32 fs, f_R = 0.18)


def load(path):
    rows = []
    for line in open(path):
        if line.startswith("{"):
            r = json.loads(line)
            r["src"] = path
            rows.append(r)
    return rows


rows = []
for p in ("h3_main.log", "h3_small.log", "h3_dense.log", "h3_heldout.log", "h3_n5peak.log", "h3_n2long.log", "h3_n7.log",
          "h3_n7fine.log", "h3_n8fine.log", "h3_n35.log", "h3_n8peak.log", "h3_c5.log", "h3_n10.log", "h3_c35.log"):
    try:
        rows += load(p)
    except FileNotFoundError:
        pass
for p in ("h3_conv_small.log", "h3_conv.log"):          # finer-step / finer-grid reruns; preferred when present
    try:
        rows += load(p)
    except FileNotFoundError:
        pass
rows = [r for r in rows if r.get("raman", True) and r.get("s", 0) == 0 and r.get("d3", 0) == 0]


def clean(r):
    # N >= 7 on n <= 16384: the most red-shifted soliton reaches the Nyquist edge and is aliased, so the tallest peak is
    # not the leading soliton (diagnostic h3_peaks_N8_T400.json); only the n = 32768 reruns (h3_n7fine, h3_n8fine) count.
    if r["N"] >= 7 and r.get("n", 16384) <= 16384:   # (N = 10 uses 65536)
        return False
    return abs(r["zeta1_re"]) < 0.05 and not r["window_limited"] and abs(r["photon_drift"]) < 1e-4


best = {}
for r in rows:
    Nk = float(r["N"]); Nk = int(Nk) if Nk.is_integer() else Nk      # keep non-integer N (3.5) separate
    key = (Nk, float(r["T0_fs"]))
    best.setdefault(key, []).append(r)
table = []
for (N, T0), rs in sorted(best.items()):
    rs = [r for r in rs if clean(r)]
    if not rs:
        table.append({"N": N, "T0_fs": T0, "eps": None, "note": "no clean row"}); continue
    # prefer the finest step, then the finest grid; within that propagation, the largest clean L
    hmin = min(r["h"] for r in rs); rs = [r for r in rs if r["h"] <= hmin * 1.0001]
    nmax = max(r.get("n", 0) for r in rs); rs = [r for r in rs if r.get("n", 0) == nmax]
    grp = {}
    for r in rs:
        grp.setdefault((r["src"], r.get("tag", ""), r.get("width", 0)), []).append(r)
    rs = sorted(max(grp.values(), key=lambda g: max(r["L_times_N"] for r in g)), key=lambda r: r["L_times_N"])
    last = rs[-1]
    prev = [r for r in rs if r["L_times_N"] < last["L_times_N"]]
    sat = bool(prev) and abs(last["excess"] - prev[-1]["excess"]) <= 0.05 * abs(last["excess"])
    table.append({"N": N, "T0_fs": T0, "tauR": TR / T0, "x": N**2 * TR / T0, "eps": last["excess"], "f1": last["f1_output_ZS"],
                  "f1_sqrtN": last["f1_output_ZS"] * np.sqrt(N), "L_times_N": last["L_times_N"], "saturated": sat,
                  "src": sorted(set(r["src"] for r in rs)), "h": rs[-1]["h"], "n": rs[-1].get("n")})

# peak per N: quadratic fit of eps against ln T0 through the three points around the grid maximum
peaks = {}
for N in sorted(set(t["N"] for t in table)):
    pts = sorted([(t["T0_fs"], t["eps"], t["f1"]) for t in table if t["N"] == N and t["eps"] is not None])
    if len(pts) < 3:
        continue
    T, e, f = map(np.array, zip(*pts))
    j = int(np.argmax(e))
    rec = {"grid_T0_max": float(T[j]), "grid_eps_max": float(e[j]), "grid_f1_max": float(f[j]), "f1max_sqrtN": float(f[j] * np.sqrt(N))}
    if 0 < j < len(T) - 1:
        X = np.log(T[j - 1:j + 2]); c = np.polyfit(X, e[j - 1:j + 2], 2)
        if c[0] < 0:
            lt = -c[1] / (2 * c[0]); rec["fit_T0_star"] = float(np.exp(lt)); rec["fit_eps_star"] = float(np.polyval(c, lt))
            rec["x_star"] = N**2 * TR / rec["fit_T0_star"]
            rec["fit_f1_star"] = (1 + rec["fit_eps_star"]) * (2 * N - 1) / N**2
            rec["fit_f1_star_sqrtN"] = rec["fit_f1_star"] * np.sqrt(N)
    peaks[N] = rec

# small-tau_R coefficient c_N = eps / tau_R at the three longest T0 with saturated values
small = {}
for N in (2, 3, 4, 5):
    pts = sorted([(t["T0_fs"], t["eps"]) for t in table if t["N"] == N and t["eps"] is not None and t["T0_fs"] >= 800 and t["saturated"]])
    if pts:
        small[N] = {"T0_fs": [p[0] for p in pts], "c_N": [p[1] / (TR / p[0]) for p in pts],
                    "local_exponents": [float(np.log(pts[i][1] / pts[i + 1][1]) / np.log(pts[i + 1][0] / pts[i][0])) for i in range(len(pts) - 1)]}

out = {"T_R_fs": TR, "table": table, "peaks": {str(k): v for k, v in peaks.items()}, "small_tauR": {str(k): v for k, v in small.items()}}
json.dump(out, open("h3_summary.json", "w"), indent=1)
for t in table:
    if t["eps"] is not None:
        print(f'N={t["N"]} T0={t["T0_fs"]:6.0f} x={t["x"]:.4f} eps={t["eps"]:+.4f} f1={t["f1"]:.4f} f1*sqrtN={t["f1_sqrtN"]:.3f} LN={t["L_times_N"]:.0f} sat={t["saturated"]}')
print(json.dumps({"peaks": out["peaks"], "small_tauR": out["small_tauR"]}, indent=1))

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    for N in sorted(set(t["N"] for t in table)):
        pts = sorted([(t["x"], t["eps"], t["T0_fs"]) for t in table if t["N"] == N and t["eps"] is not None])
        if not pts:
            continue
        x, e, T = map(np.array, zip(*pts))
        ax[0].semilogx(x, e, "o-", label=f"N={N}")
        ax[1].loglog(TR / T, e, "o-", label=f"N={N}")
    ax[0].set_xlabel(r"$x=N^2T_R/T_0$"); ax[0].set_ylabel(r"excess $\varepsilon=f_1(L)/f_1^{\rm IST}-1$"); ax[0].legend(fontsize=7)
    ax[0].axvline(0.11, color="k", lw=0.5, ls=":")
    tt = np.array([3e-4, 3e-3]); ax[1].loglog(tt, 5.0 * tt, "k:", lw=0.8, label=r"$5\,\tau_R$")
    ax[1].set_xlabel(r"$\tau_R=T_R/T_0$"); ax[1].set_ylabel(r"$\varepsilon$"); ax[1].legend(fontsize=7)
    Ns = sorted(peaks); fs = [peaks[N].get("fit_f1_star", peaks[N]["grid_f1_max"]) for N in Ns]
    ax[2].plot(Ns, fs, "o", label=r"peak $f_1^*$ (fit or grid max)")
    nn = np.linspace(2, 8, 50); ax[2].plot(nn, 1.3 / np.sqrt(nn), "k-", lw=0.8, label=r"$1.3/\sqrt{N}$")
    ax[2].plot(nn, (2 * nn - 1) / nn**2, "k--", lw=0.8, label=r"IST $(2N-1)/N^2$")
    ax[2].plot(nn, 2 / nn, "k:", lw=0.8, label=r"$2/N$ (passive-mask input bound)")
    ax[2].set_xlabel("N"); ax[2].set_ylabel(r"leading-soliton fraction $f_1$"); ax[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig("h3_excess.png", dpi=110)
except Exception as exc:   # figure is optional
    print("figure failed:", exc)
