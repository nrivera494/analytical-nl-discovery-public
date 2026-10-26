"""A6 test: gated DW yield and band yield at xi_f = 2 for the Gaussian N=3 with phase C2 w^2/2 + C3 w^3/6, vs TL."""
import numpy as np, json, sys, math
from dw_lib import *
C2, C3 = float(sys.argv[1]), float(sys.argv[2])
res = []
for d3 in [float(v) for v in sys.argv[3].split(',')]:
    wdw = 1/(2*d3); TW = max(2*(2/(4*d3) + 25), 60.0); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
    row = dict(C2=C2, C3=C3, d3=d3, Nt=Nt, TW=TW)
    for lab, h in (('h', 5e-4), ('h2', 2.5e-4)):
        p = Prop(Nt, TW, 3.0, d3, 2.0, h, 4)
        ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
        uT, _, _ = p.run(ul); uM, _, _ = p.run(ifft(np.exp(1j*(C2*p.w**2/2 + C3*p.w**3/6))*fft(ul)))
        row[lab] = dict(gated_TL=gated_fraction(uT, p.tau, p.w, p.wz, E0), gated_mask=gated_fraction(uM, p.tau, p.w, p.wz, E0),
                        band_TL=band_fraction(uT, p.w, p.wz, E0), band_mask=band_fraction(uM, p.w, p.wz, E0),
                        gated20_mask=gated_fraction(uM, p.tau, p.w, p.wz, E0, tg=20.0), gated20_TL=gated_fraction(uT, p.tau, p.w, p.wz, E0, tg=20.0))
    r = row['h2']; row['H_gated'] = r['gated_mask']/r['gated_TL']; row['H_band'] = r['band_mask']/r['band_TL']
    row['H_pred'] = math.exp(0.01662/d3)
    print(d3, 'H_gated', row['H_gated'], 'H_band', row['H_band'], 'pred', row['H_pred'], 'gated20 ratio', r['gated20_mask']/r['gated20_TL'], flush=True)
    res.append(row)
    json.dump(res, open(f'poly_yield_C2{C2:g}_C3{C3:g}.json', 'w'), indent=1, default=float)
