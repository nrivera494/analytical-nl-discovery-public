"""Is the photon-counting-optimal weight vector in the span of conserved-quantity gradients?
At checkpoints, compute u (min eigvec of V_amp) and the amplitude-quadrature projections of grad N, grad E', grad H_res
(gradients w.r.t. (x, y) quadratures, projected onto the local amplitude directions). Report the fraction of |u|^2 in their span,
and lambda_gen restricted to that span vs its orthogonal complement."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
def run(K=5, Eprime=0.6, sigma=0.3, zmax=400., dz=0.02, cps=(10, 50, 100, 200, 400), phase_seed=1, dis_seed=7):
    groups, eps, _, S4, R = gm.build(K, 0, 0)
    M = len(groups); R2 = R.reshape(M, -1); RR = R.reshape(M*M, M*M)
    I0 = np.zeros(M); a = Eprime/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    A = np.sqrt(I0)*np.exp(1j*np.random.default_rng(phase_seed).uniform(0, 2*np.pi, M)); Sm = np.eye(2*M)
    drng = np.random.default_rng(dis_seed); blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
    def fA(A):
        v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)
    def L(A):
        P = (RR @ np.outer(A, A).reshape(-1)).reshape(M, M); Q = 2*np.einsum('pqrs,q,r->ps', R, A.conj(), A, optimize=True)
        return np.block([[-(Q.imag+P.imag), -(Q.real-P.real)], [(Q.real+P.real), (P.imag-Q.imag)]])
    out = []; ci = 0
    for n in range(1, int(round(zmax/dz))+1):
        k1 = (fA(A), L(A) @ Sm); k2 = (fA(A+0.5*dz*k1[0]), L(A+0.5*dz*k1[0]) @ (Sm+0.5*dz*k1[1]))
        k3 = (fA(A+0.5*dz*k2[0]), L(A+0.5*dz*k2[0]) @ (Sm+0.5*dz*k2[1])); k4 = (fA(A+dz*k3[0]), L(A+dz*k3[0]) @ (Sm+dz*k3[1]))
        A = A + dz*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6; Sm = Sm + dz*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        if sigma > 0:
            for b in blocks:
                nb = len(b); Z = (drng.standard_normal((nb,nb)) + 1j*drng.standard_normal((nb,nb)))/2
                Hh = (Z + Z.conj().T)/np.sqrt(2); w_, V_ = np.linalg.eigh(Hh); U = (V_*np.exp(-1j*sigma*np.sqrt(dz)*w_)) @ V_.conj().T
                A[b] = U @ A[b]; xb, yb = Sm[b, :].copy(), Sm[M+b, :].copy()
                Sm[b, :] = U.real @ xb - U.imag @ yb; Sm[M+b, :] = U.imag @ xb + U.real @ yb
        z = n*dz
        if ci < len(cps) and z >= cps[ci] - 1e-9:
            ci += 1
            V = Sm @ Sm.T/2; ph = np.angle(A); I = np.abs(A)**2
            Pa = np.zeros((M, 2*M)); Pa[np.arange(M), np.arange(M)] = np.cos(ph); Pa[np.arange(M), M+np.arange(M)] = np.sin(ph)
            Va = Pa @ V @ Pa.T; ev, U_ = np.linalg.eigh(Va); u = U_[:, 0]
            # gradients (amplitude projections): N -> 2|A_p|, E' -> 2 eps_p |A_p|, H_res -> 2 Re(e^{-i phi_p} dH/dA_p^*) with dH/dA^* = sum R A* A A
            gN = 2*np.sqrt(I); gE = 2*eps*np.sqrt(I)
            dH = (R2 @ np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1)); gH = 2*np.real(np.exp(-1j*ph)*dH)
            Bm = np.stack([gN, gE, gH], 1); Qb, _ = np.linalg.qr(Bm)
            frac = float(np.sum((Qb.T @ u)**2))
            # best Fano within the span and within its orthogonal complement
            Vs = Qb.T @ Va @ Qb; lam_span = 2*np.linalg.eigvalsh(Vs)[0]
            Pc = np.eye(M) - Qb @ Qb.T; Uc, sc, _ = np.linalg.svd(Pc); Bc = Uc[:, :M-3]
            lam_comp = 2*np.linalg.eigvalsh(Bc.T @ Va @ Bc)[0]
            out.append(dict(z=z, lam_gen=float(2*ev[0]), frac_in_span=frac, lam_span=float(lam_span), lam_complement=float(lam_comp)))
            print(f"z={z:.0f}: lam_gen={10*np.log10(2*ev[0]):.1f} dB; |u|^2 in span(N,E',H_res)={frac:.3f}; best in span {10*np.log10(lam_span):.1f} dB; best in complement {10*np.log10(lam_comp):.1f} dB", flush=True)
    return out
if __name__ == '__main__':
    res = {}
    for sig in [0.3, 0.0]:
        print('sigma', sig); res[str(sig)] = run(sigma=sig)
    json.dump(res, open('gauss_structure.json', 'w'), indent=1)
