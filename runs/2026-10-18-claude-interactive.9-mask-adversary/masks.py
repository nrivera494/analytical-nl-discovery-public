"""Adversarial passive-mask optimiser for the leading ZS eigenvalue (claude-interactive.9, 2026-10-18).

q_m(t) = (1/2pi) int m(k) S(k) e^{ikt} dk on a periodic FC window; |m| <= 1 is built in by m = cos(psi) e^{i phi}.
The leading eigenvalue is tracked by shifted inverse iteration with a two-sided Rayleigh quotient (left vector
w = (v2, v1)); its gradient with respect to the mask is exact for the discrete problem:
    d zeta = sum_l (G_l dm_l + H_l conj(dm_l)),
    G_l = (S_l/T) sum_j g_j e^{i k_l t_j},  H_l = (S_l/T) sum_j h_j e^{-i k_l t_j},
with g = -i v2^2 / (2 sum v1 v2), h = -i v1^2 / (2 sum v1 v2).
Mask families (all passive, all allowed to be asymmetric):
    'phase-cheb'   phi = sum_{j=2..J} c_j T_j(k/K)                      (phase only)
    'passive-cheb' phi as above, psi = sum_{j=0..J} d_j T_j(k/K)        (amplitude and phase)
    'passive-bins' phi_l, psi_l free on every bin with |k_l| <= K        (the richest class on the grid)
    'sharp'        phi, psi = sums of steep logistic steps sigma((k - c_j)/eps) with free heights and positions
                   (sharp, multi-lobe masks: notches, steps, phase jumps)
"""
import os, sys
import numpy as np
import scipy.linalg as sla
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-18-claude-interactive.9-zs-solver-validation'))
from zs import grid, fc_matrix, fc_eigs, fc_grad


class Problem:
    def __init__(self, S_fun, n, T, K):
        self.n, self.T, self.K = n, T, K
        self.t, self.k = grid(n, T)
        self.S = S_fun(self.k).astype(float)
        self.E = np.exp(1j * np.outer(self.t, self.k))
        self.I = np.eye(2 * n)
        self.z = None
        self.v = None
        self.nfull = 0
        self.kmax = np.pi * n / T

    def pulse(self, m):
        return self.E @ (m * self.S) / self.T

    def leading_full(self, q):
        """Leading non-spurious eigenvalue from the full FC spectrum (eigenvalues only), eigenvector by inverse iteration."""
        self.nfull += 1
        w = fc_eigs(q, self.T, imag_min=1e-4)
        keep = [z for z in w if abs(z.real) < 0.6 * self.kmax]
        if not keep:
            return None, None
        z = keep[0]
        n = self.n
        M = fc_matrix(q, self.T)
        lu = sla.lu_factor(M - (z + 1e-10j) * self.I, check_finite=False)
        x = np.random.default_rng(1).standard_normal(2 * n) + 0j
        for it in range(6):
            x = sla.lu_solve(lu, x, check_finite=False)
            x /= np.linalg.norm(x)
        wv = np.concatenate([x[n:], x[:n]])
        z = (wv @ (M @ x)) / (wv @ x)
        return z, x

    def track(self, q):
        """Eigenvalue continued from the home eigenpair (the last accepted iterate); full solve if that fails."""
        n = self.n
        if self.z is None:
            return self.leading_full(q)
        M = fc_matrix(q, self.T)
        sigma = self.z
        x = self.v.copy()
        z = sigma
        r = np.inf
        for refac in range(4):
            lu = sla.lu_factor(M - sigma * self.I, check_finite=False)
            for it in range(12):
                x = sla.lu_solve(lu, x, check_finite=False)
                x /= np.linalg.norm(x)
                w = np.concatenate([x[n:], x[:n]])
                Mx = M @ x
                z = (w @ Mx) / (w @ x)
                r = np.linalg.norm(Mx - z * x)
                if r < 1e-11 * max(1, abs(z)):
                    break
            if r < 1e-11 * max(1, abs(z)):
                break
            sigma = z
        jump = abs(z - self.z)
        if r > 1e-8 or jump > 0.25 or abs(z.real) > 0.6 * self.kmax:
            return self.leading_full(q)
        return z, x

    def eta_grad(self, m):
        q = self.pulse(m)
        z, v = self.track(q)
        self.last = (z, v)
        if z is None:
            return 0.0, None, None, q
        g, h = fc_grad(v, self.n)
        G = (g @ self.E) * self.S / self.T
        H = (h @ np.conj(self.E)) * self.S / self.T
        return z, G, H, q


def cheb_basis(k, K, J, j0):
    x = np.clip(k / K, -1, 1)
    return np.stack([np.cos(j * np.arccos(x)) for j in range(j0, J + 1)], axis=1)


class Family:
    """Maps a real parameter vector to (m, dm/dphi-part, dm/dpsi-part) through linear bases or logistic steps."""

    def __init__(self, prob, kind, J=24, nsteps=6, eps=0.05, kc=0.0):
        self.p, self.kind = prob, kind
        k, K = prob.k - kc, prob.K
        self.kc, self.J, self.K = kc, J, K
        if kind == 'phase-cheb':
            self.Bphi = cheb_basis(k, K, J, 2)
            self.Bpsi = None
        elif kind == 'passive-cheb':
            self.Bphi = cheb_basis(k, K, J, 2)
            self.Bpsi = cheb_basis(k, K, J, 0)
        elif kind == 'passive-bins':
            idx = np.where(np.abs(k) <= K)[0]  # k is measured from the basis centre kc
            B = np.zeros((len(k), len(idx)))
            B[idx, np.arange(len(idx))] = 1.0
            self.Bphi = B
            self.Bpsi = B
        elif kind == 'sharp':
            self.ns, self.eps = nsteps, eps
        self.dim = self._dim()

    def _dim(self):
        if self.kind == 'sharp':
            return 4 * self.ns          # phase heights, phase positions, amplitude-angle heights, amplitude positions
        d = self.Bphi.shape[1]
        if self.Bpsi is not None:
            d += self.Bpsi.shape[1]
        return d

    def phipsi(self, x):
        k = self.p.k - self.kc
        if self.kind == 'sharp':
            ns, eps = self.ns, self.eps
            a, c, b, e = x[:ns], x[ns:2 * ns], x[2 * ns:3 * ns], x[3 * ns:]
            sp = 1 / (1 + np.exp(-(k[:, None] - c[None, :]) / eps))
            se = 1 / (1 + np.exp(-(k[:, None] - e[None, :]) / eps))
            phi = sp @ a
            psi = se @ b
            return phi, psi, (sp, se, a, b)
        nphi = self.Bphi.shape[1]
        phi = self.Bphi @ x[:nphi]
        psi = self.Bpsi @ x[nphi:] if self.Bpsi is not None else np.zeros_like(k)
        return phi, psi, None

    def phipsi_at(self, x, kk):
        """phi, psi of a smooth family evaluated at arbitrary frequencies kk (for re-evaluation on other grids)."""
        k = kk - self.kc
        if self.kind == 'sharp':
            ns, eps = self.ns, self.eps
            a, c, b, e = x[:ns], x[ns:2 * ns], x[2 * ns:3 * ns], x[3 * ns:]
            sp = 1 / (1 + np.exp(-(k[:, None] - c[None, :]) / eps))
            se = 1 / (1 + np.exp(-(k[:, None] - e[None, :]) / eps))
            return sp @ a, se @ b, None
        Bphi = cheb_basis(k, self.K, self.J, 2)
        nphi = Bphi.shape[1]
        phi = Bphi @ x[:nphi]
        psi = cheb_basis(k, self.K, self.J, 0) @ x[nphi:] if self.kind == 'passive-cheb' else np.zeros_like(k)
        return phi, psi, None

    def mask(self, x):
        phi, psi, aux = self.phipsi(x)
        return np.cos(psi) * np.exp(1j * phi), phi, psi, aux

    def value_grad(self, x):
        m, phi, psi, aux = self.mask(x)
        z, G, H, q = self.p.eta_grad(m)
        if G is None:
            return 0.0, np.zeros_like(x)
        # per-bin derivatives of eta = Im zeta
        dphi = np.imag(1j * (G * m - H * np.conj(m)))
        e = np.exp(1j * phi)
        dpsi = np.imag(-np.sin(psi) * (G * e + H * np.conj(e)))
        if self.kind == 'sharp':
            sp, se, a, b = aux
            eps = self.eps
            dsp = sp * (1 - sp) / eps
            dse = se * (1 - se) / eps
            ga = sp.T @ dphi
            gc = -(dsp.T @ dphi) * a
            gb = se.T @ dpsi
            ge = -(dse.T @ dpsi) * b
            grad = np.concatenate([ga, gc, gb, ge])
        else:
            grad = self.Bphi.T @ dphi
            if self.Bpsi is not None:
                grad = np.concatenate([grad, self.Bpsi.T @ dpsi])
        return z.imag, grad


def optimise(prob, fam, x0, bounds=None, maxiter=300, z0=None, v0=None, check_every=15):
    """L-BFGS-B maximisation of the leading eta. Trial points are tracked from the home eigenpair (last accepted
    iterate); every check_every iterations and at the end the full spectrum is computed and the home pair is reset
    to the true leading eigenvalue."""
    cache = {}

    def f(x):
        val, g = fam.value_grad(x)
        cache[x.tobytes()] = prob.last
        return -val, -g

    prob.z, prob.v = z0, v0
    if prob.z is None:
        m, *_ = fam.mask(x0)
        prob.z, prob.v = prob.leading_full(prob.pulse(m))
    state = {'it': 0}

    def cb(xk):
        state['it'] += 1
        zv = cache.get(xk.tobytes())
        if zv is not None and zv[0] is not None:
            prob.z, prob.v = zv
        if state['it'] % check_every == 0:
            m, *_ = fam.mask(xk)
            zf, vf = prob.leading_full(prob.pulse(m))
            if zf is not None and zf.imag > prob.z.imag + 1e-9:
                prob.z, prob.v = zf, vf
        if len(cache) > 50:
            cache.clear()

    res = minimize(f, x0, jac=True, method='L-BFGS-B', bounds=bounds, callback=cb,
                   options={'maxiter': maxiter, 'ftol': 1e-15, 'gtol': 1e-10, 'maxcor': 30})
    m, *_ = fam.mask(res.x)
    zf, vf = prob.leading_full(prob.pulse(m))
    return res, (zf.imag if zf is not None else 0.0)
