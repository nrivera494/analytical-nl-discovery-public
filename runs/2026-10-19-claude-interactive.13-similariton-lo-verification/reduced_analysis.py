"""Parts (i) and (iii) of C-20261019-pi-chatgpt-02 in the reduced model (reduced.py).
Writes reduced_summary.json here and the arrays to the raw-data folder."""
import json, os
import numpy as np
from reduced import run, lo_quantities

RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-19-claude-interactive.13-similariton-lo-verification")
os.makedirs(RAW, exist_ok=True)
OMEGA = np.sqrt(2) / 3            # l=2 log-gain frequency on the asymptote
T_CROSS = 2 * np.pi / OMEGA       # period of the p0-p2 cross term (13.33)
T_VAR = np.pi / OMEGA             # period of Var(p2) (6.66)
dt = 0.005
taus = np.arange(dt, 80 + dt / 2, dt)

cases = {
    "G18_asym": dict(Gam=np.sqrt(18), ap0_zeta=np.sqrt(18) / 3, note="Gamma=sqrt18, seed on the asymptote (a=1, da/dzeta=Gamma/3)"),
    "G18_unchirped": dict(Gam=np.sqrt(18), ap0_zeta=0.0, note="Gamma=sqrt18, unchirped parabolic seed (C-20261008-claude-a-02 main case)"),
    "G1_unchirped": dict(Gam=1.0, ap0_zeta=0.0, note="Gamma=1, unchirped parabolic seed (held-out amplifier of C-20261008-claude-a-02)"),
    "G1_asymchirp": dict(Gam=1.0, ap0_zeta=1.0 / 3, note="Gamma=1, seed chirp da/dzeta=Gamma/3 (not on the asymptote: A_G=2.62)"),
}


def ls_slope(x, y):
    return np.polyfit(x, y, 1)[0]


def window(r, lo, hi):
    return (r["tau"] >= lo - 1e-9) & (r["tau"] <= hi + 1e-9)


def interp(r, key, t):
    return np.interp(t, r["tau"], r[key])


summary = {"model": "reduced Legendre l=0,2 hydrodynamic covariance with intensity-quadrature ASE (reduced.py)",
           "grid": {"dtau": dt, "tau_max": 80, "rtol": 1e-12}, "cases": {}}
for name, cfg in cases.items():
    out = run(cfg["Gam"], ap0_zeta=cfg["ap0_zeta"], taus=taus)
    np.savez(os.path.join(RAW, f"reduced_{name}.npz"), tau=taus, **{k: v for k, v in out.items()})
    cs = {"note": cfg["note"], "Gamma": cfg["Gam"]}
    for nsp in (1.0, 2.0):
        r = lo_quantities({k: v.copy() for k, v in out.items()}, taus, nsp, eps0=0.05)
        lnC = np.log(r["e2CPP"])
        d = {}
        # (i) least-squares power of eps0^2 C_PP against G
        for lo, hi in ((12, 26), (26, 40), (40, 60), (60, 80)):
            m = window(r, lo, hi)
            d[f"power_ls_{lo}_{hi}"] = ls_slope(taus[m], lnC[m])
        # equal-phase powers: endpoints one cross-term period apart, starting phases inside 12..26
        starts = np.linspace(12, 26 - T_CROSS, 9)
        ep = [(np.interp(t + T_CROSS, taus, lnC) - np.interp(t, taus, lnC)) / T_CROSS for t in starts]
        d["power_equal_phase_12_26"] = {"period": T_CROSS, "starts": starts.tolist(), "powers": ep,
                                        "min": min(ep), "max": max(ep)}
        starts2 = np.linspace(40, 80 - T_CROSS, 9)
        ep2 = [(np.interp(t + T_CROSS, taus, lnC) - np.interp(t, taus, lnC)) / T_CROSS for t in starts2]
        d["power_equal_phase_40_80"] = {"min": min(ep2), "max": max(ep2)}
        # local slope range
        loc = np.gradient(lnC, taus)
        for lo, hi in ((12, 26), (40, 80)):
            m = window(r, lo, hi)
            d[f"local_power_range_{lo}_{hi}"] = [loc[m].min(), loc[m].max()]
        # prefactor ratio C_PP / [(32 nsp/9) G Phi^2]
        d["ratio_i_at"] = {str(t): float(interp(r, "ratio_i", t)) for t in (2, 4, 6, 12, 20, 26, 40, 60, 80)}
        for lo, hi in ((12, 26), (40, 80)):
            m = window(r, lo, hi)
            d[f"ratio_i_range_{lo}_{hi}"] = [r["ratio_i"][m].min(), r["ratio_i"][m].max()]
        # error exponent: envelope of |ratio-1| over successive cross-term periods vs G
        env_t, env_v = [], []
        t0 = 12.0
        while t0 + T_CROSS <= 80:
            m = window(r, t0, t0 + T_CROSS)
            k = np.argmax(np.abs(r["ratio_i"][m] - 1))
            env_t.append(taus[m][k]); env_v.append(np.abs(r["ratio_i"][m][k] - 1))
            t0 += T_CROSS
        d["ratio_err_envelope"] = {"tau": env_t, "abs_err": env_v,
                                   "fitted_exponent_vs_G": ls_slope(np.array(env_t), np.log(env_v))}
        # (iii) G^{-1/3} lambda_min
        gl = r["lam_lead"] * np.exp(-taus / 3)
        gle = r["lam_eps"] * np.exp(-taus / 3)
        for lo, hi in ((12, 26), (26, 80)):
            m = window(r, lo, hi)
            d[f"Gm13_lam_lead_range_{lo}_{hi}"] = [gl[m].min(), gl[m].max()]
            d[f"Gm13_lam_eps005_range_{lo}_{hi}"] = [gle[m].min(), gle[m].max()]
        d["lam_lead_at"] = {str(t): float(interp(r, "lam_lead", t)) for t in (2, 4, 6, 12, 26)}
        d["one_m_r2_at"] = {str(t): float(interp(r, "one_m_r2", t)) for t in (2, 4, 6, 12, 18, 26)}
        m = window(r, 12, 26)
        d["one_m_r2_power_ls_12_26"] = ls_slope(taus[m], np.log(r["one_m_r2"][m]))
        d["CAA_exact_check_maxrelerr"] = float(np.max(np.abs(r["CAA"] / (2 * nsp * np.exp(taus) - (2 * nsp - 1)) - 1)))
        # bright-field: Phi_NL^2 = theta^2/eps0^2 (eps0=0.05); divide by N0
        d["PhiNL2_eps005_at"] = {str(t): float(interp(r, "PhiNL2_over_N0_times_N0", t)) for t in (0.02, 2, 4, 6, 12, 26)}
        d["e2CPP_at"] = {str(t): float(interp(r, "e2CPP", t)) for t in (2, 4, 6, 12, 26)}
        cs[f"nsp{int(nsp)}"] = d
        np.savez(os.path.join(RAW, f"reduced_{name}_nsp{int(nsp)}_lo.npz"), **{k: v for k, v in r.items()})
    summary["cases"][name] = cs


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(f"{float(o):.10g}")
    return o


with open("reduced_summary.json", "w") as f:
    json.dump(clean(summary), f, indent=1)
for name in cases:
    for ns in ("nsp1", "nsp2"):
        d = summary["cases"][name][ns]
        print(name, ns, "LS power 12-26 %.5f | 40-60 %.6f | 60-80 %.7f" % (d["power_ls_12_26"], d["power_ls_40_60"], d["power_ls_60_80"]),
              "| eqphase 12-26 [%.5f, %.5f]" % (d["power_equal_phase_12_26"]["min"], d["power_equal_phase_12_26"]["max"]),
              "| ratio 12-26 [%.4f, %.4f] 40-80 [%.5f, %.5f]" % (*d["ratio_i_range_12_26"], *d["ratio_i_range_40_80"]),
              "| err exp %.3f" % d["ratio_err_envelope"]["fitted_exponent_vs_G"],
              "| G^-1/3 lam 12-26 [%.4f, %.4f] 26-80 [%.4f, %.4f]" % (*d["Gm13_lam_lead_range_12_26"], *d["Gm13_lam_lead_range_26_80"]),
              "| 1-r2 power %.4f" % d["one_m_r2_power_ls_12_26"])
