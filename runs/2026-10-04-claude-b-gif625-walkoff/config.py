"""Modal walk-off parameter of nominal GIF625 (ideal parabolic GRIN) at 1400 and 1550 nm.

Run id: 2026-10-04-claude-b-gif625-walkoff (agent claude-b, task T-20261004-root-02).

Re-implements the solver's analytic GRIN propagation constant (solver/src/mmgnlse_fibers.jl, functions
_grin_beta and silica_refractive_index, at the pinned solver commit):
    beta^2 = (k0 n(lambda))^2 - 2 k0 (NA/a) (order + 1),   order = 2p + |l|,
with the Malitson Sellmeier index, core radius a = 31.25 um and NA = 0.275 (the archive's "GIF625 nominal GRIN").
Derivatives in omega are taken with mpmath at 50 digits. The 1400 nm values are checked against the archive's
solver export (research_runs/2026-09-26_analytics/inputs/multimode_1400.toml, by_retained_mode_count.4).

Writes summary.json next to this file. Usage: python config.py
"""
import json
import os

import mpmath as mp

mp.mp.dps = 50
C = mp.mpf(299792458)
A = mp.mpf("31.25e-6")
NA = mp.mpf("0.275")
SECH_FWHM_FACTOR = 2 * mp.acosh(mp.sqrt(2))  # FWHM / T0 for |sech|^2, 1.7627


def n_silica(lam_m):
    l2 = (lam_m * mp.mpf(10) ** 6) ** 2
    return mp.sqrt(1 + mp.mpf("0.6961663") * l2 / (l2 - mp.mpf("0.0684043") ** 2)
                   + mp.mpf("0.4079426") * l2 / (l2 - mp.mpf("0.1162414") ** 2)
                   + mp.mpf("0.8974794") * l2 / (l2 - mp.mpf("9.896161") ** 2))


def beta(omega, order):
    lam = 2 * mp.pi * C / omega
    k0 = omega / C
    return mp.sqrt((k0 * n_silica(lam)) ** 2 - 2 * k0 * NA / A * (order + 1))


def taylor(lam_nm, order):
    w0 = 2 * mp.pi * C / (mp.mpf(lam_nm) * mp.mpf("1e-9"))
    f = lambda w: beta(w, order)
    return {"beta1_ps_per_m": float(mp.diff(f, w0, 1) * mp.mpf(10) ** 12),
            "beta2_ps2_per_m": float(mp.diff(f, w0, 2) * mp.mpf(10) ** 24),
            "beta3_ps3_per_m": float(mp.diff(f, w0, 3) * mp.mpf(10) ** 36)}


def captured_fraction(delta):
    """Weak co-launched sech minority in the sigma=1 potential: |<sech, sech e^{i delta tau}>|^2 / 4."""
    if delta == 0:
        return 1.0
    x = mp.pi * delta / 2
    return float((x / mp.sinh(x)) ** 2)


MODES = [("LP01", 0), ("LP11", 1), ("LP02_LP21", 2), ("LP03", 4)]
# multimode_1400.toml, by_retained_mode_count.4: beta_RWA_frame row 1 (beta1 relative to LP01) and row 2 (beta2)
ARCHIVE_1400 = {
    "dbeta1_ps_per_m": {"LP02_LP21": 0.11817250834155857, "LP03": 0.25418315934803104},
    "beta2_ps2_per_m": {"LP01": -0.011800370204460037, "LP02_LP21": -0.012000731421792296,
                        "LP03": -0.012228836069028087},
}


def main():
    out = {"run_id": "2026-10-04-claude-b-gif625-walkoff",
           "model": "ideal parabolic GRIN, a=31.25 um, NA=0.275, Malitson silica (solver _grin_beta)",
           "wavelengths": {}}
    for lam in (1400, 1550):
        rows = {name: taylor(lam, order) for name, order in MODES}
        b01 = rows["LP01"]
        entry = {"modes": rows, "dbeta1_vs_LP01_ps_per_m": {}, "L_D_m": {}, "delta": {},
                 "captured_fraction_weak_sech": {}}
        for name, _ in MODES[1:]:
            entry["dbeta1_vs_LP01_ps_per_m"][name] = rows[name]["beta1_ps_per_m"] - b01["beta1_ps_per_m"]
        for fwhm_ps in (0.1, 0.2, 0.25, 0.4):
            t0 = mp.mpf(fwhm_ps) / SECH_FWHM_FACTOR
            key = f"sech_fwhm_{fwhm_ps}ps"
            entry["L_D_m"][key] = float(t0 ** 2 / abs(b01["beta2_ps2_per_m"]))
            entry["delta"][key] = {}
            entry["captured_fraction_weak_sech"][key] = {}
            for name, _ in MODES[1:]:
                d = float(entry["dbeta1_vs_LP01_ps_per_m"][name] * t0 / abs(b01["beta2_ps2_per_m"]))
                entry["delta"][key][name] = d
                entry["captured_fraction_weak_sech"][key][name] = captured_fraction(d)
        entry["sech_fwhm_ps_for_delta"] = {
            name: {str(dv): float(dv * abs(b01["beta2_ps2_per_m"])
                                  / entry["dbeta1_vs_LP01_ps_per_m"][name] * SECH_FWHM_FACTOR)
                   for dv in (0.5, 1.0)}
            for name, _ in MODES[1:]}
        out["wavelengths"][str(lam)] = entry

    chk = {}
    w = out["wavelengths"]["1400"]
    for name, ref in ARCHIVE_1400["dbeta1_ps_per_m"].items():
        val = w["dbeta1_vs_LP01_ps_per_m"][name]
        chk[f"dbeta1_{name}"] = {"this_run": val, "archive": ref, "rel_diff": abs(val - ref) / abs(ref)}
    for name, ref in ARCHIVE_1400["beta2_ps2_per_m"].items():
        val = w["modes"][name]["beta2_ps2_per_m"]
        chk[f"beta2_{name}"] = {"this_run": val, "archive": ref, "rel_diff": abs(val - ref) / abs(ref)}
    out["check_vs_archive_1400"] = chk
    out["max_rel_diff_vs_archive"] = max(v["rel_diff"] for v in chk.values())

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    w15 = out["wavelengths"]["1550"]
    print(json.dumps({"max_rel_diff_vs_archive": out["max_rel_diff_vs_archive"],
                      "beta2_LP01_1550_ps2_per_m": w15["modes"]["LP01"]["beta2_ps2_per_m"],
                      "dbeta1_1550": w15["dbeta1_vs_LP01_ps_per_m"],
                      "delta_1550_0.4ps": w15["delta"]["sech_fwhm_0.4ps"],
                      "captured_1550_0.4ps": w15["captured_fraction_weak_sech"]["sech_fwhm_0.4ps"],
                      "fwhm_for_delta_1550": w15["sech_fwhm_ps_for_delta"]}, indent=1))


if __name__ == "__main__":
    main()
