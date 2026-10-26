"""Stage 3: two-solver verification of the best counterexample masks, and explicit low-order phase masks.

For the best search of each family: (i) BO on the line, cells T/4096, T/8192, T/16384, Romberg; (ii) FC with a full
eigensolver at a finer grid (smooth families: n = 1024, T = 128; per-bin: n = 768, T = 64, same bins); all
discrete eigenvalues of the masked pulse.  Explicit masks: cubic spectral phase phi = c (k-k0)^3/6 (scan), and
least-squares polynomial fits (degree 3-6, weight S^2 on k in [-3, 8]) of the optimal phase-only (Chebyshev) mask,
each evaluated on the line.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, '.')
from cx_common import *
sys.path.insert(0, '../2026-10-18-claude-interactive.9-mask-adversary')
from masks import Problem, Family

RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-18-claude-interactive.9-asym-counterexample')
ex = json.load(open('explore_summary.json'))
eta_TL = ex['eta_TL']
zTL = complex(*ex['TL_eigs_confirmed_BO'][0][:2])
n0, T0, K, kc = 384, 64.0, 13.0, 8.0
prob = Problem(S_src, n0, T0, K)


def romberg_line(mfun, z0, T):
    zs = []
    for nn in (4096, 8192, 16384):
        t, k = grid(nn, T)
        q = pulse_from_spectrum(mfun(k) * S_src(k), k, t, T)
        z, ares, it = bo_refine(q, T / nn, z0)
        zs.append(z)
        z0 = z
    r1 = [(4 * zs[1] - zs[0]) / 3, (4 * zs[2] - zs[1]) / 3]
    return (16 * r1[1] - r1[0]) / 15, zs


def fc_all(mfun, n, T):
    t, k = grid(n, T)
    q = pulse_from_spectrum(mfun(k) * S_src(k), k, t, T)
    w = fc_eigs(q, T, imag_min=0.03)
    return [z for z in w if abs(z.real) < 0.5 * np.pi * n / T], q, t


best = {'phase-cheb': 'nearTL', 'sharp': 'rand1', 'passive-cheb': 'rand1.5', 'passive-bins': 'nearTL'}
out = {"eta_TL_line": eta_TL, "families": {}}
for kind, start in best.items():
    d = np.load(os.path.join(RAW, 'mask_%s_%s.npz' % (kind, start)))
    x = d['x']
    fam = Family(prob, kind, J=24, kc=kc)
    if kind == 'passive-bins':
        m_grid, *_ = fam.mask(x)
        bins = np.round(prob.k / (2 * np.pi / T0)).astype(int)
        lut = dict(zip(bins, m_grid))
        mfun = lambda kk, lut=lut: np.array([lut.get(int(b), 1.0 + 0j) for b in np.round(kk / (2 * np.pi / T0)).astype(int)])
        Tl, nfc, Tfc = T0, 768, T0
    else:
        def mfun(kk, fam=fam, x=x):
            ph, ps, aux = fam.phipsi_at(x, kk)
            return np.cos(ps) * np.exp(1j * ph)
        Tl, nfc, Tfc = 96.0, 1024, 128.0
    zR, zs = romberg_line(mfun, zTL, Tl)
    wfc, q, t = fc_all(mfun, nfc, Tfc)
    kk = np.linspace(-40, 120, 160001)
    thr = float(np.sum(np.abs(mfun(kk) * S_src(kk)) ** 2) / np.sum(S_src(kk) ** 2)) if kind != 'passive-bins' else None
    rec = {"start": start, "eta_line_romberg": float(zR.imag), "zeta_line": [float(zR.real), float(zR.imag)],
           "eta_line_raw": [float(z.imag) for z in zs], "gain_over_TL": float(zR.imag / eta_TL - 1),
           "fc_eigs_fine": [[float(z.real), float(z.imag)] for z in wfc[:4]], "fc_grid": [nfc, Tfc],
           "fc_vs_line_diff": float(abs(wfc[0].imag - zR.imag)), "throughput_line": thr,
           "f1": float(4 * zR.imag / M0)}
    out['families'][kind] = rec
    print('%-13s line eta %.10f gain %+.4f%%  FC(%d,%g) %.10f  |diff| %.1e  other FC eigs %s' % (
        kind, zR.imag, 100 * rec['gain_over_TL'], nfc, Tfc, wfc[0].imag, rec['fc_vs_line_diff'],
        [round(z.imag, 5) for z in wfc[1:4]]), flush=True)

# explicit masks: cubic phase scan about k0 = 0 and about the spectral peak
peak = float(np.log(2 / np.pi * (1 + np.sqrt(1)) ) ) if False else None
rows = []
z0 = zTL
for k0 in (0.0, 0.4, 1.0):
    for c in np.linspace(-0.30, 0.0, 16):
        mfun = lambda kk, c=c, k0=k0: np.exp(1j * c * (kk - k0) ** 3 / 6)
        zR, zs = romberg_line(mfun, z0, 96.0)
        rows.append([k0, float(c), float(zR.imag), float(zR.imag / eta_TL - 1)])
        z0 = zR
    z0 = zTL
bestc = max(rows, key=lambda r: r[2])
out['cubic_phase_scan'] = rows
out['cubic_phase_best'] = bestc
print('cubic phase best: k0 %.1f c %.3f eta %.10f gain %+.4f%%' % (bestc[0], bestc[1], bestc[2], 100 * bestc[3]), flush=True)

# polynomial fits of the optimal phase-only Chebyshev mask
d = np.load(os.path.join(RAW, 'mask_phase-cheb_nearTL.npz'))
fam = Family(prob, 'phase-cheb', J=24, kc=kc)
kk = np.linspace(-3, 8, 2201)
ph, _, _ = fam.phipsi_at(d['x'], kk)
w = S_src(kk) ** 2
fits = []
for deg in (3, 4, 5, 6):
    A = np.vander(kk, deg + 1, increasing=True)
    coef = np.linalg.lstsq(A * np.sqrt(w)[:, None], ph * np.sqrt(w), rcond=None)[0]
    coef[:2] = 0.0                       # constant and linear phase do not change eta
    mfun = lambda k_, coef=coef: np.exp(1j * np.polyval(coef[::-1], np.clip(k_, -3, 8)))
    zR, zs = romberg_line(mfun, zTL, 96.0)
    fits.append({"degree": deg, "coef_increasing_powers_of_k": [float(c) for c in coef], "clip_k": [-3, 8],
                 "eta_line": float(zR.imag), "gain_over_TL": float(zR.imag / eta_TL - 1)})
    print('poly phase deg %d: eta %.10f gain %+.4f%%  coef %s' % (deg, zR.imag, 100 * fits[-1]['gain_over_TL'], np.round(coef, 5)), flush=True)
out['poly_phase_fits'] = fits
out['optimal_phase_samples'] = {"k": kk[::100].tolist(), "phi": ph[::100].tolist()}
json.dump(out, open('verify_summary.json', 'w'), indent=1, default=float)
