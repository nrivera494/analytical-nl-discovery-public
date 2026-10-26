#!/usr/bin/env python3
"""Re-measure the launches optimized by h4_adjoint.jl (solver, windowed-energy objective) with the numpy GNLSE (s = 0, same
grid, step and length) and the ZS content of h3_scan.measure, against the TL launch. Usage: python h4_adjoint_measure.py out.json N T0_fs M"""
import glob, json, os, sys
import numpy as np
from gnlse import GNLSE
from h3_scan import measure

out = sys.argv[1]; N = float(sys.argv[2]); T0 = float(sys.argv[3]); M = int(sys.argv[4])
d = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/h4_adjoint")
tag = f"N{N:g}_T0{int(T0)}_M{M}"
n = 8192 if N <= 4 else 16384
g = GNLSE(n, 160.0, N, T0, raman=True)
L = 4.0 / N; h = 0.4 / (N * (2 * N - 1)) ** 2; E = 2 * N**2
rows = []
launches = [("TL", (1 / np.cosh(g.t)).astype(complex))]
for f in sorted(glob.glob(os.path.join(d, tag + "_*.csv"))):
    if f.endswith("_coef.csv"):
        continue
    a = np.loadtxt(f, delimiter=",")
    assert len(a) == n and abs(a[1, 0] - a[0, 0] - g.dt) < 1e-9 and abs(a[0, 0] - g.t[0]) < 1e-9, "grid mismatch"
    launches.append((os.path.basename(f)[len(tag) + 1:-4], a[:, 1] + 1j * a[:, 2]))
for name, u0 in launches:
    u, _ = g.propagate(u0, L, h)
    m = measure(g, u, N)
    rows.append({"launch": name, "f1_ZS": 4 * m["eta1"] / E, "f1_window": m["E_window"] / E, "zeta1_re": m["zeta1_re"],
                 "launch_energy_ratio": float(np.sum(np.abs(u0) ** 2) / np.sum(1 / np.cosh(g.t) ** 2))})
    rows[-1]["ratio_ZS_to_TL"] = rows[-1]["f1_ZS"] / rows[0]["f1_ZS"]
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
json.dump({"N": N, "T0_fs": T0, "M": M, "rows": rows}, open(out, "w"), indent=1)
