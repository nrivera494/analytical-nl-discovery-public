"""Try to exceed the arctangent form with a positive intensity when the response is multi-peak (HC).
Maximize rho_HC / F_arctan(tau2 Q) at fixed Q (tau2 = tau2_eff sup-weight, or 32 fs). Both HC conventions."""
import json, numpy as np, importlib
from scipy import fft as sfft
from scipy.optimize import minimize
import hc_response as hc
fs = 1e-15
rng = np.random.default_rng(20261017)
Fa = lambda tq: 2 / np.pi * np.arctan(np.pi * tq / 2)
res = {}
for conv in ["A_over_w", "A"]:
    hc.set_convention(conv)
    k = hc.KDOT
    y = np.linspace(-14, 8, 400_001); OmF = 1e14 * np.exp(y); WF = OmF * np.imag(hc.H(OmF))
    tau2_eff = 2 / k * WF.max()
    rows = []
    for tau2_name, tau2 in [("tau2_eff", tau2_eff), ("32fs", 32e-15)]:
        for tq in [0.3, 1.0, 2.5, 5.0]:
            Qt = tq / tau2
            M = 4096; dt = min(1e-15, 1 / (60 * Qt))
            t = (np.arange(M) - M // 2) * dt
            Om = 2 * np.pi * sfft.fftfreq(M, dt)
            Wk = Om * np.imag(hc.H(Om))
            def rhoQ(p):
                E = p.sum() * dt; P = sfft.fft(p) * dt
                return 2 / k * np.sum(Wk * np.abs(P) ** 2) / (M * dt) / E**2, (p * p).sum() * dt / E**2
            def obj(s, mu=200.0):
                p = s * s; E = p.sum() * dt; P = sfft.fft(p) * dt
                S = np.sum(Wk * np.abs(P) ** 2) / (M * dt); Q = (p * p).sum() * dt / E**2
                dS = 2 / M * np.real(sfft.fft(Wk * np.conj(P)))
                dlr = dS / S - 2 * dt / E
                dQ = 2 * p * dt / E**2 - 2 * Q * dt / E
                J = -np.log(2 / k * S / E**2) + mu * np.log(Q / Qt) ** 2
                dJ = (-dlr + 2 * mu * np.log(Q / Qt) * dQ / Q) * 2 * s
                return J, dJ
            best = None
            starts = [1 / np.cosh(t * 3 * Qt)] + [np.abs(rng.normal(size=M)) * np.exp(-(t * Qt / 2) ** 2) + 1e-3 for _ in range(5)]
            for s0 in starts:
                r_ = minimize(obj, s0, jac=True, method="L-BFGS-B", options={"maxiter": 4000, "maxfun": 8000})
                rho, Q = rhoQ(r_.x ** 2)
                ratio = rho / Fa(tau2 * Q)
                if best is None or ratio > best["ratio"]:
                    best = {"tau2": tau2_name, "tau2_fs": tau2 / fs, "tau2Q_target": tq, "tau2Q": tau2 * Q, "rho": rho,
                            "F_arctan": Fa(tau2 * Q), "ratio": ratio, "eff_duration_fs": 1 / Q / fs}
            rows.append(best); print(conv, best, flush=True)
    res[conv] = {"tau2_eff_fs": tau2_eff / fs, "best": rows,
                 "max_ratio_tau2_eff": max(r["ratio"] for r in rows if r["tau2"] == "tau2_eff"),
                 "max_ratio_32fs": max(r["ratio"] for r in rows if r["tau2"] == "32fs")}
json.dump(res, open("summary_optimizer_hc.json", "w"), indent=1, default=float)
