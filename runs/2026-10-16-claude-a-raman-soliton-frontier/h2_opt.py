#!/usr/bin/env python3
"""H2 (frozen in HYPOTHESES.md, commit 3af8dfa): maximize the leading ZS eigenvalue eta_max over spectral masks of a
fixed laser spectrum |Q|. Classes: S_phi (phase-only, Legendre basis orders 2..M on the spectral support) and S_Aphi
(phase plus amplitude a = sigmoid(d0 + sum d_m P_m) in (0,1)). Analytic gradient from left/right eigenvectors
(zs.grad_zeta_q), L-BFGS-B, multi-start. Usage: python h2_opt.py out.json [laser] [amplitudes] [M] [starts]"""
import json, sys, time
import numpy as np
from numpy.polynomial import legendre
from scipy.optimize import minimize
from zs import Grid, leading_fast as leading, grad_zeta_q

out = sys.argv[1] if len(sys.argv) > 1 else "h2_opt.json"
laser = sys.argv[2] if len(sys.argv) > 2 else "sech"
amps = [float(a) for a in sys.argv[3].split(",")] if len(sys.argv) > 3 else [1.5, 2.0, 3.0, 4.0, 6.0]
M = int(sys.argv[4]) if len(sys.argv) > 4 else 12
nstarts = int(sys.argv[5]) if len(sys.argv) > 5 else 4
rng = np.random.default_rng(7)


class Problem:
    def __init__(self, laser, A, n, width, M):
        self.g = Grid(n, width)
        t = self.g.t
        if laser in ("sech", "gauss"):
            qtl = (A / np.cosh(t) if laser == "sech" else A * np.exp(-t**2 / 2)).astype(complex)
        else:   # spectrally defined lasers with flat spectral phase (TL), scaled to peak amplitude A
            k = self.g.k
            S0 = (1 / np.cosh(np.pi * k / 2)) * (1 + 0.5 * np.tanh(k)) if laser == "asym" else np.exp(-(k / 1.5) ** 8)
            qtl = np.fft.fftshift(np.fft.ifft(S0))     # S0 is in FFT order (Grid.k = 2 pi fftfreq)
            qtl = qtl * np.exp(-1j * np.angle(qtl[np.argmax(np.abs(qtl))]))
            qtl = A * qtl / np.abs(qtl).max()
        self.qtl = qtl.astype(complex)
        self.Q = np.fft.fft(np.fft.ifftshift(self.qtl))
        absQ = np.abs(self.Q)
        sup = np.abs(self.g.k[absQ > 1e-4 * absQ.max()]).max()
        self.x = np.clip(self.g.k / sup, -1, 1)
        self.P = np.array([legendre.legval(self.x, np.eye(M + 1)[m]) for m in range(M + 1)])   # (M+1, n)
        self.M = M
        self.A = A
        self.last = None

    def field(self, c, d=None):
        phi = c @ self.P[2:]
        a = np.ones(self.g.n) if d is None else 1 / (1 + np.exp(-(d[0] + d[1:] @ self.P[1:])))
        S = a * np.exp(1j * phi) * self.Q
        return np.fft.fftshift(np.fft.ifft(S)), S, a, phi

    def eval(self, c, d=None):
        q, S, a, phi = self.field(c, d)
        sigma = 1j * (np.abs(q).max() + 0.3)
        z, v, w = leading(self.g, q, sigma=sigma, k=3)
        al, be = grad_zeta_q(self.g, z, v, w)
        al_s, be_s = np.fft.ifftshift(al), np.fft.ifftshift(be)
        IA, FB = np.fft.ifft(al_s), np.fft.fft(be_s) / self.g.n
        dz_dphi = 1j * S * IA - 1j * np.conj(S) * FB
        gc = (self.P[2:] @ np.imag(dz_dphi))
        gd = None
        if d is not None:
            E = S / np.maximum(a, 1e-300)                      # e^{i phi} Q
            dz_da = E * IA + np.conj(E) * FB
            ga = np.imag(dz_da) * a * (1 - a)
            gd = np.concatenate([[ga.sum()], self.P[1:] @ ga])
        self.last = (z, np.abs(q).max())
        return z, gc, gd


def run(laser, A, M, nstarts):
    n = 512 if A <= 3 else (768 if A <= 4 else 1024)
    width = 30.0 if laser in ("sech", "asym") else (26.0 if laser == "gauss" else 60.0)
    if laser == "flattop":
        n = 768 if A <= 3 else 1024
    pb = Problem(laser, A, n, width, M)
    z0, _, _ = pb.eval(np.zeros(M - 1))
    rows = []
    for cls in ("phi", "Aphi"):
        best = None
        for s in range(nstarts):
            scale = [0.0, 0.5, 1.0, 2.0, 3.0, 0.25][s % 6]
            c0 = rng.normal(0, scale, M - 1) / (1 + np.arange(M - 1))
            if cls == "phi":
                x0 = c0
                def f(x):
                    z, gc, _ = pb.eval(x)
                    return -z.imag, -gc
            else:
                d0 = np.concatenate([[6.0], rng.normal(0, scale, M)])
                x0 = np.concatenate([c0, d0])
                def f(x):
                    z, gc, gd = pb.eval(x[:M - 1], x[M - 1:])
                    return -z.imag, -np.concatenate([gc, gd])
            t0 = time.time()
            try:
                r = minimize(f, x0, jac=True, method="L-BFGS-B", options={"maxiter": 80})
                eta = -r.fun
            except Exception as e:
                eta = np.nan
            row = {"laser": laser, "A": A, "class": cls, "start": s, "scale": scale, "eta_TL": float(z0.imag),
                   "eta_opt": float(eta), "ratio_to_TL": float(eta / z0.imag), "q_inf_final": float(pb.last[1]),
                   "bound_2N_over_2N1": None, "nit": int(r.nit) if np.isfinite(eta) else None, "wall_s": round(time.time() - t0, 1)}
            rows.append(row)
            print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
    return rows


if __name__ == "__main__":
    allrows = []
    for A in amps:
        allrows += run(laser, A, M, nstarts)
        json.dump({"rows": allrows}, open(out, "w"), indent=1)
