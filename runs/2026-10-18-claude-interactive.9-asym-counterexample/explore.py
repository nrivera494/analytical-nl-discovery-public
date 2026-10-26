"""Stage 1: TL spectrum of the asymmetric source, the even-moment hierarchy, and simple one-parameter masks."""
import json, sys, time
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln
sys.path.insert(0, '.')
from cx_common import *
from zs import logC

out = {}
# --- convention check: the FFT of S equals cos(1) sech(t - i)
n, T = 4096, 96.0
t, k = grid(n, T)
q = pulse_from_spectrum(S_src(k), k, t, T)
out['convention_max_err_q_vs_cos1_sech_t_minus_i'] = float(np.max(np.abs(q - q_TL(t))))
out['M0_numeric'] = float(np.sum(np.abs(q) ** 2) * T / n)
out['M0_closed_2cot1'] = M0
out['peak_abs_q0'] = float(np.max(np.abs(q)))
print(out, flush=True)

# --- all TL eigenvalues: FC at two resolutions, each confirmed by BO-Richardson on the analytic pulse
fc = {}
for n_, T_ in ((512, 64.0), (1024, 128.0)):
    t_, k_ = grid(n_, T_)
    w = fc_eigs(q_TL(t_), T_, imag_min=1e-3)
    w = [z for z in w if abs(z.real) < 0.5 * np.pi * n_ / T_]
    fc['%d_%g' % (n_, T_)] = [[float(z.real), float(z.imag)] for z in w[:8]]
print('FC TL eigenvalues', fc, flush=True)
out['TL_fc_eigs'] = fc
cands = fc['1024_128']
conf = []
for re_, im_ in cands:
    zR, zs = line_eta(lambda kk: np.ones_like(kk, dtype=complex), re_ + 1j * im_, T=96.0, n=8192)
    if abs(zR - (re_ + 1j * im_)) < 1e-4 and zR.imag > 1e-3:
        conf.append([float(zR.real), float(zR.imag), [float(z.imag) for z in zs]])
out['TL_eigs_confirmed_BO'] = conf
eta_TL = max(c[1] for c in conf)
out['eta_TL'] = eta_TL
out['f1_TL'] = 4 * eta_TL / M0
print('confirmed TL eigenvalues (BO-Richardson):', conf, 'f1_TL', out['f1_TL'], flush=True)

# --- even-moment hierarchy (B): U_2n = [int |q0|^2n / C_2n]^(1/(2n-1)), f1 bound 4 U_2n / M0
hier = []
for nn in range(1, 41):
    p = 2 * nn
    I = quad(lambda s: (C1 ** 2 / (np.sinh(s) ** 2 + C1 ** 2)) ** nn, -60, 60, limit=500, epsabs=0, epsrel=1e-13)[0]
    U = np.exp((np.log(I) - logC(p)) / (p - 1))
    hier.append({"n": nn, "U_2n": U, "f1_bound": 4 * U / M0})
out['hierarchy'] = hier
best = min(hier[:20], key=lambda r: r['U_2n'])
out['hierarchy_min_n_le_20'] = best
print('hierarchy n<=20 min at n=%d, f1 bound %.6f; n=1..5:' % (best['n'], best['f1_bound']), [round(r['f1_bound'], 5) for r in hier[:5]], flush=True)

# --- (F) spectral bound for this source (valid for any source), min over p >= 2
kk = np.linspace(-40, 200, 480001); dk = kk[1] - kk[0]
SS = S_src(kk)
Fv = []
for p in np.concatenate([np.linspace(2, 6, 41), np.linspace(6.5, 60, 108)]):
    pp = p / (p - 1)
    Fb = np.sqrt(pp) / (2 * np.pi) * np.exp(-(0.5 * np.log(p) + logC(p)) / (p - 1)) * np.sum(SS ** pp) * dk
    Fv.append((float(Fb), float(p)))
out['F_bound_min'] = {"eta_bound": min(Fv)[0], "p": min(Fv)[1], "f1_bound": 4 * min(Fv)[0] / M0}
print('(F) min', out['F_bound_min'], flush=True)

# --- simple masks: quadratic and cubic spectral phase, smooth low-pass and high-pass amplitude edges
z0 = conf[int(np.argmax([c[1] for c in conf]))]
z0 = z0[0] + 1j * z0[1]
k0 = 0.0
scans = {}
for name, mk, vals in (
        ("GDD phi = b k^2/2", lambda b: (lambda kk: np.exp(0.5j * b * (kk - k0) ** 2)), np.linspace(-1.0, 1.0, 21)),
        ("TOD phi = c k^3/6", lambda c: (lambda kk: np.exp(1j * c * (kk - k0) ** 3 / 6)), np.linspace(-0.3, 0.3, 13)),
        ("low-pass edge at kc (width 0.3)", lambda kc: (lambda kk: 1 / (1 + np.exp((kk - kc) / 0.3)) + 0j), np.linspace(-0.5, 6.0, 14)),
        ("high-pass edge at kc (width 0.3)", lambda kc: (lambda kk: 1 / (1 + np.exp(-(kk - kc) / 0.3)) + 0j), np.linspace(-3.0, 1.0, 9))):
    rows = []
    zz = z0
    for v in vals:
        zR, zs = line_eta(mk(v), zz, T=96.0, n=4096)
        rows.append([float(v), float(zR.real), float(zR.imag), float(zR.imag / eta_TL - 1)])
        zz = zR
    scans[name] = rows
    bestrow = max(rows, key=lambda r: r[2])
    print('%-34s best param %+.3f eta %.8f gain %+.4e' % (name, bestrow[0], bestrow[2], bestrow[3]), flush=True)
out['simple_scans'] = scans
json.dump(out, open('explore_summary.json', 'w'), indent=1, default=float)
