"""Compute and store the spectral-bin covariance for a list of cases (claude-b, T-20261008-claude-b-01).

Usage: python compute.py <run-id> <cases.json> [i0 i1]
cases.json: list of dicts with keys tag, zeta, p2, C22, delta and optional N, TW, dz, C12,
launch = "photon" (equal photon number instead of the gamma_eff energy) and N2 (amplitude factor sqrt(N2)).
Each case is written to ~/analytical-nl-discovery-data/<run-id>/<tag>.npz (nbar, Cov, parameters, wall time).
Cases already present are skipped, so the script can be restarted or split across processes with [i0 i1).
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twomode_cov as tc

RAW = os.path.expanduser("~/analytical-nl-discovery-data")


def run_case(run_id, c):
    out = os.path.join(RAW, run_id)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, c["tag"] + ".npz")
    if os.path.exists(path):
        return path
    g = tc.Grid(c.get("N", 256), c.get("TW", 40.0))
    C12 = c.get("C12", 1.0)
    C = [[1.0, C12], [C12, c["C22"]]]
    a0, b0, S = tc.launch(g, c["p2"], C)
    if c.get("launch") == "photon":          # equal photon number to the LP01 soliton: drop the 1/sqrt(Sigma)
        a0, b0 = a0 * np.sqrt(S), b0 * np.sqrt(S)
    if "N2" in c:                               # scalar launch with amplitude sqrt(N2) sech (soliton order sqrt(N2))
        a0, b0 = a0 * np.sqrt(c["N2"]), b0 * np.sqrt(c["N2"])
    t0 = time.time()
    nbar, Cov = tc.bin_covariance(g, a0, b0, c["zeta"], c.get("dz", 2e-3), C, c["delta"])
    np.savez(path, nbar=nbar, Cov=Cov, zeta=c["zeta"], p2=c["p2"], C22=c["C22"], C12=C12, delta=c["delta"],
             N=g.N, TW=g.TW, dz=c.get("dz", 2e-3), Sigma=S, wall=time.time() - t0)
    print(f"{c['tag']}: done in {time.time() - t0:.1f} s", flush=True)
    return path


if __name__ == "__main__":
    run_id, cases = sys.argv[1], json.load(open(sys.argv[2]))
    i0, i1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, len(cases))
    for c in cases[i0:i1]:
        run_case(run_id, c)
