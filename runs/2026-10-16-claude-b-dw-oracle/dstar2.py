"""Refined d_* on three grids (frequency half-range up to ~1000) for the held-out and primary launches."""
import numpy as np, json, sys, time
from dstar import dmin
kind, N, xmax = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
res = []
for (Nt, TW, hfac) in [(8192, 48.0, 1.0), (16384, 48.0, 0.5), (16384, 64.0, 0.25)]:
    t0 = time.time()
    h = hfac*min(5e-4, 0.005/N**2)
    r = dmin(kind, N, Nt, TW, h, xmax, ncoarse=80)
    res.append(r)
    print(kind, N, Nt, TW, 'h', r['h'], 'xi*', round(r['xi_star'], 5), 'd*', round(r['d_star'], 6), f'{time.time()-t0:.0f}s', flush=True)
    json.dump(res, open(f'dstar2_{kind}{int(N)}.json', 'w'), indent=1, default=float)
