"""Two-mode cross-phase NLS, linearized vacuum noise as a per-frequency-bin photon-number covariance, and filter optimizers.

claude-b, T-20261008-claude-b-01. The propagation is the split-step code of run 2026-10-04-claude-b-manakov-deviation-scan
(twomode_lib.py), unchanged in substance, generalized to any grid. Model (normalized soliton units):
    i a_z + 1/2 a_tt + (C00 |a|^2 + C01 |b|^2) a = 0
    i b_z + i d b_t + 1/2 b_tt + (C10 |a|^2 + C11 |b|^2) b = 0
Linearized vacuum noise of coherent inputs: the input field samples psi_i = sqrt(dt) * field_i have quadrature variance 1/4
(photon units), and the output count in spectral bin (m, k) is n_mk = |psi~_mk|^2 with the unitary FFT. The Jacobian
G[mk, i] = d n_mk / d(input quadrature i) is taken by central differences of the discrete split-step map (all 4N
directions in one batch). The per-bin covariance is Cov = G G^T / 4. A filter with transmission T_k in [0, 1], applied to
both modes, then has Var(N_T) = T^T C_tot T + sum_k T_k (1 - T_k) nbar_k (partition vacuum of the filter loss) and
F(T) = Var / (T . nbar), with C_tot = sum over mode pairs of Cov and nbar_k = sum_m nbar_mk.
"""
import numpy as np

fft, ifft = np.fft.fft, np.fft.ifft


class Grid:
    def __init__(self, N=256, TW=40.0):
        self.N, self.TW = N, TW
        self.t = (np.arange(N) - N // 2) * (TW / N)
        self.dt = self.t[1] - self.t[0]
        self.w = 2 * np.pi * np.fft.fftfreq(N, d=self.dt)
        self.dw = 2 * np.pi / TW
        self.k = np.round(self.w / self.dw).astype(int)
        self.order = np.argsort(self.k)          # bins sorted by frequency, for interval filters


def propagate(g, a, b, z, dz, C, d):
    """Strang split-step (linear half, nonlinear full, linear half). a, b: (..., N) complex."""
    La = np.exp((-0.5j * g.w ** 2) * dz / 2)
    Lb = np.exp((-0.5j * g.w ** 2 - d * 1j * g.w) * dz / 2)
    n = int(round(z / dz))
    for _ in range(n):
        a = ifft(La * fft(a, axis=-1), axis=-1)
        b = ifft(Lb * fft(b, axis=-1), axis=-1)
        Ia, Ib = np.abs(a) ** 2, np.abs(b) ** 2
        a = a * np.exp(1j * (C[0][0] * Ia + C[0][1] * Ib) * dz)
        b = b * np.exp(1j * (C[1][0] * Ia + C[1][1] * Ib) * dz)
        a = ifft(La * fft(a, axis=-1), axis=-1)
        b = ifft(Lb * fft(b, axis=-1), axis=-1)
    return a, b


def spectral_counts(g, a, b):
    fa = fft(a, axis=-1) * np.sqrt(g.dt / g.N)
    fb = fft(b, axis=-1) * np.sqrt(g.dt / g.N)
    return np.abs(fa) ** 2, np.abs(fb) ** 2


def bin_covariance(g, a0, b0, z, dz, C, d, eps=1e-6):
    """Return nbar (2, N) and Cov (2N, 2N) of the spectral bin counts (mode a bins first, then mode b)."""
    N = g.N
    dirs = np.zeros((4 * N, 2, N), complex)
    r = 0
    for m in (0, 1):
        for q in (1.0, 1j):
            dirs[r:r + N, m, :] = np.eye(N) * (q * eps / np.sqrt(g.dt))
            r += N
    A = np.concatenate([a0[None] + dirs[:, 0], a0[None] - dirs[:, 0]])
    B = np.concatenate([b0[None] + dirs[:, 1], b0[None] - dirs[:, 1]])
    ao, bo = propagate(g, A, B, z, dz, C, d)
    na, nb = spectral_counts(g, ao, bo)
    M = 4 * N
    G = np.concatenate([(na[:M] - na[M:]) / (2 * eps), (nb[:M] - nb[M:]) / (2 * eps)], axis=1).T   # (2N, 4N)
    am, bm = propagate(g, a0[None], b0[None], z, dz, C, d)
    nam, nbm = spectral_counts(g, am, bm)
    nbar = np.stack([nam[0], nbm[0]])
    Cov = 0.25 * G @ G.T
    return nbar, Cov


def totals(nbar, Cov, N):
    """All-mode (common filter) bin covariance C_tot (N, N) and nbar_tot (N)."""
    Caa, Cab, Cba, Cbb = Cov[:N, :N], Cov[:N, N:], Cov[N:, :N], Cov[N:, N:]
    return Caa + Cab + Cba + Cbb, nbar[0] + nbar[1]


def fano(T, Ct, nt):
    T = np.asarray(T, float)
    return (T @ Ct @ T + np.sum(T * (1 - T) * nt)) / (T @ nt)


# ---------------- filter classes ----------------

def class_sym_hard(g, Ct, nt, kmaxes):
    """A: hard symmetric band |k| <= kmax. Returns dict kmax -> F."""
    return {int(km): float(fano((np.abs(g.k) <= km).astype(float), Ct, nt)) for km in kmaxes}


def class_sym_frac(g, Ct, nt, kmax_range):
    """A': symmetric band |k| <= kmax plus bins |k| = kmax+1 at transmission f in [0, 1] (continuous effective edge
    (kmax + 1/2 + f) dw). F(f) is a ratio of a quadratic and a linear function of f; minimized exactly on [0, 1].
    Returns the best (F, kmax, f, edge) and the list over kmax."""
    best, rows = None, []
    for km in kmax_range:
        T0 = (np.abs(g.k) <= km).astype(float)
        E = (np.abs(g.k) == km + 1).astype(float)
        # Var(f) = a2 f^2 + a1 f + a0 ; mean(f) = m1 f + m0  (partition: f(1-f) * E.nt)
        a2 = E @ Ct @ E - E @ nt
        a1 = 2 * T0 @ Ct @ E + E @ nt
        a0 = T0 @ Ct @ T0
        m1, m0 = E @ nt, T0 @ nt
        fs = np.linspace(0, 1, 2001)
        Fv = (a2 * fs ** 2 + a1 * fs + a0) / (m1 * fs + m0)
        i = int(np.argmin(Fv))
        # refine with the exact stationary point if interior
        disc_f = fs[i]
        for f in np.roots([a2 * m1, 2 * a2 * m0, a1 * m0 - a0 * m1]):
            if np.isreal(f) and 0 <= f.real <= 1:
                fv = (a2 * f.real ** 2 + a1 * f.real + a0) / (m1 * f.real + m0)
                if fv < Fv[i]:
                    disc_f = f.real
        F = (a2 * disc_f ** 2 + a1 * disc_f + a0) / (m1 * disc_f + m0)
        row = dict(kmax=int(km), f=float(disc_f), edge=float((km + 0.5 + disc_f) * g.dw), F=float(F))
        rows.append(row)
        if best is None or F < best["F"]:
            best = row
    return best, rows


def class_interval(g, Ct, nt):
    """B: hard band [k1, k2] in frequency order (any position, any width). Exhaustive via 2D prefix sums."""
    o = g.order
    Cs = Ct[np.ix_(o, o)]
    ns = nt[o]
    N = len(ns)
    P = np.zeros((N + 1, N + 1))
    P[1:, 1:] = np.cumsum(np.cumsum(Cs, axis=0), axis=1)
    pn = np.concatenate([[0.0], np.cumsum(ns)])
    i1 = np.arange(N)[:, None]
    i2 = np.arange(N)[None, :]
    valid = i2 >= i1
    j1, j2 = np.broadcast_to(i1, (N, N)), np.broadcast_to(i2, (N, N))
    V = P[j2 + 1, j2 + 1] - P[j1, j2 + 1] - P[j2 + 1, j1] + P[j1, j1]
    Mn = pn[j2 + 1] - pn[j1]
    with np.errstate(divide="ignore", invalid="ignore"):
        Fm = np.where(valid & (Mn > 1e-12 * pn[-1]), V / Mn, np.inf)
    idx = np.unravel_index(np.argmin(Fm), Fm.shape)
    k_lo, k_hi = int(g.k[o][idx[0]]), int(g.k[o][idx[1]])
    return dict(F=float(Fm[idx]), k1=k_lo, k2=k_hi, w1=float((k_lo - 0.5) * g.dw), w2=float((k_hi + 0.5) * g.dw))


def class_any(g, Ct, nt, starts, iters=4000):
    """C: any transmission T in [0, 1]^N applied to both modes. Minimizes F = 1 + T^T C' T / (T . n), C' = C_tot - diag(n),
    by projected gradient descent with backtracking from the given starts. Non-convex: reports the best local minimum."""
    Cp = Ct - np.diag(nt)
    def R(T):
        return (T @ Cp @ T) / (T @ nt)
    best = None
    for T in starts:
        T = np.clip(np.asarray(T, float), 0, 1)
        step = 1.0
        val = R(T)
        for _ in range(iters):
            s = T @ nt
            q = T @ Cp @ T
            grad = (2 * (Cp @ T) * s - q * nt) / s ** 2
            while step > 1e-14:
                Tn = np.clip(T - step * grad, 0, 1)
                if Tn @ nt <= 0:
                    step *= 0.5
                    continue
                vn = R(Tn)
                if vn < val - 1e-15:
                    break
                step *= 0.5
            if step <= 1e-14:
                break
            dv = val - vn
            T, val = Tn, vn
            step *= 2.0
            if dv < 1e-15:
                break
        if best is None or val < best[0]:
            best = (val, T.copy())
    return dict(F=float(1 + best[0])), best[1]


def launch(g, p2, C):
    p1 = 1 - p2
    S = C[0][0] * p1 * p1 + (C[0][1] + C[1][0]) * p1 * p2 + C[1][1] * p2 * p2
    s = 1 / np.cosh(g.t)
    return np.sqrt(p1 / S) * s + 0j, np.sqrt(p2 / S) * s + 0j, S
