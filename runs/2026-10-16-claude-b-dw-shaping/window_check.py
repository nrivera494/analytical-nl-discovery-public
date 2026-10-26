"""Window (wrap-around) check for the large-N optimisation grids: TL band yield at xi = 2 vs time window."""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
res = []
for N, d3, h, Nt0, TW0 in [(8.0, 0.05, 1.6e-4, 1024, 70.0), (6.0, 0.03, 2.8e-4, 2048, 83.333333)]:
    for fac in [1, 2, 4]:
        TW = TW0*fac; Nt = Nt0*fac
        p = Prop(Nt, TW, N, d3, 2.0, h, 4)
        ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
        u, _, _ = p.run(ul)
        e = band_fraction(u, p.w, p.wz, E0)
        res.append(dict(N=N, d3=d3, TW=TW, Nt=Nt, eta_B=e))
        print(N, d3, 'TW', TW, 'eta_B', e, flush=True)
json.dump(res, open('window_check.json', 'w'), indent=1, default=float)
