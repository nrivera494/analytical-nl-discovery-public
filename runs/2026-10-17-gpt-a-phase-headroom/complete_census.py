#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Complete the same frozen leading-pulse census on length and TL controls."""
from postprocess import *

path=HERE/'readout_checks.json'
data=json.loads(path.read_text())
for label,item in data['cases'].items():
    needed=label.startswith('train_TL_') or label.endswith(('_length6','_length6_TL'))
    if needed and 'census' not in item:
        item.update(readout_checks(label,census=True,refine_checks=False))
        path.write_text(json.dumps(data,indent=2)+'\n')
        print(label,item['reddest_resolved_soliton_is_tallest'],flush=True)
