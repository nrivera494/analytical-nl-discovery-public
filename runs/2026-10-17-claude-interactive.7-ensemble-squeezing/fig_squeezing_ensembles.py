"""Figure fig_squeezing_ensembles.png: the condensate's own squeezing and lambda_best(n0 = 1e10) against z for each ensemble
(one thin line per realization, bold = ensemble mean), with the reference realization (phase_seed 1, dis_seed 7) dashed."""
import json, numpy as np, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(here, 'ensemble_squeezing.jsonl'))]
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
COL = {('Q-dis', 0.3): '#2a78d6', ('Q-launch', 0.3): '#86b6ef', ('Q-dis', 0.6): '#eb6834', ('Q-launch', 0.6): '#f2a37f', ('Q-strong1', 0.3): '#2f9e6b', ('Q-strong3', 0.3): '#0d366b'}
REF_OWN = [-4.91, -5.74, -5.69, -7.91, -5.79, -5.59, -1.38, 6.97]; REF_LAM = [None, None, None, -22.2, -16.9, -11.4, -4.5, 4.5]
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.2), facecolor=SURF)
for (ens, Ep), c in COL.items():
    base = ens[:-1] if ens.startswith('Q-strong') else ens; sig = {'Q-strong1': 1.0, 'Q-strong3': 3.0}.get(ens, 0.3)
    g = [r for r in rows if r['ens'] == base and abs(r['Ep'] - Ep) < 1e-9 and r['sigma'] == sig]
    if not g: continue
    z = [x['z'] for x in g[0]['records']]
    for k, ax in [('own_dB', axs[0]), ('lam_best_1e10_dB', axs[1])]:
        Y = np.array([[x[k] for x in r['records']] for r in g])
        for y in Y: ax.plot(z, y, color=c, lw=0.4, alpha=0.45)
        lab = f"{base} E'={Ep}" + (f" σ={sig}" if sig != 0.3 else '') + f" (n={len(g)})"
        ax.plot(z, Y.mean(0), color=c, lw=2, label=lab)
axs[0].plot([1, 2, 5, 10, 20, 50, 100, 200], REF_OWN, color=INK, lw=1, ls='--', label='reference realization (E\'=0.3)')
axs[1].plot([10, 20, 50, 100, 200], REF_LAM[3:], color=INK, lw=1, ls='--', label='reference realization (E\'=0.3)')
for ax, yl, t in [(axs[0], 'condensate min quadrature (dB, vacuum = 0)', "condensate's own squeezing after the thermalization fibre"),
                  (axs[1], 'best after a single-mode Kerr stage, n0 = 1e10 (dB)', 'subsequent single-mode Kerr stage (with crescent curvature)')]:
    ax.axhline(0, color=INK2, lw=0.8); ax.set_xscale('log'); ax.set_xlabel('z / L_NL'); ax.set_ylabel(yl); ax.set_title(t, fontsize=9, loc='left', color=INK)
    ax.set_facecolor(SURF); ax.grid(True, color=GRID, lw=0.5); ax.spines[['top', 'right']].set_visible(False)
axs[0].legend(frameon=False, fontsize=6.5); axs[0].set_ylim(-16, 30); axs[1].set_ylim(-36, 30)
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_squeezing_ensembles.png'), dpi=130, facecolor=SURF); print('wrote fig_squeezing_ensembles.png')
