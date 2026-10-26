"""H2d (A9): card-regime collapse of TL band yield eta_B(xi=2) vs x = d_*(N)/delta3 (Gaussian launches).
d_* from the delta3 = 0 evolution (robust minimum over xi <= 2). Also the same plot vs Roy's variable (2N-1) delta3."""
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
dstar = json.loads(sys.argv[1])          # {"3": 0.1923, ...}
rows = []
for f in ['yield_cardA.json', 'yield_cardB.json']:
    for r in json.load(open(f)):
        rows.append((r['N'], r['d3'], r['h2']['eta_B']['2'], r['h2']['eta_DW']))
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
out = []
for N in sorted(set(r[0] for r in rows)):
    rr = sorted([r for r in rows if r[0] == N], key=lambda r: r[1])
    d = dstar.get(str(int(N)))
    if d is None:
        continue
    x = np.array([d/r[1] for r in rr]); e = np.array([r[2] for r in rr])
    s = np.array([(2*N - 1)*r[1] for r in rr])
    ax[0].semilogy(x, e, 'o-', label=f'N={int(N)}, $d_*$={d:.4f}')
    ax[1].semilogy(1/s, e, 'o-', label=f'N={int(N)}')
    out += [dict(N=N, d3=r[1], x=float(d/r[1]), eta_B=r[2], roy_s=(2*N-1)*r[1]) for r in rr]
ax[0].set_xlabel(r'$x=d_*(N)/\delta_3$'); ax[0].set_ylabel(r'TL band yield $\eta_B(\xi=2)$'); ax[0].legend(fontsize=7); ax[0].set_title('collapse variable $d_*/\\delta_3$')
ax[1].set_xlabel(r'$1/[(2N-1)\delta_3]$ (Roy variable)'); ax[1].legend(fontsize=7); ax[1].set_title("Roy's variable")
plt.tight_layout(); plt.savefig('fig_collapse.png', dpi=110)
# quantitative spread: for pairs of N, compare log eta at equal x by interpolation in overlapping ranges
def spread(key):
    Ns = sorted(set(o['N'] for o in out)); res = []
    for i, a in enumerate(Ns):
        for b in Ns[i+1:]:
            A = sorted([(o[key] if key == 'x' else 1/o['roy_s'], o['eta_B']) for o in out if o['N'] == a])
            B = sorted([(o[key] if key == 'x' else 1/o['roy_s'], o['eta_B']) for o in out if o['N'] == b])
            xa = np.array([t[0] for t in A]); la = np.log([t[1] for t in A])
            for xb, eb in B:
                if xa.min() <= xb <= xa.max():
                    res.append(abs(np.log(eb) - np.interp(xb, xa, la)))
    return res
sx = spread('x'); sr = spread('roy')
print('collapse spread |d ln eta| vs x: n=%d median %.3f max %.3f' % (len(sx), np.median(sx), max(sx)) if sx else 'no overlap')
print('spread vs Roy variable: n=%d median %.3f max %.3f' % (len(sr), np.median(sr), max(sr)) if sr else 'no overlap')
json.dump(dict(points=out, spread_x=sx, spread_roy=sr, dstar=dstar), open('collapse.json', 'w'), indent=1, default=float)
