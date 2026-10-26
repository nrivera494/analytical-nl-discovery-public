#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Frozen dyadic Brownian resolution extension."""
import sys,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'2026-10-18-gpt-b-grin-squeezing/run.py'
spec=importlib.util.spec_from_file_location('independent_driver',p);driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
from squeezing import *
RUN=Path(__file__).resolve().parent

def main():
    memory_gate();m=Model(5);checks=[]
    for h in [.02,.01]:
        old=RAW/'2026-10-18-gpt-b-grin-squeezing'/f'K5_E0.3_s0.3_l4201_d7601_h{h:g}_z100_tangent.npz'
        x=np.load(old)['x'];fresh=tangent_run(m,m.launch(.3,4201),[0,1,2,5,10,20,50,100],h,.3,7601)
        checks.append(dict(dt=h,max_change=float(np.max(abs(fresh-x)))))
    save_json(RUN/'bridge_checks.json',dict(**IDENTITY,rows=checks))
    if max(x['max_change'] for x in checks)!=0:raise RuntimeError('Nested extension changed old path')
    records=[]
    for sigma in [.3,1,2,3]:
      for dis in range(7601,7613):
       for h in [.02,.01,.005,.0025]:
        records.append(driver.tangent_case(5,.3,sigma,4201,dis,zmax=50,dt=h)[-1])
        save_json(RUN/'refinement_summary.json',dict(**IDENTITY,freeze='e221a59c026e933deafe1ba16a12123eaca4f110',complete=len(records)==192,records=records))
if __name__=='__main__':main()
