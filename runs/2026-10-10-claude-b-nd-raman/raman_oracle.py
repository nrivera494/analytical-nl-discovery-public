"""Raman reservoir noise added to the linearized normal-dispersion oracle (claude-b, T-20261010-claude-interactive-05).

Model: Kerr-only mean field and noise map (nd_cov.py of run 2026-10-10-claude-b-nd-oracle) plus the Raman Langevin
(phonon reservoir) phase noise, dA = i gamma A m dz with <m(z,t) m(z',t')> = delta(z - z') R(t - t') and spectral density
C(omega) = (hbar omega0/gamma) |Im h_R(omega)| coth(hbar |omega| / 2 k_B T) (the symmetrized spectrum of
raman_bath_spectrum.jl; Agarwal response f_R = 0.18, tau1 = 12.2 fs, tau2 = 32 fs). The deterministic delayed response
is NOT included (its effect on filtered F is +0.002 to +0.04 at T0 = 100 fs, run 2026-10-10-claude-b.6-solver-nd-check).

In soliton units and shot-noise-normalized sample quadratures (vacuum covariance = identity), the noise injected over
d xi is D = 4 N^2 E R E^T d xi, E = [diag(-Im u); diag(Re u)], R the circulant with first column ifft(c_hat),
c_hat(Omega) = |Im h_R(Omega/T0)| coth(hbar Omega / (2 k_B T T0)). hbar and the photon number drop out.
Output covariance: V = J (I + W) J^T, W = sum_s w_s X_s D_s X_s^T, X_s = inverse of the time-domain quadrature Jacobian
from the input to slice s (trapezoid weights w_s over slices every `every` steps). W is accumulated for several T0 at
once (the Kerr map does not depend on T0).

From V and the count covariance C = (1/4) G (I + W) G^T: lambda_min, lambda_pass, lambda_gen, the centroid readout, the
Raman part F_R of the three weights in weights_for_solver.json (validation against run
2026-10-10-claude-b.6-solver-weighted-raman, case 2b), and the best binary filter (stage-1 search + refine).
Usage: python raman_oracle.py -> summary.json, rows in ~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-raman/
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ORA = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle")
sys.path.insert(0, ORA)
import nd_cov as nd
import refine_binary as rb

fft, ifft = np.fft.fft, np.fft.ifft
HBAR, KB = 1.054571817e-34, 1.380649e-23
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-raman")


def c_hat(Omega, T0_s, fR=0.18, tau1=12.2e-15, tau2=32e-15, temp=300.0):
    w = np.abs(Omega) / T0_s
    a, b = 1 / tau2, 1 / tau1
    imh = fR * (a * a + b * b) * 2 * a * w / ((a * a + b * b - w * w) ** 2 + 4 * a * a * w * w)
    out = np.empty_like(w)
    nz = w > 0
    out[nz] = imh[nz] / np.tanh(HBAR * w[nz] / (2 * KB * temp))
    out[~nz] = 4 * a * fR * KB * temp / (HBAR * (a * a + b * b))
    return out


def run_point(N, zr, T0_list, Nt=512, TW=40.0, phi_step=0.02, every=4, eps=1e-6):
    g = nd.Grid(Nt, TW)
    N2 = N ** 2
    xi = zr * nd.xi_wb(N)
    n = max(1, int(round(xi / (phi_step / N2))))
    dxi = xi / n
    D = 2 * Nt
    u0 = np.exp(-g.t ** 2 / 2) + 0j
    dirs = np.zeros((D, Nt), complex)
    dirs[:Nt] = np.eye(Nt) * (eps / np.sqrt(g.dt))
    dirs[Nt:] = np.eye(Nt) * (1j * eps / np.sqrt(g.dt))
    U = np.concatenate([u0[None] + dirs, u0[None] - dirs, u0[None]])
    L = np.exp((0.5j * g.w ** 2) * dxi / 2)
    Rs = {T0: np.real(ifft(c_hat(g.w, T0 * 1e-15))) for T0 in T0_list}
    idx = (np.arange(Nt)[:, None] - np.arange(Nt)[None, :]) % Nt
    Rmat = {T0: r[idx] for T0, r in Rs.items()}
    slices = list(range(0, n + 1, every))
    if slices[-1] != n:
        slices.append(n)
    zs = np.array(slices) * dxi
    wts = np.zeros(len(slices))
    wts[:-1] += np.diff(zs) / 2
    wts[1:] += np.diff(zs) / 2
    W = {T0: np.zeros((D, D)) for T0 in T0_list}

    def accumulate(U, wgt):
        du = (U[:D] - U[D:2 * D]) / (2 * eps)
        Js = np.sqrt(g.dt) * np.concatenate([du.real.T, du.imag.T])
        X = np.linalg.inv(Js)
        ub = U[-1]
        E = np.concatenate([np.diag(-ub.imag), np.diag(ub.real)])
        XE = X @ E
        for T0 in T0_list:
            W[T0] += wgt * 4 * N2 * (XE @ Rmat[T0] @ XE.T)

    k = 0
    accumulate(U, wts[0])
    k = 1
    for step in range(1, n + 1):
        U = ifft(L * fft(U, axis=-1), axis=-1)
        U = U * np.exp(1j * N2 * np.abs(U) ** 2 * dxi)
        U = ifft(L * fft(U, axis=-1), axis=-1)
        if k < len(slices) and step == slices[k]:
            accumulate(U, wts[k])
            k += 1
    out = nd.output_spectrum(g, U[:2 * D])
    dd = (out[:D] - out[D:]) / (2 * eps)
    J = np.concatenate([dd.real.T, dd.imag.T], axis=0)
    alpha = nd.output_spectrum(g, U[-1:])[0]
    return g, J, alpha, W, dict(N=N, zr=zr, xi=xi, Z=N * xi, Phi=N2 * xi, nsteps=n, n_slices=len(slices))


def chain_with(g, J, alpha, Wr):
    Nt = g.Nt
    V = J @ (np.eye(2 * Nt) + Wr) @ J.T
    ev = np.linalg.eigvalsh(V)
    p = np.concatenate([-alpha.imag, alpha.real])
    p /= np.linalg.norm(p)
    lam_pass = float(np.linalg.eigvalsh(V + 10 * np.max(np.abs(V)) * np.outer(p, p))[0])
    nbar_all = np.abs(alpha) ** 2
    G = 2 * (alpha.real[:, None] * J[:Nt] + alpha.imag[:, None] * J[Nt:])
    srt = np.sort(nbar_all)[::-1]
    thr = srt[np.searchsorted(np.cumsum(srt) / srt.sum(), 1 - 1e-9)]
    keep = np.array([i for i in g.order if nbar_all[i] >= thr])
    Gk = G[keep]
    C = 0.25 * Gk @ (np.eye(2 * Nt) + Wr) @ Gk.T
    CR = 0.25 * Gk @ Wr @ Gk.T
    nb = nbar_all[keep]
    Dm = 1 / np.sqrt(nb)
    e, vec = np.linalg.eigh(Dm[:, None] * C * Dm[None, :])
    wk = g.w[keep]
    wb = (nb * wk).sum() / nb.sum()
    wc = wk - wb
    F_cen = float(wc @ C @ wc / (wc @ (nb * wc)))
    F_cen_R = float(wc @ CR @ wc / (wc @ (nb * wc)))
    return dict(lam_min=float(ev[0]), lam_2=float(ev[1]), lam_pass=lam_pass, lam_gen=float(e[0]), F_centroid=F_cen,
                F_centroid_R=F_cen_R), C, CR, nb, keep, vec[:, 0] * Dm


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    wts = json.load(open(os.path.join(ORA, "weights_for_solver.json")))["points"]
    T0_list = [50.0, 100.0, 300.0, 1000.0]
    cases = [dict(N=10, zr=0.7, Nt=512, T0=[50.0, 100.0, 300.0, 1000.0]), dict(N=20, zr=0.7, Nt=1024, T0=[100.0, 1000.0]),
             dict(N=20, zr=0.3, Nt=1024, T0=[100.0])]
    out = {"T0_fs": T0_list, "points": {}}
    rng = np.random.default_rng(3)
    for c in cases:
        t0 = time.time()
        g, J, alpha, W, info = run_point(c["N"], c["zr"], c["T0"], Nt=c["Nt"], every=16)
        tag = f"N{c['N']}_zr{c['zr']:g}"
        res = dict(info, Nt=c["Nt"], wall_jacobian=time.time() - t0, by_T0={})
        kerr, Ck, _, nbk, keepk, evk = chain_with(g, J, alpha, np.zeros_like(W[c["T0"][0]]))
        res["kerr"] = kerr
        for T0 in c["T0"]:
            ch, C, CR, nb, keep, evec = chain_with(g, J, alpha, W[T0])
            r = dict(ch)
            # validation weights (only for the points the solver ran, at T0 = 100 fs)
            if tag in wts and T0 == 100.0:
                pw = wts[tag]
                kk = np.rint(g.w[keep] / (2 * np.pi / 40)).astype(int)
                pos = {k: i for i, k in enumerate(kk)}
                val = {}
                for name in ("w_centroid", "w_lambda_gen_eigvec", "w_best_binary"):
                    wv = np.zeros(len(keep))
                    for k, x in zip(pw["bins_k"], pw[name]):
                        if k in pos:
                            wv[pos[k]] = x
                    den = wv @ (nb * wv)
                    val[name] = dict(F_total=float(wv @ C @ wv / den), F_R=float(wv @ CR @ wv / den))
                r["validation_weights"] = val
            bb, Tb = nd.best_binary(C, nb, evec, n_random=20, n_ils=200)
            Fnn, wnn, (Fr, Tr, name) = rb.refine(C, nb, Tb, evec, rng)
            r["F_bin"] = float(min(bb["F_best"], Fr))
            r["F_interval"] = bb["F_interval"]
            r["F_nonneg_heuristic"] = Fnn
            res["by_T0"][str(T0)] = r
            np.savez(os.path.join(RAW, f"{tag}_T0_{int(T0)}.npz"), C=C, CR=CR, nbar=nb, keep=keep)
        res["wall"] = time.time() - t0
        out["points"][tag] = res
        print(tag, json.dumps({"kerr": {k: round(v, 6) for k, v in kerr.items()},
                               **{T0: {k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items() if k != "validation_weights"}
                                  for T0, r in res["by_T0"].items()}}), flush=True)
        if "validation_weights" in res["by_T0"].get("100.0", {}):
            print("  validation", json.dumps(res["by_T0"]["100.0"]["validation_weights"]), flush=True)
        json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
