"""Relaxed assumption for C-20261017-gpt-d-01/-02: multi-peak Hollenbeck-Cantrell silica response.

(1) response sanity; (2) -01 general moment expansion and short gap with HC; (3) -02 bathtub with HC W,
and whether the arctangent form survives; (4) GNLSE propagation with HC (A3, A5 launches).
claude-interactive.8
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-17-claude-interactive.8-sech-tightness"))
import hc_response as hc  # noqa: E402
from gnlse_pc import GNLSE, sech_launch, osc_H  # noqa: E402

t0 = time.time()
fs = 1e-15
CONV = "A_over_w" if "--A-over-w" in sys.argv else "A"
hc.set_convention(CONV)
out = {"run_id": "2026-10-17-claude-interactive.8-hc-relaxed", "hc_convention": CONV}
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-hc-relaxed")

# ------------------------------------------------------------------ (1) sanity
tt = np.linspace(0, 8e-12, 1_600_001)
ht = hc.h(tt)
dtt = tt[1] - tt[0]
out["hc_integral_h"] = float(np.trapz(ht, tt))
out["hc_kdot"] = hc.KDOT
out["hc_h2dot"] = hc.H2DOT
out["hc_kdot_fd"] = float((ht[1] - ht[0]) / dtt)
y = np.linspace(-14, 8, 1_100_001)
Om = 1e14 * np.exp(y)                    # 8.3e7 .. 3.0e17 rad/s
W = Om * np.imag(hc.H(Om))
out["hc_W_min"] = float(W.min())
out["hc_W_nonneg"] = bool(W.min() >= -1e-12 * W.max())
sumrule = np.trapz(W * Om, y) / np.pi   # int_{-inf}^{inf} W dOm/2pi = (1/pi) int_0^inf W dOm
out["hc_sumrule_ratio"] = float(sumrule / (hc.KDOT / 2))
iW = W.argmax()
out["hc_Om_peak"] = float(Om[iW]); out["hc_W_peak"] = float(W[iW])
tau2_eff = 2 / hc.KDOT * W[iW]           # sup-weight slope: rho <= tau2_eff Q
out["hc_tau2_eff_fs"] = float(tau2_eff / fs)
# local maxima of W on Om>0 (multimodality)
lm = np.where((W[1:-1] > W[:-2]) & (W[1:-1] > W[2:]))[0] + 1
out["hc_W_local_maxima_THz"] = [float(Om[i] / (2 * np.pi) / 1e12) for i in lm]
print("sanity", {k: out[k] for k in out if k.startswith("hc_")}, flush=True)


# ------------------------------------------------------------------ (2) -01 general expansion with HC
def rho_sech_general(T, Om, W, k):
    yv = np.pi * Om * T / 2
    s2 = np.where(yv < 1e-8, 1.0, (yv / np.sinh(np.minimum(yv, 700))) ** 2)
    return 2 / k * np.trapz(W * s2 * Om, np.log(Om)) / np.pi


def moment(j, absval=False):
    f = np.abs(ht) if absval else ht
    return float(np.trapz(tt**j * f, tt))


mu1, mu3, mu5a = moment(1), moment(3), moment(5, True)
k = hc.KDOT
out["hc_mu1_fs"] = mu1 / fs; out["hc_mu3_fs3"] = mu3 / fs**3; out["hc_mu5abs_fs5"] = mu5a / fs**5
Ts = np.geomspace(150e-15, 3e-12, 10)
long_rows = []
for T in Ts:
    rho = rho_sech_general(T, Om, W, k)
    lead = 8 * mu1 / (15 * k * T**3)
    two = lead - 16 * mu3 / (63 * k * T**5)
    bound = 16 * mu5a / (225 * k * T**7)
    long_rows.append({"T_fs": T / fs, "rho": rho, "lead": lead, "two": two, "rel_lead": (rho - lead) / rho,
                      "rel_two": (rho - two) / rho, "R": rho - two, "R_bound": bound,
                      "R_ok": bool(abs(rho - two) <= bound)})
out["hc_long"] = long_rows
sl = lambda xs, ys: float(np.polyfit(np.log(xs), np.log(np.abs(ys)), 1)[0])
sel = [r_ for r_ in long_rows if r_["T_fs"] >= 600]
out["hc_long_rel_lead_slope_T600_3000"] = sl([r_["T_fs"] for r_ in sel], [r_["rel_lead"] for r_ in sel])
out["hc_long_rel_two_slope_T600_3000"] = sl([r_["T_fs"] for r_ in sel], [r_["rel_two"] for r_ in sel])
out["hc_long_remainder_bound_all_ok"] = all(r_["R_ok"] for r_ in long_rows)
# compare with Blow-Wood closed form (tau1 12.2, tau2 32) at the same T
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-17-claude-interactive.8-sech-tightness"))
from ramanlib import rho_closed  # noqa: E402
cmp = []
for T in [5e-15, 10e-15, 20e-15, 50e-15, 100e-15, 300e-15, 1e-12]:
    rh = rho_sech_general(T, Om, W, k)
    rb = float(rho_closed(12.2 / 32, T / 12.2e-15))
    cmp.append({"T_fs": T / fs, "rho_HC": rh, "rho_BW_closed": rb, "HC_over_BW": rh / rb})
out["hc_vs_bw"] = cmp
# short gap: 1-rho ~ -h''(0+) T/k  (generalization of 2T/tau2)
short = []
for T in [0.02e-15, 0.05e-15, 0.1e-15, 0.2e-15, 0.5e-15]:
    rh = rho_sech_general(T, Om, W, k)
    short.append({"T_fs": T / fs, "one_minus_rho": 1 - rh, "pred": -hc.H2DOT * T / k,
                  "ratio": (1 - rh) / (-hc.H2DOT * T / k)})
out["hc_short"] = short
print("mu", mu1 / fs, mu3 / fs**3, mu5a / fs**5, "k", k, "TR=fR*mu1 (fs) at fR .18:", 0.18 * mu1 / fs); print("long", out["hc_long_rel_lead_slope_T600_3000"], out["hc_long_rel_two_slope_T600_3000"],
      out["hc_long_remainder_bound_all_ok"], flush=True)
print("cmp", cmp, flush=True)
print("short", short, flush=True)


# ------------------------------------------------------------------ (3) -02 bathtub with HC W
def bathtub_vals(Om, W, k, Qs):
    yv = np.log(Om)
    dy = np.gradient(yv)
    meas = 2 * Om * dy / (2 * np.pi)
    order = np.argsort(-W)
    cm = np.cumsum(meas[order]); cw = np.cumsum((W * meas)[order])
    res = []
    for Q in Qs:
        j = min(np.searchsorted(cm, Q), len(cm) - 1)
        v = (cw[j - 1] if j > 0 else 0.0) + W[order[j]] * (Q - (cm[j - 1] if j > 0 else 0.0))
        res.append(2 / k * v)
    return np.array(res)


Fa = lambda tq: 2 / np.pi * np.arctan(np.pi * tq / 2)
Qs = np.geomspace(1e-3, 1e3, 121) / tau2_eff
FW = bathtub_vals(Om, W, k, Qs)
r_eff = FW / Fa(tau2_eff * Qs)
r_bw = FW / Fa(32e-15 * Qs)
out["hc_bathtub"] = {"tau2effQ": list(tau2_eff * Qs), "F_W": list(FW), "ratio_FW_over_arctan_tau2eff": list(r_eff),
                     "ratio_FW_over_arctan_tau2_32fs": list(r_bw)}
out["hc_max_FW_over_arctan_tau2eff"] = float(r_eff.max())
out["hc_argmax_tau2effQ"] = float((tau2_eff * Qs)[r_eff.argmax()])
out["hc_max_FW_over_arctan_32fs"] = float(r_bw.max())
out["hc_argmax_32fs_Q_tau2eff"] = float((tau2_eff * Qs)[r_bw.argmax()])
print("bathtub HC: max F_W/F_arctan(tau2eff Q)", out["hc_max_FW_over_arctan_tau2eff"], "at", out["hc_argmax_tau2effQ"],
      "; vs 32 fs:", out["hc_max_FW_over_arctan_32fs"], flush=True)
# same check for the oscillator itself (sanity: should be 1 within discretisation)
Wb = Om * np.imag(osc_H(Om, 12.2e-15, 32e-15)); kb = 1 / (32e-15) ** 2 + 1 / (12.2e-15) ** 2
FWb = bathtub_vals(Om, Wb, kb, Qs)
out["bw_bathtub_max_rel_err"] = float(np.max(np.abs(FWb / Fa(32e-15 * Qs) - 1)))
# sech under HC: rho / F_arctan(tau2eff Q) and rho/F_W
sech_rows = []
for T in np.geomspace(1e-15, 2e-12, 30):
    rh = rho_sech_general(T, Om, W, k)
    Q = 1 / (3 * T)
    fw = bathtub_vals(Om, W, k, [Q])[0]
    sech_rows.append({"T_fs": T / fs, "rho": rh, "F_W": fw, "F_arctan_eff": Fa(tau2_eff * Q),
                      "F_arctan_32": Fa(32e-15 * Q), "rho_over_FW": rh / fw, "rho_over_arctan_eff": rh / Fa(tau2_eff * Q),
                      "rho_over_arctan_32": rh / Fa(32e-15 * Q)})
out["hc_sech"] = sech_rows
out["hc_sech_max_rho_over_FW"] = max(r_["rho_over_FW"] for r_ in sech_rows)
out["hc_sech_max_rho_over_arctan_eff"] = max(r_["rho_over_arctan_eff"] for r_ in sech_rows)
out["hc_sech_max_rho_over_arctan_32"] = max(r_["rho_over_arctan_32"] for r_ in sech_rows)
print("sech HC", out["hc_sech_max_rho_over_FW"], out["hc_sech_max_rho_over_arctan_eff"],
      out["hc_sech_max_rho_over_arctan_32"], flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)

# ------------------------------------------------------------------ (4) propagation with HC
if "--prop" in sys.argv:
    A = dict(lam0=1550e-9, beta2=-21.7e-27, beta3=0.127e-39, n2=2.6e-20, Aeff=80e-12, fR=0.18)
    FWfun_Q = np.geomspace(1e-4, 1e4, 2001) / tau2_eff
    FWfun_V = bathtub_vals(Om, W, k, FWfun_Q)
    prop = {}
    for name, N, fw, L, n, dtfs, ns in [("HC_A3", 3, 100, 0.25, 2**14, 1.0, 4000),
                                         ("HC_A5", 6, 100, 0.15, 2**15, 0.75, 6000),
                                         ("HC_A1", 1, 30, 0.267, 2**14, 1.0, 4000)]:
        sim = GNLSE(n, dtfs * fs, A["lam0"], A["beta2"], A["beta3"], A["n2"], A["Aeff"], A["fR"],
                    Hfun=hc.H, hfun=hc.h, kdot=hc.KDOT)
        A0, T0, P0 = sech_launch(sim, N, fw * fs, A["beta2"])
        rec, AL = sim.run(A0, L, ns, record_every=1)
        Qz = np.array([r_["Q"] for r_ in rec]); rho = np.array([r_["rho_rhs"] for r_ in rec])
        Ez = np.array([r_["E"] for r_ in rec]); zz = np.array([r_["z"] for r_ in rec])
        FWz = np.interp(np.log(Qz), np.log(FWfun_Q), FWfun_V)
        prop[name] = {"N": N, "fwhm_fs": fw, "L_m": L, "planes": len(rho),
                      "max_rho_over_FW": float((rho / FWz).max()),
                      "max_rho_over_arctan_eff": float((rho / Fa(tau2_eff * Qz)).max()),
                      "max_rho_over_arctan_32fs": float((rho / Fa(32e-15 * Qz)).max()),
                      "max_rho": float(rho.max()), "max_tau2eff_Q": float(tau2_eff * Qz.max()),
                      "retention": float(Ez[-1] / Ez[0]),
                      "retention_energy_only": float(1 / (1 + sim.kappa * Ez[0] * L)),
                      "identity_max_rel": float(max(abs(r_["dEdz_rhs"] - r_["dEdz_spec"]) / abs(r_["dEdz_spec"]) for r_ in rec)),
                      "photon_drift": float(rec[-1]["Nph"] / rec[0]["Nph"] - 1)}
        np.savez_compressed(os.path.join(RAW, name + ".npz"), z=zz, Q=Qz, rho=rho, E=Ez, FW=FWz)
        print(name, prop[name], flush=True)
    out["hc_propagation"] = prop
out["wall_s"] = time.time() - t0
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
print("wall", out["wall_s"])
