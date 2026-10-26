#!/usr/bin/env python3
# agent: claude-interactive.20; model: claude-opus-5-5; family: claude. Task T-20261019-claude-interactive.20-01.
# Re-derivation check for the manuscript (not a run; no simulation beyond a seconds-long reduced-model integration).
# Symbolic re-derivation of the cruxes (claude-interactive.20). No simulation.
import sympy as sp
z, G_, l, tau, Gam, eps, A = sp.symbols('zeta Gamma l tau Gamma_ epsilon A', positive=True)
# 1. Block equations -> second-order equation on the asymptote a = A e^{tau/3}, tau = Gamma*zeta
Gm = sp.symbols('Gm', positive=True)
a = sp.Function('a')(z); q = sp.Function('q')(z); p = sp.Function('p')(z)
L = sp.symbols('L', positive=True)  # l(l+1)
# p' = e^{Gm z}/a * q ; q' = -L/a^2 p ; eliminate p
pexpr = -a**2*sp.diff(q, z)/L
eq = sp.diff(pexpr, z) - sp.exp(Gm*z)/a*q
# use a'' = 2 e^{Gm z}/a^2  -> e^{Gm z} = a'' a^2/2
eq = sp.simplify(eq.subs(sp.exp(Gm*z), sp.diff(a, z, 2)*a**2/2))
print('eliminated (should be prop. to q\'\' + 2a\'/a q\' + L a\'\'/(2a) q):', sp.simplify(sp.expand(-eq*L/a**2)))
# on asymptote
Ast = sp.Symbol('Ast', positive=True)
asym = Ast*sp.exp(Gm*z/3)
cond = sp.simplify(sp.diff(asym, z, 2) - 2*sp.exp(Gm*z)/asym**2)
print('asymptote condition A*^3 =', sp.solve(cond, Ast**3) if False else sp.solve(sp.Eq(Ast**3, sp.solve(cond*asym**2*sp.exp(-Gm*z), Ast)[0]**3), Ast**3))
lam = sp.symbols('lambda')
char = lam**2 + sp.Rational(2, 3)*lam + L/18
print('roots:', sp.solve(char, lam))
# 2. constant drift in (u, w) = (e^{tau/3} n, eps e^{-tau/3} p): B^2 = -nu^2 I
B = sp.Matrix([[sp.Rational(1, 3), -L/(Gam*A**2)], [1/(Gam*A), -sp.Rational(1, 3)]])
print('B^2 =', sp.simplify((B*B).subs(A, (18/Gam**2)**sp.Rational(1, 3))))
# 3. spectral component on asymptote: s = n - L eps p/(a a'), a a' = (Gam/3) A^2 e^{2tau/3}; n_tau = -eps L p/(Gam A^2 e^{2 tau/3})
nt = sp.Symbol('n_tau'); pp = sp.Symbol('p'); nn = sp.Symbol('n')
s = nn - L*eps*pp/((Gam/3)*A**2*sp.exp(2*tau/3))
print('s - (n + 3 n_tau) =', sp.simplify(s - (nn + 3*(-eps*L*pp/(Gam*A**2*sp.exp(2*tau/3))))))
# l = 1 Jordan block: n1 = (c1 + c2 tau) e^{-tau/3}; s1 = n1 + 3 n1'
c1, c2 = sp.symbols('c1 c2')
n1 = (c1 + c2*tau)*sp.exp(-tau/3)
print('s_1 =', sp.simplify(n1 + 3*sp.diff(n1, tau)))
# 4. intensity-weighted mean phase: pbar = p0 + p2 * int (1-x^2) P2 / int (1-x^2)
x = sp.symbols('x')
P2 = sp.legendre(2, x)
print('pbar coefficient of p2:', sp.integrate((1-x**2)*P2, (x, -1, 1))/sp.integrate(1-x**2, (x, -1, 1)))
# 5. short-length criterion: <P>_P for parabola and Gaussian; R=1 second-order coefficient
P0 = sp.Symbol('P0', positive=True)
par = P0*(1-x**2)
print('parabola <P>_P =', sp.simplify(sp.integrate(par**2, (x, -1, 1))/sp.integrate(par, (x, -1, 1))))
gau = P0*sp.exp(-x**2)
print('gaussian <P>_P =', sp.simplify(sp.integrate(gau**2, (x, -sp.oo, sp.oo))/sp.integrate(gau, (x, -sp.oo, sp.oo))))
# second-order expansion of the matched-mode eigenvalue, dispersionless, local covariance per slot
g, nsp, k, zz = sp.symbols('g n_sp k z', positive=True)
V = sp.Matrix(2, 2, lambda i, j: sp.Function(f'V{i}{j}')(zz))
K = sp.Matrix([[0, 0], [k*sp.exp(g*zz), 0]])
rhs = g*V + K*V + V*K.T + (2*nsp-1)*g*sp.eye(2)
V0 = sp.eye(2)
V1 = rhs.subs({V[i, j]: V0[i, j] for i in range(2) for j in range(2)}).subs(zz, 0)
# second derivative: d/dz rhs = g V' + K' V + K V' + V' K^T + V K'^T
Kp = sp.diff(K, zz)
V2 = (g*V1 + Kp.subs(zz, 0)*V0 + K.subs(zz, 0)*V1 + V1*K.subs(zz, 0).T + V0*Kp.subs(zz, 0).T)
print('V1 =', sp.simplify(V1)); print('V2 =', sp.simplify(V2))
# average over slots: <k> = kb, <k^2> = k2; v = (1,-1)/sqrt2
kb, k2 = sp.symbols('kbar k2', positive=True)
V1a = V1.subs(k, kb); V2a = sp.Matrix([[V2[0, 0], V2[0, 1].subs(k, kb)], [V2[1, 0].subs(k, kb), V2[1, 1].subs(k**2, k2).subs(k, kb)]])
v = sp.Matrix([1, -1])/sp.sqrt(2)
lam1 = sp.simplify((v.T*V1a*v)[0]); c2coef = sp.simplify((v.T*V2a*v)[0]/2)
print('dlam/dz =', lam1, '; z^2 coefficient =', sp.expand(c2coef))
# at R=1: kbar = 2 nsp g; k2 = 4 g^2 (VarP + nsp^2), VarP = Var_P(gamma P/g)
VarP = sp.Symbol('VarP')
print('(gz)^2 coefficient at R=1:', sp.simplify(c2coef.subs({kb: 2*nsp*g, k2: 4*g**2*(VarP + nsp**2)})/g**2))
# parabola and Gaussian Var_P(P)/<P>_P^2
for name, prof, lim in [('parabola', par, (x, -1, 1)), ('gaussian', gau, (x, -sp.oo, sp.oo))]:
    m1 = sp.integrate(prof**2, lim)/sp.integrate(prof, lim); m2 = sp.integrate(prof**3, lim)/sp.integrate(prof, lim)
    rel = sp.simplify((m2 - m1**2)/m1**2)
    for ns in (1, 2):
        print(name, 'n_sp =', ns, ': coefficient =', sp.nsimplify(2*rel*ns**2 - ns), '=', float(2*rel*ns**2 - ns))
