"""Persistence test for optimized masks: propagate TL and mask launches to xi = 6 on a wide window; band yield
(ungated) and gated DW yield (gate |tau| < 15) at xi = 2, 3, 4, 6. Band photons that are radiated DW persist and
separate from the solitons; transient soliton spectral content does not."""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
J = json.load(open(sys.argv[1])); tagf = os.path.basename(sys.argv[1])[4:-5]
npz = np.load(os.path.join(RAW, tagf + '.npz'))
K, wl, N, d3 = J['K'], J['wl'], J['N'], J['d3']
def mask_on(w, which):
    x = np.clip(w/wl, -1, 1); B = np.polynomial.legendre.legvander(x, K)[:, 2:]
    coeff = npz['xb'] if which == 'phase' else npz['xp'][:B.shape[1]]
    ph = np.where(np.abs(w) <= wl, B @ coeff, 0.0)
    a = np.ones_like(w)
    if which == 'passive':
        # amplitudes were per in-band bin of the optimisation grid: interpolate in w
        wo = npz['w'][npz['inb']]; ao = npz['a_p'][npz['inb']]; o = np.argsort(wo)
        a = np.where(np.abs(w) <= wo.max(), np.interp(w, wo[o], ao[o]), 1.0)
    return a*np.exp(1j*ph)
xis = [2.0, 3.0, 4.0, 6.0]
wdw = J["wDW_est"]; TW = float(sys.argv[2]) if len(sys.argv) > 2 else 2*(6/(4*d3) + 40); Nt = 1 << int(math.ceil(math.log2(TW*max(2.5*wdw, 40)/np.pi)))
h = J['h']
p = Prop(Nt, TW, N, d3, 6.0, h, 4)
ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
out = dict(source=sys.argv[1], Nt=Nt, TW=TW, h=p.h)
for lab in ['TL', 'phase', 'passive']:
    u0 = ul if lab == 'TL' else ifft(mask_on(p.w, lab)*fft(ul))
    _, _, sn = p.run(u0, record=xis)
    out[lab] = {f'{x:g}': dict(band=band_fraction(sn[x], p.w, p.wz, E0), gated=gated_fraction(sn[x], p.tau, p.w, p.wz, E0)) for x in xis}
    print(lab, {k: (round(v['band'], 4), round(v['gated'], 4)) for k, v in out[lab].items()}, flush=True)
json.dump(out, open(f'long_{tagf}.json', 'w'), indent=1, default=float)
