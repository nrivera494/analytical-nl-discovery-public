"""Checks of the statement that the condensate leaves the thermalization fibre quadrature-squeezed (cond_kerr.py, column own_min_quad_dB:
-4.9 to -7.9 dB at z = 1-50 L_NL for E' = 0.3, sigma = 0.3).
A. Step-size convergence of the tangent-map result: sigma = 0 (deterministic fibre, so dz does not change the disorder path), dz = 0.02 vs 0.01.
B. Independent method: truncated-Wigner ensemble at n = 1e10 (B trajectories, full nonlinear propagation) on the same fibre and launch as
   cond_kerr.py (E' = 0.3, sigma = 0.3, dz = 0.02, launch phases default_rng(1), disorder default_rng(7), identical draw order). The condensate's
   2x2 quadrature covariance in its mean-field frame, in vacuum units (4 n x Wigner covariance), and its smallest eigenvalue.
C. Self-phase-only reference: a single mode with the condensate's accumulated nonlinear phase Phi_self(z) = int_0^z |A_0|^2 dz' (S_0000 = 1)
   has V_P = 1 + 4 Phi^2, C = 2 Phi, V_X = 1, min = 1 + 2 Phi^2 - 2 Phi sqrt(1 + Phi^2).
Output: own_squeezing_checks.json and the printed table (own_squeezing_checks_log.txt)."""
import numpy as np, json, time, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
import cond_kerr as ck
CPS = (1, 2, 5, 10, 20, 50, 100)
out = {}
# A. dz convergence (sigma = 0)
a02 = ck.run(Eprime=0.3, sigma=0.0, dz=0.02, checkpoints=CPS); a01 = ck.run(Eprime=0.3, sigma=0.0, dz=0.01, checkpoints=CPS)
out['A_dz_convergence'] = [dict(z=r2['z'], own_dB_dz002=r2['own_min_quad_dB'], own_dB_dz001=r1['own_min_quad_dB'], V_P_dz002=r2['V_P'], V_P_dz001=r1['V_P'])
                           for r2, r1 in zip(a02['records'], a01['records'])]
for r in out['A_dz_convergence']:
    print(f"A  sigma=0 z={r['z']:5.0f}: own min {r['own_dB_dz002']:7.2f} dB (dz 0.02) vs {r['own_dB_dz001']:7.2f} dB (dz 0.01); V_P {r['V_P_dz002']:.4g} vs {r['V_P_dz001']:.4g}", flush=True)
# B and C. TWA ensemble on the cond_kerr.py fibre (E' = 0.3, sigma = 0.3)
K, Eprime, sigma, dz, n, B = 5, 0.3, 0.3, 0.02, 1e10, 768
groups, eps, _, S4, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1)
rng = np.random.default_rng(1)
I0 = np.zeros(M); a = Eprime/3.; i1 = groups == 1; i2 = groups == 2
I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1 - I0.sum()
A0 = np.sqrt(I0)*np.exp(1j*rng.uniform(0, 2*np.pi, M))
nrng = np.random.default_rng(2024)
A = np.concatenate([A0[:, None], A0[:, None] + (nrng.standard_normal((M, B)) + 1j*nrng.standard_normal((M, B)))*np.sqrt(1/(4*n))], axis=1)  # column 0 noiseless
drng = np.random.default_rng(7)
blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
def rhs(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1); return 1j*(R2 @ v)
tm = {round(r['z']): r for r in [c for c in json.load(open('cond_kerr.json'))['cases'] if c['Eprime'] == 0.3 and c['sigma'] == 0.3][0]['records']}
recs = []; z = 0.0; Phi_self = 0.0; t0 = time.time(); step = 0
for zt in CPS:
    while z < zt - 1e-9:
        I0z = abs(A[0, 0])**2
        k1 = rhs(A); k2 = rhs(A + 0.5*dz*k1); k3 = rhs(A + 0.5*dz*k2); k4 = rhs(A + dz*k3); A = A + dz*(k1 + 2*k2 + 2*k3 + k4)/6
        Phi_self += 0.5*dz*(I0z + abs(A[0, 0])**2)
        for b in blocks:
            nb = len(b); Zm = (drng.standard_normal((nb, nb)) + 1j*drng.standard_normal((nb, nb)))/2
            Hh = (Zm + Zm.conj().T)/np.sqrt(2); w_, V_ = np.linalg.eigh(Hh)
            U = (V_*np.exp(-1j*sigma*np.sqrt(dz)*w_)) @ V_.conj().T
            A[b, :] = U @ A[b, :]
        z += dz
    a0 = A[0, 1:]; m = a0.mean(); d = (a0 - m)*np.exp(-1j*np.angle(m))
    Vt = 4*n*np.cov(np.vstack([d.real, d.imag]))
    ev = np.linalg.eigvalsh(Vt)
    # bootstrap error of the smallest eigenvalue
    bs = []
    brng = np.random.default_rng(11)
    for _ in range(200):
        idx = brng.integers(0, B, B); dd = d[idx] - d[idx].mean()
        bs.append(np.linalg.eigvalsh(4*n*np.cov(np.vstack([dd.real, dd.imag])))[0])
    t = tm[zt]
    spm_min = 1 + 2*Phi_self**2 - 2*Phi_self*np.sqrt(1 + Phi_self**2)
    rec = dict(z=zt, twa_min_dB=float(10*np.log10(ev[0])), twa_min_dB_err=float(10/np.log(10)*np.std(bs)/ev[0]), twa_V_X=float(Vt[0, 0]), twa_V_P=float(Vt[1, 1]),
               twa_V_P_given_X=float(Vt[1, 1] - Vt[0, 1]**2/Vt[0, 0]), tangent_min_dB=t['own_min_quad_dB'], tangent_V_P=t['V_P'], tangent_V_P_given_X=t['V_P_given_X'],
               tangent_V_X=t['V_X'], Phi_self=float(Phi_self), spm_only_V_P=float(1 + 4*Phi_self**2), spm_only_min_dB=float(10*np.log10(spm_min)),
               approx_VX_VPgX_over_VP_dB=float(10*np.log10(t['V_X']*t['V_P_given_X']/t['V_P'])))
    recs.append(rec)
    print(f"B/C z={zt:4d}: TWA min {rec['twa_min_dB']:6.2f} +- {rec['twa_min_dB_err']:.2f} dB vs tangent map {rec['tangent_min_dB']:6.2f} dB | V_P TWA {rec['twa_V_P']:.4g} vs tangent {rec['tangent_V_P']:.4g}; "
          f"V_P|X TWA {rec['twa_V_P_given_X']:.3g} vs {rec['tangent_V_P_given_X']:.3g} | SPM-only: Phi_self {Phi_self:.2f}, V_P {rec['spm_only_V_P']:.4g}, min {rec['spm_only_min_dB']:.1f} dB | "
          f"V_X V_P|X / V_P = {rec['approx_VX_VPgX_over_VP_dB']:.2f} dB | {time.time()-t0:.0f}s", flush=True)
out['B_C_twa_and_spm'] = dict(B=B, n=n, records=recs)
json.dump(out, open('own_squeezing_checks.json', 'w'), indent=1)
