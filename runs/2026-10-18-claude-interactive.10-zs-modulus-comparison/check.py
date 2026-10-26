"""Sanity check for a remark in the novelty audit of C-20261018-pi-chatgpt-01.

Question (not a claim): for a complex decaying potential q, is every ZS eigenvalue's
imaginary part at most the largest imaginary part of the ZS eigenvalues of |q|?
If so, the complex case of the claim's part (A) would follow from the real nonnegative
case published by Dolbeault-Gontier-Pizzichillo-Van Den Bosch (2024).

ZS: v' = [[-i z, q], [-conj(q), i z]] v, i.e. L v = z v with
L = [[i d/dt, -i q], [-i conj(q), -i d/dt]].
Fourier collocation on a periodic window, two grids per potential.
Writes summary.json next to this file.
"""
import json
import os

import numpy as np

L_WIN = 40.0
GRIDS = (384, 576)
IM_MIN = 0.02          # ignore eigenvalues closer than this to the real axis
MATCH_TOL = 1e-3       # two-grid agreement required (kinks in |q| converge only algebraically)


def zs_eigs(qfun, n):
    t = (np.arange(n) - n // 2) * (L_WIN / n)
    q = qfun(t)
    k = 2 * np.pi * np.fft.fftfreq(n, d=L_WIN / n)
    eye = np.eye(n)
    D = np.fft.ifft(1j * k[:, None] * np.fft.fft(eye, axis=0), axis=0)
    M = np.block([[1j * D, -1j * np.diag(q)], [-1j * np.diag(np.conj(q)), -1j * D]])
    ev = np.linalg.eigvals(M)
    return ev[ev.imag > IM_MIN]


def converged_eigs(qfun):
    a, b = (zs_eigs(qfun, n) for n in GRIDS)
    out, err = [], 0.0
    for z in a:
        if len(b) == 0:
            continue
        d = np.min(np.abs(b - z))
        if d < MATCH_TOL:
            out.append(z)
            err = max(err, d)
    return np.array(out), err, len(a), len(b)


def eta_max(qfun):
    z, err, na, nb = converged_eigs(qfun)
    if len(z) == 0:
        return 0.0, err, na, nb, z, None
    i = int(np.argmax(z.imag))
    return float(z[i].imag), err, na, nb, z, float(z[i].real)


rng = np.random.default_rng(20261018)
sech = lambda t: 1.0 / np.cosh(t)
cases = []

# 1. validation: Satsuma-Yajima, eta_max = A - 1/2
for A in (1.3, 2.0, 2.7):
    cases.append(("sech A=%g" % A, lambda t, A=A: A * sech(t), A - 0.5))

# 2. chirped sech, |q| = A sech
for A in (1.5, 2.5):
    for C in (0.1, 0.3, 0.5):
        cases.append(("A sech exp(i C t^2), A=%g C=%g" % (A, C),
                      lambda t, A=A, C=C: A * sech(t) * np.exp(1j * C * t**2), None))
# 3. other phase modulations, |q| = A sech
for A in (1.5, 2.5):
    for B in (0.5, 1.5, 3.0):
        cases.append(("A sech exp(i B tanh t), A=%g B=%g" % (A, B),
                      lambda t, A=A, B=B: A * sech(t) * np.exp(1j * B * np.tanh(t)), None))
        cases.append(("A sech exp(i B sech t), A=%g B=%g" % (A, B),
                      lambda t, A=A, B=B: A * sech(t) * np.exp(1j * B * sech(t)), None))
# 4. two humps with a relative phase
for phi in (0.0, np.pi / 2, 2.0, np.pi):
    for d in (1.0, 2.5):
        cases.append(("two sech humps a=1.2,b=0.9,d=%g,phi=%.3f" % (d, phi),
                      lambda t, d=d, phi=phi: 1.2 * sech(t - d) + 0.9 * np.exp(1j * phi) * sech(t + d), None))
# 4b. real sign-changing potentials (|q| has kinks at the zeros of q)
for A in (1.5, 2.5):
    cases.append(("odd A sech t tanh t, A=%g" % A, lambda t, A=A: A * 2.0 * sech(t) * np.tanh(t), None))
for d in (0.5, 1.5):
    cases.append(("sech(t-d) - 0.6 sech(t+d), d=%g" % d, lambda t, d=d: 1.5 * sech(t - d) - 0.9 * sech(t + d), None))
# 5. passive masks on a sech spectrum (q_m = F^{-1}(m S)), random smooth phase and amplitude
for j in range(12):
    N_ord = (2.0, 3.0, 2.5)[j % 3]
    c = rng.normal(size=6) * 1.5
    a = rng.normal(size=4) * 0.8
    def qm(t, c=c, a=a, N_ord=N_ord):
        n = len(t)
        dt = t[1] - t[0]
        w = 2 * np.pi * np.fft.fftfreq(n, d=dt)
        x = np.clip(w / 6.0, -1, 1)
        phase = sum(cj * np.polynomial.legendre.Legendre.basis(m + 2)(x) for m, cj in enumerate(c))
        amp = 1.0 / (1.0 + np.exp(-(1.5 + sum(aj * np.polynomial.legendre.Legendre.basis(m + 1)(x) for m, aj in enumerate(a)))))
        q0 = N_ord * sech(t)
        Q0 = np.fft.fft(np.fft.ifftshift(q0))
        return np.fft.fftshift(np.fft.ifft(Q0 * amp * np.exp(1j * phase)))
    cases.append(("passive mask on %g sech, draw %d" % (N_ord, j), qm, None))
# 6. random complex Gaussian sums
for j in range(10):
    amps = rng.normal(size=3) * 1.2 + 1j * rng.normal(size=3) * 1.2
    cent = rng.uniform(-3, 3, size=3)
    wid = rng.uniform(0.6, 1.6, size=3)
    cases.append(("random complex Gaussian sum %d" % j,
                  lambda t, amps=amps, cent=cent, wid=wid:
                  sum(A * np.exp(-((t - c0) / w0) ** 2 / 2) for A, c0, w0 in zip(amps, cent, wid)), None))

rows = []
worst = -np.inf
for name, qf, exact in cases:
    eq, errq, naq, nbq, zq, req = eta_max(qf)
    absf = (lambda t, qf=qf: np.abs(qf(t)))
    ea, erra, naa, nba, za, rea = eta_max(absf)
    gap = eq - ea
    worst = max(worst, gap)
    rows.append({
        "case": name,
        "eta_max_q": eq, "eta_max_abs_q": ea, "eta_q_minus_eta_absq": gap,
        "two_grid_err_q": errq, "two_grid_err_absq": erra,
        "n_eigs_q": int(len(zq)), "n_eigs_absq": int(len(za)),
        "re_zeta_at_eta_max_q": req, "re_zeta_at_eta_max_absq": rea,
        "exact_if_known": exact,
    })
    print("%-55s eta(q)=%.8f eta(|q|)=%.8f diff=%+.2e err=%.1e/%.1e" % (name, eq, ea, gap, errq, erra))

val = [r for r in rows if r["exact_if_known"] is not None]
out = {
    "grids": GRIDS, "window": L_WIN, "im_min": IM_MIN, "match_tol": MATCH_TOL,
    "validation_max_abs_error_vs_satsuma_yajima": max(abs(r["eta_max_q"] - r["exact_if_known"]) for r in val),
    "n_cases": len(rows),
    "max_eta_q_minus_eta_absq": worst,
    "n_cases_with_eta_q_above_eta_absq_by_more_than_1e-6": sum(r["eta_q_minus_eta_absq"] > 1e-6 for r in rows),
    "max_abs_re_zeta_at_eta_max_absq": max(abs(r["re_zeta_at_eta_max_absq"]) for r in rows if r["re_zeta_at_eta_max_absq"] is not None),
    "max_two_grid_err_absq": max(r["two_grid_err_absq"] for r in rows),
    "max_two_grid_err_q": max(r["two_grid_err_q"] for r in rows),
    "min_strict_margin": min(-r["eta_q_minus_eta_absq"] for r in rows if r["eta_q_minus_eta_absq"] < 0),
    "rows": rows,
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "summary.json"), "w") as f:
    json.dump(out, f, indent=1)
print("worst eta(q)-eta(|q|):", worst)
