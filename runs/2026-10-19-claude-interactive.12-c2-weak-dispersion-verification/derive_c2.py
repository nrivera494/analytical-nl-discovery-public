"""Independent derivation of the second-order coefficient c2(Phi) of the
weak-normal-dispersion squeezing law (claim C-20261019-pi-chatgpt-01).

Written by claude-interactive.12 before reading the proposer's derivation.

Model (x = t/T0, zeta = z/L, eps = L/L_D, y = Phi*eps):
    u_zeta = -i (eps/2) u_xx + i Phi |u|^2 u,   u(0,x) = exp(-x^2/2).
Local scaling at the peak: x = h^(1/2) q with h = sqrt(y).  Then
    eps d^2/dx^2 = (h/Phi) d^2/dq^2,   |u(0)|^2 = exp(-h q^2),
and every coefficient of the mean and tangent equations is a power series in h
with polynomial coefficients in q (formal local expansion).

Frame: u = e^{i Phi zeta} U, delta u = e^{i Phi zeta}(a + i b).  The real tangent
generator is
    a_z = -Phi I a + [Phi(1 - 2 rho + R) + (h/2Phi) d_q^2] b
    b_z = [Phi(2 rho + R - 1) - (h/2Phi) d_q^2] a + Phi I b
with rho = |U|^2, U^2 = R + i I.  Expand L = L0 + h L1 + h^2 L2, M = M0 + h M1 + h^2 M2
(Duhamel, time ordered), W = M^T M = W0 + h W1 + h^2 W2.  W0 is q independent with
eigenvalues lambda0 = sigma_-^2 (infinitely degenerate) and sigma_+^2 = 1/lambda0.
Quasi-degenerate perturbation theory on the lower branch:
    K1 = P W1 P  (a harmonic oscillator in q; ground state exp(-kappa q^2/2))
    lambda_min = lambda0 + h E1 + h^2 E2 + O(h^3),
    E1 = <Psi0|W1|Psi0>,  E2 = <Psi0|W2|Psi0> - |P_+ W1 Psi0|^2 / (sigma_+^2 - sigma_-^2).
Then A = E1/lambda0 and c2 = E2/E1.

Vectors are stored as polynomial prefactors of the Gaussian g(q) = exp(-kappa q^2/2):
operators act exactly on polynomial*g, and inner products use Gaussian moments.
Parametrization: r = S - Phi (so Phi = (1-r^2)/(2r), S = (1+r^2)/(2r)), all rational in r.
"""
import json
import sys
import sympy as sp

q, z, s, s1 = sp.symbols('q zeta s s1', real=True)
h = sp.symbols('h', positive=True)
r, kap = sp.symbols('r kappa', positive=True)
Phi = (1 - r**2) / (2 * r)
S = (1 + r**2) / (2 * r)
NORD = 3  # orders h^0, h^1, h^2
PROFILE = sys.argv[2] if len(sys.argv) > 2 else 'gauss'  # 'gauss': u0 = exp(-x^2/2); 'sech': u0 = sech(x)
_X = sp.symbols('X', positive=True)  # X = x^2 = h q^2
_amp = {'gauss': sp.exp(-_X / 2), 'sech': 1 / sp.cosh(sp.sqrt(_X)),
        'gq': sp.exp(-_X / 2 - _X**2 / 4)}[PROFILE]  # gq: intensity exp(-x^2 - x^4/2), kappa4 = 0
_amp_ser = sp.series(_amp, _X, 0, NORD).removeO()
import os
MEAN_DISP = int(os.environ.get('MEAN_DISP', '1'))  # 0: ablation without dispersive mean reshaping
AMP0 = [sp.expand(_amp_ser.coeff(_X, k) * q**(2 * k)) for k in range(NORD)]  # coefficient of h^k at zeta = 0


def series_coeffs(expr, n=NORD):
    expr = sp.expand(expr)
    return [sp.expand(expr.coeff(h, k)) for k in range(n)]


def re_im(expr):
    expr = sp.expand(expr)
    re = sp.expand((expr + sp.conjugate(expr)) / 2)
    im = sp.expand((expr - sp.conjugate(expr)) / (2 * sp.I))
    return re, im


# ---------------------------------------------------------------- mean field
w = [sp.Integer(1)]  # w[k]: coefficient of h^k in U
for k in range(1, NORD):
    Ulow = sum(h**j * w[j] for j in range(k))
    Uc = sp.conjugate(Ulow)
    rhs = (-sp.I * Phi * Ulow - MEAN_DISP * sp.I * h / (2 * Phi) * sp.diff(Ulow, q, 2)
           + sp.I * Phi * Ulow * Uc * Ulow)
    Fk = series_coeffs(rhs, k + 1)[k]
    reF, imF = re_im(Fk)
    w0 = AMP0[k]  # initial condition: amplitude profile expanded in h q^2
    rk = w0 + sp.integrate(reF.subs(z, s), (s, 0, z))
    mk = sp.integrate((2 * Phi * rk + imF).subs(z, s), (s, 0, z))
    w.append(sp.expand(rk + sp.I * mk))

U = sum(h**k * w[k] for k in range(NORD))
# residual check: must vanish through h^2
res = sp.diff(U, z) - (-sp.I * Phi * U - MEAN_DISP * sp.I * h / (2 * Phi) * sp.diff(U, q, 2)
                       + sp.I * Phi * U * sp.conjugate(U) * U)
res_c = series_coeffs(sp.simplify(sp.expand(res)), NORD)
assert all(sp.simplify(c) == 0 for c in res_c), res_c
assert all(sp.simplify(c) == 0 for c in series_coeffs(U.subs(z, 0) - _amp.subs(_X, h * q**2).series(h, 0, NORD).removeO()))

rho = series_coeffs(U * sp.conjugate(U))
U2 = series_coeffs(U * U)
R = [re_im(c)[0] for c in U2]
Im = [re_im(c)[1] for c in U2]
assert sp.simplify(rho[0] - 1) == 0 and sp.simplify(R[0] - 1) == 0 and Im[0] == 0
# peak intensity reshaping: rho(zeta, q=0) = 1 - h^2 zeta^2 (i.e. 1 - y zeta^2)
peak_rho2 = sp.simplify(rho[2].subs(q, 0))

# ------------------------------------------------------- tangent generator
# operator entry = (multiplication coefficient, coefficient of d_q^2)
def Lk(k, zz):
    c = lambda e: sp.expand(e.subs(z, zz))
    disp = (sp.Rational(1, 2) / Phi) if k == 1 else 0
    return [[(c(-Phi * Im[k]), 0), (c(Phi * (-2 * rho[k] + R[k])), disp)],
            [(c(Phi * (2 * rho[k] + R[k])), -disp), (c(Phi * Im[k]), 0)]]


def Dq2(P):
    """d^2/dq^2 acting on P(q) g(q), returned as prefactor of g."""
    return sp.expand(sp.diff(P, q, 2) - 2 * kap * q * sp.diff(P, q) + (kap**2 * q**2 - kap) * P)


def apply_op(L, f, transpose=False):
    out = []
    for i in range(2):
        acc = 0
        for j in range(2):
            mc, dc = L[j][i] if transpose else L[i][j]
            acc += mc * f[j]
            if dc != 0:
                acc += dc * Dq2(f[j])
        out.append(sp.expand(acc))
    return out


def M0(zz):
    return sp.Matrix([[1, 0], [2 * Phi * zz, 1]])


def mat_vec(Mx, f):
    return [sp.expand(Mx[0, 0] * f[0] + Mx[0, 1] * f[1]), sp.expand(Mx[1, 0] * f[0] + Mx[1, 1] * f[1])]


def integ(f, a, b, var=s):
    return [sp.expand(sp.integrate(fi, (var, a, b))) for fi in f]


def gauss_ip(P1, P2):
    """<P1 g, P2 g> / <g, g> with g = exp(-kappa q^2/2)."""
    poly = sp.Poly(sp.expand(P1 * P2), q)
    tot = 0
    for (n,), c in poly.terms():
        if n % 2 == 0:
            tot += c * sp.factorial2(n - 1) / (2 * kap)**(n // 2)
    return sp.expand(tot)


def vip(f1, f2):
    return sp.expand(gauss_ip(f1[0], f2[0]) + gauss_ip(f1[1], f2[1]))


# SVD of M0(1) = [[1,0],[2Phi,1]] in the r parametrization
nrm = sp.sqrt(1 + r**2)
v_m = [r / nrm, -1 / nrm]
u_m = [1 / nrm, -r / nrm]
v_p = [1 / nrm, r / nrm]
u_p = [r / nrm, 1 / nrm]
sig_m, sig_p = r, 1 / r
for vv, uu, sg in [(v_m, u_m, sig_m), (v_p, u_p, sig_p)]:
    mv = M0(1) * sp.Matrix(vv)
    assert all(sp.simplify(mv[i] - sg * uu[i]) == 0 for i in range(2))

# ---------------------------------------------------- Duhamel expansion
f0 = lambda zz: mat_vec(M0(zz), v_m)  # M0(zz) Psi0 (prefactor of g)
# f1(zeta) = int_0^zeta M0(zeta - s) L1(s) f0(s) ds
f1_z = integ(mat_vec(M0(z - s), apply_op(Lk(1, s), f0(s))), 0, z)
f1_1 = [sp.expand(e.subs(z, 1)) for e in f1_z]
# f2(1) = int_0^1 M0(1-s) [L2(s) f0(s) + L1(s) f1(s)] ds
f1_s = [e.subs(z, s) for e in f1_z]
src2 = [a + b for a, b in zip(apply_op(Lk(2, s), f0(s)), apply_op(Lk(1, s), f1_s))]
f2_1 = integ(mat_vec(M0(1 - s), src2), 0, 1)
# adjoint: chi = M1(1)^T (u_- g) = int_0^1 M0(s)^T L1(s)^T M0(1-s)^T u_- ds
chi = integ(mat_vec(M0(s).T, apply_op(Lk(1, s), mat_vec(M0(1 - s).T, u_m), transpose=True)), 0, 1)

# ------------------------------------------------------------ first order
E1_k = sp.simplify(2 * sig_m * vip(u_m, f1_1))  # <Psi0|W1|Psi0> for trial width kappa
# E1(kappa) = a/kappa + b kappa ; the harmonic-oscillator ground state minimizes it
E1_poly = sp.expand(E1_k * kap)
a_c = sp.simplify(E1_poly.coeff(kap, 0))
b_c = sp.simplify(E1_poly.coeff(kap, 2))
const_c = sp.simplify(E1_poly.coeff(kap, 1))
kappa_star = sp.sqrt(a_c / b_c)
E1 = sp.simplify(2 * sp.sqrt(a_c * b_c) + const_c)
A_r = sp.simplify(E1 / sig_m**2)

# ----------------------------------------------------------- second order
W2_exp = 2 * sig_m * vip(u_m, f2_1) + vip(f1_1, f1_1)
gplus = sp.expand(sig_p * (u_p[0] * f1_1[0] + u_p[1] * f1_1[1])
                  + sig_m * (v_p[0] * chi[0] + v_p[1] * chi[1]))
mix = gauss_ip(gplus, gplus) / (sig_p**2 - sig_m**2)
E2_k = sp.expand(W2_exp - mix)
E2 = sp.simplify(E2_k.subs(kap, kappa_star))
c2_r = sp.simplify(E2 / E1)
B_r = sp.simplify(E2 / sig_m**2)

# also: the pieces of E2, for the line-by-line comparison
f2_L2 = integ(mat_vec(M0(1 - s), apply_op(Lk(2, s), f0(s))), 0, 1)
f2_L1L1 = integ(mat_vec(M0(1 - s), apply_op(Lk(1, s), f1_s)), 0, 1)
pieces = {
    'W2_M0M2': sp.simplify((2 * sig_m * vip(u_m, f2_1)).subs(kap, kappa_star) / E1),
    'W2_M0M2_from_L2': sp.simplify((2 * sig_m * vip(u_m, f2_L2)).subs(kap, kappa_star) / E1),
    'W2_M0M2_from_L1L1_time_ordered': sp.simplify((2 * sig_m * vip(u_m, f2_L1L1)).subs(kap, kappa_star) / E1),
    'W2_M1M1': sp.simplify(vip(f1_1, f1_1).subs(kap, kappa_star) / E1),
    'branch_mixing': sp.simplify(-mix.subs(kap, kappa_star) / E1),
}

# ---------------------------------------------------- compare with the claim
P = sp.symbols('Phi', positive=True)
Sx = sp.sqrt(1 + P**2)
c2_claim = sp.sqrt(6) * (45 + 81 * P**2 + 56 * P**4 + 40 * P**3 * Sx) / (240 * P**2 * (1 + P**2))
A_claim = sp.sqrt(sp.Rational(2, 3)) * P / Sx
r_of_P = Sx - P

out = {'profile': PROFILE, 'mean_dispersion_in_mean_field': MEAN_DISP, 'peak_rho_h2_coeff': str(peak_rho2), 'kappa_star_r': str(sp.simplify(kappa_star)),
       'A_r': str(A_r), 'c2_r': str(c2_r), 'B_r': str(B_r), 'values': {}}
print('peak rho h^2 coefficient:', peak_rho2)
print('kappa*(r) =', sp.simplify(kappa_star))
print('A(r) =', A_r)
print('c2(r) =', c2_r)
maxdiff = 0
for Pv in ['1', '1.5', '2', '3', '7', '10', '40', '0.5', '0.25']:
    Pn = sp.Rational(Pv)
    rv = r_of_P.subs(P, Pn)
    c2_mine = sp.N(c2_r.subs(r, rv), 30)
    c2_card = sp.N(c2_claim.subs(P, Pn), 30)
    A_mine = sp.N(A_r.subs(r, rv), 30)
    A_card = sp.N(A_claim.subs(P, Pn), 30)
    pc = {k: float(sp.N(v.subs(r, rv), 20)) for k, v in pieces.items()}
    d = abs(c2_mine - c2_card)
    maxdiff = max(maxdiff, float(d), float(abs(A_mine - A_card)))
    out['values'][Pv] = {'c2_derived': float(c2_mine), 'c2_claim': float(c2_card), 'abs_diff': float(d),
                         'A_derived': float(A_mine), 'A_claim': float(A_card),
                         'kappa_star': float(sp.N(kappa_star.subs(r, rv))), 'c2_pieces': pc}
    print(f'Phi={Pv:>5}: c2 derived {sp.N(c2_mine, 15)}  claim {sp.N(c2_card, 15)}  |diff| {sp.N(d, 3)};'
          f'  A derived {sp.N(A_mine, 12)} claim {sp.N(A_card, 12)};  pieces {pc}')
# exact symbolic identity check
c2_claim_r = sp.sqrt(6) * (45 + 81 * Phi**2 + 56 * Phi**4 + 40 * Phi**3 * S) / (240 * Phi**2 * (1 + Phi**2))
# 0 < r < 1 for Phi > 0: |r^2 - 1| = 1 - r^2 and sqrt((1 + r^2)^2) = 1 + r^2
_fix = lambda e: e.replace(sp.Abs, lambda a: -a).subs(sp.sqrt(r**4 + 2 * r**2 + 1), 1 + r**2)
c2_r, A_r, B_r = sp.factor(_fix(c2_r)), sp.factor(_fix(A_r)), sp.factor(_fix(B_r))
out.update({'A_r': str(A_r), 'c2_r': str(c2_r), 'B_r': str(B_r)})
print('c2(r) for 0<r<1:', c2_r)
ident = sp.simplify(sp.together(c2_r - c2_claim_r))
out['symbolic_identity_residual'] = str(ident)
out['max_abs_diff_numeric'] = maxdiff
print('symbolic residual c2_derived - c2_claim (r form):', ident)
lim = sp.limit(c2_r, r, 0, '+')
out['c2_limit_Phi_inf'] = str(lim)
print('c2 as Phi -> inf (r -> 0):', lim, '=', sp.N(lim))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'derive_c2.json', 'w'), indent=1)
