"""Band-limited lambda_min: smallest eigenvalue of V compressed to output quadratures whose
N-point DFT support lies in |omega| <= omega_B (the input side keeps all 2N vacuum modes).

Reason: the solver multiplies the nonlinear term by damped_freq_window(nt), which rolls off over
the top ~1/3 of the positive-detuning band (omega > 0.34 nt domega, 68 rad/ps for nt=512,
53 rad/ps for nt=400). Single-time-bin quadratures have flat spectra, so the full-V lambda_min
sees this window; output modes band-limited well inside the flat region do not.
For beta2 = 0 the same compression of the exact time-local map is computed as a reference.

Usage: ~/agent-work/venv/bin/python runs/2026-10-10-claude-a-solver-dispersion-check/bandlimited.py case ...
Writes <raw>/bandlimited_<case>.json.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ideal_b0_compare import RAW, amplitude_covariance, ideal_map  # noqa: E402

OMEGA_B = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0]


def band_projector(N, dt, omega_b):
    """Rows: Re/Im of unitary DFT coefficients c_k = sum_m F_km (X_m + i Y_m), |omega_k| <= omega_b."""
    omega = 2 * np.pi * np.fft.fftfreq(N, d=dt)
    ks = np.nonzero(np.abs(omega) <= omega_b + 1e-12)[0]
    m = np.arange(N)
    F = np.exp(-2j * np.pi * np.outer(ks, m) / N) / np.sqrt(N)
    Q = np.vstack([np.hstack([F.real, -F.imag]), np.hstack([F.imag, F.real])])
    return Q, len(ks)


def lam_min_band(V, dt, omega_b):
    N = V.shape[0] // 2
    Q, nb = band_projector(N, dt, omega_b)
    VB = Q @ V @ Q.T
    VB = 0.5 * (VB + VB.T)
    return float(np.linalg.eigvalsh(VB)[0]), nb


def main(cases):
    for case in cases:
        d = np.load(os.path.join(RAW, case + ".npz"))
        S = d["S"]
        t = d["t_ps"]
        dt = float(t[1] - t[0])
        N = len(t)
        V = S @ S.T
        res = {"case": case, "nt": N, "dt_ps": dt, "omega_B_rad_per_ps": [], "n_bins_in_band": [],
               "lambda_min_band": [], "nyquist_rad_per_ps": float(np.pi / dt),
               "window_rolloff_start_rad_per_ps": float(0.34 * N * 2 * np.pi / (N * dt))}
        full_ev = float(np.linalg.eigvalsh(0.5 * (V + V.T))[0])
        res["lambda_min_full"] = full_ev
        meta = json.load(open(os.path.join(RAW, case + ".json")))
        ideal = abs(meta["beta2_ps2_per_m"]) == 0.0
        if ideal:
            Si, _ = ideal_map(d["A0_re"].astype(complex))
            Vi = Si @ Si.T
            res["ideal_lambda_min_band"] = []
            res["ideal_lambda_min_full"] = float(np.linalg.eigvalsh(0.5 * (Vi + Vi.T))[0])
        for wb in OMEGA_B:
            if wb > np.pi / dt + 1e-9:
                continue
            lam, nb = lam_min_band(V, dt, wb)
            res["omega_B_rad_per_ps"].append(wb)
            res["n_bins_in_band"].append(nb)
            res["lambda_min_band"].append(lam)
            if ideal:
                res["ideal_lambda_min_band"].append(lam_min_band(Vi, dt, wb)[0])
        # lambda_gen robustness: replace every output mode outside |omega| <= 60 rad/ps by
        # uncorrelated vacuum and recompute lambda_gen. If unchanged, lambda_gen cannot see the
        # solver's anti-alias window (which acts only above 0.34 nt domega).
        Abar = d["Abar_re"] + 1j * d["Abar_im"]
        Vamp, _ = amplitude_covariance(V, Abar)
        lam_gen = float(np.linalg.eigvalsh(Vamp)[0])
        Q, _ = band_projector(N, dt, min(60.0, 0.9 * np.pi / dt))
        P = Q.T @ Q
        Vv = P @ V @ P + (np.eye(2 * N) - P)
        Vamp_v, _ = amplitude_covariance(0.5 * (Vv + Vv.T), Abar)
        lam_gen_v = float(np.linalg.eigvalsh(Vamp_v)[0])
        res["lambda_gen"] = lam_gen
        res["lambda_gen_out_of_band_vacuum"] = lam_gen_v
        res["lambda_gen_rel_change_out_of_band_vacuum"] = lam_gen_v / lam_gen - 1
        with open(os.path.join(RAW, f"bandlimited_{case}.json"), "w") as f:
            json.dump(res, f, indent=1)
        print(f"{case}: lambda_gen {lam_gen:.10g}, with out-of-band (|w|>60) output replaced by vacuum "
              f"{lam_gen_v:.10g} (rel {lam_gen_v / lam_gen - 1:.2e})")
        line = f"{case}: full {full_ev:.8g}"
        for i, wb in enumerate(res["omega_B_rad_per_ps"]):
            line += f" | wB={wb:g}: {res['lambda_min_band'][i]:.8g}"
            if ideal:
                line += f" (ideal {res['ideal_lambda_min_band'][i]:.8g})"
        print(line)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1:])
