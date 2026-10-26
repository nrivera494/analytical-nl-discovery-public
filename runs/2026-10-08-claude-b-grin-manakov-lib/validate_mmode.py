"""Check that mmode_cov.py with M = 2 reproduces twomode_cov.py (zeta = 2, GRIN LP01/LP02, p2 = 0.3, delta = 0.2), and
that M = 3 with Manakov overlaps reproduces the scalar per-bin covariance. Writes validation_mmode.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twomode_cov as tc
import mmode_cov as mm

g = tc.Grid(256, 40.0)
C2 = [[1, 1], [1, 0.5]]
a0, b0, _ = tc.launch(g, 0.3, C2)
nb2, Cov2 = tc.bin_covariance(g, a0, b0, 2.0, 2e-3, C2, 0.2)
Ct2, nt2 = tc.totals(nb2, Cov2, g.N)
A0, _ = mm.launch(g, [0.7, 0.3], C2)
nbm, Covm = mm.bin_covariance(g, A0, 2.0, 2e-3, C2, [0.0, 0.2])
Ctm, ntm = mm.totals(nbm, Covm)
out = {"M2_max_rel_dCtot": float(np.max(np.abs(Ctm - Ct2)) / np.max(np.abs(Ct2))),
       "M2_max_rel_dn": float(np.max(np.abs(ntm - nt2)) / np.max(nt2))}
s = 1 / np.cosh(g.t) + 0j
nbs, Covs = tc.bin_covariance(g, s, 0 * s, 2.0, 2e-3, [[1, 1], [1, 1]], 0.0)
Cts, nts = tc.totals(nbs, Covs, g.N)
J3 = np.ones((3, 3))
A3, _ = mm.launch(g, [0.5, 0.3, 0.2], J3)
nb3, Cov3 = mm.bin_covariance(g, A3, 2.0, 2e-3, J3, [0, 0, 0])
Ct3, nt3 = mm.totals(nb3, Cov3)
out["M3_manakov_max_rel_dCtot_vs_scalar"] = float(np.max(np.abs(Ct3 - Cts)) / np.max(np.abs(Cts)))
json.dump(out, open(os.path.join(HERE, "validation_mmode.json"), "w"), indent=1)
print(out)
