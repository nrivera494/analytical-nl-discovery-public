"""Exact quantum dynamics vs truncated Wigner (TWA): mean-field collapse and number fluctuations of a condensate
(C-20261016-claude-interactive.7-02, assumption "truncated Wigner represents the quantum dynamics").

System: 4 modes of the resonant toy (resonant_model.build(K=3, J=400, seed=0)): fundamental (eps 0), two group-1 modes
(eps 1), one group-2 mode (eps 2); the tensor is restricted to these modes and to resonant entries.
H = (g/2) sum_res R_pqrs a+_p a+_q a_r a_s with g = 1/n, so L_NL = 1 for the total photon number n.
N and Q = n_1a + n_1b + 2 n_2 are conserved; the coherent input is split into (N, Q) sectors that are diagonalized exactly.
Sign convention: the state is evolved with exp(+iHz), so that the Heisenberg equation da/dz = +i dH/da+ matches the classical
(focusing-Kerr) equation dA/dz = +i g sum R A* A A used by every truncated-Wigner code in these run folders. (A first version
used exp(-iHz); that is the same as conjugating the input phases, which leaves the self/cross-phase collapse unchanged but
shifts the exchange dynamics, and showed up as an n-independent lag of the Fano-factor dip.)
Input: coherent state with mode powers n*FRAC (set on the command line) and fixed phases (0, 0.7, 1.9, 2.6).
Observables of the fundamental: coh_0 = |<a_0>|^2/<n_0> and the Fano factor F_0 = Var(n_0)/<n_0>.
TWA: Wigner sampling (vacuum noise 1/2 per mode), RK4, B = 20000 trajectories, jackknife errors over 10 blocks.
  'weyl': classical equations from the Weyl symbol H_W = H_cl - g sum_qs T_qs A_q* A_s, T_qs = sum_p R_pqps (consistent TWA);
  'bare': H_cl only (as in the large-n runs of the scrambling run folders).
Frozen-power reference (exact for SPM/XPM-only dynamics about the input powers):
  coh_0 = exp(-4 sum_q n_q sin^2(Lambda_0q z/2)), Lambda_00 = g S_0000, Lambda_0q = 2 g S_00qq.
Usage: python exact_vs_twa.py TAG f0,f1a,f1b,f2 n1 n2 ...   (appends to exact_vs_twa_TAG.json)
  TAG condensate85: powers n*(0.85, 0.05, 0.05, 0.05); TAG mixing55: n*(0.55, 0.15, 0.15, 0.15).
"""
import numpy as np, json, time, sys, os, warnings
warnings.filterwarnings('ignore')
from scipy.special import gammaln
import resonant_model as rm

groups6, eps6, u6, S6, R6 = rm.build(3, 400, 0)
sel = [0, int(np.where(groups6 == 1)[0][0]), int(np.where(groups6 == 1)[0][1]), int(np.where(groups6 == 2)[0][0])]
S = S6[np.ix_(sel, sel, sel, sel)]; eps = eps6[sel]; M = 4
res = (eps[:, None, None, None] + eps[None, :, None, None]) == (eps[None, None, :, None] + eps[None, None, None, :])
R = np.where(res, S, 0.0)
quartets = [tuple(x) for x in np.argwhere(np.abs(R) > 1e-14)]
T = np.einsum('pqps->qs', R)
FRAC = np.array([0.85, 0.05, 0.05, 0.05]); PH = np.array([0.0, 0.7, 1.9, 2.6])

def q_basis(Q):
    return np.array([(a, Q - 2*c - a, c) for c in range(Q//2 + 1) for a in range(Q - 2*c + 1)], dtype=int)

def sector_H(N, Q, g, basis):
    occ = np.column_stack([N - basis.sum(1), basis])
    valid = occ[:, 0] >= 0
    vi = np.where(valid)[0]; occv = occ[vi].astype(float); dim = len(vi)
    idx3 = -np.ones((Q + 1, Q + 1, Q//2 + 1), dtype=int)
    idx3[basis[vi, 0], basis[vi, 1], basis[vi, 2]] = np.arange(dim)
    H = np.zeros((dim, dim))
    for (p, q, r, s) in quartets:
        o = occv.copy()
        amp = np.sqrt(np.maximum(o[:, s], 0)); o[:, s] -= 1
        amp *= np.sqrt(np.maximum(o[:, r], 0)); o[:, r] -= 1
        o[:, q] += 1; amp *= np.sqrt(np.maximum(o[:, q], 0)); o[:, p] += 1; amp *= np.sqrt(np.maximum(o[:, p], 0))
        ok = (amp != 0) & (o.min(1) >= 0)
        if not ok.any(): continue
        oi = o[ok].astype(int); i = np.where(ok)[0]
        j = idx3[oi[:, 1], oi[:, 2], oi[:, 3]]
        good = j >= 0
        np.add.at(H, (j[good], i[good]), 0.5*g*R[p, q, r, s]*amp[ok][good])
    return vi, occ, H

def exact(alpha, zs, g, nsig_N=6.5, nsig_Q=7.0, wmin=1e-11):
    nbar = np.abs(alpha)**2; ntot = nbar.sum(); zs = np.asarray(zs)
    Nlo, Nhi = int(max(0, ntot - nsig_N*np.sqrt(ntot))), int(ntot + nsig_N*np.sqrt(ntot)) + 2
    qbar = nbar[1] + nbar[2] + 2*nbar[3]; qsd = np.sqrt(nbar[1] + nbar[2] + 4*nbar[3])
    Qlo, Qhi = int(max(0, qbar - nsig_Q*qsd - 2)), int(qbar + nsig_Q*qsd + 3)
    la_ = np.log(np.abs(alpha) + 1e-300); ph = np.angle(alpha)
    num = np.zeros(len(zs), complex); n0 = np.zeros(len(zs)); n0sq = np.zeros(len(zs)); norm = 0.0; maxdim = 0; nsec = 0
    for Q in range(Qlo, Qhi + 1):
        basis = q_basis(Q); prev = None; prevN = None
        for N in range(Nlo, Nhi + 1):
            occ = np.column_stack([N - basis.sum(1), basis]).astype(float)
            ok = occ[:, 0] >= 0
            if not ok.any(): prev = None; continue
            la = np.where(ok, (occ*la_).sum(1) - 0.5*gammaln(np.maximum(occ, 0) + 1).sum(1) - 0.5*ntot, -np.inf)
            amp = np.where(ok, np.exp(la)*np.exp(1j*(occ*ph).sum(1)), 0)
            w8 = np.sum(np.abs(amp)**2)
            if w8 < wmin: prev = None; continue
            vi, occ_i, H = sector_H(N, Q, g, basis)
            w, V = np.linalg.eigh(H); c = V.T @ amp[vi]
            Psi = np.zeros((len(basis), len(zs)), complex)
            Psi[vi] = V @ (np.exp(1j*np.outer(w, zs))*c[:, None])   # exp(+iHz): same sign as the classical dA/dz = +i dH/dA*
            P2 = np.abs(Psi)**2; o0 = np.maximum(occ[:, 0], 0)[:, None]
            n0 += (P2*o0).sum(0); n0sq += (P2*o0**2).sum(0); norm += w8; maxdim = max(maxdim, len(vi)); nsec += 1
            if prev is not None and prevN == N - 1:
                num += (np.conj(prev)*np.sqrt(o0)*Psi).sum(0)
            prev = Psi; prevN = N
    coh = np.abs(num)**2/n0; fano = (n0sq - n0**2)/n0
    return coh, fano, n0, dict(norm=norm, maxdim=maxdim, nsec=nsec)

def twa(alpha, zs, g, weyl=True, B=20000, nblk=10, dz=0.02, seed=0):
    rng = np.random.default_rng(seed)
    A = np.tile(alpha[:, None], (1, B)) + (rng.standard_normal((M, B)) + 1j*rng.standard_normal((M, B)))*0.5
    R2 = R.reshape(M, -1); Tw = T if weyl else 0*T
    def f(A):
        v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
        return 1j*g*(R2 @ v - Tw @ A)
    blk = np.arange(B) % nblk
    def obs(X):
        a = X[0]; m = a.mean(); p = np.abs(a)**2; n0 = p.mean() - 0.5
        return np.abs(m)**2/n0, (p.var() - 0.25)/n0
    out_c, out_f, err_c, err_f = [], [], [], []; z = 0.0
    for zt in zs:
        while z < zt - 1e-12:
            h = min(dz, zt - z)
            k1 = f(A); k2 = f(A + 0.5*h*k1); k3 = f(A + 0.5*h*k2); k4 = f(A + h*k3); A = A + h*(k1 + 2*k2 + 2*k3 + k4)/6; z += h
        c, fa = obs(A)
        jk = np.array([obs(A[:, blk != b]) for b in range(nblk)])
        ec = np.sqrt((nblk - 1)/nblk*np.sum((jk[:, 0] - jk[:, 0].mean())**2))
        ef = np.sqrt((nblk - 1)/nblk*np.sum((jk[:, 1] - jk[:, 1].mean())**2))
        out_c.append(float(c)); out_f.append(float(fa)); err_c.append(float(ec)); err_f.append(float(ef))
    return out_c, out_f, err_c, err_f

def frozen(n, zs, g):
    nq = n*FRAC; Lam = np.array([g*S[0, 0, 0, 0]] + [2*g*S[0, 0, q, q] for q in range(1, M)])
    return [float(np.exp(-4*np.sum(nq*np.sin(Lam*z/2)**2))) for z in zs]

def zhalf(zz, cc):
    for i in range(1, len(cc)):
        if cc[i] < 0.5 <= cc[i - 1]: return float(zz[i - 1] + (0.5 - cc[i - 1])*(zz[i] - zz[i - 1])/(cc[i] - cc[i - 1]))
    return None

if __name__ == '__main__':
    tag = sys.argv[1]; FRAC = np.array([float(x) for x in sys.argv[2].split(',')]); FRAC /= FRAC.sum()
    fn = f'exact_vs_twa_{tag}.json'
    out = json.load(open(fn)) if os.path.exists(fn) else []
    for n in [int(x) for x in sys.argv[3:]]:
        t0 = time.time(); g = 1.0/n
        alpha = np.sqrt(n*FRAC)*np.exp(1j*PH)
        zs = list(np.linspace(0, 6*np.sqrt(n), 31)[1:])
        ce, fe, n0e, info = exact(alpha, zs, g); te = time.time() - t0
        cw, fw, ecw, efw = twa(alpha, zs, g, weyl=True, seed=1000 + n)
        cb, fb, ecb, efb = twa(alpha, zs, g, weyl=False, seed=1000 + n)
        cf = frozen(n, zs, g)
        r = dict(tag=tag, frac=FRAC.tolist(), n=n, z=[float(z) for z in zs], coh_exact=ce.tolist(), fano_exact=fe.tolist(), n0_exact=n0e.tolist(),
                 coh_twa_weyl=cw, coh_twa_weyl_err=ecw, fano_twa_weyl=fw, fano_twa_weyl_err=efw,
                 coh_twa_bare=cb, coh_twa_bare_err=ecb, fano_twa_bare=fb, fano_twa_bare_err=efb, coh_frozen=cf,
                 zhalf_exact=zhalf(zs, ce), zhalf_twa_weyl=zhalf(zs, cw), zhalf_twa_bare=zhalf(zs, cb), zhalf_frozen=zhalf(zs, cf),
                 exact_info=info, wall_exact_s=te, wall_total_s=time.time() - t0)
        out = [o for o in out if o['n'] != n] + [r]; out.sort(key=lambda o: o['n'])
        json.dump(out, open(fn, 'w'), indent=1)
        dce = np.max(np.abs(ce - np.array(cw))); dfe = np.max(np.abs(fe - np.array(fw)))
        zr = lambda k: (r[k]/np.sqrt(n) if r[k] else float('nan'))
        print(f"{tag} n={n}: norm {info['norm']:.8f} maxdim {info['maxdim']} sectors {info['nsec']}; z_half/sqrt(n): exact {zr('zhalf_exact'):.4f}, "
              f"TWA-weyl {zr('zhalf_twa_weyl'):.4f}, TWA-bare {zr('zhalf_twa_bare'):.4f}, frozen {zr('zhalf_frozen'):.4f}; "
              f"max|coh ex-weyl| {dce:.4f} (TWA err ~{max(ecw):.4f}); max|Fano ex-weyl| {dfe:.3f} (TWA err ~{max(efw):.3f}); Fano_exact max {max(fe):.2f}; "
              f"wall exact {te:.0f}s total {time.time()-t0:.0f}s", flush=True)
