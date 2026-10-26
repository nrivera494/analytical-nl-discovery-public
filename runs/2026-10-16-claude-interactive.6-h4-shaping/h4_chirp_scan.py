"""H4 complement: global scan of low-order spectral phase (GDD, then TOD) on the TL N = 3, 100 fs laser in S28, L = 1 m,
numpy RK4IP at dz = 0.25 mm.  Photon fraction beyond 1.75 and 1.85 um, normalised to the laser photon number."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
g = Grid(2 ** 13, 0.003, wg)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
P0 = 9 * b2 / (gam * 0.0567 ** 2)
Q = sech_pulse(g, P0, 0.0567, W_off=wp - wg)
sim = GNLSE(g, fib.beta, fib.n2, lambda w: np.full_like(np.asarray(w, float), aeff0), aeff0,
            raman=OscillatorRaman(0.18, 0.0122, 0.032), w_ref=wg)
Nl = sim.photons(Q)
x = g.w - wp           # detuning from the laser centre (rad/ps)
res = {"GDD_fs2": [], "TOD_fs3": []}
t0 = time.time()
for kind, vals in [("GDD_fs2", [-3000, -1500, -750, -300, 0, 300, 750, 1500, 3000]),
                   ("TOD_fs3", [-60000, -20000, -6000, 6000, 20000, 60000])]:
    for v in vals:
        if kind == "GDD_fs2":
            phi = 0.5 * v * 1e-6 * x ** 2
        else:
            phi = v * 1e-9 * x ** 3 / 6
        out = sim.run(Q * np.exp(1j * phi), 1.0, 2.5e-4)
        rec = {"value": v, "eta_1.75": float(sim.photons(out["Aw"], g.w < wl_to_w(1.75)) / Nl),
               "eta_1.85": float(sim.photons(out["Aw"], g.w < wl_to_w(1.85)) / Nl)}
        res[kind].append(rec)
        print(kind, json.dumps(rec), "t=%.0f" % (time.time() - t0), flush=True)
tl = [r for r in res["GDD_fs2"] if r["value"] == 0][0]
res["TL"] = tl
res["best_H_1.75"] = max(r["eta_1.75"] for k in ("GDD_fs2", "TOD_fs3") for r in res[k]) / tl["eta_1.75"]
res["best_H_1.85"] = max(r["eta_1.85"] for k in ("GDD_fs2", "TOD_fs3") for r in res[k]) / tl["eta_1.85"]
json.dump(res, open(os.path.join(HERE, "summary_chirp_scan.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("TL", "best_H_1.75", "best_H_1.85")}))
