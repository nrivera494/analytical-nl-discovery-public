"""Figure fig_disorder_scan.png: (left) relaxation length against white-noise disorder strength sigma (nominal L_d = 1/sigma^2), pre-registered
L_rel (50 L_NL window) and post-hoc L_rel10 (10 L_NL window), per realization and median; (middle) the same against correlation length l_c at
fixed white-noise-equivalent strength (piecewise-constant model); (right) <I0> endpoint against the Dirichlet value for every setting."""
import json, numpy as np, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(here, 'summary.json')))['settings']
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'; B1, B2, OR, GR = '#2a78d6', '#0d366b', '#eb6834', '#2f9e6b'
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, axs = plt.subplots(1, 3, figsize=(14, 4), facecolor=SURF)
def pts(name, key):
    v = S.get(name, {}).get(key) or []
    return [x for x in v if x is not None]
ax = axs[0]
for sig in [0.1, 0.3, 1.0, 3.0]:
    n = f'deph_white_s{sig}'
    for key, c, m in [('L_rel10_posthoc', B1, 'o'), ('L_rel', OR, 's')]:
        y = pts(n, key); ax.scatter([sig]*len(y), np.maximum(y, 1), color=c, s=14, marker=m, alpha=0.7)
    for key, c in [('L_rel10_posthoc', B1), ('L_rel', OR)]:
        y = pts(n, key)
        if y: ax.scatter([sig], [max(np.median(y), 1)], color=c, s=90, marker='_', lw=2)
for n, x0 in [('G1_white_s0.1', 0.1), ('G1_white_s1.0', 1.0), ('G1_white_s3.0', 3.0)]:
    y = pts(n, 'z_on'); ax.scatter([x0*1.15]*len(y), y, color=GR, s=14, marker='^', alpha=0.7)
e4 = [json.loads(l) for l in open(os.path.join(here, '../2026-10-17-claude-interactive.7-ensemble-thermalization/ensemble_thermalization.jsonl'))]
y = [r['z_on'] for r in e4 if r['ens'] == 'E4' and r['sigma'] == 0.3 and r['z_on'] is not None]
ax.scatter([0.3*1.15]*len(y), y, color=GR, s=14, marker='^', alpha=0.7)   # LP11-only at sigma = 0.3: ensemble E4 (12 realizations)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('white-noise strength σ  (L_d ≈ 1/σ² L_NL)'); ax.set_ylabel('length / L_NL')
ax.set_title('relaxation length against disorder strength', fontsize=9, loc='left', color=INK)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], color=OR, marker='s', ls='', label='L_rel, E\'=0.6 (pre-registered, 50 L_NL window)'), Line2D([], [], color=B1, marker='o', ls='', label='L_rel10 (post hoc, 10 L_NL window)'), Line2D([], [], color=GR, marker='^', ls='', label='LP11-only onset z_on'), Line2D([], [], color=INK2, marker='_', ls='', ms=12, label='medians')], frameon=False, fontsize=6.5, loc='upper left')
ax = axs[1]
for lc in [0.1, 1.0, 10.0, 100.0]:
    for key, c, m in [('L_rel10_posthoc', B1, 'o'), ('L_rel', OR, 's')]:
        y = pts(f'deph_piecewise_s0.3_lc{lc}', key); ax.scatter([lc]*len(y), np.maximum(y, 1), color=c, s=14, marker=m, alpha=0.7)
        y2 = pts(f'deph_piecewise_s1.0_lc{lc}', key); ax.scatter([lc*1.2]*len(y2), np.maximum(y2, 1), color=c, s=14, marker='D', alpha=0.4)
for key, c in [('L_rel10_posthoc', B1), ('L_rel', OR)]:
    y = pts('deph_white_s0.3', key)
    if y: ax.axhline(max(np.median(y), 1), color=c, lw=0.8, ls='--')
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('correlation length l_c / L_NL (piecewise-constant coupling)'); ax.set_ylabel('length / L_NL')
ax.set_title('against correlation length, matched strength', fontsize=9, loc='left', color=INK)
ax.legend(handles=[Line2D([], [], color=INK2, marker='o', ls='', label='σ_eff = 0.3'), Line2D([], [], color=INK2, marker='D', ls='', alpha=0.5, label='σ_eff = 1'), Line2D([], [], color=INK2, ls='--', label='white noise σ = 0.3 (medians)')], frameon=False, fontsize=6.5, loc='upper left')
ax = axs[2]; names = list(S.keys())
for i, n in enumerate(names):
    y = np.array(S[n]['I0']) - S[n]['I0_D']; ax.scatter([i]*len(y), y, s=14, color=GR if n.startswith('G1') else B1, alpha=0.8)
ax.axhspan(-0.02, 0.02, color=GRID, alpha=0.6, zorder=0); ax.set_xticks(range(len(names))); ax.set_xticklabels([n.replace('deph_', '').replace('_', ' ') for n in names], rotation=70, fontsize=6)
ax.set_ylabel('<I0> - <I0>_Dirichlet'); ax.set_title('endpoint, z in [1000, 4000] (grey: ±0.02)', fontsize=9, loc='left', color=INK)
for a in axs: a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.5); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_disorder_scan.png'), dpi=130, facecolor=SURF); print('wrote fig_disorder_scan.png')
