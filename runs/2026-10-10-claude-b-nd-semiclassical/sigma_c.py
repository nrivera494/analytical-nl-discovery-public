"""Reduced semiclassical evaluation of lambda_min(V) (claude-b, T-20261010-claude-interactive-05).

Claim structure: in quadratures relative to the local mean phase, X (amplitude) and Ytilde = Y / N (phase scaled by
epsilon = 1/N), the linearized map is epsilon-independent at leading order (dispersionless hydrodynamics). With the
symplectic block identity this gives lambda_min(V) = 1 / (N^2 sigma_max(C)^2) + O(N^-3), where C maps the input
amplitude quadrature X0 to the output scaled phase quadrature Ytilde.

Here C is computed on the span of the first M Hermite functions (orthonormal in L^2) by central differences of the
full NLSE at a given N, so 2M propagations instead of 4 Nt. Output columns are the scaled phase quadrature
Ytilde(tau) = Im(du e^{-i arg u}) / N sampled with sqrt(dtau) weights; sigma_max is the top singular value.
Usage: python sigma_c.py  -> summary.json (Lambda_red = 1 / sigma_max^2 against N and Z; small-Z analytic form).
"""
import json, os, time
import numpy as np
from numpy.polynomial.hermite import hermval

fft, ifft = np.fft.fft, np.fft.ifft
HERE = os.path.dirname(os.path.abspath(__file__))


def hermite_functions(t, M):
    """Orthonormal Hermite functions by the stable three-term recurrence."""
    out = np.zeros((M, len(t)))
    out[0] = np.pi ** -0.25 * np.exp(-t ** 2 / 2)
    if M > 1:
        out[1] = np.sqrt(2) * t * out[0]
    for n in range(1, M - 1):
        out[n + 1] = np.sqrt(2 / (n + 1)) * t * out[n] - np.sqrt(n / (n + 1)) * out[n - 1]
    return out


def propagate(u, w, xi, dxi, N2):
    L = np.exp(0.5j * w ** 2 * dxi / 2)
    for _ in range(int(round(xi / dxi))):
        u = ifft(L * fft(u, axis=-1), axis=-1)
        u = u * np.exp(1j * N2 * np.abs(u) ** 2 * dxi)
        u = ifft(L * fft(u, axis=-1), axis=-1)
    return u


def sigma_max(N, Z, M=40, Nt=2048, TW=40.0, phi_step=0.02, eta=1e-6):
    t = (np.arange(Nt) - Nt // 2) * (TW / Nt)
    dt = t[1] - t[0]
    w = 2 * np.pi * np.fft.fftfreq(Nt, d=dt)
    N2 = N ** 2
    xi = Z / N
    n = max(1, int(round(xi / (phi_step / N2))))
    dxi = xi / n
    u0 = np.exp(-t ** 2 / 2) + 0j
    H = hermite_functions(t, M)
    batch = np.concatenate([u0[None] + eta * H, u0[None] - eta * H])
    out = propagate(batch, w, xi, dxi, N2)
    du = (out[:M] - out[M:]) / (2 * eta)
    ub = propagate(u0[None], w, xi, dxi, N2)[0]
    ph = np.exp(-1j * np.angle(ub))
    Yt = (du * ph).imag / N * np.sqrt(dt)          # (M, Nt): scaled phase quadrature of each response
    Xo = (du * ph).real * np.sqrt(dt)
    s = np.linalg.svd(Yt.T, compute_uv=False)
    return float(s[0]), float(np.linalg.svd(Xo.T, compute_uv=False)[0])


if __name__ == "__main__":
    out = {"rows": []}
    for Z in (0.1, 0.2, 0.318, 0.5, 0.742, 1.06, 1.59):
        for N in (20, 50, 100):
            t0 = time.time()
            Nt = 2048 if N <= 50 else 4096
            sm, ax = sigma_max(N, Z, Nt=Nt)
            row = dict(Z=Z, N=N, Nt=Nt, sigma_max_C=sm, Lambda_red=1 / sm ** 2, sigma_max_A=ax,
                       small_Z_form=(1 / (4 * Z ** 2)) / (1 - Z / np.sqrt(6)) ** 2, dispersionless=1 / (4 * Z ** 2),
                       wall=time.time() - t0)
            out["rows"].append(row)
            print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
