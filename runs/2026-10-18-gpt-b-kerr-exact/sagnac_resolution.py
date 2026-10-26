#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Frozen conditional pump-integral refinement."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from kerr_squeezing import moments
from scipy.stats import qmc
RUN=Path(__file__).resolve().parent
def main():
    rows=[];q=np.array([1,1,2,2,2,3,3,3,3,4,4,4,4,4]);Phi=30
    for n in [1e10,5e9]:
      ref=moments(n,1,Phi);_,u=np.linalg.eigh(ref['V']);v=u[:,0]
      for power in [14,16]:
       for seed in [8881,8882]:
        memory_gate();x=-np.log(qmc.Sobol(14,scramble=True,seed=seed).random_base2(power));x/=x.sum(axis=1,keepdims=True)
        pp=(1-.6*np.sum(x/q,axis=1))/(1-.6*np.mean(1/q));variance=0.
        for p in pp:variance+=float(v@moments(n*p,1,Phi*p)['V']@v)
        variance/=len(pp);eps2=float(np.var(pp,ddof=1));pred=ref['lambda']+eps2
        rows.append(dict(n_per_arm=n,n_total_pump=2*n,Phi=Phi,pump_samples=len(pp),seed=seed,epsilon2=eps2,
          exact_coherent=ref['lambda'],tracking_fixed=variance,prediction=pred,
          relative_error=variance/pred-1,jitter_increment_relative_error=(variance-ref['lambda'])/eps2-1))
        save_json(RUN/'sagnac_resolution.json',dict(**IDENTITY,complete=len(rows)==8,rows=rows));print('Sagnac refined',n,power,seed,flush=True)
if __name__=='__main__':main()
