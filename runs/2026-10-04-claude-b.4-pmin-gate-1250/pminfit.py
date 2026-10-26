"""Shared fitting helpers for the claude-b.4 P_min(L) runs (T-20261004-claude-interactive-03).

P_min is located by a local quadratic in x = ln P, never by the lowest sampled point:
  * fit3: the exact parabola through the lowest sampled point and its two neighbours;
  * fitls: least-squares parabola through the (up to) five points centred on the lowest sampled point.
The plateau power P_G0 (classical transfer slope G = dln n_D/dln N = 0) is located by linear interpolation in ln P of
the bright amplitude c (c = sqrt(N) dn/dN changes sign at P_G0).
"""
import math
import numpy as np


def _vertex(x, y):
    a, b, c = np.polyfit(x, y, 2)
    if a <= 0:
        return None
    xv = -b / (2 * a)
    return xv, float(np.polyval([a, b, c], xv)), float(a)


def fit_min(P, F, npts=3):
    P = np.asarray(P, float)
    F = np.asarray(F, float)
    order = np.argsort(P)
    P, F = P[order], F[order]
    i = int(np.argmin(F))
    if i == 0 or i == len(P) - 1:
        return {"ok": False, "reason": "lowest sampled point at the edge of the sweep", "P_sampled_min": float(P[i]),
                "F_sampled_min": float(F[i])}
    h = npts // 2
    lo, hi = max(0, i - h), min(len(P), i + h + 1)
    x = np.log(P[lo:hi])
    v = _vertex(x, F[lo:hi])
    if v is None:
        return {"ok": False, "reason": "parabola not convex"}
    xv, Fv, a = v
    inside = bool(x.min() <= xv <= x.max())
    # local spacing of the samples used, as a ratio
    spacing = float(np.max(np.diff(P[lo:hi]) / P[lo:hi][:-1]))
    return {"ok": True, "P_min_mw": float(math.exp(xv)), "F_min": Fv, "curvature_d2F_dlnP2": 2 * a,
            "points_used_mw": [float(p) for p in P[lo:hi]], "vertex_inside_points": inside,
            "max_relative_spacing": spacing, "P_sampled_min": float(P[i]), "F_sampled_min": float(F[i])}


def interp_at(P, Y, Pq, deg=2):
    """Local polynomial interpolation of Y(ln P) at Pq, using the deg+1 samples nearest to Pq in ln P."""
    P = np.asarray(P, float)
    Y = np.asarray(Y, float)
    o = np.argsort(np.abs(np.log(P) - math.log(Pq)))[: deg + 1]
    x = np.log(P[o])
    coef = np.polyfit(x - math.log(Pq), Y[o], deg)
    return float(coef[-1])


def zero_crossing(P, c):
    """First sign change of c(P) from + to -, linear in ln P. Returns None if no sign change in the sweep."""
    P = np.asarray(P, float)
    c = np.asarray(c, float)
    order = np.argsort(P)
    P, c = P[order], c[order]
    for k in range(len(P) - 1):
        if c[k] > 0 and c[k + 1] <= 0:
            x0, x1 = math.log(P[k]), math.log(P[k + 1])
            xz = x0 + (x1 - x0) * c[k] / (c[k] - c[k + 1])
            return {"P_G0_mw": float(math.exp(xz)), "bracket_mw": [float(P[k]), float(P[k + 1])]}
    return None
