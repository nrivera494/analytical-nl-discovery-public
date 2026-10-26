"""Figure: condensate fraction, disorder-free toy vs GGE shell prediction vs RJ, per case (dot plot)."""
import json, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
BLUE, ORANGE, GRAY = '#2a78d6', '#eb6834', '#8f8e89'
lin = json.load(open(os.path.join(here, 'gge_linear.json')))
rows = [r for r in lin if not (r['K'] == 4 and r['Eprime'] == 0.3)]   # exclude the non-ergodic case
pre = {(4, 0.9, 'focused'), (4, 0.6, 'focused'), (5, 0.9, 'focused'), (4, 0.6, 'dephased')}
labels = [f"K={r['K']}, E'={r['Eprime']}\n{'aligned' if r['launch']=='focused' else 'random'} phases" for r in rows]
y = np.arange(len(rows))[::-1]
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, ax = plt.subplots(figsize=(6.6, 3.8), facecolor=SURF); ax.set_facecolor(SURF)
ax.grid(True, axis='x', color=GRID, lw=0.6); ax.spines[['top', 'right']].set_visible(False)
for yi, r in zip(y, rows):
    ax.plot([min(r['N0_RJ'], r['N0_toy'], r['N0_shell']), max(r['N0_RJ'], r['N0_toy'], r['N0_shell'])], [yi, yi], color=GRID, lw=2, zorder=1)
ax.scatter([r['N0_RJ'] for r in rows], y, s=60, marker='|', color=GRAY, linewidths=2.2, label='Rayleigh-Jeans', zorder=2)
ax.scatter([r['N0_shell'] for r in rows], y + 0.14, s=46, marker='D', color=BLUE, edgecolor=SURF, linewidths=1.2, label='GGE on (N, E\', H_res) shell, no fit', zorder=3)
ax.scatter([r['N0_toy'] for r in rows], y - 0.14, s=40, marker='o', color=ORANGE, edgecolor=SURF, linewidths=1.2, label='toy dynamics, long-z average', zorder=4)
for yi, r in zip(y, rows):
    if (r['K'], r['Eprime'], r['launch']) in pre:
        ax.text(max(r['N0_RJ'], r['N0_toy'], r['N0_shell']) + 0.006, yi, 'pre-registered', va='center', fontsize=7, color=INK2)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7.5)
ax.set_xlabel('condensate fraction <I_0>/N'); ax.set_xlim(0.40, 0.76); ax.set_ylim(-0.6, len(rows)-0.4)
ax.set_title('Without disorder the endpoint remembers the input phases', color=INK, fontsize=9.5, loc='left', pad=26)
ax.legend(frameon=False, fontsize=7.5, loc='lower left', bbox_to_anchor=(0.0, 1.0), ncol=3, borderaxespad=0.2)
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_gge.png'), dpi=150, facecolor=SURF); print('saved')
