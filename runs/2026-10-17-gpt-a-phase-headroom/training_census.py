#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Confirm the leading-pulse identity using training fields before freezing."""
from postprocess import *

if __name__=='__main__':
    path=HERE/'training_selection.json';selection=json.loads(path.read_text());checks={}
    for key,item in selection['best'].items():
        candidates=[r for r in selection['candidates'] if r['N']==item['N'] and r['edge_mass']<1e-6
                    and r['alias_mass']<1e-6 and abs(r['mass_drift'])<2e-4 and r.get('root_ok')]
        candidates.sort(key=lambda r:(r['optimizer_best_gradient_norm']<=1e-5,r['f_zs_extrapolated']),reverse=True)
        chosen=None
        for row in candidates:
            result=readout_checks(row['label'],census=True);checks[row['label']]=result
            (HERE/'training_census.json').write_text(json.dumps(dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=HERE.name,cases=checks),indent=2)+'\n')
            print('TRAINING CENSUS',row['label'],result['reddest_resolved_soliton_is_tallest'],flush=True)
            if result['reddest_resolved_soliton_is_tallest']:
                chosen=row;break
        if chosen is None:raise RuntimeError(f'No leading-pulse identity qualified candidate for N={key}; do not freeze an invalid witness')
        item.update(mask=chosen['mask_source'],optimizer=chosen['optimizer'],training=chosen,
                    training_f_zs=chosen['f_zs_extrapolated'],
                    training_H=chosen['f_zs_extrapolated']/item['baseline']['f_zs_extrapolated'],
                    stationarity_preference_satisfied=bool(chosen['optimizer_best_gradient_norm']<=1e-5),
                    leading_identity_checked_on_training_only=True)
    selection['selection_uses']+='; require training-only census agreement between tallest and reddest resolved soliton above the declared 1% input-mass floor'
    path.write_text(json.dumps(selection,indent=2)+'\n')
