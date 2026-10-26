#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Complete the originally frozen QMC occupation grid."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import memory_gate,save_json
from kerr_squeezing import *
from scipy.special import ndtri
from scipy.stats import qmc
RUN=Path(__file__).resolve().parent
memory_gate();path=RUN/'twa_summary.json';data=json.loads(path.read_text())
for n in [64,1024]:
 for nu in [1,3]:
  for power in [14,16]:
   for seed in [8611,8612,8613,8614]:
    if any(r['n']==n and r['nu']==nu and r['shots']==2**power and r['seed']==seed for r in data['rows']):continue
    x=ndtri(qmc.Sobol(2,scramble=True,seed=seed).random_base2(power));a=np.sqrt(n)+(x[:,0]+1j*x[:,1])*np.sqrt(nu)/2
    for s in [n**(1/6),2*n**(1/6)]:
      b=a*np.exp(-1j*s/n*(abs(a)**2-1));d=b-b.mean();v=4*np.cov(np.array([d.real,d.imag]),bias=False)
      data['rows'].append(dict(n=n,nu=nu,shots=2**power,seed=seed,s=s,lambda_qmc=np.linalg.eigvalsh(v)[0],
        exact=moments(n,nu,s)['lambda'],analytic_twa=moments(n,nu,s,True)['lambda']))
data['complete_original_occupation_grid']=True
save_json(path,data)
