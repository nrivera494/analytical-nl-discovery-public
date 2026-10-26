#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Frozen independent nonlinear ensemble checks."""
import sys,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'2026-10-18-gpt-b-grin-squeezing/run.py'
spec=importlib.util.spec_from_file_location('independent_driver',p);d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
from squeezing import *
RUN=Path(__file__).resolve().parent
def main():
    records=[]
    for E,sigma,launch,first,h,held in [(.3,.3,4201,7601,.01,False),(.3,3,4201,7601,.005,False),(.45,.3,4213,7701,.01,True)]:
      for dis in range(first,first+6):
        r=d.twa_case(5,E,sigma,launch,dis,1e10,zmax=20,dt=h,power=8)
        records.append(dict(file=r['tag']+'.json',held_out=held,E=E,sigma=sigma,disorder=dis,launch=launch,dt=h))
        save_json(RUN/'nonlinear_ensemble.json',dict(**IDENTITY,complete=False,records=records))
    checks=[]
    for sigma,h in [(.3,.01),(3,.005)]:
      checks.append(d.twa_case(5,.3,sigma,4201,7601,1e10,zmax=20,dt=h,power=9)['tag']+'.json')
    checks.append(d.twa_case(5,.3,3,4201,7601,1e10,zmax=20,dt=.0025,power=8)['tag']+'.json')
    save_json(RUN/'nonlinear_ensemble.json',dict(**IDENTITY,complete=True,records=records,convergence_files=checks))
if __name__=='__main__':main()
