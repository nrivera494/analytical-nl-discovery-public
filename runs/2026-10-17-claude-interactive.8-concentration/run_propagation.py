"""C-20261017-gpt-d-02 propagation checks (and launch-plane checks for -01), claude-interactive.8.

Serial; one case at a time. Per-step scalars go to raw npz files; summary numbers to summary_propagation.json.
Usage: python run_propagation.py [case ...]   (default: all production + convergence cases)
"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "2026-10-17-claude-interactive.8-sech-tightness")
sys.path.insert(0, LIB)
from gnlse_pc import GNLSE, sech_launch  # noqa: E402

RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration")
os.makedirs(RAW, exist_ok=True)
fs = 1e-15
MAT = {
    "A": dict(lam0=1550e-9, beta2=-21.7e-27, beta3=0.127e-39, n2=2.6e-20, Aeff=80e-12, fR=0.18,
              tau1=12.2 * fs, tau2=32 * fs),
    "B": dict(lam0=2.8e-6, beta2=-60e-27, beta3=0.3e-39, n2=2.1e-20, Aeff=50e-12, fR=0.2,
              tau1=9.1 * fs, tau2=40 * fs),
}
# name: (material, N, fwhm_fs, L (m) or ('LD', mult), n, dt_fs, nsteps, held_out, kernel)
CASES = {
    "A1": ("A", 1, 30, ("LD", 20), 2**14, 1.0, 4000, False, "analytic"),
    "A2": ("A", 1, 300, 3.0, 2**14, 2.0, 1500, False, "analytic"),
    "A3": ("A", 3, 100, 0.25, 2**14, 1.0, 4000, False, "analytic"),
    "A4": ("A", 4, 200, 0.8, 2**15, 1.0, 4000, True, "analytic"),
    "A5": ("A", 6, 100, 0.15, 2**15, 0.75, 6000, True, "analytic"),
    "A6": ("A", 5, 300, 1.5, 2**15, 1.0, 3000, True, "analytic"),
    "B1": ("B", 4, 150, ("LD", 3), 2**14, 1.0, 4000, True, "analytic"),
    # convergence variants
    "A3_halfstep": ("A", 3, 100, 0.25, 2**14, 1.0, 8000, False, "analytic"),
    "A3_halfdt": ("A", 3, 100, 0.25, 2**15, 0.5, 4000, False, "analytic"),
    "A3_widewin": ("A", 3, 100, 0.25, 2**15, 1.0, 4000, False, "analytic"),
    "A3_sampled_dt1": ("A", 3, 100, 0.25, 2**14, 1.0, 4000, False, "sampled"),
    "A3_analytic_dt3": ("A", 3, 100, 0.25, 2**12 + 2**11, 3.0, 4000, False, "analytic"),
    "A3_sampled_dt3": ("A", 3, 100, 0.25, 2**12 + 2**11, 3.0, 4000, False, "sampled"),
    "A5_halfstep": ("A", 6, 100, 0.15, 2**15, 0.75, 12000, True, "analytic"),
    "A5_halfdt": ("A", 6, 100, 0.15, 2**16, 0.375, 6000, True, "analytic"),
    "B1_widewin": ("B", 4, 150, ("LD", 3), 2**16, 1.0, 4000, True, "analytic"),
    "B1_widewin_halfstep": ("B", 4, 150, ("LD", 3), 2**16, 1.0, 8000, True, "analytic"),
    # post-freeze additions (not held out; added after the audit commit to probe larger tau2 Q)
    "A7_postfreeze": ("A", 3, 30, ("LD", 3), 2**14, 0.5, 6000, False, "analytic"),
    "A7_postfreeze_halfstep": ("A", 3, 30, ("LD", 3), 2**14, 0.5, 12000, False, "analytic"),
    "A8_postfreeze": ("A", 6, 30, ("LD", 1), 2**15, 0.25, 8000, False, "analytic"),
    "A8_postfreeze_halfstep": ("A", 6, 30, ("LD", 1), 2**15, 0.25, 16000, False, "analytic"),
}


def F(tau2Q):
    return 2 / np.pi * np.arctan(np.pi * tau2Q / 2)


def run_case(name):
    mat, N, fwhm, L, n, dtfs, nsteps, held, kernel = CASES[name]
    m = MAT[mat]
    sim = GNLSE(n, dtfs * fs, m["lam0"], m["beta2"], m["beta3"], m["n2"], m["Aeff"], m["fR"],
                m["tau1"], m["tau2"], kernel=kernel)
    A0, T0, P0 = sech_launch(sim, N, fwhm * fs, m["beta2"])
    LD = T0**2 / abs(m["beta2"])
    if isinstance(L, tuple):
        L = L[1] * LD
    t0 = time.time()
    rec, AL = sim.run(A0, L, nsteps, record_every=1)
    wall = time.time() - t0
    keys = ["z", "E", "Q", "Pmax", "rho_rhs", "rho_spec", "Nph", "negfrac", "edge", "dEdz_rhs", "dEdz_spec"]
    arr = {k: np.array([r[k] for r in rec]) for k in keys}
    tau2 = m["tau2"]
    Fz = F(tau2 * arr["Q"])
    ratio = arr["rho_rhs"] / Fz
    ratio_spec = arr["rho_spec"] / Fz
    E0 = arr["E"][0]
    kap = sim.kappa
    Qmax = arr["Q"].max()
    Pmax_max = arr["Pmax"].max()
    # along-path comparison: 1/E(L) <= 1/E0 + kappa int F(Q) dz  (trapezoid on recorded planes)
    pathint = np.trapz(Fz, arr["z"])
    res = {
        "case": name, "material": mat, "N": N, "fwhm_fs": fwhm, "L_m": L, "n": n, "dt_fs": dtfs,
        "nsteps": nsteps, "held_out": held, "kernel": kernel, "T0_fs": T0 / fs, "P0_W": P0, "LD_m": LD,
        "E0_J": E0, "kappa_per_Jm": kap, "kappaE0L": kap * E0 * L, "tau2Q_launch": tau2 * arr["Q"][0],
        "tau2Q_max": tau2 * Qmax, "tau2_Pmax_over_E_max": tau2 * Pmax_max / E0,
        "rho_launch": arr["rho_rhs"][0], "rho_max": arr["rho_rhs"].max(),
        "ratio_max": ratio.max(), "ratio_spec_max": ratio_spec.max(), "z_ratio_max": arr["z"][ratio.argmax()],
        "F_max": Fz.max(), "violations": int(np.sum(ratio > 1 + 1e-6)), "planes": int(len(ratio)),
        "rho_le_F_le_1_all": bool(np.all(ratio <= 1 + 1e-6) and np.all(Fz <= 1)),
        "identity_max_rel": float(np.max(np.abs(arr["dEdz_rhs"] - arr["dEdz_spec"]) / np.abs(arr["dEdz_spec"]))),
        "photon_drift": arr["Nph"][-1] / arr["Nph"][0] - 1, "negfrac_max": arr["negfrac"].max(),
        "edge_max": arr["edge"].max(),
        "retention_actual": arr["E"][-1] / E0,
        "retention_energy_only_bound": 1 / (1 + kap * E0 * L),
        "retention_Qmax_bound": 1 / (1 + kap * E0 * L * F(tau2 * Qmax)),
        "retention_Pmax_bound": 1 / (1 + kap * E0 * L * F(tau2 * Pmax_max / E0)),
        "retention_path_comparison": 1 / (1 + kap * E0 * pathint),
        "wall_s": wall,
    }
    res["retention_ok"] = bool(res["retention_actual"] >= res["retention_Qmax_bound"] >= res["retention_energy_only_bound"])
    # integrated identity: E(L)-E0 vs trapz of dE/dz
    res["integrated_identity_rel"] = float((arr["E"][-1] - E0 - np.trapz(arr["dEdz_rhs"], arr["z"])) / (E0 - arr["E"][-1]))
    np.savez_compressed(os.path.join(RAW, name + ".npz"), **arr, F=Fz, ratio=ratio,
                        AL=AL.astype(np.complex64), t=sim.t)
    return res


if __name__ == "__main__":
    names = sys.argv[1:] or list(CASES)
    outp = os.path.join(HERE, "summary_propagation.json")
    allres = json.load(open(outp)) if os.path.exists(outp) else {}
    for nm in names:
        r = run_case(nm)
        allres[nm] = {k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in r.items()}
        json.dump(allres, open(outp, "w"), indent=1)
        print(nm, {k: r[k] for k in ["ratio_max", "rho_max", "tau2Q_max", "violations", "retention_actual",
                                     "retention_Qmax_bound", "retention_energy_only_bound", "identity_max_rel",
                                     "photon_drift", "edge_max", "wall_s"]}, flush=True)
