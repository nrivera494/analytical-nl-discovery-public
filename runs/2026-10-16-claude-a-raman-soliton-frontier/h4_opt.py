#!/usr/bin/env python3
"""H4 (frozen in HYPOTHESES.md, commit 3af8dfa): shaping headroom in the GNLSE.
Maximize f1(L) = 4 eta1(L)/E (ZS content of the largest output soliton, as in h3_scan.measure) over spectral masks of a
TL sech laser: phase phi(W) = sum_{m=2}^{M} c_m P_m(x) (Legendre, x = W/W_c on the |Q| > 1e-4 max support), optionally
with a passive amplitude a(W) = sigmoid(d0 + d2 P2(x)) in (0,1] (class Aphi). Derivative-free Powell, multi-start.
An optimized value is an achievable lower bound on the true maximum.
Usage: python h4_opt.py out.json N T0 d3 class M starts maxfev"""
import json, sys, time
import numpy as np
from numpy.polynomial import legendre
from scipy.optimize import minimize
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1]
N = float(sys.argv[2]); T0 = float(sys.argv[3]); d3 = float(sys.argv[4])
cls = sys.argv[5] if len(sys.argv) > 5 else "phi"
M = int(sys.argv[6]) if len(sys.argv) > 6 else 6
nstarts = int(sys.argv[7]) if len(sys.argv) > 7 else 3
maxfev = int(sys.argv[8]) if len(sys.argv) > 8 else 120
rng = np.random.default_rng(11)

n = 8192 if N <= 4 else 16384
width = 160.0
g = GNLSE(n, width, N, T0, raman=True, d3=d3)
u0 = (1 / np.cosh(g.t)).astype(complex)
U0 = np.fft.fft(u0)
absU = np.abs(U0)
Wc = np.abs(g.W[absU > 1e-4 * absU.max()]).max()
x = np.clip(g.W / Wc, -1, 1)
P = np.array([legendre.legval(x, np.eye(M + 1)[m]) for m in range(M + 1)])
L = 4.0 / N
h = 0.4 / (N * (2 * N - 1)) ** 2
E = 2 * N**2
hist = []


def field(p):
    c = p[:M - 1]
    phi = c @ P[2:]
    if cls == "phi":
        a = 1.0
    else:
        d0, d2 = p[M - 1], p[M]
        a = 1 / (1 + np.exp(-(d0 + d2 * P[2])))
    return np.fft.ifft(a * np.exp(1j * phi) * U0)


def f1_of(p):
    u, _ = g.propagate(field(p), L, h)
    m = measure(g, u, N)
    f1 = 4 * m["eta1"] / E
    hist.append({"p": [float(v) for v in p], "f1": f1, "t_peak": m["t_peak"], "red_shift_W": m["red_shift_W"]})
    return f1


t00 = time.time()
p_tl = np.zeros(M - 1) if cls == "phi" else np.concatenate([np.zeros(M - 1), [8.0, 0.0]])
f1_tl = f1_of(p_tl)
rows = [{"N": N, "T0_fs": T0, "d3": d3, "class": cls, "start": "TL", "f1": f1_tl}]
print(json.dumps(rows[-1]), flush=True)
best = (f1_tl, p_tl)
for s in range(nstarts):
    scale = [0.0, 1.0, 3.0, 0.5, 2.0][s % 5]
    p0 = p_tl + np.concatenate([rng.normal(0, scale, M - 1), ([] if cls == "phi" else rng.normal(0, scale, 2))])
    if s == 0:
        p0 = p_tl + 0.05 * rng.normal(size=len(p_tl))
    t0 = time.time()
    r = minimize(lambda p: -f1_of(p), p0, method="Powell", options={"maxfev": maxfev, "xtol": 1e-3, "ftol": 1e-5})
    row = {"N": N, "T0_fs": T0, "d3": d3, "class": cls, "start": s, "scale": scale, "f1_opt": float(-r.fun),
           "ratio_to_TL": float(-r.fun / f1_tl), "nfev": int(r.nfev), "p_opt": [float(v) for v in r.x], "wall_s": round(time.time() - t0, 1)}
    rows.append(row); print(json.dumps(row), flush=True)
    if -r.fun > best[0]:
        best = (-r.fun, r.x)
    json.dump({"rows": rows, "f1_TL": f1_tl, "best_f1": best[0], "best_p": [float(v) for v in best[1]],
               "headroom": best[0] / f1_tl, "integrable_bound_factor": 2 * N / (2 * N - 1), "n_evals": len(hist),
               "wall_s": round(time.time() - t00, 1)}, open(out, "w"), indent=1)
json.dump({"rows": rows, "f1_TL": f1_tl, "best_f1": best[0], "best_p": [float(v) for v in best[1]], "headroom": best[0] / f1_tl,
           "integrable_bound_factor": 2 * N / (2 * N - 1), "n_evals": len(hist), "history": hist, "wall_s": round(time.time() - t00, 1)},
          open(out, "w"), indent=1)
