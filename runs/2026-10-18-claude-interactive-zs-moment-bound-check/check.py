"""Orchestrator cheap check of the PI's GPT 6 Pro passive-mask bound on the leading ZS eigenvalue.

Bound: for any ZS bound state with imaginary part eta,  int |q|^p dt >= C_p eta^(p-1)  (p > 1), with
    C_p = p^p / (p-1)^(p-1) * sqrt(pi) Gamma(p/2) / (2 Gamma((p+1)/2)).
With the even-moment Fourier majorant, eta_max(q_m) <= [ int |q_TL|^(2n) / C_(2n) ]^(1/(2n-1)) for every integer n >= 1.
This script evaluates the bound only (closed forms, no ZS eigenvalue solver). It checks:
  (1) integer-order sech, p = 2N: bound equals the TL eigenvalue N - 1/2;
  (2) non-integer sech: ceiling on the relative improvement over TL, min_n U_2n(N)/(N - 1/2) - 1;
  (3) Gaussian q = N exp(-t^2/2): U_G(N) = inf_{p>=2} [N^p sqrt(2 pi/p) / C_p]^(1/(p-1)) and the fraction bound 4 U_G / (sqrt(pi) N^2).
Values reported in the shared chat are compared where it gives them; extra values are frozen for the verifier.
"""
import json
import numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize_scalar


def logC(p):
    return p*np.log(p) - (p-1)*np.log(p-1) + 0.5*np.log(np.pi) + gammaln(p/2) - np.log(2) - gammaln((p+1)/2)


def sech_bound(N, n):
    """U_2n(N) for q = N sech t: [N^(2n) int sech^(2n) / C_2n]^(1/(2n-1)); closed form (2n-1)/(2n) N (N/n)^(1/(2n-1))."""
    p = 2*n
    logI = p*np.log(N) + 0.5*np.log(np.pi) + gammaln(n) - gammaln(n + 0.5)
    direct = np.exp((logI - logC(p))/(p - 1))
    closed = (2*n - 1)/(2*n) * N * (N/n)**(1/(2*n - 1))
    return direct, closed


def gauss_bound(N):
    f = lambda p: (p*np.log(N) + 0.5*np.log(2*np.pi/p) - logC(p))/(p - 1)
    r = minimize_scalar(f, bounds=(2.0 + 1e-9, 2000), method='bounded', options={'xatol': 1e-12})
    return float(np.exp(r.fun)), float(r.x)


out = {"integer_sech": [], "noninteger_sech": [], "gaussian": []}
for N in (1, 2, 3, 4, 5, 6, 8):
    d, c = sech_bound(N, N)
    out["integer_sech"].append({"N": N, "bound_direct": d, "bound_closed": c, "TL_eta": N - 0.5, "rel_diff": d/(N - 0.5) - 1})

chat_nonint = {2.5: 0.43672, 3.5: 0.15446, 5.5: 0.03888, 9.5: 0.00743}   # percent, as stated in the shared chat
for N in (2.5, 3.5, 4.5, 5.5, 7.5, 9.5):
    best = min((sech_bound(N, n)[0], n) for n in range(1, 60))
    ceiling = 100*(best[0]/(N - 0.5) - 1)
    out["noninteger_sech"].append({"N": N, "best_n": best[1], "ceiling_percent": ceiling,
                                   "chat_percent": chat_nonint.get(N), "role": "compare" if N in chat_nonint else "frozen for verifier"})

chat_gauss = {2: 82.65046, 3: 62.12206, 4: 49.13244, 6: 34.41023, 10: 21.42475}   # percent, upper fraction, as stated in the chat
for N in (1.5, 2, 3, 4, 5, 6, 8, 10):
    U, p = gauss_bound(N)
    frac = 100*4*U/(np.sqrt(np.pi)*N**2)
    out["gaussian"].append({"N": N, "best_p": p, "U_G": U, "fraction_bound_percent": frac,
                            "chat_percent": chat_gauss.get(N), "role": "compare" if N in chat_gauss else "frozen for verifier"})

print(json.dumps(out, indent=1))
json.dump(out, open(__file__.replace('check.py', 'summary.json'), 'w'), indent=1)
