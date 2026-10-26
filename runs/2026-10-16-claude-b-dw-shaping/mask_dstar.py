"""A10: d_* (delta3 = 0 evolution, min over xi <= 2, robust 3-point median and raw) of optimised phase masks vs TL."""
import numpy as np, json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
from singularity import strip_width
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
J = json.load(open(sys.argv[1])); tagf = os.path.basename(sys.argv[1])[4:-5]
npz = np.load(os.path.join(RAW, tagf + '.npz')); K, wl, N = J['K'], J['wl'], J['N']
p = Prop(16384, 64.0, N, 0.0, 2.0, 2.5e-4, 4)
x = np.clip(p.w/wl, -1, 1); B = np.polynomial.legendre.legvander(x, K)[:, 2:]
phi = np.where(np.abs(p.w) <= wl, B @ npz['xb'], 0.0)
ul = np.exp(-p.tau**2/2) + 0j
u0 = ifft(np.exp(1j*phi)*fft(ul))
xs = [round(round(v/p.h)*p.h, 10) for v in np.arange(0.02, 2.0 + 1e-9, 0.0025)]
_, _, sn = p.run(u0, record=xs)
g = [(v, strip_width(sn[v], p.w)[0]) for v in xs]
g = [(v, d) for v, d in g if np.isfinite(d)]
vals = np.array([d for _, d in g]); med = np.array([np.median(vals[max(0, k-1):k+2]) for k in range(len(vals))])
i = int(np.argmin(med)); j = int(np.argmin(vals))
out = dict(source=sys.argv[1], d_star_robust=float(med[i]), xi_robust=g[i][0], d_star_raw=float(vals[j]), xi_raw=g[j][0],
           neighbours_raw=g[max(0, j-3):j+4], curve=g)
print(tagf, 'robust', round(float(med[i]), 5), 'at', g[i][0], '| raw', round(float(vals[j]), 5), 'at', g[j][0], '| neighbours', [(round(a, 4), round(b, 4)) for a, b in g[max(0, j-3):j+4]], flush=True)
json.dump(out, open(f'mask_dstar_{tagf}.json', 'w'), indent=1, default=float)
