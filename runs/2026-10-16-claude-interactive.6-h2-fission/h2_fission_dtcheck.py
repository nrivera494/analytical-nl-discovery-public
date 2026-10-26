"""Aliasing / time-step convergence check of the 100 fs fission cases of h2_fission.py.
The claim-02 held-out run (2026-10-16-claude-interactive.6-c02-heldout) showed the exact dissipation identity failing by
1.3% (N=4) and 25.7% (N=6) at dt = 3 fs, which in the discrete model indicates aliasing of the nonlinear product.
Rerun N = 4 and 6 at T0 = 56.7 fs with dt = 1.5 fs, nt = 2^15 (same 49 ps window), lossless check of the identity over
the first 0.3 m, then the full 1 m run with the silica edge for f1.  Usage: python h2_fission_dtcheck.py"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
sys.path.insert(0, HERE)
import numpy as np
from lwir import *
from h2_fission import leading, fib, ram, wp, wg, aeff0, ac, alpha, b2, gam

out = {"cases": []}
for N in [4, 6]:
    T0, L = 0.0567, 1.0
    for nt, dt in [(2 ** 15, 0.0015)]:
        g = Grid(nt, dt, wg)
        P0 = N ** 2 * b2 / (gam * T0 ** 2)
        T1 = T0 / (2 * N - 1)
        dz = min(1e-3, np.pi / 2 * T1 ** 2 / b2 / 40)
        rec = {"N": N, "T0_fs": T0 * 1e3, "nt": nt, "dt_fs": dt * 1e3, "dz_mm": dz * 1e3}
        # (i) lossless identity check over 0.3 m
        sim0 = GNLSE(g, fib.beta, fib.n2, ac, aeff0, raman=ram, alpha_w=None, shock=True, aeff_mode="const", w_ref=wl_to_w(1.65))
        A0 = sech_pulse(g, P0, T0, W_off=wp - wg)
        r0 = sim0.run(A0, 0.3, dz, n_save=400, callback=lambda z, Aw: (sim0.energy_pJ(Aw), sim0.raman_dissipation_pJ_per_m(Aw)))
        z = np.array(r0["z"]); E = np.array([d[0] for d in r0["diag"]]); Dd = np.array([d[1] for d in r0["diag"]])
        intD = np.trapezoid(Dd, z)
        rec["identity_rel_mismatch_0.3m"] = float(abs((E[-1] - E[0]) + intD) / abs(E[-1] - E[0]))
        # (ii) full run with the silica edge, leading soliton at 1 m
        t0 = time.time()
        sim = GNLSE(g, fib.beta, fib.n2, ac, aeff0, raman=ram, alpha_w=alpha, shock=True, aeff_mode="const", w_ref=wl_to_w(1.65))
        Ntot = sim.photons(A0)
        r1 = sim.run(A0, L, dz, n_save=20, callback=lambda zz, Aw: leading(g, sim, Aw))
        d = r1["diag"][-1]
        rec.update({"f1_final": d["N"] / Ntot, "lam1_final_um": float(w_to_wl(d["w"])), "T1_final_fs": d["T"] * 1e3,
                    "eta_2.0": float(sim.photons(r1["Aw"], g.w < wl_to_w(2.0)) / Ntot),
                    "eta_1.9": float(sim.photons(r1["Aw"], g.w < wl_to_w(1.9)) / Ntot), "wall_s": time.time() - t0})
        out["cases"].append(rec)
        print(json.dumps(rec), flush=True)
json.dump(out, open(os.path.join(HERE, "summary_dtcheck.json"), "w"), indent=1)
