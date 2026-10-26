"""Reduced (leading-order hydrodynamic, Legendre-separated) matched-LO covariance of the
amplifier similariton with distributed ASE.  Written by claude-interactive.13 for the
verification of C-20261019-pi-chatgpt-02, parts (i) and (iii).

Model (normalized units of C-20261008-claude-a-01/-02, re-derived in the audit report):
  background  a'' = 2 e^{Gamma zeta} / a^2,  rho0 = e^{Gamma zeta}/a,  theta = int rho0 dzeta
  blocks      dp_l/dzeta = rho0 q_l,  dq_l/dzeta = -l(l+1)/a^2 p_l,   q_l = n_l/eps0
  noise       intensity quadrature only; scaled covariance S = N0 eps0^2 Cov,
              dS_{q_l q_m}/dtau = (2l+1)(2m+1) B_lm/3 * (2 n_sp - 1) e^{-tau},
              S_{q_l q_m}(0)  = (2l+1)(2m+1) B_lm/3,      B_lm = int (1-xi^2) P_l P_m.
State y = (q0, r0, p2, q2) with r0 = p0 - theta q0 (dr0 = -theta dW0), so that the
energy-locked part theta*q0 is carried analytically and 1-r^2 has no cancellation.
Matched LO:  pbar = p0 - p2/5 = theta q0 + r0 - p2/5,
  C_AA = (9/4) G S_qq,  eps0 C_AP = 3 G S_{q pbar},  eps0^2 C_PP = 4 G S_{pbar pbar}.
Variable: tau = Gamma zeta = ln G.
"""
import numpy as np
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss

xg, wg = leggauss(40)


def P(l, x):
    return {0: np.ones_like(x), 2: 0.5 * (3 * x**2 - 1)}[l]


B = np.array([[np.sum(wg * (1 - xg**2) * P(l, xg) * P(m, xg)) for m in (0, 2)] for l in (0, 2)])
W = np.array([[(2 * l + 1) * (2 * m + 1) / 3.0 for m in (0, 2)] for l in (0, 2)]) * B  # source matrix for (q0, q2)


def rhs(tau, Y, Gam, src_in):
    """Y = [a, da/dtau, theta, S (4x4 flattened)].  src_in: 1 -> pure input run (no ASE), 0 -> ASE part."""
    a, ap, th = Y[0], Y[1], Y[2]
    S = Y[3:].reshape(4, 4)
    e = np.exp(tau)
    app = 2 * e / (Gam**2 * a**2)
    rho0 = e / a
    dth = rho0 / Gam  # dtheta/dtau
    A = np.zeros((4, 4))
    A[2, 3] = rho0 / Gam          # dp2/dtau
    A[3, 2] = -6.0 / (Gam * a**2)  # dq2/dtau
    dS = A @ S + S @ A.T
    if not src_in:
        L = np.array([[1, 0], [-th, 0], [0, 0], [0, 1]], float)
        dS = dS + np.exp(-tau) * (L @ W @ L.T)
    return np.concatenate([[ap, app, dth], dS.ravel()])


def run(Gam, a0=1.0, ap0_zeta=0.0, taus=None, rtol=1e-12):
    """Return dict of (in, ase) covariance parts on the grid taus. ap0_zeta = da/dzeta at launch."""
    taus = np.asarray(taus)
    out = {}
    for part, flag in (("in", 1), ("ase", 0)):
        S0 = np.zeros((4, 4))
        if flag:
            L0 = np.array([[1, 0], [0, 0], [0, 0], [0, 1]], float)  # theta=0 at launch, r0=p0=0 (phase noise dropped)
            S0 = L0 @ W @ L0.T
        Y0 = np.concatenate([[a0, ap0_zeta / Gam, 0.0], S0.ravel()])
        sol = solve_ivp(rhs, (0, taus[-1]), Y0, t_eval=taus, args=(Gam, flag), method="DOP853",
                        rtol=rtol, atol=1e-18)
        assert sol.success, sol.message
        out[part] = sol.y
    return out


def lo_quantities(out, taus, nsp, eps0=None):
    Y = out["in"] + (2 * nsp - 1) * out["ase"]
    Y[:3] = out["in"][:3]
    a, th = Y[0], Y[2]
    S = Y[3:].reshape(4, 4, -1)
    G = np.exp(taus)
    # pbar = th*q0 + r0 - p2/5 ; components in basis (q0, r0, p2, q2)
    c = np.zeros((4, len(taus)))
    c[0] = th; c[1] = 1.0; c[2] = -0.2
    d = np.zeros((4, len(taus)))  # residual part r0 - p2/5
    d[1] = 1.0; d[2] = -0.2
    Sqq = S[0, 0]
    Sqp = np.einsum("it,it->t", S[0], c)
    Spp = np.einsum("it,ijt,jt->t", c, S, c)
    Sdd = np.einsum("it,ijt,jt->t", d, S, d)
    Sqd = np.einsum("it,it->t", S[0], d)
    var_cond = Sdd - Sqd**2 / Sqq           # Var(pbar | q0) * N0 eps0^2
    one_m_r2 = var_cond / Spp
    CAA = 2.25 * G * Sqq
    e2CPP = 4 * G * Spp
    lam_lead = CAA * one_m_r2               # eps0 -> 0 limit of lambda_min(C_LO)
    res = dict(tau=taus, a=a, theta=th, CAA=CAA, e2CPP=e2CPP, one_m_r2=one_m_r2, lam_lead=lam_lead,
               ratio_i=9 * Spp / (8 * nsp * th**2))
    if eps0 is not None:
        CPP = e2CPP / eps0**2
        CAP = 3 * G * Sqp / eps0
        det = CAA * CPP - CAP**2
        det_alt = 9 * G**2 / eps0**2 * Sqq * var_cond  # same, without cancellation
        tr = CAA + CPP
        res["lam_eps"] = 2 * det_alt / (tr + np.sqrt(tr**2 - 4 * det_alt))
        res["PhiNL2_over_N0_times_N0"] = (th / eps0) ** 2  # Phi_NL^2 (divide by N0)
    return res


if __name__ == "__main__":
    import json, sys
    taus = np.array([2.0, 4.0, 6.0])
    o = run(np.sqrt(18.0), taus=taus)
    for part in ("in", "ase"):
        r = lo_quantities({"in": o["in"], "ase": o["ase"]} if part == "in" else o, taus, 1.0)
    # parts separately for the table of C-20261008-claude-a-02 P4
    Gm = np.exp(taus)
    for part in ("in", "ase"):
        Y = o[part]
        S = Y[3:].reshape(4, 4, -1)
        th = o["in"][2]
        c = np.zeros((4, 3)); c[0] = th; c[1] = 1; c[2] = -0.2
        Spp = np.einsum("it,ijt,jt->t", c, S, c)
        print(part, "eps0^2 C_PP / G =", 4 * Spp)
    r = lo_quantities(o, taus, 1.0)
    print("1-r^2 (nsp=1):", r["one_m_r2"])
    print("a_L:", r["a"], "theta_L:", r["theta"])
