"""Mechanical checks of predictions.md G1-G4 -> summary.txt, summary.json."""
import json, numpy as np
g1 = json.load(open('single_mode_mixed_kerr.json'))['results']; mm = json.load(open('twa_multimode_check.json'))['results']; th = json.load(open('thresholds.json'))
C = {}
def chk(n, ok, d): C[n] = dict(pass_=bool(ok), detail=d)
coh = [r for r in g1 if r['input'] == 'coherent']
chk('G1a', all(abs(r['twa_best_dB'] - 10*np.log10(0.945*r['n0']**(-1/3))) <= 0.3 for r in coh), '; '.join(f"n0 {r['n0']:.0e}: {r['twa_best_dB']:.2f} dB vs {10*np.log10(0.945*r['n0']**(-1/3)):.2f}" for r in coh))
for n0 in (1e8, 1e10):
    mix = [r for r in g1 if r['input'] != 'coherent' and r['n0'] == n0]
    k = sum(abs(r['twa_minus_formula_dB']) <= 1 for r in mix)
    chk(f'G1b_n0{n0:.0e}', k == len(mix), f"{k}/{len(mix)} within 1 dB; deviations {[round(r['twa_minus_formula_dB'], 2) for r in mix]}")
    sub = [r for r in mix if r['VP_below_Vstar']]; k = sum(abs(r['twa_minus_closed_dB']) <= 1.5 for r in sub)
    chk(f'G1c_n0{n0:.0e}', k == len(sub), f"{k}/{len(sub)} within 1.5 dB (inputs with V_P < V*); deviations {[round(r['twa_minus_closed_dB'], 2) for r in sub]}")
for n in (1e6, 1e10):
    rs = [r for r in mm if r['n'] == n]
    a = [r for r in rs if r['crit_G2'] < 0.8]; b = [r for r in rs if r['crit_G2'] > 8]
    chk(f'G2a_n{n:.0e}', all(abs(r['twa_u_dB'] - r['lam_lin_dB']) <= 1 for r in a), '; '.join(f"z={r['z']}: TWA {r['twa_u_dB']:.1f} vs lin {r['lam_lin_dB']:.1f}" for r in a))
    chk(f'G2b_n{n:.0e}', all(r['twa_u_dB'] - r['lam_lin_dB'] > 3 for r in b), '; '.join(f"z={r['z']}: TWA {r['twa_u_dB']:.1f} vs lin {r['lam_lin_dB']:.1f}" for r in b))
    a = [r for r in rs if r['crit_G3'] < 0.8]; b = [r for r in rs if r['crit_G3'] > 8]
    chk(f'G3a_n{n:.0e}', all(abs(r['twa_gen_num_dB'] - r['lam_gen_lin_dB']) <= 1 for r in a), '; '.join(f"z={r['z']}: TWA {r['twa_gen_num_dB']:.1f} vs lin {r['lam_gen_lin_dB']:.1f}" for r in a))
    if b: chk(f'G3b_n{n:.0e}', all(r['twa_gen_num_dB'] - r['lam_gen_lin_dB'] > 3 for r in b), '; '.join(f"z={r['z']}: TWA photon-number {r['twa_gen_num_dB']:.1f} vs lin {r['lam_gen_lin_dB']:.1f} (criterion {r['crit_G3']:.3g}; quadrature version {r['twa_gen_quad_dB']:.1f})" for r in b))
d = th['own_Q-dis_E0.3_s0.3']
chk('G4', all(d[str(z)]['n0star_max'] < 1e9 for z in (5, 10, 20, 50)), '; '.join(f"z={z}: max n0* {d[str(z)]['n0star_max']:.2g} (median {d[str(z)]['n0star_median']:.2g})" for z in (5, 10, 20, 50)))
json.dump(C, open('summary.json', 'w'), indent=1)
lines = [f"{k}: {'PASS' if c['pass_'] else 'FAIL'} | {c['detail']}" for k, c in C.items()]
lines.append("Observation (not predicted): the photon-number estimate of lambda_gen agrees with the linearized value within 0.5 dB at every z <= 100 for n = 1e6 and 1e10, while the linear-quadrature version fails: photon numbers are insensitive to the phase curvature of the crescent.")
open('summary.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
