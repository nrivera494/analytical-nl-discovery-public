"""Solver validation and closed-form checks for C-20261018-pi-chatgpt-01 (claude-interactive.9, 2026-10-18).

1. TL eigenvalues of q = N sech t (integer and non-integer N) against Satsuma-Yajima N - 1/2: FC at two resolutions,
   BO with Romberg extrapolation over three cell widths; measured convergence exponent of BO.
2. TL leading-soliton fractions of q = N exp(-t^2/2) (the source's Gaussian table, and held-out N).
3. Sharpness of (A): the extremiser q_* = p eta/(p-1) sech(2 eta t/(p-1)) has leading eigenvalue i eta and
   int |q_*|^p = C_p eta^(p-1)  (p = 1.5, 2, 3, 7).
4. Limits of C_p: p = 2, p -> 1 (pi/2), p -> infinity (C_p^(1/(p-1)) -> 1).
5. (A) on random complex potentials: every computed eigenvalue against C_p eta^(p-1), p in {1.2, 1.5, 2, 3, 4, 7, 12}.
6. Closed forms (C), (D), (E), (F) recomputed independently, with direct quadrature, and the held-out ceilings.
"""
import json, sys, time
import numpy as np
from scipy.special import gammaln
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
sys.path.insert(0, '.')
from zs import grid, fc_eigs, bo_refine, logC

out = {}
t_start = time.time()


def bo_romberg(qfun, tL, tR, h0, z0):
    zs = []
    for j in range(3):
        h = h0 / 2 ** j
        n = int(round((tR - tL) / h))
        tm = tL + (np.arange(n) + 0.5) * h
        z, res, it = bo_refine(qfun(tm) + 0j, h, z0)
        zs.append(z)
        z0 = z
    r1 = [(4 * zs[1] - zs[0]) / 3, (4 * zs[2] - zs[1]) / 3]
    r2 = (16 * r1[1] - r1[0]) / 15
    # convergence exponent of the raw 2nd-order scheme from three widths
    e1, e2 = abs(zs[0] - zs[1]), abs(zs[1] - zs[2])
    order = np.log2(e1 / e2) if e2 > 0 else np.nan
    return zs, r2, order


def leading_true(w, kmax, frac=0.6):
    """Discard FC eigenvalues near the Nyquist edge (spurious), keep the rest sorted by Im."""
    keep = [z for z in w if abs(z.real) < frac * kmax]
    return np.array(keep)


# ---------------------------------------------------------------- 1. sech TL
rows = []
for N in [1, 2, 3, 4, 5, 6, 8, 2.5, 3.5, 4.5, 5.5, 7.5, 9.5]:
    q = lambda t: N / np.cosh(t)
    res = {"N": N, "exact_eta": N - 0.5}
    fcv = []
    for n, T in ((512, 64.0), (768, 96.0)):
        t, k = grid(n, T)
        w = leading_true(fc_eigs(q(t) + 0j, T, imag_min=0.2), np.pi * n / T)
        fcv.append(w[0])
    res["fc_eta_512_T64"] = fcv[0].imag
    res["fc_eta_768_T96"] = fcv[1].imag
    res["fc_all_eigs_768"] = [float(z.imag) for z in w if z.imag > 0.2]
    zs, zr, order = bo_romberg(q, -46.0, 46.0, 0.02, fcv[1])
    res["bo_eta_h"] = [z.imag for z in zs]
    res["bo_romberg_eta"] = zr.imag
    res["bo_order"] = order
    res["err_fc"] = abs(fcv[1].imag - (N - 0.5))
    res["err_bo"] = abs(zr.imag - (N - 0.5))
    res["max_abs_re_zeta"] = float(max(abs(fcv[1].real), abs(zr.real)))
    rows.append(res)
    print("sech N=%-4s FC %.14f %.14f  BO-R %.14f  order %.3f" % (N, fcv[0].imag, fcv[1].imag, zr.imag, order), flush=True)
out["sech_TL"] = rows

# ---------------------------------------------------------------- 2. Gaussian TL
rows = []
src = {2: None, 3: None, 4: 0.4912507580, 5: None, 6: None, 10: None}
for N in [1.5, 2, 3, 4, 5, 6, 8, 10]:
    q = lambda t: N * np.exp(-t ** 2 / 2)
    M0 = N ** 2 * np.sqrt(np.pi)
    fcv = []
    for n, T in ((256, 40.0), (512, 60.0)):
        t, k = grid(n, T)
        w = leading_true(fc_eigs(q(t) + 0j, T, imag_min=0.05), np.pi * n / T)
        fcv.append(w[0])
    zs, zr, order = bo_romberg(q, -14.0, 14.0, 0.01, fcv[1])
    res = {"N": N, "fc_eta_256_T40": fcv[0].imag, "fc_eta_512_T60": fcv[1].imag, "bo_romberg_eta": zr.imag,
           "bo_order": order, "f1_TL_fc": 4 * fcv[1].imag / M0, "f1_TL_bo": 4 * zr.imag / M0,
           "fc_bo_diff": abs(fcv[1].imag - zr.imag), "source_f1": src.get(N)}
    rows.append(res)
    print("gauss N=%-4s f1 FC %.12f  BO %.12f  diff %.1e order %.3f" % (N, res['f1_TL_fc'], res['f1_TL_bo'], res['fc_bo_diff'], order), flush=True)
out["gauss_TL"] = rows

# ---------------------------------------------------------------- 3. sharpness of (A)
rows = []
for p in (1.5, 2.0, 3.0, 7.0):
    for eta in (1.0, 2.3):
        A, w_ = p * eta / (p - 1), (p - 1) / (2 * eta)
        q = lambda t: A / np.cosh(t / w_)
        L = 40 * w_ + 10
        n = 1024
        T = 2 * L
        t, k = grid(n, T)
        wv = leading_true(fc_eigs(q(t) + 0j, T, imag_min=0.05 * eta), np.pi * n / T)
        zs, zr, order = bo_romberg(q, -L, L, w_ / 50, wv[0])
        Ip = quad(lambda s: q(s) ** p, -L, L, limit=400, epsabs=0, epsrel=1e-13)[0]
        Cp = np.exp(logC(p))
        rows.append({"p": p, "eta_target": eta, "fc_eta": wv[0].imag, "bo_eta": zr.imag,
                     "int_qp": Ip, "Cp_eta_pm1": Cp * eta ** (p - 1), "ratio": Ip / (Cp * zr.imag ** (p - 1))})
        print("q_* p=%.1f eta=%.1f: eta FC %.13f BO %.13f  int|q|^p / (C_p eta^(p-1)) = %.13f" % (p, eta, wv[0].imag, zr.imag, rows[-1]['ratio']), flush=True)
out["sharpness_A"] = rows

# ---------------------------------------------------------------- 4. limits of C_p
lim = {"C_2": float(np.exp(logC(2.0))),
       "C_p_near_1": {str(p): float(np.exp(logC(p))) for p in (1.1, 1.01, 1.001, 1.0001)},
       "pi_over_2": np.pi / 2,
       "C_p_pow_1_over_pm1_large_p": {str(p): float(np.exp(logC(p) / (p - 1))) for p in (10, 100, 1000, 1e4, 1e5)}}
out["limits_Cp"] = lim
print("limits", json.dumps(lim), flush=True)

# ---------------------------------------------------------------- 5. (A) on random complex potentials
rng = np.random.default_rng(20261018)
ps = [1.2, 1.5, 2.0, 3.0, 4.0, 7.0, 12.0]
n, T = 512, 64.0
t, k = grid(n, T)
dt = T / n
worst = {str(p): np.inf for p in ps}
count = 0
for trial in range(60):
    # random smooth complex pulse: sum of a few complex Gaussian/sech lobes with random chirps and carriers
    q = np.zeros(n, complex)
    for j in range(rng.integers(1, 5)):
        a = rng.uniform(0.5, 4.0); w = rng.uniform(0.4, 2.5); c = rng.uniform(-6, 6); C = rng.uniform(-2, 2)
        nu = rng.uniform(-3, 3); ph = rng.uniform(0, 2 * np.pi)
        shape = np.exp(-((t - c) / w) ** 2 / 2) if rng.random() < 0.5 else 1 / np.cosh((t - c) / w)
        q += a * shape * np.exp(1j * (C * ((t - c) / w) ** 2 + nu * t + ph))
    w_all = leading_true(fc_eigs(q, T, imag_min=0.02), np.pi * n / T)
    for z in w_all:
        # confirm with BO on the same samples (line problem) to discard spurious FC eigenvalues
        zb, ares, it = bo_refine(q, dt, z)
        if abs(zb - z) > 1e-3 * max(1, abs(z)) or zb.imag <= 0.02:
            continue
        count += 1
        for p in ps:
            Ip = np.sum(np.abs(q) ** p) * dt
            worst[str(p)] = min(worst[str(p)], Ip / (np.exp(logC(p)) * zb.imag ** (p - 1)))
out["random_potentials_A"] = {"trials": 60, "eigenvalues_tested": count, "min_ratio_int_qp_over_Cp_eta_pm1": worst,
                              "note": "ratio >= 1 is the inequality (A); eigenvalues confirmed by BO on the same samples (2nd order, h = %.3f)" % dt}
print("random (A):", count, worst, flush=True)

# ---------------------------------------------------------------- 6. closed forms (C), (D), (E), (F)
def U_sech(N, n):          # [int |N sech|^(2n) / C_2n]^(1/(2n-1)), from the definition with gamma functions
    p = 2 * n
    logI = p * np.log(N) + 0.5 * np.log(np.pi) + gammaln(p / 2) - gammaln((p + 1) / 2)
    return np.exp((logI - logC(p)) / (p - 1))


def U_sech_quad(N, n):     # the same with direct quadrature of int sech^(2n)
    p = 2 * n
    I = quad(lambda s: (N / np.cosh(s)) ** p, -60, 60, limit=400, epsrel=1e-14)[0]
    return (I / np.exp(logC(p))) ** (1 / (p - 1))


C_rows = [{"N": N, "U_2N": U_sech(N, N), "U_2N_quad": U_sech_quad(N, N), "minus_TL": U_sech(N, N) - (N - 0.5),
           "f1_opt": 4 * (N - 0.5) / (2 * N ** 2), "(2N-1)/N^2": (2 * N - 1) / N ** 2} for N in range(1, 11)]
out["C_closed_form"] = C_rows
D_rows = []
for N in (2.5, 3.5, 4.5, 5.5, 7.5, 9.5):
    vals = [(U_sech(N, n), n) for n in range(1, 80)]
    best, bn = min(vals)
    D_rows.append({"N": N, "best_n": bn, "U_best": best, "U_best_quad": U_sech_quad(N, bn),
                   "ceiling_percent": 100 * (best / (N - 0.5) - 1)})
    print("(D) N=%.1f best n=%d ceiling %.5f %%" % (N, bn, D_rows[-1]['ceiling_percent']), flush=True)
out["D_ceilings"] = D_rows

E_rows = []
for N in (1.5, 2, 3, 4, 5, 6, 8, 10):
    f = lambda p: (p * np.log(N) + 0.5 * np.log(2 * np.pi / p) - logC(p)) / (p - 1)
    ps_ = np.linspace(2.0, 60.0, 5801)
    j = int(np.argmin([f(p) for p in ps_]))
    r = minimize_scalar(f, bracket=(ps_[max(j - 1, 0)] + 1e-9, ps_[j], ps_[j + 1]), tol=1e-14)
    U = float(np.exp(r.fun))
    # direct quadrature of int |q|^p at the optimal p, as an independent check of the closed form
    Iq = quad(lambda s: (N * np.exp(-s * s / 2)) ** r.x, -40, 40, limit=400, epsrel=1e-14)[0]
    Uq = (Iq / np.exp(logC(r.x))) ** (1 / (r.x - 1))
    E_rows.append({"N": N, "p_opt": float(r.x), "U_G": U, "U_G_quad": Uq, "f1_ceiling_percent": 100 * 4 * U / (np.sqrt(np.pi) * N ** 2)})
    print("(E) N=%.1f p*=%.4f ceiling f1 %.5f %%" % (N, r.x, E_rows[-1]['f1_ceiling_percent']), flush=True)
out["E_ceilings"] = E_rows

# (F): check the closed-form constant against the Hausdorff-Young chain, and that it bounds the TL eta
def F_bound(S_vals, dk, p):
    pp = p / (p - 1)
    return np.sqrt(pp) / (2 * np.pi) * np.exp(-(0.5 * np.log(p) + logC(p)) / (p - 1)) * np.sum(S_vals ** pp) * dk
F_rows = []
kk = np.linspace(-80, 80, 160001); dk = kk[1] - kk[0]
for name, S, eta_TL in (("sech N=3", 3 * np.pi / np.cosh(np.pi * kk / 2), 2.5),
                        ("gauss N=4", 4 * np.sqrt(2 * np.pi) * np.exp(-kk ** 2 / 2), out["gauss_TL"][3]["bo_romberg_eta"])):
    for p in (2.0, 3.0, 6.0, 8.0, 20.0, 200.0):
        F_rows.append({"source": name, "p": p, "F_bound": float(F_bound(S, dk, p)), "eta_TL": float(eta_TL)})
# Gaussian equality in Hausdorff-Young: for S Gaussian, (F) at p equals the (E) value at the same p
N = 4
for p in (3.0, 7.521190433344544):
    S = N * np.sqrt(2 * np.pi) * np.exp(-kk ** 2 / 2)
    lhsF = F_bound(S, dk, p)
    E_at_p = np.exp((p * np.log(N) + 0.5 * np.log(2 * np.pi / p) - logC(p)) / (p - 1))
    F_rows.append({"source": "gauss N=4, F vs E at same p", "p": p, "F_bound": float(lhsF), "E_bound": float(E_at_p),
                   "rel_diff": float(lhsF / E_at_p - 1)})
out["F_checks"] = F_rows
for r in F_rows:
    print("(F)", r, flush=True)

out["wall_time_s"] = time.time() - t_start
json.dump(out, open('summary.json', 'w'), indent=1, default=float)
print("done in %.1f s" % out["wall_time_s"])
