"""Summarize run 2026-10-04-claude-b.1-bandpass-1546-1553-20m into summary.json.

Reads the raw TOML output under ~/analytical-nl-discovery-data/<run-id>/ and compares it with the pre-registered
archive values in config.toml / preregistration.md. Usage: ~/agent-work/venv/bin/python summarize.py
"""
import json
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11 (the repo venv is 3.9)
    import tomli as tomllib

HERE = Path(__file__).resolve().parent
RUN_ID = HERE.name
RAW = Path.home() / "analytical-nl-discovery-data" / RUN_ID
cfg = tomllib.loads((HERE / "config.toml").read_text())
arch = cfg["archive"]


def rel(a, b):
    return (a - b) / abs(b)


def load(name):
    f = RAW / (name + ".toml")
    return tomllib.loads(f.read_text()) if f.exists() else None


KEYS = ["F_filter", "raman_F_increment", "F_without_reservoir", "dB_intrinsic", "mean_photons_after_filter",
        "spectral_transmission", "power_after_ideal_bandpass_mw", "pin_mw", "input_fwhm_measured_on_grid_ps",
        "input_peak_W", "photon_drift", "temporal_edge_fraction", "filter_vacuum_variance", "initial_variance",
        "nt", "window_ps", "dz", "raman_z_spacing", "edge_10_90_nm", "adjoint_seconds", "forward_seconds"]
PAIRS = {  # this-run label -> archive table
    "agarwal_nominal_edge0.5": "agarwal_nominal_edge05",
    "agarwal_nominal_edge0.0": "agarwal_nominal_edge00",
    "agarwal_coarse_edge0.5": "agarwal_coarse_edge05",
    "anisotropic_nominal_edge0.5": "anisotropic_nominal_edge05",
}

summary = {
    "run_id": RUN_ID,
    "task": "T-20261004-claude-interactive-06",
    "problem": "P-20261004-root-03",
    "agent": "claude-b.1",
    "case": "3 (pre-registered): long-pulse LP01 condition (3 nm prefilter, about 25.064 mW coupled, 1.23 ps FWHM), "
            "20 m GIF625 at 1550 nm, direct detection after a 1546.5-1553.5 nm output bandpass",
    "raw_location": str(RAW),
    "preregistration_commit": "4c79445",
    "results": {},
    "comparison_with_archive": {},
    "convergence": {},
    "checks": {},
}
labels = []
for g in cfg["grids"]:
    for e in g["edges_nm"]:
        labels.append(f"{g['kind']}_{g['tag']}_edge{float(e)}")
    if g["total_photon_check"]:
        labels.append(f"{g['kind']}_{g['tag']}_total")
labels.append("agarwal_wide_fixed_input_edge0.5")  # wide_fixed_input_check.jl
for lab in labels:
    d = load(lab)
    if d is None:
        continue
    summary["results"][lab] = {k: d[k] for k in KEYS if k in d}
    N = d["mean_photons_after_filter"]
    summary["results"][lab]["F_input_vacuum"] = d["initial_variance"] / N
    summary["results"][lab]["F_partition_vacuum"] = d["filter_vacuum_variance"] / N
    if lab in PAIRS:
        a = arch[PAIRS[lab]]
        cmp = {}
        for k, v in a.items():
            if k in d and isinstance(v, (int, float)):
                cmp[k] = {"this_run": d[k], "archive": v, "rel_diff": rel(d[k], v), "abs_diff": d[k] - v}
        summary["comparison_with_archive"][lab] = {"archive_file": a["file"], **cmp}
    if lab.endswith("_total"):
        summary["checks"][lab] = {"what": "all wavelengths (T=1) on the same propagation; expected F=1, Raman part ~0",
                                  "F": d["F_filter"], "F_minus_1": d["F_filter"] - 1.0,
                                  "F_Raman": d["raman_F_increment"]}

R = summary["results"]
base = R.get("agarwal_nominal_edge0.5")
for tag, what in (("fine", "nt 8192->16384 at fixed 80 ps window (half the sample spacing), dz 5->2.5 mm, Raman spacing 25->12.5 mm"),
                  ("wide", "window 80->160 ps at fixed 9.765625 fs sample spacing, same dz and Raman spacing; "
                           "input rebuilt from the measured spectrum on the finer frequency grid"),
                  ("wide_fixed_input", "window 80->160 ps at fixed sample spacing with the nominal input zero-padded "
                                       "in time (wide_fixed_input_check.jl)"),
                  ("coarse", "archive power-sweep grid: nt 4096, 40 ps, dz 10 mm, Raman spacing 50 mm")):
    e = R.get(f"agarwal_{tag}_edge0.5")
    if base and e:
        summary["convergence"][f"agarwal_{tag}_vs_nominal"] = {
            "what": what,
            "F_abs_change": e["F_filter"] - base["F_filter"],
            "F_rel_change": rel(e["F_filter"], base["F_filter"]),
            "F_Raman_rel_change": rel(e["raman_F_increment"], base["raman_F_increment"]),
            "P_band_rel_change": rel(e["power_after_ideal_bandpass_mw"], base["power_after_ideal_bandpass_mw"]),
            "pin_rel_change": rel(e["pin_mw"], base["pin_mw"]),
        }

# Derived numbers quoted in the exploration note. beta2 and gamma are the same fiber model's values, recorded by
# run 2026-10-04-claude-b.1-prepared-sech-readout-20m (physics_at(1550) is identical in both drivers).
import math  # noqa: E402

osc, ani = R.get("agarwal_nominal_edge0.5"), R.get("anisotropic_nominal_edge0.5")
c2 = json.loads((HERE.parent / "2026-10-04-claude-b.1-prepared-sech-readout-20m" / "summary.json").read_text())
if osc and ani and "derived" in c2:
    b2 = abs(c2["derived"]["beta2_ps2_per_m"]); gam = c2["derived"]["gamma_per_W_m"]
    T0 = osc["input_fwhm_measured_on_grid_ps"] / (2 * math.acosh(math.sqrt(2)))
    LD = T0 ** 2 / b2
    N2 = gam * osc["input_peak_W"] * T0 ** 2 / b2
    summary["derived"] = {
        "Raman_share_of_F_oscillator": osc["raman_F_increment"] / osc["F_filter"],
        "Raman_share_of_F_anisotropic": ani["raman_F_increment"] / ani["F_filter"],
        "F_ratio_anisotropic_over_oscillator": ani["F_filter"] / osc["F_filter"],
        "sech_equivalent_T0_ps_from_grid_FWHM": T0,
        "sech_FWHM_over_T0": 2 * math.acosh(math.sqrt(2)),
        "dispersion_length_m": LD,
        "zeta": cfg["setting"]["length_m"] / LD,
        "N_squared_from_peak_power": N2,
        "N": math.sqrt(N2),
        "beta2_ps2_per_m_from_run": -b2,
        "gamma_per_W_m_from_run": gam,
        "note": "indicative only: the input is a filtered measured spectrum, not a sech",
    }

(HERE / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
print(json.dumps(summary["comparison_with_archive"], indent=1))
print(json.dumps(summary["convergence"], indent=1))
print(json.dumps(summary["checks"], indent=1))
