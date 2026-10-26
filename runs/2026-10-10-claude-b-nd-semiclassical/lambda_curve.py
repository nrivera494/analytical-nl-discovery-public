"""Reduced semiclassical coefficient Lambda(Z) = 1 / sigma_max(C_Z)^2 on a fine grid of Z (claude-b,
T-20261010-claude-interactive-05). Same construction as sigma_c.py, but one propagation records the whole curve:
the batch u0 +/- eta H_m (first M Hermite functions) is propagated once and C is read out at every recorded Z.
Also records, from the mean field, the rms output bandwidth <omega^2>_out and the mean-field 'potential energy'
int rho^2 dtau (for the momentum-conservation bound on lambda_gen), and sigma_max of the amplitude block A.

Usage: python lambda_curve.py N Nt M phi_step tag   -> curve_<tag>.json
"""
import json, os, sys, time
import numpy as np
from sigma_c import hermite_functions

fft, ifft = np.fft.fft, np.fft.ifft
HERE = os.path.dirname(os.path.abspath(__file__))


def xi_wb(N):
    return 1.0 / np.sqrt(4 * N ** 2 * np.exp(-1.5) - 1)


def run(N, Nt, M, phi_step, Zmax=3.3, rec_dZ=0.01, TW=40.0, eta=1e-6, partial_path=None):
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = t[1] - t[0]
    w = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    N2 = N ** 2
    dZ = phi_step / N                      # nonlinear phase per step at the peak = phi_step
    dxi = dZ / N
    L = np.exp(0.5j * w ** 2 * dxi / 2)
    u0 = np.exp(-t ** 2 / 2) + 0j
    H = hermite_functions(t, M)
    U = np.concatenate([u0[None] + eta * H, u0[None] - eta * H, u0[None]])
    # oracle points (cases_main, cases_extra, held-out) are recorded at their exact Z as well
    zr_list = (0.1, 0.2, 0.3, 0.7, 1.0, 1.5, 2.0, 3.0)
    N_list = (5, 7, 10, 14, 20, 28, 40)
    special = sorted({round(zr * n * xi_wb(n) / dZ) for zr in zr_list for n in N_list if zr * n * xi_wb(n) <= Zmax})
    regular = set(range(int(round(rec_dZ / dZ)), int(round(Zmax / dZ)) + 1, int(round(rec_dZ / dZ))))
    targets = sorted(set(special) | regular)
    nsteps = targets[-1]
    rows = []
    k = 0
    in2 = float(np.sum(np.abs(np.fft.fft(u0)) ** 2 * w ** 2) / np.sum(np.abs(np.fft.fft(u0)) ** 2))
    t0 = time.time()
    for step in range(1, nsteps + 1):
        U = ifft(L * fft(U, axis=-1), axis=-1)
        U = U * np.exp(1j * N2 * np.abs(U) ** 2 * dxi)
        U = ifft(L * fft(U, axis=-1), axis=-1)
        if step == targets[k]:
            k += 1
            ub = U[-1]
            du = (U[:M] - U[M:2 * M]) / (2 * eta)
            ph = np.exp(-1j * np.angle(ub))
            Yt = (du * ph).imag / N * np.sqrt(dt)
            Xo = (du * ph).real * np.sqrt(dt)
            s = np.linalg.svd(Yt.T, compute_uv=False)
            sa = np.linalg.svd(Xo.T, compute_uv=False)
            sp = np.abs(np.fft.fft(ub)) ** 2
            om2 = float(np.sum(sp * w ** 2) / np.sum(sp))
            om1 = float(np.sum(sp * w) / np.sum(sp))
            rho = np.abs(ub) ** 2
            Z = step * dZ
            rows.append(dict(Z=Z, sigma_max_C=float(s[0]), Lambda_red=float(1 / s[0] ** 2), sigma2_C=float(s[1]),
                             sigma_max_A=float(sa[0]), omega2_out=om2, omega1_out=om1, omega2_in=in2,
                             int_rho2=float(np.sum(rho ** 2) * dt), int_rho=float(np.sum(rho) * dt),
                             momentum_bound_N2=float(N2 * in2 / om2)))
            if partial_path and len(rows) % 10 == 0:
                json.dump(dict(N=N, Nt=Nt, M=M, phi_step=phi_step, TW=TW, eta=eta, dZ=dZ, partial=True, rows=rows), open(partial_path, "w"))
            if k == len(targets):
                break
    return dict(N=N, Nt=Nt, M=M, phi_step=phi_step, TW=TW, eta=eta, dZ=dZ, wall=time.time() - t0, rows=rows)


if __name__ == "__main__":
    N, Nt, M, phi_step, tag = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    out = run(N, Nt, M, phi_step, partial_path=os.path.join(HERE, f"curve_{tag}.partial.json"))
    json.dump(out, open(os.path.join(HERE, f"curve_{tag}.json"), "w"), indent=1)
    print("done", tag, out["wall"])
