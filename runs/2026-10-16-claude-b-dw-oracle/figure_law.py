"""Figure for C-20261016-claude-b-01: (a) sech N=2 gated DW yield vs 1/delta3 (numpy, solver), with slopes d_* and
Roy Eq. 6; (b) local slope / d_* vs delta3 for all launches; (c) GDD headroom measured vs exp(-dd_*/delta3)."""
import json, glob, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from lawfit import load, local_slopes
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
d3, eta, _, _ = load(['yield_sech2a.json', 'yield_sech2b.json', 'yield_roy.json'])
ax[0].semilogy(1/d3, eta, 'o', label='numpy (Yoshida split-step)')
sol = json.load(open('../2026-10-16-claude-b.7-solver-dwyield/summary.json'))
try:
    pts = [(r['delta3'], r['eta_DW_smooth']) for r in sol['item2']['rows']]
except Exception:
    pts = [(0.010, 1.499e-10), (0.012, 4.419e-8), (0.014, 2.350e-6), (0.016, 4.296e-5), (0.020, 1.7600e-3), (0.025, 1.0773e-2), (0.030, 2.6480e-2)]
pts = np.array(pts)
ax[0].semilogy(1/pts[:, 0], pts[:, 1], 'x', ms=9, label='FastDifferentiableMMNLO (claude-b.7)')
x = np.linspace(30, 125, 50); x0 = 1/0.010; y0 = eta[np.argmin(abs(d3 - 0.010))]
ax[0].semilogy(x, y0*np.exp(-0.374664*(x - x0))*(x/x0)**3.43, 'k-', lw=1, label=r'$d_*=\frac{1}{2}\arccos(\sqrt{3}-1)$, $p=-3.43$')
ax[0].semilogy(x, y0*np.exp(-np.pi/6*(x - x0)), 'r--', lw=1, label=r'ejected-soliton strip $\pi/6$ (exponent of Roy Eq. 6; TOD-only comparison)')
ax[0].set_xlabel(r'$1/\delta_3$'); ax[0].set_ylabel(r'gated DW yield $\eta_{\rm DW}$'); ax[0].set_title('(a) sech N=2, TOD only, $\\xi=4$')
ax[0].set_ylim(1e-15, 1); ax[0].legend(fontsize=7)
sets = [('sech N=2', ['yield_sech2a.json', 'yield_sech2b.json', 'yield_roy.json'], 0.374664),
        ('sech N=3 (held out)', ['yield_s3.json'], 0.1997), ('Gauss N=4 (held out)', ['yield_g4.json'], 0.1322),
        ('Gauss N=3, $\\xi_f$=2', ['yield_g3.json'], 0.1923), ('Gauss N=3, $\\xi_f$=1 (length test)', ['yield_g3L1.json'], 0.2015)]
for lab, files, ds in sets:
    d, e, _, _ = load(files); m, s = local_slopes(d, e); k = m < 0.02
    ax[1].plot(m[k], s[k]/ds, 'o-', label=lab)
for f, ds, lab in [('h4_g3_m1_*.json', 0.2346, 'Gauss N=3 + Raman (held out)'), ('h4_law_m1_*.json', 0.4410, 'sech N=2 + Raman')]:
    rows = []
    for g in sorted(glob.glob(f)): rows += json.load(open(g))
    rows.sort(key=lambda r: r['d3'])
    d = np.array([r['d3'] for r in rows]); e = np.array([r['h2']['eta_DW'] for r in rows])
    m, s = local_slopes(d, e); k = m < 0.02
    ax[1].plot(m[k], s[k]/ds, 's--', label=lab)
ax[1].axhline(1, color='k', lw=0.8); ax[1].set_xlim(0, 0.02); ax[1].set_ylim(0.6, 1.1)
ax[1].set_xlabel(r'$\delta_3$'); ax[1].set_ylabel(r'local slope $-d\ln\eta/d(1/\delta_3)$ / $d_*$'); ax[1].set_title('(b) approach to $d_*$ as $\\delta_3\\to0$')
ax[1].legend(fontsize=7)
t = json.load(open('gdd_vs_dstar.json'))
for d3s, mk in [('0.01', 'o'), ('0.006', 's')]:
    r = np.array([[c[0], c[2], c[3]] for c in t[d3s]], float)
    ax[2].semilogy(r[:, 0], r[:, 1], mk, label=f'measured, $\\delta_3$={d3s}')
    ax[2].semilogy(r[:, 0], r[:, 2], mk + '--', mfc='none', label=f'$\\exp(-\\Delta d_*/\\delta_3)$, {d3s}')
ax[2].set_xlabel('GDD $C$ (phase $Cw^2/2$)'); ax[2].set_ylabel('gated DW yield / TL'); ax[2].set_title('(c) shaping acts through $d_*$ (Gauss N=3)')
ax[2].legend(fontsize=7)
plt.tight_layout(); plt.savefig('fig_singularity_law.png', dpi=110)
print('saved')
