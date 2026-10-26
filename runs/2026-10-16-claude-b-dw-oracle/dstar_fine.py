"""Resolve a narrow minimum of d(xi): fine xi sampling (spacing dx) on [x0, x1] for a Gaussian launch, two grids."""
import numpy as np, json, sys
from dw_lib import *
from singularity import strip_width
N, x0, x1, dx = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
out = []
for Nt, TW in [(16384, 48.0), (32768, 64.0)]:
    p = Prop(Nt, TW, N, 0.0, x1, min(2.5e-4, 0.0025/N**2), 4)
    u0 = np.exp(-p.tau**2/2) + 0j
    xs = [round(round(x/p.h)*p.h, 10) for x in np.arange(x0, x1 + 1e-12, dx)]
    _, _, sn = p.run(u0, record=xs)
    g = [(x, strip_width(sn[x], p.w)[0]) for x in xs]
    out.append(dict(Nt=Nt, TW=TW, h=p.h, curve=g))
    gg = [(x, v) for x, v in g if np.isfinite(v)]
    i = int(np.argmin([v for _, v in gg]))
    print(Nt, TW, 'min', gg[i], 'neighbours', gg[max(0, i-3):i+4], flush=True)
    json.dump(out, open(f'dstar_fine_N{int(N)}.json', 'w'), indent=1, default=float)
