"""Full mean-plus-tangent propagation for lambda_min at weak normal dispersion.

Written by claude-interactive.12 (independent of the proposer's and claude-a's code).

Model (x = t/T0, zeta = z/L, eps = L/L_D = y/Phi):
    u_zeta = -i (eps/2) u_xx + i Phi |u|^2 u,            u(0,x) = exp(-x^2/2)
    du_zeta = -i (eps/2) du_xx + i Phi (2|u|^2 du + u^2 du*)
Periodic Fourier grid on [-Xw, Xw), N points; interaction picture for the
dispersion (exact), the Kerr terms integrated by DOP853 (adaptive, scipy) or by
fixed-step RK4IP.  The tangent map M is real-linear; its columns are propagated for
inputs du = e_m (amplitude quadrature, the input mean is real) and du = i e_m
(phase quadrature), where e_m are the orthonormal even grid functions
(delta_{c+m} + delta_{c-m})/sqrt(2) supported in |x| <= (ne-1) dx (optionally odd
ones too).  lambda_min = sigma_min(M restricted)^2, an upper estimate of the
unrestricted value, which converges to it once the optimal mode is contained.
Vacuum covariance is the identity in these units (lambda0 = (S - Phi)^2).
"""
import json
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp


def basis(N, ne, parity):
    c = N // 2
    if parity == 'full':  # every grid point: the unrestricted map on this grid
        return np.eye(N)
    cols = []
    if parity in ('even', 'both'):
        for m in range(ne):
            e = np.zeros(N)
            if m == 0:
                e[c] = 1.0
            else:
                e[c + m] = e[c - m] = 1 / np.sqrt(2)
            cols.append(e)
    if parity in ('odd', 'both'):
        for m in range(1, ne):
            e = np.zeros(N)
            e[c + m], e[c - m] = 1 / np.sqrt(2), -1 / np.sqrt(2)
            cols.append(e)
    return np.array(cols).T


def setup(Phi, y, N, Xw, ne, parity, profile='gauss'):
    eps = y / Phi
    dx = 2 * Xw / N
    x = -Xw + dx * np.arange(N)
    assert abs(x[N // 2]) < 1e-14
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    lin = 0.5j * eps * k**2  # d/dzeta uhat = lin * uhat + F[nonlinear]
    B = basis(N, ne, parity)
    D0 = np.concatenate([B, 1j * B], axis=1)  # complex input columns
    u0 = {'gauss': np.exp(-x**2 / 2), 'sech': 1 / np.cosh(x),
          'gq': np.exp(-x**2 / 2 - x**4 / 4)}[profile]  # intensity e^{-x^2}, sech^2 x, e^{-x^2-x^4/2}
    W0 = np.concatenate([u0[:, None].astype(complex), D0], axis=1)
    return x, dx, k, lin, B, W0


def nonlin_phys(P, Phi):
    u = P[:, 0]
    dU = P[:, 1:]
    I = (u * u.conj()).real
    out = np.empty_like(P)
    out[:, 0] = 1j * Phi * I * u
    out[:, 1:] = 1j * Phi * (2 * I[:, None] * dU + (u * u)[:, None] * dU.conj())
    return out


def propagate_dop853(Phi, lin, W0, rtol, atol):
    N, ncol = W0.shape
    Y0 = np.fft.fft(W0, axis=0)  # interaction-picture state at zeta = 0
    nfev = [0]

    def rhs(z, Yf):
        nfev[0] += 1
        E = np.exp(lin * z)[:, None]
        P = np.fft.ifft(E * Yf.reshape(N, ncol), axis=0)
        return (np.fft.fft(nonlin_phys(P, Phi), axis=0) / E).ravel()

    sol = solve_ivp(rhs, (0.0, 1.0), Y0.ravel(), method='DOP853', rtol=rtol, atol=atol,
                    t_eval=[1.0])
    assert sol.success, sol.message
    Y1 = sol.y[:, -1].reshape(N, ncol)
    return np.fft.ifft(np.exp(lin)[:, None] * Y1, axis=0), nfev[0]


def propagate_rk4ip(Phi, lin, W0, nsteps):
    N, ncol = W0.shape
    h = 1.0 / nsteps
    Eh = np.exp(lin * h / 2)[:, None]
    Nf = lambda Wf: np.fft.fft(nonlin_phys(np.fft.ifft(Wf, axis=0), Phi), axis=0)
    W = np.fft.fft(W0, axis=0)
    for _ in range(nsteps):
        WI = Eh * W
        k1 = Eh * Nf(W)
        k2 = Nf(WI + h * k1 / 2)
        k3 = Nf(WI + h * k2 / 2)
        k4 = Nf(Eh * (WI + h * k3))
        W = Eh * (WI + h * (k1 + 2 * k2 + 2 * k3) / 6) + h * k4 / 6
    return np.fft.ifft(W, axis=0), 4 * nsteps


def analyse(P1, B, dx, ne, parity):
    dU = P1[:, 1:]
    M = np.concatenate([dU.real, dU.imag], axis=0)
    U_, s, Vt = np.linalg.svd(M, full_matrices=False)
    v = Vt[-1]
    nb = B.shape[1]
    w = v[:nb]**2 + v[nb:]**2  # weight on each input basis function
    if parity == 'full':
        pos = np.abs(np.arange(nb) - nb // 2)
    elif parity == 'both':
        pos = np.concatenate([np.arange(ne), np.arange(1, ne)])[:nb]
    else:
        pos = np.arange(ne)
    rms = np.sqrt(np.sum(w * (pos * dx)**2))
    edge = np.sqrt(w[pos == pos.max()].max() / w.max())
    return {'lam_min': float(s[-1]**2), 'lam_next': float(s[-2]**2), 'mode_rms_x': float(rms),
            'edge_amp_rel': float(edge), 'mean_peak_intensity': float(abs(P1[len(P1) // 2, 0])**2)}


def lam_min(Phi, y, N, Xw=10.0, ne=None, nin_sigma=10.0, parity='even', rtol=1e-13, atol=1e-16,
            method='dop853', nsteps=None, profile='gauss'):
    sig = (y / 24) ** 0.25 if y > 0 else 0.02
    dx = 2 * Xw / N
    if ne is None:
        ne = int(np.ceil(nin_sigma * sig / dx)) + 1
    x, dx, k, lin, B, W0 = setup(Phi, y, N, Xw, ne, parity, profile)
    t0 = time.time()
    if method == 'dop853':
        P1, nfev = propagate_dop853(Phi, lin, W0, rtol, atol)
    else:
        P1, nfev = propagate_rk4ip(Phi, lin, W0, nsteps)
    res = analyse(P1, B, dx, ne, parity)
    S = np.sqrt(1 + Phi**2)
    lam0 = (S - Phi)**2
    A = np.sqrt(2 / 3) * Phi / S
    rel = res['lam_min'] / lam0 - 1
    res.update({'Phi': Phi, 'y': y, 'N': N, 'Xw': Xw, 'dx': dx, 'ne': ne, 'X_in': (ne - 1) * dx,
                'sigma_pred': sig, 'parity': parity, 'method': method, 'rtol': rtol, 'atol': atol,
                'nsteps': nsteps, 'nfev': nfev, 'wall_s': time.time() - t0, 'lam0': lam0,
                'rel_excess': rel, 'profile': profile})
    if y > 0:
        res['c_eff'] = (rel / (A * np.sqrt(y)) - 1) / np.sqrt(y)
    return res


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--phi', type=float, required=True)
    ap.add_argument('--y', type=float, required=True)
    ap.add_argument('--N', type=int, required=True)
    ap.add_argument('--Xw', type=float, default=10.0)
    ap.add_argument('--nin', type=float, default=10.0)
    ap.add_argument('--parity', default='even')
    ap.add_argument('--rtol', type=float, default=1e-13)
    ap.add_argument('--atol', type=float, default=1e-16)
    ap.add_argument('--method', default='dop853')
    ap.add_argument('--nsteps', type=int, default=None)
    ap.add_argument('--tag', default='')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    r = lam_min(a.phi, a.y, a.N, a.Xw, None, a.nin, a.parity, a.rtol, a.atol, a.method, a.nsteps)
    r['tag'] = a.tag
    print(json.dumps(r))
    if a.out:
        with open(a.out, 'a') as f:
            f.write(json.dumps(r) + '\n')
