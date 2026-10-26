"""Sweep and convergence checks for c_eff(y) at fixed Phi (claude-interactive.12).

Usage: python sweep.py <raw_dir>   (writes main.jsonl and conv.jsonl there)
Single process, sequential.
"""
import json
import os
import sys

import numpy as np

import lam_min as L

RAW = sys.argv[1]
os.makedirs(RAW, exist_ok=True)
XW = 10.0


def N_for(y, per_sigma=3.0, Xw=XW):
    sig = (y / 24) ** 0.25
    return int(2 ** np.ceil(np.log2(2 * Xw * per_sigma / sig)))


def emit(fn, r):
    with open(os.path.join(RAW, fn), 'a') as f:
        f.write(json.dumps(r) + '\n')
    print(fn, json.dumps({k: r[k] for k in ('tag', 'Phi', 'y', 'N', 'ne', 'parity', 'method', 'rtol', 'nsteps',
                                            'lam_min', 'c_eff', 'edge_amp_rel', 'wall_s') if k in r}), flush=True)


what = sys.argv[2] if len(sys.argv) > 2 else 'all'
YS = [1e-4, 5e-5, 2e-5, 1e-5, 5e-6, 2e-6, 1e-6, 5e-7, 2e-7, 1e-7]
PHIS = [1.0, 1.5, 3.0, 7.0]

if what in ('all', 'main'):
    for Phi in PHIS:
        for y in YS:
            r = L.lam_min(Phi, y, N_for(y))
            r['tag'] = 'main'
            emit('main.jsonl', r)
    # below 1e-7 (noise floor) and the source's two table points
    for Phi in [3.0, 7.0]:
        for y in [5e-8, 2e-8]:
            r = L.lam_min(Phi, y, N_for(y))
            r['tag'] = 'main-small'
            emit('main.jsonl', r)
    for Phi, y in [(10.0, 1e-6), (2.0, 1e-6), (10.0, 1e-5), (2.0, 1e-5)]:
        r = L.lam_min(Phi, y, N_for(y))
        r['tag'] = 'source-table'
        emit('main.jsonl', r)

if what in ('all', 'conv'):
    for Phi in [1.0, 3.0, 7.0]:
        for y in [1e-4, 1e-7]:
            N0 = N_for(y)
            base = dict(Phi=Phi, y=y)
            cases = [('grid-2N', dict(N=2 * N0)),
                     ('window-Xw8', dict(N=N0, Xw=8.0)),
                     ('window-Xw14', dict(N=2 * N0, Xw=14.0)),
                     ('input-7sigma', dict(N=N0, nin_sigma=7.0)),
                     ('input-14sigma', dict(N=N0, nin_sigma=14.0)),
                     ('rtol-1e-12', dict(N=N0, rtol=1e-12)),
                     ('rtol-3e-14', dict(N=N0, rtol=3e-14))]
            for tag, kw in cases:
                r = L.lam_min(Phi, y, **kw)
                r['tag'] = tag
                emit('conv.jsonl', r)
        r = L.lam_min(Phi, 1e-6, N_for(1e-6), parity='both')
        r['tag'] = 'parity-both'
        emit('conv.jsonl', r)
    # second integrator: fixed-step RK4IP, two step counts (Richardson offline)
    for Phi, y in [(1.0, 1e-4), (3.0, 1e-4), (7.0, 1e-4), (3.0, 1e-6)]:
        for ns in [1000, 2000]:
            r = L.lam_min(Phi, y, N_for(y), method='rk4ip', nsteps=ns)
            r['tag'] = 'rk4ip'
            emit('conv.jsonl', r)

if what == 'sech':
    # shape specificity: sech pulse (intensity sech^2 x, same curvature as e^{-x^2}); wider window
    for Phi in [3.0, 1.0]:
        for y in [1e-4, 3e-5, 1e-5, 3e-6, 1e-6]:
            r = L.lam_min(Phi, y, N_for(y, Xw=25.0), Xw=25.0, profile='sech')
            r['tag'] = 'sech'
            emit('sech.jsonl', r)

if what == 'tight':
    # smallest y again at the tightest DOP853 tolerance (rtol 3e-14)
    for Phi in PHIS:
        for y in [1e-6, 5e-7, 2e-7, 1e-7]:
            r = L.lam_min(Phi, y, N_for(y), rtol=3e-14)
            r['tag'] = 'tight'
            emit('tight.jsonl', r)

if what == 'smallphi':
    # non-uniformity as Phi -> 0 (c2 ~ Phi^-2): Phi = 0.5 and 0.25, same y grid as main
    for Phi in [0.5, 0.25]:
        for y in [1e-4, 5e-5, 2e-5, 1e-5, 5e-6, 2e-6, 1e-6, 5e-7, 2e-7, 1e-7]:
            r = L.lam_min(Phi, y, N_for(y), rtol=3e-14)
            r['tag'] = 'smallphi'
            emit('smallphi.jsonl', r)

if what == 'full':
    # unrestricted input (all N grid points, both quadratures) against the restricted support, same coarse grid
    for Phi in [3.0, 1.0]:
        for par in ['full', 'even']:
            r = L.lam_min(Phi, 1e-4, 1024, parity=par)
            r['tag'] = 'full-vs-restricted'
            emit('full.jsonl', r)

if what == 'gq':
    # third shape, kappa4 = 0 (intensity exp(-x^2 - x^4/2)); prediction frozen in HELDOUT_kappa4.md
    for Phi in [3.0, 1.0]:
        for y in [1e-4, 3e-5, 1e-5, 3e-6, 1e-6]:
            r = L.lam_min(Phi, y, N_for(y), profile='gq', rtol=3e-14)
            r['tag'] = 'gq'
            emit('gq.jsonl', r)
