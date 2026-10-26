"""Sensitivity of the HC relaxed-assumption findings to the amplitude convention (A_i/w_i vs A_i)."""
import json, numpy as np, importlib
import hc_response as hc
fs = 1e-15
res = {}
for conv in ["A_over_w", "A"]:
    hc.set_convention(conv)
    y = np.linspace(-14, 8, 1_100_001); Om = 1e14 * np.exp(y)
    W = Om * np.imag(hc.H(Om)); k = hc.KDOT
    tt = np.linspace(0, 8e-12, 800_001); ht = hc.h(tt); mu1 = np.trapz(tt * ht, tt)
    tau2_eff = 2 / k * W.max()
    Fa = lambda tq: 2 / np.pi * np.arctan(np.pi * tq / 2)
    def rho_sech(T):
        yv = np.pi * Om * T / 2
        s2 = np.where(yv < 1e-8, 1.0, (yv / np.sinh(np.minimum(yv, 700))) ** 2)
        return 2 / k * np.trapz(W * s2 * Om, y) / np.pi
    Ts = np.geomspace(1e-15, 2e-12, 60)
    r_eff = [rho_sech(T) / Fa(tau2_eff / (3 * T)) for T in Ts]
    r_32 = [rho_sech(T) / Fa(32e-15 / (3 * T)) for T in Ts]
    res[conv] = {"mu1_fs": mu1 / fs, "TR_fs_fR018": 0.18 * mu1 / fs, "kdot": k, "tau2_eff_fs": tau2_eff / fs,
                 "W_peak_THz": float(Om[W.argmax()] / 2 / np.pi / 1e12),
                 "sech_max_rho_over_arctan_tau2eff": float(max(r_eff)), "at_T_fs": float(Ts[int(np.argmax(r_eff))] / fs),
                 "sech_max_rho_over_arctan_32fs": float(max(r_32)), "at_T_fs_32": float(Ts[int(np.argmax(r_32))] / fs)}
    print(conv, res[conv], flush=True)
json.dump(res, open("summary_convention.json", "w"), indent=1)
