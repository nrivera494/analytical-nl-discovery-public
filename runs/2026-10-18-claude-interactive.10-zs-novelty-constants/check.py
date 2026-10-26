"""Novelty-audit consistency checks for C-20261018-pi-chatgpt-01, part (A).

Compares the claimed sharp constant C_p and extremizer with two published results:
  (i)  Dolbeault-Gontier-Pizzichillo-Van Den Bosch, Rev. Mat. Iberoam. 40 (2024) 649-692,
       DOI 10.4171/RMI/1443, Theorem 1.3 (d = 1), evaluated at lambda = 0;
  (ii) Cuenin-Laptev-Tretter, Ann. Henri Poincare 15 (2014) 707-736,
       DOI 10.1007/s00023-013-0259-3, Corollary 4.6 with m = 0;
and checks symbolically that, for real q and zeta = i*eta, the ZS system maps onto the
DGPV Dirac system (D_m - V) Psi = lambda Psi at lambda = 0 with m = eta and V = q.
No ZS eigenvalue solver is used: closed forms, quadrature and sympy only.
Writes summary.json next to this file.
"""
import json
import os

import mpmath as mp
import sympy as sp

mp.mp.dps = 40
PS = [1.25, 1.5, 2, 3, 4, 7, 10]
MS = [mp.mpf(1), mp.mpf("0.7")]


def J(p):
    p = mp.mpf(p)
    return mp.sqrt(mp.pi) * mp.gamma(p / 2) / mp.gamma((p + 1) / 2)


def C_claim(p):
    p = mp.mpf(p)
    return p**p / (p - 1) ** (p - 1) * J(p) / 2


def alpha_p_DGPV(lam, p, m):
    """(alpha_D(lambda, p))^p from DGPV Theorem 1.3, eq. (1.10)."""
    p, m, lam = mp.mpf(p), mp.mpf(m), mp.mpf(lam)
    z0 = (m - lam) / (m + lam)
    half = mp.mpf(1) / 2
    return (p**p * ((m + lam) / (p - 1)) ** (p - 1) * z0 ** (p - half)
            * mp.beta(half, p) * mp.hyp2f1(half, p, p + half, -z0))


def V_DGPV(x, lam, p, m):
    """Optimal potential of DGPV Theorem 1.3, eq. (1.10)."""
    p, m, lam = mp.mpf(p), mp.mpf(m), mp.mpf(lam)
    A = p / (p - 1) * (m**2 - lam**2)
    B = 2 / (p - 1) * mp.sqrt(m**2 - lam**2)
    return A / (m * mp.cosh(B * x) + lam)


def q_star(t, p, eta):
    """Claimed extremizer of (A)."""
    p, eta = mp.mpf(p), mp.mpf(eta)
    return p * eta / (p - 1) * mp.sech(2 * eta * t / (p - 1))


def C_CLT(p):
    """CLT Cor. 4.6 at m = 0, rewritten as int ||V||^p >= C_CLT(p) |Im z|^(p-1)."""
    p = mp.mpf(p)
    return (p / (2 * (p - 1))) ** (p - 1)


rows = []
for p in PS:
    for m in MS:
        a_hyp = alpha_p_DGPV(0, p, m)
        a_quad = mp.quad(lambda x: V_DGPV(x, 0, p, m) ** p, [-mp.inf, 0, mp.inf])
        target = C_claim(p) * m ** (mp.mpf(p) - 1)
        pts = [mp.mpf(k) / 3 for k in range(-9, 10)]
        dmax = max(abs(V_DGPV(x, 0, p, m) - q_star(x, p, m)) for x in pts)
        rows.append({
            "p": float(p), "m_equals_eta": float(m),
            "C_claim_times_eta^(p-1)": float(target),
            "DGPV_alpha^p_hypergeometric_eq1.10": float(a_hyp),
            "DGPV_alpha^p_quadrature_of_V": float(a_quad),
            "rel_diff_hypergeometric": float(a_hyp / target - 1),
            "rel_diff_quadrature": float(a_quad / target - 1),
            "max_abs_diff_V_DGPV_minus_q_star_on_grid": float(dmax),
        })

clt = []
for p in [mp.mpf("1.0001"), 1.25, 1.5, 2, 3, 4, 7, 10]:
    clt.append({
        "p": float(p), "C_claim": float(C_claim(p)), "C_CLT_massless": float(C_CLT(p)),
        "ratio_C_claim_over_C_CLT": float(C_claim(p) / C_CLT(p)),
        "p*J_p*2^(p-2)": float(mp.mpf(p) * J(p) * 2 ** (mp.mpf(p) - 2)),
    })

limits = {
    "C_claim_at_p=1.000001": float(C_claim(mp.mpf("1.000001"))),
    "pi_over_2": float(mp.pi / 2),
    "DGPV_alpha_D(0,1)=arccos(0)": float(mp.acos(0)),
    "C_claim_at_p=2": float(C_claim(2)),
}

# ZS (real q, zeta = i eta): v1' = eta v1 + q v2, v2' = -q v1 - eta v2.
# DGPV eq. (5.1) linear version: phi' = -(lambda + m + V) chi, chi' = (lambda - m + V) phi.
t = sp.symbols("t", real=True)
eta = sp.symbols("eta", positive=True)
q = sp.Function("q")(t)
v1 = sp.Function("v1")(t)
v2 = sp.Function("v2")(t)
zs = {v1.diff(t): eta * v1 + q * v2, v2.diff(t): -q * v1 - eta * v2}
phi = v1 - v2
chi = -(v1 + v2)
res1 = sp.simplify(phi.diff(t).subs(zs) + (eta + q) * chi)
res2 = sp.simplify(chi.diff(t).subs(zs) - (q - eta) * phi)

# The claim's explicit bound state (derivation note, Sec. 2): v = R (cos th, -sin th).
P = sp.symbols("p", positive=True)
b = 2 * eta / (P - 1)
th = sp.atan(sp.exp(b * t))
R = sp.sech(b * t) ** ((P - 1) / 2)
qs = P * eta / (P - 1) * sp.sech(b * t)
w1, w2 = R * sp.cos(th), -R * sp.sin(th)
r1 = w1.diff(t) - (eta * w1 + qs * w2)
r2 = w2.diff(t) - (-qs * w1 - eta * w2)
resid = []
for pv in [1.5, 3, 7]:
    for tv in [-2.0, -0.3, 0.0, 0.7, 2.5]:
        sub = {P: pv, eta: 0.8, t: tv}
        resid.append(max(abs(float(r1.subs(sub).evalf(30))), abs(float(r2.subs(sub).evalf(30)))))

out = {
    "DGPV_lambda0_vs_claim": rows,
    "CLT_cor4.6_vs_claim": clt,
    "limits": limits,
    "ZS_to_DGPV_map_symbolic_residuals": [str(res1), str(res2)],
    "claim_bound_state_ZS_residual_max_abs": max(resid),
    "claim_bound_state_ZS_residual_points": "p in {1.5,3,7}, eta = 0.8, t in {-2,-0.3,0,0.7,2.5}",
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "summary.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
