#!/usr/bin/env python3
"""Re-measure the best H4 masks with content measures that are valid under third-order dispersion: for TL and for the best
Powell mask of each given h4_opt json, propagate (same model, grid, step, L = 4/N) and report f1 by the nominal-dispersion ZS
content (the optimizer's objective), the local-dispersion ZS content (time rescaled by sqrt(D), D = 1 + 6 d3 W_c), and the
windowed energy fraction. Usage: python h4_recheck.py out.json h4_N*.json ..."""
import json, sys
import numpy as np
from numpy.polynomial import legendre
from gnlse import GNLSE
from h3_beta3_measure import zs_window

out = sys.argv[1]
rows = []
for f in sys.argv[2:]:
    d = json.load(open(f))
    r0 = d["rows"][0]
    N, T0, d3, cls = r0["N"], r0["T0_fs"], r0["d3"], r0["class"]
    M = len(d["best_p"]) + 1 if cls == "phi" else len(d["best_p"]) - 1      # h4_opt: phi has M-1 coefficients, Aphi M+1
    n = 8192 if N <= 4 else 16384
    g = GNLSE(n, 160.0, N, T0, raman=True, d3=d3)
    U0 = np.fft.fft((1 / np.cosh(g.t)).astype(complex))
    absU = np.abs(U0); Wc = np.abs(g.W[absU > 1e-4 * absU.max()]).max()
    x = np.clip(g.W / Wc, -1, 1)
    P = np.array([legendre.legval(x, np.eye(M + 1)[m]) for m in range(M + 1)])
    L = 4.0 / N; h = 0.4 / (N * (2 * N - 1)) ** 2; E = 2 * N**2
    for label, p in (("TL", np.zeros(len(d["best_p"]))), ("best", np.array(d["best_p"]))):
        c = p[:M - 1]
        a = 1.0 if cls == "phi" else 1 / (1 + np.exp(-(p[M - 1] + p[M] * P[2])))
        u, _ = g.propagate(np.fft.ifft(a * np.exp(1j * (c @ P[2:])) * U0), L, h)
        eta, wc, Ew = zs_window(g, u, N)
        D = 1 + 6 * d3 * wc
        eta_loc, _, _ = zs_window(g, u, N, stretch=np.sqrt(D))
        rows.append({"file": f, "N": N, "T0_fs": T0, "d3": d3, "mask": label, "f1_ZS_nominal": 4 * eta / E,
                     "f1_ZS_local": 4 * eta_loc * np.sqrt(D) / E, "f1_window": Ew / E, "W_c": wc, "D_local": D})
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
