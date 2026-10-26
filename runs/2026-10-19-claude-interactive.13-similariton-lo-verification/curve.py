"""Full-field lambda_LO(tau) and C_PP, C_AA to tau=4 against the reduced model (asymptotic seed,
Gamma=sqrt18, n_sp=1), eps0 = 0.05 and 0.025.  claude-interactive.13."""
import json, os, sys, time, numpy as np
from fullfield import Grid, seed, lo_covariance
from reduced import run, lo_quantities
G18 = np.sqrt(18)
res = {}
# step/grid convergence at tau=4, eps0=0.05
conv = {}
for (N, L, nst) in ((4096, 16.0, 2000), (4096, 16.0, 4000), (8192, 16.0, 4000), (4096, 24.0, 4000)):
    g = Grid(N, L); p0 = seed("parabola", g.x, delta=0.05, chirp=np.sqrt(2), eps0=0.05)
    t0 = time.time(); o = lo_covariance(p0, g, 0.05, G18, 4.0, nst, nsp=1.0)
    conv[f"N{N}_L{L}_steps{nst}"] = dict(lam_min=o["lam_min"], C=o["C"].tolist(), comm_minus_1=o["comm"] - 1, wall=time.time() - t0)
    print("conv", N, L, nst, o["lam_min"], o["comm"] - 1, flush=True)
res["tau4_convergence_eps0.05"] = conv
taus = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
red_t = np.array(taus)
o_red = run(G18, ap0_zeta=np.sqrt(2), taus=red_t)
r_red = lo_quantities(o_red, red_t, 1.0, eps0=0.05)
curve = {}
for eps0, N, L in ((0.05, 4096, 16.0), (0.025, 8192, 16.0)):
    rows = []
    g = Grid(N, L); p0 = seed("parabola", g.x, delta=0.05, chirp=np.sqrt(2), eps0=eps0)
    for t in taus:
        nst = int(max(200, 1000 * t / eps0 * 0.05 * (1 + t)))
        o = lo_covariance(p0, g, eps0, G18, t, nst, nsp=1.0)
        G = np.exp(t)
        rows.append(dict(tau=t, steps=nst, lam_min=o["lam_min"], CAA=o["C"][0, 0], CAA_exact=2 * G - 1,
                         e2CPP_over_G=eps0**2 * o["C"][1, 1] / G, CAP=o["C"][0, 1], comm_minus_1=o["comm"] - 1,
                         det=float(np.linalg.det(o["C"]))))
        print(eps0, t, nst, "lam %.6f  CAA %.10f (exact %.10f)  e2CPP/G %.5f  comm-1 %.1e" % (o["lam_min"], o["C"][0, 0], 2 * G - 1,
              rows[-1]["e2CPP_over_G"], o["comm"] - 1), flush=True)
    curve[str(eps0)] = rows
res["curve"] = curve
res["reduced_same_taus"] = dict(tau=taus, lam_lead=r_red["lam_lead"].tolist(), e2CPP_over_G=(r_red["e2CPP"] / np.exp(red_t)).tolist(),
                                lam_eps005=r_red["lam_eps"].tolist())
json.dump(res, open("curve_summary.json", "w"), indent=1)
