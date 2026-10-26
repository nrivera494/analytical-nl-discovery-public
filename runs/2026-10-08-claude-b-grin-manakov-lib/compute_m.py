"""Compute and store the spectral-bin covariance for M-mode cases (claude-b, T-20261008-claude-b-01).
Usage: python compute_m.py <run-id> <cases.json>; each case: tag, zeta, p (list), C (matrix), delta (list), optional N, TW, dz.
Stores nbar (M, N), the all-mode totals Ct (N, N) and nt (N) in ~/analytical-nl-discovery-data/<run-id>/<tag>.npz
(the full M N x M N covariance is not kept)."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twomode_cov as tc
import mmode_cov as mm

RAW = os.path.expanduser("~/analytical-nl-discovery-data")
run_id, cases = sys.argv[1], json.load(open(sys.argv[2]))
os.makedirs(os.path.join(RAW, run_id), exist_ok=True)
for c in cases:
    path = os.path.join(RAW, run_id, c["tag"] + ".npz")
    if os.path.exists(path):
        continue
    g = tc.Grid(c.get("N", 256), c.get("TW", 40.0))
    A0, S = mm.launch(g, c["p"], c["C"])
    t0 = time.time()
    nbar, Cov = mm.bin_covariance(g, A0, c["zeta"], c.get("dz", 2e-3), c["C"], c["delta"])
    Ct, nt = mm.totals(nbar, Cov)
    np.savez(path, nbar=nbar, Ct=Ct, nt=nt, zeta=c["zeta"], p=np.array(c["p"]), C=np.array(c["C"]), delta=np.array(c["delta"]),
             N=g.N, TW=g.TW, dz=c.get("dz", 2e-3), Sigma=S, wall=time.time() - t0)
    print(f"{c['tag']}: done in {time.time() - t0:.1f} s", flush=True)
