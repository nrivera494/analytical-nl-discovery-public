"""Direct epsilon = 0 computation of Lambda(Z) and Pi(Z) from dispersionless hydrodynamics (claude-b,
T-20261010-claude-interactive-05). Independent of the NLSE: integrates
    rho_Z + (rho v)_tau = 0,   v_Z + v v_tau + rho_tau = 0,   theta_Z + v^2/2 + rho = 0
(the Madelung equations without quantum pressure; theta is the scaled phase, v = theta_tau) for rho0 = exp(-tau^2),
v0 = 0, theta0 = 0 and for amplitude perturbations rho0 + 2 eta sqrt(rho0) H_m (first M Hermite functions), with a
pseudo-spectral derivative and RK4 in Z. The output scaled phase quadrature is Ytilde = sqrt(rho) dtheta / eta (central
differences), C = dYtilde/dX0, Lambda = 1/sigma_1(C)^2, Pi = 1/sigma_2(C)^2. Valid only before the gradient catastrophe
(Z <= 1). Writes hydro_direct.json.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
from sigma_c import hermite_functions

fft, ifft = np.fft.fft, np.fft.ifft


def run(Nt=1024, TW=40.0, M=80, dZ=5e-4, Zs=(0.1, 0.2, 0.3, 0.5, 0.75, 1.0), eta=1e-6):
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = t[1] - t[0]
    k = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    filt = np.exp(-36 * (np.abs(k) / np.abs(k).max()) ** 36)        # standard 2/3-like exponential filter
    D = lambda f: np.real(ifft(1j * k * filt * fft(f, axis=-1), axis=-1))
    rho0 = np.exp(-t ** 2)
    H = hermite_functions(t, M)
    pert = 2 * eta * np.sqrt(rho0)[None] * H
    R = np.concatenate([rho0[None] + pert, rho0[None] - pert, rho0[None]])
    V = np.zeros_like(R)
    TH = np.zeros_like(R)

    def rhs(R, V, TH):
        return -D(R * V), -(V * D(V) + D(R)), -(0.5 * V * V + R)

    out, Z, targets = [], 0.0, sorted(Zs)
    n_total = int(round(targets[-1] / dZ))
    ti = 0
    for step in range(1, n_total + 1):
        k1 = rhs(R, V, TH)
        k2 = rhs(R + 0.5 * dZ * k1[0], V + 0.5 * dZ * k1[1], TH + 0.5 * dZ * k1[2])
        k3 = rhs(R + 0.5 * dZ * k2[0], V + 0.5 * dZ * k2[1], TH + 0.5 * dZ * k2[2])
        k4 = rhs(R + dZ * k3[0], V + dZ * k3[1], TH + dZ * k3[2])
        R = R + dZ / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        V = V + dZ / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        TH = TH + dZ / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        Z = step * dZ
        if ti < len(targets) and abs(Z - targets[ti]) < dZ / 2:
            rb = np.maximum(R[-1], 0)
            dth = (TH[:M] - TH[M:2 * M]) / (2 * eta)                 # d theta / d (input amplitude mode)
            Yt = (np.sqrt(rb)[None] * dth * np.sqrt(dt)).T             # (Nt, M), input modes orthonormal in L2
            s = np.linalg.svd(Yt, compute_uv=False)
            out.append(dict(Z=Z, sigma1=float(s[0]), sigma2=float(s[1]), Lambda=float(1 / s[0] ** 2), Pi=float(1 / s[1] ** 2),
                            min_rho=float(R[-1].min())))
            print(out[-1], flush=True)
            ti += 1
    return out


if __name__ == "__main__":
    res = {"Nt1024_dZ5e-4": run()}
    res["Nt2048_dZ2.5e-4"] = run(Nt=2048, dZ=2.5e-4)
    cr = {round(r["Z"], 2): r for r in json.load(open(os.path.join(HERE, "curve_N200.json")))["rows"]}
    cmp = []
    for r in res["Nt2048_dZ2.5e-4"]:
        c = cr.get(round(r["Z"], 2))
        if c:
            cmp.append(dict(Z=r["Z"], Lambda_hydro=r["Lambda"], Lambda_N200=c["Lambda_red"], rel=r["Lambda"] / c["Lambda_red"] - 1,
                            Pi_hydro=r["Pi"], Pi_N200=1 / c["sigma2_C"] ** 2, rel_Pi=r["Pi"] * c["sigma2_C"] ** 2 - 1))
    res["comparison"] = cmp
    for c in cmp:
        print({k: round(v, 6) for k, v in c.items()})
    json.dump(res, open(os.path.join(HERE, "hydro_direct.json"), "w"), indent=1)
