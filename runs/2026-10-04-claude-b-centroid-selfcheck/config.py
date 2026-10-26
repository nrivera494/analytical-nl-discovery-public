"""Self-check of the centroid theorem on P-20261004-claude-interactive-02 (claude-b, same family; not a verification).

Model: i a_z + 1/2 a_tt + (C11|a|^2+C12|b|^2) a = 0 ;  i b_z + i d b_t + 1/2 b_tt + (C21|a|^2+C22|b|^2) b = 0.
Claim: T_c = sum_m int t|A_m|^2 dt / N moves at constant velocity V = (d N_b + J)/N with J = int Im(A* A_t) summed
(this model: a_t-momentum enters with the dispersion coefficient 1/2 -> dT_c/dz = (d N_b + J)/N, J = sum int Im(A^* A_t)).
Checks: (1) deterministic: T_c(z) is linear in z, slope equals V(0); (2) linearized launch noise:
Var[(T_c(z)-T_c(0))/z] equals Var[V(0)] at all z, and the partition part of Var[V(0)] equals d^2 p_a p_b / N
(in units where the sensitivity formula gives Var for one 'photon' normalisation).
"""
import json, sys
import numpy as np
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "2026-10-04-claude-b-reduction-selfcheck"))
from config import propagate, t, dt, w, N as NPTS  # same grid and integrator as run 2026-10-04-claude-b-reduction-selfcheck


def centroid(a, b):
    Ia, Ib = np.abs(a)**2, np.abs(b)**2
    M = np.sum(Ia + Ib, axis=-1) * dt
    return np.sum(t * (Ia + Ib), axis=-1) * dt / M, M


def velocity(a, b, d):
    def J(f):
        ft = np.fft.ifft(1j * w * np.fft.fft(f, axis=-1), axis=-1)
        return np.sum(np.imag(np.conj(f) * ft), axis=-1) * dt
    Nb = np.sum(np.abs(b)**2, axis=-1) * dt
    _, M = centroid(a, b)
    return (d * Nb + J(a) + J(b)) / M


def grads(fun, a0, b0, eps=1e-6):
    dirs = []
    for which in (0, 1):
        for q in (1.0, 1j):
            for i in range(NPTS):
                e = np.zeros((2, NPTS), complex); e[which, i] = q * eps / np.sqrt(dt); dirs.append(e)
    E = np.array(dirs)
    A = np.concatenate([a0[None] + E[:, 0], a0[None] - E[:, 0]]); B = np.concatenate([b0[None] + E[:, 1], b0[None] - E[:, 1]])
    X = fun(A, B); M = len(dirs)
    return (X[:M] - X[M:]) / (2 * eps)


def main():
    sech = 1 / np.cosh(t)
    d, eps, C, dz = 0.8, np.sqrt(0.25), [[1, 1], [1, 0.5]], 2e-3   # p_b = eps^2/(1+eps^2) = 0.2
    a0, b0 = sech + 0j, eps * sech + 0j
    out = {"d": d, "eps": eps, "C": C}
    # (1) deterministic linearity of T_c(z)
    zs = [0.0, 0.5, 1.0, 1.5, 2.0]
    Tc = []
    for z in zs:
        a, b = propagate(a0[None], b0[None], z, dz, C, d) if z > 0 else (a0[None], b0[None])
        Tc.append(float(centroid(a, b)[0][0]))
    V0 = float(velocity(a0[None], b0[None], d)[0])
    out["Tc_of_z"] = dict(zip(map(str, zs), Tc)); out["V0"] = V0
    out["max_dev_from_line"] = float(max(abs(Tc[i] - (Tc[0] + V0 * zs[i])) for i in range(len(zs))))
    # (2) noise: Var(V0) and Var of centroid displacement / z
    gV = grads(lambda A, B: velocity(A, B, d), a0, b0)
    varV = 0.25 * np.sum(gV**2)
    res = {}
    for z in (1.0, 2.0):
        gT = grads(lambda A, B: (centroid(*propagate(A, B, z, dz, C, d))[0] - centroid(A, B)[0]) / z, a0, b0)
        res[str(z)] = float(0.25 * np.sum(gT**2))
    out["Var_V0"] = float(varV); out["Var_displacement_over_z"] = res
    # partition part: velocity noise from N_b/N fluctuations only, prediction d^2 p_a p_b / M (normalised 'photon' units)
    Na = float(np.sum(np.abs(a0)**2) * dt); Nb = float(np.sum(np.abs(b0)**2) * dt); M = Na + Nb
    gP = grads(lambda A, B: d * (np.sum(np.abs(B)**2, axis=-1) * dt) / (np.sum(np.abs(A)**2 + np.abs(B)**2, axis=-1) * dt), a0, b0)
    out["Var_partition_part"] = float(0.25 * np.sum(gP**2))
    out["predicted_partition_d2_pa_pb_over_M"] = d**2 * (Na / M) * (Nb / M) / M
    gJ = grads(lambda A, B: velocity(A, B, 0.0), a0, b0)
    out["Var_momentum_part"] = float(0.25 * np.sum(gJ**2))
    out["predicted_momentum_1_over_3M"] = 1.0 / (3 * M)
    out["ratio_partition_to_momentum"] = out["Var_partition_part"] / out["Var_momentum_part"]
    out["predicted_ratio_3_d2_pa_pb"] = 3 * d**2 * (Na / M) * (Nb / M)
    print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
