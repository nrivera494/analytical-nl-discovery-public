"""Gaussian, Kerr-only analogues of the two root-01 anchor points (claude-b, T-20261010-claude-interactive-05).

Anchor run 2026-10-04-claude-b.4-pmin-gdd0-check (GIF625 LP01 at 1250 nm, transform-limited measured spectrum, Agarwal
Raman at 300 K, bandpass 1226-1269 nm): F_min = 0.925 at 0.25 m (N^2 = 18.18, xi = L/L_D = 0.07478) and F_min = 0.834 at
1 m (N^2 = 9.92, xi = 0.2991), with T0 from the rms spectral width (the same convention as here). Their Raman terms at
P_min are 0.0158 and 0.0361. Here: unchirped Gaussian at the same N and xi, pure Kerr (numpy oracle nd_cov.py of run
2026-10-10-claude-b-nd-oracle), bound chain, best binary filter (stage-1 search), and the bandpass with the anchor's edges
in omega T0: red edge -1.789 (from the anchor's groups), blue edge +2.339 (1226 nm, same T0). The sign of omega is
immaterial for the symmetric Kerr-only problem. Writes summary.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd

points = {"anchor_0.25m": dict(N2=18.182869287103614, xi=0.07477662874402607, F_anchor=0.9250044126943715, F_Raman=0.015750963121557486),
          "anchor_1m": dict(N2=9.91961154721838, xi=0.29910651497610447, F_anchor=0.834358136018631, F_Raman=0.036095775564023276)}
lam1, lam2 = 1250.0, None
c = 299792.458  # nm/ps
w_red = -1.789244012476946   # omega T0 of the 1269 nm edge (anchor groups_at_P_min.Omega_e_T0_red)
T0 = 0.07930252863636879     # ps
w_blue = 2 * np.pi * c * (1 / 1226.0 - 1 / 1250.0) * T0
out = {"w_blue_T0": w_blue, "w_red_T0": w_red}
for tag, p in points.items():
    N2 = p["N2"]
    g = nd.Grid(1024, 80.0)
    n = max(1, int(round(p["xi"] / (0.01 / N2))))
    dxi = p["xi"] / n
    u0 = np.exp(-g.t ** 2 / 2) + 0j
    J, alpha = nd.jacobian(g, u0, p["xi"], dxi, N2)
    chain, C, nb, keep, evec = nd.bound_chain(g, J, alpha)
    bb, Tb = nd.best_binary(C, nb, evec)
    wk = g.w[keep]
    res = {}
    for name, (a, b) in {"bandpass_as_given": (w_red, w_blue), "bandpass_mirrored": (-w_blue, -w_red)}.items():
        T = ((wk >= a) & (wk <= b)).astype(float)
        res[name] = dict(F=nd.fano(T, C, nb), photon_fraction=float(nb[T > 0].sum() / nb.sum()))
    N = np.sqrt(N2)
    row = dict(N=N, xi=p["xi"], Z=N * p["xi"], Phi=N2 * p["xi"], zr=p["xi"] / nd.xi_wb(N), **chain,
               F_best_binary=bb["F_best"], F_interval=bb["F_interval"], bandpass=res,
               F_anchor=p["F_anchor"], F_anchor_minus_Raman=p["F_anchor"] - p["F_Raman"])
    out[tag] = row
    print(tag, json.dumps(row, default=float), flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
