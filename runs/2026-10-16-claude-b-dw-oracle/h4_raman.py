"""H4: TL yields in model M1 (Raman, fR = 0.18, T0 = 50 fs, self-steepening off) vs M0, RK4IP, steps h and h/2."""
import numpy as np, json, sys, time
from dw_lib import *
from m1_rk4ip import RK4IP
cases = {'roy': [('sech', 2.0, d3, 4.0, 4096, 150.0, 2.5e-4) for d3 in [0.02, 0.03, 0.04]],
         'card': [('gauss', 3.0, 0.01, 2.0, 8192, 150.0, 2.5e-4), ('gauss', 3.0, 0.02, 2.0, 4096, 100.0, 2.5e-4),
                  ('gauss', 3.0, 0.05, 2.0, 2048, 70.0, 2.5e-4), ('gauss', 6.0, 0.03, 2.0, 4096, 100.0, 1e-4),
                  ('gauss', 8.0, 0.05, 2.0, 4096, 100.0, 6e-5)]}[sys.argv[1]]
res = []
for kind, N, d3, xif, Nt, TW, h in cases:
    r0 = None
    row = dict(kind=kind, N=N, d3=d3, xif=xif, Nt=Nt, TW=TW)
    for fR in (0.0, 0.18):
        for lab, hh in (('h', h), ('h2', h/2)):
            t0 = time.time()
            r = RK4IP(Nt, TW, N, d3, xif, hh, fR=fR)
            u0 = (np.exp(-r.tau**2/2) if kind == 'gauss' else 1/np.cosh(r.tau)) + 0j
            E0 = spectrum(u0).sum()
            u, _ = r.run(u0)
            pk, wpk, _ = nsr_peak(u, u0, r.w, r.wz)
            S = spectrum(u)
            row[f'fR{fR}_{lab}'] = dict(eta_B=band_fraction(u, r.w, r.wz, E0), eta_DW=gated_fraction(u, r.tau, r.w, r.wz, E0),
                                         nsr_dB=pk, nsr_dnuT0=wpk/(2*np.pi), E_rel=S.sum()/E0,
                                         mean_w=float((r.w*S).sum()/S.sum()), kernel_dt_fs=getattr(r, 'raman_kernel_dt_fs', None),
                                         wall=time.time() - t0)
    a, b = row['fR0.0_h2'], row['fR0.18_h2']
    print(kind, N, d3, 'M0 etaB %.4e NSR %.1f dB | M1 etaB %.4e NSR %.1f dB etaDW %.4e <w> %.3f | conv M1 %.1e' % (
        a['eta_B'], a['nsr_dB'], b['eta_B'], b['nsr_dB'], b['eta_DW'], b['mean_w'],
        abs(row['fR0.18_h']['eta_B'] - b['eta_B'])/b['eta_B']), flush=True)
    res.append(row)
    json.dump(res, open(f'h4_raman_{sys.argv[1]}.json', 'w'), indent=1, default=float)
