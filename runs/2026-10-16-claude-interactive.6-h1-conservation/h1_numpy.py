"""H1: conservation structure of the forward model (numpy implementation).  Frozen in commit 4f0f1ff."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h1-conservation"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
os.makedirs(RAW, exist_ok=True)

fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
ram = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
g = Grid(2 ** 13, 0.003, wg)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
N_sol, T0, L = 3, 0.0567, 1.0
P0 = N_sol ** 2 * b2 / (gam * T0 ** 2)
A0 = sech_pulse(g, P0, T0, W_off=wp - wg)
aeff_const = lambda w: np.full_like(np.asarray(w, float), aeff0)


def make(mode="const", shock=True):
    aw = aeff_const if mode == "const" else fib.aeff_um2
    return GNLSE(g, fib.beta, fib.n2, aw, aeff0, raman=ram, alpha_w=None, shock=shock, aeff_mode=mode, w_ref=wg)


def run(sim, dz, nsave):
    def diag(z, Aw):
        return dict(N=sim.photons(Aw), E=sim.energy_pJ(Aw), wm=sim.mean_w(Aw),
                    D=sim.raman_dissipation_pJ_per_m(Aw) if sim.aeff_mode == "const" else np.nan)
    t0 = time.time()
    out = sim.run(A0, L, dz, n_save=nsave, callback=diag)
    d = out["diag"]
    res = {k: np.array([x[k] for x in d]) for k in d[0]}
    res["z"] = np.array(out["z"]); res["Aw"] = out["Aw"]; res["wall_s"] = time.time() - t0
    return res


summary = {"run_id": RUN, "case": {"fibre": "S28", "N": N_sol, "T0_fs": T0 * 1e3, "P0_W": P0, "E_pJ": 2 * P0 * T0,
                                   "L_m": L, "nt": g.nt, "dt_fs": g.dt * 1e3, "grid_centre_um": 1.75,
                                   "aeff0_um2": aeff0, "gamma0_per_W_m": gam, "beta2_ps2_per_m": -b2}}
# (a) photon drift vs dz (const, shock)
drift = {}
keep = None
for dz in [1e-3, 5e-4, 2.5e-4, 1.25e-4]:
    sim = make("const", True)
    r = run(sim, dz, 200 if dz == 2.5e-4 else 4)
    drift[dz] = (r["N"][-1] - r["N"][0]) / r["N"][0]
    print("dz %.3g mm  dN/N %.3e  wall %.1f s" % (dz * 1e3, drift[dz], r["wall_s"]), flush=True)
    if dz == 2.5e-4:
        keep = r; sim_keep = sim
dzs = np.array(sorted(drift)); dr = np.array([abs(drift[d]) for d in dzs])
p = np.polyfit(np.log(dzs), np.log(dr), 1)[0]
summary["a_photon_drift"] = {"dz_mm": (dzs * 1e3).tolist(), "rel_drift": [drift[d] for d in dzs], "exponent_p": p}
# (b) identity
r = keep
dE = r["E"][-1] - r["E"][0]
intD = np.trapezoid(r["D"], r["z"])
summary["b_identity"] = {"E0_pJ": r["E"][0], "E_L_pJ": r["E"][-1], "dE_pJ": dE, "minus_int_identity_pJ": -intD,
                         "rel_mismatch": abs(dE + intD) / abs(dE)}
# (c) monotone mean
dw = np.diff(r["wm"])
summary["c_monotone_mean"] = {"max_increase_rad_per_ps": float(dw.max()), "total_shift_rad_per_ps": float(r["wm"][-1] - r["wm"][0]),
                              "n_planes": int(len(r["z"]))}
# (d) universal bound
pref = fib.n2 / (C_M_PS * aeff0 * 1e-12)   # n2/(c Aeff) in ps/(W m)
bound = pref * ram.fR * ram.hprime0() / 2 * r["E"] ** 2
slack = r["D"] / bound
summary["d_universal_bound"] = {"max_rate_over_bound": float(slack.max()), "z_at_max": float(r["z"][np.argmax(slack)]),
                                "bound_holds_everywhere": bool(np.all(r["D"] <= bound)),
                                "rate_pJ_per_m_at_max": float(r["D"][np.argmax(slack)])}
for lc in [1.65, 1.75, 1.85]:
    summary.setdefault("eta_numpy_const", {})[str(lc)] = float(sim_keep.photons(r["Aw"], g.w < wl_to_w(lc)) / r["N"][0])
np.savez_compressed(os.path.join(RAW, "const_dz0.25mm.npz"), z=r["z"], N=r["N"], E=r["E"], wm=r["wm"], D=r["D"], Aw=r["Aw"], w=g.w)
print(json.dumps({k: summary[k] for k in ["a_photon_drift", "b_identity", "c_monotone_mean", "d_universal_bound", "eta_numpy_const"]}, indent=1), flush=True)
# (e) naive vs pc with Aeff(w); (f) no shock
for name, mode, shock in [("naive", "naive", True), ("pc", "pc", True), ("noshock_const", "const", False)]:
    sim = make(mode, shock)
    rr = run(sim, 2.5e-4, 4)
    summary["ef_" + name] = {"rel_photon_drift": float((rr["N"][-1] - rr["N"][0]) / rr["N"][0]),
                             "rel_energy_change": float((rr["E"][-1] - rr["E"][0]) / rr["E"][0]),
                             "mean_shift_rad_per_ps": float(rr["wm"][-1] - rr["wm"][0]),
                             "eta_1.75": float(sim.photons(rr["Aw"], g.w < wl_to_w(1.75)) / rr["N"][0]), "wall_s": rr["wall_s"]}
    print(name, summary["ef_" + name], flush=True)
    np.savez_compressed(os.path.join(RAW, f"{name}.npz"), Aw=rr["Aw"], w=g.w)
summary["aeff_ratio_1.55_to_1.85"] = float(fib.aeff_um2(np.array([wl_to_w(1.85)]))[0] / aeff0)
json.dump(summary, open(os.path.join(HERE, "summary_numpy.json"), "w"), indent=1, default=float)
print("done")
