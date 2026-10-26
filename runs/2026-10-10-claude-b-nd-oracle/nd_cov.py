"""Linearized quantum noise of a pulse in normally dispersive single-mode fibre: full output quadrature covariance and
the bound chain of P-20261010-claude-interactive-01 (claude-b, T-20261010-claude-interactive-05).

Model, soliton units tau = T/T0, xi = z/L_D, u = A/sqrt(P0), N^2 = gamma P0 T0^2/|beta2| (normal dispersion, beta2 > 0):
    i u_xi - 1/2 u_tautau + N^2 |u|^2 u = 0       [+ optional self-steepening s = 1/(omega0 T0)]
Strang split step (linear half, nonlinear full, linear half). Input u0 = exp(-tau^2/2) (Gaussian, 1/e intensity half-width T0).

Noise: the input field samples psi_i = sqrt(dt) u_i are coherent states (quadrature variance 1/4 in photon units). J is
the Jacobian of the output quadratures (Re, Im of the unitary-DFT spectral amplitudes, photon units) with respect to the
input quadratures, by central differences of the discrete map (all 2 Nt directions in one batch). Shot-noise-normalized
output covariance V = J J^T (V = 1 for a passive unitary map). From it:
  lambda_min(V):  smallest eigenvalue of V;
  lambda_pass:    smallest eigenvalue of V restricted to the hyperplane orthogonal to the global phase direction i*alpha;
  lambda_gen:     smallest generalized eigenvalue of (C, diag nbar), C the covariance of the spectral bin counts
                  n_k = |alpha_k|^2 (C = G G^T / 4, G = dn/d input quadratures), over bins holding the light;
  binary filters: F[T] = T^T C T / T^T nbar, T_k in {0, 1}; searched over all intervals (exhaustive), then single-bin
                  flip descent from several starts (best interval, sign patterns of the lambda_gen eigenvector, all ones,
                  random sets).
"""
import numpy as np

fft, ifft = np.fft.fft, np.fft.ifft


class Grid:
    def __init__(self, Nt=512, TW=40.0):
        self.Nt, self.TW = Nt, TW
        self.t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
        self.dt = self.t[1] - self.t[0]
        self.w = 2 * np.pi * np.fft.fftfreq(Nt, d=self.dt)
        self.order = np.argsort(self.w)


def xi_wb(N):
    """Wave-breaking distance of an unchirped Gaussian in normal dispersion, in units of L_D,
    z_wb = L_D / sqrt(4 N^2 exp(-3/2) - 1) (as quoted by Finot et al. 2008 after Anderson et al. 1992; checked in-run)."""
    return 1.0 / np.sqrt(4 * N ** 2 * np.exp(-1.5) - 1)


def propagate(g, u, xi, dxi, N2, s=0.0):
    """u: (..., Nt) complex. Normal dispersion. s: self-steepening 1/(omega0 T0) (applied in the nonlinear step to first
    order via the operator (1 + i s d/dtau) on |u|^2 u, RK2 midpoint)."""
    L = np.exp((0.5j * g.w ** 2) * dxi / 2)
    n = int(round(xi / dxi))
    for _ in range(n):
        u = ifft(L * fft(u, axis=-1), axis=-1)
        if s == 0.0:
            u = u * np.exp(1j * N2 * np.abs(u) ** 2 * dxi)
        else:
            def nl(v):
                p = np.abs(v) ** 2 * v
                return 1j * N2 * (p + 1j * s * ifft(1j * g.w * fft(p, axis=-1), axis=-1))
            k1 = nl(u)
            u = u + dxi * nl(u + 0.5 * dxi * k1)
        u = ifft(L * fft(u, axis=-1), axis=-1)
    return u


def output_spectrum(g, u):
    return fft(u, axis=-1) * np.sqrt(g.dt / g.Nt)       # photon-unit spectral amplitudes (unitary)


def jacobian(g, u0, xi, dxi, N2, s=0.0, eps=1e-6):
    """J (2Nt x 2Nt): rows = output (Re alpha_k, Im alpha_k), columns = input (x_i, y_i); and the mean output alpha."""
    Nt = g.Nt
    D = 2 * Nt
    dirs = np.zeros((D, Nt), complex)
    dirs[:Nt] = np.eye(Nt) * (eps / np.sqrt(g.dt))
    dirs[Nt:] = np.eye(Nt) * (1j * eps / np.sqrt(g.dt))
    batch = np.concatenate([u0[None] + dirs, u0[None] - dirs])
    out = output_spectrum(g, propagate(g, batch, xi, dxi, N2, s))
    d = (out[:D] - out[D:]) / (2 * eps)                  # (D, Nt) complex: d alpha_k / d input_j
    J = np.concatenate([d.real.T, d.imag.T], axis=0)       # (2Nt, D)
    alpha = output_spectrum(g, propagate(g, u0[None], xi, dxi, N2, s))[0]
    return J, alpha


def bound_chain(g, J, alpha, keep_frac=1 - 1e-9):
    """lambda_min(V), lambda_pass, lambda_gen, the count covariance C and nbar over the kept bins (frequency order)."""
    Nt = g.Nt
    V = J @ J.T
    ev = np.linalg.eigvalsh(V)
    lam_min, lam_2 = float(ev[0]), float(ev[1])
    p = np.concatenate([-alpha.imag, alpha.real])
    p /= np.linalg.norm(p)
    big = 10 * np.max(np.abs(V))
    lam_pass = float(np.linalg.eigvalsh(V + big * np.outer(p, p))[0])
    nbar_all = np.abs(alpha) ** 2
    G = 2 * (alpha.real[:, None] * J[:Nt] + alpha.imag[:, None] * J[Nt:])   # (Nt bins, D)
    o = g.order
    srt = np.sort(nbar_all)[::-1]
    thr = srt[np.searchsorted(np.cumsum(srt) / srt.sum(), keep_frac)]
    keep = [i for i in o if nbar_all[i] >= thr]
    Gk = G[keep]
    C = 0.25 * Gk @ Gk.T
    nb = nbar_all[keep]
    Dm = 1 / np.sqrt(nb)
    lam_gen = float(np.linalg.eigvalsh(Dm[:, None] * C * Dm[None, :])[0])
    evec = np.linalg.eigh(Dm[:, None] * C * Dm[None, :])[1][:, 0] * Dm
    return dict(lam_min=lam_min, lam_2=lam_2, lam_pass=lam_pass, lam_gen=lam_gen, n_bins=len(keep)), C, nb, np.array(keep), evec


def fano(T, C, nb):
    return float(T @ C @ T / (T @ nb))


def best_interval(C, nb):
    n = len(nb)
    P = np.zeros((n + 1, n + 1))
    P[1:, 1:] = np.cumsum(np.cumsum(C, axis=0), axis=1)
    pn = np.concatenate([[0.0], np.cumsum(nb)])
    i1, i2 = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    V = P[i2 + 1, i2 + 1] - P[i1, i2 + 1] - P[i2 + 1, i1] + P[i1, i1]
    M = pn[i2 + 1] - pn[i1]
    with np.errstate(divide="ignore", invalid="ignore"):
        Fm = np.where((i1 <= i2) & (M > 1e-6 * pn[-1]), V / M, np.inf)
    k = np.unravel_index(np.argmin(Fm), Fm.shape)
    T = np.zeros(n)
    T[k[0]:k[1] + 1] = 1
    return float(Fm[k]), T


def flip_descent(T, C, nb, max_sweeps=200):
    """Best-improvement single-bin flips until no flip lowers F."""
    T = T.astype(float).copy()
    CT = C @ T
    num, den = float(T @ CT), float(T @ nb)
    diagC = np.diag(C)
    for _ in range(max_sweeps):
        s = 1 - 2 * T                                   # +1 adds the bin, -1 removes it
        new_num = num + 2 * s * CT + diagC               # (T + s e_k)^T C (T + s e_k)
        new_den = den + s * nb
        with np.errstate(divide="ignore", invalid="ignore"):
            Fn = np.where(new_den > 1e-9 * nb.sum(), new_num / new_den, np.inf)
        k = int(np.argmin(Fn))
        if Fn[k] >= num / den - 1e-14:
            break
        T[k] = 1 - T[k]
        CT += s[k] * C[:, k]
        num, den = float(new_num[k]), float(new_den[k])
    return num / den, T


def iterated_local_search(T, F, C, nb, rng, n_iter=300, kmax=6):
    """Perturb the incumbent by flipping 1..kmax random bins, descend, accept if better."""
    bestF, bestT = F, T.copy()
    n = len(nb)
    for _ in range(n_iter):
        Tp = bestT.copy()
        idx = rng.choice(n, size=rng.integers(1, kmax + 1), replace=False)
        Tp[idx] = 1 - Tp[idx]
        if Tp.sum() == 0:
            continue
        Fp, Tp = flip_descent(Tp, C, nb)
        if Fp < bestF - 1e-14:
            bestF, bestT = Fp, Tp
    return bestF, bestT


def best_binary(C, nb, evec, rng_seed=0, n_random=60, n_ils=400):
    """Search: exhaustive intervals; flip descent from structured and random starts; iterated local search from the best."""
    starts = {}
    Fi, Ti = best_interval(C, nb)
    starts["interval"] = Ti
    starts["evec_pos"] = (evec > 0).astype(float)
    starts["evec_neg"] = (evec < 0).astype(float)
    for q in (0.25, 0.5):
        thr = q * np.max(np.abs(evec))
        starts[f"evec_pos_{q}"] = (evec > thr).astype(float)
        starts[f"evec_neg_{q}"] = (evec < -thr).astype(float)
    starts["all"] = np.ones(len(nb))
    rng = np.random.default_rng(rng_seed)
    for r in range(n_random):
        starts[f"random{r}"] = (rng.random(len(nb)) < 0.5).astype(float)
    best = None
    results = {}
    for name, T0 in starts.items():
        if T0.sum() == 0:
            continue
        F, T = flip_descent(T0, C, nb)
        results[name] = F
        if best is None or F < best[0]:
            best = (F, T, name)
    F_descent = best[0]
    Fils, Tils = iterated_local_search(best[1], best[0], C, nb, rng, n_iter=n_ils)
    if Fils < best[0]:
        best = (Fils, Tils, best[2] + "+ils")
    return dict(F_best=best[0], start=best[2], F_interval=Fi, F_descent=F_descent, n_on=int(best[1].sum()),
                per_start=results), best[1]
