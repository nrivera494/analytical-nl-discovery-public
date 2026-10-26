"""H3: headroom of input spectral shaping for the band yield eta_B(xi_f) (photons at w >= w_z / laser photons),
model M0, TL Gaussian laser. Classes: GDD only; phase-only (Legendre P2..PK on the laser band); passive (phase +
per-bin amplitude in [0,1]). Optimizer: L-BFGS-B on -ln eta_B with exact discrete-adjoint gradients.
Usage: python optimize.py N d3 [xif] [h] [K]"""
import numpy as np, json, sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '2026-10-16-claude-b-dw-oracle'))
from dw_lib import *
from scipy.optimize import minimize

RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping')
os.makedirs(RAW, exist_ok=True)

def pow2(x):
    import math
    return 1 << int(math.ceil(math.log2(x)))

def setup(N, d3, xif):
    # effective resonance of the leading soliton (amplitude ~ 2N-1): d3 w^3 - w^2/2 = (2N-1)^2/2
    eta1 = 2*N - 1
    r = np.roots([d3, -0.5, 0, -0.5*eta1**2]); wdw = max(r[np.isreal(r)].real)
    wmax = max(2.5*wdw, 40.0)
    TW = max(2*(xif/(4*d3) + 25), 60.0)
    return pow2(TW*wmax/np.pi), TW, wdw

def main():
    N = float(sys.argv[1]); d3 = float(sys.argv[2])
    xif = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    h = float(sys.argv[4]) if len(sys.argv) > 4 else min(1e-3, 0.01/N**2*4)
    K = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    MAXIT = int(sys.argv[6]) if len(sys.argv) > 6 else 60
    OBJ = sys.argv[7] if len(sys.argv) > 7 else 'band'   # 'band' (ungated eta_B) or 'gated' (eta_DW, |tau|<15 excluded)
    tag = f'N{N:g}_d{d3:g}_xi{xif:g}_it{MAXIT}' + ('_gated' if OBJ == 'gated' else '') + (f'_TW{sys.argv[8]}' if len(sys.argv) > 8 else '')
    Nt, TW, wdw = setup(N, d3, xif)
    if len(sys.argv) > 8:   # window override (DW group delay can exceed xif/(4 d3) at large N)
        TW = float(sys.argv[8]); Nt = pow2(TW*max(2.5*wdw, 40.0)/np.pi)
    out = dict(N=N, d3=d3, xif=xif, h=h, K=K, maxiter=MAXIT, objective=OBJ, Nt=Nt, TW=TW, wDW_est=wdw)
    p = CkptProp(Nt, TW, N, d3, xif, h, order=4, every=100)
    ul = np.exp(-p.tau**2/2) + 0j
    t0 = time.time()
    MP = (lambda **kw: GatedCkptMaskProblem(p, ul, K=K, log=True, tg=15.0, **kw)) if OBJ == 'gated' else (lambda **kw: CkptMaskProblem(p, ul, K=K, log=True, **kw))
    mp = MP(passive=False)
    out['wl'] = mp.wl; out['nphi'] = mp.nphi; out['n_inband_bins'] = len(mp.inb)
    JTL, _ = mp.value(mp.x0())
    out['eta_TL'] = JTL
    out['leak0'] = band_fraction(ul, p.w, p.wz, mp.E0)
    # step convergence of the TL value
    p2 = CkptProp(Nt, TW, N, d3, xif, h/2, order=4, every=100)
    uT2 = p2.run_ckpt(ul)[0]
    JTL2 = band_fraction(mp.g*uT2 if OBJ == 'gated' else uT2, p.w, p.wz, mp.E0)
    out['eta_TL_h2'] = JTL2
    print(tag, 'Nt', Nt, 'TW', TW, 'eta_TL', JTL, 'h/2', JTL2, f'{time.time()-t0:.0f}s', flush=True)
    # GDD scan: phi = C w^2/2  ->  Legendre: C wl^2/2 * x^2,  x^2 = (2 P2 + P0)/3
    Cs = np.linspace(-2.5, 2.5, 51)
    gdd = []
    for C in Cs:
        x = mp.x0(); x[0] = C*mp.wl**2/3
        gdd.append(mp.value(x)[0])
    gdd = np.array(gdd); ib = int(np.argmax(gdd))
    out['gdd'] = dict(C=Cs.tolist(), eta=gdd.tolist(), C_best=Cs[ib], eta_best=gdd[ib], H_gdd=gdd[ib]/JTL)
    print(tag, 'GDD best C', Cs[ib], 'eta', gdd[ib], 'H_gdd', gdd[ib]/JTL, f'{time.time()-t0:.0f}s', flush=True)
    # phase-only optimisation from three starts
    rng = np.random.default_rng(int(N*1000 + d3*1e5))
    starts = {'TL': mp.x0(), 'GDD': None, 'random': 0.5*rng.standard_normal(mp.nphi)/np.arange(2, mp.nphi + 2)}
    xg = mp.x0(); xg[0] = Cs[ib]*mp.wl**2/3; starts['GDD'] = xg
    runs = {}
    best = (JTL, mp.x0(), 'TL0')
    for name, x0 in starts.items():
        hist = []
        def fg(x):
            f, g, J = mp.value_grad(x); hist.append(J); return f, g
        r = minimize(fg, x0, jac=True, method='L-BFGS-B', options=dict(maxiter=MAXIT, maxfun=int(1.3*MAXIT)))
        Jopt = mp.value(r.x)[0]
        runs[name] = dict(eta=Jopt, H=Jopt/JTL, nit=r.nit, nfev=r.nfev, msg=str(r.message), hist=hist,
                          gradnorm=float(np.linalg.norm(r.jac)))
        print(tag, 'phase start', name, 'eta', Jopt, 'H', Jopt/JTL, 'nit', r.nit, f'{time.time()-t0:.0f}s', flush=True)
        if Jopt > best[0]:
            best = (Jopt, r.x.copy(), name)
    out['phase'] = runs
    out['H_phase'] = best[0]/JTL; out['eta_phase'] = best[0]; out['phase_best_start'] = best[2]
    xb = best[1]
    phi_b, _ = mp.unpack(xb)
    # passive optimisation starting from the best phase-only mask (amplitudes 1)
    mpp = MP(passive=True)
    xp0 = np.concatenate([xb, np.ones(len(mpp.inb))])
    hist = []
    def fgp(x):
        f, g, J = mpp.value_grad(x); hist.append(J); return f, g
    r = minimize(fgp, xp0, jac=True, method='L-BFGS-B', bounds=mpp.bounds(), options=dict(maxiter=MAXIT, maxfun=int(1.3*MAXIT)))
    Jp = mpp.value(r.x)[0]
    phi_p, a_p = mpp.unpack(r.x)
    out['passive'] = dict(eta=Jp, H=Jp/JTL, nit=r.nit, nfev=r.nfev, msg=str(r.message), hist=hist,
                          energy_kept=float((a_p**2*np.abs(mpp.Q)**2).sum()/mpp.E0), amin=float(a_p[mpp.inb].min()))
    out['H_passive'] = max(Jp, best[0])/JTL
    print(tag, 'passive eta', Jp, 'H', Jp/JTL, 'energy kept', out['passive']['energy_kept'], f'{time.time()-t0:.0f}s', flush=True)
    # diagnostics of the best phase mask: gated yield, eta_B(xi), input peak power and duration
    u0b, _ = mp.input_field(xb)
    pr = Prop(Nt, TW, N, d3, xif, h, 4)
    xis = [0.25*k for k in range(int(round(xif/0.25)) + 1)]
    uf, _, sn = pr.run(u0b, record=xis)
    uT, _, snT = pr.run(ul + 0j, record=xis)
    out['best_phase_diag'] = dict(eta_xi={f'{x:g}': band_fraction(sn[x], p.w, p.wz, mp.E0) for x in xis},
                                  etaTL_xi={f'{x:g}': band_fraction(snT[x], p.w, p.wz, mp.E0) for x in xis},
                                  gated=gated_fraction(uf, p.tau, p.w, p.wz, mp.E0), gated_TL=gated_fraction(uT, p.tau, p.w, p.wz, mp.E0),
                                  peak_in=float(np.abs(u0b).max()**2), rms_width_in=float(np.sqrt((p.tau**2*np.abs(u0b)**2).sum()/(np.abs(u0b)**2).sum())),
                                  frac_in_central_half=float((np.abs(u0b[np.abs(p.tau) < TW/4])**2).sum()/(np.abs(u0b)**2).sum()))
    # masks for the solver cross-check: phi(w) and a(w) on the in-band bins
    wb = p.w[mp.inb]
    out['mask_phase'] = dict(w=wb.tolist(), phi=phi_b[mp.inb].tolist())
    out['mask_passive'] = dict(w=wb.tolist(), phi=phi_p[mpp.inb].tolist(), a=a_p[mpp.inb].tolist())
    out['wall_s'] = time.time() - t0
    np.savez(os.path.join(RAW, f'{tag}.npz'), xb=xb, xp=r.x, w=p.w, inb=mp.inb, phi_b=phi_b, phi_p=phi_p, a_p=a_p)
    json.dump(out, open(f'opt_{tag}.json', 'w'), indent=1, default=float)
    print(tag, 'DONE', 'H_gdd', out['gdd']['H_gdd'], 'H_phase', out['H_phase'], 'H_passive', out['H_passive'], f'{time.time()-t0:.0f}s', flush=True)

if __name__ == '__main__':
    main()
