"""Self-check of the reductions in the P-20261004-root-03 / -01 review (claude-b, same family; not a verification).

Two-mode NLS, dimensionless:  i a_z + 1/2 a_tt + (C11|a|^2 + C12|b|^2) a = 0
                               i b_z + i d b_t + 1/2 b_tt + (C21|a|^2 + C22|b|^2) b = 0
Linearized vacuum noise via the sensitivity formula for coherent inputs:
  Var(X) = (1/4) sum_i [(dX/dx_i)^2 + (dX/dp_i)^2],  input field psi_i = x_i + i p_i (photon units / sqrt(nbar)),
  F = Var/<X> is independent of nbar. Hard 0/1 bandpass (no partition vacuum). Gradients by central differences
  of the discrete split-step map, all 4N directions propagated as one batch.
"""
import json, sys
import numpy as np

N, TW = 256, 40.0
t = (np.arange(N) - N // 2) * (TW / N)
dt = t[1] - t[0]
w = 2 * np.pi * np.fft.fftfreq(N, d=dt)


def propagate(a, b, z, dz, C, d):
    """a,b: (..., N) complex arrays. Strang split-step."""
    La = np.exp((-0.5j * w**2) * dz / 2)            # i a_z = -1/2 a_tt -> a_z = (i/2) a_tt -> Fourier: -(i/2) w^2
    Lb = np.exp((-0.5j * w**2 + 1j * d * w * 0 - d * 1j * w * 0) * dz / 2)
    # walk-off term: i b_z + i d b_t = ... -> b_z = -d b_t + ...; Fourier of b_t is (i w) b (numpy ifft convention: ifft(fft(f)*1j*w) = f')
    Lb = np.exp((-0.5j * w**2 - d * 1j * w) * dz / 2)
    n = int(round(z / dz))
    for _ in range(n):
        a = np.fft.ifft(La * np.fft.fft(a, axis=-1), axis=-1)
        b = np.fft.ifft(Lb * np.fft.fft(b, axis=-1), axis=-1)
        Ia, Ib = np.abs(a)**2, np.abs(b)**2
        a = a * np.exp(1j * (C[0][0] * Ia + C[0][1] * Ib) * dz)
        b = b * np.exp(1j * (C[1][0] * Ia + C[1][1] * Ib) * dz)
        a = np.fft.ifft(La * np.fft.fft(a, axis=-1), axis=-1)
        b = np.fft.ifft(Lb * np.fft.fft(b, axis=-1), axis=-1)
    return a, b


def counts(a, b, maskA, maskB):
    """Filtered photon counts per mode (unitary FFT normalisation, field samples scaled by sqrt(dt))."""
    fa = np.fft.fft(a, axis=-1) * np.sqrt(dt / N)
    fb = np.fft.fft(b, axis=-1) * np.sqrt(dt / N)
    return np.sum(maskA * np.abs(fa)**2, axis=-1), np.sum(maskB * np.abs(fb)**2, axis=-1)


def noise(a0, b0, z, dz, C, d, maskA, maskB, eps=1e-6):
    # perturbation directions: x and p of every sample of a and b; psi_i = sqrt(dt) * field sample
    dirs = []
    for which in (0, 1):
        for q in (1.0, 1j):
            for i in range(N):
                e = np.zeros((2, N), complex); e[which, i] = q * eps / np.sqrt(dt); dirs.append(e)
    E = np.array(dirs)                        # (4N, 2, N)
    A = np.concatenate([a0[None] + E[:, 0], a0[None] - E[:, 0]])
    B = np.concatenate([b0[None] + E[:, 1], b0[None] - E[:, 1]])
    ao, bo = propagate(A, B, z, dz, C, d)
    Xa, Xb = counts(ao, bo, maskA, maskB)
    M = len(dirs)
    ga = (Xa[:M] - Xa[M:]) / (2 * eps); gb = (Xb[:M] - Xb[M:]) / (2 * eps)
    am, bm = propagate(a0[None], b0[None], z, dz, C, d)
    Xa0, Xb0 = counts(am, bm, maskA, maskB)
    va, vb, cab = 0.25 * np.sum(ga**2), 0.25 * np.sum(gb**2), 0.25 * np.sum(ga * gb)
    return dict(Na=float(Xa0[0]), Nb=float(Xb0[0]), Fa=float(va / Xa0[0]), Fb=float(vb / Xb0[0]) if Xb0[0] > 0 else None,
                rho=float(cab / np.sqrt(va * vb)) if vb > 0 else None,
                Ftot=float((va + vb + 2 * cab) / (Xa0[0] + Xb0[0])))


def main():
    z, dz, Wf = 2.0, 2e-3, 0.8
    mask = (np.abs(w) < Wf).astype(float)
    sech = 1 / np.cosh(t)
    out = {"grid": {"N": N, "T_window": TW, "z": z, "dz": dz, "filter_halfwidth": Wf}}
    # scalar reference F_s
    s = noise(sech.astype(complex), 0 * sech + 0j, z, dz, [[1, 1], [1, 1]], 0.0, mask, mask)
    Fs = s["Fa"]; out["scalar"] = s
    # (1) Manakov rotation, theta = 0.3
    th = 0.3
    m = noise(np.cos(th) * sech + 0j, np.sin(th) * sech + 0j, z, dz, [[1, 1], [1, 1]], 0.0, mask, mask)
    pred = dict(Fa=np.cos(th)**2 * Fs + np.sin(th)**2, Fb=np.sin(th)**2 * Fs + np.cos(th)**2)
    pred["rho"] = np.cos(th) * np.sin(th) * (Fs - 1) / np.sqrt(pred["Fa"] * pred["Fb"]); pred["Ftot"] = Fs
    out["manakov_theta0.3"] = {"computed": m, "rotation_prediction": {k: float(v) for k, v in pred.items()}}
    # (2) GRIN matrix C22 = 1/2, small eps: rho vs eps (Fs-1)/sqrt(Fs)
    grin = []
    for eps in (0.025, 0.05, 0.1, 0.2):
        g = noise(sech + 0j, eps * sech + 0j, z, dz, [[1, 1], [1, 0.5]], 0.0, mask, mask)
        th = np.arctan(eps)
        rho_rot = np.cos(th) * np.sin(th) * (Fs - 1) / np.sqrt((np.cos(th)**2 * Fs + np.sin(th)**2) * (np.sin(th)**2 * Fs + np.cos(th)**2))
        grin.append({"eps": eps, "computed": g, "rho_first_order": float(eps * (Fs - 1) / np.sqrt(Fs)),
                     "rho_manakov_rotation": float(rho_rot), "Fb_minus_1": g["Fb"] - 1, "Fa_minus_Fs": g["Fa"] - Fs})
    out["grin_small_eps"] = grin
    # (3) walk-off gauge: d = 1 versus frequency-offset launch with shifted minority filter
    d, eps = 2 * np.pi * 6 / TW, 0.2   # commensurate with the frequency grid (0.942)
    g1 = noise(sech + 0j, eps * sech + 0j, z, dz, [[1, 1], [1, 0.5]], d, mask, mask)
    maskB_shift = (np.abs(w + d) < Wf).astype(float)   # b = btilde e^{-i d t}: spectrum of b shifted by -d relative to btilde
    g2 = noise(sech + 0j, eps * sech * np.exp(1j * d * t), z, dz, [[1, 1], [1, 0.5]], 0.0, mask, (np.abs(w - d) < Wf).astype(float))
    out["walkoff_gauge"] = {"d": d, "eps": eps, "walkoff_run": g1, "frequency_offset_run": g2}
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "manakov_check.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
