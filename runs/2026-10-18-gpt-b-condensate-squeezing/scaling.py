#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Frozen paired-vacuum curvature scaling."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from squeezing import *
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name;DATA.mkdir(exist_ok=True)
def main():
    memory_gate();m=Model(5);a=m.launch(.3,4201);zs=np.array([0,5,10,20]);tan=tangent_run(m,a,zs,sigma=.3,seed=7601);rows=[]
    for n in [1e5,3e5,1e6,3e6,1e7,3e7,1e8]:
      for b in range(4):
        ini,x=wigner_initial(a,n,power=8,seed=8861+b);noise=np.r_[x,-x];initial=np.r_[ini,2*a-ini]
        path=DATA/f'paired_n{n:g}_b{b}.npz'
        if path.exists():fields=np.load(path)['fields']
        else:
          memory_gate();fields=ensemble_run(m,initial,n,zs,sigma=.3,seed=7601);np.savez_compressed(path,fields=fields)
        for z,t,f in zip(zs,tan,fields):
          if z==0:continue
          tt=tangent_observables(t);v=sample_observables(f,n,tt,noise)
          rows.append(dict(n=n,batch=b,z=float(z),held_out=n in [1e5,3e7,1e8],own_linear=tt['lambda_own'],own=v['own_fixed_control'],own_excess=v['own_fixed_control']-tt['lambda_own'],quad_linear=tt['lambda_quad'],quad=v['quad_fixed_control'],quad_excess=v['quad_fixed_control']-tt['lambda_quad'],
              curvature_prediction=tt['own'][1,1]**2/(8*n*tt['f0'])))
      save_json(RUN/'scaling_summary.json',dict(**IDENTITY,complete=n==1e8,rows=rows));print('paired scaling',n,flush=True)
if __name__=='__main__':main()
