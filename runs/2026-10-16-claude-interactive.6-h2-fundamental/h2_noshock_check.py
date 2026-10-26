"""Exploration for task T-20261016-claude-interactive.6-05: is self-steepening the cause of the full-response model's
overestimate of the isolated-soliton shift at T0 <= 30 fs (run summary.json)?
Same cases with the shock factor removed (constant gamma0; energy is then conserved, so the energy-weighted mean
frequency is the conserved-norm centroid), against the full-response sech-overlap rate with constant gamma0 and fixed
soliton energy:  dw/dz = -(gamma0 fR / E) int dW/2pi W Im h |I_sech~|^2,  T_s = 2|beta2(w)|/(gamma0 E)."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
ram = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
ac = lambda w: np.full_like(np.asarray(w, float), aeff0)
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)


def model_const_gamma(T0, L, nst=3000):
    E = 2 * b2 / (gam * T0)
    w = wp; dz = L / nst
    def rate(w):
        b2w = abs(fib.beta2(np.array([w]))[0]); Ts = 2 * b2w / (gam * E); P = E / (2 * Ts)
        return sech_raman_rate(Ts, P, ram, gam, w, npts=6001)
    for _ in range(nst):
        k1 = rate(w); k2 = rate(w + dz / 2 * k1); k3 = rate(w + dz / 2 * k2); k4 = rate(w + dz * k3)
        w += dz / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return wp - w


res = []
for T0, L in [(0.015, 0.30), (0.020, 0.40), (0.030, 0.60), (0.050, 1.50)]:
    g = Grid(2 ** 13, 0.003, wp)
    sim = GNLSE(g, fib.beta, fib.n2, ac, aeff0, raman=ram, alpha_w=None, shock=False, aeff_mode="const", w_ref=wp)
    P0 = b2 / (gam * T0 ** 2)
    A0 = sech_pulse(g, P0, T0)
    dz = np.pi / 2 * T0 ** 2 / b2 / 100
    def wE(Aw):
        e = np.abs(Aw) ** 2
        return float((e * g.w).sum() / e.sum())
    out = sim.run(A0, L, dz, n_save=2, callback=lambda z, Aw: wE(Aw))
    sh = out["diag"][0] - out["diag"][-1]
    shm = model_const_gamma(T0, L)
    rec = {"T0_fs": T0 * 1e3, "L_m": L, "shift_gnlse_noshock": sh, "shift_model_const_gamma": shm,
           "err_model_noshock": (shm - sh) / sh}
    res.append(rec)
    print(json.dumps(rec), flush=True)
prev = json.load(open(os.path.join(HERE, "summary.json")))["cases"]
for r in res:
    p = [c for c in prev if abs(c["T0_fs"] - r["T0_fs"]) < 1e-6][0]
    r["err_model_with_shock"] = p["err_exact"]
json.dump({"cases": res}, open(os.path.join(HERE, "summary_noshock.json"), "w"), indent=1)
print(json.dumps([{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in res]))


# Variant: pure beta2 (constant, no higher-order dispersion), no shock, against the model with constant beta2.
beta_pure = lambda w: fib.beta(np.array([wp]))[0] + fib.beta(np.array([wp]), 1)[0] * (np.asarray(w) - wp) - 0.5 * b2 * (np.asarray(w) - wp) ** 2


def model_pure(T0, L, nst=3000):
    E = 2 * b2 / (gam * T0); w = wp; dz = L / nst
    Ts = 2 * b2 / (gam * E); P = E / (2 * Ts)
    r = sech_raman_rate(Ts, P, ram, gam, wp, npts=6001)   # constant: soliton unchanged when beta2, gamma constant
    return -r * L


res2 = []
for T0, L in [(0.015, 0.30), (0.020, 0.40), (0.030, 0.60), (0.050, 1.50)]:
    g = Grid(2 ** 13, 0.003, wp)
    sim = GNLSE(g, beta_pure, fib.n2, ac, aeff0, raman=ram, alpha_w=None, shock=False, aeff_mode="const", w_ref=wp)
    P0 = b2 / (gam * T0 ** 2)
    A0 = sech_pulse(g, P0, T0)
    dz = np.pi / 2 * T0 ** 2 / b2 / 100
    def wE(Aw):
        e = np.abs(Aw) ** 2
        return float((e * g.w).sum() / e.sum())
    out = sim.run(A0, L, dz, n_save=2, callback=lambda z, Aw: wE(Aw))
    sh = out["diag"][0] - out["diag"][-1]
    shm = model_pure(T0, L)
    rec = {"T0_fs": T0 * 1e3, "L_m": L, "shift_gnlse_pure_b2_noshock": sh, "shift_model_constant_rate": shm,
           "err_model": (shm - sh) / sh, "shift_per_bandwidth": sh * T0}
    res2.append(rec)
    print(json.dumps(rec), flush=True)
json.dump({"cases": res, "pure_beta2_noshock": res2}, open(os.path.join(HERE, "summary_noshock.json"), "w"), indent=1)
