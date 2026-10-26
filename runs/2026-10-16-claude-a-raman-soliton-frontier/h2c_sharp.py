#!/usr/bin/env python3
"""H2c (frozen in HYPOTHESES.md, nineteenth freeze): leading ZS eigenvalue for random sharp-featured spectral masks on sech
and Gaussian lasers (A = 3, 4), against the TL value. Families: binary 0/pi phase segments; spectral holes with random smooth
phase; piecewise-linear (pulse-splitting) phase. 100 masks per family per (laser, A). Usage: python h2c_sharp.py out.json"""
import json, sys, time
import numpy as np
from zs import leading_fast
from h2_opt import Problem

out = sys.argv[1]
rng = np.random.default_rng(31)
rows = []
for laser in ("sech", "gauss"):
    for A in (3.0, 4.0):
        n = 512 if A <= 3 else 768
        pb = Problem(laser, A, n, 30.0 if laser == "sech" else 26.0, 10)
        k = pb.g.k; Q = pb.Q
        sup = np.abs(k[np.abs(Q) > 1e-4 * np.abs(Q).max()]).max()
        z0, _, _ = leading_fast(pb.g, pb.qtl, sigma=1j * (A + 0.3))
        eta_tl = float(z0.imag)
        best = -1.0
        for fam in ("binary", "holes", "split"):
            for trial in range(100):
                m = np.ones(n, complex)
                if fam == "binary":
                    cuts = np.sort(rng.uniform(-sup, sup, rng.integers(1, 8)))
                    seg = np.searchsorted(cuts, k)
                    flips = rng.integers(0, 2, len(cuts) + 1)
                    m = np.where(flips[seg] == 1, -1.0, 1.0).astype(complex)
                elif fam == "holes":
                    for _ in range(rng.integers(1, 5)):
                        c = rng.uniform(-sup, sup); w = rng.uniform(0.02, 0.3) * sup
                        m[np.abs(k - c) < w] = 0.0
                    x = np.clip(k / sup, -1, 1)
                    phi = sum(rng.normal(0, 1.0 / (j + 1)) * np.polynomial.legendre.legval(x, np.eye(j + 1)[j]) for j in range(2, 8))
                    m = m * np.exp(1j * phi)
                else:
                    cuts = np.sort(rng.uniform(-sup, sup, rng.integers(1, 4)))
                    seg = np.searchsorted(cuts, k)
                    slopes = rng.normal(0, 4.0, len(cuts) + 1)
                    m = np.exp(1j * slopes[seg] * k)
                S = m * Q
                q = np.fft.fftshift(np.fft.ifft(S))
                if np.abs(q).max() < 0.3:
                    continue
                z, _, _ = leading_fast(pb.g, q, sigma=1j * (np.abs(q).max() + 0.3))
                r = float(z.imag) / eta_tl
                best = max(best, r)
                rows.append({"laser": laser, "A": A, "family": fam, "trial": trial, "eta_ratio": r, "q_inf_ratio": float(np.abs(q).max() / A)})
        print(json.dumps({"laser": laser, "A": A, "eta_TL": eta_tl, "max_ratio": best,
                          "n": sum(1 for r in rows if r["laser"] == laser and r["A"] == A)}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
