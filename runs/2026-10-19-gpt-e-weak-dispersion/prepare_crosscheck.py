"""gpt-e / gpt-6-astra / gpt. Export own readouts for an independent solver."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;DATA=Path('~/analytical-nl-discovery-data')
for runname,filename,phi,dispersion in [
    ('2026-10-19-gpt-e-weak-dispersion','phi7.0_y0.0001_p2_n1024_w12.0_s32_c0.0_o4_gaussian.npz',7.,1e-4/7),
    ('2026-10-19-gpt-e-strong-dispersion','N20.0_Z0.9_n1024_w24.0_s689_c0.0_o4.npz',18.,.9/20)]:
    source=DATA/runname/filename
    if not source.exists():source=DATA/runname/filename.replace('_gaussian','')
    z=np.load(source);n=len(z['t']);m=z['modes']
    q=m[:n,:2]+1j*m[n:,:2]
    rows=json.loads((HERE.parent/runname/'main.json').read_text())
    row=next(r for r in rows if (r.get('phi')==phi and (r.get('y')==1e-4 or r.get('Z')==.9)))
    np.savez(DATA/runname/'crosscheck.npz',t=z['t'],initial=np.exp(-z['t']**2/2),mean=z['mean'],
        readouts=q,variances=np.array([row['lambda_min'],row['lambda_2']]),phi=np.array([phi]),dispersion=np.array([dispersion]))
