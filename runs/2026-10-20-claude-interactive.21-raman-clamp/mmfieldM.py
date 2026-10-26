"""M-mode stationary random-field GNLSE (generalization of runs/...-raman-parity/mmfield.py) for a parabolic
fibre truncated to groups g = 0..G-1 in the Hermite-Gauss basis (claude-interactive.21, 2026-10-20).

Same equation, conventions and time-reversal structure as mmfield.py:
  dB_p/dz = i D_p(W) B_p + i [C(z) B]_p + i gamma w(W) ifft( sum_qrs S_pqrs A_q [(1-fR) A_r A_s^* + fR h_lam(*)(A_r A_s^*)] )
with D_p = -g_p dbeta + beta2 W^2/2, w = 1 + s W/omega0, h_lam = h_even + lam h_odd, and white-noise Hermitian
coupling C(z) inside each degenerate group (all su(n) generators of the group block, strength Dd).
"""
import itertools
import math

import numpy as np
import scipy.fft as sfft
from numpy.polynomial.hermite import hermgauss
from scipy.special import eval_hermite, factorial
from scipy.linalg import expm

WORKERS = 2


def hg_modes(G):
    return [(m, g - m) for g in range(G) for m in range(g + 1)]


def hg_overlap_tensor(G):
    """S_pqrs / S_0000 for Hermite-Gauss modes of groups 0..G-1 (real, fully symmetric)."""
    x, w = hermgauss(60)
    xs, ws = x / math.sqrt(2), w / math.sqrt(2)          # weight e^{-2x^2} for products of four Hermite functions
    def h(m, xx):
        return eval_hermite(m, xx) / math.sqrt(2.0 ** m * factorial(m) * math.sqrt(math.pi))
    nmax = G
    H = np.array([h(m, xs) for m in range(nmax)])
    I4 = np.einsum("ax,bx,cx,dx,x->abcd", H, H, H, H, ws)
    modes = hg_modes(G)
    M = len(modes)
    S = np.zeros((M, M, M, M))
    for p, q, r, s in itertools.product(range(M), repeat=4):
        S[p, q, r, s] = I4[modes[p][0], modes[q][0], modes[r][0], modes[s][0]] * \
                        I4[modes[p][1], modes[q][1], modes[r][1], modes[s][1]]
    S[np.abs(S) < 1e-12] = 0.0
    return S / S[0, 0, 0, 0], modes


def su_generators(n):
    """Hermitian traceless generators of su(n) (generalized Gell-Mann), normalized Tr(T_a T_b) = 2 delta_ab."""
    gens = []
    for j in range(n):
        for k in range(j + 1, n):
            a = np.zeros((n, n), complex); a[j, k] = a[k, j] = 1; gens.append(a)
            b = np.zeros((n, n), complex); b[j, k] = -1j; b[k, j] = 1j; gens.append(b)
    for l in range(1, n):
        d = np.zeros((n, n), complex)
        for j in range(l):
            d[j, j] = 1
        d[l, l] = -l
        gens.append(d * math.sqrt(2.0 / (l * (l + 1))))
    return gens


def raman_response(t, tau1, tau2):
    h = ((tau1 ** 2 + tau2 ** 2) / (tau1 * tau2 ** 2)) * np.exp(-t / tau2) * np.sin(t / tau1)
    h[t < 0] = 0.0
    return h


class ModelM:
    def __init__(self, G, N, dt, gamma, fR, tau1, tau2, omega0, dbeta, beta2, s, lam, Dd):
        self.S, self.modes = hg_overlap_tensor(G)
        self.M = len(self.modes)
        self.grp = np.array([m + n for m, n in self.modes])
        self.N, self.dt = N, dt
        self.W = 2 * np.pi * sfft.fftfreq(N, dt)
        self.nyq = N // 2
        self.gamma, self.fR, self.s, self.lam, self.Dd = gamma, fR, s, lam, Dd
        t = np.arange(N) * dt
        h = raman_response(t, tau1, tau2)
        h /= h.sum() * dt
        Hk = N * dt * sfft.ifft(h)
        Hk[self.nyq] = Hk[self.nyq].real
        self.H = Hk.real + 1j * lam * Hk.imag
        self.w = 1.0 + s * self.W / omega0
        self.w[self.nyq] = 1.0
        D = -self.grp[:, None] * dbeta + 0.5 * beta2 * self.W[None, :] ** 2
        D[:, self.nyq] = 0.0
        self.D = D
        # pair list (r <= s) and term list grouped by (p, pair) with sign of conjugation
        self.pairs = [(r, q) for r in range(self.M) for q in range(r, self.M)]
        self.pidx = {pr: i for i, pr in enumerate(self.pairs)}
        terms = []
        for p, q, r, s_ in itertools.product(range(self.M), repeat=4):
            v = self.S[p, q, r, s_]
            if v != 0:
                terms.append((p, q, r, s_, v))
        self.terms = terms
        # dense contraction tensor T[p*M+q, r*M+s] = S_pqrs for the vectorized RHS
        M_ = self.M
        self.T = self.S.reshape(M_ * M_, M_ * M_).astype(complex)
        # map ordered pair (r, s) -> (index in self.pairs, conjugate?)
        self.full_idx = np.array([self.pidx[(min(r, q), max(r, q))] for r in range(M_) for q in range(M_)])
        self.full_conj = np.array([r > q for r in range(M_) for q in range(M_)])
        # disorder blocks: each group with more than one mode
        self.blocks = []
        for g in range(G):
            idx = np.where(self.grp == g)[0]
            if len(idx) > 1:
                self.blocks.append((idx, su_generators(len(idx))))
        self.ngen = sum(len(gens) for _, gens in self.blocks)

    def rhs(self, B):
        A = sfft.fft(B, axis=-1, workers=WORKERS)
        prod = np.stack([A[:, r] * np.conj(A[:, q]) for (r, q) in self.pairs], axis=1)
        conv = sfft.fft(self.H * sfft.ifft(prod, axis=-1, workers=WORKERS), axis=-1, workers=WORKERS)
        mix = (1 - self.fR) * prod + self.fR * conv
        MIXF = mix[:, self.full_idx]                          # (R, M*M, N) ordered pairs (r, s)
        MIXF[:, self.full_conj] = np.conj(MIXF[:, self.full_conj])
        R_, M_, N_ = A.shape
        Z = np.einsum("ak,rkn->ran", self.T, MIXF, optimize=True).reshape(R_, M_, M_, N_)   # sum over (r,s)
        NL = np.einsum("rqn,rpqn->rpn", A, Z, optimize=True)
        out = 1j * self.gamma * self.w * sfft.ifft(NL, axis=-1, workers=WORKERS)
        out[..., self.nyq] = 0.0
        return out

    def disorder(self, B, g, dz):
        k = 0
        for idx, gens in self.blocks:
            Hm = sum(gi * Ti for gi, Ti in zip(g[k:k + len(gens)], gens))
            k += len(gens)
            U = expm(1j * math.sqrt(self.Dd * dz) * Hm)
            sub = B[:, idx]
            B[:, idx] = np.einsum("ij,rjn->rin", U, sub)
        return B

    def step(self, B, dz, g):
        E = np.exp(0.5j * self.D * dz)
        B = B * E
        if self.Dd > 0:
            B = self.disorder(B, g, dz)
        k1 = self.rhs(B)
        k2 = self.rhs(B + 0.5 * dz * k1)
        k3 = self.rhs(B + 0.5 * dz * k2)
        k4 = self.rhs(B + dz * k3)
        B = B + dz / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        B = B * E
        B[..., self.nyq] = 0.0
        return B

    def photon(self, B):
        return np.sum(np.abs(B) ** 2 / self.w, axis=-1)


def mirror(B):
    return np.roll(B[..., ::-1], 1, axis=-1)


def launch(rng, R, model, powers, sig):
    N, W = model.N, model.W
    B = np.zeros((R, model.M, N), complex)
    for p in range(model.M):
        gsp = np.exp(-W ** 2 / (2 * sig ** 2))
        gsp[N // 2] = 0.0
        gsp = powers[p] * gsp / gsp.sum()
        B[:, p] = np.sqrt(gsp / 2) * (rng.standard_normal((R, N)) + 1j * rng.standard_normal((R, N)))
    return B
