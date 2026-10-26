"""Figures from thermalize_*.npz.
fig_thermalization.png: rows = runs (launch x coupling); columns = (1) group powers along z with the RJ/Dirichlet values, (2) thermalized
per-mode occupations (mean over z >= 2000) against RJ T/eps_m and the condensate value, (3) condensate fraction histogram (z >= 2000) against
the Dirichlet law, (4) pooled excited-mode powers normalized to their RJ means against the Dirichlet marginal D Beta(1, D-1).
fig_nearfield.png: near-field intensity |sum_p A_p psi_p(x, y)|^2 at z = 0, 10, 100, 1e4 and the incoherent average sum_p <I_p> psi_p^2."""
import os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from grin_overlaps import hermite_functions
here = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-grin-thermalization-visual')
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
GCOL = ['#eb6834', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b']      # group 0 (fundamental) orange; groups 1-4 blue, light -> dark
runs = [('E06', 0.3, "launch: fundamental 0.6 + groups 1, 2  |  Kerr + weak linear intra-group coupling"),
        ('E06', 0.0, "same launch  |  Kerr only"),
        ('G1', 0.3, "launch: all power in group 1 (HG10, HG01) + vacuum seed  |  Kerr + weak linear intra-group coupling"),
        ('G1', 0.0, "same launch and seed  |  Kerr only")]
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2})
fig, axs = plt.subplots(4, 4, figsize=(16.5, 13.5), facecolor=SURF, gridspec_kw=dict(width_ratios=[1.6, 1, 1, 1]))
rng = np.random.default_rng(5)
for row, (name, sig, title) in enumerate(runs):
    d = np.load(os.path.join(RAW, f'thermalize_{name}_s{sig}.npz')); z, I, groups, eps, Ep = d['z'], d['I'], d['groups'], d['eps'], float(d['Eprime'])
    M = len(groups); D = M - 1; T = Ep/D; S1 = np.sum(1/eps[1:]); K = groups.max() + 1
    late = z >= 2000
    pred_g = [1 - T*S1] + [np.sum(T/eps[groups == k]) for k in range(1, K)]
    ax = axs[row, 0]
    for k in range(K):
        gpow = I[:, groups == k].sum(1)
        ax.plot(np.maximum(z, 0.25), gpow, color=GCOL[k], lw=0.35, alpha=0.35)
        # running mean in log-spaced windows
        edges = np.logspace(np.log10(0.5), 4, 45); zc, mc = [], []
        for a, b in zip(edges[:-1], edges[1:]):
            sel = (z >= a) & (z < b)
            if sel.any(): zc.append(np.sqrt(a*b)); mc.append(gpow[sel].mean())
        ax.plot(zc, mc, color=GCOL[k], lw=1.8, label=('fundamental' if k == 0 else f'group {k}'))
        ax.axhline(pred_g[k], color=GCOL[k], lw=1.0, ls='--')
    ax.set_xscale('log'); ax.set_xlim(0.25, 1e4); ax.set_ylim(0, 1.0); ax.set_ylabel('power fraction')
    ax.set_title(title, color=INK, fontsize=9, loc='left')
    if row == 0: ax.legend(frameon=False, fontsize=7.5, loc='upper left', ncol=5)
    if row == 3: ax.set_xlabel('z / L_NL  (thin: raw; thick: windowed mean; dashed: RJ / Dirichlet)')
    # per-mode thermalized occupations
    ax = axs[row, 1]; ml = I[late].mean(0)
    jit = np.concatenate([[0]] + [np.linspace(-0.18, 0.18, (groups == k).sum()) if (groups == k).sum() > 1 else [0] for k in range(1, K)])
    order = np.argsort(groups, kind='stable')
    ax.scatter(eps[order] + jit, ml[order], s=18, color=[GCOL[g] for g in groups[order]], zorder=3, label='simulation, mean over z ≥ 2000')
    ee = np.linspace(0.8, 4.2, 50); ax.plot(ee, T/ee, color=INK2, lw=1.0, ls='--', label='RJ: T/ε, T = E\'/D')
    ax.scatter([0], [1 - T*S1], marker='_', s=300, color=INK2, lw=1.5, label='RJ condensate 1 − T S₁')
    ax.set_yscale('log'); ax.set_ylim(5e-3, 1.2); ax.set_xticks(range(K)); ax.set_xlabel('mode group k (ε = k)'); ax.set_ylabel('mean power per mode')
    if row == 0: ax.legend(frameon=False, fontsize=7, loc='upper right')
    # condensate fraction histogram vs Dirichlet
    ax = axs[row, 2]
    y = rng.exponential(size=(200000, D)); y /= y.sum(1, keepdims=True); x = Ep*y/eps[1:][None, :]; I0d = 1 - x.sum(1)
    bins = np.linspace(min(I[late, 0].min(), np.percentile(I0d, 0.1)), max(I[late, 0].max(), np.percentile(I0d, 99.9)), 45)
    ax.hist(I0d, bins=bins, density=True, color=GRID, edgecolor=INK2, lw=0.5, label='Dirichlet law')
    ax.hist(I[late, 0], bins=bins, density=True, histtype='step', color=GCOL[0], lw=1.6, label='simulation')
    ax.set_xlabel('condensate fraction I₀'); ax.set_ylabel('density')
    if row == 0: ax.legend(frameon=False, fontsize=7, loc='upper left')
    # pooled excited-mode powers normalized to RJ means vs D Beta(1, D-1)
    ax = axs[row, 3]
    s = (I[late][:, 1:]/(T/eps[1:])[None, :]).ravel()
    sb = np.linspace(0, 6, 49); ss = np.linspace(0, 6, 200)
    ax.hist(s, bins=sb, density=True, histtype='step', color=GCOL[2], lw=1.6, label='simulation, all excited modes')
    ax.plot(ss, (D - 1)/D*np.clip(1 - ss/D, 0, None)**(D - 2), color=INK2, lw=1.0, ls='--', label='Dirichlet marginal D·Beta(1, D−1)')
    ax.set_yscale('log'); ax.set_ylim(1e-3, 2); ax.set_xlabel('excited-mode power / RJ mean'); ax.set_ylabel('density')
    if np.ptp(I[late, 0]) < 1e-9:
        for a_ in (axs[row, 2], axs[row, 3]):
            a_.cla(); a_.set_xticks([]); a_.set_yticks([])
            a_.text(0.5, 0.5, 'no thermalization:\nall power stays in group 1\nfor z up to 1e4 L_NL', transform=a_.transAxes, ha='center', va='center', color=INK2, fontsize=8.5)
    if row == 0: ax.legend(frameon=False, fontsize=7, loc='upper right')
for a in axs.ravel():
    a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.5); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(here, 'fig_thermalization.png'), dpi=130, facecolor=SURF)
# near field
xs = np.linspace(-4.5, 4.5, 181); X, Y = np.meshgrid(xs, xs)
h = hermite_functions(4, xs)
fig2, axs2 = plt.subplots(2, 5, figsize=(14, 5.8), facecolor=SURF)
for row, (name, sig) in enumerate([('G1', 0.3), ('E06', 0.3)]):
    d = np.load(os.path.join(RAW, f'thermalize_{name}_s{sig}.npz')); groups = d['groups']
    modes = [(nx, k - nx) for k in range(5) for nx in range(k + 1)]
    psi = np.array([np.outer(h[ny], h[nx]) for (nx, ny) in modes])        # psi_p(y, x)
    late = d['z'] >= 2000; ml = d['I'][late].mean(0)
    frames = [(f'z = {int(zz)} L_NL', np.abs(np.tensordot(A, psi, axes=(0, 0)))**2) for zz, A in zip(d['snap_z'], d['snap_A']) if int(zz) in (0, 10, 100, 10000)]
    frames.append(('average, z ≥ 2000: Σ⟨I_p⟩ψ_p²', np.tensordot(ml, psi**2, axes=(0, 0))))
    vmax = max(f[1].max() for f in frames)
    for col, (lab, img) in enumerate(frames):
        ax = axs2[row, col]; ax.imshow(img, extent=[xs[0], xs[-1], xs[0], xs[-1]], origin='lower', cmap='magma', vmin=0, vmax=vmax)
        ax.set_title(('all power in HG10, HG01 at launch: ' if (row == 0 and col == 0) else ('fundamental 0.6 at launch: ' if (row == 1 and col == 0) else '')) + lab, fontsize=8, color=INK, loc='left')
        ax.set_xticks([]); ax.set_yticks([])
fig2.tight_layout(); fig2.savefig(os.path.join(here, 'fig_nearfield.png'), dpi=130, facecolor=SURF)
print('wrote fig_thermalization.png and fig_nearfield.png')
