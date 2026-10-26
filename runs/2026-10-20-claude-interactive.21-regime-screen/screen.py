"""Regime screen for P-20261020-gpt-f-01 (claude-interactive.21, 2026-10-20).

For 50-um / NA 0.2 parabolic GRIN silica fibre, computes the dimensionless groups that decide
which collision null space applies to a random-phase field of coherence time t_c:
  W_t   = t_c^2 / (|beta2| L_NL)   temporal weak-turbulence parameter (Baudin 2022 and Xu 2014
                                    derive their Raman kinetic equations for W_t << 1)
  R_ST  = kappa / (t_c^2 dbeta)    frequency mismatch over one GRIN group spacing; the
                                    spatio-temporal resonances of Zanaglia 2026 need R_ST ~ 1
  R_d   = kappa / (t_c^2 Dbeta)    frequency mismatch over the disorder width; R_d << 1 means the
                                    disorder-broadened resonance does not resolve frequency
with kappa = beta2/2, and the Raman and shock scales. Inputs are in config.json.
Usage: python screen.py config.json summary.json
"""
import json
import math
import sys

c = 299792458.0
hbar = 1.054571817e-34
kB = 1.380649e-23
cfg = json.load(open(sys.argv[1]))


def n_silica(lam_um):
    """Malitson (1965) fused-silica Sellmeier."""
    B = [0.6961663, 0.4079426, 0.8974794]
    C = [0.0684043, 0.1162414, 9.896161]
    l2 = lam_um ** 2
    return math.sqrt(1 + sum(b * l2 / (l2 - cc ** 2) for b, cc in zip(B, C)))


def beta2_material(lam_m):
    """beta2 = lam^3/(2 pi c^2) d2n/dlam2 by central differences on the Sellmeier."""
    h = 1e-9
    f = lambda l: n_silica(l * 1e6)
    d2 = (f(lam_m + h) - 2 * f(lam_m) + f(lam_m - h)) / h ** 2
    return lam_m ** 3 / (2 * math.pi * c ** 2) * d2


# single damped-oscillator Raman response h(t) = A exp(-t/tau2) sin(t/tau1), normalized
t1, t2, fR = cfg["raman_tau1_fs"] * 1e-15, cfg["raman_tau2_fs"] * 1e-15, cfg["fR"]
T1 = 2 * t1 ** 2 * t2 / (t1 ** 2 + t2 ** 2)   # int t h(t) dt
TR = fR * T1
out = {"raman_first_moment_T1_fs": T1 * 1e15, "TR_fs": TR * 1e15, "rows": []}

a = cfg["core_radius_um"] * 1e-6
NA = cfg["NA"]
n2 = cfg["n2_m2_per_W"]
for lam_nm in cfg["wavelengths_nm"]:
    lam = lam_nm * 1e-9
    n = n_silica(lam * 1e6)
    w0 = 2 * math.pi * c / lam
    k = 2 * math.pi * n / lam
    Delta = NA ** 2 / (2 * n ** 2)
    dbeta = math.sqrt(2 * Delta) / a                 # parabolic group spacing
    rho2 = a / (k * math.sqrt(2 * Delta))
    Aeff = 2 * math.pi * rho2
    gamma0 = n2 * w0 / (c * Aeff)
    b2 = beta2_material(lam)
    kappa = b2 / 2
    Omega_ST = math.sqrt(dbeta / kappa)
    dlam_ST = lam ** 2 * Omega_ST / (2 * math.pi * c)
    for P in cfg["peak_power_W"]:
        for fill in cfg["overlap_fill_factor"]:
            LNL = 1 / (gamma0 * fill * P)
            tau_wt = math.sqrt(abs(b2) * LNL)       # t_c at which W_t = 1
            tc_lo = (TR * abs(b2) * LNL) ** (1 / 3)  # (1/W_t)(T_R/t_c) = 1
            for tc_fs in cfg["tc_fs"]:
                tc = tc_fs * 1e-15
                sigma = 1 / tc
                Wt = tc ** 2 / (abs(b2) * LNL)
                row = dict(
                    lam_nm=lam_nm, P_W=P, fill=fill, tc_fs=tc_fs, n=n, Delta=Delta,
                    dbeta_per_m=dbeta, Lbeat_mm=2 * math.pi / dbeta * 1e3,
                    Aeff_um2=Aeff * 1e12, gamma0_perWm=gamma0, beta2_fs2_per_mm=b2 * 1e27,
                    LNL_m=LNL, W_t=Wt, R_ST=kappa / (tc ** 2 * dbeta),
                    R_d={str(D): kappa / (tc ** 2 * D) for D in cfg["Dbeta_per_m"]},
                    kappa_sigma2_per_m=kappa * sigma ** 2,
                    Omega_ST_THz=Omega_ST / (2 * math.pi) / 1e12, dlam_ST_nm=dlam_ST * 1e9,
                    TR_over_tc=TR / tc, shock_1_over_w0tc=1 / (w0 * tc),
                    LR_spec_over_LNL=1 / (2 * TR * sigma),
                    joint_window_tc_fs=[tc_lo * 1e15, tau_wt * 1e15],
                    joint_window_ratio=tau_wt / tc_lo,
                    Lkin_disorder_over_LNL={str(D): {str(S): D * LNL / S ** 2 for S in cfg["Sbar"]}
                                            for D in cfg["Dbeta_per_m"]},
                    Ld_over_LNL={str(D): 1 / (D * LNL) for D in cfg["Dbeta_per_m"]},
                    LD_tc_over_Lkin={str(D): {str(S): (tc ** 2 / abs(b2)) / (D * LNL ** 2 / S ** 2)
                                              for S in cfg["Sbar"]} for D in cfg["Dbeta_per_m"]},
                )
                out["rows"].append(row)

# Noise-seeded Stokes band at the Raman gain peak (added after the first version of this run):
# power gain g_peak = 2 gamma0 fill fR max Im h(Omega) P; threshold length L_th = G_th / g_peak (G_th = 16, CW
# Smith criterion); pump-Stokes walk-off length T_env / (|beta2| Omega_peak) for the listed envelope durations.
import numpy as _np
_W = _np.linspace(1e-3, 300, 300001)  # rad/ps
_t1, _t2 = cfg["raman_tau1_fs"] * 1e-3, cfg["raman_tau2_fs"] * 1e-3  # ps
_h = ((_t1 ** 2 + _t2 ** 2) / (_t1 * _t2 ** 2)) * (1 / _t1) / ((1 / _t2 - 1j * _W) ** 2 + 1 / _t1 ** 2)
_imax = int(_np.argmax(_h.imag))
out["raman_peak"] = dict(Omega_radps=float(_W[_imax]), nu_THz=float(_W[_imax] / (2 * math.pi)), ImH_max=float(_h.imag[_imax]))
srs = []
for r in out["rows"]:
    if r["tc_fs"] != cfg["tc_fs"][0]:
        continue
    g_peak = 2 * r["gamma0_perWm"] * r["fill"] * fR * _h.imag[_imax] * r["P_W"]
    Lth = cfg["srs_threshold_gain"] / g_peak
    b2 = r["beta2_fs2_per_mm"] * 1e-27
    walk = {str(T): T * 1e-12 / (abs(b2) * _W[_imax] * 1e12) for T in cfg["envelope_ps"]}
    Lkin = {D: {S: v * r["LNL_m"] for S, v in d.items()} for D, d in r["Lkin_disorder_over_LNL"].items()}
    srs.append(dict(lam_nm=r["lam_nm"], P_W=r["P_W"], fill=r["fill"], LNL_m=r["LNL_m"], g_peak_perm=g_peak,
                    Lth_m=Lth, Lth_over_LNL=Lth / r["LNL_m"], pump_stokes_walkoff_m=walk, Lkin_m=Lkin,
                    Lkin_over_Lth={D: {S: v / Lth for S, v in d.items()} for D, d in Lkin.items()}))
out["srs"] = srs

# Lead L5: photon occupation per (mode, frequency cell) and the lattice Raman fixed point
out["lattice_theta1_fs"] = hbar / (kB * cfg["lattice_T_K"]) * 1e15
occ = []
w0 = 2 * math.pi * c / 1064e-9
for P in cfg["peak_power_W"]:
    for M in cfg["populated_modes"]:
        for bw in cfg["bandwidth_THz"]:
            nph = P / M / (hbar * w0 * bw * 1e12)
            occ.append(dict(P_W=P, M=M, bandwidth_THz=bw, n_photon_per_cell=nph,
                            spontaneous_over_stimulated=1 / nph))
out["occupation"] = occ
json.dump(out, open(sys.argv[2], "w"), indent=1)

sel = [r for r in out["rows"] if r["lam_nm"] == 1064 and r["fill"] == cfg["overlap_fill_factor"][0]]
r0 = sel[0]
print("T1 = %.3f fs, TR = %.3f fs, lattice theta1 = %.1f fs" % (T1 * 1e15, TR * 1e15, out["lattice_theta1_fs"]))
print("1064 nm: n=%.4f dbeta=%.0f /m Lbeat=%.2f mm Aeff=%.0f um2 gamma0=%.2e /W/m beta2=%.2f fs2/mm "
      "Omega_ST/2pi=%.0f THz dlam_ST=%.0f nm" % (r0["n"], r0["dbeta_per_m"], r0["Lbeat_mm"], r0["Aeff_um2"],
                                                  r0["gamma0_perWm"], r0["beta2_fs2_per_mm"],
                                                  r0["Omega_ST_THz"], r0["dlam_ST_nm"]))
print("%8s %6s %8s %9s %9s %10s %10s %9s %9s %s" % ("P_W", "tc_fs", "LNL_m", "W_t", "R_ST", "R_d(2.6)",
                                                     "R_d(42)", "TR/tc", "1/w0tc", "joint window tc_fs"))
for r in sel:
    print("%8.0f %6.0f %8.3f %9.3g %9.2e %10.3g %10.3g %9.2e %9.2e [%.1f, %.1f] ratio %.2f" % (
        r["P_W"], r["tc_fs"], r["LNL_m"], r["W_t"], r["R_ST"], r["R_d"]["2.6"], r["R_d"]["42"],
        r["TR_over_tc"], r["shock_1_over_w0tc"], r["joint_window_tc_fs"][0], r["joint_window_tc_fs"][1],
        r["joint_window_ratio"]))
print("Raman gain peak: %.1f THz, max Im h = %.3f" % (out["raman_peak"]["nu_THz"], out["raman_peak"]["ImH_max"]))
for q in out["srs"]:
    if q["lam_nm"] == 1064:
        print("P=%6.0f fill=%.1f LNL=%.3f m  L_th=%.2f m (%.0f LNL)  walkoff(1,10 ps)=%s m  Lkin/L_th=%s" % (
            q["P_W"], q["fill"], q["LNL_m"], q["Lth_m"], q["Lth_over_LNL"],
            {k: round(v, 2) for k, v in q["pump_stokes_walkoff_m"].items()},
            {D: {S: round(v, 2) for S, v in d.items()} for D, d in q["Lkin_over_Lth"].items()}))
