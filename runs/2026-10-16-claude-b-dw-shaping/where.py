"""Where (in tau and w) are the band photons of the TL and optimized launches at xi = 6? Band-filtered field
|ifft(chi_B fft(u))|^2 integrated over tau windows; band photons split by frequency into [wz, 2wz] and > 2wz;
spectral centroid and peak frequency of the main soliton."""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
exec(open('long_eval.py').read().split("xis = [2.0")[0].split("RAW = ")[0])
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
J = json.load(open(sys.argv[1])); tagf = os.path.basename(sys.argv[1])[4:-5]
npz = np.load(os.path.join(RAW, tagf + '.npz')); K, wl, N, d3 = J['K'], J['wl'], J['N'], J['d3']
def mask_on(w):
    x = np.clip(w/wl, -1, 1); B = np.polynomial.legendre.legvander(x, K)[:, 2:]
    return np.exp(1j*np.where(np.abs(w) <= wl, B @ npz['xb'], 0.0))
wdw = J['wDW_est']; TW = 2*(6/(4*d3) + 40); Nt = 1 << int(math.ceil(math.log2(TW*max(2.5*wdw, 40)/np.pi)))
p = Prop(Nt, TW, N, d3, 6.0, J['h'], 4)
ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
res = {}
for lab in ['TL', 'phase']:
    u0 = ul if lab == 'TL' else ifft(mask_on(p.w)*fft(ul))
    u, _, _ = p.run(u0)
    S = spectrum(u); wz = p.wz
    chi = (p.w >= wz)
    v = ifft(chi*fft(u)); I = np.abs(v)**2; I /= I.sum()
    # tau location of the strongest soliton (peak of |u|)
    ts = p.tau[np.argmax(np.abs(u))]
    near = np.abs(p.tau - ts) < 10
    res[lab] = dict(tau_soliton=float(ts), band=float(S[chi].sum()/E0), band_wz_2wz=float(S[(p.w >= wz) & (p.w < 2*wz)].sum()/E0),
                    band_above_2wz=float(S[p.w >= 2*wz].sum()/E0), frac_band_near_soliton=float(I[near].sum()),
                    soliton_peak_w=float(p.w[np.argmax(np.abs(fft(u*np.exp(-((p.tau-ts)/3)**2)))**2)]),
                    peak_power=float(np.abs(u).max()**2))
    print(lab, res[lab], flush=True)
json.dump(res, open(f'where_{tagf}.json', 'w'), indent=1, default=float)
