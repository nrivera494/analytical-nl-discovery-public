"""C-20261017-gpt-d-01 in the GNLSE: sech launch-plane dE/dz from (i) the nonlinear RHS and
(ii) a three-point Richardson finite difference of E(z) over short real propagation, vs the closed form.
Also re-checks with the sampled kernel at the coarsest grid. claude-interactive.8.
"""
import json, time, os, sys
import numpy as np
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gnlse_pc import GNLSE, sech_launch  # noqa: E402
from ramanlib import rho_closed  # noqa: E402

fs = 1e-15
MAT = {
    "A": dict(lam0=1550e-9, beta2=-21.7e-27, beta3=0.127e-39, n2=2.6e-20, Aeff=80e-12, fR=0.18,
              tau1=12.2 * fs, tau2=32 * fs),
    "B": dict(lam0=2.8e-6, beta2=-60e-27, beta3=0.3e-39, n2=2.1e-20, Aeff=50e-12, fR=0.2,
              tau1=9.1 * fs, tau2=40 * fs),
}
FWHM = [5, 10, 20, 30, 50, 100, 200, 300]
HELD = {("A", 10), ("A", 50), ("A", 200)} | {("B", f) for f in FWHM}
t0 = time.time()
rows = []
for mat in ["A", "B"]:
    m = MAT[mat]
    r = m["tau1"] / m["tau2"]
    for fw in FWHM:
        for kernel in (["analytic", "sampled"] if fw in (100, 300) else ["analytic"]):
            dt = fw * fs / 40
            n = 2**13
            sim = GNLSE(n, dt, m["lam0"], m["beta2"], m["beta3"], m["n2"], m["Aeff"], m["fR"],
                        m["tau1"], m["tau2"], kernel=kernel)
            A0, T0, P0 = sech_launch(sim, 1, fw * fs, m["beta2"])
            LD = T0**2 / abs(m["beta2"])
            x = T0 / m["tau1"]
            rc = float(rho_closed(r, x))
            h = 2e-3 * LD
            rec, _ = sim.run(A0, 4 * h, 4, record_every=1)
            E = np.array([q["E"] for q in rec])
            D1 = (E[1] - E[0]) / h; D2 = (E[2] - E[0]) / (2 * h); D4 = (E[4] - E[0]) / (4 * h)
            dEdz_fd = 8 / 3 * D1 - 2 * D2 + 1 / 3 * D4
            rho_fd = -dEdz_fd / (sim.kappa * E[0] ** 2)
            rows.append({"material": mat, "r": r, "fwhm_fs": fw, "kernel": kernel, "T0_fs": T0 / fs, "x": x,
                         "dt_fs": dt / fs, "held_out": (mat, fw) in HELD, "formal_short": fw == 5,
                         "omega0_T0": sim.w0 * T0, "negfrac": float(rec[0]["negfrac"]),
                         "rho_closed": rc, "rho_rhs": float(rec[0]["rho_rhs"]), "rho_spec": float(rec[0]["rho_spec"]),
                         "rho_fd": float(rho_fd), "rel_rhs": abs(rec[0]["rho_rhs"] - rc) / rc,
                         "rel_fd": abs(rho_fd - rc) / rc, "h_over_LD": 2e-3})
            print(rows[-1], flush=True)
out = {"run_id": "2026-10-17-claude-interactive.8-sech-tightness", "snapshots": rows,
       "max_rel_rhs_analytic": max(q["rel_rhs"] for q in rows if q["kernel"] == "analytic"),
       "max_rel_fd_analytic": max(q["rel_fd"] for q in rows if q["kernel"] == "analytic"),
       "max_rel_rhs_sampled": max(q["rel_rhs"] for q in rows if q["kernel"] == "sampled"),
       "wall_s": time.time() - t0}
out["pass_rhs"] = bool(out["max_rel_rhs_analytic"] < 1e-6)
out["pass_fd"] = bool(out["max_rel_fd_analytic"] < 1e-4)
json.dump(out, open(os.path.join(HERE, "summary_snapshots.json"), "w"), indent=1)
print({k: v for k, v in out.items() if k != "snapshots"})
