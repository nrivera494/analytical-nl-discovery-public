"""Mean field of an unchirped Gaussian in normal dispersion at large N (claude-b, T-20261010-claude-interactive-05).

i u_xi - 1/2 u_tautau + N^2 |u|^2 u = 0, u0 = exp(-tau^2/2); semiclassical variable Z = N xi (z / sqrt(L_D L_NL)).
1. Onset of wave breaking: the first Z at which the output intensity develops an extra local maximum (an oscillation)
   in the wings, with a relative threshold 1e-6 of the peak, for N = 10, 20, 40, 80; compared with the scale
   Z_ref = N xi_wb = N / sqrt(4 N^2 e^{-3/2} - 1) -> 1.0585.
2. Central intensity rho(0, Z) and the accumulated central nonlinear phase Phi_c(Z) = N int_0^Z rho(0, Z') dZ', the
   input of the leading-order lambda_min formula; for N = 10, 20, 40, 80 to show N-independence (hydrodynamic limit).
Writes summary.json."""
import json, os, sys
import numpy as np

fft, ifft = np.fft.fft, np.fft.ifft
HERE = os.path.dirname(os.path.abspath(__file__))


def run(N, Zmax, Nt, TW, phi_step=0.01):
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = t[1] - t[0]
    w = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    N2 = N ** 2
    dxi = phi_step / N2
    nsteps = int(round(Zmax / N / dxi))
    L = np.exp(0.5j * w ** 2 * dxi / 2)
    u = np.exp(-t ** 2 / 2) + 0j
    Zs, rho0, maxima = [], [], []
    for k in range(1, nsteps + 1):
        u = ifft(L * fft(u))
        u = u * np.exp(1j * N2 * np.abs(u) ** 2 * dxi)
        u = ifft(L * fft(u))
        if k % 10 == 0:
            I = np.abs(u) ** 2
            m = (I[1:-1] > I[:-2]) & (I[1:-1] > I[2:]) & (I[1:-1] > 1e-6 * I.max())
            Zs.append(k * dxi * N)
            rho0.append(float(I[Nt // 2]))
            maxima.append(int(m.sum()))
    Zs, rho0, maxima = np.array(Zs), np.array(rho0), np.array(maxima)
    i = np.argmax(maxima > 1)
    Zb = float(Zs[i]) if maxima.max() > 1 else None
    Phi_c = N * np.concatenate([[0.0], np.cumsum(0.5 * (rho0[1:] + rho0[:-1]) * np.diff(Zs))]) + N * Zs[0] * (1 + rho0[0]) / 2
    return dict(N=N, Z_onset=Zb, Z_ref=N / np.sqrt(4 * N ** 2 * np.exp(-1.5) - 1)), Zs, rho0, Phi_c


out = {"rows": [], "rho0": {}}
for N, Nt in ((10, 2048), (20, 4096), (40, 8192), (80, 16384)):
    r, Zs, rho0, Phi_c = run(N, 1.8, Nt, 40.0)
    out["rows"].append(r)
    out["rho0"][str(N)] = dict(Z=Zs[::5].tolist(), rho0=rho0[::5].tolist(), Phi_c_over_N=(Phi_c[::5] / N).tolist())
    print(r, flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
