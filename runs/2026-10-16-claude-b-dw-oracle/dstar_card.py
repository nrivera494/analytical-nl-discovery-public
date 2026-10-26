"""Robust d_* (3-point running median of the blue-side strip width, min over xi <= xi_f) for further launches:
Gaussian N = 5, 6, 8, 10 (xi_f = 2) and sech N = 4 (xi_f = pi/2, one breather period). Grid Nt 16384, TW 48."""
import numpy as np, json, sys
from dw_lib import *
from singularity import strip_width
out = []
for kind, N in [(k, float(n)) for k, n in (s.split(':') for s in sys.argv[1].split(','))]:
    xif = 2.0 if kind == 'gauss' else np.pi/2
    NT, TWW = (int(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (16384, 48.0)
    p = Prop(NT, TWW, N, 0.0, xif, min(2.5e-4, 0.0025/N**2), 4)
    u0 = (np.exp(-p.tau**2/2) if kind == 'gauss' else 1/np.cosh(p.tau)) + 0j
    xs = [round(round(x/p.h)*p.h, 10) for x in np.arange(0.01, xif + 1e-9, min(0.005, 0.05/N))]
    _, _, sn = p.run(u0, record=xs)
    g = [(x, strip_width(sn[x], p.w)[0]) for x in xs]
    g = [(x, v) for x, v in g if np.isfinite(v)]
    vals = np.array([v for _, v in g]); med = np.array([np.median(vals[max(0, k-1):k+2]) for k in range(len(vals))])
    i = int(np.argmin(med))
    out.append(dict(kind=kind, N=N, xif=xif, h=p.h, xi_star=g[i][0], d_star=float(med[i]), d_raw_min=float(vals.min()), n_valid=len(g)))
    print(kind, N, 'xi*', g[i][0], 'd* (robust)', round(float(med[i]), 5), 'raw min', round(float(vals.min()), 5), flush=True)
    json.dump(out, open(f'dstar_card_{sys.argv[2]}.json', 'w'), indent=1, default=float)
