"""Summarize run 2026-10-04-claude-b.1-prepared-sech-readout-20m into summary.json.

Reads the raw TOML output under ~/analytical-nl-discovery-data/<run-id>/ and compares it with the archive values
recorded in config.toml. Usage: ~/agent-work/venv/bin/python summarize.py
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


KEYS = ["F_total", "F_signal_input", "F_Raman", "F_reference_vacuum", "readout_output_power_mw",
        "F_total_dB", "reference_power_mw", "source_power_required_both_arms_mw", "fiber_output_power_mw",
        "F_signal_bright_amplitude", "F_signal_bright_phase", "F_signal_orthogonal_both_quadratures",
        "dNout_dNsignal_reference_held_fixed_adjoint", "dNout_dNsignal_reference_held_fixed_finite_difference",
        "reference_blocked_F_total", "reference_blocked_F_Raman", "photon_drift", "temporal_edge_fraction",
        "elapsed_seconds", "nt", "window_ps", "dz_m", "raman_z_spacing_m", "input_field_path",
        "beta2_ps2_km", "gamma_LP01_W_km", "effective_area_um2", "input_peak_W", "input_fwhm_ps",
        "signal_input_power_mw"]

summary = {
    "run_id": RUN_ID,
    "task": "T-20261004-claude-interactive-06",
    "problem": "P-20261004-root-03",
    "agent": "claude-b.1",
    "case": "2: prepared 0.4 ps sech, 36.76796 mW, 20 m GIF625 LP01, coherent input-copy readout "
            "(eta=0.995, r=0.7017289851, psi=-2.181661565 rad, zero delay), full scalar model with Raman",
    "raw_location": str(RAW),
    "results": {},
    "comparison_with_archive": {},
    "convergence": {},
    "checks": {},
}
for c in cfg["cases"]:
    name = c["kind"] + "_" + c["tag"]
    d = load(name)
    if d is None:
        continue
    summary["results"][name] = {k: d[k] for k in KEYS if k in d}
    a = arch.get(name)
    if a:
        cmp = {}
        for k, v in a.items():
            if k in d and isinstance(v, (int, float)) and k != "reference_blocked_F_Raman":
                cmp[k] = {"this_run": d[k], "archive": v, "rel_diff": rel(d[k], v), "abs_diff": d[k] - v}
        summary["comparison_with_archive"][name] = cmp

for kind in ("agarwal", "anisotropic"):
    std, tight, wide = (summary["results"].get(f"{kind}_{t}") for t in ("standard", "tight", "wide"))
    if std and tight:
        summary["convergence"][f"{kind}_tight_vs_standard"] = {
            "what": "nt 4096->8192 at fixed 40 ps window (half the sample spacing), dz 0.01->0.005 m, Raman z spacing 0.05->0.025 m",
            "F_total_abs_change": tight["F_total"] - std["F_total"],
            "F_total_rel_change": rel(tight["F_total"], std["F_total"]),
            "Pout_rel_change": rel(tight["readout_output_power_mw"], std["readout_output_power_mw"]),
        }
    if std and wide:
        summary["convergence"][f"{kind}_wide_vs_standard"] = {
            "what": "window 40->80 ps at fixed 9.765625 fs sample spacing (input zero-padded in time), same dz and Raman spacing",
            "F_total_abs_change": wide["F_total"] - std["F_total"],
            "F_total_rel_change": rel(wide["F_total"], std["F_total"]),
            "Pout_rel_change": rel(wide["readout_output_power_mw"], std["readout_output_power_mw"]),
        }
    if std and "reference_blocked_F_total" in std:
        summary["checks"][f"{kind}_reference_blocked_total_number"] = {
            "expected": 1.0, "F_total": std["reference_blocked_F_total"],
            "F_total_minus_1": std["reference_blocked_F_total"] - 1.0,
            "F_Raman": std["reference_blocked_F_Raman"]}
    if std and std.get("dNout_dNsignal_reference_held_fixed_finite_difference") == std.get(
            "dNout_dNsignal_reference_held_fixed_finite_difference"):  # not NaN
        adj = std["dNout_dNsignal_reference_held_fixed_adjoint"]
        fd = std["dNout_dNsignal_reference_held_fixed_finite_difference"]
        summary["checks"][f"{kind}_adjoint_vs_finite_difference_dN_dN"] = {
            "adjoint": adj, "finite_difference_pm0.05pct": fd, "rel_diff": rel(adj, fd)}
lin = load("agarwal_linear_control")
if lin:
    summary["checks"]["linear_two_port_control"] = {
        "expected": 1.0, "F_total": lin["F_total"], "F_total_minus_1": lin["F_total"] - 1.0,
        "F_signal": lin["F_signal"], "archive_F_total": arch["linear_control"]["F_total"]}

import math  # noqa: E402

# Derived numbers quoted in the exploration note.
osc, ani = summary["results"].get("agarwal_tight"), summary["results"].get("anisotropic_tight")
if osc and ani:
    summary["derived"] = {
        "Raman_share_of_F_oscillator_tight": osc["F_Raman"] / osc["F_total"],
        "Raman_share_of_F_anisotropic_tight": ani["F_Raman"] / ani["F_total"],
        "F_ratio_anisotropic_over_oscillator_tight": ani["F_total"] / osc["F_total"],
        "length_m": cfg["setting"]["length_m"],
        "beta2_ps2_per_m": osc["beta2_ps2_km"] / 1000,
        "gamma_per_W_m": osc["gamma_LP01_W_km"] / 1000,
    }

for kind in ("agarwal", "anisotropic"):
    fd = load("fd_step_check_" + kind)
    if fd is None:
        continue
    rows = sorted(fd["rows"], key=lambda r: -r["relative_power_step"])
    diffs = [r["relative_difference_adjoint_minus_fd"] for r in rows]
    ratios = [diffs[i] / diffs[i + 1] for i in range(len(diffs) - 1)]
    # Richardson extrapolation of the two smallest steps (central difference error ~ step^2).
    f1, f2 = rows[-2]["finite_difference"], rows[-1]["finite_difference"]
    rich = f2 + (f2 - f1) / 3
    adj = rows[-1]["adjoint"]
    summary["checks"][f"{kind}_finite_difference_step_halving"] = {
        "what": "adjoint dN_out/dN_signal vs central finite difference at relative power steps 2e-3 .. 1.25e-4 (standard grid)",
        "steps": [r["relative_power_step"] for r in rows],
        "rel_diff_adjoint_minus_fd": diffs,
        "ratio_per_halving": ratios,
        "exponent_log2_ratio": [math.log2(x) for x in ratios],
        "richardson_extrapolated_fd": rich,
        "adjoint": adj,
        "rel_diff_adjoint_vs_richardson": (adj - rich) / rich,
    }

(HERE / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
print(json.dumps(summary["comparison_with_archive"], indent=1))
print(json.dumps(summary["convergence"], indent=1))
print(json.dumps(summary["checks"], indent=1))
