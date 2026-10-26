"""Compare the solver's beta2 = 0 map (case b0, and b0_* diagnostics) with the exact
time-local Kerr map on the same grid, and recompute lambda_min / lambda_gen for that ideal map
with the same amplitude-quadrature procedure as sdc_lib.jl.

Ideal per-bin map (phi_j = gamma L |A0_j|^2, real input field):
  dA_out = exp(i phi) [dA + 2 i phi Re(dA)]  ->  [a'; b'] = R(phi) [[1, 0], [2 phi, 1]] [a; b].

Usage: ~/agent-work/venv/bin/python runs/2026-10-10-claude-a-solver-dispersion-check/ideal_b0_compare.py [case ...]
Writes <raw>/ideal_compare_<case>.json and prints the numbers.
"""
import json
import os
import sys

import numpy as np

RUN_ID = "2026-10-10-claude-a-solver-dispersion-check"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}")
PHI = 5.0


def amplitude_covariance(V, Abar, pad=4, thresh=1e-6):
    N = len(Abar)
    Np = pad * N
    off = (Np - N) // 2
    win = off + np.arange(N)
    Ap = np.zeros(Np, complex)
    Ap[win] = Abar
    Ak = np.fft.fft(Ap) / np.sqrt(Np)
    p = np.abs(Ak) ** 2
    kept = np.nonzero(p >= thresh * p.max())[0]
    psi = np.angle(Ak[kept])
    U = np.exp(-2j * np.pi * np.outer(kept, win) / Np) / np.sqrt(Np)
    C = np.exp(-1j * psi)[:, None] * U
    G1 = np.hstack([C.real, -C.imag])
    nk = len(kept)
    Vamp = G1 @ V @ G1.T + (np.eye(nk) - G1 @ G1.T)
    Vamp = 0.5 * (Vamp + Vamp.T)
    return Vamp, kept


def ideal_map(A0):
    phi = PHI * np.abs(A0) ** 2 / np.max(np.abs(A0) ** 2)
    N = len(A0)
    S = np.zeros((2 * N, 2 * N))
    c, s = np.cos(phi), np.sin(phi)
    j = np.arange(N)
    S[j, j] = c - 2 * phi * s
    S[j, N + j] = -s
    S[N + j, j] = s + 2 * phi * c
    S[N + j, N + j] = c
    Abar = A0 * np.exp(1j * phi)
    return S, Abar


def main(cases):
    for case in cases:
        d = np.load(os.path.join(RAW, case + ".npz"))
        S = d["S"]
        Abar = d["Abar_re"] + 1j * d["Abar_im"]
        A0 = d["A0_re"].astype(complex)
        Si, Abar_i = ideal_map(A0)
        Vi = Si @ Si.T
        lam_min_i = np.linalg.eigvalsh(0.5 * (Vi + Vi.T))[0]
        Vamp_i, kept_i = amplitude_covariance(Vi, Abar_i)
        lam_gen_i = np.linalg.eigvalsh(Vamp_i)[0]
        # solver map, same procedure (repeat for a self-consistency check of the Julia numbers)
        V = S @ S.T
        lam_min = np.linalg.eigvalsh(0.5 * (V + V.T))[0]
        Vamp, kept = amplitude_covariance(V, Abar)
        lam_gen = np.linalg.eigvalsh(Vamp)[0]
        # mixed: ideal V with solver mean field / solver V with ideal mean field (attribute differences)
        res = {
            "case": case,
            "ideal_lambda_min": lam_min_i,
            "ideal_lambda_gen": lam_gen_i,
            "ideal_n_bins_kept": int(len(kept_i)),
            "solver_lambda_min_numpy": lam_min,
            "solver_lambda_gen_numpy": lam_gen,
            "solver_n_bins_kept_numpy": int(len(kept)),
            "max_abs_S_minus_ideal": float(np.max(np.abs(S - Si))),
            "rel_fro_S_minus_ideal": float(np.linalg.norm(S - Si) / np.linalg.norm(Si)),
            "max_abs_Abar_minus_ideal_over_peak": float(np.max(np.abs(Abar - Abar_i)) / np.max(np.abs(Abar_i))),
            "rel_diff_lambda_min_solver_vs_ideal": float(lam_min / lam_min_i - 1),
            "rel_diff_lambda_gen_solver_vs_ideal": float(lam_gen / lam_gen_i - 1),
        }
        with open(os.path.join(RAW, f"ideal_compare_{case}.json"), "w") as f:
            json.dump(res, f, indent=2)
        print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:] or ["b0"])
