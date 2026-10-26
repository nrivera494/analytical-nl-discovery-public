#!/usr/bin/env python3
"""Anisotropic Raman, exact reductions (derivation note sec. 6): with the vector response split into channels
M0 = |Ax|^2+|Ay|^2 (kernel a + b/2), M1 = |Ax|^2-|Ay|^2 and M2 = 2 Re Ax Ay^* (kernel b/2 each):
  linear input   -> scalar exact shear with R = (1-fR) delta + fR (a + b),       reservoir from a + b
  circular input -> scalar exact shear with R = (2/3)(1-fR) delta + fR (a + b/2), reservoir from a + b/2
(orthogonal component dark at linear order). Lin-Agrawal-type kernels (parameters from the gnlse-python source):
fR = 0.245, h_a = Blow-Wood(12.2, 32 fs), h_b(t) = (2 tb - t)/tb^2 exp(-t/tb), tb = 96 fs, fa = 0.75, fb = 0.21, fc = 0.04.
The isotropic/anisotropic split of the fc term is not known here, so two splits are run:
  A: a = fa ha,        b = fc ha + fb hb   (rho = int b = 0.25)
  B: a = (fa+fc) ha,   b = fb hb           (rho = 0.21)
Usage: python vector_raman_exact.py out.json"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import (htilde_blow_wood, toeplitz_from_lags, covariance, lam_min, lam_pass, spectral, lam_gen,
                    binary_search4, gaussian_p, symplectic_check, lam_min_band, HBAR, KB)

TB = 96.0
def hb_tilde(w):
    u = w * TB
    return (1 - 2j * u) / (1 - 1j * u) ** 2

def lag_kernels_custom(N, dt, hfun, temp_K, n_w=2**18, w_max=None):
    if w_max is None:
        w_max = max(40.0 / 12.2, 40.0 / dt)
    w = np.linspace(-w_max, w_max, n_w); dw = w[1] - w[0]
    sinc2 = np.sinc(w * dt / (2 * np.pi)) ** 2
    ht = hfun(w)
    if temp_K > 0:
        x = HBAR * np.abs(w) * 1e15 / (2 * KB * temp_K)
        coth = np.where(x > 1e-12, 1.0 / np.tanh(np.maximum(x, 1e-300)), 0.0)
        Sres = 2 * np.abs(ht.imag) * coth
        limw = np.abs(w) < 1e-12
        if limw.any():
            c = HBAR * 1e15 / (2 * KB * temp_K)
            dImh = (hfun(np.array([1e-6])).imag - hfun(np.array([-1e-6])).imag)[0] / 2e-6
            Sres[limw] = 2 * abs(dImh) / c
    else:
        Sres = 2 * np.abs(ht.imag)
    lags = np.arange(-(N - 1), N) * dt
    k = np.empty(len(lags)); Hk = np.empty(len(lags))
    for i0 in range(0, len(lags), 256):
        tau = lags[i0:i0 + 256]
        ph = np.exp(-1j * np.outer(tau, w))
        k[i0:i0 + 256] = (ph @ (ht * sinc2)).real * dw / (2 * np.pi) * dt
        Hk[i0:i0 + 256] = (ph @ (Sres * sinc2)).real * dw / (2 * np.pi) * dt
    return k, Hk

def build(p, dt, Phi, e_fac, fR, k, Hk):
    N = len(p); sp = np.sqrt(p)
    Rm = e_fac * np.eye(N) + fR * toeplitz_from_lags(k, N)
    Hm = fR * toeplitz_from_lags(Hk, N)
    return {"K": 2 * Phi * sp[:, None] * Rm * sp[None, :], "N": 2 * Phi * sp[:, None] * Hm * sp[None, :],
            "phibar": Phi * (Rm @ p), "p": p, "dt": dt}

if __name__ == "__main__":
    fR, fa, fb, fc = 0.245, 0.75, 0.21, 0.04
    ha = lambda w: htilde_blow_wood(w)
    configs = {
        "linear (a+b, both splits)": (1 - fR, lambda w: (fa + fc) * ha(w) + fb * hb_tilde(w)),
        "circular, split A": ((2 / 3) * (1 - fR), lambda w: (fa + fc / 2) * ha(w) + (fb / 2) * hb_tilde(w)),
        "circular, split B": ((2 / 3) * (1 - fR), lambda w: (fa + fc) * ha(w) + (fb / 2) * hb_tilde(w)),
    }
    out = sys.argv[1] if len(sys.argv) > 1 else "vector_raman_exact.json"
    rows = []
    Phi = 10.0
    for T0 in (200.0, 1000.0):
        dt = min(0.8 / Phi, 0.04) * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
        for TK in (0.0, 300.0):
            for name, (e_fac, hfun) in configs.items():
                t0 = time.time()
                k, Hk = lag_kernels_custom(len(t), dt, hfun, TK)
                m = build(p, dt, Phi, e_fac, fR, k, Hk)
                V = covariance(m)
                nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
                y = w * np.sqrt(nb)
                r = binary_search4(nb, Va, w)
                Phi_eff_long = Phi * (e_fac + fR * float(hfun(np.array([0.0]))[0].real))
                row = {"T0_fs": T0, "T_K": TK, "config": name, "Phi": Phi, "Phi_eff_longpulse": Phi_eff_long,
                       "lam_min": lam_min(V), "lam_min_band": lam_min_band(m, V)[0], "lam_gen": lam_gen(Va),
                       "lam_momentum": float(y @ Va @ y / (y @ y)), "binary_F": r["F"],
                       "symplectic_min": symplectic_check(V), "wall_s": round(time.time() - t0, 1)}
                rows.append(row); print(json.dumps({kk: (round(v, 6) if isinstance(v, float) else v) for kk, v in row.items()}), flush=True)
                json.dump({"rows": rows}, open(out, "w"), indent=1)
