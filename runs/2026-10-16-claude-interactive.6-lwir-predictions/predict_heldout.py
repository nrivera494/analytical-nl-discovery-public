"""Held-out H3 prediction, frozen before any H3 GNLSE run: Z75 fibre, const Aeff, fundamental soliton at 2.8 um with
T0 = 30 fs (E = 6.09 nJ), L = 8 m.  Also the linear-T_R closed form N^4 = N0^4 - Lambda(w) along the same path."""
import sys, json, os
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
out = {}
for T0 in [0.030, 0.020]:
    m = ReachModel(fz, rz, alpha_w=alpha, rate="exact", aeff_const_um2=aeff0, npts=6001)
    b2 = abs(fz.beta2(np.array([wp]))[0]); g = m.gamma(wp)
    E = 2 * b2 / (g * T0); Nph = E / (HBAR * wp * 1e24)
    z, w, Nn, TT = m.integrate(wp, Nph, 8.0, dz=2e-3, n_out=800)
    rec = {"E_pJ": float(E), "T0_fs": T0 * 1e3}
    for zq in [2.0, 4.0, 6.0, 8.0]:
        k = int(np.argmin(abs(z - zq)))
        rec[f"at_{zq}m"] = {"Nsol": float(Nn[k] / Nph), "lam_um": float(w_to_wl(w[k]))}
    for lc in [3.2, 3.3, 3.4, 3.5, 3.6]:
        wc = wl_to_w(lc)
        eta = Nn / Nph * 0.5 * (1 + np.tanh(np.pi * TT / 2 * (wc - w)))
        k = int(np.argmax(eta))
        rec[f"opt_{lc}"] = {"eta_star": float(eta[k]), "L_star_m": float(z[k]), "interior": bool(k < len(z) - 1)}
    # linear-T_R closed form along the model path: N^4 = N0^4 - Lambda(w), Lambda = 4 int alpha/K dw
    ww = np.linspace(w[-1], wp, 4000)
    K = gordon_K(fz, rz, ww, gamma_fn=lambda x: fz.n2 * x / C_M_PS / (aeff0 * 1e-12))
    integrand = 4 * alpha(ww) / K
    Lam = np.array([np.trapezoid(integrand[i:], ww[i:]) for i in range(0, len(ww), 400)])
    rec["closed_form_N_over_N0_at_lam"] = [[float(w_to_wl(ww[i])), float(max(1 - L_ / Nph ** 4, 0) ** 0.25)]
                                           for i, L_ in zip(range(0, len(ww), 400), Lam)]
    out[f"T0_{T0*1e3:.0f}fs"] = rec
json.dump(out, open(os.path.join(HERE, "predictions_heldout.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
