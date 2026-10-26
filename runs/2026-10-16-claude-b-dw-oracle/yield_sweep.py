"""H2: transform-limited DW yield in model M0. For each case: band yield eta_B(xi) (w >= w_z), gated DW yield
eta_DW (field zeroed smoothly within |tau| < tg), Roy's NSR spectral-peak level, invariant drifts; each at step h and
h/2 (step convergence). Usage: python yield_sweep.py <set> ; results appended to yield_<set>.json."""
import numpy as np, json, sys, time, math
from dw_lib import *

def pow2(x):
    return 1 << int(math.ceil(math.log2(x)))

def setup(N, d3, xif, wfac=3.0, wmin=60.0, tg=15.0):
    wdw = 1/(2*d3)
    wmax = max(wfac*wdw, wmin)
    TW = max(2*(xif/(4*d3) + tg + 10), 40.0)
    Nt = pow2(TW*wmax/np.pi)
    return Nt, TW

def run_case(kind, N, d3, xif, xis, h, tg=15.0, Nt=None, TW=None):
    if Nt is None:
        Nt, TW = setup(N, d3, xif, tg=tg)
    out = dict(kind=kind, N=N, d3=d3, xif=xif, Nt=Nt, TW=TW, tg=tg)
    for lab, hh in [('h', h), ('h2', h/2)]:
        t0 = time.time()
        p = Prop(Nt, TW, N, d3, xif, hh, 4)
        u0 = (np.exp(-p.tau**2/2) if kind == 'gauss' else 1/np.cosh(p.tau)) + 0j
        E0 = spectrum(u0).sum()
        u, _, snaps = p.run(u0, record=list(xis))
        I0 = invariants(u0, p.w, p.dt, N, d3); I1 = invariants(u, p.w, p.dt, N, d3)
        r = dict(h=p.h, wall=None)
        r['eta_B'] = {f'{x:g}': band_fraction(snaps[x], p.w, p.wz, E0) for x in xis}
        r['eta_DW'] = gated_fraction(u, p.tau, p.w, p.wz, E0, tg=tg)
        r['eta_DW_tg_plus5'] = gated_fraction(u, p.tau, p.w, p.wz, E0, tg=tg + 5)
        pk, wpk, pk_out = nsr_peak(u, u0, p.w, p.wz)
        r['nsr_dB_input'] = pk; r['nsr_w'] = wpk; r['nsr_dnuT0'] = wpk/(2*np.pi); r['nsr_dB_outmax'] = pk_out
        r['inv_start'] = I0; r['inv_end'] = I1
        r['dE_rel'] = (I1[0] - I0[0])/I0[0]; r['dP'] = I1[1] - I0[1]; r['dH_rel'] = (I1[2] - I0[2])/abs(I0[2])
        r['leak0'] = band_fraction(u0, p.w, p.wz, E0)
        # numerical floor proxy: band power beyond 0.9 wmax (should be ~0)
        S = spectrum(u); r['edge_frac'] = S[np.abs(p.w) > 0.9*np.abs(p.w).max()].sum()/E0
        r['wall'] = time.time() - t0
        out[lab] = r
    out['conv_eta_DW'] = abs(out['h']['eta_DW'] - out['h2']['eta_DW'])/max(out['h2']['eta_DW'], 1e-300)
    out['conv_eta_B'] = abs(out['h']['eta_B'][f'{xif:g}'] - out['h2']['eta_B'][f'{xif:g}'])/max(out['h2']['eta_B'][f'{xif:g}'], 1e-300)
    return out

SETS = {
    'roy': [('sech', 2.0, d3, 4.0, [0.5, 1.0, 2.0, 3.0, 4.0], 1e-3) for d3 in [0.02, 0.03, 0.04, 0.06, 0.10]],
    'sech2a': [('sech', 2.0, d3, 4.0, [0.5, 1.0, 2.0, 3.0, 4.0], 1e-3) for d3 in [0.008, 0.010, 0.012, 0.016]],
    'g3': [('gauss', 3.0, d3, 2.0, [0.5, 1.0, 1.5, 2.0], 5e-4) for d3 in [0.0043, 0.0047, 0.0052, 0.0058, 0.0066, 0.0075, 0.009, 0.011]],
    's3': [('sech', 3.0, d3, 2.0, [0.5, 1.0, 1.5, 2.0], 5e-4) for d3 in [0.0043, 0.0047, 0.0052, 0.0058, 0.0066, 0.0075, 0.009, 0.011]],
    'g4': [('gauss', 4.0, d3, 1.0, [0.5, 1.0], 2.5e-4) for d3 in [0.0028, 0.0031, 0.0034, 0.0038, 0.0043, 0.005, 0.006]],
    'cardA': [('gauss', N, d3, 2.0, [0.5, 1.0, 1.5, 2.0], min(1e-3, 0.01/N**2)) for N in [3.0, 4.0, 6.0] for d3 in [0.01, 0.02, 0.03, 0.05]],
    'cardB': [('gauss', N, d3, 2.0, [0.5, 1.0, 1.5, 2.0], min(1e-3, 0.01/N**2)) for N in [8.0, 10.0] for d3 in [0.01, 0.02, 0.03, 0.05]],
    'g3L1': [('gauss', 3.0, d3, 1.0, [0.5, 1.0], 5e-4) for d3 in [0.0043, 0.0047, 0.0052, 0.0058]],
    's4a': [('sech', 4.0, d3, 2.0, [1.0, 2.0], 2e-4) for d3 in [0.0029, 0.0035]],
    's4b': [('sech', 4.0, d3, 2.0, [1.0, 2.0], 2e-4) for d3 in [0.0032, 0.0039]],
    's4c': [('sech', 4.0, 0.0024, 2.0, [1.0, 2.0], 2e-4)],
    's4d': [('sech', 4.0, 0.0026, 2.0, [1.0, 2.0], 2e-4)],
    'sech2b': [('sech', 2.0, d3, 4.0, [0.5, 1.0, 2.0, 3.0, 4.0], 1e-3) for d3 in [0.009, 0.011, 0.014, 0.018, 0.022, 0.025, 0.030]],
}

if __name__ == '__main__':
    name = sys.argv[1]
    cases = SETS[name]
    res = []
    for c in cases:
        r = run_case(*c)
        res.append(r)
        hh = r['h2']
        print(name, c[0], c[1], c[2], 'Nt', r['Nt'], 'TW', r['TW'], 'etaB(xif)', '%.4e' % hh['eta_B'][f'{c[3]:g}'],
              'etaDW', '%.4e' % hh['eta_DW'], 'conv', '%.1e' % r['conv_eta_DW'], 'NSR dB', round(hh['nsr_dB_input'], 2),
              'dnuT0', round(hh['nsr_dnuT0'], 3), 'dH', '%.1e' % hh['dH_rel'], 'dP', '%.1e' % hh['dP'],
              'wall', round(hh['wall'], 1), flush=True)
        json.dump(res, open(f'yield_{name}.json', 'w'), indent=1, default=float)
