"""gpt-e / gpt-6-astra / gpt. Adversarial search for a vanishing Theta prefactor."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution
from reduced import covariance
HERE=Path(__file__).resolve().parent;rows=[]
def objective(x):
    Gamma,tau=x
    result=covariance(Gamma=float(Gamma),last=float(tau),launch='unchirped',cells=128,modes=8)
    r=result['rows'][-1]
    score=np.exp(2*r['tau']/3)*r['phase_energy_deficit']
    rows.append(dict(Gamma=float(Gamma),tau=float(r['tau']),scaled_deficit=float(score),
        scaled_spectral_ratio=float(np.exp(2*r['tau']/3)*r['spectral_ratio'])))
    return score
result=differential_evolution(objective,bounds=[(.5,10.),(12.,18.)],seed=191010,popsize=4,
    maxiter=3,polish=False,workers=1,updating='immediate')
out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',seed=191010,
    bounds=[[.5,10.],[12.,18.]],objective='minimize G^(2/3)*(1-r^2), seeking failure of a positive Theta prefactor',
    optimizer_success=bool(result.success),message=result.message,minimum_scaled_deficit=float(result.fun),
    location=result.x.tolist(),evaluations=rows)
(HERE/'optimization.json').write_text(json.dumps(out,indent=2)+'\n')
