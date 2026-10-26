#!/usr/bin/env python3
"""Second implementation at large N: compare FastDifferentiableMMNLO (solver_check2.jl; N = 6, T0 = 400 fs, Agarwal Raman,
self-steepening built in) with the numpy GNLSE (s = 1/(omega0 T0)) on the same 32768-point grid, via the leading-soliton
ZS content (energy and photon-number fractions). Usage: python solver_check2_measure.py out.json"""
import json, os, sys
import numpy as np
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1]
OMEGA0 = 2 * np.pi * 299.792458 / 1550.0
N, T0 = 6, 400.0
s = 1 / (OMEGA0 * T0)
g = GNLSE(32768, 160.0, N, T0, raman=True, s=s)
u0 = (1 / np.cosh(g.t)).astype(complex)
h = 0.4 / (N * (2 * N - 1)) ** 2
u, _ = g.propagate(u0, int(round((4.0 / N) / h)) * h, h)
E = 2 * N**2
m = measure(g, u, N)
row = {"N": N, "T0_fs": T0, "s": s, "numpy_f1": 4 * m["eta1"] / E, "numpy_f1_photon": 4 * m["eta1"] / E / (1 - s * m["red_shift_W"]),
       "numpy_W": m["red_shift_W"], "numpy_t_peak": m["t_peak"]}
path = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/solver_check2/N6_T0400fs_raman1.csv")
d = np.loadtxt(path, delimiter=",")
assert len(d) == 32768 and abs(d[1, 0] - d[0, 0] - g.dt) < 1e-9 and abs(d[0, 0] - g.t[0]) < 1e-9, "grid mismatch"
us = d[:, 1] + 1j * d[:, 2]
ms = measure(g, us, N)
row.update({"solver_f1": 4 * ms["eta1"] / E, "solver_f1_photon": 4 * ms["eta1"] / E / (1 - s * ms["red_shift_W"]),
            "solver_W": ms["red_shift_W"], "solver_t_peak": ms["t_peak"], "solver_zeta1_re": ms["zeta1_re"]})
row["rel_diff_f1"] = row["solver_f1"] / row["numpy_f1"] - 1
print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
json.dump({"rows": [row]}, open(out, "w"), indent=1)
