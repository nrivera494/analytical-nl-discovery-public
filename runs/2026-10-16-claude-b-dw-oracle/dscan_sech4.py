"""Diagnostic for A11: d(xi) of the sech N=4 breather over one period at spacing 0.001 (Nt 16384, TW 48): all local
minima, to see whether several compression events with nearby d coexist."""
import numpy as np, json
from dw_lib import *
from singularity import strip_width
p = Prop(16384, 48.0, 4.0, 0.0, np.pi/2, 1.5e-4, 4)
u0 = 1/np.cosh(p.tau) + 0j
xs = [round(round(x/p.h)*p.h, 10) for x in np.arange(0.005, np.pi/2, 0.001)]
_, _, sn = p.run(u0, record=xs)
d = [(x, strip_width(sn[x], p.w)[0]) for x in xs]
g = [(x, v) for x, v in d if np.isfinite(v)]
mins = [(round(g[i][0], 4), round(g[i][1], 5)) for i in range(1, len(g)-1) if g[i][1] <= g[i-1][1] and g[i][1] <= g[i+1][1]]
mins.sort(key=lambda t: t[1])
print('lowest local minima of d(xi):', mins[:12])
json.dump(dict(curve=g, local_minima=mins), open('dscan_sech4.json', 'w'), indent=1, default=float)
