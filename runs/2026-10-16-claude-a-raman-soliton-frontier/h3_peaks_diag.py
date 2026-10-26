#!/usr/bin/env python3
"""Diagnostic for the leading-soliton identification (assumption 7 of C-20261016-claude-a-02): propagate a TL sech launch,
then list every output peak above 15% of the tallest with its local ZS content (window of half-width max(4/amp, 0.4) T0,
spectral centroid removed), its centroid frequency W_c (red = positive) and its window energy. Raw fields are saved to
~/analytical-nl-discovery-data/<run-id>/peaks_diag/. Usage: python h3_peaks_diag.py out.json N T0 [L*N ...]"""
import json, os, sys
import numpy as np
from gnlse import GNLSE
from zs import Grid, leading_fast

out = sys.argv[1]; N = int(sys.argv[2]); T0 = float(sys.argv[3])
Lfacs = [float(a) for a in sys.argv[4:]] or [4.0]
raw = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-a-raman-soliton-frontier/peaks_diag")
os.makedirs(raw, exist_ok=True)
n = 8192 if N <= 4 else 16384
g = GNLSE(n, 160.0, N, T0, raman=True)
u = (1 / np.cosh(g.t)).astype(complex)
h = 0.4 / (N * (2 * N - 1)) ** 2
E = 2 * N**2
res = []
Lprev = 0.0
for Lf in Lfacs:
    nseg = int(round((Lf / N - Lprev) / h)); u, _ = g.propagate(u, nseg * h, h); Lprev += nseg * h
    np.save(os.path.join(raw, f"N{N}_T0{int(T0)}_LN{int(Lf)}.npy"), u)
    q = N * u; a = np.abs(q)
    pk = [i for i in range(1, n - 1) if a[i] >= a[i - 1] and a[i] >= a[i + 1] and a[i] > 0.15 * a.max()]
    peaks = []
    for i in pk:
        half = max(4.0 / a[i], 0.4)
        sel = np.abs(g.t - g.t[i]) <= half
        qw = q[sel]; tw = g.t[sel] - g.t[i]
        W = np.fft.fftfreq(len(qw), g.dt) * 2 * np.pi
        Qw = np.fft.fft(qw); wc = float(np.sum(W * np.abs(Qw) ** 2) / np.sum(np.abs(Qw) ** 2))
        qz = qw * np.exp(-1j * wc * tw); nz = len(qz)
        qpad = np.zeros(2 * nz, complex); qpad[nz // 2: nz // 2 + nz] = qz
        z, _, _ = leading_fast(Grid(2 * nz, 2 * nz * g.dt), qpad, sigma=1j * (np.abs(qpad).max() + 0.3))
        peaks.append({"t": float(g.t[i]), "amp": float(a[i]), "W_c": wc, "eta": float(z.imag), "zeta_re": float(z.real),
                      "f_ZS": 4 * float(z.imag) / E, "f_window": float(np.sum(np.abs(qw) ** 2) * g.dt / E)})
    peaks.sort(key=lambda p: -p["W_c"])
    res.append({"N": N, "T0_fs": T0, "L_times_N": Lf, "n_peaks": len(peaks), "peaks_by_redshift": peaks[:12]})
    print(f"N={N} T0={T0} LN={Lf}: {len(peaks)} peaks; reddest first:")
    for p in peaks[:8]:
        print(f'   t={p["t"]:8.2f} amp={p["amp"]:6.2f} W_c={p["W_c"]:8.2f} eta={p["eta"]:6.3f} Re z={p["zeta_re"]:+.3f} f_ZS={p["f_ZS"]:.4f} f_win={p["f_window"]:.4f}', flush=True)
    json.dump({"rows": res}, open(out, "w"), indent=1)
