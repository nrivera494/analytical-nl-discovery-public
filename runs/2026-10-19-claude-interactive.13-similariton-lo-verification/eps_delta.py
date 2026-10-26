"""Full field vs reduced at tau=2 and 4: separate eps0 and seed-smoothing (delta) effects.
Memory-safe (checkpointed adjoint). claude-interactive.13."""
import json, os, numpy as np
from fullfield import Grid, seed, lo_covariance
G18 = np.sqrt(18)
fn = "eps_delta_summary.json"
out = json.load(open(fn)) if os.path.exists(fn) else {}
for t in (2.0, 4.0):
    for eps0 in (0.05, 0.025):
        for d in (0.05, 0.02):
            key = f"tau{t}_eps{eps0}_delta{d}"
            if key in out:
                continue
            N = 8192 if (eps0 < 0.04 or d < 0.04) else 4096
            g = Grid(N, 16.0); p0 = seed("parabola", g.x, delta=d, chirp=np.sqrt(2), eps0=eps0)
            nst = int(1000 * t / eps0 * 0.05 * (1 + t))
            o = lo_covariance(p0, g, eps0, G18, t, nst, nsp=1.0)
            out[key] = dict(lam_min=float(o["lam_min"]), e2CPP_over_G=float(eps0**2 * o["C"][1, 1] / np.exp(t)),
                            CAP_eps=float(eps0 * o["C"][0, 1] / np.exp(t)), comm_minus_1=float(o["comm"] - 1), N=N, steps=nst)
            print(key, out[key], flush=True)
            json.dump(out, open(fn, "w"), indent=1)
