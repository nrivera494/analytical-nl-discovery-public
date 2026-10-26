"""Robustness of the binary search (claude-b, T-20261010-claude-interactive-05): long iterated local search on two
points (N20 and N40 at z/z_wb = 0.7), 8 restarts x 2500 perturbations of 1..10 flips, starting from the final filter of
transfer_binary.py and from perturbed copies of it. Writes long_search.json."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
out = {}
for run, tag in (("2026-10-10-claude-b-nd-oracle", "N20_zr0.7"), ("2026-10-10-claude-b-nd-heldout", "N40_zr0.7")):
    d = np.load(os.path.join(RAW, run, tag + ".npz"))
    C, nb = d["C"], d["nbar"]
    T0 = np.load(os.path.join(RAW, run, tag + "_transfer.npz"))["T"].astype(float)
    F0 = nd.fano(T0, C, nb)
    rng = np.random.default_rng(2026)
    best = (F0, T0)
    t0 = time.time()
    hist = []
    for r in range(8):
        T = best[1].copy()
        if r > 0:
            idx = rng.choice(len(nb), size=len(nb) // 10, replace=False)
            T[idx] = 1 - T[idx]
        F, T = nd.flip_descent(T, C, nb)
        F, T = nd.iterated_local_search(T, F, C, nb, rng, n_iter=2500, kmax=10)
        hist.append(F)
        if F < best[0]:
            best = (F, T)
    out[tag] = dict(F_start=F0, F_long=best[0], rel_change=best[0] / F0 - 1, restarts=hist, wall=time.time() - t0)
    print(tag, out[tag], flush=True)
json.dump(out, open(os.path.join(HERE, "long_search.json"), "w"), indent=1)
