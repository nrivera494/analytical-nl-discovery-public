"""Exploratory (not frozen): spectral-overlap measure for large-yield shaping. For TL and optimised masks, the
delta3 = 0 evolution's maximum (over xi <= 2) of the fraction of photons at w >= w_z and at w >= 0.8 w_DW,
compared with the DW-yield ratio."""
import numpy as np, json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
out = {}
for f in sys.argv[1:]:
    J = json.load(open(f)); tagf = os.path.basename(f)[4:-5]
    npz = np.load(os.path.join(RAW, tagf + '.npz')); K, wl, N, d3 = J['K'], J['wl'], J['N'], J['d3']
    p = Prop(4096, 64.0, N, 0.0, 2.0, 2.5e-4, 4)
    x = np.clip(p.w/wl, -1, 1); B = np.polynomial.legendre.legvander(x, K)[:, 2:]
    phi = np.where(np.abs(p.w) <= wl, B @ npz['xb'], 0.0)
    ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
    wz = 1/(6*d3); wdw = J['wDW_est']
    xs = [round(round(v/p.h)*p.h, 10) for v in np.arange(0.01, 2.0 + 1e-9, 0.01)]
    res = {}
    for lab, u0 in [('TL', ul), ('mask', ifft(np.exp(1j*phi)*fft(ul)))]:
        _, _, sn = p.run(u0, record=xs)
        fz = [spectrum(sn[v])[p.w >= wz].sum()/E0 for v in xs]
        fd = [spectrum(sn[v])[p.w >= 0.8*wdw].sum()/E0 for v in xs]
        res[lab] = dict(max_frac_wz=max(fz), xi_wz=xs[int(np.argmax(fz))], max_frac_08wdw=max(fd), xi_08wdw=xs[int(np.argmax(fd))],
                        int_frac_wz=float(np.sum(fz)*0.01))
    r = dict(res=res, ratio_max_wz=res['mask']['max_frac_wz']/res['TL']['max_frac_wz'],
             ratio_max_08wdw=res['mask']['max_frac_08wdw']/res['TL']['max_frac_08wdw'],
             ratio_int_wz=res['mask']['int_frac_wz']/res['TL']['int_frac_wz'], H_yield=J['H_phase'])
    out[tagf] = r
    print(tagf, 'yield ratio', round(J['H_phase'], 3), '| max frac>=wz ratio', round(r['ratio_max_wz'], 3), '| max frac>=0.8wDW ratio', round(r['ratio_max_08wdw'], 3),
          '| xi-integrated frac>=wz ratio', round(r['ratio_int_wz'], 3), flush=True)
json.dump(out, open('overlap.json', 'w'), indent=1, default=float)
