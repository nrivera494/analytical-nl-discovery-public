#!/usr/bin/env python3
"""Symbolic check of the displaced-thermal Kerr optimum, R-0010 (i).

agent: claude-interactive.16; model: claude-opus-5-5; family: claude (the proposer's family).
No simulation: sympy series, then a comparison with committed numbers of run 2026-10-18-gpt-b-kerr-exact.

Exact moments of a displaced thermal input under H = chi N(N-1)/2, as derived by gpt-b
(claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md):
  u_r = exp(-i r tau) - 1,  D_r = 1 - t u_r,  t = (nu - 1)/2,
  <a^r> = alpha^r exp(-i tau r(r-1)/2) D_r^(-r-1) exp(n_d u_r / D_r),   r = 1, 2,
  lambda = 1 + 2 (n_d + t - |<a>|^2) - 2 |<a^2> - <a>^2|.
Scaling of the early shear branch: n_d = eps^-6 and tau = c eps^5, so that the shear s = tau n_d = c n_d^(1/6)
and eps^2 = n_d^(-1/3). The fast phase exp(-i c/eps) carried by each power of <a> is removed before expanding;
it cancels in the moduli.

Usage (from the repository root):  python results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go/repro/derivation.py
"""
import json
from pathlib import Path

import sympy as sp

eps, c, t = sp.symbols("epsilon c t", positive=True)
nu = sp.Symbol("nu", positive=True)
I = sp.I
ORDER = 12  # terms below eps**ORDER are kept inside the brackets; lambda is then exact through eps**5
n = eps**-6
tau = c * eps**5


def trunc(expr, order=ORDER):
    return sp.expand(sp.series(expr, eps, 0, order).removeO())


def exp_series(x, terms=4):
    # x = O(eps^4) in every use below, so four terms reach eps^12
    return sp.expand(sum(x**k / sp.factorial(k) for k in range(terms)))


u1, u2 = sp.exp(-I * tau) - 1, sp.exp(-2 * I * tau) - 1
D1, D2 = 1 - t * u1, 1 - t * u2
E1 = trunc(n * u1 / D1 + I * c / eps)          # slow part of n_d u_1/D_1
E2 = trunc(n * u2 / D2 + 2 * I * c / eps)      # slow part of n_d u_2/D_2

B1sq = trunc(trunc(D1**-4) * trunc(exp_series(2 * E1)))                         # <a>^2 e^{2ic/eps} / n_d
B2 = trunc(trunc(sp.exp(-I * tau)) * trunc(D2**-3) * trunc(exp_series(E2)))     # <a^2> e^{2ic/eps} / n_d
absA2 = trunc(trunc(D1**-2 * sp.conjugate(D1)**-2) * trunc(exp_series(E1 + sp.conjugate(E1))))  # |<a>|^2 / n_d

W = sp.expand(B2 - B1sq)                                  # (<a^2> - <a>^2) e^{2ic/eps} / n_d, O(eps^4)
P = trunc(sp.expand(W * sp.conjugate(W)) * eps**-8, ORDER - 4)
p0 = sp.simplify(P.subs(eps, 0))
x = sp.expand((P - p0) / p0)                              # O(eps^4), so three terms of sqrt(1+x) suffice
absW = sp.expand(sp.sqrt(p0) * trunc(1 + x / 2 - x**2 / 8 + x**3 / 16, ORDER - 4) * eps**4)

lam = sp.expand(1 + 2 * (n + t - n * absA2) - 2 * n * absW)
coef = {k: sp.factor(sp.simplify(lam.coeff(eps, k).subs(t, (nu - 1) / 2))) for k in range(-2, 6)}
print("lambda = sum_k C_k eps^k with eps = n_d^(-1/6) and s = c n_d^(1/6):")
for k, v in coef.items():
    print(f"  C_{k} = {v}")

lam2 = nu / (4 * c**2) + 2 * nu**2 * c**4
assert sp.simplify(coef[2] - lam2) == 0, "leading term differs from nu/(4c^2) + 2 nu^2 c^4"
assert all(coef[k] == 0 for k in (-2, -1, 0, 1, 3)), "unexpected lower-order or eps^3 term"
cstar = (16 * nu) ** sp.Rational(-1, 6)                  # minimizer of the leading term: c^6 = 1/(16 nu)
lead = sp.simplify(lam2.subs(c, cstar) / nu ** sp.Rational(4, 3))
nxt = sp.simplify(coef[4].subs(c, cstar) / lam2.subs(c, cstar) / nu ** sp.Rational(1, 3))
print("optimum: lambda_* = A (nu^4/n_d)^(1/3) [1 + B nu^(1/3) n_d^(-1/3) + ...]")
print(f"  A = {sp.nsimplify(lead)} = {sp.N(lead, 15)}   (3/(2*4^(1/3)) = {sp.N(sp.Rational(3, 2) / 4**sp.Rational(1, 3), 15)})")
print(f"  B = {sp.nsimplify(nxt)} = {sp.N(nxt, 15)}   (4^(-1/3) = {sp.N(4**sp.Rational(-1, 3), 15)})")

# Compare the next-order term with gpt-b's exact optima (committed, run 2026-10-18-gpt-b-kerr-exact).
root = Path(__file__).resolve().parents[4]
rows = json.loads((root / "runs/2026-10-18-gpt-b-kerr-exact/exact_summary.json").read_text())["rows"]
A, B = float(lead), float(nxt)
print("exact relative excess over the leading law, against B nu^(1/3) n_d^(-1/3) (1 <= nu <= 30, n_d >= 1e8):")
for r in rows:
    nu_, nd = r["nu"], r["n"]
    if nu_ > 30 or nd < 1e8:
        continue
    rel = r["exact"]["lambda"] / (A * (nu_**4 / nd) ** (1 / 3)) - 1
    pred = B * nu_ ** (1 / 3) * nd ** (-1 / 3)
    print(f"  nu={nu_:<3} n_d={nd:.0e}  exact {rel:.6f}  next-order {pred:.6f}  ratio {rel / pred:.4f}")
