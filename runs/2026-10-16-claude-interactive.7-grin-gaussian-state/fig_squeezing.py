"""Figure: linearized (pre-scrambling) state of the thermalizing GRIN field: multimode squeezing, photon-counting bound
lambda_gen, and the fundamental's own best quadrature, vs z (weak disorder sigma = 0.3)."""
import json, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
COLS = {0.3: '#2a78d6', 0.6: '#eb6834', 0.9: '#1baf7a'}; MK = {0.3: 'o', 0.6: 's', 0.9: '^'}
d = json.load(open(os.path.join(here, 'summary.json')))
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, ax = plt.subplots(1, 3, figsize=(10.0, 3.3), facecolor=SURF)
keys = [('multimode_min_quad_dB', 'best multimode quadrature (dB)', 'Multimode squeezing'),
        ('lambda_gen_dB', 'best weighted photon count, Fano (dB)', 'Mode-resolved photon counting'),
        ('condensate_min_quad_dB', 'fundamental alone, best quadrature (dB)', 'Self-cleaned fundamental alone')]
for a, (k, yl, t) in zip(ax, keys):
    a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.6); a.spines[['top', 'right']].set_visible(False)
    a.axhline(0, color=INK2, lw=0.8)
    for c in d['cases']:
        if c['sigma'] != 0.3: continue
        z = [r['z'] for r in c['records']]; v = [r[k] for r in c['records']]
        a.plot(z, v, color=COLS[c['Eprime']], lw=1.5, marker=MK[c['Eprime']], ms=4.5, label=f"E'={c['Eprime']} (f0 = {dict([(0.3,'0.87'),(0.6,'0.74'),(0.9,'0.61')])[c['Eprime']]})")
    a.set_xscale('log'); a.set_xlabel('z / L_NL'); a.set_ylabel(yl); a.set_title(t, color=INK, fontsize=9.5, loc='left')
ax[2].set_ylim(-15, 25)
ax[1].legend(frameon=False, fontsize=7.5, loc='lower left')
fig.text(0.01, -0.02, 'Linearized Gaussian state, exact GRIN Kerr tensor (K = 5), weak intra-group disorder, ideal (no loss, no Raman). 0 dB = shot noise / vacuum. Fundamental panel clipped at +25 dB.',
         fontsize=7, color=INK2)
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_squeezing.png'), dpi=150, facecolor=SURF, bbox_inches='tight'); print('saved')
