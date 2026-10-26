"""Discrete adjoint of the Strang split-step map for the spectral photon-count covariance (claude-b,
T-20261010-claude-interactive-05, continuation).

Same model, grid and step rule as nd_cov.py of run 2026-10-10-claude-b-nd-oracle (normal dispersion, Kerr only):
    step: u1 = ifft(L fft(u)),  u2 = u1 exp(i N^2 |u1|^2 dxi),  u3 = ifft(L fft(u2)),   L = exp(i w^2 dxi / 4)
    output alpha = fft(u) sqrt(dt/Nt);   input quadratures q = (x, y), du0 = (x + i y)/sqrt(dt).
For each kept bin k, the gradient g_k = d n_k / d q (n_k = |alpha_k|^2) is obtained exactly (to rounding) by propagating the
cotangent lambda = 2 alpha_k e_k backwards through the transposed linearized steps (real inner product Re sum conj(a) b):
    linear half step:   lambda <- ifft(conj(L) fft(lambda))
    nonlinear step:     lambda1 = exp(-i phi) lambda2 - 2 c Im(conj(lambda2) exp(i phi) u1) u1,   phi = c |u1|^2, c = N^2 dxi
    output map:         lambda_u = Nt ifft(lambda_alpha) sqrt(dt/Nt);   input:  g = (Re lambda0, Im lambda0)/sqrt(dt)
Count covariance C = (1/4) G G^T over the kept bins (bins holding 1 - 1e-9 of the photons, frequency order), as in nd_cov.
Batched over bins; memory: the forward states u1 at every step are stored.
"""
import numpy as np

fft, ifft = np.fft.fft, np.fft.ifft


def grid(Nt, TW):
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = t[1] - t[0]
    w = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    return t, dt, w


def xi_wb(N):
    return 1.0 / np.sqrt(4 * N ** 2 * np.exp(-1.5) - 1)


def forward(u0, w, xi, N, phi_step=0.02):
    N2 = N * N
    dxi = phi_step / N2
    n = max(1, int(round(xi / dxi)))
    dxi = xi / n
    L = np.exp((0.5j * w ** 2) * dxi / 2)
    u = u0.copy()
    U1 = np.empty((n, len(u0)), complex)
    for s in range(n):
        u1 = ifft(L * fft(u))
        U1[s] = u1
        u = ifft(L * fft(u1 * np.exp(1j * N2 * np.abs(u1) ** 2 * dxi)))
    return u, U1, dxi, L


def count_gradients(alpha_bins, bins, U1, dxi, L, N, Nt, dt, batch=256):
    """Rows g_k (len(bins) x 2Nt) for n_k = |alpha_k|^2, bins = fft indices."""
    c = N * N * dxi
    G = np.empty((len(bins), 2 * Nt))
    cL = np.conj(L)
    for b0 in range(0, len(bins), batch):
        bb = bins[b0:b0 + batch]
        lam_a = np.zeros((len(bb), Nt), complex)
        lam_a[np.arange(len(bb)), bb] = 2 * alpha_bins[b0:b0 + batch]
        lam = Nt * ifft(lam_a, axis=-1) * np.sqrt(dt / Nt)
        for s in range(U1.shape[0] - 1, -1, -1):
            lam = ifft(cL * fft(lam, axis=-1), axis=-1)                 # adjoint of the second linear half step
            u1 = U1[s]
            e = np.exp(1j * c * np.abs(u1) ** 2)
            lam = np.conj(e) * lam - 2 * c * np.imag(np.conj(lam) * e * u1) * u1   # adjoint of the nonlinear step
            lam = ifft(cL * fft(lam, axis=-1), axis=-1)                 # adjoint of the first linear half step
        G[b0:b0 + batch, :Nt] = lam.real / np.sqrt(dt)
        G[b0:b0 + batch, Nt:] = lam.imag / np.sqrt(dt)
    return G


def count_covariance(N, zr, Nt, TW, phi_step=0.02, keep_frac=1 - 1e-9, batch=256):
    t, dt, w = grid(Nt, TW)
    u0 = np.exp(-t ** 2 / 2) + 0j
    xi = zr * xi_wb(N)
    u, U1, dxi, L = forward(u0, w, xi, N, phi_step)
    alpha = fft(u) * np.sqrt(dt / Nt)
    nall = np.abs(alpha) ** 2
    order = np.argsort(w)
    srt = np.sort(nall)[::-1]
    thr = srt[np.searchsorted(np.cumsum(srt) / srt.sum(), keep_frac)]
    keep = np.array([i for i in order if nall[i] >= thr])
    G = count_gradients(alpha[keep], keep, U1, dxi, L, N, Nt, dt, batch)
    C = 0.25 * G @ G.T
    return dict(C=C, nbar=nall[keep], keep=keep, w=w, alpha=alpha, xi=xi, nsteps=U1.shape[0], dxi=dxi)
