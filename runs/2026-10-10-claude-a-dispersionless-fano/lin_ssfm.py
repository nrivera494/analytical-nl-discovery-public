"""Independent linearized split-step propagator (Kerr + beta2, scalar), for checking the dispersionless theory and
locating its breakdown in Phi^2 L/L_D. Units: T0 = 1, L = 1; gamma P0 L = Phi; beta2 = +/- delta (= L/L_D signed).
The perturbation propagates as a real-linear map; columns are unit input quadratures (X_j = 1 or Y_j = 1, with
delta A = (X + iY)/2 per time bin); outputs are lab-frame quadratures X = 2 Re dA, Y = 2 Im dA. V = S S^T.
"""
import numpy as np
from numpy.fft import fft, ifft, fftfreq


def propagate(p, dt, Phi, beta2, nz=400):
    n = len(p)
    w = 2 * np.pi * fftfreq(n, dt)
    dz = 1.0 / nz
    lin_half = np.exp(-1j * 0.5 * beta2 * (-(w**2)) * dz / 2)   # d_z A = -(i/2) beta2 d_t^2 A -> exp(+(i/2) beta2 w^2 dz)
    lin_half = np.exp(1j * 0.5 * beta2 * w**2 * dz / 2)
    A = np.sqrt(p).astype(complex)
    P = np.zeros((n, 2 * n), complex)
    P[np.arange(n), np.arange(n)] = 0.5          # X_j = 1  -> dA = 1/2
    P[np.arange(n), n + np.arange(n)] = 0.5j     # Y_j = 1  -> dA = i/2
    g = Phi                                        # gamma P0 (L = 1), |A|^2 in units of P0
    for _ in range(nz):
        A = ifft(lin_half * fft(A))
        P = ifft(lin_half[:, None] * fft(P, axis=0), axis=0)
        I = np.abs(A) ** 2
        th = np.angle(A)
        b = np.exp(-1j * th)[:, None] * P
        b = b + 2j * g * (I * dz)[:, None] * b.real
        A = A * np.exp(1j * g * I * dz)
        P = np.exp(1j * (th + g * I * dz))[:, None] * b
        A = ifft(lin_half * fft(A))
        P = ifft(lin_half[:, None] * fft(P, axis=0), axis=0)
    S = np.vstack([2 * P.real, 2 * P.imag])          # (2n x 2n): rows X_out, Y_out (lab frame)
    return A, S


def spectral_from_S(A, S, dt, pad=1, thr=1e-6):
    """Unitary-DFT bins (zero-padded window) of the output; amplitude-quadrature covariance V^amp = B S S^T B^T
    (+ vacuum of the padded region)."""
    n = len(A)
    ntot = pad * n
    t = (np.arange(ntot) - ntot // 2) * dt
    i0 = ntot // 2 - n // 2
    w = 2 * np.pi * fftfreq(ntot, dt)
    Fm = np.exp(1j * np.outer(w, t)) / np.sqrt(ntot)
    Afull = np.zeros(ntot, complex)
    Afull[i0:i0 + n] = A
    Ab = Fm @ Afull
    nb = np.abs(Ab) ** 2
    keep = nb >= thr * nb.max()
    psi = np.angle(Ab[keep])
    G = np.exp(-1j * psi)[:, None] * Fm[keep][:, i0:i0 + n]      # dA_out -> bin amplitude quadrature = 2 Re(G dA)
    # dA_out = (X_out + i Y_out)/2  ->  2 Re(G dA) = Re(G) X - Im(G) Y
    B = np.hstack([G.real, -G.imag])
    M = B @ S
    Vamp = M @ M.T
    mask = np.ones(ntot, bool)
    mask[i0:i0 + n] = False
    if mask.any():
        Go = (np.exp(-1j * psi)[:, None] * Fm[keep])[:, mask]
        Vamp += (Go @ Go.conj().T).real
    return nb[keep], Vamp, w[keep]


def propagate_ss(p, dt, Phi, s, nz=800, beta2=0.0):
    """Kerr + self-steepening (+ optional beta2), linearized by propagating the tangent map with RK4.
    dA/dz = -(i/2) beta2 A_tt + i Phi (1 + i s d_t)(|A|^2 A); s = 1/(omega0 T0) in T0 units; L = 1."""
    n = len(p)
    w = 2 * np.pi * fftfreq(n, dt)
    dz = 1.0 / nz
    dt_op = lambda f: ifft(-1j * w[:, None] * fft(f, axis=0), axis=0) if f.ndim == 2 else ifft(-1j * w * fft(f))
    # note: with numpy's fft convention, d/dt <-> multiplication by +i w? f(t) = sum F e^{+i w t}/n -> d/dt = i w
    def ddt(f):
        if f.ndim == 2:
            return ifft(1j * w[:, None] * fft(f, axis=0), axis=0)
        return ifft(1j * w * fft(f))
    lin = np.exp(1j * 0.5 * beta2 * w**2 * dz)
    def NA(A):
        q = np.abs(A) ** 2 * A
        return 1j * Phi * q - Phi * s * ddt(q)
    def NP(A, P):
        q = 2 * (np.abs(A) ** 2)[:, None] * P + (A**2)[:, None] * P.conj()
        return 1j * Phi * q - Phi * s * ddt(q)
    A = np.sqrt(p).astype(complex)
    P = np.zeros((n, 2 * n), complex)
    P[np.arange(n), np.arange(n)] = 0.5
    P[np.arange(n), n + np.arange(n)] = 0.5j
    for _ in range(nz):
        if beta2 != 0:
            A = ifft(np.sqrt(lin) * fft(A)); P = ifft(np.sqrt(lin)[:, None] * fft(P, axis=0), axis=0)
        k1a = NA(A); k1p = NP(A, P)
        A2 = A + 0.5 * dz * k1a; P2 = P + 0.5 * dz * k1p
        k2a = NA(A2); k2p = NP(A2, P2)
        A3 = A + 0.5 * dz * k2a; P3 = P + 0.5 * dz * k2p
        k3a = NA(A3); k3p = NP(A3, P3)
        A4 = A + dz * k3a; P4 = P + dz * k3p
        k4a = NA(A4); k4p = NP(A4, P4)
        A = A + dz / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
        P = P + dz / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
        if beta2 != 0:
            A = ifft(np.sqrt(lin) * fft(A)); P = ifft(np.sqrt(lin)[:, None] * fft(P, axis=0), axis=0)
    S = np.vstack([2 * P.real, 2 * P.imag])
    return A, S


def propagate_cols(p, dt, Phi, beta2, nz, cols):
    """As propagate(), but only for the input quadratures of the time slices in `cols` (X_j then Y_j, j in cols).
    min over this input subspace of |S u|^2 is an upper bound on lambda_min(V) that is tight when the optimal input
    mode is supported inside `cols` (true near the pulse peak for small dispersion)."""
    n = len(p)
    w = 2 * np.pi * fftfreq(n, dt)
    dz = 1.0 / nz
    lin_half = np.exp(1j * 0.5 * beta2 * w**2 * dz / 2)
    A = np.sqrt(p).astype(complex)
    m = len(cols)
    P = np.zeros((n, 2 * m), complex)
    P[cols, np.arange(m)] = 0.5
    P[cols, m + np.arange(m)] = 0.5j
    g = Phi
    for _ in range(nz):
        A = ifft(lin_half * fft(A))
        P = ifft(lin_half[:, None] * fft(P, axis=0), axis=0)
        I = np.abs(A) ** 2
        th = np.angle(A)
        b = np.exp(-1j * th)[:, None] * P
        b = b + 2j * g * (I * dz)[:, None] * b.real
        A = A * np.exp(1j * g * I * dz)
        P = np.exp(1j * (th + g * I * dz))[:, None] * b
        A = ifft(lin_half * fft(A))
        P = ifft(lin_half[:, None] * fft(P, axis=0), axis=0)
    S = np.vstack([2 * P.real, 2 * P.imag])
    return A, S
