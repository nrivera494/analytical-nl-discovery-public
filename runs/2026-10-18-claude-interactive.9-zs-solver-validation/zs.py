"""Independent Zakharov-Shabat (ZS) eigenvalue solver, written by claude-interactive.9 on 2026-10-18
for the verification of C-20261018-pi-chatgpt-01. It does not use the orchestrator's or the proposer's code.

Convention (the claim card's):  v' = [[-i z, q], [-conj(q), i z]] v,  bound states have Im z = eta > 0,
soliton energy 4 eta, NLSE i q_z + q_tt/2 + |q|^2 q = 0.  Spectrum convention q(t) = (1/2pi) int S(k) e^{ikt} dk.

Two independent discretisations:

1. Fourier collocation (FC) on a periodic window [-T/2, T/2) with n points (n even):
       z v = M v,   M = [[ i D, -i diag(q)], [-i diag(conj q), -i D]],
   D the Fourier differentiation matrix.  The left eigenvector of M is w = (v2, v1) exactly, so the
   discrete eigenvalue has the exact gradient
       dz = -i sum_j (v2_j^2 dq_j + v1_j^2 d(conj q)_j) / (2 sum_j v1_j v2_j).
2. Boffetta-Osborne (BO) transfer matrices for the problem on the whole line with the potential held constant on
   cells of width h (exact 2x2 exponential per cell; exponential-midpoint rule, error even in h, so Richardson
   extrapolation over h, h/2 is fourth order).  Bound states are zeros of a(z) = lim v1 e^{izt} for the Jost
   solution v ~ (e^{-izt}, 0) at t -> -inf; zeros are refined by secant iteration.
"""
import numpy as np


# ----------------------------------------------------------------------------------------------- grids

def grid(n, T):
    """Periodic grid t_j = (j - n/2) T/n and angular frequencies k (numpy FFT order)."""
    dt = T / n
    t = (np.arange(n) - n // 2) * dt
    k = 2 * np.pi * np.fft.fftfreq(n, d=dt)
    return t, k


def pulse_from_spectrum(Sm, k, t, T):
    """q(t_j) = (1/T) sum_l Sm(k_l) e^{i k_l t_j}: the discrete form of (1/2pi) int S e^{ikt} dk."""
    n = len(t)
    # e^{i k_l t_j} with t_j = t_0 + j dt: ifft gives (1/n) sum_l X_l e^{2 pi i l j / n} = (1/n) sum X_l e^{i k_l (t_j - t_0)}
    X = Sm * np.exp(1j * k * t[0])
    return np.fft.ifft(X) * n / T


# ------------------------------------------------------------------------------------- Fourier collocation

_DCACHE = {}


def fourier_diff_matrix(n, T):
    key = (n, T)
    if key not in _DCACHE:
        j = np.arange(n)
        d = j[:, None] - j[None, :]
        with np.errstate(divide='ignore', invalid='ignore'):
            D = (np.pi / T) * ((-1.0) ** d) / np.tan(np.pi * d / n)
        D[d == 0] = 0.0
        _DCACHE[key] = D
    return _DCACHE[key]


def fc_matrix(q, T):
    n = len(q)
    D = fourier_diff_matrix(n, T)
    M = np.empty((2 * n, 2 * n), dtype=complex)
    M[:n, :n] = 1j * D
    M[n:, n:] = -1j * D
    M[:n, n:] = np.diag(-1j * q)
    M[n:, :n] = np.diag(-1j * np.conj(q))
    return M


def fc_eigs(q, T, imag_min=1e-6, vectors=False):
    """All FC eigenvalues with Im z > imag_min, sorted by decreasing Im z (optionally with right eigenvectors)."""
    M = fc_matrix(q, T)
    if vectors:
        w, V = np.linalg.eig(M)
    else:
        w = np.linalg.eigvals(M)
    sel = np.where(w.imag > imag_min)[0]
    order = sel[np.argsort(-w.imag[sel])]
    if vectors:
        return w[order], V[:, order]
    return w[order]


def fc_track(q, T, z0, v0=None, iters=4, tol=1e-14):
    """Two-sided Rayleigh-quotient / inverse iteration for the FC eigenvalue nearest z0. Returns z, v (2n vector)."""
    import scipy.linalg as sla
    n = len(q)
    M = fc_matrix(q, T)
    I = np.eye(2 * n)
    x = v0.copy() if v0 is not None else np.random.default_rng(0).standard_normal(2 * n) + 0j
    z = z0
    for it in range(iters):
        lu = sla.lu_factor(M - z * I, check_finite=False)
        for _ in range(2):
            x = sla.lu_solve(lu, x, check_finite=False)
            x /= np.linalg.norm(x)
        v1, v2 = x[:n], x[n:]
        w = np.concatenate([v2, v1])
        znew = (w @ (M @ x)) / (w @ x)
        if abs(znew - z) < tol * max(1.0, abs(z)):
            z = znew
            break
        z = znew
    return z, x


def fc_grad(v, n):
    """Coefficients g, h with dz = sum_j g_j dq_j + h_j d(conj q)_j for the FC eigenvalue with right eigvec v."""
    v1, v2 = v[:n], v[n:]
    den = 2 * np.sum(v1 * v2)
    g = -1j * v2 ** 2 / den
    h = -1j * v1 ** 2 / den
    return g, h


# ---------------------------------------------------------------------------- Boffetta-Osborne transfer

def _cell_matrices(qs, h, z):
    """Scaled cell propagators e^{izh} exp(h [[-iz, q], [-conj q, iz]]) for an array of cell values qs."""
    k = np.sqrt(z * z + np.abs(qs) ** 2 + 0j)
    kh = k * h
    c = np.cos(kh)
    s = np.where(np.abs(kh) < 1e-8, h * (1 - kh ** 2 / 6), np.sin(kh) / np.where(k == 0, 1, k))
    e = np.exp(1j * z * h)
    T = np.empty((len(qs), 2, 2), dtype=complex)
    T[:, 0, 0] = e * (c - 1j * z * s)
    T[:, 0, 1] = e * s * qs
    T[:, 1, 0] = -e * s * np.conj(qs)
    T[:, 1, 1] = e * (c + 1j * z * s)
    return T


def _tree_product(T):
    """Ordered product T[n-1] @ ... @ T[1] @ T[0] by pairwise reduction."""
    while len(T) > 1:
        if len(T) % 2:
            T = np.concatenate([T, np.eye(2, dtype=complex)[None]], axis=0)
        T = np.matmul(T[1::2], T[0::2])
    return T[0]


def bo_a(qs, h, z):
    """a(z) for the line potential equal to qs[j] on consecutive cells of width h (zero outside)."""
    P = _tree_product(_cell_matrices(qs, h, z))
    return P[0, 0]


def bo_refine(qs, h, z0, tol=1e-15, maxit=60):
    """Zero of a(z) near z0 by the secant method. Returns (z, |a| at z, iterations)."""
    za, zb = z0, z0 * (1 + 1e-7) + 1e-7j
    fa, fb = bo_a(qs, h, za), bo_a(qs, h, zb)
    for it in range(maxit):
        if fb == fa:
            break
        zc = zb - fb * (zb - za) / (fb - fa)
        za, fa = zb, fb
        zb, fb = zc, bo_a(qs, h, zc)
        if abs(zb - za) < tol * max(1.0, abs(zb)):
            break
    return zb, abs(fb), it


def bo_eig_richardson(qfun, tL, tR, h, z0):
    """BO eigenvalue with cell width h and h/2 for an analytic potential qfun(t) on [tL, tR] (cell midpoints),
    and the Richardson value (4 z(h/2) - z(h))/3."""
    out = []
    for hh in (h, h / 2):
        n = int(round((tR - tL) / hh))
        tm = tL + (np.arange(n) + 0.5) * hh
        z, res, it = bo_refine(qfun(tm), hh, z0)
        out.append(z)
        z0 = z
    return out[0], out[1], (4 * out[1] - out[0]) / 3


# ------------------------------------------------------------------------------------------ the bound

def logC(p):
    """log C_p, C_p = p^p/(p-1)^(p-1) * J_p/2, J_p = int sech^p = sqrt(pi) Gamma(p/2)/Gamma((p+1)/2)."""
    from scipy.special import gammaln
    return p * np.log(p) - (p - 1) * np.log(p - 1) + 0.5 * np.log(np.pi) + gammaln(p / 2) - gammaln((p + 1) / 2) - np.log(2)
