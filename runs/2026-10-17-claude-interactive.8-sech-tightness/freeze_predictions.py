"""Freeze the claim-formula values at the verifier's held-out points BEFORE any check is run.

Evaluates only the claimed closed form and the claimed asymptotes (this is the prediction).
Output: predictions.json (committed before quadrature / propagation).
"""
import json
import mpmath as mp
from ramanlib import rho_closed, rho_long_lead, rho_long_two, rho_short_series, F_arctan

mp.mp.dps = 40

R_HELD = [0.1, 0.2275, 0.45, 1.0, 2.5, 5.0]          # 0.2275 = assumed fluoride 9.1 fs/40 fs
X_HELD = [0.0007, 0.05, 0.37, 2.2, 7.5, 33.0, 250.0, 600.0]

out = {"agent": "claude-interactive.8", "family": "claude", "model": "claude-opus-5-5",
       "note": "claim-formula values at verifier-chosen held-out points; frozen before running checks",
       "exact_formula": [], "tolerances": {}}
for r in R_HELD:
    for x in X_HELD:
        out["exact_formula"].append({"r": r, "x": x, "rho_claim": mp.nstr(rho_closed(r, x), 25),
                                     "rho_long_lead": mp.nstr(rho_long_lead(r, x), 25),
                                     "rho_long_two": mp.nstr(rho_long_two(r, x), 25),
                                     "rho_short_x1": mp.nstr(rho_short_series(r, x, 1), 25)})
out["arctan_F"] = [{"tau2Q": q, "F_claim": mp.nstr(F_arctan(q), 25)}
                   for q in [0.003, 0.03, 0.3, 3.0, 30.0, 300.0]]
out["tolerances"] = {
    "exact_vs_quadrature": "relative 1e-9 (both spectral and time-domain quadrature) at every held-out (r,x)",
    "long_leading_relerr_slope": "-2 +- 0.05 for r in {0.1,0.2275,0.45,2.5,5}, fit 8 log-spaced x in [50,400]",
    "long_leading_relerr_slope_r1": "-4 +- 0.15 at r=1 (x^-2 correction cancels), same window",
    "long_two_term_relerr_slope": "-4 +- 0.15 for r != 1, same window",
    "short_gap_ratio_slope": "(1-rho)/(2 r x) - 1 has slope +1 +- 0.05 for all held-out r, fit 8 log-spaced x in [1e-4,1e-2]",
    "short_cubic_residual_slope": "1-rho-2rx-c2 x^2 has slope 3 +- 0.1 for r != 1; 4 +- 0.15 at r = 1",
    "levelset_vs_F": "numerical bathtub maximum over a fine grid equals F within relative 1e-6 at r in {0.38125, 2.0}",
    "profiles": "rho/F <= 1 for every positive-intensity profile in the verifier suite; optimizer best < 1",
    "gnlse_launch_rhs": "sech launch-plane rho from the GNLSE nonlinear operator equals rho_claim within relative 1e-6",
    "gnlse_launch_fd": "Richardson finite-difference dE/dz from short propagation equals closed form within relative 1e-4",
    "gnlse_planes": "rho(z) <= F(Q(z)) <= 1 at every recorded plane of every launch (ratio <= 1 + 1e-6)",
    "gnlse_retention": "E(L)/E0 >= 1/(1+kappa E0 L) and >= 1/(1+kappa E0 L F(Qmax)) with Qmax the observed max over z",
}
json.dump(out, open("predictions.json", "w"), indent=1)
print(len(out["exact_formula"]), "frozen exact-formula points")
