"""Figure: exact quantum dynamics vs truncated Wigner (TWA) for 4 modes. Left: mean-field fraction of the fundamental, GRIN subset.
Middle: Fano factor of the fundamental, GRIN subset. Right: largest |coh_exact - coh_TWA| against n, all cases, with the closed-form
Wigner-truncation error of self/cross-phase dynamics (summary.json)."""
import json, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
RAMP = ['#86b6ef', '#2a78d6', '#0d366b']      # ordinal blue, light->dark = small->large n
ORANGE, GREEN = '#eb6834', '#2f9e6b'
grin = json.load(open(os.path.join(here, 'exact_vs_twa_grin4_mixing55.json')))
summ = json.load(open(os.path.join(here, 'summary.json')))
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, ax = plt.subplots(1, 3, figsize=(12.0, 3.6), facecolor=SURF)
for a in ax:
    a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.6); a.spines[['top', 'right']].set_visible(False)
for r, col in zip(grin, RAMP):
    z = np.array(r['z']); n = r['n']
    ax[0].plot(z, r['coh_exact'], color=col, lw=1.8, label=f'n = {n}, exact')
    ax[0].errorbar(z, r['coh_twa_weyl'], yerr=r['coh_twa_weyl_err'], fmt='o', ms=3, color=col, mfc=SURF, mew=1.0, elinewidth=0.8, label=f'n = {n}, TWA')
    ax[1].plot(z, r['fano_exact'], color=col, lw=1.8, label=f'n = {n}, exact')
    ax[1].errorbar(z, r['fano_twa_weyl'], yerr=r['fano_twa_weyl_err'], fmt='o', ms=3, color=col, mfc=SURF, mew=1.0, elinewidth=0.8, label=f'n = {n}, TWA')
ax[0].set_xlabel('z / L_NL'); ax[0].set_ylabel('|<a_0>|^2 / <n_0>')
ax[0].set_title('GRIN subset: mean-field collapse', color=INK, fontsize=9.5, loc='left')
ax[0].legend(frameon=False, fontsize=7, ncol=1)
ax[1].axhline(1, color=INK2, lw=0.8, ls=':')
ax[1].set_xlabel('z / L_NL'); ax[1].set_ylabel('Var(n_0) / <n_0>')
ax[1].set_title('GRIN subset: condensate number fluctuations', color=INK, fontsize=9.5, loc='left')
cases = [('condensate85', 'toy, f0 = 0.85', RAMP[1], 'o'), ('mixing55', 'toy, f0 = 0.55', ORANGE, 's'), ('grin4_mixing55', 'GRIN, f0 = 0.55', GREEN, 'D')]
for tag, lab, col, mk in cases:
    rows = sorted([v for k, v in summ.items() if not k.endswith('_exponent') and v['tag'] == tag], key=lambda v: v['n'])
    if not rows: continue
    ns = np.array([v['n'] for v in rows])
    ax[2].errorbar(ns, [v['max_abs_coh_exact_minus_twa_weyl'] for v in rows], yerr=[v['twa_weyl_err_there'] for v in rows],
                   fmt=mk, ms=5, color=col, elinewidth=0.8, label=f'{lab}: simulation')
    if tag != 'grin4_mixing55':
        ax[2].plot(ns, [v['max_abs_frozen_exact_minus_frozen_twa'] for v in rows], color=col, lw=1.2, ls='--', label=f'{lab}: closed form (SPM/XPM)')
nn = np.array([12, 120]); ax[2].plot(nn, 0.3/nn, color=INK2, lw=0.8, ls=':', label='slope -1')
ax[2].set_xscale('log'); ax[2].set_yscale('log'); ax[2].set_xlabel('photons n'); ax[2].set_ylabel('max_z |coh_exact - coh_TWA|')
ax[2].set_title('TWA error falls as 1/n', color=INK, fontsize=9.5, loc='left')
ax[2].legend(frameon=False, fontsize=6.5)
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_exact_vs_twa.png'), dpi=150, facecolor=SURF)
print('wrote fig_exact_vs_twa.png')
