"""Part 3 check (written after reading the proposer's TECHNICAL_NOTES.md section 7): my full-field code
on the proposer's launch, |U|^2 = c delta log(1+exp((1-x^2)/delta)), delta = 0.25 eps0^(2/3), c: energy 4/3,
asymptotic chirp a'(0)=Gamma/3.  claude-interactive.13."""
import json, os, sys, numpy as np
from fullfield import Grid, lo_covariance
G18 = np.sqrt(18)
def src_seed(x, eps0, Gam=G18):
    d = 0.25 * eps0 ** (2 / 3)
    rho = d * np.logaddexp(0.0, (1 - x**2) / d)
    dx = x[1] - x[0]
    rho *= (4 / 3) / (np.sum(rho) * dx)
    return np.sqrt(rho) * np.exp(-1j * (Gam / 3) * x**2 / (2 * eps0))
fn = "source_seed_summary.json"
out = json.load(open(fn)) if os.path.exists(fn) else {}
jobs = [(0.05, 0.02, 2048, 8.0, 200), (0.05, 0.02, 4096, 8.0, 400), (0.05, 0.02, 4096, 12.0, 800)]
if "tau4" in sys.argv:
    jobs = [(0.05, 4.0, 4096, 16.0, 20000), (0.05, 4.0, 8192, 16.0, 20000), (0.1, 4.0, 4096, 16.0, 10000), (0.025, 4.0, 8192, 16.0, 40000)]
for eps0, tau, N, L, nst in jobs:
    key = f"eps{eps0}_tau{tau}_N{N}_L{L}_steps{nst}"
    if key in out:
        continue
    g = Grid(N, L)
    o = lo_covariance(src_seed(g.x, eps0), g, eps0, G18, tau, nst, nsp=1.0)
    out[key] = dict(lam_min=float(o["lam_min"]), C=o["C"].tolist(), det=float(np.linalg.det(o["C"])), comm_minus_1=float(o["comm"] - 1))
    print(key, "%.10f" % o["lam_min"], np.round(o["C"], 10).tolist(), "det %.10f" % out[key]["det"], "comm-1 %.1e" % out[key]["comm_minus_1"], flush=True)
    json.dump(out, open(fn, "w"), indent=1)
