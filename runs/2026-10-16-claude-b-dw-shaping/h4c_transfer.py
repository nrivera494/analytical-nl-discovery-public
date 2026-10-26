"""H4c: masks optimised in M0 (no Raman) evaluated in M1 (Raman fR = 0.18, T0 = 50 fs; RK4IP) against the TL launch,
band yield (w >= w_z) at xi_f = 2 and at xi = 6 (persistence)."""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
from m1_rk4ip import RK4IP
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
J = json.load(open(sys.argv[1])); tagf = os.path.basename(sys.argv[1])[4:-5]
npz = np.load(os.path.join(RAW, tagf + '.npz')); K, wl, N, d3 = J['K'], J['wl'], J['N'], J['d3']
def phase_on(w):
    x = np.clip(w/wl, -1, 1); B = np.polynomial.legendre.legvander(x, K)[:, 2:]
    return np.exp(1j*np.where(np.abs(w) <= wl, B @ npz['xb'], 0.0))
TW = 2*(6/(4*d3) + 40); Nt = 1 << int(math.ceil(math.log2(TW*max(2.5*J['wDW_est'], 40)/np.pi)))
out = dict(source=sys.argv[1], Nt=Nt, TW=TW)
for model, fR in [('M0', 0.0), ('M1', 0.18)]:
    r = RK4IP(Nt, TW, N, d3, 6.0, J['h']/2, fR=fR)
    ul = np.exp(-r.tau**2/2) + 0j; E0 = spectrum(ul).sum()
    for lab, u0 in [('TL', ul), ('phase', ifft(phase_on(r.w)*fft(ul)))]:
        _, sn = r.run(u0, record=[2.0, 6.0])
        out[f'{model}_{lab}'] = {f'{x:g}': band_fraction(sn[x], r.w, r.wz, E0) for x in [2.0, 6.0]}
    g2 = out[f'{model}_phase']['2']/out[f'{model}_TL']['2']; g6 = out[f'{model}_phase']['6']/out[f'{model}_TL']['6']
    out[f'{model}_gain'] = dict(xi2=g2, xi6=g6)
    print(model, 'TL', out[f'{model}_TL'], 'phase', out[f'{model}_phase'], 'gain xi2 %.3f xi6 %.3f' % (g2, g6), flush=True)
json.dump(out, open(f'h4c_{tagf}.json', 'w'), indent=1, default=float)
