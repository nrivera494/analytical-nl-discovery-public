#!/usr/bin/env python3
"""Compare the numpy GNLSE (gnlse.py) with FastDifferentiableMMNLO (solver_check.jl) on the same launches.
Both include self-steepening s = 1/(omega0 T0) at 1550 nm (the solver's Kerr prefactor contains it), Blow-Wood Raman, beta2 only.
For each case: f1(L) from the same ZS measurement (h3_scan.measure), and the relative L2 distance between the output fields
(after allowing for complex conjugation, i.e. the opposite Fourier sign convention). Usage: python solver_check_measure.py out.json"""
import json, os, sys
import numpy as np
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1] if len(sys.argv) > 1 else "solver_check.json"
OMEGA0 = 2 * np.pi * 299.792458 / 1550.0
datadir = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/solver_check")
rows = []
for N, T0, raman in ((3, 100.0, True), (4, 200.0, True), (3, 100.0, False)):
    n, width = 8192, 160.0
    g = GNLSE(n, width, N, T0, raman=raman, s=1 / (OMEGA0 * T0))
    u0 = (1 / np.cosh(g.t)).astype(complex)
    h = 0.4 / (N * (2 * N - 1)) ** 2
    nsteps = int(round((4.0 / N) / h))
    u, _ = g.propagate(u0, nsteps * h, h)
    m = measure(g, u, N)
    E = 2 * N**2
    f10 = (2 * N - 1) / N**2
    row = {"N": N, "T0_fs": T0, "raman": raman, "s": 1 / (OMEGA0 * T0), "L_times_N": 4.0,
           "numpy_f1": 4 * m["eta1"] / E, "numpy_excess": 4 * m["eta1"] / E / f10 - 1, "numpy_t_peak": m["t_peak"],
           "numpy_shift_W": m["red_shift_W"]}
    tag = f"N{N}_T0{int(T0)}fs_raman{int(raman)}"
    path = os.path.join(datadir, tag + ".csv")
    if os.path.exists(path):
        d = np.loadtxt(path, delimiter=",")
        us = d[:, 1] + 1j * d[:, 2]
        assert len(us) == n and abs(d[1, 0] - d[0, 0] - g.dt) < 1e-9, "grid mismatch"
        # the solver's time axis may be offset by half a sample from ours; align by interpolation-free check of t[0]
        ms = measure(g, us, N)
        ms_c = measure(g, np.conj(us), N)
        dist = np.linalg.norm(us - u) / np.linalg.norm(u)
        dist_c = np.linalg.norm(np.conj(us) - u) / np.linalg.norm(u)
        row.update({"solver_f1": 4 * ms["eta1"] / E, "solver_excess": 4 * ms["eta1"] / E / f10 - 1,
                    "solver_f1_conj": 4 * ms_c["eta1"] / E, "solver_t_peak": ms["t_peak"], "solver_shift_W": ms["red_shift_W"],
                    "solver_t0_offset": float(d[0, 0] - g.t[0]),
                    "rel_L2_field_distance": float(dist), "rel_L2_field_distance_conj": float(dist_c)})
    rows.append(row)
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
