"""K(zeta; T) for every hard interval filter T = [k1, k2] (any position and width with at least 0.5% of the photons),
from the stored covariances of run 2026-10-08-claude-b-kw-map (claude-b, T-20261008-claude-b-01).
K0 = 2 K(p2 = 0.1) - K(p2 = 0.2) at each interval. Reports, for each zeta, the fraction of intervals with K0 < 0 and the
largest K0. Writes all_intervals.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc
from analysis import load, q2

RID = "2026-10-08-claude-b-kw-map"


def interval_F(g, Ct, nt):
    o = g.order
    Cs, ns = Ct[np.ix_(o, o)], nt[o]
    N = len(ns)
    P = np.zeros((N + 1, N + 1))
    P[1:, 1:] = np.cumsum(np.cumsum(Cs, axis=0), axis=1)
    pn = np.concatenate([[0.0], np.cumsum(ns)])
    i1, i2 = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
    V = P[i2 + 1, i2 + 1] - P[i1, i2 + 1] - P[i2 + 1, i1] + P[i1, i1]
    M = pn[i2 + 1] - pn[i1]
    return V, M, i1 <= i2


out = {}
for z in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0):
    zt = f"z{z:g}"
    g, Cs, ns, _ = load(RID, f"{zt}_scalar")
    Vs, Ms, valid = interval_F(g, Cs, ns)
    mask = valid & (Ms > 5e-3 * Ms.max())
    Fs = np.where(mask, Vs / np.where(mask, Ms, 1), np.nan)
    K = []
    for p2 in (0.1, 0.2):
        _, Ct, nt, _ = load(RID, f"{zt}_K_p2_{p2:g}")
        V, M, _ = interval_F(g, Ct, nt)
        F = np.where(mask, V / np.where(mask, M, 1), np.nan)
        K.append((F - Fs) / q2(p2, 1, 0.5))
    K0 = 2 * K[0] - K[1]
    vals = K0[mask]
    out[zt] = dict(n_intervals=int(mask.sum()), frac_negative=float(np.mean(vals < 0)), max_K0=float(np.max(vals)),
                   min_K0=float(np.min(vals)))
    print(zt, out[zt], flush=True)
json.dump(out, open(os.path.join(HERE, "all_intervals.json"), "w"), indent=1)
