"""Refined attack on C-20261017-gpt-d-02 at small/moderate Q (claude-interactive.8): larger windows, more starts.
Maximizes rho at fixed Q over positive intensities p = s^2 (oscillator r = 0.38125, tau1 = 1 units)."""
import json, numpy as np
from scipy import fft as sfft
from scipy.optimize import minimize
rng = np.random.default_rng(20261018)
r = 0.38125; a = r; k = a * a + 1; tau2 = 1 / a; w0 = np.sqrt(k)
W_osc = lambda Om: 2 * a * k * Om**2 / ((k - Om**2) ** 2 + 4 * a * a * Om**2)
F = lambda tq: 2 / np.pi * np.arctan(np.pi * tq / 2)
rows = []
for tq in [0.01, 0.03, 0.1, 0.3]:
    Qt = tq / tau2
    M = 8192; dt = min(0.25, 8 / Qt / M)
    t = (np.arange(M) - M // 2) * dt
    Om = 2 * np.pi * sfft.fftfreq(M, dt); Wk = W_osc(Om)
    def obj(s, mu=400.0):
        p = s * s; E = p.sum() * dt; P = sfft.fft(p) * dt
        S = np.sum(Wk * np.abs(P) ** 2) / (M * dt); Q = (p * p).sum() * dt / E**2
        dS = 2 / M * np.real(sfft.fft(Wk * np.conj(P)))
        dQ = 2 * p * dt / E**2 - 2 * Q * dt / E
        J = -np.log(2 / k * S / E**2) + mu * np.log(Q / Qt) ** 2
        dJ = (-(dS / S - 2 * dt / E) + 2 * mu * np.log(Q / Qt) * dQ / Q) * 2 * s
        return J, dJ
    env = np.exp(-(t * Qt / 2) ** 2)
    starts = {f"random{j}": np.abs(rng.normal(size=M)) * env + 1e-3 for j in range(3)}
    for sig in [0.6]:
        tr = sum(np.exp(-((t - m * 2 * np.pi / w0) / sig) ** 2 / 2) for m in range(-int(1.5 / Qt), int(1.5 / Qt) + 1))
        starts[f"train{sig}"] = np.sqrt(tr * env) + 1e-3
    starts["cos"] = np.sqrt((1 + np.cos(w0 * t)) * env) + 1e-3
    best = None
    for nm, s0 in starts.items():
        res = minimize(obj, s0, jac=True, method="L-BFGS-B", options={"maxiter": 2500, "maxfun": 5000})
        p = res.x**2; E = p.sum() * dt; P = sfft.fft(p) * dt
        rho = 2 / k * np.sum(Wk * np.abs(P) ** 2) / (M * dt) / E**2; Q = (p * p).sum() * dt / E**2
        row = {"tau2Q_target": tq, "start": nm, "tau2Q": tau2 * Q, "rho": rho, "F": F(tau2 * Q), "ratio": rho / F(tau2 * Q), "nit": int(res.nit)}
        print(row, flush=True)
        if best is None or row["ratio"] > best["ratio"]:
            best = row
    rows.append(best); print(best, flush=True)
json.dump({"r": r, "seed": 20261018, "M": 8192, "best": rows, "max_ratio": max(b["ratio"] for b in rows)},
          open("summary_optimizer_refine.json", "w"), indent=1)
