#!/usr/bin/env python3
"""H4 with a larger mask basis and a gradient method: maximize f1(L = 4/N) over phase masks phi = sum_{m=2}^{M} c_m P_m(x)
(M = 12, 11 coefficients) with L-BFGS-B on forward-difference gradients (step 1e-3 rad), from (i) TL and (ii) the best
Powell mask of h4_opt (padded with zeros). Same model, grid and measurement as h4_opt.py. An adjoint gradient (solver
discrete adjoint + ZS eigenvalue gradient as terminal condition) is left as a task. Usage: python h4_grad.py out.json N T0 d3 [powell.json|none] [M] [maxiter]"""
import json, sys, time
import numpy as np
from numpy.polynomial import legendre
from scipy.optimize import minimize
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1]; N = float(sys.argv[2]); T0 = float(sys.argv[3]); d3 = float(sys.argv[4])
powell = json.load(open(sys.argv[5])) if len(sys.argv) > 5 and sys.argv[5] != "none" else None
M = int(sys.argv[6]) if len(sys.argv) > 6 else 12
MAXIT = int(sys.argv[7]) if len(sys.argv) > 7 else 25
n = 8192 if N <= 4 else 16384
g = GNLSE(n, 160.0, N, T0, raman=True, d3=d3)
U0 = np.fft.fft((1 / np.cosh(g.t)).astype(complex))
absU = np.abs(U0)
Wc = np.abs(g.W[absU > 1e-4 * absU.max()]).max()
x = np.clip(g.W / Wc, -1, 1)
P = np.array([legendre.legval(x, np.eye(M + 1)[m]) for m in range(M + 1)])
L = 4.0 / N; h = 0.4 / (N * (2 * N - 1)) ** 2; E = 2 * N**2
hist = []


def f1_of(c):
    u, _ = g.propagate(np.fft.ifft(np.exp(1j * (c @ P[2:])) * U0), L, h)
    f1 = 4 * measure(g, u, N)["eta1"] / E
    hist.append(f1)
    return f1


def fg(c):
    f0 = f1_of(c)
    gr = np.zeros_like(c)
    for i in range(len(c)):
        e = np.zeros_like(c); e[i] = 1e-3
        gr[i] = (f1_of(c + e) - f0) / 1e-3
    return -f0, -gr


t00 = time.time()
f1_tl = f1_of(np.zeros(M - 1))
rows = [{"start": "TL", "f1": f1_tl}]
print(json.dumps(rows[-1]), flush=True)
starts = [("TL", np.zeros(M - 1))]
if powell:
    p = np.array(powell["best_p"]); c0 = np.zeros(M - 1); c0[:len(p)] = p[:M - 1]
    starts.append(("powell_best", c0))
best = (f1_tl, np.zeros(M - 1))
for name, c0 in starts:
    t0 = time.time()
    r = minimize(fg, c0, jac=True, method="L-BFGS-B", options={"maxiter": MAXIT})
    row = {"start": name, "f1_opt": float(-r.fun), "ratio_to_TL": float(-r.fun / f1_tl), "nit": int(r.nit), "nfev": int(r.nfev),
           "c_opt": [float(v) for v in r.x], "grad_norm_final": float(np.linalg.norm(r.jac)), "wall_s": round(time.time() - t0, 1)}
    rows.append(row); print(json.dumps(row), flush=True)
    if -r.fun > best[0]:
        best = (-r.fun, r.x)
    json.dump({"N": N, "T0_fs": T0, "d3": d3, "M": M, "rows": rows, "f1_TL": f1_tl, "best_f1": best[0], "headroom": best[0] / f1_tl,
               "best_c": [float(v) for v in best[1]], "n_evals": len(hist), "wall_s": round(time.time() - t00, 1)}, open(out, "w"), indent=1)
