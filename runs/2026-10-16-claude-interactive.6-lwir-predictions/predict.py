"""Frozen reduced-model predictions for H2.2 and H3 (computed before any production GNLSE run).

Run:  ~/agent-work/venv/bin/python predict.py   (numpy/scipy only)
"""
import sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

out = {}
# ---------------- H2.2: isolated fundamental solitons in the SMF-28 model (lossless, constant Aeff = Aeff(1.55 um))
fs = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
rs = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55)
aeff0 = float(fs.aeff_um2(np.array([wp]))[0])
h22 = []
for T0, L in [(0.015, 0.30), (0.020, 0.40), (0.030, 0.60), (0.050, 1.50), (0.080, 4.0)]:
    rec = {"T0_fs": T0 * 1e3, "L_m": L}
    for rate in ["exact", "gordon"]:
        m = ReachModel(fs, rs, alpha_w=None, rate=rate, aeff_const_um2=aeff0)
        b2 = abs(fs.beta2(np.array([wp]))[0]); g = m.gamma(wp)
        Nph = 2 * b2 / (g * T0) / (HBAR * wp * 1e24)
        z, w, Nn, TT = m.integrate(wp, Nph, L, dz=L / 4000)
        rec["shift_" + rate] = float(wp - w[-1])
        rec["Ts_end_fs_" + rate] = float(TT[-1] * 1e3)
    rec["E_pJ"] = float(2 * b2 / (g * T0))
    rec["ratio_exact_over_gordon"] = rec["shift_exact"] / rec["shift_gordon"]
    h22.append(rec)
out["H2.2_fundamental_SMF28"] = h22
out["TR_silica_fs"] = rs.TR() * 1e3
out["aeff0_SMF28_um2"] = aeff0

# ---------------- H3: ZrF4 7.5/125 NA 0.30, fundamental soliton at 2.8 um, T0 = 20 fs,
#                  edge 1 dB/m at 4.2 um (Gauthier 2022), slope B = 92 um (assumed)
fz = StepIndexFiber("ZrF4", 3.75, 0.30, n=600, n2=2.1e-20)
rz = OscillatorRaman(0.20, 0.0209, 0.053)
B = 92.0; A = 1.0 * np.exp(B / 4.2)
alpha = lambda w: edge_loss(w, A, B)
wp2 = wl_to_w(2.8)
aeffz = float(fz.aeff_um2(np.array([wp2]))[0])
res3 = {}
for mode, ac in [("const_aeff", aeffz), ("aeff_w", None)]:
    m = ReachModel(fz, rz, alpha_w=alpha, rate="exact", aeff_const_um2=ac)
    b2 = abs(fz.beta2(np.array([wp2]))[0]); g = m.gamma(wp2)
    T0 = 0.020
    E = 2 * b2 / (g * T0); Nph = E / (HBAR * wp2 * 1e24)
    z, w, Nn, TT = m.integrate(wp2, Nph, 20.0, dz=1e-3, n_out=2000)
    m0 = ReachModel(fz, rz, alpha_w=None, rate="exact", aeff_const_um2=ac)
    z0, w0_, N0_, T0_ = m0.integrate(wp2, Nph, 20.0, dz=1e-3, n_out=2000)
    rec = {"E_pJ": float(E), "N0_photons": float(Nph), "T0_fs": 20.0, "aeff0_um2": aeffz}
    rec["traj_z_lam_Nfrac_Ts"] = [[float(a), float(w_to_wl(b)), float(c / Nph), float(d * 1e3)]
                                  for a, b, c, d in zip(z[::50], w[::50], Nn[::50], TT[::50])]
    Lst = {}
    for lc in [3.3, 3.4, 3.5, 3.6, 3.7]:
        wc = wl_to_w(lc)
        a = np.pi * TT / 2
        frac = 0.5 * (1 + np.tanh(a * (wc - w)))   # photon fraction of a sech^2 spectrum beyond wc
        eta = Nn / Nph * frac
        k = int(np.argmax(eta))
        Lst[str(lc)] = {"L_star_m": float(z[k]), "eta_star": float(eta[k]), "eta_at_20m": float(eta[-1]),
                        "crossing_z_m": float(np.interp(-wc, -w, z)) if w[-1] < wc else None}
    rec["optimum"] = Lst
    rec["lossless_end_lam_um"] = float(w_to_wl(w0_[-1]))
    res3[mode] = rec
out["H3_ZrF4"] = res3
out["H3_edge"] = {"A_dB_per_m_at_lam_inf": float(A), "B_um": B, "w_e_rad_per_ps": 2 * np.pi * C_UM_PS / B}
json.dump(out, open(os.path.join(HERE, "predictions.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "H3_ZrF4"}, indent=1))
for mode in res3:
    print(mode, "E", res3[mode]["E_pJ"], "lossless end", res3[mode]["lossless_end_lam_um"])
    print("  traj (z, lam, N/N0, Ts):", res3[mode]["traj_z_lam_Nfrac_Ts"][::4])
    print("  optimum:", res3[mode]["optimum"])
