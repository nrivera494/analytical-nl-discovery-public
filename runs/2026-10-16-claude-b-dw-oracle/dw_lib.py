"""Numpy oracle for dispersive-wave (DW) yield in the TOD-perturbed NLSE, with an exact discrete adjoint.

claude-b, T-20261016-claude-interactive-03. Model M0 (Roy, Bhadra & Agrawal 2009, Eqs. 1-2):
    i u_xi + (1/2) u_tautau + N^2 |u|^2 u = i delta3 u_tautautau,   delta3 = beta3 / (6 |beta2| T0).
Physics Fourier convention: u(tau) = (1/2pi) int uhat(w) exp(-i w tau) dw, w > 0 blue. On the grid
uhat_k = fft(u)_k (times dt), with w_k = -2 pi fftfreq_k, so d/dtau -> -i w and the linear step is
uhat -> uhat exp(i D(w) h), D(w) = delta3 w^3 - w^2/2. Zero-dispersion frequency w_z = 1/(6 delta3).

Integrator: Strang splitting (order 2) or its Yoshida triple-jump composition (order 4); the nonlinear
sub-step u -> u exp(i N^2 |u|^2 c h) is exact. The discrete adjoint below is the exact derivative of
that map (to rounding):
    linear sub-step L(c h):     lam <- ifft(conj(E) fft(lam)),  E = exp(i D c h)
    nonlinear sub-step (coef a = N^2 c h, input u1, phi = a |u1|^2):
                                lam <- exp(-i phi) lam - 2 a Im(conj(lam) exp(i phi) u1) u1
Real objective J(u), lam = dJ/d conj(u) (Wirtinger), dJ = 2 Re sum conj(lam) du.
"""
import numpy as np

fft, ifft = np.fft.fft, np.fft.ifft

YA = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
YB = 1.0 - 2.0 * YA


def grid(Nt, TW):
    tau = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = TW / Nt
    w = -2.0 * np.pi * np.fft.fftfreq(Nt, d=dt)
    return tau, dt, w


def Dfun(w, d3):
    return d3 * w ** 3 - 0.5 * w ** 2


def schedule(nsteps, order):
    """Global list of sub-steps for nsteps steps: ('L', c) or ('N', c), c in units of h; adjacent L merged."""
    if order == 2:
        per = [('L', 0.5), ('N', 1.0), ('L', 0.5)]
    elif order == 4:
        per = [('L', YA / 2), ('N', YA), ('L', (YA + YB) / 2), ('N', YB), ('L', (YA + YB) / 2), ('N', YA),
               ('L', YA / 2)]
    else:
        raise ValueError(order)
    out = []
    for _ in range(nsteps):
        for op in per:
            if op[0] == 'L' and out and out[-1][0] == 'L':
                out[-1] = ('L', out[-1][1] + op[1])
            else:
                out.append(op)
    return out


class Prop:
    """Fixed-step propagator for model M0 on a periodic grid."""

    def __init__(self, Nt, TW, N, d3, xi, h, order=4):
        self.tau, self.dt, self.w = grid(Nt, TW)
        self.Nt, self.TW, self.N, self.d3 = Nt, TW, N, d3
        self.nsteps = max(1, int(np.ceil(xi / h - 1e-9)))
        self.h = xi / self.nsteps
        self.xi = xi
        self.order = order
        self.sched = schedule(self.nsteps, order)
        D = Dfun(self.w, d3)
        self._E = {}
        for kind, c in self.sched:
            if kind == 'L' and c not in self._E:
                self._E[c] = np.exp(1j * D * c * self.h)
        self.N2 = N * N
        self.wz = 1.0 / (6.0 * d3) if d3 > 0 else np.inf

    def run(self, u0, store=False, record=()):
        """Propagate; optionally store the input of every nonlinear sub-step; record callables at step ends.
        record: list of xi values at which to call snapshot (returns dict xi -> field)."""
        u = u0.astype(complex).copy()
        U = [] if store else None
        rec_steps = {int(round(x / self.h)): x for x in record}
        snaps = {}
        if 0 in rec_steps:
            snaps[rec_steps[0]] = u.copy()
        nN = 0
        per_step = 3 if self.order == 4 else 1
        for kind, c in self.sched:
            if kind == 'L':
                u = ifft(self._E[c] * fft(u))
            else:
                if store:
                    U.append(u)
                u = u * np.exp(1j * self.N2 * c * self.h * (u.real ** 2 + u.imag ** 2))
                nN += 1
                if nN % per_step == 0:
                    s = nN // per_step
                    if s in rec_steps and s != self.nsteps:
                        # field at the end of a step needs the trailing linear half sub-step
                        cl = (YA / 2) if self.order == 4 else 0.5
                        snaps[rec_steps[s]] = ifft(np.exp(1j * Dfun(self.w, self.d3) * cl * self.h) * fft(u))
        if self.nsteps in rec_steps:
            snaps[rec_steps[self.nsteps]] = u.copy()
        return u, U, snaps

    def adjoint(self, lam, U):
        """Back-propagate lam = dJ/dconj(u_final) to dJ/dconj(u0) using stored nonlinear-step inputs U."""
        lam = lam.astype(complex).copy()
        k = len(U)
        for kind, c in reversed(self.sched):
            if kind == 'L':
                lam = ifft(np.conj(self._E[c]) * fft(lam))
            else:
                k -= 1
                u1 = U[k]
                a = self.N2 * c * self.h
                e = np.exp(1j * a * (u1.real ** 2 + u1.imag ** 2))
                lam = np.conj(e) * lam - 2.0 * a * np.imag(np.conj(lam) * e * u1) * u1
        return lam


def spectrum(u):
    return np.abs(fft(u)) ** 2


def band_mask(w, wz):
    return w >= wz


def band_fraction(u, w, wz, E0):
    """Fraction of E0 (sum |fft(u_laser)|^2) found at w >= wz."""
    S = spectrum(u)
    return S[w >= wz].sum() / E0


def gate(tau, tg, s=1.0):
    """Smooth gate: 0 for |tau| < tg, 1 outside, tanh edges of width s."""
    return 1.0 - 0.5 * (np.tanh((tau + tg) / s) - np.tanh((tau - tg) / s))


def gated_fraction(u, tau, w, wz, E0, tg=15.0, s=1.0):
    v = u * gate(tau, tg, s)
    return band_fraction(v, w, wz, E0)


def invariants(u, w, dt, N, d3):
    """E = int|u|^2, P = <w>, H = int K n dw/2pi - N^2/2 int |u|^4, K = -D (normalized units)."""
    Nt = len(u)
    uh = fft(u) * dt
    dw = 2 * np.pi / (Nt * dt)
    n = np.abs(uh) ** 2 / (2 * np.pi)
    E = n.sum() * dw
    P = (w * n).sum() * dw / E
    H = (-Dfun(w, d3) * n).sum() * dw - 0.5 * N * N * (np.abs(u) ** 4).sum() * dt
    return E, P, H


def nsr_peak(u, uin, w, wz):
    """Roy's observable: max spectral density at w >= wz over max input spectral density (dB), and peak w."""
    S = spectrum(u)
    S0 = spectrum(uin)
    m = w >= wz
    i = np.argmax(np.where(m, S, -1))
    return 10 * np.log10(S[i] / S0.max()), w[i], 10 * np.log10(S[i] / S.max())


# ---------------------------------------------------------------- masks and gradients

class MaskProblem:
    """Objective J = eta_B(xi_f) (fraction of laser photons at w >= wz) for input fft(u_in) = m(w) fft(u_laser).
    Phase in a Legendre basis on the laser band [-wl, wl]; amplitude a_k in [0,1] per in-band bin (passive)."""

    def __init__(self, prop, ulaser, K=24, wl=None, band_thresh=1e-5, passive=False, log=True, gated=None):
        self.p = prop
        self.Q = fft(ulaser)
        self.E0 = (np.abs(self.Q) ** 2).sum()
        aQ = np.abs(self.Q)
        self.inb = np.where(aQ > band_thresh * aQ.max())[0]
        w = prop.w
        if wl is None:
            wl = np.abs(w[self.inb]).max()
        self.wl = wl
        x = np.clip(w[self.inb] / wl, -1, 1)
        self.K = K
        self.B = np.polynomial.legendre.legvander(x, K)[:, 2:]   # drop constant and linear (phase offset, delay)
        self.nphi = self.B.shape[1]
        self.passive = passive
        self.log = log
        self.chi = (w >= prop.wz).astype(float)
        self.gated = gated
        self.nev = 0

    def unpack(self, x):
        phi = np.zeros(self.p.Nt)
        phi[self.inb] = self.B @ x[:self.nphi]
        a = np.ones(self.p.Nt)
        if self.passive:
            a[self.inb] = x[self.nphi:]
        return phi, a

    def x0(self, coeffs=None):
        c = np.zeros(self.nphi) if coeffs is None else np.asarray(coeffs, float)
        if self.passive:
            return np.concatenate([c, np.ones(len(self.inb))])
        return c

    def bounds(self):
        b = [(None, None)] * self.nphi
        if self.passive:
            b += [(0.0, 1.0)] * len(self.inb)
        return b

    def input_field(self, x):
        phi, a = self.unpack(x)
        m = a * np.exp(1j * phi)
        return ifft(m * self.Q), m

    def value(self, x):
        u0, _ = self.input_field(x)
        u, _, _ = self.p.run(u0)
        J = band_fraction(u, self.p.w, self.p.wz, self.E0)
        return J, u

    def value_grad(self, x):
        """Returns (f, g) for minimisation: f = -log J (or -J)."""
        self.nev += 1
        u0, m = self.input_field(x)
        u, U, _ = self.p.run(u0, store=True)
        uh = fft(u)
        J = (np.abs(uh) ** 2 * self.chi).sum() / self.E0
        lam = self.p.Nt * ifft(self.chi * uh) / self.E0
        lam0 = self.p.adjoint(lam, U)
        Lam = fft(lam0)
        Nt = self.p.Nt
        base = m * self.Q * np.conj(Lam)
        dphi = -(2.0 / Nt) * np.imag(base)          # dJ/dphi_k
        g = [self.B.T @ dphi[self.inb]]
        if self.passive:
            phi, a = self.unpack(x)
            da = (2.0 / Nt) * np.real(np.exp(1j * phi) * self.Q * np.conj(Lam))
            g.append(da[self.inb])
        g = np.concatenate(g)
        if self.log:
            return -np.log(J), -g / J, J
        return -J, -g, J


# ---------------------------------------------------------------- checkpointed variant (bounded memory)

class CkptProp(Prop):
    """Same Yoshida/Strang map, but with an unmerged per-step schedule so that the state at every step boundary is
    well defined; forward states are checkpointed every `every` steps and recomputed segment-wise in the adjoint."""

    def __init__(self, *a, every=50, **k):
        super().__init__(*a, **k)
        if self.order == 4:
            self.per = [('L', YA / 2), ('N', YA), ('L', (YA + YB) / 2), ('N', YB), ('L', (YA + YB) / 2), ('N', YA),
                        ('L', YA / 2)]
        else:
            self.per = [('L', 0.5), ('N', 1.0), ('L', 0.5)]
        D = Dfun(self.w, self.d3)
        self._Es = {c: np.exp(1j * D * c * self.h) for kind, c in self.per if kind == 'L'}
        self.every = every

    def step(self, u, store=None):
        for kind, c in self.per:
            if kind == 'L':
                u = ifft(self._Es[c] * fft(u))
            else:
                if store is not None:
                    store.append(u)
                u = u * np.exp(1j * self.N2 * c * self.h * (u.real ** 2 + u.imag ** 2))
        return u

    def run_ckpt(self, u0):
        u = u0.astype(complex).copy()
        ck = {}
        for s in range(self.nsteps):
            if s % self.every == 0:
                ck[s] = u.copy()
            u = self.step(u)
        return u, ck

    def adjoint_ckpt(self, lam, ck):
        lam = lam.astype(complex).copy()
        starts = sorted(ck)
        for s0 in reversed(starts):
            s1 = min(s0 + self.every, self.nsteps)
            u = ck[s0].copy()
            seg = []
            for s in range(s0, s1):
                st = []
                u = self.step(u, st)
                seg.append(st)
            for s in range(s1 - 1, s0 - 1, -1):
                st = seg[s - s0]
                k = len(st)
                for kind, c in reversed(self.per):
                    if kind == 'L':
                        lam = ifft(np.conj(self._Es[c]) * fft(lam))
                    else:
                        k -= 1
                        u1 = st[k]
                        a = self.N2 * c * self.h
                        e = np.exp(1j * a * (u1.real ** 2 + u1.imag ** 2))
                        lam = np.conj(e) * lam - 2.0 * a * np.imag(np.conj(lam) * e * u1) * u1
        return lam


class CkptMaskProblem(MaskProblem):
    def value(self, x):
        u0, _ = self.input_field(x)
        u, _ = self.p.run_ckpt(u0)
        return band_fraction(u, self.p.w, self.p.wz, self.E0), u

    def value_grad(self, x):
        self.nev += 1
        u0, m = self.input_field(x)
        u, ck = self.p.run_ckpt(u0)
        uh = fft(u)
        J = (np.abs(uh) ** 2 * self.chi).sum() / self.E0
        lam = self.p.Nt * ifft(self.chi * uh) / self.E0
        lam0 = self.p.adjoint_ckpt(lam, ck)
        Lam = fft(lam0)
        Nt = self.p.Nt
        dphi = -(2.0 / Nt) * np.imag(m * self.Q * np.conj(Lam))
        g = [self.B.T @ dphi[self.inb]]
        if self.passive:
            phi, a = self.unpack(x)
            da = (2.0 / Nt) * np.real(np.exp(1j * phi) * self.Q * np.conj(Lam))
            g.append(da[self.inb])
        g = np.concatenate(g)
        if self.log:
            return -np.log(J), -g / J, J
        return -J, -g, J


class GatedCkptMaskProblem(CkptMaskProblem):
    """Objective on the gated field v = g(tau) u (smooth gate zeroing |tau| < tg): J = sum_{w >= wz} |fft(v)|^2 / E0.
    Adjoint seed: lam = g * Nt ifft(chi fft(g u)) / E0 (g real)."""

    def __init__(self, *a, tg=15.0, gs=1.0, **k):
        super().__init__(*a, **k)
        self.g = gate(self.p.tau, tg, gs)

    def value(self, x):
        u0, _ = self.input_field(x)
        u, _ = self.p.run_ckpt(u0)
        return band_fraction(self.g * u, self.p.w, self.p.wz, self.E0), u

    def value_grad(self, x):
        self.nev += 1
        u0, m = self.input_field(x)
        u, ck = self.p.run_ckpt(u0)
        vh = fft(self.g * u)
        J = (np.abs(vh) ** 2 * self.chi).sum() / self.E0
        lam = self.g * self.p.Nt * ifft(self.chi * vh) / self.E0
        lam0 = self.p.adjoint_ckpt(lam, ck)
        Lam = fft(lam0)
        Nt = self.p.Nt
        dphi = -(2.0 / Nt) * np.imag(m * self.Q * np.conj(Lam))
        g = [self.B.T @ dphi[self.inb]]
        if self.passive:
            phi, a = self.unpack(x)
            da = (2.0 / Nt) * np.real(np.exp(1j * phi) * self.Q * np.conj(Lam))
            g.append(da[self.inb])
        g = np.concatenate(g)
        if self.log:
            return -np.log(J), -g / J, J
        return -J, -g, J
