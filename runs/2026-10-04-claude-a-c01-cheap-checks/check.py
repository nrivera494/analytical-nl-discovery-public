#!/usr/bin/env python3
"""Cheap checks and frozen predictions for claim C-20261004-claude-a-01.

Model: dispersionless (hydrodynamic) limit of the normal-dispersion NLSE,
    i eps psi_s = -(eps^2/2) psi_xx + |psi|^2 psi   (complex conjugate of the Agrawal form),
linearized about the passively expanding parabola rho = (1 - x^2/a^2)/a, v = x a'/a, a'' = 2/a^2.
Comoving coordinate xi = x/a(s).  Unit orbit: a = cosh^2(theta), s = theta/2 + sinh(2 theta)/4, mu = tanh(theta).

Block l (Legendre P_l(xi)) in the variables (p_l, n_l/eps):
    p = physical phase perturbation (rad), n = Legendre coefficient of (1 - xi^2) * nu, nu = delta rho / rho,
    dp/dtheta = n/eps,  dn/dtheta = -eps l(l+1) sech^2(theta) p.
Fundamental matrix Phi_l(mu) = [[P_l, Q_l], [(1-mu^2) P_l', (1-mu^2) Q_l']], det = 1.

Nothing here runs the NLSE solver.  Sections A are symbolic (sympy), sections B numeric (mpmath / numpy).
Usage: python check.py <output_dir>
"""
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

T_START = time.time()
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT.mkdir(parents=True, exist_ok=True)
mp.mp.dps = 30
RES = {"checks": {}, "predictions": {}}


def record(name, ok, detail):
    RES["checks"][name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ---------------------------------------------------------------- A. symbolic
s, x = sp.symbols("s x", real=True)
th = sp.symbols("theta", real=True)
a = sp.Function("a")(s)
add = {sp.Derivative(a, (s, 2)): 2 / a**2}
rho = (1 - x**2 / a**2) / a
v = x * a.diff(s) / a

# A1 background solves the dispersionless equations; unit-orbit parametrization.
r1 = sp.simplify((rho.diff(s) + (rho * v).diff(x)).subs(add))
r2 = sp.simplify((v.diff(s) + v * v.diff(x) + rho.diff(x)).subs(add))
a_th = sp.cosh(th) ** 2
s_th = th / 2 + sp.sinh(2 * th) / 4
ds = sp.diff(s_th, th)
adot = sp.diff(a_th, th) / ds
addot = sp.diff(adot, th) / ds
c1 = sp.simplify(ds - sp.cosh(th) ** 2)
c2 = sp.simplify(addot - 2 / a_th**2)
c3 = sp.simplify(adot - 2 * sp.tanh(th))
c4 = sp.simplify(adot**2 - 4 * (1 - 1 / a_th))
record("A1_background_residual", all(e == 0 for e in (r1, r2, c1, c2, c3, c4)),
       f"continuity {r1}, momentum {r2}; a=cosh^2, s=theta/2+sinh(2theta)/4: ds/dtheta-a={c1}, "
       f"a''-2/a^2={c2}, a'-2tanh={c3}, a'^2-4(1-1/a)={c4}; theta = int ds/a since (ds/dtheta)/a = 1")

# A2 linearized hydrodynamics separates in Legendre polynomials of xi = x/a.
f = sp.Function("f")(s)
g = sp.Function("g")(s)
ok_sep = True
for l in range(0, 7):
    P = sp.legendre(l, x / a)
    drho = f * P / a          # delta rho = n/a with n = f(s) P_l(xi)
    phi = g * P               # hydrodynamic phase perturbation (delta S)
    R1 = drho.diff(s) + (rho * phi.diff(x) + v * drho).diff(x)
    R2 = phi.diff(s) + v * phi.diff(x) + drho
    e1 = sp.simplify(sp.expand(R1 - (f.diff(s) - l * (l + 1) * g / a**2) * P / a))
    e2 = sp.simplify(sp.expand(R2 - (g.diff(s) + f / a) * P))
    ok_sep &= (e1 == 0 and e2 == 0)
record("A2_legendre_separation", ok_sep,
       "for l=0..6: continuity -> n_l' = l(l+1) phi_l / a^2 and Bernoulli -> phi_l' = -n_l / a exactly")


# A3 block equation phi'' + l(l+1) sech^2 phi = 0 solved by P_l(tanh), Q_l(tanh).
def Qsym(l, z):
    W = sum(sp.Rational(1, k) * sp.legendre(k - 1, z) * sp.legendre(l - k, z) for k in range(1, l + 1))
    return sp.legendre(l, z) * sp.atanh(z) - W


ok_pt = True
for l in range(0, 7):
    for F in (sp.legendre(l, sp.tanh(th)), Qsym(l, sp.tanh(th))):
        res = sp.simplify(sp.diff(F, th, 2) + l * (l + 1) * sp.sech(th) ** 2 * F)
        ok_pt &= (res == 0)
record("A3_poschl_teller_residual", ok_pt,
       "P_l(tanh theta) and Q_l(tanh theta) solve phi'' + l(l+1) sech^2(theta) phi = 0 for l=0..6")

# A4 symmetry-generated solutions agree with the Legendre functions.
mu_t = sp.tanh(th)
transl = sp.simplify(adot - 2 * sp.legendre(1, mu_t))
boost = sp.simplify(((a_th - s_th * adot) + Qsym(1, mu_t)).replace(sp.atanh(sp.tanh(th)), th).rewrite(sp.exp))
ttrans = sp.simplify((1 - sp.Rational(3, 2) / a_th) - sp.legendre(2, mu_t))
pw = (a_th * adot + 6 * s_th / a_th - 4 * s_th) / 6           # power-scaling solution of the l=2 block
pw_res = sp.simplify(sp.diff(pw, th, 2) + 6 * sp.sech(th) ** 2 * pw)
record("A4_symmetry_solutions", all(e == 0 for e in (transl, boost, ttrans, pw_res)),
       f"translation=2P_1 ({transl}), Galilean boost=-Q_1 ({boost}), time shift=P_2 ({ttrans}), "
       f"peak-power scaling solves l=2 block ({pw_res})")

# A5 linearized conservation laws (hydrodynamic phase convention phi, d phi/dtheta = -n, dn/dtheta = l(l+1) sech^2 phi).
m = sp.symbols("mu")
n0, n1, f1, n2, f2 = sp.symbols("n0 n1 phi1 n2 phi2")
rules = {n0: 0, n1: 2 * (1 - m**2) * f1, f1: -n1, n2: 6 * (1 - m**2) * f2, f2: -n2, m: 1 - m**2}


def ddtheta(expr):
    return sum(sp.diff(expr, q) * rules[q] for q in rules)


dP = m * n1 + (1 - m**2) * f1                                   # momentum (mean frequency)
dH = (2 * m**2 * (sp.Rational(2, 3) * n0 + sp.Rational(4, 15) * n2)
      + (1 - m**2) * (sp.Rational(4, 3) * n0 - sp.Rational(4, 15) * n2)
      + sp.Rational(8, 5) * m * (1 - m**2) * f2)                 # first variation of H = int(rho v^2/2 + rho^2/2)
cP = sp.simplify(ddtheta(dP))
cH = sp.simplify(ddtheta(dH))
record("A5_conservation_laws", cP == 0 and cH == 0,
       f"d/dtheta of: energy n0 -> 0 (l=0 block), momentum -> {cP}, linearized Hamiltonian -> {cH}")

# A6 units of the dimensionless groups.
from sympy.physics import units as u
z_, T0_, P0_, b2_, gam_, hw_ = u.meter, u.second, u.watt, u.second**2 / u.meter, 1 / (u.watt * u.meter), u.joule
groups = {
    "zeta = z sqrt(gamma P0 beta2)/T0": z_ * sp.sqrt(gam_ * P0_ * b2_) / T0_,
    "eps = sqrt(beta2/(gamma P0 T0^2))": sp.sqrt(b2_ / (gam_ * P0_ * T0_**2)),
    "n0 = P0 T0/(hbar omega0)": P0_ * T0_ / hw_,
    "Phi_NL = gamma P0 z": gam_ * P0_ * z_,
}
dims = {k: str(sp.simplify(u.convert_to(e, [u.meter, u.second, u.kilogram]))) for k, e in groups.items()}
record("A6_units", all(d == "1" for d in dims.values()), f"all groups dimensionless: {dims}")


# ---------------------------------------------------------------- B. numeric
def PQ(l, z):
    """Ferrers P_l, Q_l and derivatives on (-1, 1) via recurrences in mpmath."""
    z = mp.mpf(z)
    P = [mp.mpf(1), z]
    Q = [mp.atanh(z), z * mp.atanh(z) - 1]
    for k in range(1, l):
        P.append(((2 * k + 1) * z * P[k] - k * P[k - 1]) / (k + 1))
        Q.append(((2 * k + 1) * z * Q[k] - k * Q[k - 1]) / (k + 1))
    if l == 0:
        return P[0], Q[0], mp.mpf(0), 1 / (1 - z**2)
    dP = l * (P[l - 1] - z * P[l]) / (1 - z**2)
    dQ = l * (Q[l - 1] - z * Q[l]) / (1 - z**2)
    return P[l], Q[l], dP, dQ


def Phi(l, mu):
    P, Q, dP, dQ = PQ(l, mu)
    w = 1 - mp.mpf(mu) ** 2
    return mp.matrix([[P, Q], [w * dP, w * dQ]])


def M(l, mu, mu0):
    """Block propagator for (p_l, n_l/eps_tilde) from mu0 to mu."""
    return Phi(l, mu) * mp.inverse(Phi(l, mu0))


def theta_of_s(s_val):
    return mp.findroot(lambda t: t / 2 + mp.sinh(2 * t) / 4 - s_val, (0, 6), solver='illinois')


def s_of_theta(t):
    return t / 2 + mp.sinh(2 * t) / 4


# B1 zero-length identity, B2 symplecticity and composition.
err_id = max(abs(x_) for l in range(0, 11) for mu0 in (0, -0.5, 0.3) for x_ in (M(l, mu0, mu0) - mp.eye(2)))
err_det = max(abs(mp.det(M(l, mu, mu0)) - 1) for l in range(0, 11) for mu0 in (0, -0.5)
              for mu in (-0.4, 0.1, 0.5, 0.9, 0.99))
err_comp = max(abs(x_) for l in range(0, 11)
               for x_ in (M(l, 0.9, 0.2) * M(l, 0.2, -0.5) - M(l, 0.9, -0.5)))
record("B1_zero_length_identity", err_id < 1e-20, f"max |M_l(mu0,mu0) - I| = {mp.nstr(err_id, 3)} (l<=10)")
record("B2_symplectic_and_group_law", err_det < 1e-15 and err_comp < 1e-15,
       f"max |det M_l - 1| = {mp.nstr(err_det, 3)}, max composition error = {mp.nstr(err_comp, 3)} (l<=10)")

# B3 independent check: integrate the block ODE in s directly (not in theta), compare with Legendre propagator.
from scipy.integrate import solve_ivp


def block_rhs(s_val, y, lam):
    # y = [a, adot, p, n/eps]; d p/ds = (n/eps)/a ; d(n/eps)/ds = -lam p / a^2
    aa, ad, p_, q_ = y
    return [ad, 2 / aa**2, q_ / aa, -lam * p_ / aa**2]


err_ode = 0.0
for l in range(0, 7):
    for y0 in ([1, 0], [0, 1]):
        sol = solve_ivp(block_rhs, (0, 6.0), [1.0, 0.0, *y0], args=(l * (l + 1),), rtol=1e-12, atol=1e-13)
        aa, ad, p_, q_ = sol.y[:, -1]
        mu_end = ad / 2
        pred = M(l, mu_end, 0) * mp.matrix(y0)
        err_ode = max(err_ode, abs(p_ - float(pred[0])), abs(q_ - float(pred[1])))
record("B3_direct_ode_vs_legendre", err_ode < 1e-8,
       f"max deviation over l=0..6 at s=6 between solve_ivp in s and Legendre propagator: {err_ode:.2e}")

# ---- matched local oscillator (LO = output mean field) ----------------------------------
# Quadratures X_A (amplitude) and X_P (phase), shot noise = 1.  For a coherent input:
#   C_AA = 1, C_AP = <G>, C_PP = <G^2> + K,   <f> = (3/4) int (1-xi^2) f dxi
#   G(xi) = (4/(3 eps~)) [Dtheta - M2_12 P_2(xi)],  K = 1 + (1 - M2_11)^2 J_delta / 3,
#   J_delta = int_{-1+delta}^{1-delta} P_2^2/(1-xi^2) = ln((2-delta)/delta) - 3 + O(delta).
P2m, P2v = mp.mpf(-1) / 5, mp.mpf(1) / 7          # <P_2>, <P_2^2> with weight (3/4)(1-xi^2)


def J(delta):
    return mp.quad(lambda t: ((3 * t**2 - 1) / 2) ** 2 / (1 - t**2), [-1 + delta, 0, 1 - delta])


def matched(mu, mu0=0.0, eps=None, delta=None):
    t, t0 = mp.atanh(mu), mp.atanh(mu0)
    M2 = M(2, mu, mu0)
    m12, m11 = M2[0, 1], M2[0, 0]
    g1 = (t - t0) - m12 * P2m                                   # eps~ <G> / (4/3)
    g2 = (t - t0) ** 2 - 2 * (t - t0) * m12 * P2m + m12**2 * P2v
    R_inf = (g2 - g1**2) / g2
    out = {"theta": t, "M2_11": m11, "M2_12": m12, "R_inf": R_inf, "edge_weight": (1 - m11) ** 2}
    if eps is not None:
        G1, G2 = (4 / (3 * eps)) * g1, (4 / (3 * eps)) ** 2 * g2
        K = 1 + (1 - m11) ** 2 * J(delta) / 3 if delta is not None else mp.mpf(1)   # delta=None: no edge term
        C = mp.matrix([[1, G1], [G1, G2 + K]])
        ev = mp.eig(C)[0]
        out.update(C=C, K=K, Vmin=min(ev), Vmax=max(ev), det=mp.det(C))
    return out


# B4a commutator [X_A, X_P] = 2i is preserved (pulled-back weights), any mu, mu0.
def comm_matched(mu, mu0):
    # pulled-back p-weight on input is (4/3)*sin*[1 - M2_11 P_2(xi)]/... ; commutator = (i/E) int a1 b2 / (1-xi^2)
    m11 = M(2, mu, mu0)[0, 0]
    return (mp.mpf(3) / 4) * mp.quad(lambda t: 2 * (mp.mpf(2) / 3) * (1 - m11 * (3 * t**2 - 1) / 2), [-1, 1])


err_comm = max(abs(comm_matched(mu, mu0) - 2) for mu0 in (0, -0.5) for mu in (0.0, 0.3, 0.7, 0.95))
record("B4a_commutator_matched_LO", err_comm < 1e-20,
       f"[X_A, X_P]/i over mu in {{0,.3,.7,.95}}, mu0 in {{0,-.5}}: max |value - 2| = {mp.nstr(err_comm, 3)}")

# B4b uncertainty (Robertson-Schroedinger): det C >= 1 and C_AA = 1 (photon number conserved).
dets = []
for mu0 in (0, -0.5):
    for mu in (0.05, 0.3, 0.6, 0.9, 0.9375, 0.99):
        for eps in (0.1, 0.02):
            for delta in (1e-2, 1e-4):
                dets.append(matched(mu, mu0, eps, delta)["det"])
record("B4b_uncertainty", min(dets) >= 1 - 1e-20,
       f"min det C over grid = {mp.nstr(min(dets), 8)} (>= 1 required); C_AA = 1 identically (number conserved)")

# B4c generic polynomial LOs: commutators of pulled-back quadratures equal output commutators.
rng = np.random.default_rng(20261004)
LMAX = 8
xg, wg = np.polynomial.legendre.leggauss(40)


def leg(l, z):
    return np.polynomial.legendre.legval(z, [0] * l + [1])


def pullback(alpha, beta, mu, mu0, eps):
    """Output readout X = int alpha n + 2 int (1-xi^2) beta p  (LO = Abar*(alpha_c + i beta)),
    returned as input Legendre weights (wn_l on n_l^in, wp_l on p_l^in)."""
    A = [np.sum(wg * alpha(xg) * leg(l, xg)) for l in range(LMAX + 3)]
    B = [np.sum(wg * (1 - xg**2) * beta(xg) * leg(l, xg)) for l in range(LMAX + 3)]
    wn, wp = [], []
    for l in range(LMAX + 3):
        Ml = np.array(M(l, mu, mu0).tolist(), dtype=float)
        # output: n_l = eps*(Ml[1,0] p + Ml[1,1] n/eps), p_l = Ml[0,0] p + Ml[0,1] n/eps
        wp.append(A[l] * eps * Ml[1, 0] + 2 * B[l] * Ml[0, 0])
        wn.append(A[l] * Ml[1, 1] + 2 * B[l] * Ml[0, 1] / eps)
    return np.array(wn), np.array(wp)


def commutator(w1, w2):
    # [n_l, p_m] = i (2l+1)/2 delta_lm / n0 ; drop i/n0
    (n1_, p1_), (n2_, p2_) = w1, w2
    c = np.array([(2 * l + 1) / 2 for l in range(len(n1_))])
    return np.sum(c * (n1_ * p2_ - p1_ * n2_))


errs = []
for _ in range(20):
    c1_, c2_ = rng.normal(size=(2, 4))
    al1 = lambda z, c=c1_: np.polynomial.polynomial.polyval(z, c)
    be2 = lambda z, c=c2_: np.polynomial.polynomial.polyval(z, c)
    zero = lambda z: 0 * z
    mu, mu0, eps = rng.uniform(0, 0.97), rng.choice([0.0, -0.5]), rng.uniform(0.01, 0.1)
    out = commutator((pullback(al1, zero, mu0, mu0, eps)), pullback(zero, be2, mu0, mu0, eps))
    back = commutator(pullback(al1, zero, mu, mu0, eps), pullback(zero, be2, mu, mu0, eps))
    errs.append(abs(out - back) / max(1, abs(out)))
record("B4c_commutator_generic_polynomial_LO", max(errs) < 1e-9,
       f"20 random LO pairs (degree 3 polynomials x mean field): max relative commutator change = {max(errs):.1e}")

# B4d linear (low-power) limit: P0 -> 0 at fixed fibre, length and T0 gives V -> 1 (coherent state kept).
eps1, s1 = 0.05, 2.0                       # values at the reference power P_ref
lin = []
for pw_ in (1e-2, 1e-4, 1e-6):
    eps_p, s_p = eps1 / math.sqrt(pw_), s1 * math.sqrt(pw_)
    mu_p = mp.tanh(theta_of_s(s_p))
    r = matched(mu_p, 0, eps_p, 1e-3)
    phi_nl = mp.atanh(mu_p) / eps_p
    lin.append((pw_, float(phi_nl), float(r["Vmin"]), float(r["Vmax"])))
ok_lin = all(abs(1 - vmin) < 3 * phinl and abs(vmax - 1) < 3 * phinl for _, phinl, vmin, vmax in lin)
record("B4d_linear_limit", ok_lin and lin[-1][2] > 0.999,
       f"(P0/P_ref, Phi_NL, Vmin, Vmax) = {[(p_, round(f_, 6), round(v1, 6), round(v2, 6)) for p_, f_, v1, v2 in lin]}")

# B4e pure-SPM limit (mu -> 0 at fixed Phi_NL -> large): R -> 1 - (int I^2)^2/(int I int I^3) = 1/15 for I = 1-xi^2.
I1, I2, I3 = mp.quad(lambda t: 1 - t**2, [-1, 1]), mp.quad(lambda t: (1 - t**2) ** 2, [-1, 1]), mp.quad(lambda t: (1 - t**2) ** 3, [-1, 1])
R_spm = 1 - I2**2 / (I1 * I3)
R_small = matched(mp.mpf("1e-6"), 0)["R_inf"]
record("B4e_pure_SPM_limit", abs(R_spm - mp.mpf(1) / 15) < 1e-25 and abs(R_small - R_spm) < 1e-9,
       f"profile-limited SPM squeezing for I=1-xi^2: {mp.nstr(R_spm, 12)} (=1/15); R_inf(mu=1e-6) = {mp.nstr(R_small, 12)}")

# B4f edge-log asymptotics of J_delta.
jd = [(d, float(J(d) - (mp.log((2 - d) / d) - 3))) for d in (1e-2, 1e-3, 1e-4, 1e-5)]
record("B4f_edge_integral_asymptotics", abs(jd[-1][1]) < 1e-4,
       f"J_delta - [ln((2-delta)/delta) - 3] for delta=1e-2..1e-5: {[(d, round(e, 7)) for d, e in jd]}")

# B5 pre-chirped (held-out) launch: unit-orbit mapping vs direct integration in s with input normalization.
def rhs_chirped(s_val, y, lam):
    aa, ad, p_, q_, ph = y
    return [ad, 2 / aa**2, q_ / aa, -lam * p_ / aa**2, 1 / aa]


err_h = 0.0
amh_, th0h_ = 0.75, mp.atanh(-0.5)
for z in (0.5, 1.0, 2.0, 4.0):
    t = mp.findroot(lambda q: amh_ ** 1.5 * (s_of_theta(q) - s_of_theta(th0h_)) - z, (th0h_, 4), solver='illinois')
    D = np.diag([1, 1 / math.sqrt(amh_)])
    for l in (0, 2, 3):
        Mu = np.array(M(l, mp.tanh(t), -0.5).tolist(), dtype=float)
        Mi = D @ Mu @ np.linalg.inv(D)
        for j, y0 in enumerate(([1, 0], [0, 1])):
            sol = solve_ivp(rhs_chirped, (0, z), [1.0, -2 / math.sqrt(3), *y0, 0.0], args=(l * (l + 1),),
                            rtol=1e-12, atol=1e-13)
            err_h = max(err_h, np.max(np.abs(sol.y[2:4, -1] - Mi[:, j])),
                        abs(sol.y[0, -1] - amh_ * float(mp.cosh(t) ** 2)),
                        abs(sol.y[4, -1] - float(t - th0h_) * math.sqrt(amh_)))
record("B5_prechirped_mapping", err_h < 1e-8,
       f"pre-chirped launch (a(0)=1, a'(0)=-2/sqrt3): width, eps*Phi_NL and blocks l=0,2,3 from the unit orbit "
       f"agree with direct integration in s to {err_h:.1e}")

# B7 the claim's moment readouts recover the Legendre amplitudes n_0..n_3, p_0..p_3 exactly.
def readout_check(seed=7, a_=2.3, ad_=1.4, eps_=0.05):
    r = np.random.default_rng(seed)
    nc, pc = r.normal(size=7), r.normal(size=7)
    xs, ws = np.polynomial.legendre.leggauss(30)
    n = np.polynomial.legendre.legval(xs, nc)
    pp = np.polynomial.legendre.legval(xs, pc)
    dp = np.polynomial.legendre.legval(xs, np.polynomial.legendre.legder(pc))
    I = lambda f: float(np.sum(ws * f))
    mom_rho = lambda k: a_**k * I(xs**k * n)                                        # int x^k drho dx
    mom_rv = lambda k: a_**k * I(xs**k * (n * xs * ad_ - (eps_ / a_) * (1 - xs**2) * dp))   # delta int x^k rho v dx
    imag = I((1 - xs**2) * pp)                                                       # int Im(psibar* dpsi) dx
    n0 = 0.5 * mom_rho(0)
    n2 = 15 / 4 * (mom_rho(2) / a_**2 - 2 / 3 * n0)
    p2 = -5 / (4 * eps_) * (mom_rv(1) - ad_ / a_ * mom_rho(2))
    p0 = 3 / 4 * (imag + 4 / 15 * p2)
    n1 = 1.5 * mom_rho(1) / a_
    n3 = 35 / 4 * (mom_rho(3) / a_**3 - 2 / 5 * n1)
    p1 = -3 * a_ / (4 * eps_) * (mom_rv(0) - ad_ / a_ * mom_rho(1))
    p3 = -35 / 16 * ((mom_rv(2) - ad_ / a_ * mom_rho(3)) / (eps_ * a_) + 4 / 15 * p1)
    got = np.array([n0, n1, n2, n3, p0, p1, p2, p3])
    want = np.array([*nc[:4], *pc[:4]])
    return float(np.max(np.abs(got - want)))


err_ro = max(readout_check(seed=s_) for s_ in range(5))
record("B7_moment_readouts_exact", err_ro < 1e-10,
       f"moment readouts of the claim recover n_0..n_3, p_0..p_3 of random degree-6 perturbations to {err_ro:.1e}")

# B8 static 1D edge layer: Hastings-McLeod mass identity int [q^2 - (-y/2)_+] dy = 0 (used in derivation note Sec. 6).
from scipy.integrate import solve_bvp
from scipy.special import airy


def hm_mass(Y1=14.0, Y2=6.0):
    qas = lambda y: np.sqrt(-y / 2) * (1 + 1 / (8 * y**3) - 73 / (128 * y**6))
    y = np.linspace(-Y1, Y2, 4001)
    q0 = np.where(y < 0, np.sqrt(np.maximum(-y / 2, 0) + 1e-3), airy(y)[0])
    sol = solve_bvp(lambda yy, Y: np.vstack([Y[1], yy * Y[0] + 2 * Y[0] ** 3]),
                    lambda Ya, Yb: np.array([Ya[0] - qas(-Y1), Yb[0] - airy(Y2)[0]]),
                    y, np.vstack([q0, np.gradient(q0, y)]), tol=1e-10, max_nodes=200000)
    yy = np.linspace(-Y1, Y2, 400001)
    q = sol.sol(yy)[0]
    inner = np.trapezoid(q**2 - np.maximum(-yy / 2, 0), yy) if hasattr(np, "trapezoid") else np.trapz(q**2 - np.maximum(-yy / 2, 0), yy)
    return float(sol.sol(0.0)[0]), float(inner - 1 / (8 * Y1)), sol.status


q0_hm, mass_hm, st_hm = hm_mass()
record("B8_hastings_mcleod_mass_identity", st_hm == 0 and abs(q0_hm - 0.3670615515) < 1e-8 and abs(mass_hm) < 2e-5,
       f"Hastings-McLeod by solve_bvp: q(0) = {q0_hm:.10f} (the commonly quoted value, not sourced here, is 0.3670615515); "
       f"int[q^2-(-y/2)_+]dy (with -1/(8Y) tail) = {mass_hm:.1e}, i.e. zero edge-layer mass at O(eps^(4/3))")

# ---------------------------------------------------------------- C. frozen predictions
mu_star = mp.findroot(lambda z: PQ(2, z)[1], (0.9, 0.97), solver='illinois')
th_star = mp.atanh(mu_star)
pred = RES["predictions"]
pred["mu_star"] = float(mu_star)
pred["theta_star"] = float(th_star)
pred["a_star"] = float(mp.cosh(th_star) ** 2)
pred["zeta_star"] = float(s_of_theta(th_star))
pred["edge_log_slope_at_mu_star"] = float(2 * mu_star**4)
# local slope d det/d ln(1/eps) at zeta* for delta = c eps^(2/3): 3 mu*^4 (2/3) * 2 P_2(1-delta)^2/(2-delta)
pred["edge_local_slope_at_mu_star"] = {
    f"eps={e},c={c}": float(3 * mu_star**4 * (mp.mpf(2) / 3) * 2 * ((3 * (1 - c * e ** (2 / 3)) ** 2 - 1) / 2) ** 2
                            / (2 - c * e ** (2 / 3)))
    for e in (0.1, 0.05, 0.025, 0.0125) for c in (1, 2, 4)}

# B6 physical meaning of zeta*: at fixed L and T0 the output chirp rate (in units of the far-field value 1/(beta2 L))
# is zeta*adot/a; its stationary point in P0 (zeta ∝ sqrt(P0)) coincides with Q_2(mu)=0.
def chirp_rate(z):
    t = theta_of_s(z)
    return z * 2 * mp.tanh(t) / mp.cosh(t) ** 2


z_stat = mp.findroot(lambda z: mp.diff(chirp_rate, z), (3, 7), solver='illinois')
record("B6_chirp_rate_stationary_at_zeta_star", abs(z_stat - s_of_theta(th_star)) < 1e-15,
       f"d/dP0 of output chirp rate at fixed L vanishes at zeta = {mp.nstr(z_stat, 12)} "
       f"(zeta* = {mp.nstr(s_of_theta(th_star), 12)}); max chirp rate = {mp.nstr(chirp_rate(z_stat), 8)} x 1/(beta2 L)")
pred["chirp_rate_max_over_far_field"] = float(chirp_rate(z_stat))
pred["chirp_rate_table_zeta_adot_over_a"] = {str(z): float(chirp_rate(z)) for z in (1, 2, 3, 6, 8, 20)}


def row(s_val, mu0=0.0, am=1.0, th0=0.0):
    """Main case mu0 = 0.  Held-out case: unit orbit with offset; all block matrices are converted to the
    input-pulse variables (p, n/eps) with eps = 1/N of the launched pulse: M_in = D M_unit D^-1,
    D = diag(1, 1/sqrt(a_m)); eps*Phi = (theta - theta0) * sqrt(a_m)."""
    if mu0 == 0.0:
        t = theta_of_s(s_val)
    else:
        st0 = s_of_theta(th0)
        t = mp.findroot(lambda q: am ** 1.5 * (s_of_theta(q) - st0) - s_val, (th0, 4), solver='illinois')
    mu = mp.tanh(t)
    r = matched(mu, mu0)
    sa = mp.sqrt(am)
    D = mp.matrix([[1, 0], [0, 1 / sa]])
    conv = lambda Mx: D * Mx * mp.inverse(D)
    blocks = {f"M{l}": conv(M(l, mu, mu0)) for l in (0, 2, 3, 4)}
    g1 = (r["theta"] - mp.atanh(mu0)) - r["M2_12"] * P2m
    d = {
        "zeta": s_val, "mu": float(mu), "theta": float(t),
        "width_ratio_a": float(am * mp.cosh(t) ** 2),
        "epsPhiNL_peak": float((t - mp.atanh(mu0)) * sa),
        "eps_Phi_eff_matchedLO": float((mp.mpf(2) / 3) * g1 * sa),
        "R_inf": float(r["R_inf"]), "R_inf_dB": float(10 * mp.log10(r["R_inf"])) if r["R_inf"] > 1e-30 else None,
        "edge_log_slope": float(2 * (1 - r["M2_11"]) ** 2 / 9),
    }
    for k, Mx in blocks.items():
        d[k] = [[float(Mx[i, j]) for j in range(2)] for i in range(2)]
    return d


# Example system (illustration of the regime bounds; not a prediction): standard fibre near 1.06 um.
def example_system(T0=2e-12, P0=500.0, beta2=20e-27, gamma=5e-3, beta3=4e-41, TR=3e-15, lam=1.06e-6,
                   loss_dB_per_km=1.0):
    hbar, c0 = 1.054571817e-34, 2.99792458e8
    w0 = 2 * math.pi * c0 / lam
    LD, LNL = T0**2 / beta2, 1 / (gamma * P0)
    N = math.sqrt(LD / LNL)
    Z = math.sqrt(LD * LNL)
    zs = float(s_of_theta(th_star))
    Lstar = zs * Z
    eta = 10 ** (-loss_dB_per_km * Lstar / 1e3 / 10)
    return {"T0_ps": T0 * 1e12, "P0_W": P0, "beta2_ps2_per_km": beta2 * 1e27, "gamma_per_W_km": gamma * 1e3,
            "N": N, "eps": 1 / N, "sqrt_LD_LNL_m": Z, "L_star_m": Lstar,
            "delta3": 2 * N * beta3 / (3 * beta2 * T0), "tauR_zeta_star": TR / T0 * zs,
            "self_steepening": 2 * N / (w0 * T0), "n0_photons": P0 * T0 / (hbar * w0),
            "spectral_half_width_THz_far_field": 2 * N / T0 / (2 * math.pi) / 1e12,
            "transmission_at_L_star": eta, "loss_floor_dB": 10 * math.log10(1 - eta)}


pred["example_system"] = example_system()

main_s = [0.25, 0.5, 1.0, 2.0, 3.0, float(s_of_theta(th_star)), 6.0, 8.0, 10.0]
pred["main_mu0_0"] = [row(z) for z in main_s]
# held-out: pre-chirped launch, mu0 = -1/2 (a_m = 3/4); zeta measured from the launch in input units.
mu0h = mp.mpf(-1) / 2
th0h = mp.atanh(mu0h)
amh = mp.mpf(3) / 4
mu_z = mp.findroot(lambda z: M(2, z, mu0h)[0, 1], (0.6, 0.7), solver='illinois')
pred["heldout_mu0_minus_half"] = {
    "launch_chirp_C_over_N": float(2 / mp.sqrt(3)),
    "min_width_ratio": float(amh),
    "zeta_at_min_width": float(amh ** 1.5 * (0 - s_of_theta(th0h))),
    "mu_zero_of_M2_12": float(mu_z),
    "zeta_zero_of_M2_12": float(amh ** 1.5 * (s_of_theta(mp.atanh(mu_z)) - s_of_theta(th0h))),
    "rows": [row(z, float(mu0h), float(amh), th0h) for z in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0)],
}
# finite-eps matched-LO numbers with the edge cutoff delta = eps^(2/3) (illustration; edge constant not predicted)
fin = []
for eps in (0.1, 0.05, 0.025, 0.0125):
    for z in (1.0, 2.0, float(s_of_theta(th_star)), 8.0):
        mu = mp.tanh(theta_of_s(z))
        r = matched(mu, 0, eps, eps ** (2 / 3))
        r1 = matched(mu, 0, eps, None)   # K = 1: edge term dropped
        fin.append({"eps": eps, "zeta": z, "C_AP": float(r["C"][0, 1]), "C_PP": float(r["C"][1, 1]),
                    "Vmin_K1": float(r1["Vmin"]),
                    "Vmin": float(r["Vmin"]), "Vmin_dB": float(10 * mp.log10(r["Vmin"])), "det": float(r["det"])})
pred["finite_eps_matched_LO_with_delta_eps23"] = fin

# figure
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    zs = np.linspace(0.02, 12, 400)
    Rm = [float(matched(mp.tanh(theta_of_s(z)), 0)["R_inf"]) for z in zs]
    st0 = s_of_theta(th0h)
    Rh = []
    for z in zs:
        t = mp.findroot(lambda q: amh ** 1.5 * (s_of_theta(q) - st0) - z, (th0h, 4), solver='illinois')
        Rh.append(float(matched(mp.tanh(t), mu0h)["R_inf"]))
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.semilogy(zs, Rm, label=r"unchirped launch ($\mu_0=0$)")
    ax.semilogy(zs, Rh, "--", label=r"held-out: pre-chirped launch ($\mu_0=-1/2$)")
    ax.axhline(1 / 15, color="0.6", lw=0.8)
    ax.axhline(2 / 65, color="0.6", lw=0.8, ls=":")
    ax.set_xlabel(r"$\zeta = z/\sqrt{L_D L_{NL}}$")
    ax.set_ylabel(r"$R_\infty$ (matched-LO variance, $\varepsilon\to 0$)")
    ax.set_ylim(1e-6, 0.2)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "R_inf_vs_zeta.png", dpi=130)
except Exception as e:  # figure is optional
    print("figure skipped:", e)

RES["wall_time_s"] = round(time.time() - T_START, 1)
RES["all_checks_pass"] = all(c["pass"] for c in RES["checks"].values())
(OUT / "summary.json").write_text(json.dumps(RES, indent=1, default=float))
print("all checks pass:", RES["all_checks_pass"], "| wall time", RES["wall_time_s"], "s")
print(json.dumps({k: pred[k] for k in ("mu_star", "theta_star", "a_star", "zeta_star", "edge_log_slope_at_mu_star")}))
