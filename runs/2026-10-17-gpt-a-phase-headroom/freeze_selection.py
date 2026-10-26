#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Create the reviewable coefficient manifest before selected-mask holdouts."""
from independent import *
import hashlib,datetime

if __name__=='__main__':
    selection=json.loads((HERE/'training_selection.json').read_text())
    if set(selection['best'])!={'3','4','5'}:raise RuntimeError('A training candidate is missing')
    masks={}
    for key,item in selection['best'].items():
        path=HERE/f'selected_N{key}_coef.csv';c=coefficients(item['mask'])
        np.savetxt(path,c,delimiter=',',header=f"agent: gpt-a; model: gpt-6-astra; family: gpt\nN={key}; T0={item['T0_fs']} fs; Legendre orders 2-31; standard FFT; cutoff 2*pi\nSource: {item['optimizer']}; selection uses training data only")
        masks[key]=dict(N=int(key),T0_fs=item['T0_fs'],coefficient_file=path.name,
                        coefficient_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        source_optimizer=item['optimizer'],training_f_zs=item['training_f_zs'],training_H=item['training_H'],
                        optimizer_raw_gradient=item['training']['optimizer_best_gradient_norm'],
                        leading_identity_checked_on_training_only=item.get('leading_identity_checked_on_training_only',False),
                        stationarity_preference_satisfied=item['stationarity_preference_satisfied'])
    manifest=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=HERE.name,
                  frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  selection_information='Training cases and training-only gradient checks; no selected-mask held-out output.',
                  phase='sum c_m P_m(clip(k/(2*pi),-1,1)), m=2,...,31; standard FFT; fixed physical frequency in duration tests',
                  masks=masks)
    (HERE/'selected_masks.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))
