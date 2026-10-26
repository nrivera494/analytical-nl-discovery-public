"""Exact Kerr overlap tensor of a parabolic GRIN fibre in the Hermite-Gauss basis (one polarization, scalar),
normalized so that S_0000 = 1. Modes (nx, ny) with nx+ny = k < K; eps'_k = k."""
import numpy as np
from numpy.polynomial.hermite import hermgauss
from math import factorial, pi, sqrt
def hermite_functions(nmax, x):
    # orthonormal Hermite functions psi_n(x) = (2^n n! sqrt(pi))^{-1/2} H_n(x) e^{-x^2/2}
    psi = np.zeros((nmax+1, len(x)))
    psi[0] = pi**-0.25*np.exp(-x**2/2)
    if nmax >= 1: psi[1] = sqrt(2)*x*psi[0]
    for n in range(2, nmax+1):
        psi[n] = sqrt(2/n)*x*psi[n-1] - sqrt((n-1)/n)*psi[n-2]
    return psi
def grin_tensor(K):
    modes = [(nx, k-nx) for k in range(K) for nx in range(k+1)]
    M = len(modes); nmax = K-1
    # 1D quadruple overlaps T[a,b,c,d] = int psi_a psi_b psi_c psi_d dx, exact with Gauss-Hermite (weight e^{-2x^2} after scaling)
    xg, wg = hermgauss(4*nmax+4)
    x = xg/np.sqrt(2); w = wg/np.sqrt(2)          # int f(x) e^{-2x^2} dx with nodes for e^{-x^2}
    psi = hermite_functions(nmax, x)*np.exp(x**2/2)  # strip one Gaussian factor; product of four gives e^{-2x^2}
    T = np.einsum('ax,bx,cx,dx,x->abcd', psi, psi, psi, psi, w)
    nx = np.array([m[0] for m in modes]); ny = np.array([m[1] for m in modes])
    S = T[np.ix_(nx, nx, nx, nx)]*T[np.ix_(ny, ny, ny, ny)]
    S /= S[0, 0, 0, 0]
    groups = np.array([m[0]+m[1] for m in modes])
    return modes, groups, S
if __name__ == '__main__':
    modes, groups, S = grin_tensor(4)
    print(len(modes), 'modes; S0000 =', S[0,0,0,0], ' S0011 (fund, LP11a) =', S[0,0,1,1], ' symmetric:', np.allclose(S, S.transpose(1,0,2,3)) and np.allclose(S, S.transpose(2,1,0,3)))
    # sanity: 2D Gaussian: int phi0^4 = 1/(2 pi) in units w=1; ratio S_(10)(10)00 / S0000 should be 1/2 for HG10 vs HG00 cross overlap
    print('ratio S(HG10,HG10,00,00)/S0000 =', S[1,1,0,0], '(expected 0.5)')
