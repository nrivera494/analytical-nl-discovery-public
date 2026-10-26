"""Fits, exponents, summary.json and fig_summary.png (claude-interactive.12).

Usage: python analyse.py <raw_dir>
"""
import json
import os
import sys

import numpy as np

RAW = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))


def load(fn):
    p = os.path.join(RAW, fn)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def c2_claim(P):
    S = np.sqrt(1 + P**2)
    return np.sqrt(6) * (45 + 81 * P**2 + 56 * P**4 + 40 * P**3 * S) / (240 * P**2 * (1 + P**2))


def A_claim(P):
    return np.sqrt(2 / 3) * P / np.sqrt(1 + P**2)


main = load('main.jsonl')
conv = load('conv.jsonl')
tight = load('tight.jsonl')  # rtol 3e-14 reruns of y <= 1e-6; they replace the rtol 1e-13 values
sech = load('sech.jsonl')
_tk = {(r['Phi'], r['y']): r for r in tight}
main_rtol13 = list(main)  # convergence variants (rtol 1e-13) are compared with these
main = [dict(_tk[(r['Phi'], r['y'])], tag=r['tag'], rtol_replaced=r['rtol'])
        if r['tag'] == 'main' and (r['Phi'], r['y']) in _tk else r for r in main]
deriv = json.load(open(os.path.join(HERE, 'derive_c2.json')))
HELD = {1.0: True, 1.5: True, 3.0: False, 7.0: True}
FROZEN = {1.0: 1.21744000, 1.5: 1.05254743, 7.0: 0.98098336, 3.0: 0.98946456}

summary = {'run_id': os.path.basename(HERE), 'frozen_c2': {str(k): v for k, v in FROZEN.items()},
           'derivation': {'c2_r_form': deriv['c2_r'], 'kappa_star': deriv['kappa_star_r'],
                          'symbolic_identity_residual': deriv['symbolic_identity_residual'],
                          'c2_limit_Phi_inf': deriv['c2_limit_Phi_inf'],
                          'values': {k: {kk: v[kk] for kk in ('c2_derived', 'c2_claim', 'abs_diff', 'A_derived')}
                                     for k, v in deriv['values'].items()}},
           'per_phi': {}}

fits_for_plot = {}
for P in [1.0, 1.5, 3.0, 7.0]:
    rows = sorted([r for r in main if r['Phi'] == P and r['tag'] in ('main', 'main-small')], key=lambda r: -r['y'])
    y = np.array([r['y'] for r in rows])
    ce = np.array([r['c_eff'] for r in rows])
    rel = np.array([r['rel_excess'] for r in rows])
    sy = np.sqrt(y)
    core = (y >= 1e-7) & (y <= 1e-4)
    # fit 1: c + d sqrt(y) + e y over 1e-7..1e-4 (10 points)
    X = np.vstack([np.ones(core.sum()), sy[core], y[core]]).T
    q_c, q_d, q_e = np.linalg.lstsq(X, ce[core], rcond=None)[0]
    # fit 2: c + d sqrt(y) over 1e-7..1e-5 (6 points)
    sm = (y >= 1e-7) & (y <= 1e-5)
    l_d, l_c = np.polyfit(sy[sm], ce[sm], 1)
    # fit 3: c + d sqrt(y) + e y over 2e-7..2e-5 (subset, drops ends)
    mid = (y >= 2e-7) & (y <= 2e-5)
    Xm = np.vstack([np.ones(mid.sum()), sy[mid], y[mid]]).T
    m_c = np.linalg.lstsq(Xm, ce[mid], rcond=None)[0][0]
    ests = [q_c, l_c, m_c]
    c2p = c2_claim(P)
    # exponents: leading excess vs y; remainder after the c2 term vs y
    lead_exp = np.polyfit(np.log(y[core]), np.log(rel[core]), 1)[0]
    R = (ce - c2p) * sy  # = rel/(A sqrt y) - 1 - c2 sqrt y ; claim: O(y)
    rem_exp = np.polyfit(np.log(y[core]), np.log(np.abs(R[core])), 1)[0]
    # local slope of c_eff in sqrt(y) between the two largest and two smallest core y
    summary['per_phi'][str(P)] = {
        'held_out': HELD[P], 'c2_frozen': FROZEN[P], 'c2_closed_form': float(c2p), 'A': float(A_claim(P)),
        'c2_extrap_quadratic_1e-7_1e-4': float(q_c), 'slope_d_quadratic': float(q_d), 'curv_e_quadratic': float(q_e),
        'c2_extrap_linear_1e-7_1e-5': float(l_c), 'slope_d_linear': float(l_d),
        'c2_extrap_quadratic_2e-7_2e-5': float(m_c),
        'c2_extrap_best': float(q_c), 'c2_extrap_spread': float(max(ests) - min(ests)),
        'extrap_minus_claim': float(q_c - c2p),
        'leading_excess_exponent_1e-7_1e-4': float(lead_exp),
        'remainder_exponent_in_y_1e-7_1e-4': float(rem_exp),
        'points': [{'y': float(a), 'c_eff': float(b), 'lam_min': r['lam_min'], 'rel_excess': float(c),
                    'N': r['N'], 'ne': r['ne'], 'X_in': r['X_in'], 'mode_rms_x': r['mode_rms_x'],
                    'sigma_pred': r['sigma_pred'], 'edge_amp_rel': r['edge_amp_rel'], 'tag': r['tag']}
                   for a, b, c, r in zip(y, ce, rel, rows)],
    }
    fits_for_plot[P] = (q_c, q_d, q_e, sy, ce, y)
    print(f'Phi={P}: extrap {q_c:.6f} (lin {l_c:.6f}, mid {m_c:.6f}) vs c2 {c2p:.6f} '
          f'[diff {q_c - c2p:+.1e}]; slope d={q_d:.3f}; lead exp {lead_exp:.5f}; remainder exp {rem_exp:.4f}')

# shape specificity: sech pulse against the c2 predicted by derive_c2.py for that profile
dsech = json.load(open(os.path.join(HERE, 'derive_c2_sech.json')))
summary['sech'] = {'c2_r_form_sech': dsech['c2_r'], 'c2_limit_Phi_inf_sech': dsech['c2_limit_Phi_inf'], 'per_phi': {}}
for P in sorted({r['Phi'] for r in sech}):
    rows = sorted([r for r in sech if r['Phi'] == P], key=lambda r: -r['y'])
    y = np.array([r['y'] for r in rows]); ce = np.array([r['c_eff'] for r in rows]); sy = np.sqrt(y)
    X = np.vstack([np.ones(len(y)), sy, y]).T
    c, d, e = np.linalg.lstsq(X, ce, rcond=None)[0]
    pred = dsech['values'][f'{P:g}']['c2_derived']
    rem_exp = np.polyfit(np.log(y), np.log(np.abs((ce - pred) * sy)), 1)[0]
    summary['sech']['per_phi'][str(P)] = {'c2_sech_predicted': pred, 'c2_gauss_closed_form': float(c2_claim(P)),
                                          'c2_extrap_quadratic': float(c), 'slope_d': float(d),
                                          'extrap_minus_pred': float(c - pred), 'remainder_exponent_in_y': float(rem_exp),
                                          'points': [{'y': float(a), 'c_eff': float(b), 'N': r['N'], 'Xw': r['Xw'],
                                                      'edge_amp_rel': r['edge_amp_rel']} for a, b, r in zip(y, ce, rows)]}
    print(f'sech Phi={P}: extrap {c:.6f} vs predicted {pred:.6f} [diff {c - pred:+.1e}] slope {d:.3f} '
          f'rem exp {rem_exp:.4f} (Gaussian c2 {c2_claim(P):.6f})')

# third shape, kappa4 = 0 (intensity exp(-x^2 - x^4/2)), prediction frozen in HELDOUT_kappa4.md (commit 76856b7)
gq = load('gq.jsonl')
dgq = json.load(open(os.path.join(HERE, 'derive_c2_gq.json')))
summary['kappa4_zero_shape'] = {'c2_r_form': dgq['c2_r'], 'c2_limit_Phi_inf': dgq['c2_limit_Phi_inf'],
                                'frozen_rule': 'c2(Phi,kappa4) = c2(Phi) - 3/(4 sqrt 6) (kappa4 - 1/2)', 'per_phi': {}}
for P in sorted({r['Phi'] for r in gq}):
    rows = sorted([r for r in gq if r['Phi'] == P], key=lambda r: -r['y'])
    y = np.array([r['y'] for r in rows]); ce = np.array([r['c_eff'] for r in rows]); sy = np.sqrt(y)
    X = np.vstack([np.ones(len(y)), sy, y]).T
    c, d, e = np.linalg.lstsq(X, ce, rcond=None)[0]
    frozen = float(c2_claim(P) + 3 / (8 * np.sqrt(6)))
    sym = dgq['values'][f'{P:g}']['c2_derived']
    summary['kappa4_zero_shape']['per_phi'][str(P)] = {'c2_frozen_prediction': frozen, 'c2_symbolic': sym,
                                                       'c2_extrap_quadratic': float(c), 'slope_d': float(d),
                                                       'extrap_minus_frozen': float(c - frozen),
                                                       'points': [{'y': float(a), 'c_eff': float(b)} for a, b in zip(y, ce)]}
    print(f'kappa4=0 Phi={P}: extrap {c:.6f} vs frozen {frozen:.6f} (symbolic {sym:.6f}) [diff {c - frozen:+.1e}] slope {d:.3f}')

# non-uniformity as Phi -> 0: Phi = 0.5, 0.25 (rtol 3e-14), fit as for the main cases
smallphi = load('smallphi.jsonl')
summary['small_phi'] = {}
for P in sorted({r['Phi'] for r in smallphi}):
    rows = sorted([r for r in smallphi if r['Phi'] == P], key=lambda r: -r['y'])
    y = np.array([r['y'] for r in rows]); ce = np.array([r['c_eff'] for r in rows]); sy = np.sqrt(y)
    X = np.vstack([np.ones(len(y)), sy, y]).T
    c, d, e = np.linalg.lstsq(X, ce, rcond=None)[0]
    sm = y <= 1e-5
    c_lin = np.polyfit(sy[sm], ce[sm], 1)[1]
    c2p = c2_claim(P)
    rem_exp = np.polyfit(np.log(y), np.log(np.abs((ce - c2p) * sy)), 1)[0]
    summary['small_phi'][str(P)] = {'c2_closed_form': float(c2p), 'c2_extrap_quadratic': float(c),
                                    'c2_extrap_linear_1e-7_1e-5': float(c_lin), 'slope_d': float(d), 'curv_e': float(e),
                                    'extrap_minus_claim': float(c - c2p), 'remainder_exponent_in_y': float(rem_exp),
                                    'sqrt_y_over_Phi2_at_1e-4': float(1e-2 / P**2),
                                    'points': [{'y': float(a), 'c_eff': float(b)} for a, b in zip(y, ce)]}
    print(f'small Phi={P}: extrap {c:.5f} (lin {c_lin:.5f}) vs c2 {c2p:.5f} [diff {c - c2p:+.1e}] slope {d:.2f} '
          f'curv {e:.0f} rem exp {rem_exp:.3f}')

# extra points at the source's table values
summary['source_table_points'] = [{'Phi': r['Phi'], 'y': r['y'], 'c_eff': r['c_eff'], 'c2_closed_form': float(c2_claim(r['Phi']))}
                                  for r in main if r['tag'] == 'source-table']

# convergence table: spread of c_eff and lam over variants, per (Phi, y)
convsum = {}
for r in conv:
    key = f"Phi={r['Phi']},y={r['y']:g}"
    base = [m for m in main_rtol13 if m['Phi'] == r['Phi'] and m['y'] == r['y'] and m['tag'] == 'main']
    if not base:
        continue
    b = base[0]
    convsum.setdefault(key, {'base_lam': b['lam_min'], 'base_c_eff': b['c_eff'], 'variants': {}})
    tag = r['tag'] + (f"-{r['nsteps']}" if r['tag'] == 'rk4ip' else '')
    convsum[key]['variants'][tag] = {'lam_rel_diff': r['lam_min'] / b['lam_min'] - 1,
                                     'c_eff_diff': r['c_eff'] - b['c_eff'], 'edge_amp_rel': r['edge_amp_rel'],
                                     'N': r['N'], 'Xw': r['Xw'], 'ne': r['ne']}
# Richardson for RK4IP pairs
for key, v in convsum.items():
    va = v['variants']
    if 'rk4ip-1000' in va and 'rk4ip-2000' in va:
        b = v['base_lam']
        l1 = b * (1 + va['rk4ip-1000']['lam_rel_diff'])
        l2 = b * (1 + va['rk4ip-2000']['lam_rel_diff'])
        lr = l2 + (l2 - l1) / 15
        v['rk4ip_richardson_lam_rel_diff_vs_dop853'] = lr / b - 1
summary['convergence'] = convsum
for key, v in convsum.items():
    worst = max((abs(x['c_eff_diff']), t) for t, x in v['variants'].items())
    print(key, 'max |c_eff diff| over variants:', f'{worst[0]:.1e} ({worst[1]})',
          'RK4IP-Richardson rel:', v.get('rk4ip_richardson_lam_rel_diff_vs_dop853'))
json.dump(summary, open(os.path.join(HERE, 'summary.json'), 'w'), indent=1)

# ------------------------------------------------------------------ figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INK, MUTED, BLUE = '#1f1f1e', '#6b6a64', '#2a78d6'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False})
fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.4))
for ax, P in zip(axs.ravel(), [3.0, 1.0, 1.5, 7.0]):
    q_c, q_d, q_e, sy, ce, y = fits_for_plot[P]
    c2p = c2_claim(P)
    held = HELD[P]
    ss = np.linspace(0, 0.0105, 200)
    ax.plot(ss * 1e3, q_c + q_d * ss + q_e * ss**2, color=BLUE, lw=1.2, alpha=0.6, zorder=1)
    ax.plot(sy * 1e3, ce, 'o', ms=6, mec=BLUE, mew=1.5, mfc='white' if held else BLUE, zorder=3)
    ax.plot([0], [c2p], marker='_', ms=22, mew=2.5, color=INK, zorder=4, clip_on=False)
    ax.axhline(c2p, color=INK, lw=0.6, ls=':', zorder=0)
    ax.text(0.03, 0.05, f'claimed $c_2$ = {c2p:.6f}' + (' (frozen)' if held else '') +
            f'\nextrapolated  {q_c:.6f}\nslope in $\\sqrt{{y}}$: {q_d:.2f}',
            transform=ax.transAxes, fontsize=8, color=INK, va='bottom', ha='left', linespacing=1.4)
    ax.set_title(f'$\\Phi$ = {P:g}' + ('  (held out, frozen before computing)' if held else '  (source table)'),
                 fontsize=9, color=INK, loc='left')
    ax.set_xlim(-0.3, 10.5)
    lo = min(ce.min(), c2p)
    hi = max(ce.max(), c2p)
    pad = 0.12 * (hi - lo)
    ax.set_ylim(lo - pad, hi + 2.2 * pad)
    ax.grid(True, color='#e6e5df', lw=0.6)
    ax.set_axisbelow(True)
for ax in axs[1]:
    ax.set_xlabel(r'$\sqrt{y}\ \times 10^3$   ($y = \Phi L/L_D$, from $10^{-7}$ to $10^{-4}$)')
for ax in axs[:, 0]:
    ax.set_ylabel(r'$c_{\rm eff}(y)$')
fig.suptitle(r'Weak normal dispersion, Gaussian pulse: $c_{\rm eff}=[(\lambda_{\min}/\lambda_0-1)/(A\sqrt{y})-1]/\sqrt{y}\to c_2(\Phi)$ as $y\to0$'
             '\nfull mean + tangent propagation (claude-interactive.12), $10^{-7}\\leq y\\leq10^{-4}$'
             '\nbar at $\\sqrt{y}=0$: claimed $c_2$;  line: fit $c+d\\sqrt{y}+ey$;  open symbols: held-out $\\Phi$',
             fontsize=9.5, color=INK, x=0.02, ha='left')
fig.tight_layout(rect=(0, 0, 1, 0.90))
out = os.path.join(HERE, 'fig_summary.png')
fig.savefig(out, dpi=110)
print('figure', out, os.path.getsize(out), 'bytes')
