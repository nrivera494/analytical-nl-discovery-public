#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
from pathlib import Path
import json,platform,subprocess,time
import numpy as np
import tomli,yaml
ROOT=Path(__file__).resolve().parents[1];RUN='2026-10-08-gpt-a-similariton-wavebreaking';OUT=ROOT/'runs'/RUN
with (OUT/'config.toml').open('rb') as f:cfg=tomli.load(f)
raw=Path(cfg['raw_location']);recs={};cases=[]
for c in cfg['cases']:
 p=raw/(c['label']+'.toml')
 if not p.exists():continue
 with p.open('rb') as f:r=tomli.load(f)
 recs[r['label']]=r;rows=r['rows']
 o={k:v for k,v in r.items() if k!='rows'}
 for name in ['compressive_velocity_gradient','compressive_riemann_gradient','maximum_scaled_density_gradient']:
  j=max(range(len(rows)),key=lambda i:rows[i][name]);o['max_'+name]=rows[j][name];o['time_of_max_'+name]=rows[j]['gain_length']
 o['maximum_time_guard']=max(a['time_guard_fraction'] for a in rows);cases.append(o)
by={a['label']:a for a in cases};groups=[]
for label,r in recs.items():
 if not label.endswith('_n8192') or label.startswith('shock'):continue
 prefix=label[:-6];labs=[prefix+'_n'+str(n) for n in [2048,4096,8192]]
 if not all(a in by for a in labs):continue
 gg=np.array([by[a]['max_maximum_scaled_density_gradient'] for a in labs]);rr=gg[1:]/gg[:-1]
 rows=[recs[a]['rows'] for a in labs]
 rho=np.array([[b['maximum_scaled_density_gradient'] for b in a] for a in rows]);tt=[a['gain_length'] for a in rows[-1]]
 ratios=rho[1:]/np.maximum(rho[:-1],1e-30)
 # Descriptive resolution-dependent indicator, not an analytic catastrophe time.
 indicated=(ratios[0]>1.4)&(ratios[1]>1.4)&(rho[-1]>10)
 groups.append(dict(label=prefix,shape=r['shape'],width=r['width'],chirp=r['chirp'],
  peak_density_gradients=gg.tolist(),successive_peak_ratios=rr.tolist(),
  resolved_steepening_indicator=bool(all(rr>1.4) and gg[-1]>10),
  interpretation=('resolved steepening' if all(rr>1.4) and gg[-1]>10 else
                  'possible steepening' if np.any(indicated) or all(rr>1.3) else 'no growth on this horizon'),
  first_simultaneous_indicator_gain_length=next((t for t,b in zip(tt,indicated) if b),None)))
shock=[]
for n in [1024,2048,4096,8192]:
 lab=f'shock_n{n}'
 if lab in recs:
  rows=recs[lab]['rows'];shock.append(dict(nt=n,
   gradients_at_gain_lengths={f'{z:g}':min(rows,key=lambda a:abs(a['gain_length']-z))['compressive_riemann_gradient'] for z in [.04,.06,.07,.075,.08,.10,.12]}))
summary=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',expected_cases=len(cfg['cases']),completed_cases=len(cases),
 cases=cases,shape_grid=groups,protected_shock_example=shock,
 classification='Exploratory: peak density gradient increases by >1.4 at both successive spatial refinements and fine-grid peak >10. Does not prove exact shock time; absence is not proof of regularity.')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
commit=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
meta=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',task='T-20261008-gpt-a-01',solver_commit=commit,
 exploration='explorations/2026-10-08-gpt-a-similariton-attraction.md',
 solver_dirty=False,solver_used=False,hardware=platform.platform(),hostname=platform.node(),wall_seconds=sum(r['elapsed_seconds'] for r in recs.values()),
 raw_location=str(raw),evaluator='evaluator/similariton_hydro.jl',summary_evaluator='evaluator/similariton_hydro_summarize.py',
 caveat='Finite-volume entropy continuation; does not identify the dispersive NLSE with entropy Euler after breaking.')
(OUT/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
print('cases',len(cases),'of',len(cfg['cases']),'indicators',sum(g['resolved_steepening_indicator'] for g in groups),'of',len(groups))
for g in groups:print(g)
