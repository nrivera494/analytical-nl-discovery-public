"""Edge-of-regime scan for (ii): below the short-length threshold (R<1), is the matched mode squeezed at
some finite length? Full field, complete ASE, n_sp=1, eps0=0.05, unchirped Gaussian and smoothed parabola.
claude-interactive.13."""
import json, numpy as np
from fullfield import Grid, seed, lo_covariance, kappa
eps0 = 0.05; g = Grid(2048, 8.0); out = {}
taus = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0]
for kind in ("gaussian", "parabola"):
    p0 = seed(kind, g.x, delta=0.05)
    kap, rpk = kappa(p0, g)
    for R in ((0.5, 0.85, 0.9, 0.95, 1.0) if kind == "gaussian" else (0.5, 0.7, 0.75, 0.8, 0.85, 0.9)):
        Gam = kap / (eps0 * R)
        rows = []
        for t in taus:
            phi = (np.exp(t) - 1) / (Gam * eps0)            # rough peak nonlinear phase
            nst = int(max(200, 60 * phi))
            o = lo_covariance(p0, g, eps0, Gam, t, nst, nsp=1.0)
            rows.append(dict(tau=t, lam_min=float(o["lam_min"]), steps=nst, comm_minus_1=float(o["comm"] - 1)))
        lmin = min(rows, key=lambda r: r["lam_min"])
        out[f"{kind}_R{R}"] = dict(Gamma=Gam, gammaP0_over_g=rpk / (eps0 * Gam), rows=rows, min_lam=lmin["lam_min"], tau_at_min=lmin["tau"])
        print(kind, R, "Gamma %.2f  min lambda %.4f at tau %.2f" % (Gam, lmin["lam_min"], lmin["tau"]), [round(r["lam_min"], 4) for r in rows], flush=True)
        json.dump(out, open("finite_length_summary.json", "w"), indent=1)
