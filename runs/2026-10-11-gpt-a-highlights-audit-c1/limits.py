"""Independent Gaussian Hamiltonian small-Z check; gpt-a, gpt-6-astra, gpt."""
import json,time
from pathlib import Path
import numpy as np
from audit import Map,PROVENANCE
out=dict(provenance=PROVENANCE,rows=[])
for N in (20,80):
 for Z in (.01,.02,.04):
  start=time.time();m=Map(N,Z,nt=1024,window=24,phase_step=.001,dispersion_step=.25)
  E0=np.sum(abs(m.u0)**2);K=np.sum(abs(m.u0)**4-abs(m.u)**4)/E0
  expected=2/(3*np.sqrt(3))+1/(2*np.sqrt(2)*N*N)
  out['rows'].append(dict(N=N,Z=Z,K=float(K),K_over_Z_squared=float(K/Z**2),predicted_small_Z_finite_N=float(expected),relative_remainder=float(K/Z**2/expected-1),wall_seconds=time.time()-start))
Path(__file__).with_name('limits.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
