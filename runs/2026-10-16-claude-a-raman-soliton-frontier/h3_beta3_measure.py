#!/usr/bin/env python3
"""Relaxed-assumption check for H3 with third-order dispersion d3 = beta3/(6|beta2|T0) (and self-steepening).
With d3 != 0 the leading soliton sits at W_c where the local normalized GVD is D = 1 + 6 d3 W_c (red = positive W), so the
ZS content computed with the nominal dispersion is not its soliton content. Three content measures are reported:
  f1_ZS_nominal  = 4 eta1/E (nominal ZS, as in h3_scan.measure),
  f1_ZS_local    = 4 eta1' sqrt(D)/E, eta1' from ZS on the window with time rescaled by sqrt(D) (local-dispersion soliton),
  f1_window      = windowed energy / E;
and for s != 0 the photon-number versions (divide by 1 - s W_c). Photon number is checked with the corrected sign.
Usage: python h3_beta3_measure.py out.json"""
import json, sys
import numpy as np
from gnlse import GNLSE
from zs import Grid, leading_fast

OMEGA0 = 2 * np.pi * 299.792458 / 1550.0


def zs_window(g, u, N, stretch=1.0):
    q = N * u
    k = int(np.argmax(np.abs(q)))
    amp = np.abs(q[k]); half = max(6.0 / max(amp, 1e-3), 1.0)
    sel = np.abs(g.t - g.t[k]) <= half
    qw = q[sel]; tw = g.t[sel] - g.t[k]
    W = np.fft.fftfreq(len(qw), g.dt) * 2 * np.pi
    Qw = np.fft.fft(qw); wc = np.sum(W * np.abs(Qw) ** 2) / np.sum(np.abs(Qw) ** 2)
    qz = qw * np.exp(-1j * wc * tw)
    nz = len(qz); dt_s = g.dt / stretch
    qpad = np.zeros(2 * nz, complex); qpad[nz // 2: nz // 2 + nz] = qz
    gz = Grid(2 * nz, 2 * nz * dt_s)
    z, _, _ = leading_fast(gz, qpad, sigma=1j * (np.abs(qpad).max() + 0.3))
    return float(z.imag), float(wc), float(np.sum(np.abs(qw) ** 2) * g.dt)



if __name__ == "__main__":
    out = sys.argv[1]
    rows = []
    for N in (2, 3, 4):
        for s_on, d3 in ((False, 0.0), (False, 0.02), (False, 0.05), (True, 0.05)):
            T0 = 100.0
            s = 1 / (OMEGA0 * T0) if s_on else 0.0
            g = GNLSE(8192, 160.0, N, T0, raman=True, s=s, d3=d3)
            u0 = (1 / np.cosh(g.t)).astype(complex)
            h = 0.4 / (N * (2 * N - 1)) ** 2
            u, _ = g.propagate(u0, int(round((4.0 / N) / h)) * h, h)
            E = 2 * N**2
            eta, wc, Ew = zs_window(g, u, N)
            D = 1 + 6 * d3 * wc
            eta_loc, _, _ = zs_window(g, u, N, stretch=np.sqrt(D))
            qd = 1 - s * wc
            row = {"N": N, "T0_fs": T0, "s": s, "d3": d3, "W_c": wc, "D_local": D,
                   "f1_ZS_nominal": 4 * eta / E, "f1_ZS_local": 4 * eta_loc * np.sqrt(D) / E, "f1_window": Ew / E,
                   "f1_ZS_local_photon": 4 * eta_loc * np.sqrt(D) / E / qd, "f1_window_photon": Ew / E / qd,
                   "photon_drift": g.photons(u) / g.photons(u0) - 1}
            rows.append(row)
            print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
