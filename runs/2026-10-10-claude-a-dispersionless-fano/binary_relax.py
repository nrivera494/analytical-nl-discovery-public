#!/usr/bin/env python3
"""Binary-filter search through the box extension of the binary objective.
For binary T, F[T] = T'Sig T / T'nbar = 1 + T'(Sig - D)T / nbar'T with D = diag(nbar) (uses T_i^2 = T_i).
J(d) = 1 + d'(Sig - D)d / nbar'd extends it to d in [0,1]^n. Error-diffusion dithering of d over frequency-sorted bins
realizes J(d) closely (dither error is high-'quefrency', i.e. lands at dark delays as vacuum; see dither_ramp.json).
Search: L-BFGS-B local minima of J from several starts -> dither -> exact F -> tabu polish (dlfano.tabu_search).
This is a search heuristic (upper bounds on min_T F), not a certificate. Usage: python binary_relax.py out.json [Phis] [pulse] [pad]"""
import json, sys, time, warnings
import numpy as np
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, gaussian_p, fano_of, best_improvement, tabu_search

def dither(d, order):
    T = np.zeros_like(d); e = 0.0
    for i in order:
        e += d[i]
        if e >= 0.5:
            T[i] = 1.0; e -= 1.0
    return T

out = sys.argv[1] if len(sys.argv) > 1 else "binary_relax.json"
Phis = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [5.0, 10.0, 20.0]
pulse = sys.argv[3] if len(sys.argv) > 3 else "gaussian"
PAD = int(sys.argv[4]) if len(sys.argv) > 4 else 8
RAW = "~/analytical-nl-discovery-data/2026-10-10-claude-a-dispersionless-fano"
from dlfano import sech_p
rows = []
rng = np.random.default_rng(5)
for Phi in Phis:
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi)
    if pulse == "gaussian":
        t = np.arange(-7, 7, dt); p = gaussian_p(t)
    else:
        t = np.arange(-14, 14, dt); p = sech_p(t, 0.9445)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=PAD, thr=1e-6)
    s = np.sqrt(nb); Sig = s[:, None] * Va * s[None, :]; M = Sig - np.diag(nb)
    scale = nb.sum()
    def J(d):
        den = nb @ d
        q = d @ M @ d
        val = 1 + q / den
        g = (2 * (M @ d) * den - q * nb) / den**2
        return val, g
    order = np.argsort(w)
    starts = [np.full(len(nb), 0.5), (w > 0).astype(float), np.clip(0.5 + 0.5 * w / np.abs(w).max(), 0, 1)]
    wm = np.abs(w[nb > 1e-3 * nb.max()]).max()
    for a in (0.5, 1.0, 2.0):
        starts.append(np.where(w > 0, np.clip(w / (a * wm), 0, 1), 0.0))
    starts += [rng.uniform(0, 1, len(nb)) for _ in range(3)]
    best = None
    for k, d0 in enumerate(starts):
        r = minimize(J, d0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * len(nb), options={"maxiter": 3000})
        d = r.x
        T = dither(d, order)
        Fd = fano_of(T, nb, Va)
        F1, T1 = best_improvement(T, Sig, nb)
        F2, T2 = tabu_search(T1, Sig, nb, rng)
        F2 = fano_of(T2, nb, Va)
        frac_int = float(np.mean((d < 1e-6) | (d > 1 - 1e-6)))
        row = {"pulse": pulse, "Phi": Phi, "start": k, "J_relaxed": float(r.fun), "F_dithered": Fd, "F_polished": F2,
               "frac_integral": frac_int, "n_bins": int(len(nb)), "n_selected": int(T2.sum())}
        rows.append(row); print(json.dumps({kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in row.items()}), flush=True)
        if best is None or F2 < best[0]:
            best = (F2, T2, d)
    rows.append({"pulse": pulse, "Phi": Phi, "pad": PAD, "best_F": best[0], "best_selected": int(best[1].sum()), "n_bins": int(len(nb)), "wall_s": round(time.time() - t0, 1)})
    print(json.dumps(rows[-1]), flush=True)
    np.savez(f"{RAW}/binary_relax_{pulse}_Phi{Phi:g}" + ("" if PAD == 8 else f"_pad{PAD}") + ".npz", T=best[1], d=best[2], w=w, nbar=nb)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
