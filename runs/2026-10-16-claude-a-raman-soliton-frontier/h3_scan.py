#!/usr/bin/env python3
"""H3 (frozen in HYPOTHESES.md, commit 3af8dfa): Raman transfer to the leading soliton in the GNLSE.
TL sech launch q(0) = N sech(tau). Output: ZS content of the largest output soliton (window around the highest peak),
f1(L) = 4 eta1 / E, E = 2 N^2, against the input value f1(0) = (2N-1)/N^2. Controls: Raman off (integrable).
Usage: python h3_scan.py out.json [mode]   mode = main | relaxed | conv"""
import json, sys, time
import numpy as np
from gnlse import GNLSE, h_bw_tilde
from zs import Grid, leading_fast, all_eigs

out = sys.argv[1] if len(sys.argv) > 1 else "h3_scan.json"
mode = sys.argv[2] if len(sys.argv) > 2 else "main"
OMEGA0 = 2 * np.pi * 299.792458 / 1550.0          # rad/fs at 1550 nm


def measure(g, u, N):
    q = N * u
    k = int(np.argmax(np.abs(q)))
    amp = np.abs(q[k])                               # ~ 2 eta for a sech soliton
    half = max(6.0 / max(amp, 1e-3), 1.0)
    sel = np.abs(g.t - g.t[k]) <= half
    qw = q[sel]
    # recentre in time and frequency (remove carrier) for the ZS grid
    tw = g.t[sel] - g.t[k]
    W = np.fft.fftfreq(len(qw), g.dt) * 2 * np.pi
    Qw = np.fft.fft(qw)
    wc = np.sum(W * np.abs(Qw) ** 2) / np.sum(np.abs(Qw) ** 2)
    qz = qw * np.exp(-1j * wc * tw)                 # numpy-centroid removed
    nz = len(qz)
    width = nz * g.dt * 2.0
    npad = 2 * nz
    qpad = np.zeros(npad, complex); qpad[nz // 2: nz // 2 + nz] = qz
    gz = Grid(npad, width)
    z, v, w = leading_fast(gz, qpad, sigma=1j * (np.abs(qpad).max() + 0.3))
    Ewin = np.sum(np.abs(qw) ** 2) * g.dt
    return {"eta1": float(z.imag), "zeta1_re": float(z.real), "peak_amp": float(amp), "t_peak": float(g.t[k]),
            "red_shift_W": float(wc), "E_window": float(Ewin), "window_half": float(half)}


def run(N, T0, Lfac, raman=True, s=0.0, d3=0.0, hfac=1.0, width=160.0, n=None, _depth=0):
    t0 = time.time()
    if n is None:
        n = 8192 if N <= 4 else 16384
    g = GNLSE(n, width, N, T0, raman=raman, s=s, d3=d3)
    u0 = 1 / np.cosh(g.t)
    L = Lfac / N
    h = hfac * 0.1 / (N * (2 * N - 1)) ** 2 * 4.0
    u, _ = g.propagate(u0.astype(complex), L, h)
    m = measure(g, u, N)
    E = 2 * N**2
    f10 = (2 * N - 1) / N**2
    f1 = 4 * m["eta1"] / E
    row = {"N": N, "T0_fs": T0, "L_over_LD": L, "L_times_N": Lfac, "raman": raman, "s": s, "d3": d3, "h": h,
           "f1_input_IST": f10, "f1_output_ZS": f1, "excess": f1 / f10 - 1, "f1_window_energy": m["E_window"] / E,
           "photon_drift": g.photons(u) / g.photons(u0.astype(complex)) - 1, **m, "wall_s": round(time.time() - t0, 1)}
    Wmax = np.pi / g.dt
    limited = (abs(m["t_peak"]) > 0.4 * width) or (abs(m["red_shift_W"]) > 0.8 * Wmax)
    row["width"] = width; row["n"] = n; row["window_limited"] = bool(limited)
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
    if limited and _depth < 2:
        return run(N, T0, Lfac, raman, s, d3, hfac, width=2 * width, n=4 * n if abs(m["red_shift_W"]) > 0.8 * Wmax else 2 * n, _depth=_depth + 1)
    return row


if __name__ == "__main__":
    rows = []
    if mode == "main":
        for N in (2, 3, 4):
            for T0 in (25.0, 50.0, 100.0, 200.0, 400.0):
                for Lfac in (4.0, 8.0):
                    rows.append(run(N, T0, Lfac))
                    json.dump({"rows": rows}, open(out, "w"), indent=1)
            rows.append(run(N, 100.0, 4.0, raman=False))
            json.dump({"rows": rows}, open(out, "w"), indent=1)
        for N, T0s in ((6, (100.0, 200.0, 400.0)), (8, (200.0, 400.0))):
            for T0 in T0s:
                rows.append(run(N, T0, 4.0))
                json.dump({"rows": rows}, open(out, "w"), indent=1)
            rows.append(run(N, 200.0, 4.0, raman=False))
            json.dump({"rows": rows}, open(out, "w"), indent=1)
    elif mode == "conv":
        for N, T0 in ((3, 100.0), (6, 100.0)):
            for hf in (1.0, 0.5):
                rows.append(run(N, T0, 4.0, hfac=hf))
                json.dump({"rows": rows}, open(out, "w"), indent=1)
    elif mode == "relaxed":
        for N in (2, 3, 4, 6):
            T0 = 100.0
            rows.append(run(N, T0, 4.0, s=1 / (OMEGA0 * T0)))
            rows.append(run(N, T0, 4.0, d3=0.02))
            rows.append(run(N, T0, 4.0, d3=0.05))
            rows.append(run(N, T0, 4.0, s=1 / (OMEGA0 * T0), d3=0.05))
            json.dump({"rows": rows}, open(out, "w"), indent=1)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
