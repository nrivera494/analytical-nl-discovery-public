"""Freeze convergence checks, gpt-d / gpt-6-astra / gpt."""
from propagate import *
cases=[('c02-heldout6-step','c02-heldout6',{'h':.0000125},{}),
       ('c02-heldout6-fine','c02-heldout6',{}, {'n':32768,'dt':.00075}),
       ('c02-heldout6-wide','c02-heldout6',{}, {'n':32768,'dt':.0015}),
       ('c02-core-step','c02-core',{'h':.0000625},{}),
       ('c02-short0p5-wide','c02-short0p5',{}, {'n':32768})]
rows=[]
for slug,src,p,g in cases:
 cfg=json.loads((ROOT/'runs'/('2026-10-16-gpt-d-'+src)/'config.yaml').read_text())
 cfg['run_id']='2026-10-16-gpt-d-'+slug;cfg['propagation'].update(p);cfg['grid'].update(g)
 cfg['convergence_of']='2026-10-16-gpt-d-'+src
 if cfg['grid']['n']>16384:
  cfg['grid_exception']='Convergence only: preserve the existing window while halving dt, or double the existing window. N=6 compression has nonzero near-Nyquist occupation; the 0.5-fs pulse has projection tails. No dense matrices and no field z-history; memory remains far below 3 GB.'
 rd=ROOT/'runs'/cfg['run_id'];rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
 rows.append({'run_id':cfg['run_id'],'expected':'Retention and rate bounds continue to hold; identity mismatch decreases with temporal refinement; numerical parameter changes are reported, not fitted away.'})
dump(Path(__file__).parent/'convergence_predictions.json',{'identity':IDENTITY,'cases':rows})
