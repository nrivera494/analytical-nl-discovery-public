"""Second-order (Raman^2) modal drift of the fundamental for a parabolic GRIN mode set with RJ populations.

Formula (exploration note section 3.4; linear-gain multimode Langmuir equation, no Kerr, equal spectral widths sigma):
  dN_p/N_p = (g1^2 z^2 sigma^2 / 2) [ s_p^2 - sum_q S_pqpq P_q s_q ],   s_p = sum_q S_pqpq P_q,  g1 = 2 gamma0 fR T1,
with S normalized to S_0000 = 1 (gamma0 is the fundamental-mode coefficient). Modes: Hermite-Gauss u_mn of the
parabolic profile, groups g = m + n, linear energies eps_g = g * dbeta; populations RJ n_p = T/(eps_p - mu).
Outputs the second-order modal Raman length L2 = sqrt(2 / (g1^2 sigma^2 |bracket_0|)) and, for comparison,
the in-band spectral-drift length L_R^spec = 1/(g1 sigma^2/sigma * s_mean) = 1/(g1 sigma s_mean).
usage: python grin_second_order.py  (writes grin_second_order.json)
"""
import json
import math

import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.special import eval_hermite, factorial

G = 10                       # groups 0..G-1 -> G(G+1)/2 modes
x, wq = hermgauss(80)        # integrate f(x) e^{-x^2}


def h2(m, xx):
    """|h_m(x)|^2 e^{x^2/1}: Hermite function squared without its Gaussian, for weight e^{-x^2}."""
    return eval_hermite(m, xx) ** 2 / (2.0 ** m * factorial(m) * math.sqrt(math.pi))


# 1-D overlap I_mm' = int h_m^2 h_m'^2 dx with h_m = H_m(x) e^{-x^2/2}/norm: product has weight e^{-2x^2}
xs, ws = x / math.sqrt(2), wq / math.sqrt(2)
I = np.array([[np.sum(ws * h2(m, xs) * h2(k, xs)) for k in range(G)] for m in range(G)])
modes = [(m, g - m) for g in range(G) for m in range(g + 1)]
M = len(modes)
S = np.array([[I[a[0], b[0]] * I[a[1], b[1]] for b in modes] for a in modes])
S /= S[0, 0]
grp = np.array([m + n for m, n in modes])

gamma0, fR, tau1, tau2 = 1.15e-3, 0.18, 0.0122, 0.032          # /W/m, ps
T1 = 2 * tau1 ** 2 * tau2 / (tau1 ** 2 + tau2 ** 2)
g1 = 2 * gamma0 * fR * T1
out = {"G": G, "M": M, "S_00qq_by_group": {int(g): float(S[0][grp == g].mean()) for g in range(G)}, "cases": []}
for P_W in (1e3, 1e4):
    for frac0 in (0.1, 0.3, 0.6):
        # RJ with eps_g = g (units of dbeta); find mu < 0 giving the requested fundamental fraction at fixed T scale
        def frac(mu):
            n = 1.0 / (grp - mu)
            return n[0] / n.sum()
        lo, hi = -1e6, -1e-9
        for _ in range(200):
            mid = -math.sqrt(lo * hi) if lo < 0 and hi < 0 else 0.5 * (lo + hi)
            (lo, hi) = (mid, hi) if frac(mid) < frac0 else (lo, mid)
        mu = 0.5 * (lo + hi)
        n = 1.0 / (grp - mu)
        Pq = P_W * n / n.sum()
        s = S @ Pq
        bracket = s ** 2 - S @ (Pq * s)
        for sigma in (1.0, 5.0):      # rad/ps (t_c = 1 ps, 200 fs)
            coeff = g1 ** 2 * sigma ** 2 / 2          # per m^2 per W^2
            rel = coeff * bracket                     # dN_p/N_p per z^2
            L2 = math.sqrt(1.0 / abs(rel[0])) if rel[0] != 0 else float("inf")
            s_mean = float(np.sum(Pq * s) / P_W)
            LRspec = 1.0 / (g1 * sigma * s_mean)
            grp_rel = {int(g): float((rel[grp == g] * Pq[grp == g]).sum() / Pq[grp == g].sum()) for g in range(G)}
            out["cases"].append(dict(P_W=P_W, fundamental_fraction=frac0, mu_over_dbeta=mu, sigma_radps=sigma,
                                     dF0_over_F0_per_m2=float(rel[0]), sign0=int(np.sign(rel[0])),
                                     L2_m_for_unit_relative_change=L2, LR_spec_m=LRspec, L2_over_LRspec=L2 / LRspec,
                                     group_rel_per_m2=grp_rel,
                                     photon_conservation_residual=float(np.sum(rel * Pq) / P_W)))
json.dump(out, open("grin_second_order.json", "w"), indent=1)
print("modes", M, "S_00qq by group:", {k: round(v, 3) for k, v in out["S_00qq_by_group"].items()})
for c in out["cases"]:
    print("P=%5.0f W F0=%.1f sigma=%.0f: dF0/F0 = %+.3e z^2 /m^2 ; L2 = %.0f m ; L_R^spec = %.0f m ; L2/LRspec = %.2f ; cons=%.1e"
          % (c["P_W"], c["fundamental_fraction"], c["sigma_radps"], c["dF0_over_F0_per_m2"], c["L2_m_for_unit_relative_change"],
             c["LR_spec_m"], c["L2_over_LRspec"], c["photon_conservation_residual"]))
