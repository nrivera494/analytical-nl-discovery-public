"""d_* = min over xi of the analyticity-strip width of the delta3 = 0 NLSE solution, for TL launches.
Coarse scan then fine scan around the minimum; two grids for convergence."""
import numpy as np, json, sys, time
from dw_lib import *
from singularity import strip_width

def dmin(kind, N, Nt, TW, h, xmax, ncoarse=60):
    tau, dt, w = grid(Nt, TW)
    u0 = (np.exp(-tau**2/2) if kind == 'gauss' else 1/np.cosh(tau)) + 0j
    xs = list(np.round(np.linspace(xmax/ncoarse, xmax, ncoarse), 8))
    p = Prop(Nt, TW, N, 0.0, xmax, h, 4)
    xs = [round(round(x/p.h)*p.h, 10) for x in xs]
    _, _, snaps = p.run(u0, record=xs)
    ds = [(x, strip_width(snaps[x], w)[0]) for x in xs]
    ds = [(x, d) for x, d in ds if np.isfinite(d) and d > 0]
    i = int(np.argmin([d for _, d in ds]))
    x0 = ds[i][0]; step = xmax/ncoarse
    xf = list(np.linspace(max(x0 - 1.5*step, step/10), x0 + 1.5*step, 31))
    p2 = Prop(Nt, TW, N, 0.0, max(xf), h, 4)
    xf = [round(round(x/p2.h)*p2.h, 10) for x in xf]
    _, _, snaps = p2.run(u0, record=xf)
    df = [(x, strip_width(snaps[x], w)[0]) for x in xf]
    df = [(x, d) for x, d in df if np.isfinite(d) and d > 0]
    j = int(np.argmin([d for _, d in df]))
    # parabolic refinement
    if 0 < j < len(df) - 1:
        (x1, y1), (x2, y2), (x3, y3) = df[j-1], df[j], df[j+1]
        den = (x1 - x2)*(x1 - x3)*(x2 - x3)
        A = (x3*(y2 - y1) + x2*(y1 - y3) + x1*(y3 - y2))/den
        B = (x3**2*(y1 - y2) + x2**2*(y3 - y1) + x1**2*(y2 - y3))/den
        C = (x2*x3*(x2 - x3)*y1 + x3*x1*(x3 - x1)*y2 + x1*x2*(x1 - x2)*y3)/den
        xv = -B/(2*A); dv = C - B**2/(4*A)
    else:
        xv, dv = df[j]
    return dict(kind=kind, N=N, Nt=Nt, TW=TW, h=p.h, xi_star=xv, d_star=dv, coarse=ds, fine=df)

cases = [('sech', 2.0), ('sech', 3.0), ('gauss', 3.0), ('gauss', 4.0), ('gauss', 6.0), ('gauss', 8.0), ('gauss', 10.0)]
if len(sys.argv) > 1:
    cases = [c for c in cases if f'{c[0]}{int(c[1])}' in sys.argv[1:]]
out = {}
for kind, N in cases:
    t0 = time.time()
    xmax = 1.2 if kind == 'sech' else min(1.0, 2.0/N)
    res = []
    for (Nt, TW, hfac) in [(4096, 40.0, 1.0), (8192, 48.0, 0.5)]:
        h = hfac*min(5e-4, 0.005/N**2)
        r = dmin(kind, N, Nt, TW, h, xmax)
        res.append(r)
        print(kind, N, Nt, 'xi*', round(r['xi_star'], 5), 'd*', round(r['d_star'], 6), f'{time.time()-t0:.0f}s', flush=True)
    out[f'{kind}{int(N)}'] = res
    json.dump(out, open(f'dstar_{"_".join(sys.argv[1:]) or "all"}.json', 'w'), indent=1, default=float)
