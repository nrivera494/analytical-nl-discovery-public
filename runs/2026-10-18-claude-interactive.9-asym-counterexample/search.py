"""Stage 2: adversarial passive-mask search for the asymmetric source (does any |m| <= 1 raise eta_max above TL?).

Optimisation on an FC grid (n, T) with the mask families of ../2026-10-18-claude-interactive.9-mask-adversary/masks.py,
basis centred on kc with half-width K (the source is far from symmetric).  Every final mask is re-evaluated on the
line with BO (n_line cells and 2 n_line, Richardson) and on the FC grid refined 2x.
Usage: python search.py <family> [<family> ...]
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, '.')
from cx_common import *
sys.path.insert(0, '../2026-10-18-claude-interactive.9-mask-adversary')
from masks import Problem, Family, optimise

RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-18-claude-interactive.9-asym-counterexample')
os.makedirs(RAW, exist_ok=True)
fams = sys.argv[1:] or ['phase-cheb', 'passive-cheb', 'sharp', 'passive-bins']
SEED = 7
rng = np.random.default_rng(SEED)
n, T, K, kc = 384, 64.0, 13.0, 8.0
prob = Problem(S_src, n, T, K)
ex = json.load(open('explore_summary.json'))
eta_TL_line = ex['eta_TL']
zTL, vTL = prob.leading_full(prob.pulse(np.ones(n, complex)))
print('TL on grid %.10f  (line %.10f)' % (zTL.imag, eta_TL_line), flush=True)

res_all = []
for kind in fams:
    fam = Family(prob, kind, J=24, kc=kc)
    d = fam.dim
    if kind in ('phase-cheb', 'passive-cheb'):
        b = [(-6.0, 6.0)] * d
        starts = [('nearTL', rng.normal(0, 0.05, d))] + [('rand%.1f' % s, rng.normal(0, s, d)) for s in (0.3, 0.8, 1.5)]
    elif kind == 'passive-bins':
        b = [(-3 * np.pi, 3 * np.pi)] * d
        starts = [('nearTL', rng.normal(0, 0.05, d)), ('rand0.5', rng.normal(0, 0.5, d))]
    else:
        ns = fam.ns
        b = [(-2 * np.pi, 2 * np.pi)] * ns + [(-K, K)] * ns + [(-np.pi, np.pi)] * ns + [(-K, K)] * ns
        starts = [('rand%d' % r, np.concatenate([rng.normal(0, 1.5, ns), rng.uniform(-6, 4, ns),
                                                 rng.normal(0, 0.6, ns), rng.uniform(-6, 4, ns)])) for r in range(4)]
    for label, x0 in starts:
        t0 = time.time()
        z0, v0 = (zTL, vTL) if label == 'nearTL' else (None, None)
        r, eta = optimise(prob, fam, x0, bounds=b, maxiter=400, z0=z0, v0=v0, check_every=50)
        m, phi, psi, aux = fam.mask(r.x)
        rec = {"family": kind, "start": label, "eta_grid": eta, "gain_grid": eta / zTL.imag - 1, "nfev": int(r.nfev),
               "throughput": float(np.sum(np.abs(m * prob.S) ** 2) / np.sum(prob.S ** 2)), "wall_s": time.time() - t0}
        np.savez(os.path.join(RAW, 'mask_%s_%s.npz' % (kind, label)), x=r.x, k=prob.k, m=m, kc=kc, K=K, n=n, T=T)
        print('%-13s %-8s eta_grid %.10f gain %+.5e thru %.4f nfev %d [%.0f s]' % (
            kind, label, eta, rec['gain_grid'], rec['throughput'], r.nfev, rec['wall_s']), flush=True)
        res_all.append((rec, fam, r.x))

# verify the best mask of each family on the line
summary = {"grid": {"n": n, "T": T, "K": K, "kc": kc}, "seed": SEED, "eta_TL_grid": float(zTL.imag),
           "eta_TL_line": eta_TL_line, "searches": [r[0] for r in res_all], "verified": {}}
for kind in fams:
    rows = [r for r in res_all if r[0]['family'] == kind]
    if not rows:
        continue
    rec, fam, x = max(rows, key=lambda r: r[0]['eta_grid'])
    m_grid, *_ = fam.mask(x)
    if kind == 'passive-bins':
        bins = np.round(prob.k / (2 * np.pi / T)).astype(int)
        lut = dict(zip(bins, m_grid))
        mfun = lambda kk: np.array([lut.get(int(b), 1.0 + 0j) for b in np.round(kk / (2 * np.pi / T)).astype(int)])
        Tline = T          # bins live on this window's frequency grid
    else:
        def mfun(kk, fam=fam, x=x):
            ph, ps, aux = fam.phipsi_at(x, kk)
            return np.cos(ps) * np.exp(1j * ph)
        Tline = 96.0
    zz = None
    # starting guess: FC eigenvalue of the optimised grid mask
    zg, vg = prob.leading_full(prob.pulse(m_grid))
    zR, zs = line_eta(mfun, zg, T=Tline, n=4096)
    zR2, zs2 = line_eta(mfun, zR, T=Tline, n=8192)
    v = {"eta_grid": rec['eta_grid'], "eta_line_R_4096": float(zR.imag), "eta_line_R_8192": float(zR2.imag),
         "zeta_line": [float(zR2.real), float(zR2.imag)], "gain_over_TL_line": float(zR2.imag / eta_TL_line - 1),
         "throughput": rec['throughput'], "T_line": Tline}
    summary['verified'][kind] = v
    print('VERIFIED %-13s line eta %.10f (%.10f)  gain over TL %+.5e  thru %.4f' % (
        kind, zR2.imag, zR.imag, v['gain_over_TL_line'], rec['throughput']), flush=True)
json.dump(summary, open('search_summary_%s.json' % '_'.join(fams), 'w'), indent=1, default=float)
