"""A5 held-out: gated DW yield of the Gaussian N=3 in model M1 (Raman, T0 = 50 fs), xi_f = 2, RK4IP at h and h/2."""
import numpy as np, json, sys, math, time
from dw_lib import *
from m1_rk4ip import RK4IP
res = []
for d3 in [float(v) for v in sys.argv[1].split(',')]:
    wdw = 1/(2*d3); TW = max(2*(2/(4*d3) + 25), 60.0); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
    row = dict(d3=d3, Nt=Nt, TW=TW)
    for lab, h in (('h', 2.5e-4), ('h2', 1.25e-4)):
        t0 = time.time()
        r = RK4IP(Nt, TW, 3.0, d3, 2.0, h, fR=0.18)
        u0 = np.exp(-r.tau**2/2) + 0j; E0 = spectrum(u0).sum()
        u, _ = r.run(u0)
        row[lab] = dict(eta_B=band_fraction(u, r.w, r.wz, E0), eta_DW=gated_fraction(u, r.tau, r.w, r.wz, E0),
                        eta_DW_tg20=gated_fraction(u, r.tau, r.w, r.wz, E0, tg=20.0), kernel_dt_fs=r.raman_kernel_dt_fs, wall=time.time()-t0)
    row['conv_eta_DW'] = abs(row['h']['eta_DW'] - row['h2']['eta_DW'])/row['h2']['eta_DW']
    row['d3'] = d3
    print('M1 gauss3', d3, row['h2'], 'conv', row['conv_eta_DW'], flush=True)
    res.append(row)
    json.dump(res, open(f'h4_g3_m1_{sys.argv[2]}.json', 'w'), indent=1, default=float)
