"""Gain-bandwidth baseline and full-field convergence; gpt-a, gpt-6-astra, gpt."""
import json,gc
from pathlib import Path
from gain import run,PROVENANCE
out=dict(provenance=PROVENANCE,rows=[])
cases=[dict(case='asym',eps=.05,U=4.,edge='e23'),
       dict(case='heldout',eps=.05,U=2.,edge='e23',refine=2)]
for case in cases:
    r=run(**case);out['rows'].append(r)
    Path(__file__).with_name('convergence.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:r[k] for k in ['case','eps','gL','steps','nt','compressed_input','compressed_ASE','wall_seconds']}),flush=True)
    gc.collect()
