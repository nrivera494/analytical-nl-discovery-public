"""Bound chain at (N, z/z_wb) points (claude-b, T-20261010-claude-interactive-05).
Usage: python run_points.py <run-id> <cases.json> [i0 i1]
case: tag, N, zr (= xi / xi_wb), optional Nt, TW, phi_step (N^2 dxi per step, default 0.02), s (self-steepening).
Stores per case ~/analytical-nl-discovery-data/<run-id>/<tag>.npz (C, nbar, kept bins, alpha, best binary filter) and
appends one JSON line to ~/analytical-nl-discovery-data/<run-id>/rows.jsonl.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd

RAW = os.path.expanduser("~/analytical-nl-discovery-data")


def run_case(run_id, c):
    out = os.path.join(RAW, run_id)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, c["tag"] + ".npz")
    if os.path.exists(path):
        return None
    g = nd.Grid(c.get("Nt", 512), c.get("TW", 40.0))
    N = c["N"]
    N2 = N ** 2
    xw = nd.xi_wb(N)
    xi = c["zr"] * xw
    dxi = c.get("phi_step", 0.02) / N2
    nsteps = max(1, int(round(xi / dxi)))
    dxi = xi / nsteps
    u0 = np.exp(-g.t ** 2 / 2) + 0j
    t0 = time.time()
    J, alpha = nd.jacobian(g, u0, xi, dxi, N2, c.get("s", 0.0))
    chain, C, nb, keep, evec = nd.bound_chain(g, J, alpha)
    bb, Tbest = nd.best_binary(C, nb, evec)
    # symmetric band (classic bandpass) optimum, for reference
    w_keep = g.w[keep]
    Fsym = min(nd.fano((np.abs(w_keep) <= W).astype(float), C, nb) for W in np.unique(np.abs(w_keep)) if np.sum(np.abs(w_keep) <= W) > 0)
    # mean-field diagnostics: output intensity maxima, rms widths
    u = nd.propagate(g, u0[None], xi, dxi, N2, c.get("s", 0.0))[0]
    I = np.abs(u) ** 2
    nmax = int(np.sum((I[1:-1] > I[:-2]) & (I[1:-1] > I[2:]) & (I[1:-1] > 1e-4 * I.max())))
    Iw = np.abs(alpha) ** 2
    rms_t = float(np.sqrt(np.sum(g.t ** 2 * I) / np.sum(I)))
    rms_w = float(np.sqrt(np.sum(g.w ** 2 * Iw) / np.sum(Iw)))
    edge_frac = float((np.sum(I[:g.Nt // 16]) + np.sum(I[-g.Nt // 16:])) / np.sum(I))
    spec_edge = float(np.sum(Iw[np.abs(g.w) > 0.8 * np.abs(g.w).max()]) / np.sum(Iw))
    row = dict(tag=c["tag"], N=N, zr=c["zr"], xi=xi, xi_wb=xw, Nt=g.Nt, TW=g.TW, dxi=dxi, nsteps=nsteps, s=c.get("s", 0.0),
               Phi_peak=N2 * xi, **chain, F_best=bb["F_best"], best_start=bb["start"], F_interval=bb["F_interval"], F_descent=bb["F_descent"],
               F_symband=float(Fsym), n_on=bb["n_on"], intensity_maxima=nmax, rms_t=rms_t, rms_w=rms_w,
               time_edge_fraction=edge_frac, spectral_edge_fraction=spec_edge, wall=time.time() - t0)
    np.savez(path, C=C, nbar=nb, keep=keep, w=g.w, alpha=alpha, Tbest=Tbest, evec=evec)
    with open(os.path.join(out, "rows.jsonl"), "a") as fh:
        fh.write(json.dumps(row) + "\n")
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items() if k not in ("per_start",)}), flush=True)
    return row


if __name__ == "__main__":
    run_id, cases = sys.argv[1], json.load(open(sys.argv[2]))
    i0, i1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, len(cases))
    for c in cases[i0:i1]:
        run_case(run_id, c)
