"""Dispersionless limit of the bound chain, as a cross-check with T-20261010-claude-interactive-04 (claude-b,
T-20261010-claude-interactive-05). Pure SPM of u0 = exp(-tau^2/2): u = u0 exp(i Phi |u0|^2) (exact, one step), linearized
by central differences, same bound-chain and stage-1 binary-search code as run 2026-10-10-claude-b-nd-oracle.
Compared with: lambda_min -> V_min(Phi) = (sqrt(1 + Phi^2) - Phi)^2 (single-slice Kerr shear at the peak; the grid
infimum), the centroid identity F_cen = 1/(1 + 2 Phi^2 <rho_tau^2>_rho) = 1/(1 + (4/(3 sqrt 3)) Phi^2), and lambda_gen.
Writes summary.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd

out = {}
for Phi in (1.0, 2.0, 5.0, 10.0):
    g = nd.Grid(1024, 40.0)
    eps = 1e-6
    Nt = g.Nt
    D = 2 * Nt
    u0 = np.exp(-g.t ** 2 / 2) + 0j
    dirs = np.zeros((D, Nt), complex)
    dirs[:Nt] = np.eye(Nt) * (eps / np.sqrt(g.dt))
    dirs[Nt:] = np.eye(Nt) * (1j * eps / np.sqrt(g.dt))
    spm = lambda u: u * np.exp(1j * Phi * np.abs(u) ** 2)
    o = nd.output_spectrum(g, spm(np.concatenate([u0[None] + dirs, u0[None] - dirs])))
    d = (o[:D] - o[D:]) / (2 * eps)
    J = np.concatenate([d.real.T, d.imag.T], axis=0)
    alpha = nd.output_spectrum(g, spm(u0[None]))[0]
    chain, C, nb, keep, evec = nd.bound_chain(g, J, alpha)
    bb, Tb = nd.best_binary(C, nb, evec, n_random=30, n_ils=300)
    wk = g.w[keep]
    wb = (nb * wk).sum() / nb.sum()
    wc = wk - wb
    F_cen = float(wc @ C @ wc / (wc @ (nb * wc)))
    res = dict(Phi=Phi, **chain, F_centroid=F_cen, F_centroid_closed_form=1 / (1 + 4 / (3 * np.sqrt(3)) * Phi ** 2),
               V_min_peak=(np.sqrt(1 + Phi ** 2) - Phi) ** 2, F_best_binary=bb["F_best"], F_interval=bb["F_interval"],
               gap_dB_centroid_over_gen=10 * np.log10(F_cen / chain["lam_gen"]))
    out[str(Phi)] = res
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in res.items()}), flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
