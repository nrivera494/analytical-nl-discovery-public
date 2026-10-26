"""Known limit: fundamental soliton (sech, N = 1) in M0. Its strip width is constant (pi/2), so the law predicts a
steady Cherenkov flux d eta/d xi ~ exp(-(pi/2)/delta3) (Akhmediev-Karlsson). Measure the gated band yield (w >= w_z,
smooth gate |tau| < 20 around tau = 0, where the soliton stays) at xi = 20..40 and fit the late-time slope.
An earlier run with gate |tau| < 8 to xi = 20 was contaminated by the soliton's exponential tails (kept in superseded/)."""
import numpy as np, json, sys, math
from dw_lib import *
res = []
for d3 in [float(v) for v in sys.argv[1].split(',')]:
    wdw = 1/(2*d3); xif = 40.0
    TW = 2*(xif*(1/(4*d3)) + 40); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
    p = Prop(Nt, TW, 1.0, d3, xif, 2e-3, 4)
    u0 = 1/np.cosh(p.tau) + 0j; E0 = spectrum(u0).sum()
    xs = [20.0, 24.0, 28.0, 32.0, 36.0, 40.0]
    _, _, sn = p.run(u0, record=xs)
    eta = [gated_fraction(sn[x], p.tau, p.w, p.wz, E0, tg=20.0) for x in xs]
    b, a = np.polyfit(xs, eta, 1)
    res.append(dict(d3=d3, Nt=Nt, TW=TW, xi=xs, eta=eta, flux=b, offset=a))
    print(d3, 'flux', b, 'offset', a, 'eta', ['%.3e' % e for e in eta], flush=True)
    json.dump(res, open(f'n1_flux_{sys.argv[2]}.json', 'w'), indent=1, default=float)
