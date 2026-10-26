"""Part (ii): smoothing limit of the parabola threshold, convergence of the slope, and an explicit
squeezed case with full ASE; lambda_LO(tau) curve to tau=4.  claude-interactive.13."""
import json, os, time, numpy as np
from fullfield import Grid, seed, lo_covariance, kappa
eps0 = 0.05
res = {}
# (a) kappa of the softplus parabola as delta -> 0 (sharp value 4/5)
kd = {}
for d in (0.2, 0.1, 0.05, 0.02, 0.01, 0.005):
    g = Grid(65536, 8.0)
    k, rp = kappa(seed("parabola", g.x, delta=d), g)
    kd[str(d)] = dict(kappa=k, rho_peak=rp, thr_nsp1=rp / k, thr_nsp2=2 * rp / k, kappa_minus_0p8=k - 0.8)
res["smoothing_limit"] = kd
ds = np.array([0.02, 0.01, 0.005]); dev = np.array([0.8 - kd[str(d)]["kappa"] for d in ds])
res["smoothing_limit_exponent"] = float(np.polyfit(np.log(ds), np.log(dev), 1)[0])
# (b) slope at delta=0.01 (finer grid), n_sp=2, around the threshold; and step/grid convergence of one slope
taus = np.array([0.5, 1, 2, 3, 4]) * 1e-3
def slope(p0, g, Gam, nsp, nst):
    lams = [lo_covariance(p0, g, eps0, Gam, t, nst, nsp=nsp)["lam_min"] for t in taus]
    return np.polyfit(taus, (np.array(lams) - 1) / taus, 2)[-1]
g = Grid(8192, 8.0)
p0 = seed("parabola", g.x, delta=0.01, chirp=np.sqrt(2), eps0=eps0)
k, rp = kappa(p0, g)
rows = []
for gp in (2.40, 2.48, 2.50, 2.52, 2.60):   # gamma P0/g
    Gam = rp / (eps0 * gp)
    s = slope(p0, g, Gam, 2.0, 60)
    rows.append(dict(gammaP0_over_g=gp, R=k / (2 * eps0 * Gam), slope=s, slope_theory=4 * (1 - k / (2 * eps0 * Gam))))
res["delta0.01_nsp2_scan"] = dict(kappa=k, threshold=2 * rp / k, rows=rows)
conv = {}
for (N, L, nst) in ((2048, 8.0, 60), (4096, 8.0, 60), (2048, 12.0, 60), (2048, 8.0, 240)):
    gg = Grid(N, L)
    pp = seed("parabola", gg.x, delta=0.05, chirp=np.sqrt(2), eps0=eps0)
    kk, rr = kappa(pp, gg)
    Gam = kk / (2 * eps0 * 0.9)
    conv[f"N{N}_L{L}_steps{nst}"] = slope(pp, gg, Gam, 2.0, nst)
res["slope_convergence_R0.9_nsp2"] = dict(values=conv, theory=4 * (1 - 0.9))
# (c) explicit squeezed case: smoothed parabola delta=0.05, asymptotic chirp, eps0=0.05, Gamma=sqrt18, nsp=1, tau=0.02
ex = {}
for (N, L, nst) in ((2048, 8.0, 200), (4096, 8.0, 400), (4096, 12.0, 800), (8192, 12.0, 800)):
    gg = Grid(N, L)
    for ch in (0.0, np.sqrt(2)):
        pp = seed("parabola", gg.x, delta=0.05, chirp=ch, eps0=eps0)
        o = lo_covariance(pp, gg, eps0, np.sqrt(18), 0.02, nst, nsp=1.0)
        ex[f"chirp{ch:.4f}_N{N}_L{L}_steps{nst}"] = dict(lam_min=o["lam_min"], lam_max=o["lam_max"], comm_minus_1=o["comm"] - 1,
            C=o["C"].tolist(), C_in=o["C_in"].tolist(), C_ase_unit=o["C_ase_unit"].tolist(), det=float(np.linalg.det(o["C"])))
gg = Grid(2048, 8.0); pp = seed("gaussian", gg.x)
o = lo_covariance(pp, gg, eps0, np.sqrt(18), 0.02, 200, nsp=2.0)
ex["gaussian_nsp2_tau0.02"] = dict(lam_min=o["lam_min"], comm_minus_1=o["comm"] - 1, R=kappa(pp, gg)[0] / (2 * eps0 * np.sqrt(18)))
res["explicit_tau0.02"] = ex
json.dump(res, open("explicit_summary.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items()}, indent=1)[:6000])
