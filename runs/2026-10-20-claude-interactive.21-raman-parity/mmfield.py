"""Three-mode stationary random-field GNLSE with Kerr, Raman, shock, walk-off and intra-group
random coupling (claude-interactive.21, 2026-10-20, exploration for P-20261020-gpt-f-01).

Standalone numpy/scipy code, not the repository solver. Scalar real modes of a parabolic fibre in
the Hermite-Gauss basis: 0 = HG00 (LP01), 1 = HG10, 2 = HG01 (the degenerate LP11 pair).
Spectral representation B_p[k] = ifft(A_p)[k], A_p(t_j) = sum_k B_p[k] exp(-i W_k t_j),
W_k = 2 pi fftfreq(N, dt).  Model (z in m, t in ps, power in W):

  dB_p/dz = i D_p(W) B_p + i [C(z) B]_p
            + i gamma w(W) ifft( sum_qrs S_pqrs A_q [(1-fR) A_r A_s^* + fR h_lam (*) (A_r A_s^*)] )

  D_0 = 0, D_1 = D_2 = -dbeta + b1 W + 0 ; all modes add beta2 W^2/2
  w(W) = 1 + s W / omega0                 (s = 0 or 1: shock off/on)
  h_lam = h_even + lam h_odd              (lam = 1: physical Raman; lam = -1: mirrored response)
  C(z): white-noise Hermitian coupling inside the {1,2} block (Pauli matrices), strength Dd.

The time-reversal map R: A(t) -> A(-t), i.e. B[k] -> B[-k], sends the model (lam, s, b1) to
(-lam, -s, -b1).  The Nyquist bin is held at zero so that R is exact on the grid.
"""
import numpy as np
import scipy.fft as sfft

WORKERS = 2


def hg_overlaps():
    """Fully symmetric overlap tensor S_pqrs / S_0000 for HG00, HG10, HG01 (exact values)."""
    S = np.zeros((3, 3, 3, 3))
    def put(idx, v):
        import itertools
        for perm in set(itertools.permutations(idx)):
            S[perm] = v
    put((0, 0, 0, 0), 1.0)
    put((0, 0, 1, 1), 0.5)
    put((0, 0, 2, 2), 0.5)
    put((1, 1, 1, 1), 0.75)
    put((2, 2, 2, 2), 0.75)
    put((1, 1, 2, 2), 0.25)
    return S


def raman_response(t, tau1, tau2):
    h = ((tau1 ** 2 + tau2 ** 2) / (tau1 * tau2 ** 2)) * np.exp(-t / tau2) * np.sin(t / tau1)
    h[t < 0] = 0.0
    return h


class Model:
    def __init__(self, N, dt, gamma, fR, tau1, tau2, omega0, dbeta, beta2, b1, s, lam, Dd):
        self.N, self.dt = N, dt
        self.W = 2 * np.pi * sfft.fftfreq(N, dt)
        self.nyq = N // 2
        self.gamma, self.fR, self.s, self.lam = gamma, fR, s, lam
        t = np.arange(N) * dt
        h = raman_response(t, tau1, tau2)
        h /= h.sum() * dt                      # sampled response normalized: H(0) = 1 exactly
        H = N * dt * sfft.ifft(h)              # H_k = dt sum_j h_j exp(i W_k t_j)  ~ h~(W_k)
        H[self.nyq] = H[self.nyq].real
        self.H = H.real + 1j * lam * H.imag    # even part + lam * odd part
        self.w = 1.0 + s * self.W / omega0
        self.w[self.nyq] = 1.0
        D = np.zeros((3, N))
        D[1] = -dbeta + b1 * self.W
        D[2] = -dbeta + b1 * self.W
        D += 0.5 * beta2 * self.W ** 2
        D[:, self.nyq] = 0.0
        self.D = D
        self.S = hg_overlaps()
        self.Dd = Dd
        # nonzero (p,q,r,s) entries
        self.terms = [(p, q, r, ss, self.S[p, q, r, ss]) for p in range(3) for q in range(3)
                      for r in range(3) for ss in range(3) if self.S[p, q, r, ss] != 0]

    def rhs(self, B):
        """Nonlinear part dB/dz for B of shape (R, 3, N)."""
        A = sfft.fft(B, axis=-1, workers=WORKERS)
        R = B.shape[0]
        prod = {}
        conv = {}
        for r in range(3):
            for ss in range(3):
                if r <= ss:
                    prod[(r, ss)] = A[:, r] * np.conj(A[:, ss])
        # Raman convolution of each product; (s,r) is the complex conjugate of (r,s) since h is real
        allp = np.stack([prod[k] for k in sorted(prod)], axis=1)
        allc = sfft.fft(self.H * sfft.ifft(allp, axis=-1, workers=WORKERS), axis=-1, workers=WORKERS)
        for i, k in enumerate(sorted(prod)):
            conv[k] = allc[:, i]
        NL = np.zeros_like(A)
        fR = self.fR
        for (p, q, r, ss, v) in self.terms:
            if r <= ss:
                pr, cv = prod[(r, ss)], conv[(r, ss)]
            else:
                pr, cv = np.conj(prod[(ss, r)]), np.conj(conv[(ss, r)])
            NL[:, p] += v * A[:, q] * ((1 - fR) * pr + fR * cv)
        out = 1j * self.gamma * self.w * sfft.ifft(NL, axis=-1, workers=WORKERS)
        out[..., self.nyq] = 0.0
        return out

    def disorder_unitary(self, g, dz):
        """exp(i sqrt(Dd dz) g.sigma) on the {1,2} block; g has shape (3,)."""
        a = np.sqrt(self.Dd * dz) * np.asarray(g)
        th = np.linalg.norm(a)
        if th == 0:
            return np.eye(2, dtype=complex)
        n = a / th
        sx = np.array([[0, 1], [1, 0]], complex)
        sy = np.array([[0, -1j], [1j, 0]], complex)
        sz = np.array([[1, 0], [0, -1]], complex)
        Hm = n[0] * sx + n[1] * sy + n[2] * sz
        return np.cos(th) * np.eye(2) + 1j * np.sin(th) * Hm

    def step(self, B, dz, g):
        """Strang step: L(dz/2) . [disorder] . RK4 nonlinear(dz) . L(dz/2)."""
        E = np.exp(0.5j * self.D * dz)
        B = B * E
        if self.Dd > 0:
            U = self.disorder_unitary(g, dz)
            b1, b2 = B[:, 1].copy(), B[:, 2].copy()
            B[:, 1] = U[0, 0] * b1 + U[0, 1] * b2
            B[:, 2] = U[1, 0] * b1 + U[1, 1] * b2
        k1 = self.rhs(B)
        k2 = self.rhs(B + 0.5 * dz * k1)
        k3 = self.rhs(B + 0.5 * dz * k2)
        k4 = self.rhs(B + dz * k3)
        B = B + dz / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        B = B * E
        B[..., self.nyq] = 0.0
        return B

    def photon(self, B):
        """Photon-number-like modal invariant sum_k |B|^2 / w (shape (R, 3))."""
        return np.sum(np.abs(B) ** 2 / self.w, axis=-1)

    def power(self, B):
        return np.sum(np.abs(B) ** 2, axis=-1)


def mirror(B):
    """R: B[k] -> B[-k mod N]."""
    return np.roll(B[..., ::-1], 1, axis=-1)


def launch(rng, R, N, dt, powers, sig, cen, photon_symmetric=False, omega0=None):
    """Stationary complex-Gaussian fields with Gaussian spectral densities.
    Energy spectra b_p(W) ~ exp(-(W-c_p)^2/(2 sig_p^2)), or photon spectra symmetric
    (b_p = w * Gaussian) when photon_symmetric (shock-RJ-like tilt)."""
    W = 2 * np.pi * sfft.fftfreq(N, dt)
    B = np.zeros((R, 3, N), complex)
    dens = np.zeros((3, N))
    for p in range(3):
        g = np.exp(-(W - cen[p]) ** 2 / (2 * sig[p] ** 2))
        if photon_symmetric:
            g = g * (1 + W / omega0)
        g[N // 2] = 0.0
        g = powers[p] * g / g.sum()
        dens[p] = g
        B[:, p] = np.sqrt(g / 2) * (rng.standard_normal((R, N)) + 1j * rng.standard_normal((R, N)))
    return B, dens


def first_order_slope(model, dens):
    """Closed-form first-order Raman modal photon transfer for Gaussian stationary fields:
    dN~_p/dz = -2 gamma fR sum_q S_pqpq sum_{l,k} b_p[l] b_q[k] Im H(W_l - W_k)  (lam = 1 odd part).
    Returns the lam-odd slope (per unit lam)."""
    N = model.N
    Hodd = model.H.imag / model.lam if model.lam != 0 else None
    out = np.zeros(3)
    for p in range(3):
        for q in range(3):
            Spq = model.S[p, q, p, q]
            if Spq == 0:
                continue
            # sum_{l,k} b_p[l] b_q[k] ImH[l-k]  = sum_l b_p[l] (ImH (*) b_q)[l]  (circular)
            cconv = np.real(sfft.ifft(sfft.fft(Hodd) * sfft.fft(dens[q])))
            out[p] += -2 * model.gamma * model.fR * Spq * np.sum(dens[p] * cconv)
    return out
