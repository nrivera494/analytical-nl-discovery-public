"""Summary and scaling figure for the large-N binary-filter study (claude-b, T-20261010-claude-interactive-05,
continuation). Combines the oracle grid (runs 2026-10-10-claude-b-nd-oracle, -heldout; finite differences) with the
adjoint-based large-N points of this run (N = 56, 80, 112), using the best binary values after the extra search
(big_search.json). Fits log-log slopes of the best binary F, the parity bound, lambda_even and the non-negative-weight
heuristic over N >= 20. Writes summary.json and fig_scaling.png."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
ORA = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle")
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-11-claude-b-nd-binary-theory")
S = {p["tag"]: p for p in json.load(open(os.path.join(ORA, "summary.json")))["points"]}
PB = json.load(open(os.path.join(ORA, "parity_bound.json")))
big = {json.loads(l)["tag"]: json.loads(l) for l in open(os.path.join(RAW, "rows.jsonl"))}
bs = json.load(open(os.path.join(HERE, "big_search.json")))
pts = {}
for zr in (0.3, 0.7, 1.0, 1.5):
    rows = []
    for p in sorted([q for q in S.values() if q["zr"] == zr and q["s"] == 0 and q["resolved"]], key=lambda q: q["N"]):
        rows.append(dict(N=p["N"], source="oracle (finite differences)", lam_gen=p["lam_gen"], lam_even=PB[p["tag"]]["lam_even"],
                         F_par=PB[p["tag"]]["F_par"], F_nonneg=p["F_nonneg_heuristic"], F_bin=p["F_bin"], F_interval=p["F_interval"]))
    for t, r in sorted(big.items(), key=lambda kv: kv[1]["N"]):
        if r["zr"] == zr:
            Fb = min(r["F_bin"], bs.get(t, {}).get("F_new", r["F_bin"]))
            rows.append(dict(N=r["N"], source="adjoint", lam_gen=r["lam_gen"], lam_even=r["lam_even"], F_par=r["F_par"],
                             F_nonneg=r["F_nonneg_heuristic"], F_bin=Fb, F_interval=r["F_interval"], centroid_check=r["centroid_check"]))
    fits = {}
    for q in ("F_bin", "F_par", "lam_even", "F_nonneg", "lam_gen"):
        Ns = np.array([r["N"] for r in rows if r["N"] >= 20]); y = np.array([r[q] for r in rows if r["N"] >= 20])
        sl, ic = np.polyfit(np.log(Ns), np.log(y), 1)
        last = np.log(y[-1] / y[-2]) / np.log(Ns[-1] / Ns[-2])
        fits[q] = dict(slope_N_ge_20=float(sl), prefactor=float(np.exp(ic)), last_local_slope=float(last), N_range=[int(Ns[0]), int(Ns[-1])])
    pts[str(zr)] = dict(rows=rows, fits=fits)
json.dump(pts, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
for zr, d in pts.items():
    print("z/z_wb =", zr)
    for q, f in d["fits"].items():
        print("   %-9s slope %.2f (N %d-%d), prefactor %.3f, last local slope %.2f" % (q, f["slope_N_ge_20"], f["N_range"][0], f["N_range"][1], f["prefactor"], f["last_local_slope"]))
fig, axs = plt.subplots(1, 4, figsize=(18, 4.3), sharey=True)
for ax, zr in zip(axs, ("0.3", "0.7", "1.0", "1.5")):
    R = pts[zr]["rows"]
    N = [r["N"] for r in R]
    for q, sty, lab in (("F_bin", "mo-", "best binary found"), ("F_nonneg", "c^-", "non-negative weights (heuristic)"),
                        ("lam_even", "gs-", r"$\lambda_{\rm even}$"), ("F_par", "gd--", "parity bound (C-20261010-claude-a-03)"),
                        ("lam_gen", "r.-", r"$\lambda_{\rm gen}$ (odd, centroid)")):
        ax.plot(N, [r[q] for r in R], sty, ms=4, label=lab)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("N"); ax.set_title(f"z/z_wb = {zr} (large N: adjoint)")
    ax.grid(True, which="both", alpha=0.3)
axs[0].set_ylabel("Fano factor"); axs[0].legend(fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_scaling.png"), dpi=110)
