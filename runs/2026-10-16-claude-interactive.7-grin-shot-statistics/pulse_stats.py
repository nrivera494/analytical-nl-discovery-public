"""Statistics across time within one pulse, and their shot-to-shot reproducibility.
Model, launch and disorder as in shot_stats.py (exact GRIN tensor, K = 5, E' = 0.6, sigma = 0.3, dz = 0.05; z in L_NL at PEAK power).
Each time slice t of a Gaussian pulse is an independent cell (no dispersion) with power fraction s(t) = exp(-t^2), launched with the
same mode shape: A = sqrt(s) A0. Resonant model without disorder: exact scaling I_p(z; s) = s i_p(s z), so the slices sample one
trajectory at lengths s z. With disorder (here) the scaling is approximate.
Two pulses ('shots'): the same slices with independent vacuum noise at n = 1e10 photons per peak cell, to show shot-to-shot reproducibility.
Recorded at z = 10, 30, 100, 300: within the FWHM (s >= 1/2), across slices: relative variance of the normalized mode fractions
f_p = I_p / sum I (median over the 5 launched excited modes), the condensate fraction f_0 (mean, relative variance), and the
shot-to-shot difference between the two pulses; also the energy-weighted pulse-integrated f_p against the Dirichlet means."""
import numpy as np, json, time, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
K, Eprime, sigma, dz, n = 5, 0.6, 0.3, 0.05, 1e10
zrec = [10, 30, 100, 300]
groups, eps, _, S, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1)
blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
I0 = np.zeros(M); a = Eprime/3.; i1 = groups == 1; i2 = groups == 2
I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1 - I0.sum()
ph0 = np.random.default_rng(1).uniform(0, 2*np.pi, M)
A0 = np.sqrt(I0)*np.exp(1j*ph0)
Ts = 128; t = np.linspace(-np.sqrt(np.log(2)), np.sqrt(np.log(2)), Ts); s = np.exp(-t**2)   # FWHM: s in [1/2, 1]
nrng = np.random.default_rng(99)
def pulse():
    return np.sqrt(s)[None, :]*A0[:, None] + (nrng.standard_normal((M, Ts)) + 1j*nrng.standard_normal((M, Ts)))*np.sqrt(1/(4*n))
A = np.concatenate([pulse(), pulse()], axis=1)
def rhs(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1); return 1j*(R2 @ v)
drng = np.random.default_rng(7)
def unitaries():
    Us = []
    for b in blocks:
        nb = len(b); Z = (drng.standard_normal((nb, nb)) + 1j*drng.standard_normal((nb, nb)))/2
        Hh = (Z + Z.conj().T)/np.sqrt(2); w, V = np.linalg.eigh(Hh); Us.append((V*np.exp(-1j*sigma*np.sqrt(dz)*w)) @ V.conj().T)
    return Us
D = M - 1; ex = eps[1:]; T = Eprime/D; S1 = np.sum(1/ex); S2 = np.sum(1/ex**2)
dir_ref = dict(g2_excited_minus_1=(D - 1)/(D + 1), f0_mean=1 - T*S1, f0_relvar=T**2*D*(S2 - S1**2/D)/(D + 1)/(1 - T*S1)**2,
               f_mean_excited=(T/ex).tolist())
launched = np.where((groups == 1) | (groups == 2))[0]
recs = []; z = 0.0; t0 = time.time()
for zt in zrec:
    while z < zt - 1e-9:
        k1 = rhs(A); k2 = rhs(A + 0.5*dz*k1); k3 = rhs(A + 0.5*dz*k2); k4 = rhs(A + dz*k3); A = A + dz*(k1 + 2*k2 + 2*k3 + k4)/6
        for b, U in zip(blocks, unitaries()): A[b, :] = U @ A[b, :]
        z += dz
    I = np.abs(A)**2; f = I/I.sum(0); fa, fb = f[:, :Ts], f[:, Ts:]
    rv = fa.var(1)/fa.mean(1)**2
    w = s/s.sum(); integ = (fa*w[None, :]).sum(1)     # energy-weighted pulse-integrated fractions (FWHM part)
    shot = np.abs(fa - fb).max()
    recs.append(dict(z=zt, relvar_launched_median=float(np.median(rv[launched])), relvar_excited_median=float(np.median(rv[1:])),
                     f0_mean=float(fa[0].mean()), f0_relvar=float(rv[0]), integrated_f0=float(integ[0]),
                     integrated_group_fractions=[float(integ[groups == k].sum()) for k in range(K)],
                     max_abs_shot_to_shot_difference_of_fractions=float(shot)))
    r = recs[-1]
    print(f"z={zt:4d}: across the pulse (FWHM): launched relvar {r['relvar_launched_median']:.3f}, all-excited {r['relvar_excited_median']:.3f} "
          f"(Dirichlet {dir_ref['g2_excited_minus_1']:.3f}); f0 mean {r['f0_mean']:.3f} relvar {r['f0_relvar']:.2e} (Dirichlet {dir_ref['f0_mean']:.3f}, {dir_ref['f0_relvar']:.2e}); "
          f"integrated f0 {r['integrated_f0']:.3f}; max |pulse1 - pulse2| {shot:.1e}; {time.time()-t0:.0f}s", flush=True)
group_rj = [1 - T*S1] + [float(np.sum(T/ex[(groups[1:] == k)])) for k in range(1, K)]
json.dump(dict(K=K, Eprime=Eprime, sigma=sigma, dz=dz, n=n, slices=Ts, s_range=[float(s.min()), 1.0], dirichlet=dir_ref,
               group_fractions_rj=group_rj, records=recs), open('pulse_stats.json', 'w'), indent=1)
print('RJ group fractions', [round(x, 3) for x in group_rj])
