#!/usr/bin/env python3
"""Two-polarization dispersionless Kerr + vector Raman (isotropic a, anisotropic b) with its thermal reservoir,
propagated in z (needed for elliptical input, where the anisotropic channels exchange power between circular
components and there is no exact shear). Linear basis x, y. Units: z in [0, 1], Phi = gamma P0 L, A in sqrt(P0).
Channels (derivation note sec. 6): M0 = |Ax|^2 + |Ay|^2 (kernel r0 = a + b/2), M1 = |Ax|^2 - |Ay|^2 (r1 = b/2),
M2 = 2 Re(Ax Ay^*) (r2 = b/2); c_ik = dM_k/dA_i^*.
  dA_i/dz = i Phi [(1-fR) E_i + fR sum_k c_ik (R_k M_k)] + i sum_k c_ik Gamma_k,
  <Gamma_k(t,z) Gamma_k(t',z')> = (Phi fR / 2) H_k(t-t') delta(z-z'),  H_k = 2|Im r_k~| coth (symmetrized).
Lab-frame quadratures X_c = 2 Re dA_c, Y_c = 2 Im dA_c (shot noise 1). Covariance by the Lyapunov equation
dV/dz = J V + (J V)^T + D(z), V(0) = I, RK4 together with the mean field; J applied as an operator.
Usage: python vector_raman_prop.py out.json"""
import json, sys, time, warnings
import numpy as np
from numpy.fft import fftfreq
warnings.filterwarnings("ignore")
from dlfano import htilde_blow_wood, toeplitz_from_lags, gaussian_p, binary_search4
from vector_raman_exact import hb_tilde, lag_kernels_custom

def kernels(n, dt, TK, split, fR):
    fa, fb, fc = 0.75, 0.21, 0.04
    ha = lambda w: htilde_blow_wood(w)
    if split == "A":
        a = lambda w: fa * ha(w); b = lambda w: fc * ha(w) + fb * hb_tilde(w)
    else:
        a = lambda w: (fa + fc) * ha(w); b = lambda w: fb * hb_tilde(w)
    r = [lambda w: a(w) + 0.5 * b(w), lambda w: 0.5 * b(w), lambda w: 0.5 * b(w)]
    Rm, Hm = [], []
    for rk in r:
        k, Hk = lag_kernels_custom(n, dt, rk, TK)
        Rm.append(toeplitz_from_lags(k, n)); Hm.append(toeplitz_from_lags(Hk, n))
    return Rm, Hm

def rhs_field(Ax, Ay, Phi, fR, Rm):
    ax2, ay2 = np.abs(Ax) ** 2, np.abs(Ay) ** 2
    Ex = (ax2 + (2 / 3) * ay2) * Ax + (1 / 3) * np.conj(Ax) * Ay**2
    Ey = (ay2 + (2 / 3) * ax2) * Ay + (1 / 3) * np.conj(Ay) * Ax**2
    M = [ax2 + ay2, ax2 - ay2, 2 * np.real(Ax * np.conj(Ay))]
    RM = [Rm[k] @ M[k] for k in range(3)] if fR > 0 else [0, 0, 0]
    Fx = 1j * Phi * ((1 - fR) * Ex + fR * (Ax * RM[0] + Ax * RM[1] + Ay * RM[2]))
    Fy = 1j * Phi * ((1 - fR) * Ey + fR * (Ay * RM[0] - Ay * RM[1] + Ax * RM[2]))
    return Fx, Fy, RM

def apply_J(Ax, Ay, RM, Phi, fR, Rm, U):
    """U: (4n, m) real columns [X_x; Y_x; X_y; Y_y] -> J U."""
    n = len(Ax)
    dAx = (U[:n] + 1j * U[n:2 * n]) / 2; dAy = (U[2 * n:3 * n] + 1j * U[3 * n:]) / 2
    AX, AY = Ax[:, None], Ay[:, None]
    ax2, ay2 = np.abs(AX) ** 2, np.abs(AY) ** 2
    dEx = (2 * ax2 * dAx + AX**2 * np.conj(dAx) + (2 / 3) * ay2 * dAx + (2 / 3) * AX * 2 * np.real(np.conj(AY) * dAy)
           + (1 / 3) * AY**2 * np.conj(dAx) + (2 / 3) * np.conj(AX) * AY * dAy)
    dEy = (2 * ay2 * dAy + AY**2 * np.conj(dAy) + (2 / 3) * ax2 * dAy + (2 / 3) * AY * 2 * np.real(np.conj(AX) * dAx)
           + (1 / 3) * AX**2 * np.conj(dAy) + (2 / 3) * np.conj(AY) * AX * dAx)
    dFx = (1 - fR) * dEx; dFy = (1 - fR) * dEy
    if fR > 0:
        sx = 2 * np.real(np.conj(AX) * dAx); sy = 2 * np.real(np.conj(AY) * dAy)
        dM = [sx + sy, sx - sy, 2 * np.real(dAx * np.conj(AY) + AX * np.conj(dAy))]
        RdM = [Rm[k] @ dM[k] for k in range(3)]
        RMc = [x[:, None] for x in RM]
        dFx = dFx + fR * (dAx * RMc[0] + AX * RdM[0] + dAx * RMc[1] + AX * RdM[1] + dAy * RMc[2] + AY * RdM[2])
        dFy = dFy + fR * (dAy * RMc[0] + AY * RdM[0] - dAy * RMc[1] - AY * RdM[1] + dAx * RMc[2] + AX * RdM[2])
    dFx = 1j * Phi * dFx; dFy = 1j * Phi * dFy
    return np.vstack([2 * dFx.real, 2 * dFx.imag, 2 * dFy.real, 2 * dFy.imag])

def noise_D(Ax, Ay, Phi, fR, Hm):
    n = len(Ax)
    if fR == 0:
        return np.zeros((4 * n, 4 * n))
    c = [(Ax, Ay), (Ax, -Ay), (Ay, Ax)]
    D = np.zeros((4 * n, 4 * n))
    for k in range(3):
        cx, cy = c[k]
        g = np.concatenate([-cx.imag, cx.real, -cy.imag, cy.real])        # noise i c Gamma -> (X, Y) = 2 Gamma (-Im c, Re c)
        Hk4 = np.tile(Hm[k], (4, 4))
        D += 2 * Phi * fR * (g[:, None] * Hk4 * g[None, :])
    return D

def propagate(p, dt, Phi, fR, chi, Rm, Hm, nz):
    n = len(p)
    Ax = (np.sqrt(p) * np.cos(chi)).astype(complex); Ay = 1j * np.sqrt(p) * np.sin(chi)
    V = np.eye(4 * n); dz = 1.0 / nz
    def f(Ax, Ay, V):
        Fx, Fy, RM = rhs_field(Ax, Ay, Phi, fR, Rm)
        JV = apply_J(Ax, Ay, RM, Phi, fR, Rm, V)
        return Fx, Fy, JV + JV.T + noise_D(Ax, Ay, Phi, fR, Hm)
    for _ in range(nz):
        k1 = f(Ax, Ay, V)
        k2 = f(Ax + 0.5 * dz * k1[0], Ay + 0.5 * dz * k1[1], V + 0.5 * dz * k1[2])
        k3 = f(Ax + 0.5 * dz * k2[0], Ay + 0.5 * dz * k2[1], V + 0.5 * dz * k2[2])
        k4 = f(Ax + dz * k3[0], Ay + dz * k3[1], V + dz * k3[2])
        Ax = Ax + dz / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        Ay = Ay + dz / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        V = V + dz / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
    return Ax, Ay, 0.5 * (V + V.T)

def bins_insensitive(Ax, Ay, V, dt, pad=8, thr=1e-6):
    """Polarization-resolved amplitude-quadrature bins (x then y), then polarization-insensitive combination."""
    n = len(Ax); ntot = pad * n
    t = (np.arange(ntot) - ntot // 2) * dt; i0 = ntot // 2 - n // 2
    w = 2 * np.pi * fftfreq(ntot, dt)
    Fm = np.exp(1j * np.outer(w, t)) / np.sqrt(ntot)
    rows, nbs, ws, vac = [], [], [], []
    Abs = []
    for A in (Ax, Ay):
        full = np.zeros(ntot, complex); full[i0:i0 + n] = A
        Abs.append(Fm @ full)
    gmax = max(float((np.abs(Ab) ** 2).max()) for Ab in Abs)       # one threshold for both channels
    for c, A in enumerate((Ax, Ay)):
        Ab = Abs[c]; nb = np.abs(Ab) ** 2
        keep = nb >= thr * gmax
        if not keep.any():
            continue                                                 # dark channel: no bins (linear order)
        psi = np.angle(Ab[keep])
        G = np.exp(-1j * psi)[:, None] * Fm[keep][:, i0:i0 + n]
        B = np.zeros((keep.sum(), 4 * n))
        B[:, 2 * c * n:(2 * c + 1) * n] = G.real; B[:, (2 * c + 1) * n:(2 * c + 2) * n] = -G.imag
        rows.append(B); nbs.append(nb[keep]); ws.append(w[keep])
        mask = np.ones(ntot, bool); mask[i0:i0 + n] = False
        Go = (np.exp(-1j * psi)[:, None] * Fm[keep])[:, mask]
        vac.append((Go @ Go.conj().T).real)
    B = np.vstack(rows); Va = B @ V @ B.T
    off = 0
    for v in vac:
        k = v.shape[0]; Va[off:off + k, off:off + k] += v; off += k
    nb = np.concatenate(nbs); w = np.concatenate(ws)
    s = np.sqrt(nb); Sig = s[:, None] * Va * s[None, :]
    key = np.round(w, 9); freqs = np.unique(key)
    Mx = (key[None, :] == freqs[:, None]).astype(float)
    Sig2 = Mx @ Sig @ Mx.T; nb2 = Mx @ nb
    ok = nb2 > 0
    Sig2 = Sig2[np.ix_(ok, ok)]; nb2 = nb2[ok]; freqs = freqs[ok]
    s2 = np.sqrt(nb2)
    return nb, Va, w, nb2, Sig2 / s2[:, None] / s2[None, :], freqs

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "vector_raman_prop.json"
    cases = [  # (label, T0 fs, T K, fR, chi, split)
        ("check: Kerr only, elliptical chi=pi/8 (compare polarization.json)", 200.0, 0.0, 0.0, np.pi / 8, "A"),
        ("check: circular, split A, 300 K (compare vector_raman_exact.json)", 200.0, 300.0, 0.245, np.pi / 4, "A"),
        ("check: linear, 300 K (compare vector_raman_exact.json)", 200.0, 300.0, 0.245, 0.0, "A"),
        ("elliptical chi=pi/8, split A, 0 K", 200.0, 0.0, 0.245, np.pi / 8, "A"),
        ("elliptical chi=pi/8, split A, 300 K", 200.0, 300.0, 0.245, np.pi / 8, "A"),
        ("elliptical chi=pi/8, split B, 300 K", 200.0, 300.0, 0.245, np.pi / 8, "B"),
    ]
    Phi = 10.0
    rows = []
    import os
    sel = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else list(range(len(cases)))
    if len(sys.argv) > 2 and os.path.exists(out):
        rows = json.load(open(out))["rows"]
    for ci, (label, T0, TK, fR, chi, split) in enumerate(cases):
        if ci not in sel:
            continue
        t0 = time.time()
        dt = min(0.8 / Phi, 0.04) * T0; t = np.arange(-7 * T0, 7 * T0, dt); p = gaussian_p(t, T0)
        n = len(p)
        Rm, Hm = kernels(n, dt, TK, split, fR) if fR > 0 else (None, None)
        Ax, Ay, V = propagate(p, dt, Phi, fR, chi, Rm, Hm, nz=400)
        Om = np.zeros((4 * n, 4 * n)); I = np.eye(n)
        Om[:n, n:2 * n] = I; Om[n:2 * n, :n] = -I; Om[2 * n:3 * n, 3 * n:] = I; Om[3 * n:, 2 * n:3 * n] = -I   # vacuum V = I, [X,Y] = 2i: V + i Om >= 0
        symp = float(np.linalg.eigvalsh(V + 1j * Om)[0])
        lmin = float(np.linalg.eigvalsh(V)[0])
        nb, Va, w, nb2, Va2, f2 = bins_insensitive(Ax, Ay, V, dt)
        lg_res = float(np.linalg.eigvalsh(Va)[0]); lg_ins = float(np.linalg.eigvalsh(Va2)[0])
        rb = binary_search4(nb2, Va2, f2)
        P0 = np.abs(Ax) ** 2 + np.abs(Ay) ** 2
        Ap = (Ax - 1j * Ay) / np.sqrt(2); Am = (Ax + 1j * Ay) / np.sqrt(2)
        k0 = np.argmin(np.abs(t))
        row = {"case": label, "T0_fs": T0, "T_K": TK, "fR": fR, "chi": chi, "split": split, "Phi": Phi, "N_t": n,
               "lam_min": lmin, "symplectic_min": symp, "lam_gen_resolved_xy": lg_res, "lam_gen_insensitive": lg_ins,
               "binary_insensitive": rb["F"], "power_conservation_err": float(np.abs(P0 - p).max()),
               "peak_circ_fraction_plus_out": float(np.abs(Ap[k0]) ** 2 / P0[k0]),
               "peak_circ_fraction_plus_in": float((np.cos(chi) + np.sin(chi)) ** 2 / 2),
               "wall_s": round(time.time() - t0, 1)}
        rows.append(row); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
