"""Exact one-dimensional cutoff optimization in a constant-coefficient ODE.
This is an algebraic check, not a claimed physical constant-K fibre design.
gpt-d/gpt-6-astra/gpt.
"""
import math,json
from pathlib import Path
rows=[]
for q in [.001,.003,.01,.03,.1]:
 def objective(s):
  u=(1-s)**.25;x=s/(8*q*u)
  return u*(1+math.tanh(x))/2
 # Golden-section maximization, independent of the claim's stationary formula.
 lo,hi=0.,1.-1e-12;gold=(math.sqrt(5)-1)/2
 x1=hi-gold*(hi-lo);x2=lo+gold*(hi-lo)
 for _ in range(140):
  if objective(x1)>objective(x2):hi=x2;x2=x1;x1=hi-gold*(hi-lo)
  else:lo=x1;x1=x2;x2=lo+gold*(hi-lo)
 s=(lo+hi)/2;sc=8*q*math.atanh(1-2*q)
 rows.append({'q':q,'exact_s':s,'closed_s':sc,'exact_eta_over_Ncut':objective(s),'closed_eta_over_Ncut':1-q*(1+math.log(1/q)),'exact_alpha_distance_from_cutoff':-.25*math.log(1-s),'closed_alpha_distance_from_cutoff':-.25*math.log(1-sc),'length_from_cutoff_ratio':math.log(1-sc)/math.log(1-s),'omitted_delta_dlog_a_at_closed_point':sc/(4*(1-sc))})
out={'agent':'gpt-d','model':'gpt-6-astra','family':'gpt','definition':'s=4 epsilon_cutoff delta; a=a_cutoff/(1-s)^(1/4)','cases':rows}
Path(__file__).with_name('cutoff_constant_summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
