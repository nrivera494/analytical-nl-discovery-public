#!/usr/bin/env python3
"""Numeric checks and frozen predictions for the amplifier-similariton noise channel (T-20261008-claude-a-01).

Dimensionless units (input parabola: half-width T0, peak power P0; Z0 = sqrt(L_D L_NL)):
  x = T/T0, zeta = z/Z0, eps0 = sqrt(L_NL/L_D) = 1/N0soliton, Gam = g Z0, n0 = P0 T0/(hbar w0),
  photon number N0 = (4/3) n0, energy E(zeta) = (4/3) e^{Gam zeta}.
Background (dispersionless): a'' = 2 e^{Gam zeta}/a^2, a(0)=1, a'(0)=adot0;  theta' = e^{Gam zeta}/a.
Blocks (Legendre l, lam = l(l+1)), y = (p_l, q_l = n_l/eps0):  p' = (e^{Gam zeta}/a) q,  q' = -(lam/a^2) p.
Noise (Wigner/symmetric): input vacuum <dpsi dpsi*> = delta/(2 n0); ASE <f f*>_sym = Gam (n_sp - 1/2)/n0 delta delta.
Every variance is reported as I_in + (2 n_sp - 1) * I_ase, in units of 1/N0 (times the stated scale).
Usage: python numeric.py <outdir>
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from numpy.polynomial import legendre as npleg
from scipy.integrate import solve_ivp, quad
from scipy.special import lpmv

T0 = time.time()
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
CHK, PRED = {}, {}
LMAX = 4


def record(name, ok, detail):
    CHK[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# Legendre Gram data: B_lm = int (1-xi^2) P_l P_m, c_l = (2l+1)/2
xg, wg = npleg.leggauss(60)
P = np.array([npleg.legval(xg, [0] * l + [1]) for l in range(LMAX + 3)])
B = np.array([[np.sum(wg * (1 - xg**2) * P[l] * P[m]) for m in range(LMAX + 1)] for l in range(LMAX + 1)])
cfac = np.array([(2 * l + 1) / 2 for l in range(LMAX + 1)])


def solve_background(Gam, adot0, zL, npts=4001):
    """Background a(zeta), a'(zeta), theta(zeta) and fundamental matrices Phi_l(zeta) for l <= LMAX."""
    def rhs(zt, y):
        a, ad, th = y[0], y[1], y[2]
        out = [ad, 2 * math.exp(Gam * zt) / a**2, math.exp(Gam * zt) / a]
        for l in range(LMAX + 1):
            lam = l * (l + 1)
            F = y[3 + 4 * l: 7 + 4 * l].reshape(2, 2)
            A = np.array([[0.0, math.exp(Gam * zt) / a], [-lam / a**2, 0.0]])
            out.extend((A @ F).ravel())
        return out
    y0 = [1.0, adot0, 0.0] + [1.0, 0.0, 0.0, 1.0] * (LMAX + 1)
    zs = np.linspace(0, zL, npts)
    sol = solve_ivp(rhs, (0, zL), y0, t_eval=zs, rtol=1e-11, atol=1e-12, method="DOP853")
    a, ad, th = sol.y[0], sol.y[1], sol.y[2]
    Phi = [sol.y[3 + 4 * l: 7 + 4 * l].T.reshape(-1, 2, 2) for l in range(LMAX + 1)]
    return zs, a, ad, th, Phi


def simpson(y, x):
    return float(np.trapezoid(y, x)) if hasattr(np, "trapezoid") else float(np.trapz(y, x))


def collective(Gam, adot0, gL, npts=4001):
    """Exact-Ehrenfest collective-coordinate noise with the leading-order (rank-one, chirp) Wigner covariance."""
    zL = gL / Gam
    zs, a, ad, th, Phi = solve_background(Gam, adot0, zL, npts)
    aL, adL = a[-1], ad[-1]
    X = a + ad * (zL - zs)                       # extrapolated width
    h = X - ad * aL / adL                        # compressed-timing transfer (compressor D = eps0 aL/a'L)
    wts = Gam * np.exp(-Gam * zs)                # ASE weight per dzeta, times (2 n_sp - 1)
    out = {
        "a_L": aL, "adot_L": adL, "theta_L": th[-1], "G": math.exp(gL),
        # N0 Var(T_c) / sigma_xL^2   (sigma_xL^2 = a_L^2/5)
        "timing_rel_in": X[0] ** 2 / aL**2, "timing_rel_ase": simpson(wts * X**2, zs) / aL**2,
        # N0 Var(T_comp) / T0^2  (units T0^2; the factor 1/5 included)
        "comp_timing_in": h[0] ** 2 / 5, "comp_timing_ase": simpson(wts * h**2, zs) / 5,
        # N0 Var(Omega_c) / sigma_kL^2  (sigma_kL^2 = a'_L^2/(5 eps0^2)); input TL part dropped (O(eps0^2 ln))
        "freq_rel_in": ad[0] ** 2 / adL**2, "freq_rel_ase": simpson(wts * ad**2, zs) / adL**2,
        # N0 eps0 Cov(T_c, Omega_c), units T0 * (1/T0) * eps0
        "cov_in": X[0] * ad[0] / 5, "cov_ase": simpson(wts * X * ad, zs) / 5,
        "zs": zs, "a": a, "ad": ad, "th": th, "Phi": Phi, "zL": zL,
    }
    return out


def block_noise(bg, Gam):
    """Leading-order block covariance: sources only in q = n/eps0 (intensity), scaled by eps0^2 n0 -> report in N0 units.
    Returns Sigma_in[l][m] and Sigma_ase[l][m] (2x2 each) at zeta_L, in units of 1/(eps0^2 N0)."""
    zs, Phi, a = bg["zs"], bg["Phi"], bg["a"]
    zL = bg["zL"]
    n0_over_N0 = 3 / 4                      # 1/n0 = (4/3)/N0
    Minv = [np.linalg.inv(Phi[l]) for l in range(LMAX + 1)]
    ML = [Phi[l][-1] for l in range(LMAX + 1)]
    Sin = np.zeros((LMAX + 1, LMAX + 1, 2, 2))
    Sase = np.zeros((LMAX + 1, LMAX + 1, 2, 2))
    for l in range(LMAX + 1):
        for m in range(LMAX + 1):
            qq = cfac[l] * cfac[m] * B[l, m] / n0_over_N0      # <q_l q_m> per unit (1/(eps0^2 N0)) at input
            # input: M_l(L,0) [[0,0],[0,qq]] M_m(L,0)^T
            Sin[l, m] = ML[l] @ np.array([[0, 0], [0, qq]]) @ ML[m].T
            # ASE: int M_l(L,z) [[0,0],[0, qq * Gam e^{-Gam z}]] M_m(L,z)^T dz   (times (2 n_sp - 1))
            Ml_z = np.einsum("ij,zjk->zik", ML[l], Minv[l])
            Mm_z = np.einsum("ij,zjk->zik", ML[m], Minv[m])
            integrand = qq * Gam * np.exp(-Gam * zs)[:, None, None] * np.einsum("zi,zj->zij", Ml_z[:, :, 1], Mm_z[:, :, 1])
            Sase[l, m] = np.array([[simpson(integrand[:, i, j], zs) for j in range(2)] for i in range(2)])
    return Sin, Sase


# ---------------------------------------------------------------- checks
# C1 zero-length identity and det = 1 (Liouville; traceless generator) with gain
bg = collective(math.sqrt(18), 0.0, 4.0)
dets = [abs(np.linalg.det(bg["Phi"][l][k]) - 1) for l in range(LMAX + 1) for k in range(0, 4001, 400)]
idt = max(np.max(np.abs(bg["Phi"][l][0] - np.eye(2))) for l in range(LMAX + 1))
record("C1_identity_and_det", idt < 1e-14 and max(dets) < 1e-8,
       f"Phi_l(0) = I (max dev {idt:.1e}); |det Phi_l - 1| <= {max(dets):.1e} along the amplifier (l <= 4)")

# C2 Gam -> 0 reproduces the passive Legendre blocks of C-20261004-claude-a-01
def passive_M(l, mu):
    th = math.atanh(mu)
    def PQ(z):
        Pl = lpmv(0, l, z)
        # Ferrers Q via recurrence
        Q = [math.atanh(z), z * math.atanh(z) - 1]
        Pp = [1.0, z]
        for k in range(1, l):
            Pp.append(((2 * k + 1) * z * Pp[k] - k * Pp[k - 1]) / (k + 1))
            Q.append(((2 * k + 1) * z * Q[k] - k * Q[k - 1]) / (k + 1))
        Ql = Q[l]
        if l == 0:
            return Pp[0], Q[0], 0.0, 1 / (1 - z * z)
        dP = l * (Pp[l - 1] - z * Pp[l]) / (1 - z * z)
        dQ = l * (Q[l - 1] - z * Q[l]) / (1 - z * z)
        return Pp[l], Ql, dP, dQ
    def Phi_mu(z):
        Pl, Ql, dP, dQ = PQ(z)
        w_ = 1 - z * z
        return np.array([[Pl, Ql], [w_ * dP, w_ * dQ]])
    return Phi_mu(mu) @ np.linalg.inv(Phi_mu(0.0))


zs_p = 2.0
bgp = collective(1e-9, 0.0, 1e-9 * zs_p)
errp = 0.0
for l in range(LMAX + 1):
    mu = bgp["ad"][-1] / 2
    errp = max(errp, np.max(np.abs(bgp["Phi"][l][-1] - passive_M(l, mu))))
record("C2_passive_limit", errp < 1e-6,
       f"Gam = 1e-9, zeta = 2: block matrices equal the passive P_l/Q_l propagator (max dev {errp:.1e})")

# C3 Lyapunov and global convergence of the rescaled width for several launches
def s_traj(Gam, adot0, tau_end=40.0):
    A = (18 / Gam**2) ** (1 / 3)
    zL = tau_end / Gam
    zs, a, ad, th, _ = solve_background(Gam, adot0, zL, 2001)
    s = a / (A * np.exp(Gam * zs / 3))
    sp_ = (ad / (A * np.exp(Gam * zs / 3)) - s * Gam / 3) / Gam    # ds/dtau
    V = sp_**2 / 2 + s**2 / 18 + 1 / (9 * s)
    return s, V


lyap_ok, finals = True, []
for Gam_, ad0 in [(0.3, 0.0), (1.0, 0.0), (math.sqrt(18), 0.0), (10.0, 0.0), (math.sqrt(18), -1.0), (1.0, 2.0)]:
    s, V = s_traj(Gam_, ad0)
    lyap_ok &= bool(np.all(np.diff(V) <= 1e-9))
    finals.append((Gam_, ad0, round(float(s[-1]), 6), round(float(V[-1]), 6)))
record("C3_lyapunov_and_convergence", lyap_ok and all(abs(f[2] - 1) < 1e-3 for f in finals),
       f"V(tau) non-increasing; s(tau=40) -> 1 and V -> 1/6 for (Gam, a'(0)) launches: {finals}")

# C4 asymptotic launch: numerics reproduce the closed forms
GamA = math.sqrt(18)                          # A = 1
for gL in (3.0, 6.0):
    bgA = collective(GamA, GamA / 3, gL)      # a = e^{Gam zeta/3} exactly
    U = gL
    comp_cf = (1 / 45) * (U**2 * 0 + 0) if False else None
    # closed forms (A = 1): comp_in = (U/3)^2/5, comp_ase = (1/45)(3U^2 - 18U + 54(1 - e^{-U/3}))
    comp_in_cf = (U / 3) ** 2 / 5
    comp_ase_cf = (3 * U**2 - 18 * U + 54 * (1 - math.exp(-U / 3))) / 45
    freq_in_cf = math.exp(-2 * U / 3)
    freq_ase_cf = 3 * (1 - math.exp(-U / 3)) * math.exp(-2 * U / 3)
    errA = max(abs(bgA["comp_timing_in"] - comp_in_cf), abs(bgA["comp_timing_ase"] - comp_ase_cf) / comp_ase_cf,
               abs(bgA["freq_rel_in"] - freq_in_cf) / freq_in_cf, abs(bgA["freq_rel_ase"] - freq_ase_cf) / freq_ase_cf,
               abs(bgA["a_L"] - math.exp(U / 3)))
    record(f"C4_asymptotic_closed_forms_gL{int(gL)}", errA < 1e-6,
           f"asymptotic launch, gL={gL}: compressed timing, frequency jitter and width match closed forms (max rel dev {errA:.1e})")

# C5 linear-amplifier limit of the energy noise (exact for any Kerr/GVD with flat gain)
for G_, nsp in [(10.0, 1.0), (100.0, 1.0), (100.0, 2.0)]:
    # N0 Var(N)/<N>^2 = [1 + 2 n_sp (G-1)]/G ; Wigner form: dV/dz = 2gV + 2g(n_sp-1/2)E -> same expression
    gl = math.log(G_)
    Vz = solve_ivp(lambda zz, V: [2 * V[0] + 2 * (nsp - 0.5) * math.exp(zz)], (0, gl), [1.0], rtol=1e-12, atol=1e-14).y[0, -1]
    rel = Vz / G_**2
    cf = (1 + 2 * nsp * (G_ - 1)) / G_
    record(f"C5_energy_noise_G{int(G_)}_nsp{nsp}", abs(rel - cf) < 1e-9,
           f"Wigner energy-variance ODE gives N0 Var(N)/<N>^2 = {rel:.6f} vs [1+2n_sp(G-1)]/G = {cf:.6f}")

# C6 uncertainty for the centroid pair at the output (Robertson-Schroedinger, units 1/N_out): det >= 1/4
# use the exact Wigner covariance of the input parabola including the transform-limited part with an edge cutoff
def tl_parabola(delta):     # <((sqrt rho)_x)^2>/E for rho = 1-x^2 on |x|<1-delta, times 1 (a = 1)
    return (3 / 4) * quad(lambda x: x**2 / (1 - x**2), -1 + delta, 1 - delta)[0]


Sig_in = np.array([[1 / 5, 0], [0, tl_parabola(1e-3)]])
detin = np.linalg.det(Sig_in)
record("C6_input_uncertainty", detin >= 0.25,
       f"input centroid pair det(W) = {detin:.3f} >= 1/4 (TF parabola, edge cutoff 1e-3; the TL bandwidth is log-divergent)")

# ---------------------------------------------------------------- predictions
def pack(Gam, adot0, gL, label):
    c = collective(Gam, adot0, gL)
    Sin, Sase = block_noise(c, Gam)
    zs, a, ad = c["zs"], c["a"], c["ad"]
    aL, adL = c["a_L"], c["ad"][-1]
    # mean (matched-LO) phase pbar = p0 - p2/5; scaled eps0^2 N0 Var(pbar)
    vec = {0: np.array([1.0, 0.0]), 2: np.array([-0.2, 0.0])}
    def var_lin(coeffs, S):
        tot = 0.0
        for l, cl in coeffs.items():
            for m, cm in coeffs.items():
                tot += cl @ S[l, m] @ cm
        return float(tot)
    pbar_in, pbar_ase = var_lin(vec, Sin), var_lin(vec, Sase)
    # energy component n0 = (2/3) dE/E: eps0^2 N0 Var(q0) -> N0 Var(n0) = Var(q0)*eps0^2...
    n0_in, n0_ase = Sin[0, 0][1, 1], Sase[0, 0][1, 1]
    # cross covariance pbar with n0 (Kerr correlation), in units 1/(eps0 N0) after multiplying q by eps0
    cr_in = var_lin({0: np.array([1.0, 0.0]), 2: np.array([-0.2, 0.0])}, Sin) if False else None
    corr_in = float(np.array([1.0, 0.0]) @ Sin[0, 0] @ np.array([0.0, 1.0]) - 0.2 * (np.array([1.0, 0.0]) @ Sin[2, 0] @ np.array([0.0, 1.0])))
    corr_ase = float(np.array([1.0, 0.0]) @ Sase[0, 0] @ np.array([0.0, 1.0]) - 0.2 * (np.array([1.0, 0.0]) @ Sase[2, 0] @ np.array([0.0, 1.0])))
    # spectral components s_l/eps0 = q_l - l(l+1) p_l/(a a') at output; variance per l (units 1/(eps0^2 N0) * eps0^2 = 1/N0)
    spec = {}
    for l in range(LMAX + 1):
        v = np.array([-l * (l + 1) / (aL * adL), 1.0])
        spec[l] = {"in": float(v @ Sin[l, l] @ v), "ase": float(v @ Sase[l, l] @ v)}
    # covariance matrix of s_l (l<=4) for (2 n_sp - 1) = 1 (n_sp = 1) -> eigenvalues in L^2(-1,1) metric
    Cs = np.zeros((LMAX + 1, LMAX + 1))
    for l in range(LMAX + 1):
        vl = np.array([-l * (l + 1) / (aL * adL), 1.0])
        for m in range(LMAX + 1):
            vm = np.array([-m * (m + 1) / (aL * adL), 1.0])
            Cs[l, m] = vl @ (Sin[l, m] + Sase[l, m]) @ vm
    Gh = np.diag(np.sqrt(2 / (2 * np.arange(LMAX + 1) + 1)))
    ev = np.sort(np.linalg.eigvalsh(Gh @ Cs @ Gh))[::-1]
    # photon-normalized l=2 quadratures: singular values of the block map (amplitude gains), times 1/sqrt(G)
    ML2 = c["Phi"][2][-1]
    G = math.exp(gL)
    D_L = np.diag([1.0, 1.0])   # (p, q) -> quadratures up to l-dependent constants; gains relative to linear amp
    sv = np.linalg.svd(np.diag([math.sqrt(G), math.sqrt(G)]) @ ML2, compute_uv=False)
    out = {
        "label": label, "Gam": Gam, "adot0": adot0, "gL": gL, "G": G, "zeta_L": c["zL"],
        "a_L": aL, "adot_L": adL, "theta_L_eps0PhiNL": c["theta_L"],
        "energy_relvar_N0": {"formula": "[1+2 n_sp (G-1)]/G", "nsp1": (1 + 2 * (G - 1)) / G},
        "timing_rel_N0": {"in": c["timing_rel_in"], "ase": c["timing_rel_ase"]},
        "comp_timing_N0_T0sq": {"in": c["comp_timing_in"], "ase": c["comp_timing_ase"]},
        "freq_rel_N0": {"in": c["freq_rel_in"], "ase": c["freq_rel_ase"]},
        "cov_Tc_Omc_N0_eps0": {"in": c["cov_in"], "ase": c["cov_ase"]},
        "pbar_var_eps0sq_N0": {"in": pbar_in, "ase": pbar_ase},
        "n0_var_N0_check": {"in": n0_in, "ase": n0_ase, "expect_in": 4 / 9, "expect_ase": (4 / 9) * (1 - 1 / G)},
        "pbar_n0_cov_eps0_N0": {"in": corr_in, "ase": corr_ase},
        "spectral_var_l_N0": spec,
        "spectral_cov_eigs_nsp1": [float(e) for e in ev],
        "spectral_eig_ratio_2nd_1st_nsp1": float(ev[1] / ev[0]),
        "l2_block_singular_values_over_sqrtG": [float(s_ / math.sqrt(G)) for s_ in sv],
    }
    # matched local oscillator (LO = output mean field), output shot-noise units, n_sp = 1 combination plus parts:
    #   C_AA = G + (2n_sp-1)(G-1)   (exact);  eps0^2 C_PP / G = 4 eps0^2 N0 Var(pbar)  (leading order, Kerr-converted)
    #   r = corr(pbar, n0) (n0 = (2/3) dN/N);  1 - r^2 = fraction of phase-quadrature noise not predictable from N
    pv = pbar_in + pbar_ase
    nv = n0_in + n0_ase
    cv = corr_in + corr_ase
    r2 = cv**2 / (pv * nv)
    out["blocks_at_output"] = {f"M{l}": [[float(v) for v in row] for row in c["Phi"][l][-1]] for l in (0, 1, 2, 3)}
    out["matched_LO"] = {"C_AA": {"in": G, "ase": G - 1},
                         "eps0sq_C_PP_over_G": {"in": 4 * pbar_in, "ase": 4 * pbar_ase},
                         "r2_nsp1": r2, "one_minus_r2_nsp1": 1 - r2}
    return out, c, Sin, Sase


main, held = [], []
for gL in (2.0, 4.0, 6.0):
    main.append(pack(math.sqrt(18), 0.0, gL, "main: Gam=sqrt(18), unchirped parabola")[0])
    held.append(pack(1.0, 0.0, gL, "held-out: Gam=1, unchirped parabola")[0])
asym = [pack(math.sqrt(18), math.sqrt(18) / 3, gL, "asymptotic launch, Gam=sqrt(18)")[0] for gL in (2.0, 4.0, 6.0, 9.0, 12.0)]

# C7 energy block consistency: Var(n0) from the block machinery equals (4/9)[1+(2nsp-1)(1-1/G)]/G... in N0 units
okn = True
for r in main + held:
    G = r["G"]
    e_in = r["n0_var_N0_check"]["in"] * 1.0
    e_ase = r["n0_var_N0_check"]["ase"]
    # q0 = n0/eps0, Sigma scaled by eps0^2 N0 -> N0 Var(n0) = Sigma_qq ; expected (4/9)*[1/G... relative to E(zeta_L)]:
    # relative energy variance N0 Var(dE/E) = [1 + (2nsp-1)(1-1/G)]/G ... n0 = (2/3) dE/E
    okn &= abs(e_in - 4 / 9) < 1e-6 and abs(e_ase - (4 / 9) * (1 - 1 / G)) < 1e-4
record("C7_energy_block_vs_exact", okn,
       "block-noise machinery reproduces N0 Var(n_0) = (4/9)[1 + (2n_sp-1)(1-1/G)] (exact energy result; n_0 = (2/3)dE/E)")

# C8 phase-sensitive amplification exponents for l=2 on the asymptote (orchestrator sketch: G^{1/3} and G^{5/3} in power)
gls = [r["gL"] for r in asym]
svs = np.array([r["l2_block_singular_values_over_sqrtG"] for r in asym])     # amplitude gains / sqrt(G)
# photon-normalized: intensity quadrature ~ sqrt(E) eps0 q, phase quadrature ~ sqrt(E) p  -> need diag scaling
def l2_quadrature_gains(gL):
    c = collective(math.sqrt(18), math.sqrt(18) / 3, gL)
    M = c["Phi"][2][-1]
    G = math.exp(gL)
    # (p, q) at output -> (phase quad, intensity quad) amplitudes scale with sqrt(E_L) and sqrt(E_L)*eps0 (eps0 const)
    Mq = math.sqrt(G) * M
    sv = np.linalg.svd(Mq, compute_uv=False)
    return np.log(sv) / gL                      # amplitude-gain exponents per gL
expo = np.array([l2_quadrature_gains(g_) for g_ in (12.0, 18.0, 24.0)])
# envelope exponents in POWER = 2 x amplitude exponents; expect 5/3 and 1/3 asymptotically (oscillation modulates)
pow_exp = 2 * expo[-1]
record("C8_shape_mode_phase_sensitive_exponents", abs(pow_exp[0] - 5 / 3) < 0.08 and abs(pow_exp[1] - 1 / 3) < 0.08,
       f"l=2 block on the asymptote: power-gain exponents of the photon-normalized quadratures at gL=24: "
       f"{pow_exp[0]:.3f} (phase-shape; sketch 5/3) and {pow_exp[1]:.3f} (intensity-shape; sketch 1/3); "
       f"gL=12,18,24 rows: {np.round(2 * expo, 3).tolist()}")

# asymptotic scaling exponents (asymptotic launch): spectral 2nd/1st eigenvalue ratio and 1 - r^2 versus G
far = [pack(math.sqrt(18), math.sqrt(18) / 3, g_, "asymptotic launch, Gam=sqrt(18)")[0] for g_ in (12.0, 15.0, 18.0)]
rat = np.array([r["spectral_eig_ratio_2nd_1st_nsp1"] for r in far])
omr = np.array([r["matched_LO"]["one_minus_r2_nsp1"] for r in far])
gl_ = np.array([12.0, 15.0, 18.0])
slope_rat = np.polyfit(gl_, np.log(rat), 1)[0]
slope_omr = np.polyfit(gl_, np.log(omr), 1)[0]
PRED["asymptotic_exponents"] = {"gL": gl_.tolist(), "spectral_ratio": rat.tolist(), "one_minus_r2": omr.tolist(),
                                "dlog_ratio_dgL": slope_rat, "dlog_one_minus_r2_dgL": slope_omr}
record("C9_asymptotic_suppression_exponents", abs(slope_rat + 2 / 3) < 0.1,
       f"asymptotic launch, gL=12..18: d ln(lambda_2/lambda_1)/d(gL) = {slope_rat:.3f} (expected -2/3: shape/shift modes decay "
       f"as G^(-2/3) relative to the energy mode); d ln(1 - r^2)/d(gL) = {slope_omr:.3f}")

def readouts_with_gain(seed, a_, ad_, eps_, Gam_, zeta_):
    r = np.random.default_rng(seed)
    nc, pc = r.normal(size=7), r.normal(size=7)
    xs, ws = npleg.leggauss(30)
    n = npleg.legval(xs, nc)
    pp = npleg.legval(xs, pc)
    dp = npleg.legval(xs, npleg.legder(pc))
    rho0 = math.exp(Gam_ * zeta_) / a_
    E = (4 / 3) * rho0 * a_
    I = lambda f: float(np.sum(ws * f))
    # x = a xi, dx = a dxi; drho = rho0 n; rho_bar = rho0 (1-xi^2); v_bar = x a'/a; dv = -eps p_x = -(eps/a) p_xi
    mom_rho = lambda k: rho0 * a_ ** (k + 1) * I(xs**k * n)
    mom_rv = lambda k: a_ ** (k + 1) * I(xs**k * (rho0 * n * (a_ * xs) * ad_ / a_ + rho0 * (1 - xs**2) * (-(eps_ / a_) * dp)))
    imag = rho0 * a_ * I((1 - xs**2) * pp)
    n0 = (2 / 3) * mom_rho(0) / E
    n2 = 15 / 4 * ((4 / 3) * mom_rho(2) / (a_**2 * E) - 2 / 3 * n0)
    p2 = -5 / (3 * eps_ * E) * (mom_rv(1) - ad_ / a_ * mom_rho(2))
    p0 = imag / E + p2 / 5
    n1 = 2 * mom_rho(1) / (a_ * E)
    n3 = 35 / 4 * ((4 / 3) * mom_rho(3) / (a_**3 * E) - 2 / 5 * n1)
    p1 = -(a_ / (eps_ * E)) * (mom_rv(0) - ad_ / a_ * mom_rho(1))
    p3 = -35 / 16 * ((4 / (3 * eps_ * E * a_)) * (mom_rv(2) - ad_ / a_ * mom_rho(3)) + 4 / 15 * p1)
    got = np.array([n0, n1, n2, n3, p0, p1, p2, p3])
    return float(np.max(np.abs(got - np.array([*nc[:4], *pc[:4]]))))


e10 = max(readouts_with_gain(s_, a_, ad_, 0.05, Gm, zz) for s_ in range(4)
          for (a_, ad_, Gm, zz) in [(1.0, 0.0, 0.0, 0.0), (2.3, 1.4, 1.0, 1.1), (7.5, 11.7, math.sqrt(18), 6 / math.sqrt(18))])
record("C10_moment_readouts_with_gain", e10 < 1e-10,
       f"generalized moment readouts (with E(zeta) and rho0 = e^(Gam zeta)/a) recover n_0..n_3, p_0..p_3 exactly (max dev {e10:.1e})")

# C11 Kerr-converted mean-phase noise (l = 0 block only) on the asymptotic launch: closed form
#   eps0^2 N0 Var(p0) = (4/9) [ theta_L^2 + (2nsp-1) Gam int e^{-Gam z} (theta_L - theta(z))^2 dz ],
#   theta = (3/(2 Gam A)) (e^{2u/3} - 1), u = Gam zeta, A = 1 for Gam = sqrt(18).
def kerr_p0_closed(U, Gam=math.sqrt(18), A=1.0):
    k = 3 / (2 * Gam * A)
    tin = (math.exp(2 * U / 3) - 1) ** 2
    tase = math.exp(4 * U / 3) * (1 - math.exp(-U)) - 6 * math.exp(2 * U / 3) * (1 - math.exp(-U / 3)) + 3 * (math.exp(U / 3) - 1)
    return (4 / 9) * k**2 * tin, (4 / 9) * k**2 * tase


errk = 0.0
kerr_rows = []
for U in (2.0, 6.0, 12.0):
    cA = collective(math.sqrt(18), math.sqrt(18) / 3, U)
    SinA, SaseA = block_noise(cA, math.sqrt(18))
    num_in, num_ase = SinA[0, 0][0, 0], SaseA[0, 0][0, 0]
    cf_in, cf_ase = kerr_p0_closed(U)
    errk = max(errk, abs(num_in / cf_in - 1), abs(num_ase / cf_ase - 1))
    kerr_rows.append((U, num_in, num_ase, cf_in, cf_ase))
PRED["kerr_p0_asymptotic"] = {"rows_U_numin_numase_cfin_cfase": kerr_rows}
record("C11_kerr_phase_closed_form", errk < 1e-5,
       f"l=0 Kerr-converted phase noise on the asymptotic launch matches (4/9)[theta_L^2 + (2nsp-1) Gam int e^(-Gam z)(theta_L-theta)^2] "
       f"in closed form (max rel dev {errk:.1e})")

# Example systems (illustration of the regime groups; not predictions)
def example(T0_ps, E0_pJ, g_per_m, L_m, beta2_ps2_per_m=0.025, gamma_per_W_m=0.005, lam_um=1.03, beta3_ps3_per_m=4e-5,
            TR_fs=3.0):
    P0 = 3 * E0_pJ * 1e-12 / (4 * T0_ps * 1e-12)          # parabola: E = (4/3) P0 T0
    LD = T0_ps**2 / beta2_ps2_per_m
    LNL = 1 / (gamma_per_W_m * P0)
    eps0 = math.sqrt(LNL / LD)
    Z0 = math.sqrt(LD * LNL)
    Gam = g_per_m * Z0
    gL = g_per_m * L_m
    c = collective(Gam, 0.0, gL, 2001)
    aL, adL = c["a_L"], c["ad"][-1]
    w_edge_THz = adL / (eps0 * T0_ps) / (2 * math.pi)     # output spectral half-width (frequency), hydrodynamic
    w0 = 2 * math.pi * 2.99792458e8 / (lam_um * 1e-6)
    hbar = 1.054571817e-34
    N0 = E0_pJ * 1e-12 / (hbar * w0)
    eps_eff_L = eps0 / math.sqrt(aL * math.exp(Gam * c["zL"]))
    return {"T0_ps": T0_ps, "E0_pJ": E0_pJ, "g_per_m": g_per_m, "L_m": L_m, "P0_W": P0, "eps0": eps0, "Gam": Gam,
            "gL": gL, "Z0_m": Z0, "N0_photons": N0, "a_L": aL, "output_halfwidth_ps": aL * T0_ps,
            "output_spectral_halfwidth_THz": w_edge_THz, "eps_eff_out": eps_eff_L,
            "delta3_out": beta3_ps3_per_m * (adL / (eps0 * T0_ps)) / (3 * beta2_ps2_per_m),
            "TR_over_Tp_in": TR_fs * 1e-3 / T0_ps}


PRED["example_systems"] = {
    "short_low_energy_seed": example(0.2, 10.0, 1.9, 3.2),     # typical Yb similariton amplifier seed: eps0 > 1 (outside (b))
    "energetic_parabolic_seed": example(3.0, 500.0, 0.2, 30.0),
}

PRED["main"] = main
PRED["heldout"] = held
PRED["asymptotic_launch"] = asym
PRED["A_asym_width_const"] = {"Gam=sqrt18": 1.0, "Gam=1": 18 ** (1 / 3)}

res = {"checks": CHK, "predictions": PRED, "wall_time_s": round(time.time() - T0, 1),
       "all_checks_pass": all(v["pass"] for v in CHK.values())}
(OUT / "numeric.json").write_text(json.dumps(res, indent=1, default=float))
print("all numeric checks pass:", res["all_checks_pass"], "| wall", res["wall_time_s"], "s")
