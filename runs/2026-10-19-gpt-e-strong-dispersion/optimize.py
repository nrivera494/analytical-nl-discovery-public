"""gpt-e / gpt-6-astra / gpt. Seek a passive-readout ordering counterexample."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json
from pathlib import Path
from scipy.optimize import minimize_scalar
from run import case
HERE=Path(__file__).resolve().parent;rows=[]
def objective(z):
    r=case(10.,float(z),n=512,compute_C=False);rows.append(r)
    return r['pass_vs_second']
result=minimize_scalar(objective,bounds=(.5,2.4),method='bounded',options=dict(maxiter=9,xatol=.03))
out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',bounds_Z=[.5,2.4],N=10.,
    objective='lambda_pass/lambda_2-1: seek a negative ordering violation',
    optimizer_success=bool(result.success),message=result.message,Z=float(result.x),
    minimum_relative_gap=float(result.fun),evaluations=rows)
(HERE/'optimization.json').write_text(json.dumps(out,indent=2)+'\n')
