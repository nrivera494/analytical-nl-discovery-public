"""d(xi) of the delta3 = 0 evolution over the whole propagation range [0, xi_f] used in the yield sweeps (post hoc
check of the frozen definition 'minimum over xi'; the A1 scans stopped at xi = 1.0 (Gaussian N=3), 0.7 (N=4))."""
import numpy as np, json, sys
from dw_lib import *
from singularity import strip_width
kind, N, xif = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
Nt, TW = 16384, 48.0
h = min(2.5e-4, 0.0025/N**2)
xs = list(np.round(np.arange(0.02, xif + 1e-9, 0.01), 6))
p = Prop(Nt, TW, N, 0.0, xif, h, 4)
xs = [round(round(x/p.h)*p.h, 10) for x in xs]
u0 = (np.exp(-p.tau**2/2) if kind == 'gauss' else 1/np.cosh(p.tau)) + 0j
_, _, sn = p.run(u0, record=xs)
d = [(x, strip_width(sn[x], p.w)[0]) for x in xs]
good = [(x, v) for x, v in d if np.isfinite(v)]
# local minima
mins = [(good[i][0], good[i][1]) for i in range(1, len(good)-1) if good[i][1] < good[i-1][1] and good[i][1] < good[i+1][1]]
print(kind, N, 'local minima of d(xi):', [(round(a, 3), round(b, 4)) for a, b in mins])
json.dump(dict(kind=kind, N=N, xif=xif, Nt=Nt, TW=TW, h=p.h, d=d, local_minima=mins), open(f'dscan_full_{kind}{int(N)}.json', 'w'), indent=1, default=float)
