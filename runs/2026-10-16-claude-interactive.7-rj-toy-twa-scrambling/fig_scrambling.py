"""Figure: mean-field collapse of a coherent input vs a dephased input (truncated Wigner, toy), and the collapse length vs n."""
import json, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-rj-toy-twa-scrambling')
here = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
RAMP = ['#86b6ef', '#6da7ec', '#3987e5', '#2a78d6', '#1c5cab', '#184f95', '#0d366b']   # ordinal blue, light->dark = small->large n
ORANGE = '#eb6834'
curves = []
for fname in ['twa_scramble.json', 'twa_scramble2.json']:
    o = json.load(open(os.path.join(RAW, fname))); z = np.array(o['z'])
    for j, (l, n) in enumerate(o['cols']):
        cm = np.array([rec[j]['coh'] for rec in o['records']]).mean(1)
        rv = np.median(np.array([rec[j]['relvar'] for rec in o['records']])[:, 1:], axis=1)
        curves.append((l, n, z, cm, rv))
coh = sorted([c for c in curves if c[0] == 'coherent'], key=lambda c: c[1])
deph = [c for c in curves if c[0] == 'dephased']
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.6), facecolor=SURF)
for a in ax:
    a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.6); a.spines[['top', 'right']].set_visible(False)
for (l, n, z, cm, rv), col in zip(coh, RAMP):
    ax[0].plot(z, cm, color=col, lw=1.6, label=f'coherent, n = 1e{int(np.log10(n))}')
ax[0].plot(deph[0][2], deph[0][3], color=ORANGE, lw=1.6, ls='--', label='dephased (all n)')
ax[0].set_xscale('log'); ax[0].set_xlabel('z / L_NL'); ax[0].set_ylabel('mean-field fraction |<a>|^2 / <n>  (mode average)')
ax[0].set_title('Coherent input keeps its mean field until z_E', color=INK, fontsize=9.5, loc='left')
ax[0].legend(frameon=False, fontsize=7.5, loc='lower left', bbox_to_anchor=(0.0, 0.07))
# right: half-collapse length vs n, with the two-branch model fitted on n = 1e6 and 1e8 (see twa2_predictions.txt)
ns = np.array([c[1] for c in coh]); zh = []
for (l, n, z, cm, rv) in coh:
    k = np.argmax(cm < 0.5); zh.append(z[k-1] + (0.5-cm[k-1])*(z[k]-z[k-1])/(cm[k]-cm[k-1]))
from scipy.optimize import brentq
a_, c_, lam = 1.57, 0.95, 0.0037
nn = np.logspace(3.7, 11.3, 60); pred = [brentq(lambda zz: a_*zz*zz/(2*n)+c_*np.exp(2*lam*zz)/n-0.693, 1, 2e4) for n in nn]
ax[1].plot(nn, pred, color=INK2, lw=1.2, label='two-channel model (fit at n = 1e6, 1e8)')
pre = np.isin(ns, [1e5, 1e7, 1e9, 1e11])
ax[1].plot(ns[~pre], np.array(zh)[~pre], 'o', color=RAMP[3], ms=6, label='used in fit / first set')
ax[1].plot(ns[pre], np.array(zh)[pre], 's', color=ORANGE, ms=6, label='predicted before run')
ax[1].set_xscale('log'); ax[1].set_xlabel('photons per cell n'); ax[1].set_ylabel('z_E (mean-field half-collapse) / L_NL')
ax[1].set_title('sqrt(n) (ballistic) then ln n (chaotic)', color=INK, fontsize=9.5, loc='left')
ax[1].legend(frameon=False, fontsize=7.5, loc='upper left')
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_scrambling.png'), dpi=150, facecolor=SURF)
print('saved')
