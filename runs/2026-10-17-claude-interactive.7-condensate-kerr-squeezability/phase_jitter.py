"""Condensate phase spread across shots, Var(phi_0) = -ln coh_0, from runs/2026-10-16-claude-interactive.7-grin-shot-statistics/shot_stats.json
(15 GRIN modes, E' = 0.6, sigma = 0.3, 128 shots): quiet laser at n = 1e10, and 1% RMS common-mode amplitude jitter. Compared with the
linearized prediction V_P/(4 n0) from cond_kerr.json (same launch and disorder strength; dz differs, 0.05 vs 0.02). Output: phase_jitter.txt."""
import json, numpy as np
d = json.load(open('../2026-10-16-claude-interactive.7-grin-shot-statistics/shot_stats.json'))
ck = [c for c in json.load(open('cond_kerr.json'))['cases'] if c['Eprime'] == 0.6 and c['sigma'] == 0.3][0]
lin = {round(r['z']): r['V_P']/(4*r['f0']*1e10) for r in ck['records']}
lines = []
for r in d['records']:
    vq = -np.log(r['q1e10']['coh'][0]); vr = -np.log(r['rin1pc']['coh'][0]); z = r['z']
    lines.append(f"z={z:4d}: quiet n=1e10 Var(phi_0) = {vq:.2e} rad^2" + (f" (linearized V_P/4n0 = {lin[z]:.2e})" if z in lin else "")
                 + f" | 1% jitter: Var(phi_0) = {vr:.3e} rad^2, RMS {np.sqrt(vr):.3f} rad")
open('phase_jitter.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
