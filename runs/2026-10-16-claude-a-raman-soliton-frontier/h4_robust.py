#!/usr/bin/env python3
"""H4d (frozen in HYPOTHESES.md, twentieth freeze): robustness of the two best phase masks found at N = 4.
Mask A: h4grad_N4_T100.json (Legendre orders 2..12 on the spectral support, numpy convention), designed at T0 = 100 fs.
Mask B: h4_adjoint N4_T0200_M16_TL_coef.csv (orders 2..16, solver convention A_w = fftshift(ifft(A_t))), designed at T0 = 200 fs;
it is applied by loading the optimized launch field shape and is therefore only re-used at its own T0 with self-steepening;
for the T0 detuning it is rebuilt from its coefficients in the solver convention. Usage: python h4_robust.py out.json [best2 [detune]]"""
import json, os, sys
import numpy as np
from numpy.polynomial import legendre
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1]
OMEGA0 = 2 * np.pi * 299.792458 / 1550.0
N = 4.0; E = 2 * N**2; n = 8192
rows = []


def legendre_set(x, M):
    return np.array([legendre.legval(x, np.eye(M + 1)[m]) for m in range(M + 1)])


def run(T0, s, phase_fn):
    g = GNLSE(n, 160.0, N, T0, raman=True, s=s)
    U0 = np.fft.fft((1 / np.cosh(g.t)).astype(complex))
    out = {}
    for label, use in (("TL", False), ("mask", True)):
        U = U0 * (np.exp(1j * phase_fn(g, U0)) if use else 1.0)
        h = 0.4 / (N * (2 * N - 1)) ** 2
        u, _ = g.propagate(np.fft.ifft(U), 4.0 / N, h)
        m = measure(g, u, N)
        f1 = 4 * m["eta1"] / E
        out[label] = {"f1": f1, "f1_photon": f1 / (1 - s * m["red_shift_W"]), "W_c": m["red_shift_W"], "zeta1_re": m["zeta1_re"]}
    return out


# mask A = the TL-start optimum of h4grad_N4_T100 (+6.2 %); the json's best_c later became mask A2 (+9.0 %) from the second start
cA = np.loadtxt("h4grad_N4_T100_maskA_coef.csv", delimiter=","); MA = 12


def phaseA(g, U0):
    a = np.abs(U0); Wc = np.abs(g.W[a > 1e-4 * a.max()]).max()
    return cA @ legendre_set(np.clip(g.W / Wc, -1, 1), MA)[2:]


cB = np.loadtxt(os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/h4_adjoint/N4_T0200_M16_TL_coef.csv"), delimiter=",")
MB = 16


def phaseB(g, U0):
    # solver convention: A_w = fftshift(ifft(A_t)) on the centred axis Om = fftshift(2 pi fftfreq(n, dt)) (positive Om <-> ifft).
    # numpy U = fft(u) at frequency W corresponds to the solver's spectral bin at Om = -W (ifft/fft sign flip).
    a = np.abs(U0); Wc = np.abs(g.W[a > 1e-4 * a.max()]).max()
    return cB @ legendre_set(np.clip(-g.W / Wc, -1, 1), MB)[2:]


masks = [("A", phaseA, (100.0, 90.0, 110.0)), ("B", phaseB, (200.0, 180.0, 220.0))]
if len(sys.argv) > 2 and sys.argv[2] == "best2":     # H4f: masks A2 and B2, self-steepening only
    cA = np.loadtxt("h4grad_N4_T100_maskA2_coef.csv", delimiter=",")
    cB = np.loadtxt("h4_adjoint_N4_T200_maskB2_coef.csv", delimiter=",")
    masks = [("A2", phaseA, (100.0,)), ("B2", phaseB, (200.0,))]
    if len(sys.argv) > 3 and sys.argv[3] == "detune":   # H4h: +-10 % pulse duration, s = 0
        masks = [("A2", phaseA, (90.0, 110.0)), ("B2", phaseB, (180.0, 220.0))]
for name, fn, T0s in masks:
    for T0 in T0s:
        for s in ((0.0, 1 / (OMEGA0 * T0)) if T0 in (100.0, 200.0) else (0.0,)):
            r = run(T0, s, fn)
            row = {"mask": name, "T0_fs": T0, "s": s, "TL": r["TL"], "masked": r["mask"],
                   "gain_energy": r["mask"]["f1"] / r["TL"]["f1"] - 1, "gain_photon": r["mask"]["f1_photon"] / r["TL"]["f1_photon"] - 1}
            rows.append(row)
            print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in row.items() if k not in ("TL", "masked")}), flush=True)
            json.dump({"rows": rows}, open(out, "w"), indent=1)
