"""Minimal model for the photon-counting squeezing: 1D Hermite-Gauss ladder modes (0, 1, 2) with exact overlaps (x-only,
y in the ground state), resonant dynamics (process 0 + 2 <-> 1 + 1 plus SPM/XPM). Linearized state from the tangent map;
lambda_gen(z) = 2 lambda_min(V_amp). Launch: I = (1 - a - b, a, b) with given phases."""
import numpy as np, json, sys
from grin_overlaps import hermite_functions
from numpy.polynomial.hermite import hermgauss
def tensor1d(nmax):
    xg, wg = hermgauss(4*nmax+8); x = xg/np.sqrt(2); w = wg/np.sqrt(2)
    psi = hermite_functions(nmax, x)*np.exp(x**2/2)
    T = np.einsum('ax,bx,cx,dx,x->abcd', psi, psi, psi, psi, w)
    return T/T[0, 0, 0, 0]
def run(I0, ph0, zs=(1, 2, 5, 10, 20, 50, 100, 200, 400, 800), dz=0.01, modes=(0, 1, 2)):
    T = tensor1d(max(modes)); idx = np.array(modes); S = T[np.ix_(idx, idx, idx, idx)]
    eps = idx.astype(float); M = len(idx)
    res = (eps[:,None,None,None] + eps[None,:,None,None]) == (eps[None,None,:,None] + eps[None,None,None,:])
    R = np.where(res, S, 0.0); R2 = R.reshape(M, -1); RR = R.reshape(M*M, M*M)
    A = np.sqrt(np.array(I0, float))*np.exp(1j*np.array(ph0, float)); Sm = np.eye(2*M)
    def fA(A):
        v = np.multiply.outer(np.multiply.outer(A.conj(), A), A).reshape(-1); return 1j*(R2 @ v)
    def L(A):
        P = (RR @ np.outer(A, A).reshape(-1)).reshape(M, M); Q = 2*np.einsum('pqrs,q,r->ps', R, A.conj(), A)
        return np.block([[-(Q.imag+P.imag), -(Q.real-P.real)], [(Q.real+P.real), (P.imag-Q.imag)]])
    out = []; zi = 0; zs = sorted(zs)
    for n in range(1, int(round(max(zs)/dz))+1):
        k1 = (fA(A), L(A) @ Sm); k2 = (fA(A+0.5*dz*k1[0]), L(A+0.5*dz*k1[0]) @ (Sm+0.5*dz*k1[1]))
        k3 = (fA(A+0.5*dz*k2[0]), L(A+0.5*dz*k2[0]) @ (Sm+0.5*dz*k2[1])); k4 = (fA(A+dz*k3[0]), L(A+dz*k3[0]) @ (Sm+dz*k3[1]))
        A = A + dz*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6; Sm = Sm + dz*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
        z = n*dz
        if zi < len(zs) and z >= zs[zi] - 1e-9:
            zi += 1
            V = Sm @ Sm.T/2; ph = np.angle(A); I = np.abs(A)**2
            Pa = np.zeros((M, 2*M)); Pa[np.arange(M), np.arange(M)] = np.cos(ph); Pa[np.arange(M), M+np.arange(M)] = np.sin(ph)
            Va = Pa @ V @ Pa.T; ev, U = np.linalg.eigh(Va)
            out.append(dict(z=z, lam_gen=float(2*ev[0]), I=I.tolist(), weights=(U[:, 0]/np.sqrt(np.maximum(I, 1e-12))).tolist(),
                            mm=float(1/(2*np.linalg.svd(Sm, compute_uv=False)[0]**2)/0.5)))
    return out
if __name__ == '__main__':
    for I0 in [(0.8, 0.1, 0.1), (0.6, 0.2, 0.2), (0.9, 0.05, 0.05)]:
        o = run(I0, (0.3, 1.1, 2.0))
        print('I0', I0, ' '.join(f"z={r['z']:.0f}:{10*np.log10(r['lam_gen']):.1f}dB" for r in o))
