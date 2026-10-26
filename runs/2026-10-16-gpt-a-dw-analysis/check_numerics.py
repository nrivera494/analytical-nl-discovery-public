#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt. Numerical audit diagnostics."""
import importlib.util
import json
from pathlib import Path
try:
    import tomllib
except ImportError:
    import tomli as tomllib
import numpy as np

folder=Path(__file__).resolve().parent
root=folder.parent
spec=importlib.util.spec_from_file_location('independent_gnlse',root/'2026-10-16-gpt-a-dw-core/simulate.py')
sim=importlib.util.module_from_spec(spec);spec.loader.exec_module(sim)

def read(slug):
    p=root/('2026-10-16-gpt-a-'+slug)/'summary.json'
    return json.loads(p.read_text()) if p.exists() else {}

def output(case):return case['outputs'][str(case['config']['zmax'])]
def difference(a,b):return None if a is None or b is None else a-b

baselines={
 'roy01':('dw-roy','roy_s1_d0.01'),
 'roy008':('dw-convergence','roy_s1_d0.008'),
 'core008':('dw-law','sech2_d0.008'),
 'sech3':('dw-heldout','sech3_none_z2_d0.0043'),
 'gauss4':('dw-heldout','gauss4_none_z1_d0.0028'),
 'M1gauss3':('dw-heldout','gauss3_M1_z2_d0.0055'),
 'gauss35':('dw-heldout','own_gauss35_x44'),
 'sech4_d0.0029':('dw-heldout','sech4_excluded_d0.0029'),
 'sech4_d0.0039':('dw-heldout','sech4_excluded_d0.0039'),
 'P5':('dw-followup','frozenP5_d0.0043'),
}
convergence=read('dw-convergence').get('cases',{})
variant_sources={name:'dw-convergence' for name in convergence}
for name,case in read('dw-followup').get('cases',{}).items():
    convergence[name]=case
    variant_sources[name]='dw-followup'
rows=[]
for tag,(slug,name) in baselines.items():
    case=read(slug).get('cases',{}).get(name)
    if case is None:continue
    baseline=output(case)
    for key,c in convergence.items():
        if not key.startswith(tag+'_') or c['config']['delta3']==0:continue
        m=output(c)
        rows.append(dict(baseline_run=slug,baseline_case=name,variant=key,variant_run=variant_sources[key],
            relative_gate15=m['eta_gate15']/baseline['eta_gate15']-1,
            relative_gate20=m['eta_gate20']/baseline['eta_gate20']-1,
            peak_delta_db=difference(m['peak_db'],baseline['peak_db']),
            energy_drift=m['energy_relative_drift'],formal_norm_drift=m['formal_norm_relative_drift'],
            time_edge_fraction=m['time_edge_fraction'],spectral_edge_fraction=m['spectral_edge_fraction'],
            dt_fs=c['dt_fs'],kernel_dc=c['raman_kernel_dc'],wall_seconds=c['wall_seconds']))

julia_cfg=tomllib.loads((root/'2026-10-16-gpt-a-dw-julia/config.toml').read_text())
julia={}
for cfg in julia_cfg['cases']:
    path=Path(julia_cfg['raw_location'])/(cfg['name']+'.npz')
    if not path.exists():continue
    data=np.load(path);m=sim.metrics(data['q'],data['q0'],data['t'],data['w'],cfg)
    damp=data['damping'];w=data['w'];p=abs(data['q'])**2;p0=abs(data['q0'])**2
    pref=(1+cfg['shock']*sim.S_PAPER*w)*damp
    keep=pref>1e-12
    weighted=sum(p[keep]/pref[keep]);weighted0=sum(p0[keep]/pref[keep])
    m['window_weighted_norm_drift']=weighted/weighted0-1
    m['min_damping_in_resonant_band']=min(damp[(w>=.75*m['w_roy'])&(w<=1.5*m['w_roy'])])
    m['damping_at_peak']=None if m['peak_w'] is None else damp[np.argmin(abs(w-m['peak_w']))]
    julia[cfg['name']]=dict(config=cfg,metrics=m,wall_seconds=float(data['elapsed']),
        process_peak_rss_mb=float(data['peak_rss_mb']))

filter_comparison=[]
for name,case in julia.items():
    if not name.endswith('_flat'):continue
    other=julia.get(name[:-5]+'_damp')
    if other is None:continue
    a=case['metrics'];b=other['metrics']
    filter_comparison.append(dict(case=name[:-5],
        eta_flat=a['eta_gate15'],eta_damp=b['eta_gate15'],
        relative_gate15=b['eta_gate15']/a['eta_gate15']-1,
        peak_delta_db=difference(b['peak_db'],a['peak_db']),
        damping_at_peak=b['damping_at_peak'],formal_norm_drift=b['formal_norm_relative_drift'],
        window_weighted_norm_drift=b['window_weighted_norm_drift']))

solver_comparison=[]
for julia_name,slug,case_name in [
    ('roy02_flat','dw-roy','roy_pilot_d002'),
    ('roy01_flat','dw-roy','roy_s1_d0.01'),
    ('core01_flat','dw-law','sech2_d0.01'),
]:
    if julia_name not in julia:continue
    case=read(slug).get('cases',{}).get(case_name)
    if case is None:continue
    a=julia[julia_name]['metrics'];b=output(case)
    jq=np.load(Path(julia_cfg['raw_location'])/(julia_name+'.npz'))['q']
    pq=np.load(Path('~/analytical-nl-discovery-data')/('2026-10-16-gpt-a-'+slug)/(case_name+'_z4.npz'))['q']
    solver_comparison.append(dict(julia_case=julia_name,python_run=slug,python_case=case_name,
        relative_gate15=a['eta_gate15']/b['eta_gate15']-1,peak_delta_db=difference(a['peak_db'],b['peak_db']),
        complex_field_relative_l2=float(np.linalg.norm(jq-pq)/np.linalg.norm(pq))))

symmetry=None
raw=Path('~/analytical-nl-discovery-data/2026-10-16-gpt-a-dw-convergence')
if (raw/'symmetry_+1_z2.npz').exists() and (raw/'symmetry_-1_z2.npz').exists():
    pos=np.load(raw/'symmetry_+1_z2.npz')['q'];neg=np.load(raw/'symmetry_-1_z2.npz')['q']
    reflection=(-np.arange(len(neg)))%len(neg)
    symmetry=dict(relative_l2_error=float(np.linalg.norm(pos-neg[reflection])/np.linalg.norm(pos)))

strip_convergence=[]
for key,c in convergence.items():
    if not c.get('strip_min'):continue
    if key.startswith('collapse_'):continue
    slug,name=('dw-strips','sech2_roy_s1') if key.startswith('roy_') else ('dw-heldout-strips','gauss3.5_none')
    anchor=read(slug)['cases'][name]['strip_min']
    for band,v in c['strip_min'].items():
        if not band.startswith('blue'):continue
        b=anchor.get(band)
        strip_convergence.append(dict(variant=key,band=band,z=v['z'],d=v['d'],d_log=v['d_log'],
            relative_d=None if b is None else v['d']/b['d']-1,
            relative_d_log=None if b is None else v['d_log']/b['d_log']-1))

kernel_order=None
kernel_coarse=next((r for r in rows if r['variant']=='roy01_sampled'),None)
kernel_fine=next((r for r in rows if r['variant']=='roy01_sampled_fine'),None)
if kernel_coarse is not None and kernel_fine is not None:
    kernel_order=dict(coarse_dt_fs=kernel_coarse['dt_fs'],fine_dt_fs=kernel_fine['dt_fs'],
        coarse_relative_yield_error=kernel_coarse['relative_gate20'],
        fine_relative_yield_error=kernel_fine['relative_gate20'],
        measured_order=float(np.log(abs(kernel_coarse['relative_gate20']/kernel_fine['relative_gate20']))/
            np.log(kernel_coarse['dt_fs']/kernel_fine['dt_fs'])),predicted_order=2)
result=dict(**sim.IDENTITY,convergence=rows,julia=julia,filter_comparison=filter_comparison,
            solver_comparison=solver_comparison,symmetry=symmetry,strip_convergence=strip_convergence,
            raman_kernel_order=kernel_order)
sim.write_json(folder/'numerics.json',result)
if julia:
    import yaml,platform
    jfolder=root/'2026-10-16-gpt-a-dw-julia'
    sim.write_json(jfolder/'summary.json',dict(**sim.IDENTITY,run_id=jfolder.name,cases=julia,
        solver_comparison=solver_comparison,filter_comparison=filter_comparison))
    (jfolder/'config.yaml').write_text(yaml.safe_dump(julia_cfg,sort_keys=False))
    (jfolder/'meta.yaml').write_text(yaml.safe_dump(dict(**sim.IDENTITY,run_id=jfolder.name,
        solver_commit=sim.SOLVER_COMMIT,solver_dirty=False,
        implementation='Pinned PulsePropagation fixed-step RK4IP; flat or solver-window nonlinear prefactor supplied explicitly',
        raw_location=julia_cfg['raw_location'],hardware=platform.platform(),
        wall_seconds=sum(v['wall_seconds'] for v in julia.values()),claim='C-20261016-claude-b-01'),sort_keys=False))
print(json.dumps(sim.clean_json({k:v for k,v in result.items() if k!='julia'}),indent=2))
