"""Cross-check of the reduced semiclassical method (C-20261010-claude-b-01) against the Legendre-block propagator of
C-20261004-claude-a-01 for an unchirped parabolic pulse in normal dispersion (claude-b, T-20261010-claude-interactive-05).

Leading order: lambda_min(V) = Lambda/N^2 with Lambda = 1/sigma_1(C)^2, lambda_pass = Pi/N^2 with Pi = 1/sigma_2(C)^2
(when sigma_2 is odd), where C maps the input amplitude quadrature X0 to the output scaled phase Ytilde = eps sqrt(rho) dtheta.

(1) Legendre blocks (claude-a's propagator, statement (a) of C-20261004-claude-a-01). Parabola rho0 = 1 - tau^2 on |tau| < 1,
    comoving xi = tau / a, a = cosh^2 theta, zeta = theta/2 + sinh(2 theta)/4, mu = tanh theta.
    With delta A = A (nu/2 + i p), n = (1 - xi^2) nu = sum n_l P_l, p = sum p_l P_l, and amplitude-only input,
    p_l(mu) = m_l(mu) n_l(0) / eps with m_l = P_l(0) Q_l(mu) - Q_l(0) P_l(mu) (Wronskian of the Ferrers functions = 1 at 0).
    Input X0 = sum_j x_j phi_j (orthonormal Legendre on [-1, 1]); n = 2 sqrt(1 - xi^2) X0, so n_l = sum_j K_lj x_j,
    K_lj = (2l + 1) int sqrt(1 - xi^2) phi_j P_l. Output norm ||Ytilde||^2 = int (1 - xi^2) p^2 dxi (times eps^2).
    sigma_k(C)^2 = eigenvalues of K^T D G D K, D = diag(m_l), G_lk = int (1 - xi^2) P_l P_k.
(2) Reduced numerics: same as lambda_curve.py (central differences of the full NLSE on the first M Hermite functions)
    with u0 = sqrt(max(1 - tau^2, 0)).
Usage: python parabola.py -> summary.json
"""
import json, os, sys, time
import numpy as np
from scipy.special import lpn, lqn, roots_legendre

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-semiclassical"))
from sigma_c import hermite_functions

fft, ifft = np.fft.fft, np.fft.ifft


def theta_of_zeta(zeta):
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid / 2 + np.sinh(2 * mid) / 4 < zeta:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def legendre_sigma(zeta, L=80, nq=800):
    th = theta_of_zeta(zeta)
    mu = np.tanh(th)
    P0 = lpn(L, 0.0)[0]
    Q0 = lqn(L, 0.0)[0]
    Pm = lpn(L, mu)[0]
    Qm = lqn(L, mu)[0]
    m = P0 * Qm - Q0 * Pm
    x, wq = roots_legendre(nq)
    Pl = np.array([lpn(L, xx)[0] for xx in x]).T          # (L+1, nq)
    phi = Pl * np.sqrt((2 * np.arange(L + 1) + 1) / 2)[:, None]
    s = np.sqrt(1 - x ** 2)
    K = (2 * np.arange(L + 1) + 1)[:, None] * ((Pl * s * wq) @ phi.T)      # K_lj
    G = (Pl * (1 - x ** 2) * wq) @ Pl.T
    D = np.diag(m)
    H = K.T @ D @ G @ D @ K
    ev = np.sort(np.linalg.eigvalsh(0.5 * (H + H.T)))[::-1]
    # parity of the top two singular vectors (phi_j has parity (-1)^j)
    w, U = np.linalg.eigh(0.5 * (H + H.T))
    U = U[:, np.argsort(w)[::-1]]
    par = [float(np.sum(U[0::2, k] ** 2)) for k in range(2)]  # weight on even j
    return dict(zeta=zeta, theta=th, mu=mu, a=np.cosh(th) ** 2, sigma1=float(np.sqrt(ev[0])), sigma2=float(np.sqrt(ev[1])),
                Lambda=float(1 / ev[0]), Pi=float(1 / ev[1]), even_weight_top=par[0], even_weight_second=par[1],
                m_0=float(m[0]), m_2=float(m[2]))


def reduced_curve(N, Nt, M, phi_step, zetas, TW=40.0, eta=1e-6):
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = t[1] - t[0]
    w = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    dZ = phi_step / N
    dxi = dZ / N
    Lop = np.exp(0.5j * w ** 2 * dxi / 2)
    u0 = np.sqrt(np.maximum(1 - t ** 2, 0)) + 0j
    H = hermite_functions(t, M)
    U = np.concatenate([u0[None] + eta * H, u0[None] - eta * H, u0[None]])
    targets = sorted({int(round(z / dZ)) for z in zetas})
    rows, k = [], 0
    for step in range(1, targets[-1] + 1):
        U = ifft(Lop * fft(U, axis=-1), axis=-1)
        U = U * np.exp(1j * N ** 2 * np.abs(U) ** 2 * dxi)
        U = ifft(Lop * fft(U, axis=-1), axis=-1)
        if step == targets[k]:
            k += 1
            ub = U[-1]
            du = (U[:M] - U[M:2 * M]) / (2 * eta)
            ph = np.exp(-1j * np.angle(ub))
            Yt = (du * ph).imag / N * np.sqrt(dt)
            s = np.linalg.svd(Yt.T, compute_uv=False)
            rows.append(dict(zeta=step * dZ, sigma1=float(s[0]), sigma2=float(s[1]), Lambda=float(1 / s[0] ** 2), Pi=float(1 / s[1] ** 2)))
    return rows


if __name__ == "__main__":
    zetas = [0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 4.737126]
    out = {"legendre": [legendre_sigma(z) for z in zetas], "legendre_L40": [legendre_sigma(z, L=40) for z in zetas]}
    for r in out["legendre"]:
        print("legendre", {k: round(v, 6) for k, v in r.items()}, flush=True)
    t0 = time.time()
    out["reduced_N50"] = reduced_curve(50, 2048, 80, 0.02, zetas)
    out["reduced_N50_wall"] = time.time() - t0
    for r in out["reduced_N50"]:
        print("reduced N50", {k: round(v, 6) for k, v in r.items()}, flush=True)
    t0 = time.time()
    out["reduced_N100"] = reduced_curve(100, 4096, 80, 0.02, [z for z in zetas if z <= 2.0])
    out["reduced_N100_wall"] = time.time() - t0
    for r in out["reduced_N100"]:
        print("reduced N100", {k: round(v, 6) for k, v in r.items()}, flush=True)
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
