#!/usr/bin/env python3
# agent: claude-interactive.20; model: claude-opus-5-5; family: claude. Task T-20261019-claude-interactive.20-01.
# Re-derivation check for the manuscript (not a run; no simulation beyond a seconds-long reduced-model integration).
# Small independent check (claude-interactive.20): leading-order Legendre covariance on the similariton
# asymptote, l = 0..4, intensity-quadrature vacuum + ASE (phase quadrature dropped, as in the reduced model).
import numpy as np
from numpy.polynomial import legendre as Lg
from scipy.integrate import solve_ivp
Gam, eps, nsp = np.sqrt(18.), 0.05, 1.0
A = (18/Gam**2)**(1/3)
lmax = 4; ls = np.arange(lmax+1); Lv = ls*(ls+1)
# B_lm = int (1-x^2) P_l P_m ; vacuum covariance of n_l per unit 1/N: (2l+1)(2m+1)/3 B_lm
xg, wg = Lg.leggauss(40)
P = np.array([Lg.legval(xg, np.eye(lmax+1)[k]) for k in ls])
Bm = (P*(1-xg**2)*wg) @ P.T
S = np.outer(2*ls+1, 2*ls+1)/3*Bm
m = lmax+1
def drift(t):
    M = np.zeros((2*m, 2*m))
    # n_l' = -eps L p_l /(Gam A^2 e^{2t/3});  p_l' = e^{2t/3} n_l/(Gam A eps)
    M[:m, m:] = np.diag(-eps*Lv/(Gam*A**2*np.exp(2*t/3)))
    M[m:, :m] = np.eye(m)*np.exp(2*t/3)/(Gam*A*eps)
    return M
def rhs(t, y):
    C = y.reshape(2*m, 2*m); M = drift(t)
    D = np.zeros((2*m, 2*m)); D[:m, :m] = (2*nsp-1)*np.exp(-t)*S
    return (M@C + C@M.T + D).ravel()
C0 = np.zeros((2*m, 2*m)); C0[:m, :m] = S
taus = np.linspace(0, 30, 3001)
# integrate in rescaled variables to keep conditioning: use (u, w) = (e^{t/3} n, eps e^{-t/3} p)
def rhs_uw(t, y):
    C = y.reshape(2*m, 2*m)
    M = np.zeros((2*m, 2*m)); M[:m, :m] = np.eye(m)/3; M[m:, m:] = -np.eye(m)/3
    M[:m, m:] = np.diag(-Lv/(Gam*A**2)); M[m:, :m] = np.eye(m)/(Gam*A)
    D = np.zeros((2*m, 2*m)); D[:m, :m] = (2*nsp-1)*np.exp(-t/3)*S
    return (M@C + C@M.T + D).ravel()
sol = solve_ivp(rhs_uw, (0, 30), C0.ravel(), t_eval=taus, method='DOP853', rtol=1e-11, atol=1e-14)
out = []
for t, y in zip(sol.t, sol.y.T):
    Cuw = y.reshape(2*m, 2*m)
    T = np.diag(np.r_[np.exp(-t/3)*np.ones(m), np.exp(t/3)/eps*np.ones(m)])   # (n, p) = T (u, w)
    C = T@Cuw@T
    G = np.exp(t)
    n, p = slice(0, m), slice(m, 2*m)
    Vn2, Vp2 = C[2, 2], C[m+2, m+2]
    # spectral s_l = n_l + 3 n_l,tau = n_l - 3 eps L p_l/(Gam A^2 e^{2t/3})
    R = np.hstack([np.eye(m), np.diag(-3*eps*Lv/(Gam*A**2*np.exp(2*t/3)))])
    Cs = R@C@R.T; W = np.sqrt(2/(2*ls+1)); CL2 = W[:, None]*Cs*W[None, :]
    mu = np.sort(np.linalg.eigvalsh(CL2))[::-1]
    a0 = np.zeros(2*m); a0[0] = 1
    pb = np.zeros(2*m); pb[m] = 1; pb[m+2] = -1/5
    vn, vp, cr = a0@C@a0, pb@C@pb, a0@C@pb
    Nout = G  # N0 = 1
    CAA, CPP, CAP = 9/4*Nout*vn, 4*Nout*vp, 3*Nout*cr
    def1 = 1 - cr**2/(vn*vp)
    Phi = 3/(2*Gam*A*eps)*(np.exp(2*t/3)-1)
    det = CAA*CPP*def1; tr = CAA+CPP; lmax_ = 0.5*(tr+np.sqrt(tr*tr-4*det)); lmin = det/lmax_
    out.append((t, Nout*Vn2, eps**2*Nout*Vp2, mu[1]/mu[0], def1, CAA, CPP/((32*nsp/9)*G*Phi**2), lmin*G**(-1/3)))
out = np.array(out)
def fit(col, a, b):
    s = (out[:, 0] >= a) & (out[:, 0] <= b)
    return np.polyfit(out[s, 0], np.log(out[s, col]), 1)[0]
print('exponents 12-26: N Var n2 %.5f, eps2 N Var p2 %.5f, mu2/mu1 %.5f, 1-r2 %.5f' % (fit(1, 12, 26), fit(2, 12, 26), fit(3, 12, 26), fit(4, 12, 26)))
for tt in (4, 12, 15, 18):
    k = np.argmin(abs(out[:, 0]-tt)); print('tau=%g: mu2/mu1=%.7g  1-r2=%.7g  CAA=%.6f (exact %.6f)  CPP ratio=%.5f  G^-1/3 lmin=%.4f' % (tt, out[k, 3], out[k, 4], out[k, 5], 2*nsp*np.exp(tt)-(2*nsp-1), out[k, 6], out[k, 7]))
s = (out[:, 0] >= 12) & (out[:, 0] <= 26)
print('G^-1/3 lambda_min range 12-26: [%.4f, %.4f]' % (out[s, 7].min(), out[s, 7].max()))
print('CPP ratio range 12-26: [%.5f, %.5f]' % (out[s, 6].min(), out[s, 6].max()))
Gc = np.exp(out[:, 0]); cpp_e2 = out[:, 6]*(32*nsp/9)*Gc*(3/(2*Gam*A)*(np.exp(2*out[:, 0]/3)-1))**2  # eps^2 CPP
print('power of eps^2 CPP over 12-26: %.5f' % np.polyfit(out[s, 0], np.log(cpp_e2[s]), 1)[0])
