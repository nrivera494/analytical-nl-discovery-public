"""Integrator check of the counterexample (run 2026-10-08-claude-b-optimum, claude-b, T-20261008-claude-b-01).

Replaces the Strang split step of twomode_cov.py by RK4 in the interaction picture (RK4IP, fourth order) and recomputes
zeta = 2, delta = 0, GRIN C22 = 1/2: the scalar launch and p2 = 0.75, at steps h = 4e-3 and 2e-3. Reports the best hard
symmetric band of each launch and min F_GRIN - min F_s, to compare with the split-step value -1.054e-2.
Writes rk4ip_check.json.
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-claude-b-grin-manakov-lib"))
import twomode_cov as tc

fft, ifft = np.fft.fft, np.fft.ifft


def propagate_rk4ip(g, a, b, z, dz, C, d):
    La = np.exp((-0.5j * g.w ** 2) * dz / 2)
    Lb = np.exp((-0.5j * g.w ** 2 - d * 1j * g.w) * dz / 2)

    def lin(x, y):
        return ifft(La * fft(x, axis=-1), axis=-1), ifft(Lb * fft(y, axis=-1), axis=-1)

    def nl(x, y):
        Ix, Iy = np.abs(x) ** 2, np.abs(y) ** 2
        return 1j * (C[0][0] * Ix + C[0][1] * Iy) * x * dz, 1j * (C[1][0] * Ix + C[1][1] * Iy) * y * dz

    n = int(round(z / dz))
    for _ in range(n):
        aI, bI = lin(a, b)
        k1a, k1b = nl(a, b)
        k1a, k1b = lin(k1a, k1b)
        k2a, k2b = nl(aI + k1a / 2, bI + k1b / 2)
        k3a, k3b = nl(aI + k2a / 2, bI + k2b / 2)
        ta, tb = lin(aI + k3a, bI + k3b)
        k4a, k4b = nl(ta, tb)
        ua, ub = lin(aI + k1a / 6 + k2a / 3 + k3a / 3, bI + k1b / 6 + k2b / 3 + k3b / 3)
        a, b = ua + k4a / 6, ub + k4b / 6
    return a, b


tc.propagate = propagate_rk4ip          # bin_covariance looks up propagate at call time
g = tc.Grid(256, 40.0)
out = {}
for h in (4e-3, 2e-3):
    t0 = time.time()
    s = 1 / np.cosh(g.t) + 0j
    nb, Cov = tc.bin_covariance(g, s, 0 * s, 2.0, h, [[1, 1], [1, 1]], 0.0)
    Cs, ns = tc.totals(nb, Cov, g.N)
    a0, b0, _ = tc.launch(g, 0.75, [[1, 1], [1, 0.5]])
    nb, Cov = tc.bin_covariance(g, a0, b0, 2.0, h, [[1, 1], [1, 0.5]], 0.0)
    Cg, ng = tc.totals(nb, Cov, g.N)
    As = tc.class_sym_hard(g, Cs, ns, range(1, 15))
    Ag = tc.class_sym_hard(g, Cg, ng, range(1, 15))
    out[f"h_{h:g}"] = dict(min_F_s=min(As.values()), kmax_s=min(As, key=As.get), min_F_grin=min(Ag.values()),
                           kmax_grin=min(Ag, key=Ag.get), diff=min(Ag.values()) - min(As.values()), wall=time.time() - t0)
    print(h, out[f"h_{h:g}"], flush=True)
json.dump(out, open(os.path.join(HERE, "rk4ip_check.json"), "w"), indent=1, default=float)
