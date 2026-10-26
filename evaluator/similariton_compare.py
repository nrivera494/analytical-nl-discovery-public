#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Cross-run convergence and independent-coordinate comparisons."""
from pathlib import Path
import json,platform,subprocess,time
import numpy as np
import tomli,yaml
from numpy.polynomial.legendre import leggauss
from similariton_summarize import load_run
ROOT=Path(__file__).resolve().parents[1]
RUN='2026-10-08-gpt-a-similariton-comparison';OUT=ROOT/'runs'/RUN
OUT.mkdir(exist_ok=True);start=time.monotonic()
metrics=['density_l1','width_ratio','chirp_ratio','core_scaled_velocity_rms','wing_mass_fraction']
def compare(a,b):
 ra={round(r['gain_length'],9):r for r in a['rows']};rb={round(r['gain_length'],9):r for r in b['rows']}
 zs=sorted(set(ra)&set(rb));d={k:[abs(ra[z][k]-rb[z][k]) for z in zs] for k in metrics}
 def passed(v):return v['density_l1']<.1 and abs(v['width_ratio']-1)<.05 and abs(v['chirp_ratio']-1)<.05 and v['core_scaled_velocity_rms']<.02
 return dict(common_samples=len(zs),end_gain_length=zs[-1],final_classification_unchanged=passed(ra[zs[-1]])==passed(rb[zs[-1]]),maximum_absolute_difference={k:max(v) for k,v in d.items()},
             final_absolute_difference={k:v[-1] for k,v in d.items()})
def load(name):return load_run('2026-10-08-gpt-a-similariton-'+name)[2]
base=load('map');conv=load('map-convergence');rate=load('rates-safe');rc=load('rates-convergence')
map_comparisons={}
refs={'gaussian':'gaussian_N10_w1_q0','sech':'sech_N10_w2_q0p3333','supergaussian':'supergaussian_N10_w0p5_qm0p5','N5_supergaussian':'supergaussian_N5_w0p5_qm0p5'}
for name,ref in refs.items():
 for tag in ['step','grid','window']:
  lab=f'{name}_{tag}'
  if lab in conv:map_comparisons[lab]=compare(base[ref],conv[lab])
for name in ['heldout','odd']:
 for tag in ['step','grid','window']:
  if f'{name}_{tag}' in conv and f'{name}_base' in conv:
   map_comparisons[f'{name}_{tag}']=compare(conv[f'{name}_base'],conv[f'{name}_{tag}'])
rate_comparisons={}
for tag in ['grid','step','window','amplitude']:
 for pm in ['minus','plus']:
  lab=f'{tag}_width_{pm}'
  if lab in rc and tag!='amplitude':rate_comparisons[lab]=compare(rate[f'N10_width_{pm}'],rc[lab])
for N in [5,20]:
 for pm in ['minus','plus']:
  lab=f'N{N}_grid_width_{pm}'
  if lab in rc:rate_comparisons[lab]=compare(rate[f'N{N}_width_{pm}'],rc[lab])
second={}
for mode in ['width','chirp']:
 for pm in ['minus','plus']:
  lab=f'N10_{mode}_{pm}'
  if lab in conv and lab in rate:second[lab]=compare(conv[lab],rate[lab])
pilot=load('pilot');lp=load('lens-pilot')
for label in pilot:
 if label in lp:second[label]=compare(pilot[label],lp[label])
odd={}
for label,r in conv.items():
 if not label.startswith('odd_'):continue
 odd[label]=dict(maximum_even_overlap=max(a['even_parabolic_field_overlap'] for a in r['rows']),
   maximum_scaled_central_density=max(a['central_scaled_density'] for a in r['rows']),
   final_density_l1=r['rows'][-1]['density_l1'],final_width_ratio=r['rows'][-1]['width_ratio'],
   minimum_normalized_phase_optimized_field_distance_squared=min(2-2*a['even_parabolic_field_overlap'] for a in r['rows']))
fits={}
for suffix in ['rates-safe','rates-convergence','rates-fine','rates-final-controls','rates-lower-n-refinement','rates-prefix-control','map-convergence']:
 p=ROOT/'runs'/('2026-10-08-gpt-a-similariton-'+suffix)/'summary.json'
 if p.exists():fits[suffix]=json.loads(p.read_text())['paired_width_chirp_fits']
pv={};pvraw=Path.home()/'analytical-nl-discovery-data'/'2026-10-08-gpt-a-similariton-physical-vacuum'
directraw=pvraw.with_name(pvraw.name+'-direct')
for name in ['linear_l3','linear_l4','finite_mixed','heldout_asymmetric']:
 paths=[directraw/f'{name}_degree{n}.npz' for n in [32,64]]
 if not all(p.exists() for p in paths):continue
 a,b=[np.load(p) for p in paths]
 pv[name]=dict(maximum_degree_change_displacement=float(np.max(np.abs(a['displacement']-b['displacement'][::2]))),
  maximum_degree_change_velocity=float(np.max(np.abs(a['velocity']-b['velocity'][::2]))),
  maximum_degree_change_energy_relative_to_initial=float(np.max(np.abs(a['H']-b['H']))/a['H'][0]))
 for n in [32,64]:
  a=np.load(pvraw/f'{name}_degree{n}.npz');b=np.load(directraw/f'{name}_degree{n}.npz')
  pv[name][f'blas_vs_direct_degree{n}']=dict(maximum_displacement_change=float(np.max(abs(a['displacement']-b['displacement']))),
    maximum_velocity_change=float(np.max(abs(a['velocity']-b['velocity']))))
  aq,wq=leggauss(256);bary=(-1.)**np.arange(n+1);bary[[0,-1]]*=.5
  B=bary[None,:]/(aq[:,None]-b['a'][None,:]);B/=B.sum(axis=1)[:,None]
  Vq=np.einsum('ij,jk->ik',B,b['velocity'],optimize=False)
  vel2=np.sum((wq*(1-aq*aq)/18)[:,None]*Vq**2,axis=0)
  pv[name][f'direct_degree{n}_stronger_inequality_maximum_residual']=float(np.max(b['Hdot']+b['H']/3+vel2/6))
hydro={};hydro_raw=Path.home()/'analytical-nl-discovery-data'/'2026-10-08-gpt-a-similariton-wavebreaking'
for name,refname in [('gaussian','gaussian_w1_q0p3333_n8192'),('sech','sech_w2_qm0p5_n8192'),('supergaussian','supergaussian_w0p5_q0_n8192')]:
 def hr(label):
  with (hydro_raw/(label+'.toml')).open('rb') as f:return tomli.load(f)['rows']
 a=hr(refname)
 for tag in ['step','grid','window']:
  b=hr(name+'_'+tag);metric='maximum_scaled_density_gradient'
  am=max(v[metric] for v in a);bm=max(v[metric] for v in b)
  hydro[name+'_'+tag]=dict(base_peak_density_gradient=am,refined_peak_density_gradient=bm,peak_ratio=bm/am,
     maximum_time_guard=max(v['time_guard_fraction'] for v in b))
long_compare={};late_refinement={};additional_refinement={};fine_rates={};rate_final_controls={};prefix_controls={}
if (ROOT/'runs'/'2026-10-08-gpt-a-similariton-long-inputs'/'config.toml').exists():
 long=load('long-inputs')
 for label,r in long.items():
  if label=='heldout_order6':other=conv.get('heldout_grid')
  else:other=next((v for v in base.values() if v['shape']==r['shape'] and v['width']==r['width'] and abs(v['chirp']-r['chirp'])<1e-9 and v['Nstar']==r['Nstar']),None)
  if other:long_compare[label]=compare(r,other)
if (ROOT/'runs'/'2026-10-08-gpt-a-similariton-long-refinement'/'config.toml').exists():
 lr=load('long-refinement')
 for label,r in lr.items():
  late_refinement[label+'_vs_coarse']=compare(long['gaussian_w2_qm0p5'],r)
 for label,refname in [('gaussian_grid65536','gaussian_grid32768'),('gaussian_step65536','gaussian_grid65536'),('gaussian_window131072','gaussian_grid65536')]:
  if label in lr and refname in lr:late_refinement[label+'_vs_'+refname]=compare(lr[refname],lr[label])
if (ROOT/'runs'/'2026-10-08-gpt-a-similariton-long-additional'/'config.toml').exists():
 la=load('long-additional')
 for name in ['heldout_order6','sech_w2_qm0p5','supergaussian_w2_qm0p5']:
  for n in [32768,65536]:
   label=f'{name}_n{n}'
   if label in la:additional_refinement[label+'_vs_coarse']=compare(long[name],la[label])
  lo,hi=f'{name}_n32768',f'{name}_n65536'
  if lo in la and hi in la:additional_refinement[hi+'_vs_'+lo]=compare(la[lo],la[hi])
for ns,runname,oldprefix in [(20,'rates-fine','N20_grid_width'),(5,'rates-lower-n-refinement','N5_grid_width'),(10,'rates-lower-n-refinement','grid_width')]:
 if not (ROOT/'runs'/('2026-10-08-gpt-a-similariton-'+runname)/'config.toml').exists():continue
 rf=load(runname)
 for tag in ['minus','plus']:
  lab=f'N{ns}_width_{tag}';old=f'{oldprefix}_{tag}'
  if lab in rf and old in rc:
   fine_rates[lab]=compare(rc[old],rf[lab])
   cut=lambda r:dict(r,rows=[v for v in r['rows'] if v['gain_length']<=6+1e-9])
   fine_rates[lab]['prefix_grid_control_to_gain6']=compare(cut(rate[lab]),cut(rc[old]))
   pa=Path.home()/'analytical-nl-discovery-data'/'2026-10-08-gpt-a-similariton-rates-safe'/(lab+'.npz')
   pb=Path.home()/'analytical-nl-discovery-data'/'2026-10-08-gpt-a-similariton-rates-convergence'/(old+'.npz')
   a,b=np.load(pa),np.load(pb);fa=a['fields'][:,np.argmin(abs(a['z']-6))];fb=b['fields'][:,np.argmin(abs(b['z']-6))]
   n=len(fa);nh=n//2;fw=np.fft.ifft(fa);ff=np.zeros(len(fb),complex);ff[:nh]=fw[:nh];ff[-nh:]=fw[nh:]
   fa=np.fft.fft(ff);phase=np.angle(np.vdot(fa,fb))
   fine_rates[lab]['checkpoint_phase_optimized_relative_field_l2']=float(np.linalg.norm(fb*np.exp(-1j*phase)-fa)/np.linalg.norm(fb))
if (ROOT/'runs'/'2026-10-08-gpt-a-similariton-rates-final-controls'/'config.toml').exists():
 controls=load('rates-final-controls')
 for tag in ['step','window']:
  for pm in ['minus','plus']:
   label=f'N20_{tag}_width_{pm}'
   if label in controls:rate_final_controls[label]=compare(rc[f'N20_grid_width_{pm}'],controls[label])
if (ROOT/'runs'/'2026-10-08-gpt-a-similariton-rates-prefix-control'/'summary.json').exists():
 controls=load('rates-prefix-control');fine=load('rates-fine')
 for pm in ['minus','plus']:
  label=f'N20_width_{pm}'
  if label in controls:prefix_controls[label]=compare(fine[label],controls[label])
 a=next(v for v in fits['rates-fine'] if v['pair']=='N20_width')['fits']['6-12']
 b=next(v for v in fits['rates-prefix-control'] if v['pair']=='N20_width')['fits']['6-12']
 prefix_controls['fit_change_from_16384_to_8192_prefix']={k:b[k]-a[k] for k in a}
summary=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',
 map_convergence=map_comparisons,rate_trajectory_convergence=rate_comparisons,
 independent_coordinate_solvers=second,odd_counterexample=odd,paired_rate_fits=fits,
 physical_vacuum_convergence=pv,long_continuation_agreement_through_gain8=long_compare,
 hydrodynamic_refinements=hydro,
 late_gaussian_refinements=late_refinement,late_additional_refinements=additional_refinement,
 further_rate_grid_refinement=fine_rates,further_rate_time_window_controls=rate_final_controls,
 propagated_prefix_controls=prefix_controls,
 caveat='Absolute changes in specified observables. No claim of whole-field/edge-profile convergence or global basin.')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
inputs=['map','map-convergence','pilot','lens-pilot','rates-safe','rates-convergence','rates-fine','rates-final-controls','rates-lower-n-refinement','rates-prefix-control','physical-vacuum','physical-vacuum-direct','wavebreaking','long-inputs','long-refinement','long-additional']
(OUT/'config.yaml').write_text(yaml.safe_dump(dict(agent='gpt-a',model='gpt-6-astra',family='gpt',task='T-20261008-gpt-a-01',
    evaluator='evaluator/similariton_compare.py',input_runs=['2026-10-08-gpt-a-similariton-'+a for a in inputs],metrics=metrics),sort_keys=False))
commit=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
meta=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',task='T-20261008-gpt-a-01',solver_commit=commit,
 exploration='explorations/2026-10-08-gpt-a-similariton-attraction.md',
 solver_dirty=False,hardware=platform.platform(),hostname=platform.node(),wall_seconds=time.monotonic()-start,
 raw_location='Derived from the absolute raw locations in the input-run meta.yaml files; no additional raw data')
(OUT/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
print('map comparisons',len(map_comparisons),'rate comparisons',len(rate_comparisons),'second solver',len(second),'odd',odd)
