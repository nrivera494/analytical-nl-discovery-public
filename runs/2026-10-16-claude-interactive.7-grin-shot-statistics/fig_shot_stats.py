"""Figure: shot-to-shot relative variance of mode powers against z for five input ensembles (summary.json)."""
import json, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
s = json.load(open(os.path.join(here, 'summary.json'))); rows = s['rows']; D = s['dirichlet']
z = np.array([r['z'] for r in rows])
ens = [('q1e10', 'quiet laser, n = 1e10', '#0d366b', 'o', '-'), ('q1e6', 'technical noise, n_eff = 1e6', '#2a78d6', 's', '-'),
       ('q1e4', 'technical noise, n_eff = 1e4', '#86b6ef', 'D', '-'), ('rin1pc', '1% common-mode amplitude jitter', '#eb6834', '^', '--'),
       ('deph', 'random phases every shot', '#2f9e6b', 'v', ':')]
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, ax = plt.subplots(1, 2, figsize=(12.0, 3.8), facecolor=SURF)
for a in ax:
    a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.6); a.spines[['top', 'right']].set_visible(False); a.set_xscale('log'); a.set_yscale('log')
for key, lab, col, mk, ls in ens:
    ax[0].plot(z, [r[key]['relvar_launched_median'] for r in rows], ls=ls, marker=mk, ms=4, lw=1.4, color=col, label=lab)
    ax[1].plot(z, [r[key]['relvar_I0'] for r in rows], ls=ls, marker=mk, ms=4, lw=1.4, color=col, label=lab)
ax[0].axhline(D['g2_excited'] - 1, color=INK2, lw=1.0, ls='-.', label='thermal (Dirichlet) 0.867')
ax[1].axhline(D['I0_relvar'], color=INK2, lw=1.0, ls='-.', label='thermal (Dirichlet) 2.7e-3')
ax[0].set_xlabel('z / L_NL'); ax[0].set_ylabel('Var(I_p) / <I_p>^2 across shots')
ax[1].set_xlabel('z / L_NL'); ax[1].set_ylabel('Var(I_0) / <I_0>^2 across shots')
ax[0].set_title('Launched excited modes (median): g2 - 1', color=INK, fontsize=9.5, loc='left')
ax[1].set_title('Fundamental (condensate)', color=INK, fontsize=9.5, loc='left')
h, l = ax[0].get_legend_handles_labels(); ax[1].legend(h + [ax[1].get_lines()[-1]], l + ['thermal (Dirichlet), fundamental'], frameon=False, fontsize=7.5, loc='center left', bbox_to_anchor=(1.02, 0.5))
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_shot_stats.png'), dpi=150, facecolor=SURF)
print('wrote fig_shot_stats.png')
