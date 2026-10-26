#!/usr/bin/env python3
"""Box-relaxation + dithering + tabu binary search (as binary_relax.py) for the Raman models (Blow-Wood, fR = 0.18):
held-out sech (T_s = 188.9 fs, 300 K, Phi = 5, 15; same grid as heldout_eval.py) and Gaussian points
(T0 = 200 and 1000 fs, Phi = 10 and 20, 300 K; same grid as scan_raman.py). Reports the best over this search and the
earlier tabu values. Usage: python binary_relax_raman.py out.json"""
import json, sys, time, warnings
import numpy as np
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, lag_kernels, gaussian_p, sech_p, fano_of, best_improvement, tabu_search

def dither(d, order):
    T = np.zeros_like(d); e = 0.0
    for i in order:
        e += d[i]
        if e >= 0.5:
            T[i] = 1.0; e -= 1.0
    return T

def relax_search(nb, Va, w, rng, n_rand=3):
    s = np.sqrt(nb); Sig = s[:, None] * Va * s[None, :]; M = Sig - np.diag(nb)
    def J(d):
        den = nb @ d; q = d @ M @ d
        return 1 + q / den, (2 * (M @ d) * den - q * nb) / den**2
    order = np.argsort(w)
    wm = np.abs(w[nb > 1e-3 * nb.max()]).max()
    starts = [np.full(len(nb), 0.5), (w > 0).astype(float), (w < 0).astype(float)]
    for a in (0.5, 1.0, 2.0):
        starts.append(np.where(w > 0, np.clip(w / (a * wm), 0, 1), 0.0)); starts.append(np.where(w < 0, np.clip(-w / (a * wm), 0, 1), 0.0))
    starts += [rng.uniform(0, 1, len(nb)) for _ in range(n_rand)]
    best = None
    for d0 in starts:
        r = minimize(J, d0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * len(nb), options={"maxiter": 3000})
        T = dither(r.x, order)
        F1, T1 = best_improvement(T, Sig, nb)
        F2, T2 = tabu_search(T1, Sig, nb, rng)
        F2 = fano_of(T2, nb, Va)
        if best is None or F2 < best:
            best = F2
    return float(best)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "binary_relax_raman.json"
    rng = np.random.default_rng(9)
    prev = {}
    for r in json.load(open("heldout_results.json"))["rows"]:
        prev[("sech", 188.9, r["Phi"], 300.0 if r["case"] == "raman300" else None)] = r["binary_F"]
    for r in json.load(open("scan_raman_gaussian.json"))["rows"]:
        prev[("gaussian", r["T0_fs"], r["Phi"], r["T_K"])] = r["binary_F"]
    cases = [("sech", 188.9, 5.0, 300.0), ("sech", 188.9, 15.0, 300.0),
             ("gaussian", 200.0, 10.0, 300.0), ("gaussian", 200.0, 20.0, 300.0),
             ("gaussian", 1000.0, 10.0, 300.0), ("gaussian", 1000.0, 20.0, 300.0)]
    rows = []
    for (pulse, T0, Phi, TK) in cases:
        t0 = time.time()
        if pulse == "sech":
            # same grid as heldout_eval.py: T0 = 200 fs reference, T_s = 0.9445 T0
            T0g = 200.0
            dt = min(0.8 / Phi, 0.04) * T0g
            t = np.arange(-14 * T0g, 14 * T0g, dt)
            p = sech_p(t, 0.9445 * T0g)
        else:
            dt = min(0.8 / Phi, 0.04) * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
        m = build_model(p, dt, Phi, fR=0.18, temp_K=TK, kern=lag_kernels(len(t), dt, 0.18, TK))
        V = covariance(m)
        nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
        F = relax_search(nb, Va, w, rng)
        key = (pulse, T0, Phi, TK)
        rows.append({"pulse": pulse, "T0_or_Ts_fs": T0, "Phi": Phi, "T_K": TK, "N_t": len(t), "n_bins": int(len(nb)),
                     "binary_relax": F, "binary_tabu_earlier": prev.get(key), "wall_s": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
