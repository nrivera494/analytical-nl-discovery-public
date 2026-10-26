"""Targeted grid/step and shape checks; gpt-a, gpt-6-astra, gpt."""
import json,gc,time
from pathlib import Path
from audit import Map,PROVENANCE
cases=[dict(N=800,Z=.01,nt=4096,phase_step=.0125),
       dict(N=20,Z=1.5,nt=4096,phase_step=.00625),
       dict(N=4,Z=.7,nt=1024,shape='quartic',chirp=-2.,shift=.6,beta3=.15),
       dict(N=4,Z=.7,nt=1024,shape='sech',chirp=1.,shift=-.9,beta_sign=-1.)]
out=dict(provenance=PROVENANCE,rows=[])
for case in cases:
    start=time.time();m=Map(**case,dispersion_step=.25)
    r=m.reduced() if case['N']==800 else m.diagnostics(eigen=case['N']==20)
    r.update(case);r['wall_seconds']=time.time()-start
    out['rows'].append(r);Path(__file__).with_name('convergence.json').write_text(json.dumps(out,indent=2));print(json.dumps(r),flush=True)
    del m;gc.collect()
