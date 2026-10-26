#!/usr/bin/env python3
"""H3 extensions (frozen predictions in HYPOTHESES.md: H3e at 12:05, H3f at 12:10).
Same model and measurement as h3_scan.py, but the field is propagated in segments and the leading soliton is measured
after each segment, so the excess eps(L) = f1(L)/f1(0) - 1 is followed in L and its saturation is visible.
Modes:
  small   N = 2, 3, 4 at T0 = 400, 800, 1600, 3200 fs, L*N up to 32 (perturbative small-tau_R limit, H3b/H3f)
  dense   N = 2, 3, 4, 5 at T0 = 35, 70, 140, 280, 560 fs, L*N up to 16 (collapse variable, H3f)
  heldout N = 5 at T0 = 100, 200 fs; N = 6 and 8 at 400 and 800 fs, L*N up to 12 (H3e)
  n8peak  N = 8 at T0 = 600, 450 fs on n = 32768 (H3m)
  rshape  N = 3, 4 with two Raman responses of the same T_R (tau1 = 10, 16 fs) (H3k)
  gauss   Gaussian launch, peak 4 (exploration)
  gauss6  Gaussian launch, peak 6 (H3n, held out)
  as2s3   N = 3, 4 with an As2S3-like response, fR = 0.10 (H3o)
  lin     Lin-Agrawal multi-component response, N = 3, 4 (H3s)
  c35     N = 3 and 5 at T0 = 6400 fs (H3r)
  n10     N = 10 at its predicted peak T0 = 870 fs on n = 65536 (verifier prediction of C-02)
  sspeak  self-steepening at the transfer maximum (H3q)
  as2s3fine  finer T0 grid around the As2S3-like peaks (resolves H3o on a finer grid; not a new prediction)
  c5      N = 5 small-tau_R coefficient (H3p)
  n35     N = 3.5 (non-integer, held out, H3j) at T0 = 110-240 fs
  n7fine  N = 7 at T0 = 500 fs on n = 32768 (the n = 16384 row was frequency-limited)
  n8fine  N = 8 at T0 = 800, 400 fs on n = 32768 (Nyquist doubled; the n = 16384 rows were frequency-limited)
  n7      N = 7 at T0 = 500 fs (H3i) and N = 6 at 280, 560 fs
  conv_small  step halving/quartering at the smallest tau_R (N = 2, 3, 4)
  n2long  N = 2 at T0 = 280-6400 fs to L*N = 64-128 (saturation of the N = 2 excess)
  n5peak  N = 5 at T0 = 340, 400 fs (H3g i, ii)
  conv    dt halving and step halving at (N, T0) = (6, 400), (8, 200), (4, 200)
Usage: python h3_ext.py out.json mode"""
import json, sys, time
import numpy as np
from gnlse import GNLSE
from h3_scan import measure
from zs import Grid, leading_fast

out = sys.argv[1]
mode = sys.argv[2]


def evolve(N, T0, Lfacs, raman=True, s=0.0, d3=0.0, hfac=1.0, width=160.0, n=None, tag="", tau1=12.2, tau2=32.0, launch="sech", fR=0.18, response="bw"):
    t00 = time.time()
    if n is None:
        n = 8192 if N <= 4 else 16384
    g = GNLSE(n, width, N, T0, fR=fR, raman=raman, s=s, d3=d3, tau1=tau1, tau2=tau2, response=response)
    if launch == "sech":
        u = (1 / np.cosh(g.t)).astype(complex)
        f10 = (2 * N - 1) / N**2
        E = 2 * N**2
    else:   # Gaussian launch exp(-tau^2/2), peak N in q units; IST content from the ZS eigenvalue of the launch
        u = np.exp(-g.t**2 / 2).astype(complex)
        E = N**2 * np.sqrt(np.pi)
        gz = Grid(768, 26.0)
        z0, _, _ = leading_fast(gz, (N * np.exp(-gz.t**2 / 2)).astype(complex), sigma=1j * (N + 0.3))
        f10 = 4 * float(z0.imag) / E
    p0 = g.photons(u)
    h = hfac * 0.4 / (N * (2 * N - 1)) ** 2
    Lprev = 0.0
    out_rows = []
    Wmax = np.pi / g.dt
    for Lf in Lfacs:
        L = Lf / N
        nseg = int(round((L - Lprev) / h))
        u, _ = g.propagate(u, nseg * h, h)
        Lprev += nseg * h
        m = measure(g, u, N)
        f1 = 4 * m["eta1"] / E
        limited = (abs(m["t_peak"]) > 0.4 * width) or (abs(m["red_shift_W"]) > 0.8 * Wmax)
        row = {"tag": tag, "N": N, "T0_fs": T0, "L_times_N": Lf, "raman": raman, "s": s, "d3": d3, "h": h, "n": n, "width": width,
               "tau1": tau1, "tau2": tau2, "fR": fR, "response": response, "launch": launch, "E": E,
               "f1_input_IST": f10, "f1_output_ZS": f1, "excess": f1 / f10 - 1, "f1_window_energy": m["E_window"] / E,
               "photon_drift": g.photons(u) / p0 - 1, **m, "window_limited": bool(limited), "wall_s": round(time.time() - t00, 1)}
        out_rows.append(row)
        print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
        if limited:
            break
    return out_rows


rows = []


def save():
    json.dump({"mode": mode, "rows": rows}, open(out, "w"), indent=1)


if mode == "small":
    for N in (3, 2, 4):
        for T0 in (400.0, 800.0, 1600.0, 3200.0):
            rows += evolve(N, T0, (4.0, 8.0, 16.0, 32.0), tag="small"); save()
elif mode == "dense":
    for N in (3, 4, 2, 5):
        for T0 in (35.0, 70.0, 140.0, 280.0, 560.0):
            rows += evolve(N, T0, (4.0, 8.0, 16.0), tag="dense"); save()
elif mode == "heldout":
    for N, T0 in ((5, 100.0), (5, 200.0), (6, 400.0), (6, 800.0), (8, 400.0), (8, 800.0)):
        rows += evolve(N, T0, (4.0, 6.0, 8.0, 12.0), tag="heldout"); save()
elif mode == "n8peak":
    for T0 in (600.0, 450.0):
        rows += evolve(8, T0, (2.5, 3.0, 3.5), n=32768, tag="n8peak"); save()
elif mode == "rshape":
    for t1, t2 in ((10.0, 19.495103805976708), (16.0, 58.67602782946432)):
        for N, T0s in ((3, (70.0, 100.0, 140.0, 200.0, 280.0)), (4, (100.0, 140.0, 200.0, 280.0, 400.0))):
            for T0 in T0s:
                rows += evolve(N, T0, (4.0, 8.0), tag=f"rshape tau1={t1}", tau1=t1, tau2=t2); save()
elif mode == "as2s3":
    for N, T0s in ((3, (40.0, 80.0, 160.0, 320.0, 640.0)), (4, (60.0, 120.0, 240.0, 480.0, 960.0))):
        for T0 in T0s:
            rows += evolve(N, T0, (4.0, 8.0, 16.0), tag="as2s3", tau1=15.5, tau2=230.5, fR=0.10); save()
elif mode == "lin":
    for N, T0s in ((3, (70.0, 100.0, 140.0, 200.0, 280.0)), (4, (100.0, 140.0, 200.0, 280.0, 400.0))):
        for T0 in T0s:
            rows += evolve(N, T0, (4.0, 8.0), tag="lin-agrawal", fR=0.245, response="lin"); save()
elif mode == "c35":
    rows += evolve(3, 6400.0, (16.0, 32.0, 64.0), tag="c35"); save()
    rows += evolve(5, 6400.0, (8.0, 16.0, 32.0), tag="c35"); save()
elif mode == "n10":
    rows += evolve(10, 870.0, (2.0, 2.5, 3.0), n=65536, tag="n10"); save()
elif mode == "sspeak":
    OMEGA0 = 2 * np.pi * 299.792458 / 1550.0
    for N, T0 in ((4, 200.0), (6, 400.0)):
        rows += evolve(N, T0, (4.0,), s=1 / (OMEGA0 * T0), tag="sspeak"); save()
elif mode == "as2s3fine":
    for N, T0s in ((3, (120.0, 200.0, 240.0)), (4, (180.0, 300.0, 360.0))):
        for T0 in T0s:
            rows += evolve(N, T0, (4.0, 8.0), tag="as2s3fine", tau1=15.5, tau2=230.5, fR=0.10); save()
elif mode == "c5":
    for T0 in (3200.0, 1600.0):
        rows += evolve(5, T0, (8.0, 16.0, 32.0), tag="c5"); save()
elif mode == "gauss6":
    for T0 in (380.0, 300.0, 460.0):
        rows += evolve(6, T0, (4.0, 6.0), tag="gauss6", launch="gauss"); save()
elif mode == "gauss":
    for T0 in (100.0, 140.0, 200.0, 280.0, 400.0):
        rows += evolve(4, T0, (4.0, 8.0), tag="gauss", launch="gauss"); save()
elif mode == "n35":
    for T0 in (110.0, 140.0, 170.0, 200.0, 240.0):
        rows += evolve(3.5, T0, (4.0, 8.0, 16.0), n=8192, tag="n35"); save()
elif mode == "n7fine":
    rows += evolve(7, 500.0, (3.0, 4.0, 5.0), n=32768, tag="n7fine"); save()
elif mode == "n8fine":
    rows += evolve(8, 800.0, (2.5, 3.0, 4.0), n=32768, tag="n8fine"); save()
    rows += evolve(8, 400.0, (4.0, 6.0), n=32768, tag="n8fine"); save()
elif mode == "n7":
    rows += evolve(7, 500.0, (4.0, 6.0, 8.0), tag="n7"); save()
    for T0 in (560.0, 280.0):
        rows += evolve(6, T0, (4.0, 6.0, 8.0), tag="n6peak"); save()
elif mode == "conv_small":
    for N, T0, Ls in ((2, 3200.0, (64.0, 128.0)), (2, 6400.0, (64.0, 128.0)), (3, 3200.0, (16.0, 32.0)), (4, 3200.0, (16.0, 32.0))):
        rows += evolve(N, T0, Ls, hfac=0.5, tag="h/2"); save()
        rows += evolve(N, T0, Ls, hfac=0.25, tag="h/4"); save()
elif mode == "n2long":
    for T0 in (1600.0, 3200.0, 6400.0):
        rows += evolve(2, T0, (32.0, 64.0, 128.0), tag="n2long"); save()
    for T0 in (280.0, 560.0):
        rows += evolve(2, T0, (16.0, 32.0, 64.0), tag="n2long"); save()
elif mode == "n5peak":
    for T0 in (340.0, 400.0):
        rows += evolve(5, T0, (4.0, 8.0, 16.0), tag="n5peak"); save()
elif mode == "conv":
    for N, T0 in ((4, 200.0), (6, 400.0), (8, 200.0)):
        nb = 8192 if N <= 4 else 16384
        rows += evolve(N, T0, (4.0,), tag="base"); save()
        rows += evolve(N, T0, (4.0,), n=2 * nb, tag="dt/2"); save()
        rows += evolve(N, T0, (4.0,), hfac=0.5, tag="h/2"); save()
        rows += evolve(N, T0, (4.0,), n=2 * nb, width=320.0, tag="window x2"); save()
save()
