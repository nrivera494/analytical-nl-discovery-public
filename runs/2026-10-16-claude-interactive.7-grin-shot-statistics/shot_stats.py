"""Shot-to-shot statistics of the output mode powers at large photon number, for input noise closer to experiments.
Exact GRIN Kerr tensor, K = 5 (15 Hermite-Gauss modes), resonant model, weak Brownian intra-group disorder sigma = 0.3
(dis_seed 7), launch E' = 0.6 (fundamental + equal power in groups 1 and 2, phases phase_seed 1), as in
runs/2026-10-16-claude-interactive.7-grin-twa-scrambling. Units: N = 1 for the mean field, z in L_NL.
Ensembles (B trajectories each, classical dynamics; for quantum noise this is truncated Wigner):
  q1e10   coherent input, vacuum noise for n = 1e10 photons per cell (quantum limit of a quiet laser)
  q1e6    the same noise shape with n_eff = 1e6 (isotropic technical noise; F_in = n/n_eff, e.g. 40 dB above shot noise at n = 1e10)
  q1e4    n_eff = 1e4
  rin1pc  common-mode amplitude jitter A -> A (1 + 0.01 xi) (1% RMS amplitude, 2% RMS power) plus vacuum noise at n = 1e10
  deph    random phase per mode per shot (fixed powers) plus vacuum noise at n = 1e10
Recorded: mean mode powers, relative variance of each mode power across shots (g2 - 1), mean-field fraction, the fraction
f0 = I_0/sum I and its relative variance, and corr(I_0, I_group1). Reference: Dirichlet (C-20261016-claude-interactive.7-01)."""
import numpy as np, json, time, warnings, sys
warnings.filterwarnings('ignore')
import grin_model as gm
K, Eprime, sigma, B, dz = 5, 0.6, 0.3, 128, 0.05
# optional: python shot_stats.py K ens1,ens2,...  (all five ensembles are always drawn, in the same order, then subset)
if len(sys.argv) > 1: K = int(sys.argv[1])
KEEP = sys.argv[2].split(',') if len(sys.argv) > 2 else None
OUT = 'shot_stats.json' if (K == 5 and KEEP is None) else f'shot_stats_K{K}.json'
zrec = [1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300]
groups, eps, _, S, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1)
blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
I0 = np.zeros(M); a = Eprime/3.; i1 = groups == 1; i2 = groups == 2
I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1 - I0.sum()
ph0 = np.random.default_rng(1).uniform(0, 2*np.pi, M)
A0 = np.sqrt(I0)*np.exp(1j*ph0)
nrng = np.random.default_rng(4242)
def vac(n): return (nrng.standard_normal((M, B)) + 1j*nrng.standard_normal((M, B)))*np.sqrt(1/(4*n))
ens = {}
ens['q1e10'] = A0[:, None] + vac(1e10)
ens['q1e6'] = A0[:, None] + vac(1e6)
ens['q1e4'] = A0[:, None] + vac(1e4)
ens['rin1pc'] = A0[:, None]*(1 + 0.01*nrng.standard_normal(B))[None, :] + vac(1e10)
ens['deph'] = (np.sqrt(I0)[:, None]*np.exp(1j*nrng.uniform(0, 2*np.pi, (M, B)))) + vac(1e10)
names = list(ens) if KEEP is None else [k for k in ens if k in KEEP]; A = np.concatenate([ens[k] for k in names], axis=1)
def rhs(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1); return 1j*(R2 @ v)
drng = np.random.default_rng(7)
def unitaries():
    Us = []
    for b in blocks:
        nb = len(b); Z = (drng.standard_normal((nb, nb)) + 1j*drng.standard_normal((nb, nb)))/2
        Hh = (Z + Z.conj().T)/np.sqrt(2); w, V = np.linalg.eigh(Hh); Us.append((V*np.exp(-1j*sigma*np.sqrt(dz)*w)) @ V.conj().T)
    return Us
# Dirichlet reference (condensed regime, E' <= kappa N): excited modes g2 = 2D/(D+1); Var N0 = T^2 D (S2 - S1^2/D)/(D+1)
D = M - 1; ex = eps[1:]; T = Eprime/D; S1 = np.sum(1/ex); S2 = np.sum(1/ex**2)
dir_ref = dict(g2_excited=2*D/(D+1), I0_mean=1 - T*S1, I0_relvar=T**2*D*(S2 - S1**2/D)/(D+1)/(1 - T*S1)**2)
recs = []; t0 = time.time(); z = 0.0; step = 0
for zt in zrec:
    while z < zt - 1e-9:
        k1 = rhs(A); k2 = rhs(A + 0.5*dz*k1); k3 = rhs(A + 0.5*dz*k2); k4 = rhs(A + dz*k3); A = A + dz*(k1 + 2*k2 + 2*k3 + k4)/6
        for b, U in zip(blocks, unitaries()): A[b, :] = U @ A[b, :]
        z += dz; step += 1
    row = dict(z=zt)
    for j, nm in enumerate(names):
        X = A[:, j*B:(j + 1)*B]; I = np.abs(X)**2; Ntot = I.sum(0); f0 = I[0]/Ntot
        g1 = I[groups == 1].sum(0)
        row[nm] = dict(I_mean=I.mean(1).tolist(), relvar=(I.var(1)/I.mean(1)**2).tolist(), coh=(np.abs(X.mean(1))**2/I.mean(1)).tolist(),
                       f0_mean=float(f0.mean()), f0_relvar=float(f0.var()/f0.mean()**2), N_relvar=float(Ntot.var()/Ntot.mean()**2),
                       corr_I0_g1=float(np.corrcoef(I[0], g1)[0, 1]))
    recs.append(row)
    print(f"z={zt:4d}: med relvar excited " + "  ".join(f"{nm} {np.median(row[nm]['relvar'][1:]):.2e}" for nm in names)
          + " | f0 relvar " + " ".join(f"{nm} {row[nm]['f0_relvar']:.2e}" for nm in names) + f" | {time.time()-t0:.0f}s", flush=True)
json.dump(dict(K=K, Eprime=Eprime, sigma=sigma, B=B, dz=dz, ensembles=names, I0_launch=I0.tolist(), groups=groups.tolist(),
               dirichlet=dir_ref, records=recs, wall_s=time.time() - t0), open(OUT, 'w'), indent=1)
print('Dirichlet reference', dir_ref, 'wall', time.time() - t0)
