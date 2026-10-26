"""Stage 5: the mildly asymmetric held-out spectrum of C-20261016-claude-a-01, S = c sech(pi k/2) (1 + tanh(k)/2), with
c = A pi so that the TL peak is A (A = 2, 4). Same optimiser and mask families as search.py; best masks re-evaluated on
the line (BO, cells T/4096 and T/8192, Richardson)."""
import json, os, sys
import numpy as np
sys.path.insert(0, '.')
from cx_common import grid, pulse_from_spectrum, bo_refine
sys.path.insert(0, '../2026-10-18-claude-interactive.9-mask-adversary')
from masks import Problem, Family, optimise

rng = np.random.default_rng(11)
n, T, K = 256, 48.0, 12.0
out = {"grid": {"n": n, "T": T, "K": K}, "seed": 11, "cases": []}
for A in (2.0, 4.0):
    S = lambda k, A=A: A * np.pi / np.cosh(np.pi * k / 2) * (1 + 0.5 * np.tanh(k))
    prob = Problem(S, n, T, K)
    zTL, vTL = prob.leading_full(prob.pulse(np.ones(n, complex)))
    rows = []
    for kind, starts in (('phase-cheb', ['nearTL', 0.3, 0.8]), ('passive-cheb', ['nearTL', 0.5]),
                         ('passive-bins', ['nearTL', 0.5]), ('sharp', [0, 1])):
        fam = Family(prob, kind, J=24)
        for st in starts:
            if kind == 'sharp':
                ns = fam.ns
                x0 = np.concatenate([rng.normal(0, 1.5, ns), rng.uniform(-4, 4, ns), rng.normal(0, 0.6, ns), rng.uniform(-4, 4, ns)])
                b = [(-2 * np.pi, 2 * np.pi)] * ns + [(-K, K)] * ns + [(-np.pi, np.pi)] * ns + [(-K, K)] * ns
            else:
                x0 = rng.normal(0, 0.05 if st == 'nearTL' else st, fam.dim)
                b = [(-4.0, 4.0)] * fam.dim if kind != 'passive-bins' else [(-3 * np.pi, 3 * np.pi)] * fam.dim
            z0, v0 = (zTL, vTL) if st == 'nearTL' else (None, None)
            r, eta = optimise(prob, fam, x0, bounds=b, maxiter=300, z0=z0, v0=v0, check_every=25)
            rows.append((eta, kind, str(st), r.x, fam))
            print('A=%g %-13s %-6s eta %.12f gain %+.3e' % (A, kind, st, eta, eta / zTL.imag - 1), flush=True)
    eta, kind, st, x, fam = max(rows, key=lambda r: r[0])
    m, *_ = fam.mask(x)
    # line check of the best mask and of TL on the same footing (bins live on this window's frequency grid)
    bins = np.round(prob.k / (2 * np.pi / T)).astype(int)
    lut = dict(zip(bins, m))
    vals = {}
    for label, mm in (('TL', None), ('best', lut)):
        zs = []
        zz = zTL
        for nn in (4096, 8192):
            t2, k2 = grid(nn, T)
            mk = np.ones(nn, complex) if mm is None else np.array([mm.get(int(bb), 1.0 + 0j) for bb in np.round(k2 / (2 * np.pi / T)).astype(int)])
            q = pulse_from_spectrum(mk * S(k2), k2, t2, T)
            z, ares, it = bo_refine(q, T / nn, zz)
            zs.append(z)
            zz = z
        vals[label] = float(((4 * zs[1] - zs[0]) / 3).imag)
    rec = {"A": A, "eta_TL_grid": float(zTL.imag), "best_grid": {"family": kind, "start": st, "eta": eta},
           "line_eta_TL": vals['TL'], "line_eta_best": vals['best'], "gain_line": vals['best'] / vals['TL'] - 1,
           "all": [{"family": r[1], "start": r[2], "eta": r[0]} for r in rows]}
    out['cases'].append(rec)
    print('== A=%g: TL %.12f best %.12f (%s %s) line gain %+.3e' % (A, vals['TL'], vals['best'], kind, st, rec['gain_line']), flush=True)
json.dump(out, open('mild_asym_summary.json', 'w'), indent=1, default=float)
