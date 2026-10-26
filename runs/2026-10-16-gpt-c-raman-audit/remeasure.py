"""Re-extract stored fields, retaining failed first measurements. gpt-c/gpt-6-astra/gpt."""
import json,sys
from pathlib import Path
import numpy as np
from independent import RAW,census,write_json
for name in sys.argv[1:]:
    path=Path(name); r=json.loads(path.read_text())
    for cp in r['checkpoints']:
        data=np.load(RAW/(r['case']['id']+'_zN'+str(cp['zN'])+'.npz'))
        if 'measurement_v1' not in cp: cp['measurement_v1']={k:cp[k] for k in ['peaks','leading']}
        cp.update(census(data['t'],data['q'],r['case']))
    r['extraction_version']=2;write_json(path,r)
    print(path.name,[(c['zN'],None if c['leading'] is None else c['leading']['f_zs']) for c in r['checkpoints']],flush=True)
