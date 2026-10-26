"""Second integrator (RK4IP, fR = 0) on held-out law points: gated DW yield, compared with the Yoshida split-step
values of yield_s3.json / yield_g4.json."""
import numpy as np, json, sys, math
from dw_lib import *
from m1_rk4ip import RK4IP
kind, N, xif, h = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
ref = {r['d3']: r['h2']['eta_DW'] for r in json.load(open(sys.argv[5]))}
out = []
for d3 in [float(v) for v in sys.argv[6].split(',')]:
    wdw = 1/(2*d3); TW = max(2*(xif/(4*d3) + 25), 40.0); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
    r = RK4IP(Nt, TW, N, d3, xif, h, fR=0.0)
    u0 = (np.exp(-r.tau**2/2) if kind == 'gauss' else 1/np.cosh(r.tau)) + 0j; E0 = spectrum(u0).sum()
    u, _ = r.run(u0)
    e = gated_fraction(u, r.tau, r.w, r.wz, E0)
    out.append(dict(kind=kind, N=N, d3=d3, Nt=Nt, TW=TW, h=h, eta_DW_rk4ip=e, eta_DW_split=ref.get(d3), rel=(e/ref[d3] - 1) if d3 in ref else None))
    print(kind, N, d3, 'RK4IP', e, 'split', ref.get(d3), 'rel', out[-1]['rel'], flush=True)
    json.dump(out, open(f'rk4ip_heldout_{kind}{int(N)}.json', 'w'), indent=1, default=float)
