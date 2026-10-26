"""Relaxed assumption for C-02(b): the gated-objective mask optimised in M0 at Gaussian N=3, delta3 = 0.01, evaluated
in M1 (Raman fR = 0.18, T0 = 50 fs, RK4IP) and in M0 (RK4IP), gated DW yield at xi_f = 2 vs TL."""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
from m1_rk4ip import RK4IP
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
J = json.load(open('opt_N3_d0.01_xi2_it100_gated.json')); tagf = 'N3_d0.01_xi2_it100_gated'
npz = np.load(os.path.join(RAW, tagf + '.npz')); K, wl, N = J['K'], J['wl'], J['N']
out = {}
for d3 in [float(v) for v in sys.argv[1].split(',')]:
    TW = 2*(2/(4*d3) + 25); Nt = 1 << int(math.ceil(math.log2(TW*3/(2*d3)/np.pi)))
    for model, fR in [('M0', 0.0), ('M1', 0.18)]:
        r = RK4IP(Nt, TW, N, d3, 2.0, 2.5e-4, fR=fR)
        x = np.clip(r.w/wl, -1, 1); B = np.polynomial.legendre.legvander(x, K)[:, 2:]
        phi = np.where(np.abs(r.w) <= wl, B @ npz['xb'], 0.0)
        ul = np.exp(-r.tau**2/2) + 0j; E0 = spectrum(ul).sum()
        uT, _ = r.run(ul); uM, _ = r.run(ifft(np.exp(1j*phi)*fft(ul)))
        gT = gated_fraction(uT, r.tau, r.w, r.wz, E0); gM = gated_fraction(uM, r.tau, r.w, r.wz, E0)
        out[f'{model}_d{d3:g}'] = dict(Nt=Nt, TW=TW, gated_TL=gT, gated_mask=gM, H=gM/gT, kernel_dt_fs=getattr(r, 'raman_kernel_dt_fs', None))
        print(model, d3, 'gated TL %.4e mask %.4e H %.3f' % (gT, gM, gM/gT), flush=True)
        json.dump(out, open('h4c_gated_N3_d0.01.json', 'w'), indent=1, default=float)
