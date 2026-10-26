"""Direct view of thermalization in the GRIN resonant model (exact Hermite-Gauss Kerr tensor, K = 5 groups, 15 modes, S_0000 = 1,
z in L_NL, total power N = 1). Classical field dynamics only (no noise), single trajectories, RK4 dz = 0.05, z up to 1e4.
Mode coupling: (i) Kerr only (sigma = 0): the resonant four-wave mixing among modes with eps_p + eps_q = eps_r + eps_s;
(ii) Kerr + weak random LINEAR coupling inside each degenerate group (Brownian U(k+1), sigma = 0.3, dis_seed 7). The linear coupling
cannot move power between groups (it conserves every group's power); only the Kerr terms do.
Launches (random fixed phases, phase_seed 1):
  'E06'  fundamental 0.6, groups 1 and 2 at 0.2 each (E' = 0.6, Dirichlet <I_0> = 0.739);
  'G1'   all power in group 1 (the two HG10/HG01 modes, 0.5 each; E' = 1, Dirichlet <I_0> = 0.565): the fundamental starts empty.
         Every other mode is then exactly empty, and every Kerr source term for an empty mode vanishes (each needs another empty-mode
         amplitude), so a noiseless field never leaves group 1. The G1 runs therefore add one vacuum-noise sample at n = 1e10 photons
         per cell to every mode (E|delta|^2 = 1/(2n), default_rng(31)): spontaneous four-wave mixing seeds the transfer.
Recorded every 0.5 L_NL: all 15 mode powers. Field snapshots A(z) at z = 0, 1, 10, 100, 1000, 1e4 for near-field images.
Outputs thermalize_<launch>_s<sigma>.npz (2.6 MB each, in the raw-data folder RAW) and a printed summary vs the Dirichlet/RJ prediction for z in [2000, 1e4]."""
import numpy as np, time, warnings, sys, os
warnings.filterwarnings('ignore')
import grin_model as gm
K, dz, zmax, every = 5, 0.05, 1.0e4, 0.5
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-grin-thermalization-visual'); os.makedirs(RAW, exist_ok=True)
groups, eps, _, S, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1)
blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
def launch(name):
    I0 = np.zeros(M)
    if name == 'E06':
        I0[groups == 1] = 0.2/2; I0[groups == 2] = 0.2/3; I0[0] = 0.6
    elif name == 'G1':
        I0[groups == 1] = 0.5
    ph = np.random.default_rng(1).uniform(0, 2*np.pi, M)
    return np.sqrt(I0)*np.exp(1j*ph)
def rhs(A):
    v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)
def run(name, sigma, seed_n=None):
    A = launch(name); drng = np.random.default_rng(7)
    if seed_n is not None:
        sr = np.random.default_rng(31); A = A + (sr.standard_normal(M) + 1j*sr.standard_normal(M))*np.sqrt(1/(4*seed_n))
    nst = int(round(zmax/dz)); ev = int(round(every/dz)); snaps_at = {0: None, 1: None, 10: None, 100: None, 1000: None, 10000: None}
    Is = [np.abs(A)**2]; zs = [0.0]; snaps = {0: A.copy()}; t0 = time.time()
    for s in range(1, nst + 1):
        k1 = rhs(A); k2 = rhs(A + 0.5*dz*k1); k3 = rhs(A + 0.5*dz*k2); k4 = rhs(A + dz*k3); A = A + dz*(k1 + 2*k2 + 2*k3 + k4)/6
        if sigma > 0:
            for b in blocks:
                nb = len(b); Z = (drng.standard_normal((nb, nb)) + 1j*drng.standard_normal((nb, nb)))/2
                Hh = (Z + Z.conj().T)/np.sqrt(2); w, V = np.linalg.eigh(Hh)
                A[b] = ((V*np.exp(-1j*sigma*np.sqrt(dz)*w)) @ V.conj().T) @ A[b]
        if s % ev == 0:
            Is.append(np.abs(A)**2); zs.append(s*dz)
        zz = round(s*dz, 6)
        if zz in snaps_at: snaps[int(zz)] = A.copy()
    Is = np.array(Is); zs = np.array(zs)
    # conservation checks
    N = Is.sum(1); E = (Is*eps[None, :]).sum(1)
    D = M - 1; Ep = float(E[0]); T = Ep/D; S1 = np.sum(1/eps[1:])
    late = zs >= 2000
    mean_late = Is[late].mean(0); g2 = (Is[late]**2).mean(0)/mean_late**2
    pred_I0 = 1 - T*S1; pred_ex = T/eps[1:]
    np.savez(os.path.join(RAW, f'thermalize_{name}_s{sigma}.npz'), z=zs, I=Is, groups=groups, eps=eps, Eprime=Ep,
             snap_z=np.array(sorted(snaps)), snap_A=np.array([snaps[k] for k in sorted(snaps)]))
    gp = [mean_late[groups == k].sum() for k in range(K)]; gpr = [pred_I0] + [np.sum(T/eps[groups == k]) for k in range(1, K)]
    print(f"{name} sigma={sigma}: E'={Ep:.3f}; drift N {np.ptp(N):.1e}, E' {np.ptp(E):.1e}; z>=2000: <I_0> {mean_late[0]:.3f} (Dirichlet {pred_I0:.3f}); "
          f"group powers {np.round(gp, 3).tolist()} vs RJ {np.round(gpr, 3).tolist()}; mean excited g2 {g2[1:].mean():.3f} (Dirichlet {2*D/(D+1):.3f}); "
          f"Var I_0 {Is[late, 0].var():.2e} (Dirichlet {T**2*D*(np.sum(1/eps[1:]**2) - S1**2/D)/(D+1):.2e}); wall {time.time()-t0:.0f}s", flush=True)
if __name__ == '__main__':
    names = sys.argv[1:] or ['E06', 'G1']
    for name in names:
        for sigma in [0.3, 0.0]:
            run(name, sigma, seed_n=(1e10 if name == 'G1' else None))
