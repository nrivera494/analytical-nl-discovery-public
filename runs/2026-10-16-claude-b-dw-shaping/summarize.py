"""Collect the shaping-run numbers into summary.json (run 2026-10-16-claude-b-dw-shaping)."""
import json, glob, re, os
S = dict(run_id='2026-10-16-claude-b-dw-shaping', agent='claude-b', model='claude-opus-5-5', family='claude', optimisations={}, logs_only={})
for f in sorted(glob.glob('opt_*.json')):
    J = json.load(open(f))
    S['optimisations'][f] = dict(N=J['N'], d3=J['d3'], xif=J['xif'], objective=J.get('objective', 'band'), maxiter=J.get('maxiter', 60), Nt=J['Nt'], TW=J['TW'], h=J['h'],
        eta_TL=J['eta_TL'], eta_TL_h2=J['eta_TL_h2'], H_gdd=J['gdd']['H_gdd'], C_best=J['gdd']['C_best'], H_phase=J['H_phase'], eta_phase=J['eta_phase'],
        phase_starts={k: dict(H=v['H'], nit=v['nit'], gradnorm=v['gradnorm']) for k, v in J['phase'].items()}, H_passive=J['H_passive'],
        passive_energy_kept=J['passive']['energy_kept'], best_phase_diag={k: v for k, v in J['best_phase_diag'].items() if k not in ('eta_xi', 'etaTL_xi')},
        eta_xi_best=J['best_phase_diag']['eta_xi'], eta_xi_TL=J['best_phase_diag']['etaTL_xi'])
# per-start results of runs that were stopped or have not finished (from their logs)
for f in sorted(glob.glob('opt_*.log')):
    lines = [l.strip() for l in open(f) if l.startswith('N')]
    S['logs_only'][f] = lines
for pat in ['long_*.json', 'where_*.json', 'h4c_*.json', 'window_check.json', 'transfer_*.json']:
    for f in sorted(glob.glob(pat)):
        S[f] = json.load(open(f))
json.dump(S, open('summary.json', 'w'), indent=1, default=float)
print('written; optimisations:', list(S['optimisations']))
