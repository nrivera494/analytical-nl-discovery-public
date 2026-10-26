"""Truncated-Wigner (nonlinear, stochastic) check of part (ii) of C-20261019-pi-chatgpt-02, relaxing the
linearization of the noise. Same grid and Strang scheme as fullfield.py, so splitting error cancels in the
comparison with the linearized adjoint result.  claude-interactive.13.  numpy seed 20261019.
Wigner sampling: grid mode b_j = psi_j sqrt(dx/hbar), hbar = E0/N0 (N0 photons). Vacuum: Re b, Im b ~ N(0, 1/4).
Amplifier substep (power gain Gh): b -> sqrt(Gh) b + nu, Re nu, Im nu ~ N(0, (2nsp-1)(Gh-1)/4).
Kerr (normal-ordered NLSE in Wigner form): psi -> psi exp(i h (|psi|^2 - hbar/dx)/eps0)."""
import json, sys, time, numpy as np
from fullfield import Grid, seed, lo_covariance
rng = np.random.default_rng(20261019)

def twa(psi0, g, eps0, Gam, tau, nst, nsp, N0, M, batch):
    E0 = np.sum(np.abs(psi0)**2) * g.dx
    hb = E0 / N0
    h = tau / Gam / nst
    Dh = np.exp(1j * eps0 * g.k**2 * (h / 2) / 2)
    ga, Gh = np.exp(Gam * h / 4), np.exp(Gam * h / 2)
    sa = np.sqrt((2 * nsp - 1) * (Gh - 1) / 4 * hb / g.dx)   # per-quadrature std of nu in psi units
    s0 = np.sqrt(0.25 * hb / g.dx)
    kf = h / eps0
    # deterministic mean (noise-free) for the LO, same scheme
    p = psi0.astype(complex).copy()
    for n in range(nst):
        p = np.fft.ifft(Dh * np.fft.fft(p)); p = ga * p; p = p * np.exp(1j * kf * np.abs(p)**2); p = ga * p; p = np.fft.ifft(Dh * np.fft.fft(p))
    uL = p / np.linalg.norm(p)
    X, P, means = [], [], []
    for b in range(M // batch):
        psi = psi0[None, :] + s0 * (rng.standard_normal((batch, g.N)) + 1j * rng.standard_normal((batch, g.N)))
        for n in range(nst):
            psi = np.fft.ifft(Dh * np.fft.fft(psi, axis=1), axis=1)
            psi = ga * psi + sa * (rng.standard_normal(psi.shape) + 1j * rng.standard_normal(psi.shape))
            psi = psi * np.exp(1j * kf * (np.abs(psi)**2 - hb / g.dx))
            psi = ga * psi + sa * (rng.standard_normal(psi.shape) + 1j * rng.standard_normal(psi.shape))
            psi = np.fft.ifft(Dh * np.fft.fft(psi, axis=1), axis=1)
        bm = psi * np.sqrt(g.dx / hb)                       # mode amplitudes
        z = bm @ np.conj(uL)                                # sum_j u_j^* b_j
        X.append(2 * z.real); P.append(2 * z.imag)
        means.append(psi.mean(axis=0))
    X = np.concatenate(X); P = np.concatenate(P)
    C = np.cov(np.vstack([X, P]))
    # LO from the ensemble mean instead of the noise-free field
    pm = np.mean(means, axis=0); um = pm / np.linalg.norm(pm)
    lam = np.linalg.eigvalsh(C)[0]
    # bootstrap error of lambda_min
    nb = 200; bs = []
    idx = np.arange(len(X))
    for _ in range(nb):
        s = rng.choice(idx, size=len(idx))
        bs.append(np.linalg.eigvalsh(np.cov(np.vstack([X[s], P[s]])))[0])
    return dict(C=C.tolist(), lam_min=lam, lam_err=float(np.std(bs)), M=len(X),
                lo_mismatch=float(1 - abs(np.vdot(uL, um))), phase_of_mean_vs_noisefree=float(np.angle(np.vdot(uL, um))))

if __name__ == "__main__" and "modes" not in sys.argv:
    g = Grid(256, 12.0); eps0 = 0.05; G18 = np.sqrt(18)
    p0 = seed("gaussian", g.x)
    out = {"grid": {"N": g.N, "L": g.L}, "seed": "gaussian exp(-x^2/2)", "eps0": eps0, "Gamma": G18, "numpy_seed": 20261019, "cases": {}}
    for (nsp, tau, N0, nst) in ((1.0, 0.3, 1e6, 100), (2.0, 0.3, 1e6, 100), (1.0, 0.3, 1e3, 100), (1.0, 1.0, 1e6, 200)):
        t0 = time.time()
        lin = lo_covariance(p0, g, eps0, G18, tau, nst, nsp=nsp)
        r = twa(p0, g, eps0, G18, tau, nst, nsp, N0, M=200000, batch=20000)
        key = f"nsp{int(nsp)}_tau{tau}_N0{N0:.0e}"
        r.update(lam_linearized=lin["lam_min"], C_linearized=lin["C"].tolist(), wall=time.time() - t0,
                 dev_in_sigma=(r["lam_min"] - lin["lam_min"]) / r["lam_err"], PhiNL2_over_N0=None)
        out["cases"][key] = r
        print(key, "TWA %.5f +- %.5f   linearized %.5f   (%.1f sigma)  lo_mismatch %.1e  wall %.0fs" % (r["lam_min"], r["lam_err"], lin["lam_min"], r["dev_in_sigma"], r["lo_mismatch"], r["wall"]), flush=True)
        json.dump(out, open("twa_summary.json", "w"), indent=1)


if __name__ == "__main__" and "modes" in sys.argv:
    # validity test of TWA at small N0: dependence on the number of grid modes (TWA needs photons >> modes)
    eps0 = 0.05; G18 = np.sqrt(18)
    fn = "twa_modes_summary.json"
    res = {}
    for N, L in ((64, 12.0), (128, 12.0)):
        g = Grid(N, L); p0 = seed("gaussian", g.x)
        lin = lo_covariance(p0, g, eps0, G18, 0.3, 100, nsp=1.0)
        for N0 in (1e3, 1e4):
            r = twa(p0, g, eps0, G18, 0.3, 100, 1.0, N0, M=100000, batch=20000)
            r.update(lam_linearized=float(lin["lam_min"]), grid_modes=N)
            res[f"N{N}_N0{N0:.0e}"] = r
            print(f"modes {N} N0 {N0:.0e}: TWA %.5f +- %.5f   linearized %.5f" % (r["lam_min"], r["lam_err"], lin["lam_min"]), flush=True)
            json.dump(res, open(fn, "w"), indent=1)
