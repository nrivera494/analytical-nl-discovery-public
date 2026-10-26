"""Unit checks of dw_lib: exact N=2 breather (order of accuracy), invariants, adjoint vs finite differences."""
import numpy as np, json, time
from dw_lib import *

def breather2(tau, xi):
    # Satsuma-Yajima N=2 for i v_xi + v_tt/2 + |v|^2 v = 0, v(0)=2 sech; u = v/N with N=2
    num = 4*(np.cosh(3*tau) + 3*np.exp(4j*xi)*np.cosh(tau))*np.exp(0.5j*xi)
    den = np.cosh(4*tau) + 4*np.cosh(2*tau) + 3*np.cos(4*xi)
    return num/den/2.0

out = {}
Nt, TW = 1024, 40.0
tau, dt, w = grid(Nt, TW)
u0 = 1/np.cosh(tau) + 0j
xi = np.pi/4
errs = {}
for order in (2, 4):
    e = []
    for h in (0.01, 0.005, 0.0025):
        p = Prop(Nt, TW, 2.0, 0.0, xi, h, order)
        u, _, _ = p.run(u0)
        e.append(np.abs(u - breather2(tau, xi)).max())
    errs[order] = e
    print('order', order, 'max err', e, 'ratios', [e[i]/e[i+1] for i in range(2)])
out['breather_err'] = {str(k): v for k, v in errs.items()}
# invariants with TOD
p = Prop(2048, 80.0, 2.0, 0.03, 2.0, 0.002, 4)
tau2, dt2, w2 = p.tau, p.dt, p.w
u0b = 1/np.cosh(tau2) + 0j
I0 = invariants(u0b, w2, dt2, 2.0, 0.03)
u, _, _ = p.run(u0b)
I1 = invariants(u, w2, dt2, 2.0, 0.03)
print('invariants start', I0, 'end', I1)
out['inv_tod'] = dict(start=I0, end=I1)
# adjoint check (phase-only and passive) on a small case
p = Prop(512, 40.0, 2.5, 0.05, 0.6, 0.004, 4)
ul = np.exp(-p.tau**2/2) + 0j
for passive in (False, True):
    mp = MaskProblem(p, ul, K=8, passive=passive, log=False)
    rng = np.random.default_rng(1)
    x = mp.x0(0.3*rng.standard_normal(mp.nphi))
    if passive:
        x[mp.nphi:] = 0.5 + 0.4*rng.random(len(mp.inb))
    f, g, J = mp.value_grad(x)
    idx = [0, 3, mp.nphi-1] + ([mp.nphi + 2, mp.nphi + len(mp.inb)//2] if passive else [])
    for i in idx:
        ep = 1e-6
        xp = x.copy(); xp[i] += ep
        xm = x.copy(); xm[i] -= ep
        fd = -(mp.value(xp)[0] - mp.value(xm)[0])/(2*ep)
        print('passive' if passive else 'phase', i, 'adj', g[i], 'fd', fd, 'rel', abs(g[i]-fd)/abs(fd))
        out.setdefault('adjoint', []).append(dict(passive=passive, i=int(i), adj=float(g[i]), fd=float(fd)))
    print('J', J)
json.dump(out, open('test_lib.json', 'w'), indent=1, default=float)
