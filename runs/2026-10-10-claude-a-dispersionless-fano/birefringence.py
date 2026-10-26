#!/usr/bin/env python3
"""Dispersionless two-polarization Kerr with linear birefringence of arbitrary strength (no walk-off, no Raman):
    dA_x/dz = +i(db/2) A_x + i g [(|A_x|^2 + (2/3)|A_y|^2) A_x + (1/3) A_x^* A_y^2]
    dA_y/dz = -i(db/2) A_y + i g [(|A_y|^2 + (2/3)|A_x|^2) A_y + (1/3) A_y^* A_x^2]
Units: T0 = 1, L = 1, g P0 L = Phi, db L = b Phi with b = Delta-beta/(gamma P0) = 2 pi L_NL/L_B.
b -> 0: isotropic fibre; b -> infinity: strong birefringence (coherent term averages out).
Without dispersion every time slice evolves independently, so the tangent map is 4x4 per slice (RK4 in z).
Reports lambda_min(V), lambda_gen for polarization-resolved and polarization-insensitive spectral bins, the momentum
bound <w^2>_in/<w^2>_out (total over both channels; momentum and number are conserved here), the parity bound, and
the best binary filter (box relaxation + dithering + tabu, as binary_relax.py).
Usage: python birefringence.py out.json [Phi] [theta_deg] [b list]"""
import json, sys, time, warnings
import numpy as np
from numpy.fft import fftfreq
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
from dlfano import gaussian_p, vmin_kerr, fano_of, best_improvement, tabu_search


def rhs(Ax, Ay, Px, Py, g, db):
    """Field and tangent right-hand sides. Px, Py: (n, k) complex perturbations."""
    ax2, ay2 = np.abs(Ax) ** 2, np.abs(Ay) ** 2
    fAx = 1j * (db / 2) * Ax + 1j * g * ((ax2 + (2 / 3) * ay2) * Ax + (1 / 3) * np.conj(Ax) * Ay**2)
    fAy = -1j * (db / 2) * Ay + 1j * g * ((ay2 + (2 / 3) * ax2) * Ay + (1 / 3) * np.conj(Ay) * Ax**2)
    AX, AY = Ax[:, None], Ay[:, None]
    dNx = (2 * np.abs(AX) ** 2 * Px + AX**2 * np.conj(Px) + (2 / 3) * np.abs(AY) ** 2 * Px
           + (2 / 3) * AX * (np.conj(AY) * Py + AY * np.conj(Py)) + (1 / 3) * AY**2 * np.conj(Px)
           + (2 / 3) * np.conj(AX) * AY * Py)
    dNy = (2 * np.abs(AY) ** 2 * Py + AY**2 * np.conj(Py) + (2 / 3) * np.abs(AX) ** 2 * Py
           + (2 / 3) * AY * (np.conj(AX) * Px + AX * np.conj(Px)) + (1 / 3) * AX**2 * np.conj(Py)
           + (2 / 3) * np.conj(AY) * AX * Px)
    fPx = 1j * (db / 2) * Px + 1j * g * dNx
    fPy = -1j * (db / 2) * Py + 1j * g * dNy
    return fAx, fAy, fPx, fPy


def propagate(p, Phi, b, cx, nz):
    n = len(p)
    Ax = np.sqrt(p * cx).astype(complex); Ay = np.sqrt(p * (1 - cx)).astype(complex)
    # perturbation basis per slice: X_x, Y_x, X_y, Y_y  (dA = (X + iY)/2)
    Px = np.zeros((n, 4), complex); Py = np.zeros((n, 4), complex)
    Px[:, 0] = 0.5; Px[:, 1] = 0.5j; Py[:, 2] = 0.5; Py[:, 3] = 0.5j
    g, db, dz = Phi, b * Phi, 1.0 / nz
    for _ in range(nz):
        k1 = rhs(Ax, Ay, Px, Py, g, db)
        k2 = rhs(Ax + 0.5 * dz * k1[0], Ay + 0.5 * dz * k1[1], Px + 0.5 * dz * k1[2], Py + 0.5 * dz * k1[3], g, db)
        k3 = rhs(Ax + 0.5 * dz * k2[0], Ay + 0.5 * dz * k2[1], Px + 0.5 * dz * k2[2], Py + 0.5 * dz * k2[3], g, db)
        k4 = rhs(Ax + dz * k3[0], Ay + dz * k3[1], Px + dz * k3[2], Py + dz * k3[3], g, db)
        Ax = Ax + dz / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        Ay = Ay + dz / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        Px = Px + dz / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        Py = Py + dz / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
    # per-slice output map M_t (4x4): rows X_x, Y_x, X_y, Y_y (lab frame), columns the input quadratures
    M = np.stack([2 * Px.real, 2 * Px.imag, 2 * Py.real, 2 * Py.imag], axis=1)   # (n, 4, 4)
    return Ax, Ay, M


def bins(Ax, Ay, M, dt, pad=4, thr=1e-6):
    """Polarization-resolved bins (channel x then y). Returns nbar, Vamp, w, channel."""
    n = len(Ax); ntot = pad * n
    t = (np.arange(ntot) - ntot // 2) * dt; i0 = ntot // 2 - n // 2
    w = 2 * np.pi * fftfreq(ntot, dt)
    Fm = np.exp(1j * np.outer(w, t)) / np.sqrt(ntot)
    # full input-to-output map S (4n x 4n), output rows ordered [X_x(t), Y_x(t), X_y(t), Y_y(t)] blocks over t
    rowsM, nbs, ws, chs, vacs = [], [], [], [], []
    for c, A in enumerate((Ax, Ay)):
        full = np.zeros(ntot, complex); full[i0:i0 + n] = A
        Ab = Fm @ full; nb = np.abs(Ab) ** 2
        keep = nb >= thr * nb.max()
        psi = np.angle(Ab[keep])
        G = np.exp(-1j * psi)[:, None] * Fm[keep][:, i0:i0 + n]               # bins x n
        # bin amplitude quadrature = Re(G) X_c - Im(G) Y_c ; X_c(t) = sum_j M[t, 2c, j] u_j(t)
        Xc = M[:, 2 * c, :]; Yc = M[:, 2 * c + 1, :]                         # (n, 4)
        # result: bins x (4n) with input ordering (t, j)
        R = (G.real[:, :, None] * Xc[None, :, :] - G.imag[:, :, None] * Yc[None, :, :]).reshape(keep.sum(), 4 * n)
        rowsM.append(R); nbs.append(nb[keep]); ws.append(w[keep]); chs.append(np.full(keep.sum(), c))
        mask = np.ones(ntot, bool); mask[i0:i0 + n] = False
        Go = (np.exp(-1j * psi)[:, None] * Fm[keep])[:, mask]
        vacs.append((Go @ Go.conj().T).real)
    R = np.vstack(rowsM)
    Vamp = R @ R.T
    off = 0
    for v in vacs:
        k = v.shape[0]; Vamp[off:off + k, off:off + k] += v; off += k
    return np.concatenate(nbs), Vamp, np.concatenate(ws), np.concatenate(chs)


def insensitive(nb, Vamp, w):
    s = np.sqrt(nb); Sig = s[:, None] * Vamp * s[None, :]
    key = np.round(w, 9); freqs = np.unique(key)
    Mx = (key[None, :] == freqs[:, None]).astype(float)
    Sig2 = Mx @ Sig @ Mx.T; nb2 = Mx @ nb
    s2 = np.sqrt(nb2)
    return nb2, Sig2 / s2[:, None] / s2[None, :], freqs


def parity_bound(Vamp, w, ch):
    key = {(int(c), round(x, 9)): i for i, (x, c) in enumerate(zip(w, ch))}
    P = np.zeros((len(w), len(w)))
    for i, (x, c) in enumerate(zip(w, ch)):
        j = key.get((int(c), round(-x, 9)))
        P[i, j if j is not None else i] = 1.0
    comm = float(np.abs(P @ Vamp - Vamp @ P).max())
    ev, U = np.linalg.eigh(P)
    lo = np.linalg.eigvalsh(U[:, ev < 0].T @ Vamp @ U[:, ev < 0])[0]
    le = np.linalg.eigvalsh(U[:, ev > 0].T @ Vamp @ U[:, ev > 0])[0]
    return float(lo), float(le), float((lo + le) / 2 if lo <= le else le), comm


def dither(d, order):
    T = np.zeros_like(d); e = 0.0
    for i in order:
        e += d[i]
        if e >= 0.5:
            T[i] = 1.0; e -= 1.0
    return T


def binary_relax(nb, Vamp, w, rng, ch=None):
    s = np.sqrt(nb); Sig = s[:, None] * Vamp * s[None, :]; Mq = Sig - np.diag(nb)
    def J(d):
        den = nb @ d; q = d @ Mq @ d
        return 1 + q / den, (2 * (Mq @ d) * den - q * nb) / den**2
    order = np.lexsort((w, ch)) if ch is not None else np.argsort(w)
    wm = np.abs(w[nb > 1e-3 * nb.max()]).max()
    starts = [np.full(len(nb), 0.5), (w > 0).astype(float), (w < 0).astype(float)]
    starts += [np.where(w > 0, np.clip(w / (a * wm), 0, 1), 0.0) for a in (0.5, 1.0, 2.0)]
    if ch is not None:
        starts += [((w > 0) & (ch == c)).astype(float) for c in (0, 1)]
    best = None
    for d0 in starts:
        r = minimize(J, d0, jac=True, method="L-BFGS-B", bounds=[(0, 1)] * len(nb), options={"maxiter": 3000})
        T = dither(r.x, order)
        F1, T1 = best_improvement(T, Sig, nb)
        F2, T2 = tabu_search(T1, Sig, nb, rng)
        F2 = fano_of(T2, nb, Vamp)
        if best is None or F2 < best:
            best = F2
    return float(best)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "birefringence.json"
    Phi = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    theta = float(sys.argv[3]) if len(sys.argv) > 3 else 45.0
    blist = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [0, 0.1, 0.3, 0.667, 1, 2, 3, 10, 30, 100]
    cx = np.cos(np.deg2rad(theta)) ** 2
    dt = 0.04; t = np.arange(-7, 7, dt); p = gaussian_p(t)
    rng = np.random.default_rng(3)
    rows = []
    for b in blist:
        t0 = time.time()
        nz = int(max(400, 60 * b * Phi / (2 * np.pi), 40 * Phi))
        Ax, Ay, M = propagate(p, Phi, b, cx, nz)
        V = np.einsum("tij,tkj->tik", M, M)
        lmin_t = np.linalg.eigvalsh(V)[:, 0]
        symp = None
        nb, Va, w, ch = bins(Ax, Ay, M, dt, pad=4)
        lg_res = float(np.linalg.eigvalsh(Va)[0])
        nbi, Vai, wi = insensitive(nb, Va, w)
        lg_ins = float(np.linalg.eigvalsh(Vai)[0])
        # momentum bound (total over channels)
        w2in = float((w**2 * 0).sum())
        tt = t
        def w2(A):
            F = np.fft.fft(A); ww = 2 * np.pi * fftfreq(len(A), dt)
            return (ww**2 * np.abs(F) ** 2).sum(), (np.abs(F) ** 2).sum()
        a1, n1 = w2(np.sqrt(p * cx).astype(complex)); a2, n2 = w2(np.sqrt(p * (1 - cx)).astype(complex))
        b1, m1 = w2(Ax); b2, m2 = w2(Ay)
        lamP = ((a1 + a2) / (n1 + n2)) / ((b1 + b2) / (m1 + m2))
        lo, le, fpar, comm = parity_bound(Va, w, ch)
        loi, lei, fpari, commi = parity_bound(Vai, wi, np.zeros(len(wi)))
        Fb_res = binary_relax(nb, Va, w, rng, ch)
        Fb_ins = binary_relax(nbi, Vai, wi, rng)
        S0 = np.abs(Ax) ** 2 + np.abs(Ay) ** 2
        S1 = (np.abs(Ax) ** 2 - np.abs(Ay) ** 2) / S0; S3 = 2 * np.imag(np.conj(Ax) * Ay) / S0
        k0 = np.argmin(np.abs(t))
        row = {"Phi": Phi, "theta_deg": theta, "b_dbeta_over_gammaP0": b, "L_B_over_L_NL": (2 * np.pi / b if b > 0 else None),
               "nz": nz, "lam_min": float(lmin_t.min()), "t_at_lam_min": float(t[np.argmin(lmin_t)]),
               "Vmin_isotropic_linear": float(vmin_kerr(Phi)), "Vmin_strong_biref": float(vmin_kerr((Phi / 2) * (1 + np.sqrt(1 - (20 / 9) * cx * (1 - cx))))),
               "lam_gen_resolved": lg_res, "lam_gen_insensitive": lg_ins, "lam_P_total": float(lamP),
               "parity_bound_resolved": fpar, "parity_comm": comm, "parity_bound_insensitive": fpari,
               "binary_resolved": Fb_res, "binary_insensitive": Fb_ins,
               "peak_S1": float(S1[k0]), "peak_S3": float(S3[k0]), "power_conservation_err": float(np.abs(S0 - p).max()),
               "wall_s": round(time.time() - t0, 1)}
        rows.append(row)
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
        json.dump({"rows": rows}, open(out, "w"), indent=1)
