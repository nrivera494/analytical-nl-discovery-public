"""Part (ii) of C-20261019-pi-chatgpt-02: initial slope of lambda_LO from full-field linearized
propagation at small tau, against 2 n_sp (1 - R), R = gamma int P^2 / (int P n_sp g).
claude-interactive.13."""
import json, os, numpy as np
from fullfield import Grid, seed, lo_covariance, kappa
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-19-claude-interactive.13-similariton-lo-verification")
eps0 = 0.05
gr = Grid(2048, 8.0)
taus = np.array([0.5, 1, 2, 3, 4]) * 1e-3
Rs = {("parabola", 1.0): [0.5, 0.9, 0.98, 1.0, 1.02, 1.3, 1.7], ("parabola", 2.0): [0.6, 0.95, 0.99, 1.0, 1.01, 1.4, 1.8],
      ("gaussian", 1.0): [0.7, 0.85, 0.97, 1.0, 1.03, 1.5, 1.9], ("gaussian", 2.0): [0.8, 0.92, 0.995, 1.0, 1.005, 1.6, 2.0]}
shapes = {
    "parabola_d0.05_unchirped": dict(kind="parabola", delta=0.05, chirp=0.0),
    "parabola_d0.05_asymchirp": dict(kind="parabola", delta=0.05, chirp=np.sqrt(2)),
    "gaussian_unchirped": dict(kind="gaussian", chirp=0.0),
}
def slope_fit(lams):
    y = (np.array(lams) - 1) / taus
    c = np.polyfit(taus, y, 2)
    return c[-1], c[-2]
out = {"eps0": eps0, "grid": {"N": gr.N, "L": gr.L}, "taus": taus.tolist(), "R_targets": {f"{k[0]}_nsp{int(k[1])}": v for k, v in Rs.items()}, "cases": {}}
for sname, s in shapes.items():
    p0 = seed(s["kind"], gr.x, delta=s.get("delta", 0.05), chirp=s["chirp"], eps0=eps0)
    kap, rpk = kappa(p0, gr)
    for nsp in (1.0, 2.0):
        rows = []
        for R in Rs[(s["kind"], nsp)]:
            Gam = kap / (nsp * eps0 * R)
            lams, comms = [], []
            for t in taus:
                o = lo_covariance(p0, gr, eps0, Gam, t, 60, nsp=nsp)
                lams.append(o["lam_min"]); comms.append(o["comm"] - 1)
            s0, curv = slope_fit(lams)
            rows.append(dict(R=R, Gamma=Gam, gammaP0_over_g=rpk / (eps0 * Gam), slope=s0, slope_theory=2 * nsp * (1 - R),
                             curvature=curv, lam=lams, max_comm_err=float(np.max(np.abs(comms)))))
        Rarr = np.array([r["R"] for r in rows]); sl = np.array([r["slope"] for r in rows])
        # root of slope(R) by local linear interpolation between bracketing points
        i = np.where(np.sign(sl[:-1]) != np.sign(sl[1:]))[0]
        roots = [float(Rarr[j] - sl[j] * (Rarr[j + 1] - Rarr[j]) / (sl[j + 1] - sl[j])) for j in i]
        exact_zero = [r["slope"] for r in rows if r["R"] == 1.0]
        out["cases"][f"{sname}_nsp{int(nsp)}"] = dict(kappa=kap, rho_peak=rpk, threshold_gammaP0_over_g_smoothed=nsp * rpk / kap,
            rows=rows, root_R=roots, slope_at_R1=exact_zero,
            max_abs_slope_err=float(np.max(np.abs(sl - 2 * nsp * (1 - Rarr)))),
            root_gammaP0_over_g=[nsp * rpk / kap / r0 * 1.0 for r0 in roots])
        print(sname, int(nsp), "kappa=%.6f thr(gP0/g)=%.6f" % (kap, nsp * rpk / kap), "roots R:", roots,
              "slope(R=1)=%.2e" % exact_zero[0], "max|slope-th|=%.2e" % out["cases"][f"{sname}_nsp{int(nsp)}"]["max_abs_slope_err"],
              "max comm err %.1e" % max(r["max_comm_err"] for r in rows))
json.dump(out, open("slopes_summary.json", "w"), indent=1)
