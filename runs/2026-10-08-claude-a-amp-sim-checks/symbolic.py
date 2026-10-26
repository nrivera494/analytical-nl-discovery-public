#!/usr/bin/env python3
"""Symbolic checks for the amplifier-similariton noise derivation (task T-20261008-claude-a-01).

Model (Agrawal convention): dA/dz = -(i/2) b2 A_TT + i gam |A|^2 A + (g/2) A  (+ ASE Langevin noise).
Dispersionless form with rho = |A|^2, v = -b2 * dphi/dT:
    rho_z + (rho v)_T = g rho,     v_z + v v_T = -gam b2 rho_T.
Prints PASS/FAIL lines and writes symbolic.json next to this file.
"""
import json
import sys
from pathlib import Path

import sympy as sp
from sympy.calculus.euler import euler_equations

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
res = {}


def record(name, ok, detail):
    res[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


z, T, g, gam, b2, E0 = sp.symbols("z T g gamma beta2 E0", positive=True)
Tp = sp.Function("T_p")(z)
rho0 = 3 * E0 * sp.exp(g * z) / (4 * Tp)                  # energy E = (4/3) rho0 Tp = E0 e^{gz}
width_ode = {sp.Derivative(Tp, (z, 2)): sp.Rational(3, 2) * gam * b2 * E0 * sp.exp(g * z) / Tp**2}
rho = rho0 * (1 - T**2 / Tp**2)
v = Tp.diff(z) / Tp * T

# G1: parabolic family with linear chirp is invariant under the gain equations.
r1 = sp.simplify(rho.diff(z) + (rho * v).diff(T) - g * rho)
r2 = sp.simplify((v.diff(z) + v * v.diff(T) + gam * b2 * rho.diff(T)).subs(width_ode))
record("G1_parabolic_family_with_gain", r1 == 0 and r2 == 0,
       f"continuity-with-gain residual {r1}; momentum residual {r2} given Tp'' = (3/2) gam b2 E0 e^(gz)/Tp^2")

# G2: rescaled width s(tau), Tp = c e^{tau/3} s(tau), tau = g z, c^3 = 27 gam b2 E0/(2 g^2); Lyapunov function.
tau = sp.symbols("tau", real=True)
s = sp.Function("s")(tau)
c = sp.symbols("c", positive=True)
Tp_s = c * sp.exp(tau / 3) * s
d2 = g**2 * sp.diff(Tp_s, tau, 2)                              # Tp'' in z
rhs = sp.Rational(3, 2) * gam * b2 * E0 * sp.exp(tau) / Tp_s**2
c3 = 27 * gam * b2 * E0 / (2 * g**2)
expr = sp.simplify((d2 - rhs).subs(gam, 2 * g**2 * c**3 / (27 * b2 * E0)) / (g**2 * c * sp.exp(tau / 3)))
target = sp.diff(s, tau, 2) + sp.Rational(2, 3) * s.diff(tau) + s / 9 - 1 / (9 * s**2)
g2a = sp.simplify(expr - target)
V = s.diff(tau) ** 2 / 2 + s**2 / 18 + 1 / (9 * s)
sode = {sp.Derivative(s, (tau, 2)): -sp.Rational(2, 3) * s.diff(tau) - s / 9 + 1 / (9 * s**2)}
dV = sp.simplify(V.diff(tau).subs(sode) + sp.Rational(2, 3) * s.diff(tau) ** 2)
Vs = s**2 / 18 + 1 / (9 * s)
x_ = sp.symbols("x", positive=True)
crit = sp.solve(sp.diff(Vs.subs(s, x_), x_), x_)
record("G2_rescaled_width_and_Lyapunov", g2a == 0 and dV == 0 and crit == [1],
       f"Tp''-RHS reduces to s''+(2/3)s'+s/9-1/(9s^2) (residual {g2a}); dV/dtau = -(2/3)s'^2 (residual {dV}); "
       f"V(s) has its only critical point at s = {crit}")

# G3: linearization about ANY parabolic background with gain separates in Legendre P_l(T/Tp).
# Lab-frame linearized equations (dispersionless), with delta v = psi_T (psi = -b2 * phase perturbation):
#   drho_z + (rho dv + v drho)_T - g drho = 0 ;   psi_z + v psi_T + gam b2 drho = 0.
f = sp.Function("f")(z)            # n_l(z): delta rho = rho0 * n_l * P_l
h = sp.Function("h")(z)            # psi_l(z)
ok = True
for l in range(0, 7):
    P = sp.legendre(l, T / Tp)
    drho = rho0 * f * P
    psi = h * P
    R1 = drho.diff(z) + (rho * psi.diff(T) + v * drho).diff(T) - g * drho
    R2 = psi.diff(z) + v * psi.diff(T) + gam * b2 * drho
    e1 = sp.simplify(sp.expand(R1 - rho0 * (f.diff(z) - l * (l + 1) * h / Tp**2) * P))
    e2 = sp.simplify(sp.expand(R2 - (h.diff(z) + gam * b2 * rho0 * f) * P))
    ok &= (e1 == 0 and e2 == 0)
record("G3_legendre_separation_with_gain", ok,
       "for l=0..6 and any Tp(z): n_l' = l(l+1) psi_l/Tp^2, psi_l' = -gam b2 rho0 n_l "
       "(n = delta rho/rho0, psi = -b2 p); gain drops out of the blocks")

# G4: second-order block equation for n_l and its asymptotic rates (orchestrator sketch).
lam_l = sp.symbols("lambda_l")
n = sp.Function("n")(z)
p_from_n = -n.diff(z) * Tp**2 / (b2 * sp.Symbol("L"))     # placeholder, the check below uses the first-order system
# Direct: with p = psi/(-b2): n' = -(b2 L/Tp^2) p, p' = gam rho0 n  ->  n'' + 2(Tp'/Tp) n' + L (Tp''/(2Tp)) n = 0
Lsym = sp.symbols("L", positive=True)
pz = sp.Function("p")(z)
n_eq = sp.Eq(n.diff(z), -(b2 * Lsym / Tp**2) * pz)
p_eq = sp.Eq(pz.diff(z), gam * rho0 * n)
n2 = sp.diff(n_eq.rhs, z).subs(pz.diff(z), p_eq.rhs)
pz_sol = sp.solve(n_eq, pz)[0]
lhs = (n2 + 2 * Tp.diff(z) / Tp * n.diff(z) + Lsym * (Tp.diff(z, 2) / (2 * Tp)) * n).subs(pz, pz_sol).subs(width_ode)
g4a = sp.simplify(lhs.subs(n.diff(z), -(b2 * Lsym / Tp**2) * pz_sol))
lam = sp.symbols("lambda")
Gs = sp.symbols("G", positive=True)
charpoly = lam**2 + sp.Rational(2, 3) * Gs * lam + Lsym * Gs**2 / 18
roots = sp.solve(charpoly, lam)
expected = [Gs / 3 * (-1 - sp.sqrt(1 - Lsym / 2)), Gs / 3 * (-1 + sp.sqrt(1 - Lsym / 2))]
g4b = all(any(sp.simplify(r - e) == 0 for e in expected) for r in roots)
record("G4_block_ode_and_asymptotic_rates", g4a == 0 and g4b,
       "n_l'' + 2(Tp'/Tp) n_l' + l(l+1)(Tp''/(2Tp)) n_l = 0 (residual 0); on Tp ∝ e^{gz/3}: "
       "lambda = (g/3)[-1 ± sqrt(1 - l(l+1)/2)] (orchestrator sketch confirmed)")

# G5: Ehrenfest relations for the dimensionless NLSE with gain:
#   psi_zeta = -(i/2) eps psi_xx + (i/eps)|psi|^2 psi + (Gam/2) psi.
x = sp.symbols("x", real=True)
eps, Gam = sp.symbols("epsilon Gamma", positive=True)
u = sp.Function("u", real=True)(x)
w = sp.Function("w", real=True)(x)
rho_d = u**2 + w**2
# real and imaginary parts of the right-hand side for psi = u + i w
u_t = (eps / 2) * w.diff(x, 2) - rho_d * w / eps + Gam * u / 2
w_t = -(eps / 2) * u.diff(x, 2) + rho_d * u / eps + Gam * w / 2


def varder(F, fn, kmax=4):
    """Euler operator: zero iff F is a total x-derivative."""
    out = 0
    for k in range(kmax + 1):
        dk = fn if k == 0 else fn.diff(x, k)
        out += (-1) ** k * sp.diff(sp.diff(F, dk), x, k)
    return sp.simplify(sp.expand(out))


drho = sp.expand(2 * (u * u_t + w * w_t))
flux_rho = eps * (u * w.diff(x) - w * u.diff(x))
e_energy = sp.simplify(drho - Gam * rho_d - flux_rho.diff(x))
K = w * u.diff(x) - u * w.diff(x)                                    # momentum density, K = -Im(psi* psi_x)
dK = sp.expand(w_t * u.diff(x) + w * sp.diff(u_t, x) - u_t * w.diff(x) - u * sp.diff(w_t, x))
resid = sp.expand(dK - Gam * K)
e_mom = [varder(resid, u), varder(resid, w)]
sanity = varder(u**2, u)
e_cent = sp.simplify(flux_rho - eps * (-K))
e_mom_ok = all(e == 0 for e in e_mom) and sanity != 0
record("G5_ehrenfest_with_flat_gain", e_energy == 0 and e_mom_ok and e_cent == 0,
       "rho_zeta + d_x J = Gam rho with J = -eps Im(psi* psi_x); momentum density obeys K_zeta = Gam K + d_x(...) "
       "(Euler-Lagrange test of the remainder: 0); centroid: d/dzeta int x rho = Gam int x rho + eps int K. Hence "
       "E = E0 e^{Gam zeta}, Omega_c = const, T_c' = eps Omega_c without noise, for any pulse")

(OUT / "symbolic.json").write_text(json.dumps(res, indent=1))
print("all symbolic checks pass:", all(r["pass"] for r in res.values()))
