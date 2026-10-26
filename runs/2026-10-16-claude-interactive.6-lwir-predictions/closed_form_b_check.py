"""Symbolic-residual check of C-20261016-claude-interactive.6-01 (b) inside the reduced model (no GNLSE):
exact N(w)/N0 = (1 - Lambda(w)/N0^4)^(1/4) from quadrature of Lambda = 4 int alpha/K dw (linear-T_R K, Z75, const Aeff,
main-case launch), against the closed form [1 - exp(-(w - w_inf)/w_eff)]^(1/4) with w_eff = -1/(d ln(4 alpha/K)/dw)
evaluated at w_inf, and the terminal condition alpha(w_inf) = K(w_inf) N0^4 / (4 w_eff)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

fz = StepIndexFiber("ZrF4", 3.75, 0.30, n=600, n2=2.1e-20)
rz = OscillatorRaman(0.20, 0.0209, 0.053)
B = 92.0; A = 1.0 * np.exp(B / 4.2)
alpha = lambda w: edge_loss(w, A, B)
wp = wl_to_w(2.8)
aeff0 = float(fz.aeff_um2(np.array([wp]))[0])
gfun = lambda w: fz.n2 * np.asarray(w) / C_M_PS / (aeff0 * 1e-12)
b2 = abs(fz.beta2(np.array([wp]))[0]); g0 = gfun(wp)
T0 = 0.020
N0 = 2 * b2 / (g0 * T0) / (HBAR * wp * 1e24)
w = np.linspace(wl_to_w(6.0), wp, 200001)
f = 4 * alpha(w) / gordon_K(fz, rz, w, gamma_fn=gfun)          # 4 alpha / K
Lam = np.concatenate([np.cumsum((0.5 * (f[1:] + f[:-1]) * np.diff(w))[::-1])[::-1], [0.0]])   # int_w^wp
k = int(np.argmin(np.abs(Lam - N0 ** 4)))
w_inf = w[k]
slope = np.gradient(np.log(f), w)[k]
w_eff = -1 / slope
out = {"N0_photons": N0, "lambda_inf_um": float(w_to_wl(w_inf)), "w_eff_rad_per_ps": float(w_eff),
       "w_edge_rad_per_ps": 2 * np.pi * C_UM_PS / B,
       "terminal_condition_ratio": float(alpha(np.array([w_inf]))[0] /
                                         (gordon_K(fz, rz, np.array([w_inf]), gamma_fn=gfun)[0] * N0 ** 4 / (4 * w_eff))),
       "rows": []}
for x in [0.1, 0.25, 0.5, 1.0, 2.0, 4.0]:
    wq = w_inf + x * w_eff
    j = int(np.argmin(np.abs(w - wq)))
    exact = max(1 - Lam[j] / N0 ** 4, 0) ** 0.25
    closed = (1 - np.exp(-x)) ** 0.25
    out["rows"].append({"x_over_w_eff": x, "lambda_um": float(w_to_wl(w[j])), "N_over_N0_exact": float(exact),
                        "N_over_N0_closed_form": float(closed), "diff": float(closed - exact)})
json.dump(out, open(os.path.join(HERE, "closed_form_b_check.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
