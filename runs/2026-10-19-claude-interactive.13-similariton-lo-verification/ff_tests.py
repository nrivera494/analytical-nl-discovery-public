"""Sanity tests of fullfield.py (claude-interactive.13)."""
import numpy as np, json
from fullfield import Grid, seed, lo_covariance, kappa
res = {}
gr = Grid(1024, 8.0)
eps0 = 0.05
# 1. linear amplifier, Kerr off, chirped smoothed parabola: C_LO = [2 nsp G - (2nsp-1)] I
for nsp in (1.0, 2.0):
    p0 = seed("parabola", gr.x, delta=0.05, chirp=np.sqrt(2), eps0=eps0)
    o = lo_covariance(p0, gr, eps0, np.sqrt(18), 1.0, 200, nsp=nsp, kerr=False)
    G = np.e
    exact = 2 * nsp * G - (2 * nsp - 1)
    res[f"linear_amp_nsp{int(nsp)}"] = dict(C=o["C"].tolist(), exact=exact, comm=o["comm"],
        maxdev=float(np.max(np.abs(o["C"] - exact * np.eye(2)))))
# 2. passive Kerr, tiny dispersion, short length: dispersionless single-mode shear per time slot
eps_small = 1e-4
p0 = seed("gaussian", gr.x)
zL = 0.002  # nonlinear phase at peak = zL/eps -> 20 rad? use zL*1/eps
o = lo_covariance(p0, gr, eps_small, 0.0, zL, 400, nsp=1.0)
rho = np.abs(p0) ** 2; wgt = rho / rho.sum()
s = 2 * rho * zL / eps_small   # local shear 2 gamma P z
Cth = np.array([[1, np.sum(wgt * s)], [np.sum(wgt * s), 1 + np.sum(wgt * s**2)]])
res["passive_kerr_dispersionless"] = dict(C=o["C"].tolist(), C_theory=Cth.tolist(), comm=o["comm"],
    maxdev=float(np.max(np.abs(o["C"] - Cth))))
# 3. commutator, Kerr + gain + dispersion, longer run
p0 = seed("parabola", gr.x, delta=0.05, chirp=np.sqrt(2), eps0=eps0)
o = lo_covariance(p0, gr, eps0, np.sqrt(18), 1.0, 1000, nsp=1.0)
res["commutator_tau1"] = dict(comm_minus_1=o["comm"] - 1, lam_min=o["lam_min"], det=float(np.linalg.det(o["C"])))
print(json.dumps(res, indent=1))
json.dump(res, open("ff_tests.json", "w"), indent=1)
