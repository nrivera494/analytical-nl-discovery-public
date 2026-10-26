#!/usr/bin/env python3
"""Binary-filter continuation in Phi (Kerr only, Gaussian): the optimum at one Phi, mapped by nu = omega/Phi, seeds
the search at the next Phi (both directions). Usage: python continuation.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, lam_gen, binary_search4, gaussian_p, best_improvement, tabu_search

out = sys.argv[1]
Phis = [10, 12.5, 15, 17.5, 20, 25, 30]
pad = 8
data = {}
for Phi in Phis:
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=pad, thr=1e-6)
    data[Phi] = (nb, Va, w)
best = {}
rng = np.random.default_rng(5)
def mapped(Tsrc, wsrc, Phisrc, wdst, Phidst):
    nus, nud = wsrc / Phisrc, wdst / Phidst
    o = np.argsort(nus)
    return np.interp(nud, nus[o], Tsrc[o]) > 0.5
# initial independent searches
for Phi in Phis:
    nb, Va, w = data[Phi]
    r = binary_search4(nb, Va, w)
    best[Phi] = (r["F"], r["T"])
    print(f"independent Phi={Phi}: F={r['F']:.4f}", flush=True)
# two sweeps of continuation (up and down)
for sweep in range(2):
    order = Phis if sweep % 2 == 0 else Phis[::-1]
    for a, b in zip(order[:-1], order[1:]):
        nb, Va, w = data[b]
        s = np.sqrt(nb); Sig = s[:, None] * Va * s[None, :]
        Ta = best[a][1]; wa = data[a][2]
        T0 = mapped(Ta, wa, a, w, b).astype(float)
        F1, T1 = best_improvement(T0, Sig, nb)
        F2, T2 = tabu_search(T1, Sig, nb, rng, n_iter=40 * len(nb))
        if F2 < best[b][0]:
            best[b] = (F2, T2)
        print(f"sweep {sweep} {a}->{b}: seeded F={F2:.4f}, best now {best[b][0]:.4f}", flush=True)
res = {str(P): {"binary_F": best[P][0], "n_bins": int(len(data[P][0])), "selected": int(best[P][1].sum()),
                "lam_gen": lam_gen(data[P][1])} for P in Phis}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res))
