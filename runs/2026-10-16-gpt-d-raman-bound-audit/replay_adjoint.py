"""Validate the frozen optimized phase in an independent implementation."""
from propagate import *
import tomli
raw=RAW/'2026-10-16-gpt-d-c02-adjoint';m=tomli.loads((raw/'metrics.toml').read_text())
for variant,n,dt,h in [('base',4096,.00025,.000005),('step',4096,.00025,.0000025),('fine',8192,.000125,.000005),('wide',8192,.00025,.000005)]:
 for shaped in [False,True]:
  rid='2026-10-16-gpt-d-c02-mask-'+variant+('-shaped' if shaped else '-tl');rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True)
  cfg={'run_id':rid,'identity':IDENTITY,'fibre':{'material':'S28','loss_scale':0.,'dispersion':'quadratic'},'grid':{'n':n,'dt':dt,'carrier_um':.4},'input':{'shape':'sech','E_pJ':200.,'phase_coefficients':m['best_coefficients'] if shaped else [0.]*5},'positive_frequency_model':True,'omega_min_fraction':.1,'scope':'Formal model replay, not a calibrated fibre prediction; analytic Raman kernel.','propagation':{'T':.002,'L':.0005,'h':h,'save_every':.00005},'expected':{'max_rate_over_bound':1.,'integrated_loss_ratio_ceiling':1/(1+.000931031319858533*200*.0005)}}
  dump(rd/'config.yaml',cfg);execute_bound(rd/'config.yaml')
