"""Summarize saved bounded alternate checks; gpt-a, gpt-6-astra, gpt."""
import json
from pathlib import Path
import numpy as np

base = Path(__file__).resolve().parent
r = json.loads((base / 'results.json').read_text())['rows']
s = r[0]
out = dict(agent='gpt-a', model='gpt-6-astra', family='gpt', run_id=base.name,
           status='complete-bounded-check', scalar_F=s['best_F'], grin_F=r[1]['best_F'],
           grin_minus_scalar=r[1]['best_F']-s['best_F'],
           manakov_max_difference=float(max(abs(np.array(r[2]['hard_band_F'])-s['hard_band_F']))),
           fractional_manakov_difference=r[2]['fractional_F']-s['fractional_F'],
           asymmetric_manakov_difference=r[2]['asymmetric_F']-s['asymmetric_F'],
           refined_scalar_F=r[3]['best_F'], refined_grin_F=r[4]['best_F'],
           walkoff_0p6_F=r[-2]['best_F'], unequal_dispersion_1p02_F=r[-1]['best_F'])
out['near_manakov'] = []
for j, epsilon in enumerate([.02, .04, .08]):
    minus, plus = r[5+2*j:7+2*j]
    even = (minus['best_F']+plus['best_F'])/2-s['best_F']
    odd = (plus['best_F']-minus['best_F'])/2
    out['near_manakov'].append(dict(epsilon=epsilon, even_delta_F=even,
        odd_delta_F=odd, coefficient_over_q_squared=even/plus['q_squared']))
x = np.log([v['epsilon'] for v in out['near_manakov']])
for parity in ['even', 'odd']:
    y = np.log(abs(np.array([v[f'{parity}_delta_F'] for v in out['near_manakov']])))
    out[f'{parity}_power'] = float(np.polyfit(x, y, 1)[0])
out['max_energy_error'] = max(abs(v['energy_error']) for v in r)
out['case_wall_time_sum_s'] = sum(v['wall_seconds'] for v in r)
(base / 'summary.json').write_text(json.dumps(out, indent=2)+'\n')
