"""Held-out test of C-20261016-claude-interactive.6-02 (frozen in commit 87f4742): TL sech launches in S28 (lossless,
const Aeff, shock, Raman): rate/bound ratio through the first compression, the energy-retention bound
E(z)/E(0) >= 1/(1 + kappa_U E(0) z), and the identity integrated against Delta E."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
ram = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
ac = lambda w: np.full_like(np.asarray(w, float), aeff0)
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
kU = fib.n2 * ram.fR * ram.hprime0() / (2 * C_M_PS * aeff0 * 1e-12)     # per (pJ m)
res = {"kappa_U_per_pJ_m": kU, "cases": []}
CASES = [(4, 0.0567, 0.3, 2 ** 14, 0.003), (6, 0.0567, 0.3, 2 ** 14, 0.003), (6, 0.1702, 1.5, 2 ** 14, 0.003)]
if len(sys.argv) > 1 and sys.argv[1] == "fine":
    CASES = [(4, 0.0567, 0.3, 2 ** 15, 0.0015), (6, 0.0567, 0.3, 2 ** 15, 0.0015)]
for N, T0, L, NT, DT in CASES:
    g = Grid(NT, DT, wg)
    sim = GNLSE(g, fib.beta, fib.n2, ac, aeff0, raman=ram, alpha_w=None, shock=True, aeff_mode="const", w_ref=wl_to_w(1.65))
    P0 = N ** 2 * b2 / (gam * T0 ** 2)
    A0 = sech_pulse(g, P0, T0, W_off=wp - wg)
    T1 = T0 / (2 * N - 1)
    dz = min(5e-4, np.pi / 2 * T1 ** 2 / b2 / 40)
    t0 = time.time()
    out = sim.run(A0, L, dz, n_save=400, callback=lambda z, Aw: (sim.energy_pJ(Aw), sim.raman_dissipation_pJ_per_m(Aw)))
    z = np.array(out["z"]); E = np.array([d[0] for d in out["diag"]]); D = np.array([d[1] for d in out["diag"]])
    ratio = D / (kU * E ** 2)
    retention_margin = E / E[0] - 1 / (1 + kU * E[0] * z)
    intD = np.concatenate([[0], np.cumsum(0.5 * (D[1:] + D[:-1]) * np.diff(z))])
    rec = {"N": N, "T0_fs": T0 * 1e3, "L_m": L, "nt": NT, "dt_fs": DT * 1e3, "dz_mm": out["dz"] * 1e3, "E0_pJ": float(E[0]), "wall_s": time.time() - t0,
           "max_rate_over_bound": float(ratio.max()), "z_at_max_m": float(z[np.argmax(ratio)]),
           "min_retention_margin": float(retention_margin.min()), "E_L_over_E0": float(E[-1] / E[0]),
           "retention_bound_at_L": float(1 / (1 + kU * E[0] * L)),
           "identity_rel_mismatch": float(abs((E[-1] - E[0]) + intD[-1]) / abs(E[-1] - E[0]))}
    res["cases"].append(rec)
    print(json.dumps(rec), flush=True)
json.dump(res, open(os.path.join(HERE, "summary_fine.json" if (len(sys.argv) > 1 and sys.argv[1] == "fine") else "summary.json"), "w"), indent=1)
