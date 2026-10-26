"""d_*(C2, C3) for the Gaussian N=3 with spectral phase C2 w^2/2 + C3 w^3/6, min over xi <= 2 of the delta3 = 0 strip width."""
import numpy as np, json, sys
from dw_lib import *
from singularity import strip_width
N, xif = 3.0, 2.0
pairs = [tuple(float(a) for a in s.split(':')) for s in sys.argv[1].split(',')]
Nt, TW, h = 16384, 64.0, 2.5e-4
out = []
for C2, C3 in pairs:
    p = Prop(Nt, TW, N, 0.0, xif, h, 4)
    ul = np.exp(-p.tau**2/2) + 0j
    u0 = ifft(np.exp(1j*(C2*p.w**2/2 + C3*p.w**3/6))*fft(ul))
    xs = [round(round(x/p.h)*p.h, 10) for x in np.arange(0.02, xif + 1e-9, 0.005)]
    _, _, sn = p.run(u0, record=xs)
    d = [(x, strip_width(sn[x], p.w)[0], strip_width(sn[x], p.w, side=-1)[0]) for x in xs]
    g = [(x, a) for x, a, b in d if np.isfinite(a)]   # blue side (upper half-plane singularities) controls the blue DW
    # robust minimum: 3-point running median (isolated single-xi fit outliers occur, e.g. (C2,C3)=(-0.2,-0.6) at xi=0.555)
    vals = np.array([v for _, v in g]); med = np.array([np.median(vals[max(0, k-1):k+2]) for k in range(len(vals))])
    i = int(np.argmin(med))
    out.append(dict(C2=C2, C3=C3, xi_star=g[i][0], d_star=float(med[i]), d_raw_min=float(vals.min()), xi_raw_min=g[int(np.argmin(vals))][0],
                    curve=[(x, a) for x, a in g]))
    print(C2, C3, 'xi*', g[i][0], 'd*', round(g[i][1], 5), flush=True)
    json.dump(out, open(f'dstar_poly_{sys.argv[2]}.json', 'w'), indent=1, default=float)
