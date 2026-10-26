"""Exact linearized dispersionless theory of filtered Fano factors (T-20261010-claude-interactive-04).

Model: dA/dz = i gamma A (R * |A|^2) + i A Gamma_R, with R(t) = (1-fR) delta(t) + fR h_R(t) and no dispersion or
self-steepening. Then |A(t)|^2 is z-invariant, and in the frame of the mean phase the linearized quadratures obey
    X_out = X_in,   Y_out = Y_in + K X_in + N_R,
    K = 2 Phi sqrt(p) R sqrt(p)   (Phi = gamma P0 L, p = P/P0),
    <N_R N_R>_sym = 2 Phi sqrt(p) fR H sqrt(p),   H(tau) = int dw/2pi 2|Im h(w)| coth(hbar|w|/2kT) e^{-i w tau}.
Shot noise = 1. Output quadrature covariance:
    V = [[I, K^T], [K, I + K K^T + N]].
Time bins are boxcar modes of width dt. Spectral bins are unitary DFT modes of the (zero-padded) window.
"""
import numpy as np
from numpy.fft import fft, ifft, fftfreq

HBAR = 1.054571817e-34
KB = 1.380649e-23


def htilde_blow_wood(w, tau1=12.2, tau2=32.0):
    """Blow-Wood Raman response spectrum, h~(w) = int_0^inf h(t) e^{i w t} dt, w in rad/fs, tau in fs; h~(0) = 1."""
    a, b = 1.0 / tau2, 1.0 / tau1
    pref = (tau1**2 + tau2**2) / (tau1 * tau2**2)
    return pref * b / ((a - 1j * w) ** 2 + b**2)


def lag_kernels(N, dt, fR, temp_K=300.0, tau1=12.2, tau2=32.0, n_w=2**18, w_max=None):
    """Bin-averaged Toeplitz kernels on a boxcar grid (dt in fs).
    k[m]  = <u_j | h * u_{j-m}>        (response, dimensionless, sum ~ 1)
    Hk[m] = <u_j | H * u_{j-m}>        (reservoir, symmetrized coth spectrum)
    Returns arrays indexed by lag m = -(N-1)..(N-1) (offset N-1)."""
    if fR == 0:
        z = np.zeros(2 * N - 1)
        return z, z
    if w_max is None:
        w_max = max(40.0 / tau1, 40.0 / dt)              # rad/fs
    w = np.linspace(-w_max, w_max, n_w)
    dw = w[1] - w[0]
    sinc2 = np.sinc(w * dt / (2 * np.pi)) ** 2           # np.sinc(x) = sin(pi x)/(pi x)
    ht = htilde_blow_wood(w, tau1, tau2)
    if temp_K > 0:
        x = HBAR * np.abs(w) * 1e15 / (2 * KB * temp_K)
        with np.errstate(divide="ignore", invalid="ignore"):
            coth = np.where(x > 1e-12, 1.0 / np.tanh(np.maximum(x, 1e-300)), 0.0)
        # at w -> 0: 2|Im h| coth -> finite; handle the exact zero bin by its limit
        limw = np.abs(w) < 1e-12
    else:
        coth = np.ones_like(w)
        limw = np.zeros_like(w, dtype=bool)
    Sres = 2 * np.abs(ht.imag) * coth
    if limw.any():
        # 2|Im h(w)| coth(c|w|) -> 2 |d Im h/dw|(0) / c as w -> 0, c = hbar 1e15/(2 kB T)
        c = HBAR * 1e15 / (2 * KB * temp_K)
        dImh = (htilde_blow_wood(1e-6, tau1, tau2).imag - htilde_blow_wood(-1e-6, tau1, tau2).imag) / 2e-6
        Sres[limw] = 2 * abs(dImh) / c
    lags = np.arange(-(N - 1), N) * dt
    # integrals int dw/2pi F(w) dt sinc^2 e^{-i w tau}
    k = np.empty(len(lags))
    Hk = np.empty(len(lags))
    for i0 in range(0, len(lags), 256):
        tau = lags[i0:i0 + 256]
        ph = np.exp(-1j * np.outer(tau, w))
        k[i0:i0 + 256] = (ph @ (ht * sinc2)).real * dw / (2 * np.pi) * dt
        Hk[i0:i0 + 256] = (ph @ (Sres * sinc2)).real * dw / (2 * np.pi) * dt
    return k, Hk


def toeplitz_from_lags(lagvals, N):
    idx = np.arange(N)
    return lagvals[(idx[:, None] - idx[None, :]) + (N - 1)]


def build_model(p, dt, Phi, fR=0.0, temp_K=300.0, tau1=12.2, tau2=32.0, kern=None):
    """p: normalized intensity on the time grid (peak 1). Returns dict with K, Nres, phibar."""
    N = len(p)
    sp = np.sqrt(p)
    if fR == 0:
        Rm = np.eye(N)
        Hm = np.zeros((N, N))
    else:
        if kern is None:
            kern = lag_kernels(N, dt, fR, temp_K, tau1, tau2)
        k, Hk = kern
        Rm = (1 - fR) * np.eye(N) + fR * toeplitz_from_lags(k, N)
        Hm = fR * toeplitz_from_lags(Hk, N)
    K = 2 * Phi * sp[:, None] * Rm * sp[None, :]
    Nres = 2 * Phi * sp[:, None] * Hm * sp[None, :]
    phibar = Phi * (Rm @ p)          # mean phase (R * p)(t); Rm rows sum ~ 1 for slowly varying p
    return {"K": K, "N": Nres, "phibar": phibar, "p": p, "dt": dt}


def covariance(model):
    K, Nres = model["K"], model["N"]
    n = K.shape[0]
    I = np.eye(n)
    V = np.block([[I, K.T], [K, I + K @ K.T + Nres]])
    return V


def lam_min(V):
    return float(np.linalg.eigvalsh(V)[0])


def lam_pass(V, p):
    """Smallest eigenvalue of V on the hyperplane orthogonal to the global phase quadrature (0, sqrt p)."""
    n = len(p)
    e = np.concatenate([np.zeros(n), np.sqrt(p)])
    e /= np.linalg.norm(e)
    # Householder reflector mapping e -> first basis vector; complement = remaining columns
    v = e.copy()
    v[0] -= 1.0 if e[0] >= 0 else -1.0
    if np.linalg.norm(v) < 1e-14:
        Q = np.eye(2 * n)[:, 1:]
    else:
        v /= np.linalg.norm(v)
        Hh = np.eye(2 * n) - 2 * np.outer(v, v)
        Q = Hh[:, 1:]
    return float(np.linalg.eigvalsh(Q.T @ V @ Q)[0])


def symplectic_check(V):
    """min eigenvalue of V + i Omega (must be >= 0 for a physical state), Omega = [[0, I], [-I, 0]]."""
    n = V.shape[0] // 2
    Om = np.block([[np.zeros((n, n)), np.eye(n)], [-np.eye(n), np.zeros((n, n))]])
    return float(np.linalg.eigvalsh(V + 1j * Om)[0])


def spectral(model, V, pad=1, thr=1e-6):
    """Unitary-DFT spectral bins of the zero-padded window. Returns (nbar, Vamp, idx, omega)."""
    p, phib, dt = model["p"], model["phibar"], model["dt"]
    n = len(p)
    ntot = pad * n
    t = (np.arange(ntot) - ntot // 2) * dt
    i0 = ntot // 2 - n // 2
    mean = np.zeros(ntot, complex)
    mean[i0:i0 + n] = np.sqrt(p) * np.exp(1j * phib)
    w = 2 * np.pi * fftfreq(ntot, dt)
    # bin field: A_k = sum_j e^{i w_k t_j} A_j / sqrt(ntot)
    Fm = np.exp(1j * np.outer(w, t)) / np.sqrt(ntot)           # ntot x ntot
    Abar = Fm @ mean
    nbar = np.abs(Abar) ** 2
    keep = nbar >= thr * nbar.max()
    psi = np.angle(Abar[keep])
    # rows: e^{-i psi_k} v_k(t_j) e^{i phibar_j}, restricted to the pulse region (vacuum elsewhere: V = I there)
    G = np.exp(-1j * psi)[:, None] * Fm[keep][:, i0:i0 + n] * np.exp(1j * phib)[None, :]
    Gfull = np.exp(-1j * psi)[:, None] * Fm[keep]                 # for the vacuum part outside the pulse
    C, S = G.real, G.imag
    B = np.hstack([C, -S])
    Vamp = B @ V @ B.T
    # vacuum outside the pulse: contributes (Gout Gout^dagger).real with identity covariance
    mask = np.ones(ntot, bool)
    mask[i0:i0 + n] = False
    if mask.any():
        Go = Gfull[:, mask]
        Vamp += (Go @ Go.conj().T).real
    return nbar[keep], Vamp, np.where(keep)[0], w[keep]


def lam_gen(Vamp):
    return float(np.linalg.eigvalsh(Vamp)[0])


def fano_of(T, nbar, Vamp):
    s = np.sqrt(nbar)
    y = T * s
    den = T @ nbar
    return float(y @ Vamp @ y / den) if den > 0 else np.inf


def binary_search(nbar, Vamp, n_thresh=60, n_restarts=6, rng=None, max_pass=50):
    """Heuristic binary optimization: thresholds of the generalized eigenvectors (several), then single-flip
    local search (first improvement) until no flip improves; plus random restarts. Returns (best F, best T)."""
    rng = np.random.default_rng(0) if rng is None else rng
    s = np.sqrt(nbar)
    Sig = s[:, None] * Vamp * s[None, :]
    n = len(nbar)
    evals, evecs = np.linalg.eigh(Vamp)
    starts = []
    for j in range(min(4, n)):
        u = evecs[:, j] / s                               # generalized eigenvector in count weights
        for sign in (1, -1):
            uu = sign * u
            mx = uu.max()
            if mx <= 0:
                continue
            for th in np.linspace(0.0, 0.95, n_thresh // 4):
                starts.append((uu > th * mx).astype(float))
    for _ in range(n_restarts):
        starts.append((rng.random(n) < 0.5).astype(float))
    best_F, best_T = np.inf, None

    def local_search(T):
        T = T.copy()
        if T.sum() == 0:
            T[np.argmax(nbar)] = 1
        num = T @ Sig @ T
        den = T @ nbar
        g = Sig @ T                                       # Sig T
        for _ in range(max_pass):
            improved = False
            for i in rng.permutation(n):
                d = 1 - 2 * T[i]                          # +1 add, -1 remove
                nnum = num + 2 * d * g[i] + Sig[i, i]
                nden = den + d * nbar[i]
                if nden <= 0:
                    continue
                if nnum / nden < num / den - 1e-15:
                    T[i] += d
                    num, den = nnum, nden
                    g += d * Sig[:, i]
                    improved = True
            if not improved:
                break
        return num / den, T

    # evaluate starts quickly, refine the best few
    scored = sorted(((fano_of(T, nbar, Vamp), k) for k, T in enumerate(starts) if T.sum() > 0))[:8]
    for _, k in scored:
        F, T = local_search(starts[k])
        if F < best_F:
            best_F, best_T = F, T
    return float(best_F), best_T


def gaussian_p(t, T0=1.0):
    return np.exp(-(t / T0) ** 2)


def sech_p(t, Ts=1.0):
    return 1.0 / np.cosh(t / Ts) ** 2


def vmin_kerr(Phi):
    return 1 + 2 * Phi**2 - 2 * Phi * np.sqrt(1 + Phi**2)


def db(x):
    return 10 * np.log10(x)


# ---------------------------------------------------------------- stronger binary search
def _ratio(num, den):
    return num / den if den > 0 else np.inf


def band_scan(nbar, Vamp, w):
    """Exhaustive search over contiguous bands [i, j] and over symmetric pairs of bands (+/- frequency),
    using 2D prefix sums. Returns (best F, T) for each family."""
    s = np.sqrt(nbar)
    Sig = s[:, None] * Vamp * s[None, :]
    n = len(nbar)
    order = np.argsort(w)
    Sg = Sig[np.ix_(order, order)]
    nb = nbar[order]
    P2 = np.zeros((n + 1, n + 1))
    P2[1:, 1:] = Sg.cumsum(0).cumsum(1)
    P1 = np.concatenate([[0], nb.cumsum()])
    best = (np.inf, None)
    for i in range(n):
        j = np.arange(i + 1, n + 1)
        num = P2[j, j] - P2[i, j] - P2[j, i] + P2[i, i]
        den = P1[j] - P1[i]
        F = num / den
        k = np.argmin(F)
        if F[k] < best[0]:
            T = np.zeros(n)
            T[order[i:j[k]]] = 1
            best = (float(F[k]), T)
    return best


def best_improvement(T, Sig, nbar, max_steps=100000):
    T = T.copy().astype(float)
    if T.sum() == 0:
        T[np.argmax(nbar)] = 1
    num = T @ Sig @ T
    den = T @ nbar
    g = Sig @ T
    dg = np.diag(Sig)
    for _ in range(max_steps):
        d = 1 - 2 * T
        nnum = num + 2 * d * g + dg
        nden = den + d * nbar
        with np.errstate(divide="ignore", invalid="ignore"):
            cand = np.where(nden > 0, nnum / nden, np.inf)
        i = int(np.argmin(cand))
        if cand[i] < num / den - 1e-14:
            T[i] += d[i]
            num, den = nnum[i], nden[i]
            g += d[i] * Sig[:, i]
        else:
            break
    return float(T @ Sig @ T / (T @ nbar)), T


def anneal(T, Sig, nbar, rng, n_iter=200000, T0=None, T1=None):
    T = T.copy().astype(float)
    if T.sum() == 0:
        T[np.argmax(nbar)] = 1
    n = len(T)
    num = T @ Sig @ T
    den = T @ nbar
    g = Sig @ T
    dg = np.diag(Sig)
    cur = num / den
    best = (cur, T.copy())
    T0 = cur * 0.05 if T0 is None else T0
    T1 = cur * 1e-5 if T1 is None else T1
    idx = rng.integers(0, n, n_iter)
    u = rng.random(n_iter)
    temps = T0 * (T1 / T0) ** (np.arange(n_iter) / n_iter)
    for it in range(n_iter):
        i = idx[it]
        d = 1 - 2 * T[i]
        nnum = num + 2 * d * g[i] + dg[i]
        nden = den + d * nbar[i]
        if nden <= 0:
            continue
        new = nnum / nden
        if new < cur or u[it] < np.exp(-(new - cur) / temps[it]):
            T[i] += d
            num, den, cur = nnum, nden, new
            g += d * Sig[:, i]
            if cur < best[0]:
                best = (cur, T.copy())
    return best


def binary_search2(nbar, Vamp, w, rng=None, n_anneal=3, n_iter=200000):
    """Stronger heuristic: exhaustive contiguous bands; thresholds of the 6 lowest generalized eigenvectors;
    best-improvement local search from every start; simulated annealing from the best three.
    Returns dict with the best F and its filter, and the best contiguous band."""
    rng = np.random.default_rng(1) if rng is None else rng
    s = np.sqrt(nbar)
    Sig = s[:, None] * Vamp * s[None, :]
    n = len(nbar)
    band_F, band_T = band_scan(nbar, Vamp, w)
    starts = [band_T]
    ev, evec = np.linalg.eigh(Vamp)
    for j in range(min(6, n)):
        u = evec[:, j] / s
        for sign in (1, -1):
            uu = sign * u
            mx = uu.max()
            if mx <= 0:
                continue
            for th in np.linspace(0.0, 0.9, 10):
                starts.append((uu > th * mx).astype(float))
    for _ in range(10):
        starts.append((rng.random(n) < rng.uniform(0.1, 0.9)).astype(float))
    refined = []
    for T in starts:
        if T.sum() == 0:
            continue
        refined.append(best_improvement(T, Sig, nbar))
    refined.sort(key=lambda x: x[0])
    best = refined[0]
    for F, T in refined[:n_anneal]:
        Fa, Ta = anneal(T, Sig, nbar, rng, n_iter=n_iter)
        Fa, Ta = best_improvement(Ta, Sig, nbar)
        if Fa < best[0]:
            best = (Fa, Ta)
    return {"F": float(best[0]), "T": best[1], "band_F": float(band_F), "band_T": band_T}


def tabu_search(T, Sig, nbar, rng, n_iter=None, tenure=None):
    """Tabu search on the Fano ratio: at every step apply the best non-tabu single flip (even if it worsens),
    keep a tabu list of recently flipped bins, track the best ratio seen. O(n) per step (vectorized)."""
    T = T.copy().astype(float)
    if T.sum() == 0:
        T[np.argmax(nbar)] = 1
    n = len(T)
    n_iter = 20 * n if n_iter is None else n_iter
    tenure = max(7, n // 15) if tenure is None else tenure
    num = T @ Sig @ T
    den = T @ nbar
    g = Sig @ T
    dg = np.diag(Sig)
    tabu_until = np.zeros(n, dtype=int)
    best = (num / den, T.copy())
    for it in range(n_iter):
        if it % 100 == 0:                                   # resync to avoid floating-point drift
            num = T @ Sig @ T
            den = T @ nbar
            g = Sig @ T
        d = 1 - 2 * T
        nnum = num + 2 * d * g + dg
        nden = den + d * nbar
        with np.errstate(divide="ignore", invalid="ignore"):
            cand = np.where(nden > 0, nnum / nden, np.inf)
        allowed = tabu_until <= it
        # aspiration: allow tabu move if it beats the global best
        allowed |= cand < best[0] - 1e-14
        cand = np.where(allowed, cand, np.inf)
        i = int(np.argmin(cand))
        if not np.isfinite(cand[i]):
            break
        T[i] += d[i]
        num, den = nnum[i], nden[i]
        g += d[i] * Sig[:, i]
        tabu_until[i] = it + tenure + rng.integers(0, max(2, tenure // 3))
        if num / den < best[0] - 1e-14:
            best = (num / den, T.copy())
    Tb = best[1]
    return (float(Tb @ Sig @ Tb / (Tb @ nbar)), Tb)


def binary_search3(nbar, Vamp, w, rng=None, n_starts=12, n_iter=None):
    """band scan + eigenvector thresholds + random starts -> best-improvement -> tabu search from the best
    n_starts; returns dict with best F, filter, and the best contiguous band."""
    rng = np.random.default_rng(7) if rng is None else rng
    s = np.sqrt(nbar)
    Sig = s[:, None] * Vamp * s[None, :]
    n = len(nbar)
    band_F, band_T = band_scan(nbar, Vamp, w)
    starts = [band_T, np.ones(n)]
    ev, evec = np.linalg.eigh(Vamp)
    for j in range(min(8, n)):
        u = evec[:, j] / s
        for sign in (1, -1):
            uu = sign * u
            mx = uu.max()
            if mx <= 0:
                continue
            for th in np.linspace(-0.5, 0.9, 15):
                starts.append((uu > th * mx).astype(float))
    for _ in range(20):
        starts.append((rng.random(n) < rng.uniform(0.2, 0.8)).astype(float))
    refined = sorted((best_improvement(T, Sig, nbar) for T in starts if T.sum() > 0), key=lambda x: x[0])
    best = refined[0]
    for F, T in refined[:n_starts]:
        Ft, Tt = tabu_search(T, Sig, nbar, rng, n_iter=n_iter)
        if Ft < best[0]:
            best = (Ft, Tt)
    return {"F": float(best[0]), "T": best[1], "band_F": float(band_F)}


def binary_search4(nbar, Vamp, w, rng=None, n_iter=None, extra_starts=()):
    """binary_search3 + brightness-threshold starts T = 1[nbar > c max] and nested-subset seeding:
    solve on bright subsets (c = 1e-2, 1e-3, ...), embed each optimum as a start for the next level.
    Monotone by construction in the bin set (every subset optimum is a start)."""
    rng = np.random.default_rng(11) if rng is None else rng
    s = np.sqrt(nbar)
    Sig = s[:, None] * Vamp * s[None, :]
    n = len(nbar)
    starts = list(extra_starts)
    for c in (0.5, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 1e-3, 1e-4):
        starts.append((nbar > c * nbar.max()).astype(float))
    best = None
    prev = None
    for c in (1e-2, 1e-3, 1e-4, 1e-5, 0.0):
        keep = nbar >= c * nbar.max()
        sub = np.where(keep)[0]
        loc_starts = [T[sub] for T in starts] + ([prev[sub]] if prev is not None else [])
        r = binary_search3(nbar[sub], Vamp[np.ix_(sub, sub)], w[sub], rng=rng, n_iter=n_iter)
        cands = [(r["F"], r["T"])]
        for T in loc_starts:
            if T.sum() == 0:
                continue
            F1, T1 = best_improvement(T, Sig[np.ix_(sub, sub)], nbar[sub])
            F2, T2 = tabu_search(T1, Sig[np.ix_(sub, sub)], nbar[sub], rng, n_iter=n_iter)
            cands.append((F2, T2))
        Fb, Tb = min(cands, key=lambda x: x[0])
        full = np.zeros(n)
        full[sub] = Tb
        if best is None or Fb < best[0]:
            best = (Fb, full)
        prev = best[1]
    Tb = best[1]
    Fexact = float((Tb * s) @ Vamp @ (Tb * s) / (Tb @ nbar))
    return {"F": Fexact, "T": Tb}


# ---------------------------------------------------------------- closed forms (1D integrals)
def raman_kernel_samples(dtf, tau1=12.2, tau2=32.0, tmax=None):
    tmax = 20 * tau2 if tmax is None else tmax
    tt = np.arange(0, tmax, dtf)
    h = ((tau1**2 + tau2**2) / (tau1 * tau2**2)) * np.exp(-tt / tau2) * np.sin(tt / tau1)
    return h / (h.sum() * dtf)            # normalize the sampled kernel to integrate to 1


def momentum_formula(p_func, T0, Phi, fR=0.0, temp_K=300.0, tau1=12.2, tau2=32.0, dtf=0.25, span=12.0):
    """lambda_P,R = [I1 + Phi^2 D_R + (Phi/2) fR S_R] / [I1 + Phi^2 I2_R]: the Fano factor of the momentum-weighted
    spectral count (weights = omega) in the dispersionless model, exact for an infinite, fully resolved spectrum.
    p_func(t) gives the normalized intensity (peak 1); time in fs."""
    t = np.arange(-span * T0, span * T0, dtf)
    p = p_func(t)
    sp = np.sqrt(p)
    dsp = np.gradient(sp, dtf)
    dp = np.gradient(p, dtf)
    I1 = np.sum(dsp**2) * dtf
    if fR == 0:
        Rdp = dp
        RTdp = dp
        S_R = 0.0
    else:
        h = raman_kernel_samples(dtf, tau1, tau2)
        conv = np.convolve(dp, h, mode="full")[: len(dp)] * dtf             # (h * p')(t) = int h(s) p'(t-s) ds
        corr = np.convolve(dp[::-1], h, mode="full")[: len(dp)][::-1] * dtf  # int h(s) p'(t+s) ds
        Rdp = (1 - fR) * dp + fR * conv
        RTdp = (1 - fR) * dp + fR * corr
        # reservoir: int dw/2pi Htilde(w) |FT p'|^2 ; Htilde = 2|Im h~| coth
        n = len(t)
        w = 2 * np.pi * np.fft.fftfreq(n, dtf)
        P = np.fft.fft(dp) * dtf
        ht = htilde_blow_wood(w, tau1, tau2)
        if temp_K > 0:
            x = HBAR * np.abs(w) * 1e15 / (2 * KB * temp_K)
            with np.errstate(divide="ignore", invalid="ignore"):
                Hw = np.where(x > 0, 2 * np.abs(ht.imag) / np.tanh(np.maximum(x, 1e-300)), 0.0)
            c = HBAR * 1e15 / (2 * KB * temp_K)
            Hw[w == 0] = 2 * 2 * (2 / tau2) / ((1 / tau2) ** 2 + (1 / tau1) ** 2) / (2 * c) if False else 2 * (2 * (1 / tau2) / ((1 / tau2) ** 2 + (1 / tau1) ** 2)) / c
        else:
            Hw = 2 * np.abs(ht.imag)
        S_R = float(np.sum(Hw * np.abs(P) ** 2) * (w[1] - w[0]) / (2 * np.pi))
    I2R = np.sum(p * Rdp**2) * dtf
    D_R = np.sum(p * (RTdp - Rdp) ** 2) * dtf
    lamP = (I1 + Phi**2 * D_R + 0.5 * Phi * fR * S_R) / (I1 + Phi**2 * I2R)
    return {"I1": I1, "I2R": I2R, "D_R": D_R, "S_R": S_R, "lam_P": float(lamP),
            "wasted_ratio_vs_kerr_anchor": None}


def lam_min_band(model, V, band_factor=1.2, extra=3.0):
    """Smallest eigenvalue of V restricted to lab-frame quadratures of DFT modes with |omega| <= Omega_b,
    Omega_b = band_factor * max|d phibar/dt| + extra/T_rms (the bright SPM band plus margin)."""
    p, phib, dt = model["p"], model["phibar"], model["dt"]
    n = len(p)
    t = (np.arange(n) - n // 2) * dt
    w = 2 * np.pi * fftfreq(n, dt)
    trms = np.sqrt(np.sum(t**2 * p) / np.sum(p))
    Wb = band_factor * np.max(np.abs(np.gradient(phib, dt))) + extra / trms
    sel = np.abs(w) <= Wb
    Fm = np.exp(1j * np.outer(w[sel], t)) / np.sqrt(n)        # f_k(t) = e^{i w t}/sqrt(n), rows = f_k
    G = Fm.conj() * np.exp(1j * phib)[None, :]                # <f_k| e^{i phibar} (X+iY)/2 > -> components
    c, s = G.real, G.imag
    Q = np.vstack([np.hstack([c, -s]), np.hstack([s, c])])    # orthonormal rows (2 n_b x 2 n)
    return float(np.linalg.eigvalsh(Q @ V @ Q.T)[0]), float(Wb), int(sel.sum())
