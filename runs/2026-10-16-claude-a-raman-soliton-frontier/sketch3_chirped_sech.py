#!/usr/bin/env python3
"""Check of the card's sketch 3 (Chekhovskoy et al., arXiv:2003.02215, as quoted on the card): the chirped sech
q = A sech(t)^(1 + iC) has ZS eigenvalues i(sqrt(A^2 - C^2/4) - 1/2 - k), k = 0, 1, ... while positive. Two grids.
Usage: python sketch3_chirped_sech.py out.json"""
import json, sys
import numpy as np
import scipy.linalg as sla
from zs import Grid

out = sys.argv[1]
rows = []
for A in (2.0, 3.0):
    for C in (0.0, 1.0, 2.0, 3.0):
        pred = [np.sqrt(A**2 - C**2 / 4) - 0.5 - k for k in range(6)]
        pred = [p for p in pred if p > 0]
        res = []
        for n in (512, 768):
            g = Grid(n, 40.0)
            q = (A * np.cosh(g.t) ** (-(1 + 1j * C))).astype(complex)
            ev = sla.eigvals(g.M(q))
            ev = ev[(ev.imag > 0.05) & (np.abs(ev.real) < 0.5) & (np.abs(ev) < 50)]
            res.append(sorted(ev.imag, reverse=True)[:len(pred)])
        rows.append({"A": A, "C": C, "predicted": pred, "computed": [float(v) for v in res[1]],
                     "max_abs_err": float(max(abs(a - b) for a, b in zip(res[1], pred))) if len(res[1]) == len(pred) else None,
                     "two_grid": float(max(abs(a - b) for a, b in zip(res[0], res[1]))) if len(res[0]) == len(res[1]) and res[0] else None})
        print(json.dumps(rows[-1]), flush=True)
json.dump({"rows": rows}, open(out, "w"), indent=1)
