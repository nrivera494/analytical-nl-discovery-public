"""C-20261017-gpt-d-02 static checks (claude-interactive.8): numerical bathtub, profile suite, optimizer.

Units tau1 = 1, a = r = tau1/tau2, b = 1.  rho = (2/k) int W |p^|^2 dOm/2pi, Q = int p^2.
"""
import json, time, os
import numpy as np
from scipy import fft as sfft
from scipy.optimize import minimize

t0 = time.time()
rng = np.random.default_rng(20261017)
out = {"run_id": "2026-10-17-claude-interactive.8-concentration", "seed": 20261017}


def W_osc(Om, a, b=1.0):
    w02 = a * a + b * b
    return 2 * a * w02 * Om**2 / ((w02 - Om**2) ** 2 + 4 * a * a * Om**2)


def F(tau2Q):
    return 2 / np.pi * np.arctan(np.pi * tau2Q / 2)


# ------------------------------------------------------------------ 1. numerical bathtub
def bathtub(Wfun, k, Q, ylo=-18, yhi=18, npts=4_000_001, w0=1.0):
    """max (2/k) int W f dOm/2pi over 0<=f<=1, int f dOm/2pi = Q; log grid Om = w0 e^y, both signs."""
    y = np.linspace(ylo, yhi, npts)
    dy = y[1] - y[0]
    Om = w0 * np.exp(y)
    Wv = Wfun(Om)
    meas = 2 * Om * dy / (2 * np.pi)          # both signs, measure in dOm/2pi
    order = np.argsort(-Wv)
    cm = np.cumsum(meas[order])
    j = np.searchsorted(cm, Q)
    val = np.sum(Wv[order[:j]] * meas[order[:j]])
    rem = Q - (cm[j - 1] if j > 0 else 0.0)
    val += Wv[order[j]] * rem
    sel = order[: j + 1]
    return 2 / k * val, Om[sel].min(), Om[sel].max()


lev = []
for r in [0.38125, 2.0]:
    a = r; k = a * a + 1
    for tq in [0.003, 0.03, 0.3, 3.0, 30.0, 300.0]:
        Q = tq * r                              # tau2 = 1/a = 1/r  ->  Q = tau2Q * r
        num, lo, hi = bathtub(lambda Om: W_osc(Om, a), k, Q, w0=np.sqrt(k))
        # claimed band edges: Om+ Om- = k, Om+ - Om- = pi Q
        c = np.pi * Q
        Op = (c + np.sqrt(c * c + 4 * k)) / 2; Om_ = (-c + np.sqrt(c * c + 4 * k)) / 2
        lev.append({"r": r, "tau2Q": tq, "bathtub": num, "F": F(tq), "rel": abs(num - F(tq)) / F(tq),
                    "band_lo": lo, "band_hi": hi, "claimed_lo": Om_, "claimed_hi": Op,
                    "W_edge_claim": 2 * a * k / (c * c + 4 * a * a), "W_edge_num": W_osc(lo, a)})
out["levelset"] = lev
out["levelset_max_rel"] = max(x["rel"] for x in lev)
out["levelset_pass"] = bool(out["levelset_max_rel"] < 1e-6)
print("levelset max rel", out["levelset_max_rel"], flush=True)


# ------------------------------------------------------------------ 2. profile suite
def rho_Q(p, dt, a, b=1.0):
    M = len(p)
    P = sfft.fft(p) * dt
    Om = 2 * np.pi * sfft.fftfreq(M, dt)
    k = a * a + b * b
    E = p.sum() * dt
    S = np.sum(W_osc(Om, a, b) * np.abs(P) ** 2) / (M * dt)
    return 2 / k * S / E**2, (p * p).sum() * dt / E**2


def grid(M, dt):
    return (np.arange(M) - M // 2) * dt


prof = []
for r in [0.38125, 0.2275, 2.0]:
    a = r; tau2 = 1 / a
    for T in [0.05, 0.3, 1.0, 3.0, 10.0]:
        dt = min(T / 40, 0.02); M = int(2 ** np.ceil(np.log2(max(80 * T, 60) / dt)))
        t = grid(M, dt)
        u = t / T
        shapes = {
            "sech2": 1 / np.cosh(u) ** 2,
            "gauss": np.exp(-u**2),
            "supergauss4": np.exp(-u**4),
            "supergauss8": np.exp(-u**8),
            "rect": (np.abs(u) < 1).astype(float),
            "triangle": np.clip(1 - np.abs(u), 0, None),
            "lorentz2": 1 / (1 + u**2) ** 2,
            "pair_incoh_d3": 1 / np.cosh(u - 1.5) ** 2 + 0.5 / np.cosh((u + 1.5) / 0.7) ** 2,
        }
        # coherent pairs with frequency offset / chirp (intensity fringes)
        for dOm in [0.5, 1.0, np.sqrt(a * a + 1), 2.0]:
            A1 = 1 / np.cosh(u - 0.3) * np.exp(-1j * dOm * t / 2)
            A2 = 0.8 / np.cosh(u + 0.3) * np.exp(1j * dOm * t / 2)
            shapes[f"pair_coh_dOm{dOm:.3f}"] = np.abs(A1 + A2) ** 2
        for C in [2.0, 8.0]:
            A1 = np.exp(-u**2 / 2 * (1 + 1j * C)); A2 = np.exp(-(u - 1) ** 2 / 2 * (1 + 1j * C))
            shapes[f"chirped_pair_C{C}"] = np.abs(A1 + A2) ** 2
        # fission-like: three solitons of different widths/amplitudes + weak pedestal
        fis = np.zeros_like(t, dtype=complex)
        for amp, wid, pos, om in [(3.0, 0.3, 0.0, 0.0), (1.5, 0.6, 2.5, 0.4), (0.8, 1.2, -3.0, -0.3)]:
            fis += amp / np.cosh((t / T - pos) / wid) * np.exp(-1j * om * t + 1j * rng.uniform(0, 2 * np.pi))
        fis += 0.1 * np.exp(-(t / (8 * T)) ** 2) * np.exp(1j * rng.uniform(0, 2 * np.pi, len(t)) * 0)
        shapes["fission_like"] = np.abs(fis) ** 2
        for nm, p in shapes.items():
            rho, Q = rho_Q(p, dt, a)
            prof.append({"r": r, "T": T, "shape": nm, "rho": rho, "tau2Q": tau2 * Q, "F": F(tau2 * Q),
                         "ratio": rho / F(tau2 * Q), "ratio_supweight": rho / min(1.0, tau2 * Q)})
    # random positive intensities and resonant pulse trains (long, small Q)
    dt = 0.05; M = 2**14; t = grid(M, dt)
    for j in range(20):
        sp = (rng.normal(size=M) + 1j * rng.normal(size=M)) * np.exp(-((2 * np.pi * sfft.fftfreq(M, dt)) / rng.uniform(0.3, 3)) ** 2)
        env = np.exp(-(t / rng.uniform(5, 60)) ** 2)
        p = np.abs(sfft.ifft(sp)) ** 2 * env
        rho, Q = rho_Q(p, dt, a)
        prof.append({"r": r, "T": None, "shape": f"random_{j}", "rho": rho, "tau2Q": tau2 * Q,
                     "F": F(tau2 * Q), "ratio": rho / F(tau2 * Q), "ratio_supweight": rho / min(1.0, tau2 * Q)})
    w0 = np.sqrt(a * a + 1)
    for sig in [0.3, 0.6, 1.0, 1.5]:
        for Lenv in [20.0, 80.0]:
            per = 2 * np.pi / w0
            p = np.zeros(M)
            for m_ in range(-int(3 * Lenv / per), int(3 * Lenv / per) + 1):
                p += np.exp(-((t - m_ * per) / sig) ** 2 / 2)
            p *= np.exp(-(t / Lenv) ** 2)
            rho, Q = rho_Q(p, dt, a)
            prof.append({"r": r, "T": None, "shape": f"resonant_train_sig{sig}_L{Lenv}", "rho": rho,
                         "tau2Q": tau2 * Q, "F": F(tau2 * Q), "ratio": rho / F(tau2 * Q),
                         "ratio_supweight": rho / min(1.0, tau2 * Q)})
    for Lenv in [20.0, 80.0]:
        p = (1 + np.cos(w0 * t)) * np.exp(-(t / Lenv) ** 2)
        rho, Q = rho_Q(p, dt, a)
        prof.append({"r": r, "T": None, "shape": f"cos_modulated_L{Lenv}", "rho": rho, "tau2Q": tau2 * Q,
                     "F": F(tau2 * Q), "ratio": rho / F(tau2 * Q), "ratio_supweight": rho / min(1.0, tau2 * Q)})
out["profiles"] = prof
out["profiles_max_ratio"] = max(x["ratio"] for x in prof)
out["profiles_argmax"] = max(prof, key=lambda x: x["ratio"])
out["profiles_count"] = len(prof)
out["profiles_pass"] = bool(out["profiles_max_ratio"] <= 1.0)
print("profiles", len(prof), "max ratio", out["profiles_max_ratio"], out["profiles_argmax"], flush=True)


# ------------------------------------------------------------------ 3. optimizer: beat F at fixed Q
def optimize_at(tq, r, M, dt, s0, mu=200.0, iters=3000):
    a = r; tau2 = 1 / a; k = a * a + 1
    Om = 2 * np.pi * sfft.fftfreq(M, dt)
    Wk = W_osc(Om, a)
    Qt = tq / tau2

    def obj(s):
        p = s * s
        E = p.sum() * dt
        P = sfft.fft(p) * dt
        S = np.sum(Wk * np.abs(P) ** 2) / (M * dt)
        Q = (p * p).sum() * dt / E**2
        rho = 2 / k * S / E**2
        # gradients wrt p
        dS = 2 * dt / (M * dt) * np.real(sfft.fft(Wk * np.conj(P)))
        dlogrho = dS / S - 2 * dt / E
        dQ = 2 * p * dt / E**2 - 2 * Q * dt / E
        pen = mu * np.log(Q / Qt) ** 2
        dpen = 2 * mu * np.log(Q / Qt) * dQ / Q
        J = -np.log(rho) + pen
        dJ = (-dlogrho + dpen) * 2 * s
        return J, dJ

    res = minimize(obj, s0, jac=True, method="L-BFGS-B", options={"maxiter": iters, "maxfun": 2 * iters})
    p = res.x**2
    rho, Q = rho_Q(p, dt, a)
    return {"r": r, "tau2Q_target": tq, "tau2Q": tau2 * Q, "rho": rho, "F": F(tau2 * Q),
            "ratio": rho / F(tau2 * Q), "ratio_supweight": rho / min(1.0, tau2 * Q), "nit": int(res.nit)}, p


opt = []
best_profiles = {}
for r in [0.38125, 2.0]:
    a = r; tau2 = 1 / a; w0 = np.sqrt(a * a + 1)
    for tq in [0.1, 0.3, 1.0, 3.0, 10.0]:
        Qt = tq / tau2
        dt = min(0.05, 1 / (60 * Qt)); M = 4096
        t = grid(M, dt)
        starts = {
            "sech": 1 / np.cosh(t * 3 * Qt),
            "random": np.abs(rng.normal(size=M)) * np.exp(-(t * Qt / 2) ** 2) + 1e-3,
            "cos_mod": np.sqrt(1 + np.cos(w0 * t)) * np.exp(-(t * Qt) ** 2 / 4) + 1e-3,
            "train": np.sqrt(sum(np.exp(-((t - m_ * 2 * np.pi / w0) / 0.5) ** 2 / 2) for m_ in range(-40, 41))
                             * np.exp(-(t * Qt) ** 2 / 4)) + 1e-3,
        }
        for nm, s0 in starts.items():
            res, p = optimize_at(tq, r, M, dt, s0)
            res["start"] = nm
            opt.append(res)
            key = (r, tq)
            if key not in best_profiles or res["ratio"] > best_profiles[key][0]["ratio"]:
                best_profiles[key] = (res, p, dt)
        print("opt r", r, "tau2Q", tq, max((o["ratio"] for o in opt if o["r"] == r and o["tau2Q_target"] == tq)),
              flush=True)
out["optimizer"] = opt
out["optimizer_best_by_Q"] = [best_profiles[k_][0] for k_ in sorted(best_profiles)]
out["optimizer_max_ratio"] = max(o["ratio"] for o in opt)
out["optimizer_pass"] = bool(out["optimizer_max_ratio"] < 1.0)
raw = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration")
np.savez_compressed(os.path.join(raw, "optimizer_best_profiles.npz"),
                    **{f"r{k_[0]}_tq{k_[1]}": v[1] for k_, v in best_profiles.items()},
                    **{f"dt_r{k_[0]}_tq{k_[1]}": v[2] for k_, v in best_profiles.items()})
out["wall_s"] = time.time() - t0
json.dump(out, open("summary_static.json", "w"), indent=1, default=float)
print("optimizer max ratio", out["optimizer_max_ratio"])
for b_ in out["optimizer_best_by_Q"]:
    print(b_)
print("wall", out["wall_s"])
