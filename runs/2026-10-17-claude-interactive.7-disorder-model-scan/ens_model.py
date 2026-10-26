"""Shared integrator for the ensemble runs (task T-20261017-claude-interactive.7-02): resonant GRIN model with the exact Hermite-Gauss
Kerr tensor (K = 5, 15 modes, S_0000 = 1, N = 1, z in L_NL), RK4, launches and disorder models as fixed in predictions.md.
Draw order and launch construction are identical to the earlier runs, so phase_seed 1 / dis_seed 7 reproduces the reference realization."""
import numpy as np, os, time
import grin_model as gm
from grin_overlaps import grin_tensor, hermite_functions
K = 5
groups, eps, _, S, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1)
blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
modes, _, _ = grin_tensor(K)
psi0 = hermite_functions(K, np.array([0.0]))[:, 0]
centre = np.array([psi0[nx]*psi0[ny] for nx, ny in modes])
D = M - 1; S1 = float(np.sum(1/eps[1:])); S2 = float(np.sum(1/eps[1:]**2))

def dirichlet(Ep):
    T = Ep/D
    return dict(I0=1 - T*S1, VarI0=T**2*D*(S2 - S1**2/D)/(D + 1), g2=2*D/(D + 1),
                Pk=[1 - T*S1] + [float(np.sum(T/eps[groups == k])) for k in range(1, K)])

def launch(kind, Ep, phase_seed, vac_seed=None, n_vac=1e10):
    I0 = np.zeros(M)
    if kind in ('deph', 'focused'):
        if Ep <= 1.0: a = Ep/3.; ga, gb = 1, 2
        else: a = Ep/5.; ga, gb = 2, 3
        I0[groups == ga] = a/np.sum(groups == ga); I0[groups == gb] = a/np.sum(groups == gb); I0[0] = 1 - I0.sum()
    elif kind == 'G1':
        I0[groups == 1] = 0.5
    else:
        raise ValueError(kind)
    ph = np.random.default_rng(phase_seed).uniform(0, 2*np.pi, M)
    if kind == 'focused':
        nz = np.abs(centre) > 1e-12; ph[nz] = np.where(centre[nz] > 0, 0.0, np.pi)
    A = np.sqrt(I0)*np.exp(1j*ph)
    if vac_seed is not None:
        r = np.random.default_rng(vac_seed); A = A + (r.standard_normal(M) + 1j*r.standard_normal(M))*np.sqrt(1/(4*n_vac))
    return A

def _draw_H(rng, nb):
    Z = (rng.standard_normal((nb, nb)) + 1j*rng.standard_normal((nb, nb)))/2
    return (Z + Z.conj().T)/np.sqrt(2)

class WhiteDisorder:
    """Original model: Brownian U(k+1) in each degenerate group, increment exp(-i sigma sqrt(dz) H), H GUE (E|H_ij|^2 = 1/2), every step."""
    def __init__(self, sigma, seed, dz):
        self.rng = np.random.default_rng(seed); self.a = sigma*np.sqrt(dz)
    def step(self, A):
        for b in blocks:
            w, V = np.linalg.eigh(_draw_H(self.rng, len(b)))
            A[b] = ((V*np.exp(-1j*self.a*w)) @ V.conj().T) @ A[b]
        return A

class PiecewiseDisorder:
    """Finite correlation length: a fixed H per group acts as exp(-i s H dz) per step and is redrawn every l_c; s = sigma_eff/sqrt(l_c)
    gives the white-noise-equivalent strength sigma_eff^2 (cf. Delta beta = sigma_beta^2 l_beta)."""
    def __init__(self, sigma_eff, lc, seed, dz):
        self.rng = np.random.default_rng(seed); self.s = sigma_eff/np.sqrt(lc); self.dz = dz
        self.nstep = max(1, int(round(lc/dz))); self.count = 0; self.U = None
    def step(self, A):
        if self.count % self.nstep == 0:
            self.U = []
            for b in blocks:
                w, V = np.linalg.eigh(_draw_H(self.rng, len(b))); self.U.append((V*np.exp(-1j*self.s*self.dz*w)) @ V.conj().T)
        for b, U in zip(blocks, self.U): A[b] = U @ A[b]
        self.count += 1
        return A

def rhs(A):
    v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)

def run(kind, Ep, phase_seed, disorder=None, vac_seed=None, zmax=4000., dz=0.05, every=0.5, W=(1000., 4000.), raw_path=None):
    t0 = time.time()
    A = launch(kind, Ep, phase_seed, vac_seed)
    Ep_true = float(np.sum(eps*np.abs(A)**2))
    nst = int(round(zmax/dz)); ev = int(round(every/dz))
    I = np.empty((nst//ev + 1, M)); I[0] = np.abs(A)**2
    for s in range(1, nst + 1):
        k1 = rhs(A); k2 = rhs(A + 0.5*dz*k1); k3 = rhs(A + 0.5*dz*k2); k4 = rhs(A + dz*k3); A = A + dz*(k1 + 2*k2 + 2*k3 + k4)/6
        if disorder is not None: A = disorder.step(A)
        if s % ev == 0: I[s//ev] = np.abs(A)**2
    z = np.arange(I.shape[0])*every
    ref = dirichlet(Ep_true)
    sel = (z >= W[0]) & (z <= W[1]); X = I[sel]
    I0m = float(X[:, 0].mean()); VarI0 = float(X[:, 0].var())
    g2 = float(np.mean((X[:, 1:]**2).mean(0)/X[:, 1:].mean(0)**2))
    Pk = [float(X[:, groups == k].sum(1).mean()) for k in range(K)]
    DRJ = float(max(abs(Pk[k]/ref['Pk'][k] - 1) for k in range(1, K)))
    blk = np.array_split(X[:, 0], 8); be = float(np.std([b.mean() for b in blk], ddof=1)/np.sqrt(8))
    # L_rel: first z with |mean I0 over [z, z+50] - <I0>_D| <= 0.02
    nw = int(round(50/every)); cs = np.concatenate([[0], np.cumsum(I[:, 0])]); rm = (cs[nw:] - cs[:-nw])/nw
    hit = np.where(np.abs(rm - ref['I0']) <= 0.02)[0]; Lrel = float(z[hit[0]]) if len(hit) else None
    on = np.where(I[:, 0] > 0.3)[0]; zon = float(z[on[0]]) if len(on) else None
    N = I.sum(1); E = (I*eps[None, :]).sum(1)
    if raw_path is not None:
        np.savez_compressed(raw_path, z=z[::4], I=I[::4].astype(np.float32))
    return dict(kind=kind, Eprime=Ep_true, phase_seed=phase_seed, vac_seed=vac_seed, I0=I0m, I0_D=ref['I0'], VarI0=VarI0, VarI0_D=ref['VarI0'],
                relvar0=VarI0/I0m**2 if I0m > 0 else None, g2_ex=g2, Pk=Pk, Pk_RJ=ref['Pk'], D_RJ=DRJ, block_err_I0=be, L_rel=Lrel, z_on=zon,
                I0_max=float(I[:, 0].max()), drift_N=float(np.ptp(N)), drift_E=float(np.ptp(E)), wall_s=time.time() - t0)
