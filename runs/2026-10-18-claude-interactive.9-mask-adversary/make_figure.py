"""Summary figure: relative gain over TL of the leading ZS eigenvalue vs N. Ceilings (C)-(E) as curves,
TL as the zero line, adversarially optimised passive masks as points (open = held-out cases)."""
import glob, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import gammaln
from scipy.optimize import minimize_scalar
sys.path.insert(0, '../2026-10-18-claude-interactive.9-zs-solver-validation')
from zs import grid, fc_eigs, logC

cases = []
for f in sorted(glob.glob('part_*.json')) + (['summary.json'] if glob.os.path.exists('summary.json') else []):
    cases += json.load(open(f))['cases']
by = {}
for c in cases:
    by[c['name']] = c          # later files override earlier ones
cases = list(by.values())


def sech_ceiling_rel(N):
    best = np.inf
    for n in range(1, 200):
        p = 2 * n
        logI = p * np.log(N) + 0.5 * np.log(np.pi) + gammaln(p / 2) - gammaln((p + 1) / 2)
        best = min(best, np.exp((logI - logC(p)) / (p - 1)))
    return best / (N - 0.5) - 1


def gauss_U(N):
    f = lambda p: (p * np.log(N) + 0.5 * np.log(2 * np.pi / p) - logC(p)) / (p - 1)
    ps = np.linspace(2.0, 80.0, 3901)
    j = int(np.argmin([f(p) for p in ps]))
    r = minimize_scalar(f, bracket=(ps[max(j - 1, 0)] + 1e-9, ps[j], ps[j + 1]), tol=1e-14)
    return float(np.exp(r.fun))


Ns = np.linspace(1.0, 10.0, 721)
sech_c = np.array([sech_ceiling_rel(N) for N in Ns])
Ng = np.linspace(1.25, 10.0, 36)
g_tl = []
for N in Ng:
    t, k = grid(256, 40.0)
    w = fc_eigs(N * np.exp(-t ** 2 / 2) + 0j, 40.0, imag_min=0.05)
    w = [z for z in w if abs(z.real) < 0.6 * np.pi * 256 / 40.0]
    g_tl.append(w[0].imag)
g_c = np.array([gauss_U(N) for N in Ng]) / np.array(g_tl) - 1
json.dump({"sech_N": Ns.tolist(), "sech_ceiling_rel": sech_c.tolist(), "gauss_N": Ng.tolist(),
           "gauss_TL_eta_fc256": g_tl, "gauss_ceiling_rel": g_c.tolist()}, open('figure_curves.json', 'w'))

fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=110)
c_sech, c_g = '#1f5fa8', '#c2571a'
ax.plot(Ns, 100 * sech_c, color=c_sech, lw=1.6, label='ceiling (C)/(D), sech laser')
ax.plot(Ng, 100 * g_c, color=c_g, lw=1.6, ls='--', label='ceiling (E), Gaussian laser')
ax.axhline(0, color='0.25', lw=1.0, label='transform-limited launch')
for c in cases:
    col = c_sech if c['kind'] == 'sech' else c_g
    mk = 'o' if c['kind'] == 'sech' else 's'
    y = 100 * c['best_verified_rel_gain_over_TL']
    held = c['held_out'] and not (c['kind'] == 'gauss' and c['N'] == 1.5)   # Gaussian N = 1.5 is in the source's README table
    ax.plot(c['N'], y, mk, ms=7, mfc='white' if held else col, mec=col, mew=1.6, zorder=5)
ax.plot([], [], 'o', color='0.3', ms=7, label='best of 13 adversarial passive-mask searches')
ax.plot([], [], 'o', mfc='white', mec='0.3', ms=7, mew=1.6, label='same, held-out case')
ax.plot([], [], 's', mfc='0.3', mec='0.3', ms=6, label='(circles: sech; squares: Gaussian)')
ax.set_xlabel(r'soliton number $N$ of the transform-limited laser')
ax.set_ylabel(r'gain in $\eta_{\max}$ over TL (%)')
ax.set_xlim(1.4, 10.1)
ax.set_ylim(-0.025, 0.5)
ax.legend(fontsize=7.6, frameon=False, loc='upper right')
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig('fig_summary.png', dpi=110)
print('max |gain| of verified best masks:', max(abs(c['best_verified_rel_gain_over_TL']) for c in cases))
