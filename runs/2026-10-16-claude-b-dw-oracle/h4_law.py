"""H4 mechanism test: with Raman (M1), is the DW exponent still set by the strip width of the TOD-free (but Raman)
evolution? (i) d(xi) of the delta3 = 0 M1 evolution (RK4IP) of sech N=2, T0 = 50 fs; (ii) gated DW yield of M1
for delta3 in a range; local slopes vs d_*^{M1} and vs Roy/AK's pi/(2(2N-1))."""
import numpy as np, json, sys, time, math
from dw_lib import *
from m1_rk4ip import RK4IP
from singularity import strip_width
part = sys.argv[1]
if part == 'dstar':
    out = {}
    for kind, N, xif in [('sech', 2.0, 2.0), ('gauss', 3.0, 2.0)]:
        r = RK4IP(16384, 64.0, N, 0.0, xif, 1e-4, fR=0.18)
        u0 = (np.exp(-r.tau**2/2) if kind == 'gauss' else 1/np.cosh(r.tau)) + 0j
        xs = list(np.round(np.arange(0.02, xif + 1e-9, 0.01), 6))
        xs = [round(round(x/r.h)*r.h, 10) for x in xs]
        _, sn = r.run(u0, record=xs)
        d = [(x, strip_width(sn[x], r.w)[0], strip_width(sn[x], r.w, side=-1)[0]) for x in xs]
        good = [(x, a, b) for x, a, b in d if np.isfinite(a)]
        i = int(np.argmin([a for _, a, _ in good]))
        print(kind, N, 'M1 blue-side strip min', good[i], flush=True)
        out[f'{kind}{int(N)}'] = dict(d=d, min_blue=good[i])
    json.dump(out, open('h4_dstar_m1.json', 'w'), indent=1, default=float)
else:
    d3s = [float(v) for v in sys.argv[2].split(',')]
    res = []
    for d3 in d3s:
        wdw = 1/(2*d3); TW = max(2*(4/(4*d3) + 25), 60.0); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
        row = dict(d3=d3, Nt=Nt, TW=TW)
        for lab, h in (('h', 5e-4), ('h2', 2.5e-4)):
            r = RK4IP(Nt, TW, 2.0, d3, 4.0, h, fR=0.18)
            u0 = 1/np.cosh(r.tau) + 0j; E0 = spectrum(u0).sum()
            u, _ = r.run(u0)
            row[lab] = dict(eta_B=band_fraction(u, r.w, r.wz, E0), eta_DW=gated_fraction(u, r.tau, r.w, r.wz, E0),
                            kernel_dt_fs=r.raman_kernel_dt_fs)
        print('M1 sech2', d3, row['h2'], 'conv', abs(row['h']['eta_DW'] - row['h2']['eta_DW'])/row['h2']['eta_DW'], flush=True)
        res.append(row)
        json.dump(res, open(f'h4_law_m1_{sys.argv[3]}.json', 'w'), indent=1, default=float)
