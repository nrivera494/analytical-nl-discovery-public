"""Same diagnostics as where.py for chirped launches (GDD C), Gaussian N=3, delta3 = 0.01, at xi = 2 and 4."""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
d3, N = 0.01, 3.0
TW = 2*(4/(4*d3) + 40); Nt = 1 << int(math.ceil(math.log2(TW*150/np.pi)))
p = Prop(Nt, TW, N, d3, 4.0, 5e-4, 4)
ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
res = {}
for C in [0.0, -0.2, -0.4]:
    u0 = ifft(np.exp(1j*C*p.w**2/2)*fft(ul))
    _, _, sn = p.run(u0, record=[2.0, 4.0])
    for x in [2.0, 4.0]:
        u = sn[x]; S = spectrum(u); wz = p.wz
        v = ifft((p.w >= wz)*fft(u)); I = np.abs(v)**2; I /= I.sum()
        ts = p.tau[np.argmax(np.abs(u))]
        r = dict(C=C, xi=x, tau_soliton=float(ts), band=float(S[p.w >= wz].sum()/E0), band_wz_2wz=float(S[(p.w >= wz) & (p.w < 2*wz)].sum()/E0),
                 band_above_2wz=float(S[p.w >= 2*wz].sum()/E0), frac_band_within10_of_soliton=float(I[np.abs(p.tau - ts) < 10].sum()),
                 gated=gated_fraction(u, p.tau, p.w, wz, E0), peak_power=float(np.abs(u).max()**2))
        res[f'C{C}_xi{x}'] = r
        print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
json.dump(res, open('where_gdd_N3_d0.01.json', 'w'), indent=1, default=float)
