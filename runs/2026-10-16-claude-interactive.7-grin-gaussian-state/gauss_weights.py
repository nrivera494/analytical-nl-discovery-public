"""Structure of the optimal photon-counting weights in the linearized state (GRIN K=5, E'=0.6, sigma=0.3 and 0).
At checkpoints: the eigenvector u of V_amp with the smallest eigenvalue -> weights w_p = u_p/sqrt(I_p) on mode photon numbers.
Report the share of |u|^2 per group, the share carried by within-group differences (orthogonal to the group-uniform vector),
and the overlap with the conserved directions (total N: u ~ sqrt(I); E': u ~ eps sqrt(I))."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import gauss_state as gs, grin_model as gm

def analyze(Eprime, sigma, zmax=400., checkpoints=(10, 50, 100, 200, 400)):
    # rerun the integration but keep S and A at checkpoints
    groups, eps, _, S4, R = gm.build(5, 0, 0)
    M = len(groups)
    out = []
    o = gs.run(Eprime=Eprime, sigma=sigma, zmax=zmax, checkpoints=checkpoints)
    return o
# gauss_state.run does not return S; re-implement minimal extraction by monkeypatching: simpler to copy the loop
import types
def run_keep(K=5, Eprime=0.6, sigma=0.3, zmax=400., dz=0.02, checkpoints=(10, 50, 100, 200, 400), phase_seed=1, dis_seed=7):
    groups, eps, _, S4, R = gm.build(K, 0, 0)
    M = len(groups); R2 = R.reshape(M, -1); RR = R.reshape(M*M, M*M)
    rng = np.random.default_rng(phase_seed)
    I0 = np.zeros(M); a = Eprime/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    A = np.sqrt(I0)*np.exp(1j*rng.uniform(0, 2*np.pi, M)); Smat = np.eye(2*M)
    drng = np.random.default_rng(dis_seed); blocks = [np.where(groups==k)[0] for k in range(K) if np.sum(groups==k) > 1]
    def fA(A):
        v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)
    def Lmat(A):
        P = (RR @ np.outer(A, A).reshape(-1)).reshape(M, M); Q = 2*np.einsum('pqrs,q,r->ps', R, A.conj(), A, optimize=True)
        return np.block([[-(Q.imag+P.imag), -(Q.real-P.real)], [(Q.real+P.real), (P.imag-Q.imag)]])
    res = []; cps = sorted(checkpoints); ci = 0
    for n in range(1, int(round(zmax/dz))+1):
        k1 = (fA(A), Lmat(A) @ Smat); k2 = (fA(A+0.5*dz*k1[0]), Lmat(A+0.5*dz*k1[0]) @ (Smat+0.5*dz*k1[1]))
        k3 = (fA(A+0.5*dz*k2[0]), Lmat(A+0.5*dz*k2[0]) @ (Smat+0.5*dz*k2[1])); k4 = (fA(A+dz*k3[0]), Lmat(A+dz*k3[0]) @ (Smat+dz*k3[1]))
        A = A + dz*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6; Smat = Smat + dz*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        if sigma > 0:
            for b in blocks:
                nb = len(b); Z = (drng.standard_normal((nb,nb)) + 1j*drng.standard_normal((nb,nb)))/2
                Hh = (Z + Z.conj().T)/np.sqrt(2); w_, V_ = np.linalg.eigh(Hh); U = (V_*np.exp(-1j*sigma*np.sqrt(dz)*w_)) @ V_.conj().T
                A[b] = U @ A[b]; xb, yb = Smat[b, :].copy(), Smat[M+b, :].copy()
                Smat[b, :] = U.real @ xb - U.imag @ yb; Smat[M+b, :] = U.imag @ xb + U.real @ yb
        z = n*dz
        if ci < len(cps) and z >= cps[ci] - 1e-9:
            ci += 1
            V = Smat @ Smat.T/2; I = np.abs(A)**2; ph = np.angle(A)
            Pa = np.zeros((M, 2*M)); Pa[np.arange(M), np.arange(M)] = np.cos(ph); Pa[np.arange(M), M+np.arange(M)] = np.sin(ph)
            Vamp = Pa @ V @ Pa.T; ev, U_ = np.linalg.eigh(Vamp); u = U_[:, 0]
            share = [float(np.sum(u[groups==k]**2)) for k in range(K)]
            within = float(sum(np.sum((u[groups==k] - u[groups==k].mean())**2) for k in range(K)))
            nN = np.sqrt(I)/np.linalg.norm(np.sqrt(I)); nE = eps*np.sqrt(I); nE = nE/np.linalg.norm(nE) if np.linalg.norm(nE) > 0 else nE
            res.append(dict(z=z, lam_gen=float(2*ev[0]), second=float(2*ev[1]), third=float(2*ev[2]), group_share=[round(x, 3) for x in share],
                            within_group_share=round(within, 3), overlap_N=round(float(abs(u @ nN)), 3), overlap_E=round(float(abs(u @ nE)), 3),
                            n_below_shot=int(np.sum(2*ev < 1.0))))
    return res
if __name__ == '__main__':
    out = {}
    for sig in [0.3, 0.0]:
        r = run_keep(sigma=sig); out[str(sig)] = r
        for x in r: print(f"sigma={sig} z={x['z']:.0f} lam_gen={x['lam_gen']:.4f} next={x['second']:.4f},{x['third']:.4f} #below_shot={x['n_below_shot']} groups={x['group_share']} within={x['within_group_share']} ovN={x['overlap_N']} ovE={x['overlap_E']}")
    json.dump(out, open('gauss_weights.json', 'w'), indent=1)
