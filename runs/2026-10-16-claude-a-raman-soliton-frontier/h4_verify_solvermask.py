#!/usr/bin/env python3
"""Saturation and census check of a mask found by h4_adjoint.jl (solver convention: phase phi(Omega) applied to
A_w = fftshift(ifft(A_t)); numpy applies it as phi(-W) to fft(u)). N = 4, T0 from the command line, Legendre orders 2..M.
f1 at L*N = 4, 6, 8 for TL and the mask; per-peak census at the last L. Same check as the inline one that produced
h4_verify_maskB.json. Usage: python h4_verify_solvermask.py out.json coef.csv T0_fs M"""
import json, sys
import numpy as np
from numpy.polynomial import legendre
from gnlse import GNLSE
from h3_scan import measure
from zs import Grid, leading_fast

out, coef, T0, M = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
N = 4.0; E = 2 * N**2; n = 8192
c = np.loadtxt(coef, delimiter=",")
g = GNLSE(n, 160.0, N, T0, raman=True)
U0 = np.fft.fft((1 / np.cosh(g.t)).astype(complex)); a = np.abs(U0); Wc = np.abs(g.W[a > 1e-4 * a.max()]).max()
P = np.array([legendre.legval(np.clip(-g.W / Wc, -1, 1), np.eye(M + 1)[m]) for m in range(M + 1)])
h = 0.4 / (N * (2 * N - 1)) ** 2
rows = []
for label, phi in (("TL", 0.0), ("mask", c @ P[2:])):
    u = np.fft.ifft(U0 * np.exp(1j * phi)); Lp = 0.0
    for Lf in (4.0, 6.0, 8.0):
        ns = int(round((Lf / N - Lp) / h)); u, _ = g.propagate(u, ns * h, h); Lp += ns * h
        m = measure(g, u, N)
        rows.append({"mask": label, "L_times_N": Lf, "f1_ZS": 4 * m["eta1"] / E, "f1_window": m["E_window"] / E,
                     "zeta1_re": m["zeta1_re"], "t_peak": m["t_peak"], "W": m["red_shift_W"],
                     "window_limited": bool(abs(m["t_peak"]) > 64 or abs(m["red_shift_W"]) > 0.8 * np.pi / g.dt)})
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
    q = N * u; aa = np.abs(q)
    pk = [i for i in range(1, n - 1) if aa[i] >= aa[i - 1] and aa[i] >= aa[i + 1] and aa[i] > 0.15 * aa.max()]
    cen = []
    for i in pk:
        half = max(4.0 / aa[i], 0.4); sel = np.abs(g.t - g.t[i]) <= half; qw = q[sel]; tw = g.t[sel] - g.t[i]
        W = np.fft.fftfreq(len(qw), g.dt) * 2 * np.pi; Qw = np.fft.fft(qw); wc = float(np.sum(W * np.abs(Qw) ** 2) / np.sum(np.abs(Qw) ** 2))
        qz = qw * np.exp(-1j * wc * tw); nz = len(qz); qp = np.zeros(2 * nz, complex); qp[nz // 2: nz // 2 + nz] = qz
        z, _, _ = leading_fast(Grid(2 * nz, 2 * nz * g.dt), qp, sigma=1j * (np.abs(qp).max() + 0.3))
        cen.append({"t": float(g.t[i]), "W_c": wc, "f_ZS": 4 * float(z.imag) / E})
    cen = sorted(cen, key=lambda r: -r["W_c"])[:4]
    print("   census:", [{k: round(v, 3) for k, v in x.items()} for x in cen], flush=True)
    rows.append({"mask": label, "census_last_L": cen})
json.dump({"coef": coef, "T0_fs": T0, "rows": rows}, open(out, "w"), indent=1)
