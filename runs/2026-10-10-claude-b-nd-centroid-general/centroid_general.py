"""Generality check of the spectral-centroid identity of C-20261010-claude-b-02 (claude-b, T-20261010-claude-interactive-05):
F(w = omega - mean) from the linearized count covariance vs <dw^2>_in/<dw^2>_out for the Gaussian with
(i) anomalous dispersion (soliton orders 1.5 and 3), (ii) normal dispersion plus third-order dispersion, (iii) anomalous plus TOD.
Model: i u_xi + sgn/2 u_tautau + i d3/6 u_tautautau + N^2|u|^2 u = 0 written as the linear phase exp(i D(w) dxi) with
D(w) = -sgn w^2/2 + d3 w^3/6 (numpy fft convention of nd_cov.py), Strang splitting, peak phase step 0.01. Writes summary.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd
fft, ifft = np.fft.fft, np.fft.ifft


def jac(g, N, xi, sgn, d3, eps=1e-6, phi_step=0.01):
    Nt = g.Nt; D = 2 * Nt; N2 = N * N
    n = max(1, int(round(xi * N2 / phi_step))); dxi = xi / n
    Dw = 0.5 * sgn * g.w ** 2 + d3 * g.w ** 3 / 6       # sgn = +1 normal (as nd_cov), -1 anomalous
    L = np.exp(1j * Dw * dxi / 2)
    u0 = np.exp(-g.t ** 2 / 2) + 0j
    dirs = np.zeros((D, Nt), complex)
    dirs[:Nt] = np.eye(Nt) * (eps / np.sqrt(g.dt)); dirs[Nt:] = np.eye(Nt) * (1j * eps / np.sqrt(g.dt))
    U = np.concatenate([u0[None] + dirs, u0[None] - dirs, u0[None]])
    for _ in range(n):
        U = ifft(L * fft(U, axis=-1), axis=-1)
        U = U * np.exp(1j * N2 * np.abs(U) ** 2 * dxi)
        U = ifft(L * fft(U, axis=-1), axis=-1)
    o = nd.output_spectrum(g, U)
    d = (o[:D] - o[D:2 * D]) / (2 * eps)
    return np.concatenate([d.real.T, d.imag.T], axis=0), o[-1]


out = {}
for name, N, xi, sgn, d3 in (("anomalous_N1.5", 1.5, 1.0, -1, 0.0), ("anomalous_N3", 3.0, 0.5, -1, 0.0),
                             ("normal_N5_TOD0.3", 5.0, 0.1, +1, 0.3), ("anomalous_N3_TOD0.3", 3.0, 0.5, -1, 0.3)):
    g = nd.Grid(512, 40.0)
    J, alpha = jac(g, N, xi, sgn, d3)
    chain, C, nb, keep, evec = nd.bound_chain(g, J, alpha)
    nall = np.abs(alpha) ** 2
    wb = (nall * g.w).sum() / nall.sum()
    u0s = np.abs(nd.output_spectrum(g, (np.exp(-g.t ** 2 / 2) + 0j)[None])[0]) ** 2
    win = (u0s * g.w).sum() / u0s.sum()
    ratio = float((u0s * (g.w - win) ** 2).sum() / u0s.sum() / ((nall * (g.w - wb) ** 2).sum() / nall.sum()))
    wc = g.w[keep] - wb
    F = float(wc @ C @ wc / (wc @ (nb * wc)))
    out[name] = dict(N=N, xi=xi, sgn=sgn, d3=d3, mean_in=float(win), mean_out=float(wb), F_centroid=F, ratio=ratio,
                     rel=F / ratio - 1, lam_gen=chain["lam_gen"], lam_min=chain["lam_min"])
    print(name, {k: (round(v, 8) if isinstance(v, float) else v) for k, v in out[name].items()}, flush=True)
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
