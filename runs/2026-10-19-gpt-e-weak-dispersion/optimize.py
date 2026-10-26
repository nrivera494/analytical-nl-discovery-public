"""gpt-e / gpt-6-astra / gpt. Bounded search for largest coefficient discrepancy."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json
from pathlib import Path
from scipy.optimize import minimize_scalar
from run import case
HERE=Path(__file__).resolve().parent;rows=[]
def objective(phi):
    r=case(float(phi),.01);rows.append(r)
    # Card's approximate second coefficient c2~=1, at the top of its y interval.
    return -abs(r['ratio']/1.1-1)
result=minimize_scalar(objective,bounds=(2.,40.),method='bounded',options=dict(maxiter=12,xatol=.02))
out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',bounds=[2.,40.],y=.01,
    objective='negative absolute excess discrepancy from leading*(1+sqrt(y))',
    optimizer_success=bool(result.success),message=result.message,phi=float(result.x),
    maximum_discrepancy=float(-result.fun),evaluations=rows)
(HERE/'optimization.json').write_text(json.dumps(out,indent=2)+'\n')
