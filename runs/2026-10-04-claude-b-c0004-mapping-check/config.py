"""Cheap check of claim C-0004 (dispersion-flipped symmetry mapping) on the pulsed scalar NLSE.

Run id: 2026-10-04-claude-b-c0004-mapping-check (agent claude-b, task T-20261002-claude-interactive-04).

Model (retarded frame, dimensionless: z in units of L_D, T in units of T0):
    dA/dz = -i (b2/2) A_TT + (b3/6) A_TTT + i g_k |A|^2 A + (g/2) A
Forward: amplifier (g > 0). The test asks which map takes the amplifier OUTPUT back to its INPUT:
  (M1)  B_in(T) = conj(A_out(-T)), propagate in the matched absorber (g -> -g), same b2, b3, g_k;
        expect B_out(T) = conj(A_in(-T)).
  (M2)  as M1 but without envelope time reversal: B_in(T) = conj(A_out(T)); expect conj(A_in(T)).
  (C4)  claim C-0004: as M2 but with b2 -> -b2 (dispersion sign flipped).
  (C4r) as M1 but with b2 -> -b2.
The split-step integrator is second-order Strang splitting; the step-size check halves dz.
Writes summary.json next to this file.
"""
import json
import os

import numpy as np


def propagate(A0, T, L, dz, b2, b3, gk, g):
    n = len(T)
    dT = T[1] - T[0]
    w = 2 * np.pi * np.fft.fftfreq(n, d=dT)
    # linear operator in Fourier space for d/dT -> -i w (numpy convention A(T) = sum a(w) e^{-i w T}? use explicit):
    # with numpy fft, A_T  <->  (i w) * fft(A) for ifft(fft(A)*(1j*w)) being the derivative
    D = -1j * (b2 / 2) * (1j * w) ** 2 + (b3 / 6) * (1j * w) ** 3 + g / 2
    half = np.exp(D * dz / 2)
    A = A0.astype(complex).copy()
    nsteps = int(round(L / dz))
    for _ in range(nsteps):
        A = np.fft.ifft(half * np.fft.fft(A))
        A = A * np.exp(1j * gk * np.abs(A) ** 2 * dz)
        A = np.fft.ifft(half * np.fft.fft(A))
    return A


def rel_err(x, y):
    return float(np.linalg.norm(x - y) / np.linalg.norm(y))


def run(dz):
    n, span = 2048, 80.0
    T = (np.arange(n) - n // 2) * (span / n)
    Ain = 1.5 * (1 / np.cosh(T)) * np.exp(-1j * 0.3 * T ** 2)  # chirped sech, N = 1.5 for g_k = 1, b2 = -1
    b2, b3, gk, g, L = -1.0, 0.1, 1.0, 0.4, 2.0
    Aout = propagate(Ain, T, L, dz, b2, b3, gk, g)
    rev = lambda x: np.roll(x[::-1], 1)  # T -> -T on the symmetric grid (index i -> -i mod n)
    out = {}
    B = propagate(np.conj(rev(Aout)), T, L, dz, b2, b3, gk, -g)
    out["M1_conj_timereversal_gainflip"] = rel_err(B, np.conj(rev(Ain)))
    B = propagate(np.conj(Aout), T, L, dz, b2, b3, gk, -g)
    out["M2_conj_gainflip_no_timereversal"] = rel_err(B, np.conj(Ain))
    B = propagate(np.conj(Aout), T, L, dz, -b2, b3, gk, -g)
    out["C4_claim_conj_gainflip_b2flipped"] = rel_err(B, np.conj(Ain))
    B = propagate(np.conj(rev(Aout)), T, L, dz, -b2, b3, gk, -g)
    out["C4r_conj_timereversal_gainflip_b2flipped"] = rel_err(B, np.conj(rev(Ain)))
    # b3 = 0 control: without odd dispersion the time reversal should not matter
    Aout0 = propagate(Ain, T, L, dz, b2, 0.0, gk, g)
    B = propagate(np.conj(Aout0), T, L, dz, b2, 0.0, gk, -g)
    out["M2_b3zero_conj_gainflip_no_timereversal"] = rel_err(B, np.conj(Ain))
    B = propagate(np.conj(Aout0), T, L, dz, -b2, 0.0, gk, -g)
    out["C4_b3zero_claim_b2flipped"] = rel_err(B, np.conj(Ain))
    out["edge_fraction_output"] = float(np.sum(np.abs(Aout[: n // 16]) ** 2 + np.abs(Aout[-n // 16:]) ** 2) / np.sum(np.abs(Aout) ** 2))
    return out


def main():
    res = {"run_id": "2026-10-04-claude-b-c0004-mapping-check",
           "model": "dA/dz = -i(b2/2)A_TT + (b3/6)A_TTT + i g_k|A|^2 A + (g/2)A; b2=-1, b3=0.1, g_k=1, g=0.4, L=2 (units of L_D, T0); input 1.5 sech(T) exp(-0.3 i T^2); 2048 points over 80 T0",
           "dz_1e-3": run(1e-3), "dz_5e-4": run(5e-4)}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "summary.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
