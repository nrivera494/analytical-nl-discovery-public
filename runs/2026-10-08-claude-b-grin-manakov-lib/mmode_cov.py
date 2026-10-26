"""M-mode generalization of twomode_cov.py (claude-b, T-20261008-claude-b-01).

    i a_m,z + i d_m a_m,t + 1/2 a_m,tt + (sum_n C_mn |a_n|^2) a_m = 0,   m = 0..M-1
Same Strang split step and the same central-difference Jacobian of the spectral-bin counts as twomode_cov.py; for M = 2
it performs the same floating-point operations mode by mode (checked in validate_mmode.py). Returns nbar (M, N) and the
per-bin covariance (M N, M N); the all-mode common-filter totals are summed over mode pairs.
"""
import numpy as np
import twomode_cov as tc

fft, ifft = np.fft.fft, np.fft.ifft


def propagate(g, A, z, dz, C, d):
    """A: (..., M, N) complex. C: (M, M). d: (M,)."""
    C = np.asarray(C, float)
    d = np.asarray(d, float)
    L = np.exp((-0.5j * g.w[None, :] ** 2 - 1j * d[:, None] * g.w[None, :]) * dz / 2)    # (M, N)
    n = int(round(z / dz))
    for _ in range(n):
        A = ifft(L * fft(A, axis=-1), axis=-1)
        I = np.abs(A) ** 2                                   # (..., M, N)
        phase = np.einsum("mn,...nt->...mt", C, I)
        A = A * np.exp(1j * phase * dz)
        A = ifft(L * fft(A, axis=-1), axis=-1)
    return A


def bin_covariance(g, A0, z, dz, C, d, eps=1e-6):
    M, N = A0.shape
    D = 2 * M * N
    dirs = np.zeros((D, M, N), complex)
    r = 0
    for m in range(M):
        for q in (1.0, 1j):
            dirs[r:r + N, m, :] = np.eye(N) * (q * eps / np.sqrt(g.dt))
            r += N
    batch = np.concatenate([A0[None] + dirs, A0[None] - dirs])
    out = propagate(g, batch, z, dz, C, d)
    counts = np.abs(fft(out, axis=-1) * np.sqrt(g.dt / g.N)) ** 2          # (2D, M, N)
    G = ((counts[:D] - counts[D:]) / (2 * eps)).reshape(D, M * N).T       # (M N, D)
    mean = propagate(g, A0[None], z, dz, C, d)
    nbar = (np.abs(fft(mean[0], axis=-1) * np.sqrt(g.dt / g.N)) ** 2)
    return nbar, 0.25 * G @ G.T


def totals(nbar, Cov):
    M, N = nbar.shape
    Ct = Cov.reshape(M, N, M, N).sum(axis=(0, 2))
    return Ct, nbar.sum(axis=0)


def launch(g, p, C):
    p = np.asarray(p, float)
    S = p @ np.asarray(C, float) @ p
    s = 1 / np.cosh(g.t)
    return (np.sqrt(p / S)[:, None] * s[None, :]).astype(complex), S


def q2(p, C):
    p = np.asarray(p, float)
    c = np.sqrt(p)
    D = np.asarray(C, float) - 1.0
    v = c * (D @ p)
    v = v - c * (c @ v)
    return float(v @ v)
