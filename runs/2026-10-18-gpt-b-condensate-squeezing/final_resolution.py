#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Last frozen strong-disorder convergence checks."""
import sys,importlib.util,datetime
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'2026-10-18-gpt-b-grin-squeezing/run.py'
s=importlib.util.spec_from_file_location('independent_driver',p);d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
from squeezing import *
RUN=Path(__file__).resolve().parent
records=[];nonlinear=[];skipped=[]
# This session must stop production by 09:56 EDT to preserve finalization time.
# Later reproductions are unlimited; --unlimited also disables this session cap.
now=datetime.datetime.now(datetime.timezone.utc)
deadline=datetime.datetime(2026,10,18,13,56,tzinfo=datetime.timezone.utc)
cap=now.date()==deadline.date() and '--unlimited' not in sys.argv
def budget(seconds):
 return not cap or (deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds()>seconds
def checkpoint():
 save_json(RUN/'final_resolution.json',dict(**IDENTITY,complete=False,records=records,
   nonlinear_files=nonlinear,skipped=skipped,budget_deadline_UTC=deadline.isoformat() if cap else None))
for sigma in [2,3]:
 for dis in range(7601,7613):
  for h in [.00125,.000625]:
   tag=f'K5_E0.3_s{sigma:g}_l4201_d{dis}_h{h:g}_z20'
   cached=(d.DATA/(tag+'_tangent.npz')).exists()
   if not cached and not budget(45):
    skipped.append(dict(kind='tangent',sigma=sigma,disorder=dis,dt=h,reason='session production deadline'));checkpoint();continue
   records.append(d.tangent_case(5,.3,sigma,4201,dis,20,h)[-1])
   checkpoint()
for h in [.00125,.000625]:
 tag=f'K5_E0.3_s3_l4201_d7601_h{h:g}_z20_n1e+10_p8_loss0_w1'
 cached=all((d.DATA/(tag+f'_b{b}.npz')).exists() for b in range(4))
 if not cached and not budget(360 if h==.00125 else 700):
  skipped.append(dict(kind='nonlinear',sigma=3,disorder=7601,dt=h,reason='insufficient time before session production deadline'));checkpoint();continue
 nonlinear.append(d.twa_case(5,.3,3,4201,7601,1e10,20,dt=h,power=8)['tag']+'.json')
 checkpoint()
save_json(RUN/'final_resolution.json',dict(**IDENTITY,complete=not skipped,records=records,nonlinear_files=nonlinear,
 skipped=skipped,budget_deadline_UTC=deadline.isoformat() if cap else None))
