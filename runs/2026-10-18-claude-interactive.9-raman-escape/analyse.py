"""Leading ZS eigenvalue of the propagated field, plane by plane, for the Raman and no-Raman runs of propagate.jl.

Soliton units of the launch: q = sqrt(gamma T0^2/|beta2|) A, t_n = T/T0, so the TL input N sech t_n has eta_max = N - 1/2
(the passive-mask ceiling of C-20261018-pi-chatgpt-01 (C) for integer N). Eigenvalues by Boffetta-Osborne on the
cropped field (cells = samples and every other sample, Richardson), started from (a) the previous plane's eigenvalue
and (b) a guess from the tallest pulse (eta ~ peak/2, xi ~ -Omega/2 from its mean instantaneous frequency); the
largest converged Im is kept. The tallest pulse's mean carrier is removed first (Galilean invariance).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, '../2026-10-18-claude-interactive.9-zs-solver-validation')
from zs import bo_refine, bo_a

RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-18-claude-interactive.9-raman-escape')
c_light = 2.99792458e-4
w0 = 2 * np.pi * c_light / 1550e-9
gamma = 2.6e-20 * w0 / c_light / 80e-12
beta2 = -21.7e-27 * 1e24
t = np.fromfile(os.path.join(RAW, 't_f64.bin'), dtype=np.float64)
Nt = len(t)


def eig_plane(q, tn, guesses):
    dtn = tn[1] - tn[0]
    amp = np.abs(q)
    keep = np.where(amp > 1e-9 * amp.max())[0]
    i0, i1 = max(keep[0] - 200, 0), min(keep[-1] + 200, len(q) - 1)
    if (i1 - i0) % 2:
        i1 -= 1
    qc = q[i0:i1]
    best = None
    for g in guesses:
        try:
            z1, r1, _ = bo_refine(qc, dtn, g)
            z2, r2, _ = bo_refine(qc[::2], 2 * dtn, z1)
        except Exception:
            continue
        if not (np.isfinite(z1) and np.isfinite(z2)) or z1.imag <= 0.05:
            continue
        zR = (4 * z1 - z2) / 3
        if abs(z1 - z2) > 0.05:
            continue
        if best is None or zR.imag > best[0].imag + 1e-9:
            best = (zR, z1, z2)
    return best


out = {}
for fn in sorted(os.listdir(RAW)):
    if not fn.startswith('fields_'):
        continue
    tag = fn[len('fields_'):-4]
    T0 = float(tag.split('_T0')[1].split('_')[0])
    N = float(tag.split('N')[1].split('_')[0])
    A = np.fromfile(os.path.join(RAW, fn), dtype=np.complex128).reshape(-1, Nt).T   # (Nt, planes), Julia column-major
    scale = np.sqrt(gamma * T0 ** 2 / abs(beta2))
    tn = t / T0
    rows = []
    zprev = 1j * (N - 0.5)
    for j in range(A.shape[1]):
        q = scale * A[:, j]
        ip = int(np.argmax(np.abs(q)))
        sl = slice(max(ip - 300, 0), min(ip + 300, Nt))
        ph = np.unwrap(np.angle(q[sl]))
        w = np.abs(q[sl]) ** 2
        Om = np.sum(np.gradient(ph, tn[sl]) * w) / np.sum(w)
        # remove the tallest pulse's carrier (Galilean invariance: eta unchanged, xi shifts by Om/2)
        qd = q * np.exp(-1j * Om * tn)
        res = eig_plane(qd, tn, [1j * np.abs(q[ip]) / 2, 1j * zprev.imag, 1j * (zprev.imag + 0.1), 0.3 + 1j * zprev.imag])
        M = np.sum(np.abs(q) ** 2) * (tn[1] - tn[0])
        if res is None:
            rows.append({"plane": j, "eta": None, "mass": M})
            continue
        zR, z1, z2 = res
        zprev = zR
        rows.append({"plane": j, "zeta": [float(zR.real), float(zR.imag)], "eta": float(zR.imag),
                     "eta_h_2h": [float(z1.imag), float(z2.imag)], "peak": float(np.abs(q[ip])),
                     "t_peak_T0": float(tn[ip]), "Omega_peak": float(Om), "mass": float(M)})
        print('%-40s plane %2d  eta %.6f  (h %.6f, 2h %.6f)  peak %.3f  t %.1f  Omega %.2f  mass %.5f' % (
            tag, j, zR.imag, z1.imag, z2.imag, np.abs(q[ip]), tn[ip], Om, M), flush=True)
    etas = [r['eta'] for r in rows if r['eta'] is not None]
    out[tag] = {"N": N, "T0_ps": T0, "integrable_ceiling_eta": N - 0.5, "planes": rows,
                "max_eta": max(etas), "max_eta_over_ceiling": max(etas) / (N - 0.5) - 1}
    print('== %s: max eta %.6f vs integrable ceiling %.2f (%+.3f%%)' % (tag, max(etas), N - 0.5, 100 * (max(etas) / (N - 0.5) - 1)), flush=True)
json.dump(out, open('summary.json', 'w'), indent=1)
