#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt. Precision-run summaries."""
import json
import math
import platform
from pathlib import Path
import tomli
import yaml
import numpy as np
import mpmath as mp

folder=Path(__file__).resolve().parent
raw=Path('~/analytical-nl-discovery-data')/folder.name
identity=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')
cases={p.stem:tomli.loads(p.read_text()) for p in sorted(raw.glob('*.toml'))}
for name,c in cases.items():
    path=raw/(name+'_spectrum.tsv')
    if not path.exists():continue
    data=np.loadtxt(path)
    q=data[:,1]+1j*data[:,2]
    intensity=abs(np.fft.fft(q))**2
    t=(np.arange(c['n'])-c['n']//2)*c['window']/c['n']+c['center']
    c['core_peak_time']=float(t[intensity.argmax()])
    c['core_peak_intensity']=float(intensity.max())
    c['leading_ray_clearance']=(c['xi']-math.pi/4)/(4*c['delta3']) if c['delta3'] else None
    w=data[:,0];q0=np.fft.ifft(1/np.cosh(t));p0=abs(q0)**2
    spaper=835/(2*np.pi*299.792458*50)
    physical=(1+spaper*w)>0
    weight=np.zeros_like(w);weight[physical]=1/(1+spaper*w[physical])
    norm0=float(sum(p0*weight));delta=c['measurement_delta3']
    band=w>=1/(6*delta);wr=1/(2*delta)+18*delta
    resonant=(w>=.75*wr)&(w<=1.5*wr)
    p15=data[:,3]**2+data[:,4]**2;p20=data[:,5]**2+data[:,6]**2
    nyquist=np.pi*c['n']/c['window']
    spectral_edge=abs(w)>.95*nyquist
    positive_edge=w>.95*nyquist
    c['ungated_last_5pct_nyquist_energy_fraction']=float(sum(abs(q[spectral_edge])**2)/sum(p0))
    c['gate20_positive_last_5pct_nyquist_over_resonant']=float(sum(p20[positive_edge])/sum(p20[resonant]))
    c['resonant_peak_over_nyquist']=float(w[np.flatnonzero(resonant)[np.argmax(p20[resonant])]]/nyquist)
    c['physical_photon_gate15']=float(sum(p15[band]*weight[band])/norm0)
    c['physical_photon_resonant_gate20']=float(sum(p20[resonant]*weight[resonant])/norm0)
    c['physical_gate_ratio']=c['physical_photon_gate15']/c['physical_photon_resonant_gate20']
    dispersion_energy=w*w/2-c['delta3']*w**3
    hamiltonian=c['window']*sum(dispersion_energy*abs(q)**2)-2*c['window']/c['n']*sum(intensity**2)
    initial_h=c['window']*sum(dispersion_energy*p0)-2*c['window']/c['n']*sum((1/np.cosh(t))**4)
    c['hamiltonian_relative_drift_from_saved_spectrum']=float((hamiltonian-initial_h)/abs(initial_h))
    c['momentum_drift_per_initial_energy']=float(sum(w*(abs(q)**2-p0))/sum(p0))
checks=[]
if 'primary' in cases:
    base=cases['primary']['metrics']
    for name in ['halfstep','window','lower_halfstep','quarterstep','precompression_halfstep','precompression_window','precompression_grid']:
        if name not in cases:continue
        reference='precompression_grid_reference' if name=='precompression_grid' else ('precompression' if name.startswith('precompression_') else ('lower' if name=='lower_halfstep' else ('halfstep' if name=='quarterstep' else 'primary')))
        base=cases[reference]['metrics']
        m=cases[name]['metrics']
        checks.append(dict(variant=name,reference=reference,relative_gate15=m['eta_gate15']/base['eta_gate15']-1,
            relative_gate20=m['eta_gate20']/base['eta_gate20']-1,
            relative_resonant_gate20=m['eta_resonant_gate20']/base['eta_resonant_gate20']-1))
    for name,c in cases.items():
        if 'metrics' not in c:continue
        m=c['metrics']
        c['gate15_over_gate20']=m['eta_gate15']/m['eta_gate20']
        c['broad_over_resonant_gate15']=m['eta_gate15']/m['eta_resonant_gate15']
slopes=[]
rows=sorted([cases[n] for n in ['lower','middle','primary','upper'] if n in cases],key=lambda c:c['delta3'])
dstar=math.acos(math.sqrt(3)-1)/2
for a,b in zip(rows[:-1],rows[1:]):
    record=dict(delta3_interval=[a['delta3'],b['delta3']],predicted_radiation_rate=dstar,
        exact_null_rate=dstar/3)
    for field in ['eta_gate15','eta_gate20','eta_resonant_gate20']:
        record[field+'_slope']=-(math.log(b['metrics'][field])-math.log(a['metrics'][field]))/(1/b['delta3']-1/a['delta3'])
    slopes.append(record)
cfg=yaml.safe_load((folder/'config.yaml').read_text())
mp.mp.dps=60
z=mp.mpf(str(cfg['unique_minimum_attack']['xi']));delta=mp.mpf(str(cfg['unique_minimum_attack']['delta3']))
dend=mp.acos(mp.sqrt(3)*abs(mp.sin(2*z))-1)/2
pole=1j*dend
residue=2*mp.exp(.5j*z)*(mp.cosh(3*pole)+3*mp.exp(4j*z)*mp.cosh(pole))/(4*mp.sinh(4*pole)+8*mp.sinh(2*pole))
gate=1/(1+mp.exp(-2*(pole-15)))+1/(1+mp.exp(2*(pole+15)))
null_eta=mp.pi*abs(residue*gate)**2/(2*dend)*mp.exp(-dend/(3*delta))
selection_null=dict(xi=float(z),delta3=float(delta),endpoint_strip=float(dend),
    leading_pole_null_eta=float(null_eta),rate=float(dend/3),
    note='TOD-free endpoint null used to select the unique-minimum test; not a propagated-TOD prediction.')
adaptive=None
if 'middle' in cases:
    prediction=cfg['adaptive_frozen_case']['predicted_gate15']
    actual=cases['middle']['metrics']['eta_gate15']
    adaptive=dict(prediction=prediction,actual=actual,log_error=math.log(actual/prediction),
        tolerance=cfg['adaptive_frozen_case']['log_error_tolerance'])
orders={}
if all(n in cases for n in ['primary','halfstep','quarterstep']):
    for field in ['eta_gate15','eta_resonant_gate20']:
        a,b,c=[cases[n]['metrics'][field] for n in ['primary','halfstep','quarterstep']]
        orders[field]=dict(measured_order=math.log(abs((a-b)/(b-c)))/math.log(2),predicted_order=4)
result=dict(**identity,run_id=folder.name,cases=cases,convergence=checks,local_slopes=slopes,adaptive_prediction=adaptive,step_orders=orders,endpoint_selection_null=selection_null,
    note='Full-TOD propagations except the explicitly labeled propagated_null and the pilot exact null.')
(folder/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
complete=all(k in cases for k in ['primary','halfstep','window','propagated_null','upper','lower','precompression','precompression_halfstep','precompression_window','precompression_grid'])
budget_stopped=[p.stem for p in raw.glob('*.log') if 'Reserved closeout time reached' in p.read_text(errors='replace')]
meta_deferred=[c['name'] for c in cfg['conditional_cases'] if c.get('status','').startswith('deferred')]
if 'deferred' in cfg['adaptive_frozen_case']['status']:meta_deferred.append('middle')
meta=dict(**identity,run_id=folder.name,solver_commit='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',
    solver_dirty=False,implementation='independent Double64 RK4IP and GenericFFT, dependency versions in Manifest.toml',
    status='complete' if complete else ('partial; numerical budget stopped' if budget_stopped else 'in-progress'),raw_location=str(raw),hardware=platform.platform(),
    wall_seconds=sum(c['wall_seconds'] for c in cases.values()),deferred_cases=meta_deferred,budget_stopped_cases=budget_stopped)
(folder/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
lines=['<!-- agent: gpt-a; model: gpt-6-astra; family: gpt -->','',
    '# Higher-precision evidence','',f'Source run: `{folder.name}`. Full-precision arithmetic is used before gating and Fourier measurement.','',
    '| Case | xi | TOD | Steps | Gate-15 band | Gate-20 resonant | Ratio | Core peak time |',
    '|---|---:|---:|---:|---:|---:|---:|---:|']
for name,c in cases.items():
    if 'metrics' not in c:continue
    m=c['metrics'];ratio=m['eta_gate15']/m['eta_resonant_gate20']
    lines.append(f"| {name} | {c['xi']:.8g} | {c['delta3']:g} | {c['steps']} | {m['eta_gate15']:.9e} | {m['eta_resonant_gate20']:.9e} | {ratio:.6g} | {c['core_peak_time']:.5g} |")
lines+=['','The `propagated_null` has zero TOD; its measurement band is labeled by 0.003. It is not radiation generation.','',
    '| Variant / reference | Gate-15 change | Resonant gate-20 change | Both below 1%? |',
    '|---|---:|---:|---|']
for c in checks:
    passed=max(abs(c['relative_gate15']),abs(c['relative_resonant_gate20']))<.01
    lines.append(f"| {c['variant']} / {c['reference']} | {100*c['relative_gate15']:.6g}% | {100*c['relative_resonant_gate20']:.6g}% | {'yes' if passed else 'no'} |")
lines+=['','| TOD interval at xi=3*pi/4 | Gate-15 local rate | Resonant gate-20 rate | Claimed d_star |',
    '|---|---:|---:|---:|']
for r in slopes:
    lines.append(f"| {r['delta3_interval']} | {r['eta_gate15_slope']:.8g} | {r['eta_resonant_gate20_slope']:.8g} | {dstar:.8g} |")
if adaptive:
    lines+=['',f"Adaptive frozen gate-tail prediction: log-error {adaptive['log_error']:.8g}; tolerance {adaptive['tolerance']:g}."]
lines+=['','Deferred optional cases: '+', '.join(meta_deferred)+'. Their absence does not count as a passed test.','']
(folder/'tables.md').write_text('\n'.join(lines))
print(json.dumps(dict(cases=list(cases),convergence=checks,local_slopes=slopes),indent=2))
