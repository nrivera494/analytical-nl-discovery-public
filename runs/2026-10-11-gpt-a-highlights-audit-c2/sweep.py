"""Independent finite-edge/gain-bandwidth checks: gpt-a, gpt-6-astra, gpt."""
import json,gc
from pathlib import Path
from gain import run,PROVENANCE
out=dict(provenance=PROVENANCE,rows=[])
cases=[dict(case='asym',eps=e,U=4.,edge=edge) for e in [.1,.025,.0125] for edge in ['e1','e23']]
cases += [dict(case='main',eps=e,U=4.,edge='e23') for e in [.1,.05,.025]]
cases += [dict(case='heldout',eps=e,U=2.,edge='e23') for e in [.05,.025]]
cases += [dict(case='asym',eps=.05,U=4.,gbw=.05,edge='e23'),dict(case='asym',eps=.05,U=.02,edge='e23')]
for case in cases:
 r=run(**case);out['rows'].append(r);Path(__file__).with_name('sweep.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:r[k] for k in ['case','eps','gL','edge','gbw','nt','steps','compressed_input','compressed_ASE','energy_error','wall_seconds']}),flush=True);gc.collect()
