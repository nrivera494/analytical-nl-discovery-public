"""H2.2: isolated fundamental solitons in S28 (const Aeff, shock, Raman, lossless).
GNLSE photon-mean shift vs exact-overlap reduced model vs Gordon's law.  Frozen in commit 4f0f1ff."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h2-fundamental"
fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
ram = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
ac = lambda w: np.full_like(np.asarray(w, float), aeff0)
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
cases = [(0.015, 0.30), (0.020, 0.40), (0.030, 0.60), (0.050, 1.50), (0.080, 4.0), (0.120, 10.0), (0.200, 30.0)]
res = []
for T0, L in cases:
    nt = 2 ** 13 if T0 < 0.1 else 2 ** 14
    g = Grid(nt, 0.003, wp)
    sim = GNLSE(g, fib.beta, fib.n2, ac, aeff0, raman=ram, alpha_w=None, shock=True, aeff_mode="const", w_ref=wp)
    P0 = b2 / (gam * T0 ** 2)
    A0 = sech_pulse(g, P0, T0)
    z0 = np.pi / 2 * T0 ** 2 / b2
    dz = z0 / 100
    t0 = time.time()
    out = sim.run(A0, L, dz, n_save=20, callback=lambda z, Aw: (sim.mean_w(Aw), sim.photons(Aw)))
    wm = np.array([d[0] for d in out["diag"]]); Nn = np.array([d[1] for d in out["diag"]])
    shift_gnlse = wm[0] - wm[-1]
    rec = {"T0_fs": T0 * 1e3, "L_m": L, "dz_mm": out["dz"] * 1e3, "nt": nt, "shift_gnlse": float(shift_gnlse),
           "photon_drift": float((Nn[-1] - Nn[0]) / Nn[0]), "wall_s": time.time() - t0}
    # step-halving check on the first and the 50 fs case
    if T0 in (0.015, 0.050):
        out2 = sim.run(A0, L, dz / 2, n_save=2, callback=lambda z, Aw: sim.mean_w(Aw))
        rec["shift_gnlse_half_dz"] = float(out2["diag"][0] - out2["diag"][-1])
    for rate in ["exact", "gordon"]:
        m = ReachModel(fib, ram, alpha_w=None, rate=rate, aeff_const_um2=aeff0)
        Nph = 2 * b2 / (gam * T0) / (HBAR * wp * 1e24)
        zz, ww, NN, TT = m.integrate(wp, Nph, L, dz=L / 4000)
        rec["shift_" + rate] = float(wp - ww[-1]); rec["Ts_end_fs_" + rate] = float(TT[-1] * 1e3)
    rec["err_exact"] = (rec["shift_exact"] - shift_gnlse) / shift_gnlse
    rec["err_gordon"] = (rec["shift_gordon"] - shift_gnlse) / shift_gnlse
    res.append(rec)
    print(json.dumps(rec), flush=True)
sel = [r for r in res if r["T0_fs"] >= 50]
x = np.log([r["T0_fs"] for r in sel]); y = np.log([abs(r["err_gordon"]) for r in sel])
q = -np.polyfit(x, y, 1)[0]
summary = {"run_id": RUN, "cases": res, "gordon_error_exponent_q_T0_50_to_200": float(q),
           "TR_model_fs": ram.TR() * 1e3, "aeff0_um2": aeff0}
json.dump(summary, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print("q =", q)
