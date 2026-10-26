"""H3f on optimized masks: for a phase mask phi(w) (Legendre series from an optimize.py run), compute
(a) d_*[phi] = min over xi <= xi_f of the strip width of the delta3 = 0 evolution (Nt 16384, TW 64);
(b) gated DW yield eta_DW(xi_f) at other delta3 for mask and TL; compare H = eta_mask/eta_TL with exp(-(d_*[phi]-d_*[TL])/delta3).
Usage: python mask_transfer.py <opt json> <d3 list>"""
import numpy as np, json, sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
from singularity import strip_width
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
J = json.load(open(sys.argv[1])); tagf = os.path.basename(sys.argv[1])[4:-5]
npz = np.load(os.path.join(RAW, tagf + '.npz'))
xb = npz['xb']; K = J['K']; wl = J['wl']; N = J['N']; xif = J['xif']
def phi_on(w):
    x = np.clip(w/wl, -1, 1)
    B = np.polynomial.legendre.legvander(x, K)[:, 2:]
    ph = B @ xb
    return np.where(np.abs(w) <= wl, ph, 0.0)
def dstar(phase):
    p = Prop(16384, 64.0, N, 0.0, xif, min(2.5e-4, 0.0025/N**2), 4)
    ul = np.exp(-p.tau**2/2) + 0j
    u0 = ifft(np.exp(1j*phase(p.w))*fft(ul)) if phase else ul
    xs = [round(round(x/p.h)*p.h, 10) for x in np.arange(0.02, xif + 1e-9, 0.005)]
    _, _, sn = p.run(u0, record=xs)
    d = [(x, strip_width(sn[x], p.w)[0]) for x in xs]
    g = [(x, v) for x, v in d if np.isfinite(v)]
    i = int(np.argmin([v for _, v in g]))
    if 0 < i < len(g) - 1:
        (x1, y1), (x2, y2), (x3, y3) = g[i-1], g[i], g[i+1]
        M = np.array([[x1**2, x1, 1], [x2**2, x2, 1], [x3**2, x3, 1]]); a, b, c = np.linalg.solve(M, [y1, y2, y3])
        return -b/(2*a), c - b*b/(4*a)
    return g[i]
out = dict(source=sys.argv[1], N=N, xif=xif, K=K, wl=wl)
out['dstar_TL'] = dstar(None); out['dstar_mask'] = dstar(phi_on)
print('d* TL', out['dstar_TL'], 'mask', out['dstar_mask'], flush=True)
out['yields'] = []
for d3 in [float(v) for v in sys.argv[2].split(',')]:
    wdw = 1/(2*d3); TW = max(2*(xif/(4*d3) + 25), 60.0); Nt = 1 << int(math.ceil(math.log2(TW*3*wdw/np.pi)))
    p = Prop(Nt, TW, N, d3, xif, 5e-4 if N <= 3 else 0.004/N**2, 4)
    ul = np.exp(-p.tau**2/2) + 0j; E0 = spectrum(ul).sum()
    uT, _, _ = p.run(ul); uM, _, _ = p.run(ifft(np.exp(1j*phi_on(p.w))*fft(ul)))
    eT = gated_fraction(uT, p.tau, p.w, p.wz, E0); eM = gated_fraction(uM, p.tau, p.w, p.wz, E0)
    bT = band_fraction(uT, p.w, p.wz, E0); bM = band_fraction(uM, p.w, p.wz, E0)
    pred = math.exp(-(out['dstar_mask'][1] - out['dstar_TL'][1])/d3)
    out['yields'].append(dict(d3=d3, Nt=Nt, TW=TW, gated_TL=eT, gated_mask=eM, H_gated=eM/eT, band_TL=bT, band_mask=bM, H_band=bM/bT, H_pred=pred))
    print(d3, 'H_gated', eM/eT, 'H_band', bM/bT, 'pred exp(-dd/d3)', pred, flush=True)
    json.dump(out, open(f'transfer_{tagf}.json', 'w'), indent=1, default=float)
