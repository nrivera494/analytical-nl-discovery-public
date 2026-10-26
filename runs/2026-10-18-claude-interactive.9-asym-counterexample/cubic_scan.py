"""Stage 4: explicit cubic spectral phase phi = c (k - k0)^3 / 6 on the asymmetric source, scanned on the line (BO,
Romberg over T/4096, T/8192, T/16384 cells, T = 96)."""
import json, sys
import numpy as np
sys.path.insert(0, '.')
from cx_common import *

ex = json.load(open('explore_summary.json'))
eta_TL = ex['eta_TL']
zTL = complex(*ex['TL_eigs_confirmed_BO'][0][:2])


def romberg_line(mfun, z0, T):
    zs = []
    for nn in (4096, 8192, 16384):
        t, k = grid(nn, T)
        q = pulse_from_spectrum(mfun(k) * S_src(k), k, t, T)
        z, ares, it = bo_refine(q, T / nn, z0)
        zs.append(z)
        z0 = z
    r1 = [(4 * zs[1] - zs[0]) / 3, (4 * zs[2] - zs[1]) / 3]
    return (16 * r1[1] - r1[0]) / 15


rows = []
for k0 in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0):
    z0 = zTL
    for c in np.linspace(0.0, -1.5, 31):
        z = romberg_line(lambda kk, c=c, k0=k0: np.exp(1j * c * (kk - k0) ** 3 / 6), z0, 96.0)
        if not np.isfinite(z) or z.imag <= 0:
            break
        rows.append([k0, float(c), float(z.imag), float(z.imag / eta_TL - 1)])
        z0 = z
    b = max([r for r in rows if r[0] == k0], key=lambda r: r[2])
    print('k0 %.1f: best c %.3f eta %.10f gain %+.4f%%' % (k0, b[1], b[2], 100 * b[3]), flush=True)
best = max(rows, key=lambda r: r[2])
print('overall best cubic phase: k0 %.1f c %.3f eta %.10f gain %+.4f%%' % tuple(best[:3] + [100 * best[3]]))
json.dump({"eta_TL_line": eta_TL, "rows_k0_c_eta_gain": rows, "best": best}, open('cubic_scan_summary.json', 'w'), indent=1)
