"""Figure fig_ensembles.png: per-realization outcomes of the thermalization ensembles (strip plots): <I0> - <I0>_Dirichlet, excited g2,
Var I0 / Var_Dirichlet, and D_RJ, for E1 (disorder seeds), E2 (launch draws), E3 (Kerr only), E4 (LP11-only), E5 (centre-focused)."""
import json, numpy as np, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(here, 'ensemble_thermalization.jsonl'))]
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
COL = {'E1': '#2a78d6', 'E2': '#86b6ef', 'E3': '#eb6834', 'E4': '#2f9e6b', 'E5': '#0d366b'}
groups = []
for ens, kind, Eps, sig, lab in [('E1', 'deph', [0.3, 0.6, 0.9], 0.3, 'disorder seeds'), ('E2', 'deph', [0.3, 0.6, 0.9], 0.3, 'launch draws'),
                                 ('E3', 'deph', [0.3, 0.6, 0.9], 0.0, 'Kerr only'), ('E4', 'G1', [1.0], 0.3, 'LP11-only'), ('E4', 'G1', [1.0], 0.0, 'LP11-only, Kerr only'),
                                 ('E5', 'focused', [0.6, 0.9], 0.3, 'focused'), ('E5', 'focused', [0.6, 0.9], 0.0, 'focused, Kerr only')]:
    for Ep in Eps:
        g = [r for r in rows if r['ens'] == ens and r['kind'] == kind and abs(r['Eprime'] - Ep) < 1e-3 and r['sigma'] == sig]
        if g: groups.append((f"{lab}\nE'={Ep}", COL[ens], g))
plt.rcParams.update({'font.size': 8, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, axs = plt.subplots(4, 1, figsize=(13, 10), facecolor=SURF, sharex=True)
specs = [('<I0> - <I0>_Dirichlet', lambda r: r['I0'] - r['I0_D'], [(-0.015, 0.015)]), ('excited-mode g2', lambda r: r['g2_ex'], [(1.8667 - 0.06, 1.8667 + 0.06)]),
         ('Var I0 / Var_Dirichlet', lambda r: r['VarI0']/r['VarI0_D'] if r['VarI0_D'] > 0 else np.nan, [(0.65, 1.35)]), ('D_RJ (max relative group deviation)', lambda r: r['D_RJ'], [(0, 0.15)])]
rng = np.random.default_rng(0)
for ax, (lab, f, bands) in zip(axs, specs):
    for i, (gl, c, g) in enumerate(groups):
        y = np.array([f(r) for r in g]); x = i + rng.uniform(-0.18, 0.18, len(y))
        ax.scatter(x, y, s=14, color=c, alpha=0.85, edgecolor='none')
    for lo, hi in bands: ax.axhspan(lo, hi, color=GRID, alpha=0.6, zorder=0)
    ax.set_ylabel(lab); ax.set_facecolor(SURF); ax.grid(True, axis='y', color=GRID, lw=0.5); ax.spines[['top', 'right']].set_visible(False)
axs[0].set_ylim(-0.14, 0.04); axs[0].text(0.62, 0.08, 'LP11-only, Kerr only: -0.57 (off scale; no thermalization)', transform=axs[0].transAxes, fontsize=7, color=INK2)
axs[1].set_ylim(0.9, 2.1); axs[3].set_yscale('symlog', linthresh=0.1)
axs[-1].set_xticks(range(len(groups))); axs[-1].set_xticklabels([g[0] for g in groups], rotation=0, fontsize=6.5)
axs[0].set_title('Thermalization ensembles: one dot per realization (grey bands: pre-registered tolerances)', color=INK, fontsize=9.5, loc='left')
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_ensembles.png'), dpi=130, facecolor=SURF); print('wrote fig_ensembles.png')
