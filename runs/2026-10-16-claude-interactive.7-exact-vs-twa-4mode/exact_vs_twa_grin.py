"""Same comparison as exact_vs_twa.py, with the exact GRIN Kerr tensor (Hermite-Gauss basis, grin_overlaps.grin_tensor(3),
S_0000 = 1) restricted to the 4 modes HG00 (eps 0), HG01 and HG10 (eps 1), HG02 (eps 2) and to resonant entries.
Unlike the random-tensor toy (exchange couplings ~ 1/(3 sqrt(J)) ~ 0.02 of the self/cross-phase ones), the exchange couplings
here are O(1), so power exchange happens within a few L_NL. x- and y-parity are extra exact symmetries of this subset.
Usage: python exact_vs_twa_grin.py TAG f0,f1a,f1b,f2 n1 n2 ...   (writes exact_vs_twa_grin4_TAG.json)"""
import numpy as np, json, sys, os, time
import exact_vs_twa as ev
from grin_overlaps import grin_tensor

modes6, groups6, S6 = grin_tensor(3)
SEL = [0, 1, 2, 3]
S = S6[np.ix_(SEL, SEL, SEL, SEL)]; eps = groups6[SEL].astype(float)
res = (eps[:, None, None, None] + eps[None, :, None, None]) == (eps[None, None, :, None] + eps[None, None, None, :])
R = np.where(res, S, 0.0)
ev.S = S; ev.R = R; ev.quartets = [tuple(x) for x in np.argwhere(np.abs(R) > 1e-14)]; ev.T = np.einsum('pqps->qs', R)

if __name__ == '__main__':
    tag = sys.argv[1]; FRAC = np.array([float(x) for x in sys.argv[2].split(',')]); FRAC /= FRAC.sum(); ev.FRAC = FRAC
    fn = f'exact_vs_twa_grin4_{tag}.json'
    out = json.load(open(fn)) if os.path.exists(fn) else []
    for n in [int(x) for x in sys.argv[3:]]:
        t0 = time.time(); g = 1.0/n
        alpha = np.sqrt(n*FRAC)*np.exp(1j*ev.PH)
        zs = list(np.linspace(0, 6*np.sqrt(n), 31)[1:])
        ce, fe, n0e, info = ev.exact(alpha, zs, g); te = time.time() - t0
        cw, fw, ecw, efw = ev.twa(alpha, zs, g, weyl=True, seed=2000 + n)
        cb, fb, ecb, efb = ev.twa(alpha, zs, g, weyl=False, seed=2000 + n)
        cf = ev.frozen(n, zs, g)
        r = dict(tensor='grin4', modes=[list(modes6[i]) for i in SEL], tag='grin4_' + tag, frac=FRAC.tolist(), n=n, z=[float(z) for z in zs],
                 coh_exact=ce.tolist(), fano_exact=fe.tolist(), n0_exact=n0e.tolist(),
                 coh_twa_weyl=cw, coh_twa_weyl_err=ecw, fano_twa_weyl=fw, fano_twa_weyl_err=efw,
                 coh_twa_bare=cb, coh_twa_bare_err=ecb, fano_twa_bare=fb, fano_twa_bare_err=efb, coh_frozen=cf,
                 zhalf_exact=ev.zhalf(zs, ce), zhalf_twa_weyl=ev.zhalf(zs, cw), zhalf_twa_bare=ev.zhalf(zs, cb), zhalf_frozen=ev.zhalf(zs, cf),
                 exact_info=info, wall_exact_s=te, wall_total_s=time.time() - t0)
        out = [o for o in out if o['n'] != n] + [r]; out.sort(key=lambda o: o['n'])
        json.dump(out, open(fn, 'w'), indent=1)
        dce = np.max(np.abs(ce - np.array(cw))); dfe = np.max(np.abs(fe - np.array(fw)))
        zr = lambda k: (r[k]/np.sqrt(n) if r[k] else float('nan'))
        print(f"grin4_{tag} n={n}: norm {info['norm']:.8f} maxdim {info['maxdim']} sectors {info['nsec']}; z_half/sqrt(n): exact {zr('zhalf_exact'):.4f}, "
              f"TWA-weyl {zr('zhalf_twa_weyl'):.4f}, TWA-bare {zr('zhalf_twa_bare'):.4f}, frozen {zr('zhalf_frozen'):.4f}; "
              f"max|coh ex-weyl| {dce:.4f} (TWA err ~{max(ecw):.4f}); max|Fano ex-weyl| {dfe:.3f} (TWA err ~{max(efw):.3f}); Fano_exact max {max(fe):.2f}; "
              f"wall exact {te:.0f}s total {time.time()-t0:.0f}s", flush=True)
