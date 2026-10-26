"""Convergence follow-up: gpt-a, gpt-6-astra, gpt. No proposer imports."""
import json,time,gc
from pathlib import Path
from audit import Map,PROVENANCE
out=dict(provenance=PROVENANCE,rows=[])
cases=[dict(N=N,Z=Z,nt=2048,phase_step=.025) for Z in [.01,.02,.04,.08,.16] for N in [400,800]]
cases += [dict(N=N,Z=Z,nt=2048,phase_step=.0125) for Z in [.5,1.5] for N in [12,20,32,48]]
cases += [dict(N=192,Z=Z,nt=4096,phase_step=.04) for Z in [.5,1.5]]
for case in cases:
 start=time.time();m=Map(**case,dispersion_step=.25)
 r=m.reduced() if case['N']>=192 else m.diagnostics()
 r.update(case);r['wall_seconds']=time.time()-start
 out['rows'].append(r);Path(__file__).with_name('refined.json').write_text(json.dumps(out,indent=2));print(json.dumps(r),flush=True)
 del m;gc.collect()
