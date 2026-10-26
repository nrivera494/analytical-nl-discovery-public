#!/usr/bin/env python3
"""Second pass of the box-relaxation binary search with continuation starts: every saved best density d(w) from
binary_relax.py (all Phi, Gaussian) is mapped to the target Phi by nu = w/Phi (linear interpolation), and used, with its
mirror d(-w), as an L-BFGS-B start; then dither + best-improvement + tabu as in binary_relax.py.
Usage: python binary_relax2.py out.json Phis [pad] [n_random_starts]"""
import glob, json, sys, time, warnings
import numpy as np
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p, fano_of, best_improvement, tabu_search
RAW = "~/analytical-nl-discovery-data/2026-10-10-claude-a-dispersionless-fano"

def dither(d, order):
    T = np.zeros_like(d); e = 0.0
    for i in order:
        e += d[i]
        if e >= 0.5:
            T[i] = 1.0; e -= 1.0
    return T

out = sys.argv[1]
Phis = [float(x) for x in sys.argv[2].split(",")]
PAD = int(sys.argv[3]) if len(sys.argv) > 3 else 8
NRAND = int(sys.argv[4]) if len(sys.argv) > 4 else 0
seeds = []
for f in sorted(glob.glob(f"{RAW}/binary_relax*_gaussian_Phi*.npz")):
    z = np.load(f)
    P0 = float(f.split("Phi")[-1].replace(".npz", "").split("_pad")[0])
    o = np.argsort(z["w"])
    seeds.append((P0, z["w"][o] / P0, z["d"][o]))
rows = []
rng = np.random.default_rng(7)
for Phi in Phis:
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=PAD, thr=1e-6)
    s = np.sqrt(nb); Sig = s[:, None] * Va * s[None, :]; M = Sig - np.diag(nb)
    def J(d):
        den = nb @ d; q = d @ M @ d
        return 1 + q / den, (2 * (M @ d) * den - q * nb) / den**2
    order = np.argsort(w)
    best = None
    allseeds = list(seeds) + [(-1.0, None, None)] * NRAND
    for (P0, nu, dd) in allseeds:
        for mirror in ((False, True) if nu is not None else (False,)):
            d0 = np.interp((-w if mirror else w) / Phi, nu, dd, left=0.0, right=0.0) if nu is not None else rng.uniform(0, 1, len(nb))
            if d0.sum() < 1e-9:
                continue
            r = minimize(J, d0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * len(nb), options={"maxiter": 3000})
            T = dither(r.x, order)
            F1, T1 = best_improvement(T, Sig, nb)
            F2, T2 = tabu_search(T1, Sig, nb, rng)
            F2 = fano_of(T2, nb, Va)
            rows.append({"Phi": Phi, "seed_Phi": P0, "mirror": mirror, "J_relaxed": float(r.fun), "F_polished": F2})
            if best is None or F2 < best[0]:
                best = (F2, T2, r.x, P0, mirror)
    rows.append({"Phi": Phi, "pad": PAD, "n_seeds": len(allseeds), "best_F": best[0], "best_seed_Phi": best[3], "best_mirror": best[4],
                 "best_selected": int(best[1].sum()), "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)})
    print(json.dumps(rows[-1]), flush=True)
    np.savez(f"{RAW}/binary_relax2_gaussian_Phi{Phi:g}" + ("" if PAD == 8 else f"_pad{PAD}") + ".npz", T=best[1], d=best[2], w=w, nbar=nb)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
