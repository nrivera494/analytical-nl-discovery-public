"""Gradient catastrophe of the dispersionless (epsilon = 0) hydrodynamics for rho0 = exp(-tau^2), v0 = 0 (claude-b,
T-20261010-claude-interactive-05). Integrates rho_Z + (rho v)_tau = 0, v_Z + v v_tau + rho_tau = 0 pseudo-spectrally
(RK4, light exponential filter) and records max |v_tau| and max |rho_tau|; the breaking distance Z_b is estimated by
fitting max|v_tau| ~ a / (Z_b - Z) on the approach. Two grids for convergence. Writes gradient_catastrophe.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
fft, ifft = np.fft.fft, np.fft.ifft
out = {}
for Nt, dZ in ((4096, 2e-4), (8192, 1e-4)):
    TW = 40.0
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt); dt = t[1] - t[0]
    k = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    filt = np.exp(-36 * (np.abs(k) / np.abs(k).max()) ** 36)
    D = lambda f: np.real(ifft(1j * k * filt * fft(f)))
    R = np.exp(-t ** 2); V = np.zeros(Nt)
    rhs = lambda R, V: (-D(R * V), -(V * D(V) + D(R)))
    Zs, gv, gr = [], [], []
    Z = 0.0
    while Z < 1.4:
        k1 = rhs(R, V); k2 = rhs(R + 0.5 * dZ * k1[0], V + 0.5 * dZ * k1[1])
        k3 = rhs(R + 0.5 * dZ * k2[0], V + 0.5 * dZ * k2[1]); k4 = rhs(R + dZ * k3[0], V + dZ * k3[1])
        R = R + dZ / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); V = V + dZ / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        Z += dZ
        if not np.all(np.isfinite(R)):
            break
        if int(round(Z / dZ)) % 50 == 0:
            Zs.append(Z); gv.append(float(np.max(np.abs(D(V))))); gr.append(float(np.max(np.abs(D(R)))))
    Zs, gv = np.array(Zs), np.array(gv)
    # fit 1/max|v_tau| = (Z_b - Z)/a on the window where max|v_tau| is between 5 and 50 times its Z = 0.5 value
    g0 = gv[np.argmin(np.abs(Zs - 0.5))]
    m = (gv > 5 * g0) & (gv < 50 * g0)
    fit = np.polyfit(Zs[m], 1 / gv[m], 1) if m.sum() > 3 else [np.nan, np.nan]
    Zb = float(-fit[1] / fit[0]) if m.sum() > 3 else None
    out[f"Nt{Nt}"] = dict(Z_b_fit=Zb, fit_points=int(m.sum()), Z_last=float(Zs[-1]), maxv_tau_last=float(gv[-1]),
                          samples=[(float(z), float(a)) for z, a in zip(Zs[::20], gv[::20])])
    print(Nt, 'Z_b (fit 1/max|v_tau| linear) =', Zb, ' points', int(m.sum()), ' last Z', Zs[-1], 'max|v_tau|', gv[-1], flush=True)
json.dump(out, open(os.path.join(HERE, "gradient_catastrophe.json"), "w"), indent=1)
