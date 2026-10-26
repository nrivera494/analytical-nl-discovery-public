"""Measured GDD curve eta_B(C)/eta_B(0) and gated version, Gaussian N=3, xi_f=2, model M0 (Yoshida split-step),
at the C values of the d_*(C) scan; also at delta3 = 0.006 and 0.0075 (deeper in the exponentially small regime)."""
import numpy as np, json, sys
from dw_lib import *
d3 = float(sys.argv[1])
Cs = [-1.0, -0.8, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.2, 0.5, 1.0]
import math
wdw = 1/(2*d3); TW = max(2*(2/(4*d3) + 25), 60.0); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
p = Prop(Nt, TW, 3.0, d3, 2.0, 5e-4, 4)
ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
out = dict(d3=d3, Nt=Nt, TW=TW, h=p.h, C=Cs, eta_B=[], eta_DW=[])
for C in Cs:
    u0 = ifft(np.exp(1j*C*p.w**2/2)*fft(ul))
    u, _, _ = p.run(u0)
    out['eta_B'].append(band_fraction(u, p.w, p.wz, E0)); out['eta_DW'].append(gated_fraction(u, p.tau, p.w, p.wz, E0))
    print(d3, C, out['eta_B'][-1], out['eta_DW'][-1], flush=True)
json.dump(out, open(f'gdd_curve_N3_d{d3:g}.json', 'w'), indent=1, default=float)
