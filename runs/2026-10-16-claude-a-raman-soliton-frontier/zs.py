"""Zakharov-Shabat (focusing) eigenvalues by Fourier collocation, with analytic eigenvalue gradients for spectral masks.

ZS: psi1' = -i zeta psi1 + q psi2, psi2' = i zeta psi2 - conj(q) psi1. As an eigenproblem zeta v = M v with
M = [[i d/dt, -i q], [-i conj(q), -i d/dt]] on a periodic grid (spectral differentiation). A bound state zeta = xi + i eta
(eta > 0) carries a soliton of energy 4 eta in NLSE units (i u_xi + u_tt/2 + |u|^2 u = 0).
"""
import numpy as np
from numpy.fft import fft, ifft, fftfreq
import scipy.linalg as sla
import scipy.sparse.linalg as spla


class Grid:
    def __init__(self, n, width):
        self.n = n
        self.dt = width / n
        self.t = (np.arange(n) - n // 2) * self.dt
        self.k = 2 * np.pi * fftfreq(n, self.dt)
        F = np.fft.fft(np.eye(n), axis=0)
        self.D = np.fft.ifft(1j * self.k[:, None] * F, axis=0)      # spectral derivative matrix

    def M(self, q):
        n = self.n
        Z = np.zeros((2 * n, 2 * n), complex)
        Z[:n, :n] = 1j * self.D
        Z[n:, n:] = -1j * self.D
        Z[np.arange(n), n + np.arange(n)] = -1j * q
        Z[n + np.arange(n), np.arange(n)] = -1j * np.conj(q)
        return Z


def all_eigs(grid, q, eta_min=1e-3):
    """All eigenvalues with Im > eta_min (dense), sorted by Im descending."""
    ev = sla.eigvals(grid.M(q))
    ev = ev[ev.imag > eta_min]
    return ev[np.argsort(-ev.imag)]


def bound_states(q, width, n, eta_min=0.02, tol=2e-3):
    """Eigenvalues confirmed on two grids (n and 3n/2): returns list sorted by Im descending."""
    g1, g2 = Grid(n, width), Grid(int(1.5 * n) // 2 * 2, width)
    t1 = g1.t
    q1 = q(t1) if callable(q) else q
    e1 = all_eigs(g1, q1, eta_min)
    e2 = all_eigs(g2, q(g2.t) if callable(q) else np.interp(g2.t, t1, q1.real) + 1j * np.interp(g2.t, t1, q1.imag), eta_min)
    out = [z for z in e1 if len(e2) and np.min(np.abs(e2 - z)) < tol]
    return np.array(out)


def leading(grid, q, sigma, k=3):
    """Eigenvalues nearest sigma (shift-invert); returns (zeta, right vec, left vec) for the one with largest Im."""
    M = grid.M(q)
    vals, vecs = spla.eigs(M, k=k, sigma=sigma, which="LM")
    j = int(np.argmax(vals.imag))
    z, v = vals[j], vecs[:, j]
    lv, lw = spla.eigs(M.conj().T, k=k, sigma=np.conj(z), which="LM")
    jj = int(np.argmin(np.abs(np.conj(lv) - z)))
    w = lw[:, jj]
    return z, v, w


def grad_zeta_q(grid, z, v, w):
    """dzeta = sum_j alpha_j dq_j + beta_j conj(dq_j)."""
    n = grid.n
    norm = np.vdot(w, v)                       # w^H v
    alpha = -1j * np.conj(w[:n]) * v[n:] / norm
    beta = -1j * np.conj(w[n:]) * v[:n] / norm
    return alpha, beta


def grad_wrt_spectrum(grid, alpha, beta, mQ):
    """For q = ifft(S), S = m Q: dzeta = sum_k [ dS_k * ifft(alpha)_k + conj(dS_k) * fft(beta)_k / n ]."""
    return np.fft.ifft(alpha), np.fft.fft(beta) / grid.n


def eta_wkb(absq, dt, tol=1e-12):
    """Solve int (|q|^2 - eta^2)_+^(1/2) dt = pi/2 for eta (0 if int|q| < pi/2)."""
    if np.sum(absq) * dt < np.pi / 2:
        return 0.0
    lo, hi = 0.0, float(absq.max())
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        val = np.sum(np.sqrt(np.maximum(absq**2 - mid**2, 0))) * dt
        if val > np.pi / 2:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def leading_fast(grid, q, sigma, k=3, iters=14, rng=np.random.default_rng(0)):
    """Leading (max-Im) eigenvalue among the k nearest to sigma, with right/left eigenvectors.
    Subspace inverse iteration + Rayleigh-Ritz, then shifted inverse iteration (right and left) at the Ritz value."""
    M = grid.M(q)
    n2 = M.shape[0]
    I = np.eye(n2)
    lu = sla.lu_factor(M - sigma * I)
    Q = rng.normal(size=(n2, k)) + 1j * rng.normal(size=(n2, k))
    for _ in range(iters):
        Q = sla.lu_solve(lu, Q)
        Q, _ = np.linalg.qr(Q)
    H = Q.conj().T @ M @ Q
    vals, Y = np.linalg.eig(H)
    j = int(np.argmax(vals.imag))
    z0 = vals[j]
    lu2 = sla.lu_factor(M - (z0 + 1e-7 * (1 + abs(z0))) * I)
    v = Q @ Y[:, j]
    w = v.conj().copy()
    for _ in range(3):
        v = sla.lu_solve(lu2, v); v /= np.linalg.norm(v)
        w = sla.lu_solve(lu2, w, trans=2); w /= np.linalg.norm(w)
    z = np.vdot(w, M @ v) / np.vdot(w, v)
    return z, v, w
