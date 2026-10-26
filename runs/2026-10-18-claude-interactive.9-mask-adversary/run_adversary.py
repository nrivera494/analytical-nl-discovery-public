"""Adversarial maximisation of eta_max over passive masks |m| <= 1, against the ceilings of C-20261018-pi-chatgpt-01.

For each source: TL eigenvalue on the optimisation grid; 13 L-BFGS-B searches over four mask families
(phase-only Chebyshev, amplitude-and-phase Chebyshev, per-bin amplitude and phase, sharp logistic steps), from
near-TL and random starts; the best mask of each family is re-evaluated (a) on a time grid refined 2x with the same
frequency bins (FC, full eigensolver), (b) as a line potential with Boffetta-Osborne transfer matrices and Romberg
extrapolation over three cell widths, and (c) for the smooth families, on a window doubled in T with the mask
evaluated as a function of k.  Ceilings: integer sech N - 1/2 (C); non-integer sech min_n U_2n (D); Gaussian (E).
Run with OPENBLAS_NUM_THREADS=1.
"""
import json, os, sys, time
import numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize_scalar
sys.path.insert(0, '.')
from masks import Problem, Family, optimise
sys.path.insert(0, '../2026-10-18-claude-interactive.9-zs-solver-validation')
from zs import grid, fc_eigs, bo_refine, logC, pulse_from_spectrum

RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-18-claude-interactive.9-mask-adversary')
os.makedirs(RAW, exist_ok=True)
SEED = 20261018
rng = np.random.default_rng(SEED)


def ceiling_sech(N):
    best = np.inf
    for n in range(1, 120):
        p = 2 * n
        logI = p * np.log(N) + 0.5 * np.log(np.pi) + gammaln(p / 2) - gammaln((p + 1) / 2)
        best = min(best, np.exp((logI - logC(p)) / (p - 1)))
    return best


def ceiling_gauss(N):
    f = lambda p: (p * np.log(N) + 0.5 * np.log(2 * np.pi / p) - logC(p)) / (p - 1)
    ps = np.linspace(2.0, 80.0, 7801)
    j = int(np.argmin([f(p) for p in ps]))
    r = minimize_scalar(f, bracket=(ps[max(j - 1, 0)] + 1e-9, ps[j], ps[j + 1]), tol=1e-14)
    return float(np.exp(r.fun))


CASES = []
for N in (2, 3, 4, 6, 2.5, 4.5, 7.5):
    CASES.append(dict(name='sech N=%g' % N, kind='sech', N=N, M0=2 * N ** 2,
                      S=(lambda N: (lambda k: N * np.pi / np.cosh(np.pi * k / 2)))(N),
                      qTL=(lambda N: (lambda t: N / np.cosh(t)))(N),
                      n=192 if N <= 4.5 else 256, T=36.0, K=12.0, ceiling=(N - 0.5) if float(N).is_integer() else ceiling_sech(N),
                      exact_TL=N - 0.5, held_out=N in (4.5, 7.5)))
for N in (1.5, 4, 5, 8):
    CASES.append(dict(name='gauss N=%g' % N, kind='gauss', N=N, M0=N ** 2 * np.sqrt(np.pi),
                      S=(lambda N: (lambda k: N * np.sqrt(2 * np.pi) * np.exp(-k ** 2 / 2)))(N),
                      qTL=(lambda N: (lambda t: N * np.exp(-t ** 2 / 2)))(N),
                      n=256, T=40.0, K=7.0, ceiling=ceiling_gauss(N), exact_TL=None, held_out=N in (1.5, 5, 8)))

only = sys.argv[1:]  # optional subset of case names


def starts(fam, K):
    """(label, x0, bounds) for each search of this family."""
    d = fam.dim
    out = []
    if fam.kind in ('phase-cheb', 'passive-cheb'):
        b = [(-4.0, 4.0)] * d
        out.append(('nearTL', rng.normal(0, 0.05, d), b))
        for s in (0.3, 0.8, 1.5):
            x = rng.normal(0, s, d)
            if fam.kind == 'passive-cheb':
                x[fam.Bphi.shape[1]:] *= 0.5
            out.append(('rand%.1f' % s, x, b))
    elif fam.kind == 'passive-bins':
        b = [(-3 * np.pi, 3 * np.pi)] * d
        out.append(('nearTL', rng.normal(0, 0.05, d), b))
        out.append(('rand0.6', rng.normal(0, 0.6, d), b))
    elif fam.kind == 'sharp':
        ns = fam.ns
        b = [(-2 * np.pi, 2 * np.pi)] * ns + [(-K, K)] * ns + [(-np.pi, np.pi)] * ns + [(-K, K)] * ns
        for r in range(3):
            x = np.concatenate([rng.normal(0, 1.5, ns), rng.uniform(-K / 3, K / 3, ns),
                                rng.normal(0, 0.6, ns), rng.uniform(-K / 3, K / 3, ns)])
            out.append(('rand%d' % r, x, b))
    return out


def verify(case, fam, x, prob):
    """Re-evaluate the mask: 2x time refinement (same bins), BO line problem (Romberg), and 2x window (smooth families)."""
    m, *_ = fam.mask(x)
    res = {}
    n, T = prob.n, prob.T
    # (a) refine time grid 2x, same frequency bins: zero-pad the spectrum beyond the old Nyquist with m = 1
    t2, k2 = grid(2 * n, T)
    m2 = np.ones(2 * n, complex)
    # map old bins (fftfreq order) into the new array
    idx_old = np.round(prob.k / (2 * np.pi / T)).astype(int)
    idx_new = np.round(k2 / (2 * np.pi / T)).astype(int)
    pos = {v: i for i, v in enumerate(idx_new)}
    for i_old, v in enumerate(idx_old):
        m2[pos[v]] = m[i_old]
    q2 = pulse_from_spectrum(m2 * case['S'](k2), k2, t2, T)
    w = fc_eigs(q2, T, imag_min=1e-3)
    w = [z for z in w if abs(z.real) < 0.6 * np.pi * 2 * n / T]
    res['fc_refined_eta'] = float(w[0].imag)
    res['fc_refined_zeta'] = [float(w[0].real), float(w[0].imag)]
    # (b) BO on the line, potential = the band-limited periodic pulse restricted to one window, Romberg over 3 widths
    zs = []
    z0 = w[0]
    for j in range(3):
        nn = 4 * n * 2 ** j
        t4, k4 = grid(nn, T)
        m4 = np.ones(nn, complex)
        idx4 = np.round(k4 / (2 * np.pi / T)).astype(int)
        pos4 = {v: i for i, v in enumerate(idx4)}
        for i_old, v in enumerate(idx_old):
            m4[pos4[v]] = m[i_old]
        q4 = pulse_from_spectrum(m4 * case['S'](k4), k4, t4, T)
        z, ares, it = bo_refine(q4, T / nn, z0)
        zs.append(z)
        z0 = z
    r1 = [(4 * zs[1] - zs[0]) / 3, (4 * zs[2] - zs[1]) / 3]
    res['bo_romberg_eta'] = float(((16 * r1[1] - r1[0]) / 15).imag)
    res['bo_raw_eta'] = [float(z.imag) for z in zs]
    # energy near the window edges (outer 10% on each side), relative to total
    q = prob.pulse(m)
    edge = np.abs(prob.t) > 0.4 * T
    res['edge_energy_fraction'] = float(np.sum(np.abs(q[edge]) ** 2) / np.sum(np.abs(q) ** 2))
    res['throughput'] = float(np.sum(np.abs(m * prob.S) ** 2) / np.sum(prob.S ** 2))
    # (c) doubled window, mask evaluated as a function of k (smooth families only)
    if fam.kind != 'passive-bins':
        P2 = Problem(case['S'], 2 * n, 2 * T, prob.K)
        F2 = Family(P2, fam.kind, J=24)
        m3, *_ = F2.mask(x)
        q3 = P2.pulse(m3)
        w3 = fc_eigs(q3, 2 * T, imag_min=1e-3)
        w3 = [z for z in w3 if abs(z.real) < 0.6 * np.pi * 2 * n / (2 * T)]
        res['fc_window2x_eta'] = float(w3[0].imag)
    return res


summary = {"seed": SEED, "cases": []}
t_all = time.time()
for case in CASES:
    if only and case['name'] not in only:
        continue
    tc = time.time()
    prob = Problem(case['S'], case['n'], case['T'], case['K'])
    q0 = prob.pulse(np.ones(case['n'], complex))
    zTL, vTL = prob.leading_full(q0)
    rec = {"name": case['name'], "kind": case['kind'], "N": case['N'], "held_out": case['held_out'],
           "grid": {"n": case['n'], "T": case['T'], "K": case['K']},
           "ceiling_eta": case['ceiling'], "TL_eta_grid": float(zTL.imag), "exact_TL": case['exact_TL'],
           "M0": case['M0'], "searches": []}
    best = {}
    for kind in ('phase-cheb', 'passive-cheb', 'passive-bins', 'sharp'):
        fam = Family(prob, kind, J=24)
        for label, x0, b in starts(fam, case['K']):
            # start the tracker from the TL eigenpair when the start is near TL, otherwise from a full solve
            z0, v0 = (zTL, vTL) if label == 'nearTL' else (None, None)
            res, eta = optimise(prob, fam, x0, bounds=b, maxiter=300 if kind != 'passive-bins' else 250, z0=z0, v0=v0)
            rec['searches'].append({"family": kind, "start": label, "eta": eta, "nfev": int(res.nfev), "nit": int(res.nit),
                                    "message": str(res.message), "tracked_eta_at_end": float(-res.fun),
                                    "excess_over_ceiling": eta - case['ceiling'], "rel_gain_over_TL_grid": eta / zTL.imag - 1})
            if kind not in best or eta > best[kind][0]:
                best[kind] = (eta, res.x.copy(), fam)
            print("%-11s %-13s %-7s eta %.12f  vs ceiling %+.3e  vs TL %+.3e  nfev %d" % (
                case['name'], kind, label, eta, eta - case['ceiling'], eta / zTL.imag - 1, res.nfev), flush=True)
    rec['best'] = {}
    for kind, (eta, x, fam) in best.items():
        v = verify(case, fam, x, prob)
        v['eta_opt_grid'] = eta
        rec['best'][kind] = v
        np.savez(os.path.join(RAW, '%s_%s_best.npz' % (case['name'].replace(' ', '_').replace('=', ''), kind)), x=x, k=prob.k, S=prob.S)
        print("   verify %-13s grid %.12f  refined %.12f  BO-R %.12f  2xT %s  edge %.1e  thru %.3f" % (
            kind, eta, v['fc_refined_eta'], v['bo_romberg_eta'], ('%.12f' % v['fc_window2x_eta']) if 'fc_window2x_eta' in v else '-',
            v['edge_energy_fraction'], v['throughput']), flush=True)
    famTL = Family(prob, 'phase-cheb', J=24)
    vTL = verify(case, famTL, np.zeros(famTL.dim), prob)
    rec['TL_verified'] = vTL
    TLv = vTL['bo_romberg_eta']
    vals = [max(v['fc_refined_eta'], v['bo_romberg_eta']) for v in rec['best'].values()]
    rec['best_verified_eta'] = max(vals)
    rec['best_verified_excess_over_ceiling'] = max(vals) - case['ceiling']
    rec['best_verified_rel_gain_over_TL'] = max(vals) / TLv - 1
    rec['ceiling_rel_headroom'] = case['ceiling'] / TLv - 1
    print("   verify TL            refined %.12f  BO-R %.12f" % (vTL['fc_refined_eta'], vTL['bo_romberg_eta']), flush=True)
    rec['wall_s'] = time.time() - tc
    summary['cases'].append(rec)
    print("== %s: TL %.12f ceiling %.12f best(verified) %.12f  gain %.3e of headroom %.3e  [%.0f s]" % (
        case['name'], zTL.imag, case['ceiling'], rec['best_verified_eta'], rec['best_verified_rel_gain_over_TL'],
        rec['ceiling_rel_headroom'], rec['wall_s']), flush=True)
    json.dump(summary, open(('part_' + '_'.join(o.replace(' ', '').replace('=', '') for o in only) + '.json') if only else 'summary.json', 'w'), indent=1, default=float)
summary['wall_time_s'] = time.time() - t_all
json.dump(summary, open(('part_' + '_'.join(o.replace(' ', '').replace('=', '') for o in only) + '.json') if only else 'summary.json', 'w'), indent=1, default=float)
