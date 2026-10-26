"""G2 and G3 of predictions.md: multimode quadrature squeezing and photon-counting squeezing of the linearized (tangent-map) state against a
truncated-Wigner ensemble propagated on the same trajectory and the same disorder realization.
GRIN resonant model, K = 5, E' = 0.6, sigma = 0.3, phase_seed 1, dis_seed 7, dz = 0.02 (as runs/2026-10-16-claude-interactive.7-grin-gaussian-state);
B = 512 trajectories; n in {1e6, 1e10}; checkpoints z = 5, 10, 20, 50, 100. Deviations are taken from the noiseless reference trajectory (column 0).
Vacuum-1 units: Wigner covariance of (Re dA, Im dA) times 4n.
- lam_lin = 1/sigma_max^2 and u_min from V = S S^T; TWA: variance of u_min . dx.
- lam_gen,lin = min eigenvalue of V_amp = Pa V Pa^T (amplitude quadratures at the reference phases), weights c; TWA (photon numbers):
  Var(sum_p w_p N_p) / sum_p w_p^2 <N_p> with w_p = c_p / sqrt(<N_p>), N_p = n |A_p|^2; and the linear-quadrature version Var(c . dX).
Bootstrap errors from 100 resamples. Output twa_multimode_check.json and printed lines."""
import json, numpy as np, time, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
K, Ep, sigma, dz, B = 5, 0.6, 0.3, 0.02, 512
CPS = [5, 10, 20, 50, 100]
groups, eps, _, S4, R = gm.build(K, 0, 0)
M = len(groups); R2 = R.reshape(M, -1); RR = R.reshape(M*M, M*M)
blocks = [np.where(groups == k)[0] for k in range(K) if np.sum(groups == k) > 1]
def fA(A):
    v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1); return 1j*(R2 @ v)
def Lmat(a):
    P = (RR @ np.outer(a, a).reshape(-1)).reshape(M, M)
    Q = 2*np.einsum('pqrs,q,r->ps', R, a.conj(), a, optimize=True)
    Qr, Qi, Pr, Pi = Q.real, Q.imag, P.real, P.imag
    return np.block([[-(Qi + Pi), -(Qr - Pr)], [(Qr + Pr), (Pi - Qi)]])
def boot(fn, X, nb=100, seed=5):
    r = np.random.default_rng(seed); n = X.shape[1]
    return float(np.std([fn(X[:, r.integers(0, n, n)]) for _ in range(nb)], ddof=1))
out = []
for n in (1e6, 1e10):
    t0 = time.time()
    I0 = np.zeros(M); a = Ep/3.; I0[groups == 1] = a/np.sum(groups == 1); I0[groups == 2] = a/np.sum(groups == 2); I0[0] = 1 - I0.sum()
    A0 = np.sqrt(I0)*np.exp(1j*np.random.default_rng(1).uniform(0, 2*np.pi, M))
    nr = np.random.default_rng(909)
    A = np.concatenate([A0[:, None], A0[:, None] + (nr.standard_normal((M, B)) + 1j*nr.standard_normal((M, B)))*np.sqrt(1/(4*n))], axis=1)
    Sm = np.eye(2*M); drng = np.random.default_rng(7); z = 0.0; ci = 0
    for step in range(1, int(round(max(CPS)/dz)) + 1):
        a0 = A[:, 0].copy()
        k1 = fA(A); s1 = Lmat(a0) @ Sm
        a1 = A + 0.5*dz*k1; k2 = fA(a1); s2 = Lmat(a1[:, 0]) @ (Sm + 0.5*dz*s1)
        a2 = A + 0.5*dz*k2; k3 = fA(a2); s3 = Lmat(a2[:, 0]) @ (Sm + 0.5*dz*s2)
        a3 = A + dz*k3; k4 = fA(a3); s4 = Lmat(a3[:, 0]) @ (Sm + dz*s3)
        A = A + dz*(k1 + 2*k2 + 2*k3 + k4)/6; Sm = Sm + dz*(s1 + 2*s2 + 2*s3 + s4)/6
        for b in blocks:
            nb = len(b); Zm = (drng.standard_normal((nb, nb)) + 1j*drng.standard_normal((nb, nb)))/2
            Hh = (Zm + Zm.conj().T)/np.sqrt(2); w_, V_ = np.linalg.eigh(Hh)
            U = (V_*np.exp(-1j*sigma*np.sqrt(dz)*w_)) @ V_.conj().T
            A[b, :] = U @ A[b, :]
            Ur, Ui = U.real, U.imag; xb, yb = Sm[b, :].copy(), Sm[M + b, :].copy()
            Sm[b, :] = Ur @ xb - Ui @ yb; Sm[M + b, :] = Ui @ xb + Ur @ yb
        z = step*dz
        if ci < len(CPS) and z >= CPS[ci] - 1e-9:
            zc = CPS[ci]; ci += 1
            ref = A[:, 0]; dA = A[:, 1:] - ref[:, None]; dx = np.vstack([dA.real, dA.imag])*np.sqrt(4*n)     # vacuum-1 units
            V = Sm @ Sm.T; w, Ev = np.linalg.eigh(V); lam_lin = w[0]; u = Ev[:, 0]
            ph = np.angle(ref); Pa = np.zeros((M, 2*M)); Pa[np.arange(M), np.arange(M)] = np.cos(ph); Pa[np.arange(M), M + np.arange(M)] = np.sin(ph)
            Va = Pa @ V @ Pa.T; wa, Ea = np.linalg.eigh(Va); lam_gen_lin = wa[0]; c = Ea[:, 0]
            Nbar = n*np.abs(ref)**2; wts = c/np.sqrt(Nbar); Np = n*np.abs(A[:, 1:])**2
            f_u = lambda X: float(np.var(u @ X, ddof=1))
            dX = Pa @ dx
            f_cq = lambda X: float(np.var(c @ X, ddof=1))
            f_num = lambda Y: float(np.var(wts @ Y, ddof=1)/np.sum(wts**2*Nbar))
            lu, lq, ln_ = f_u(dx), f_cq(dX), f_num(Np)
            Vloc = (lambda R_: R_ @ V[np.ix_([0, M], [0, M])] @ R_.T)(np.array([[np.cos(ph[0]), np.sin(ph[0])], [-np.sin(ph[0]), np.cos(ph[0])]]))
            n0 = n*np.abs(ref[0])**2; smax2 = 1/lam_lin
            rec = dict(n=n, z=zc, n0=float(n0), sigma_max2=float(smax2), lam_lin_dB=float(10*np.log10(lam_lin)), twa_u_dB=float(10*np.log10(lu)),
                       twa_u_err_dB=float(10/np.log(10)*boot(f_u, dx)/lu), crit_G2=float(smax2**3/n0),
                       lam_gen_lin_dB=float(10*np.log10(lam_gen_lin)), twa_gen_quad_dB=float(10*np.log10(lq)), twa_gen_num_dB=float(10*np.log10(ln_)),
                       twa_gen_num_err_dB=float(10/np.log(10)*boot(f_num, Np)/ln_), V_P0=float(Vloc[1, 1]), crit_G3=float(Vloc[1, 1]**2/(lam_gen_lin*n0)))
            out.append(rec)
            print(f"n={n:.0e} z={zc:4d}: lam_lin {rec['lam_lin_dB']:6.1f} dB, TWA along u_min {rec['twa_u_dB']:6.1f} +- {rec['twa_u_err_dB']:.2f} (sigma_max^6/n0 = {rec['crit_G2']:.3g}) | "
                  f"lam_gen lin {rec['lam_gen_lin_dB']:6.1f}, TWA quad {rec['twa_gen_quad_dB']:6.1f}, TWA photon-number {rec['twa_gen_num_dB']:6.1f} +- {rec['twa_gen_num_err_dB']:.2f} "
                  f"(V_P0^2/(lam n0) = {rec['crit_G3']:.3g}) | {time.time()-t0:.0f}s", flush=True)
json.dump(dict(B=B, results=out), open('twa_multimode_check.json', 'w'), indent=1)
