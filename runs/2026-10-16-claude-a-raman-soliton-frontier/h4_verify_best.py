#!/usr/bin/env python3
"""Artefact checks for an optimized H4 mask (h4_grad.py output): propagate TL and the best mask with the same model and
measure the leading soliton at L*N = 4, 6, 8 (saturation), with Re zeta, windowed energy and photon drift; repeat at half
step; and take a per-peak census (all peaks above 15% of the tallest: ZS content and centroid frequency) at L*N = 4 and 8.
Usage: python h4_verify_best.py out.json h4grad_N4_T100.json"""
import json, sys
import numpy as np
from numpy.polynomial import legendre
from gnlse import GNLSE
from h3_scan import measure
from zs import Grid, leading_fast

out = sys.argv[1]; d = json.load(open(sys.argv[2]))
N, T0, d3, M = d["N"], d["T0_fs"], d["d3"], d["M"]
n = 8192 if N <= 4 else 16384
E = 2 * N**2


def census(g, u):
    q = N * u; a = np.abs(q)
    pk = [i for i in range(1, len(a) - 1) if a[i] >= a[i - 1] and a[i] >= a[i + 1] and a[i] > 0.15 * a.max()]
    res = []
    for i in pk:
        half = max(4.0 / a[i], 0.4); sel = np.abs(g.t - g.t[i]) <= half
        qw = q[sel]; tw = g.t[sel] - g.t[i]
        W = np.fft.fftfreq(len(qw), g.dt) * 2 * np.pi; Qw = np.fft.fft(qw)
        wc = float(np.sum(W * np.abs(Qw) ** 2) / np.sum(np.abs(Qw) ** 2))
        qz = qw * np.exp(-1j * wc * tw); nz = len(qz)
        qp = np.zeros(2 * nz, complex); qp[nz // 2: nz // 2 + nz] = qz
        z, _, _ = leading_fast(Grid(2 * nz, 2 * nz * g.dt), qp, sigma=1j * (np.abs(qp).max() + 0.3))
        res.append({"t": float(g.t[i]), "amp": float(a[i]), "W_c": wc, "f_ZS": 4 * float(z.imag) / E, "Re_zeta": float(z.real)})
    return sorted(res, key=lambda r: -r["W_c"])[:6]


rows = []
for hfac in (1.0, 0.5):
    g = GNLSE(n, 160.0, N, T0, raman=True, d3=d3)
    U0 = np.fft.fft((1 / np.cosh(g.t)).astype(complex))
    absU = np.abs(U0); Wc = np.abs(g.W[absU > 1e-4 * absU.max()]).max()
    x = np.clip(g.W / Wc, -1, 1)
    P = np.array([legendre.legval(x, np.eye(M + 1)[m]) for m in range(M + 1)])
    h = hfac * 0.4 / (N * (2 * N - 1)) ** 2
    for label, c in (("TL", np.zeros(M - 1)), ("best", np.array(d["best_c"]))):
        u = np.fft.ifft(np.exp(1j * (c @ P[2:])) * U0); p0 = g.photons(u); Lp = 0.0
        for Lf in (4.0, 6.0, 8.0):
            ns = int(round((Lf / N - Lp) / h)); u, _ = g.propagate(u, ns * h, h); Lp += ns * h
            m = measure(g, u, N)
            row = {"hfac": hfac, "mask": label, "L_times_N": Lf, "f1_ZS": 4 * m["eta1"] / E, "f1_window": m["E_window"] / E,
                   "zeta1_re": m["zeta1_re"], "t_peak": m["t_peak"], "red_shift_W": m["red_shift_W"],
                   "photon_drift": g.photons(u) / p0 - 1}
            if hfac == 1.0 and Lf in (4.0, 8.0):
                row["census"] = census(g, u)
            rows.append(row)
            print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in row.items() if k != "census"}), flush=True)
            if "census" in row:
                for p in row["census"]:
                    print("    ", {k: round(v, 4) for k, v in p.items()}, flush=True)
json.dump({"source": sys.argv[2], "rows": rows}, open(out, "w"), indent=1)
