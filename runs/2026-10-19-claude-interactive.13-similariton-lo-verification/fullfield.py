"""Full-field linearized (Bogoliubov) matched-LO covariance of the gain NLSE with a complete
ASE reservoir, by an exact discrete adjoint.  Written by claude-interactive.13 for the
verification of C-20261019-pi-chatgpt-02, part (ii) (and cross-checks of (i)/(iii) at moderate gain).

Normalized model (x = T/T0, zeta = z/sqrt(LD LNL), eps0 = sqrt(LNL/LD), Gamma = g sqrt(LD LNL)):
    d psi/d zeta = -(i eps0/2) psi_xx + (i/eps0)|psi|^2 psi + (Gamma/2) psi        (gamma P0/g = 1/(eps0 Gamma))
Fluctuations b_j (one discrete mode per grid point, [b_j, b_k^+] = delta_jk), both quadratures.
Strang step:  D(h/2) . A(h/2) . K(h) . A(h/2) . D(h/2), with
    D: exact dispersion in Fourier space (unitary)
    K: exact Kerr phase of the background, tangent T b = e^{i phi}[b + 2i(h/eps0) Re(psi^* b) psi] (symplectic)
    A: linear amplifier substep of power gain Gh = e^{Gamma h/2}: b -> sqrt(Gh) b + nu, with
       Var(2<w,nu>) = (2 n_sp - 1)(Gh - 1)|w|^2 and [nu, nu^+] = -(Gh - 1)  (complete reservoir).
Output functionals F = 2<l, b_L>, <w,b> = Re sum w^* b.  Matched LO: l_X = u, l_P = i u, u = psi_L/|psi_L|.
Cov(F1,F2) = <w1(0),w2(0)> + sum_k (2n_sp-1)(Gh-1) <w1_k,w2_k>,
[F1,F2]/2i = Im sum w1(0)^* w2(0) - sum_k (Gh-1) Im sum w1_k^* w2_k   (must equal 1 for X_A, P_LO).
"""
import numpy as np


def seed(kind, x, delta=0.05, chirp=0.0, eps0=0.05):
    """Initial field.  kind='parabola': rho = delta*softplus((1-x^2)/delta); 'gaussian': rho = exp(-x^2).
    chirp = a'(0) (= da/dzeta of the hydrodynamic width); phase S = -chirp x^2/2, psi = sqrt(rho) e^{iS/eps0}."""
    if kind == "parabola":
        s = (1 - x**2) / delta
        rho = delta * np.logaddexp(0.0, s)
    elif kind == "gaussian":
        rho = np.exp(-x**2)
    else:
        raise ValueError(kind)
    return np.sqrt(rho) * np.exp(-1j * chirp * x**2 / (2 * eps0))


class Grid:
    def __init__(self, N, L):
        self.N, self.L = N, L
        self.dx = L / N
        self.x = (np.arange(N) - N // 2) * self.dx
        self.k = 2 * np.pi * np.fft.fftfreq(N, d=self.dx)


def lo_covariance(psi0, grid, eps0, Gam, tau_L, nsteps, nsp=1.0, kerr=True, return_traj=False):
    """Matched-LO 2x2 covariance at tau_L = Gamma*zeta_L (in output shot-noise units) and the commutator."""
    zL = tau_L / Gam if Gam > 0 else tau_L
    h = zL / nsteps
    Dh = np.exp(1j * eps0 * grid.k**2 * (h / 2) / 2)   # D(h/2) multiplier in Fourier space
    ga = np.exp(Gam * h / 4)                             # amplitude factor of A(h/2)
    Gh = np.exp(Gam * h / 2)                             # power gain of A(h/2)
    kfac = (h / eps0) if kerr else 0.0

    def step(psi, rec=None, n=None):
        psi = np.fft.ifft(Dh * np.fft.fft(psi))
        psi = ga * psi
        if rec is not None:
            rec[n] = psi
        psi = psi * np.exp(1j * kfac * np.abs(psi) ** 2)
        psi = ga * psi
        return np.fft.ifft(Dh * np.fft.fft(psi))

    # forward pass with checkpoints every ck steps (memory ~ N*(nsteps/ck + ck)*16 bytes);
    # each segment is recomputed in the backward pass to recover the background at the input of each K
    ck = int(max(1, min(nsteps, round(np.sqrt(nsteps)))))
    starts = list(range(0, nsteps, ck))
    cps = []
    psi = psi0.astype(complex).copy()
    for n in range(nsteps):
        if n % ck == 0:
            cps.append(psi.copy())
        psi = step(psi)
    psiL = psi
    u = psiL / np.linalg.norm(psiL)
    w = np.stack([u, 1j * u])                              # adjoint vectors for X_A and P_LO
    Cn = np.zeros((2, 2))                                  # ASE sum of <w_i, w_j>
    Om = 0.0                                               # reservoir commutator sum
    Dc = np.conj(Dh)
    def acc(w):
        g = np.real(np.conj(w) @ w.T)                      # Gram matrix <w_i, w_j>
        o = np.imag(np.vdot(w[0], w[1]))
        return g, o
    for si in range(len(starts) - 1, -1, -1):
        n0 = starts[si]; n1 = min(nsteps, n0 + ck)
        seg = np.empty((n1 - n0, grid.N), complex)
        p = cps[si].copy()
        for j in range(n1 - n0):
            p = step(p, seg, j)
        for n in range(n1 - 1, n0 - 1, -1):
            w = np.fft.ifft(Dc * np.fft.fft(w, axis=1), axis=1)  # D^T
            g, o = acc(w); Cn += g; Om += o                      # noise injected by the second A(h/2)
            w = ga * w
            pb = seg[n - n0]
            phi = kfac * np.abs(pb) ** 2
            ew = np.exp(-1j * phi) * w
            w = ew + 2 * kfac * np.imag(np.conj(pb) * ew) * pb   # K^T
            g, o = acc(w); Cn += g; Om += o                      # noise injected by the first A(h/2)
            w = ga * w
            w = np.fft.ifft(Dc * np.fft.fft(w, axis=1), axis=1)  # D^T
    g0, o0 = acc(w)
    C = g0 + (2 * nsp - 1) * (Gh - 1) * Cn
    comm = o0 - (Gh - 1) * Om
    lam = np.linalg.eigvalsh(C)
    out = dict(C=C, lam_min=lam[0], lam_max=lam[1], comm=comm, N_out_over_N0=np.linalg.norm(psiL)**2 / np.linalg.norm(psi0)**2,
               C_in=g0, C_ase_unit=(Gh - 1) * Cn, comm_input_only=o0)
    if return_traj:
        out["psiL"] = psiL
    return out


def kappa(psi0, grid):
    """int rho^2 / int rho and the peak of rho, for the seed."""
    rho = np.abs(psi0) ** 2
    return np.sum(rho**2) / np.sum(rho), rho.max()
