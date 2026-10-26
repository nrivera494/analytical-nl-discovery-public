"""Shared analysis helpers for the T-20261008-claude-b-01 runs (claude-b): load stored covariances, evaluate filter classes,
and the second-order invariants ||q||^2 and ||r||^2.

||q||^2 = || P_perp diag(c) Delta p ||^2, c = sqrt(p), P_perp = 1 - c c^T, Delta = C - J (J = all ones);
||r||^2 = || P_perp diag(delta) c ||^2.
For two modes with C = [[1, C12], [C12, C22]]: q = c1 c2 [ (1 - C22) p2 ... ] reduces to
||q||^2 = p1 p2 [ (C12 - 1)(p1 - p2) + (C22 - 1) p2 ]^2 ... computed numerically below to avoid algebra slips.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twomode_cov as tc

RAW = os.path.expanduser("~/analytical-nl-discovery-data")


def load(run_id, tag):
    d = np.load(os.path.join(RAW, run_id, tag + ".npz"))
    g = tc.Grid(int(d["N"]), float(d["TW"]))
    Ct, nt = tc.totals(d["nbar"], d["Cov"], g.N)
    return g, Ct, nt, d


def q2(p2, C12, C22):
    p = np.array([1 - p2, p2])
    c = np.sqrt(p)
    D = np.array([[1.0, C12], [C12, C22]]) - 1.0
    v = c * (D @ p)
    v = v - c * (c @ v)
    return float(v @ v)


def r2(p2, delta):
    p = np.array([1 - p2, p2])
    c = np.sqrt(p)
    v = np.array([0.0, delta]) * c
    v = v - c * (c @ v)
    return float(v @ v)


def scalar_optima(g, Ct, nt, kmax_max=20):
    """LP01 optimal filters in the four classes; returns dict class -> (F, T)."""
    A = tc.class_sym_hard(g, Ct, nt, range(0, kmax_max))
    kA = min(A, key=A.get)
    TA = (np.abs(g.k) <= kA).astype(float)
    Ap, _ = tc.class_sym_frac(g, Ct, nt, range(0, kmax_max))
    TAp = (np.abs(g.k) <= Ap["kmax"]).astype(float) + Ap["f"] * (np.abs(g.k) == Ap["kmax"] + 1)
    B = tc.class_interval(g, Ct, nt)
    TB = ((g.k >= B["k1"]) & (g.k <= B["k2"])).astype(float)
    starts = [TA, TAp, TB, np.ones(g.N), 0.5 * np.ones(g.N), (np.abs(g.k) <= kA + 2) * 0.7 + 0.0,
              (g.k >= 0).astype(float), (g.k <= 0).astype(float)]
    Cres, TC = tc.class_any(g, Ct, nt, starts)
    return {"sym_hard": (A[kA], TA, dict(kmax=kA)), "sym_frac": (Ap["F"], TAp, Ap),
            "interval": (B["F"], TB, B), "any": (Cres["F"], TC, {})}
