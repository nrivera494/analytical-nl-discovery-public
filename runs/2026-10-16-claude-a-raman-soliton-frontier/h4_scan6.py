#!/usr/bin/env python3
"""H4 at N = 6 (frozen conjecture, HYPOTHESES.md): one-parameter scans of the two simplest phase masks, quadratic (chirp)
and cubic spectral phase, c2 P2(x) and c3 P3(x) with x = W/W_c on the |Q| > 1e-4 max support (as in h4_opt.py), for a TL
sech laser with N = 6 at T0 given on the command line. Objective f1(L = 4/N) as in h3_scan.measure. A full Powell search is
too expensive at N = 6 under the present machine load; these scans give an achievable lower bound on the headroom.
Usage: python h4_scan6.py out.json T0 d3"""
import json, sys, time
import numpy as np
from numpy.polynomial import legendre
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1]; T0 = float(sys.argv[2]); d3 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
N = 6
g = GNLSE(16384, 160.0, N, T0, raman=True, d3=d3)
U0 = np.fft.fft((1 / np.cosh(g.t)).astype(complex))
absU = np.abs(U0)
Wc = np.abs(g.W[absU > 1e-4 * absU.max()]).max()
x = np.clip(g.W / Wc, -1, 1)
P2 = legendre.legval(x, [0, 0, 1]); P3 = legendre.legval(x, [0, 0, 0, 1])
L = 4.0 / N; h = 0.4 / (N * (2 * N - 1)) ** 2; E = 2 * N**2
rows = []
for kind, c in [("TL", 0.0)] + [(k, v) for k in ("c2", "c3") for v in (-4.0, -2.0, -1.0, 1.0, 2.0, 4.0)]:
    t0 = time.time()
    phi = 0.0 if kind == "TL" else c * (P2 if kind == "c2" else P3)
    u, _ = g.propagate(np.fft.ifft(np.exp(1j * phi) * U0), L, h)
    m = measure(g, u, N)
    rows.append({"N": N, "T0_fs": T0, "d3": d3, "mask": kind, "coef": c, "f1": 4 * m["eta1"] / E, "zeta1_re": m["zeta1_re"],
                 "t_peak": m["t_peak"], "red_shift_W": m["red_shift_W"], "wall_s": round(time.time() - t0, 1)})
    rows[-1]["ratio_to_TL"] = rows[-1]["f1"] / rows[0]["f1"]
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
