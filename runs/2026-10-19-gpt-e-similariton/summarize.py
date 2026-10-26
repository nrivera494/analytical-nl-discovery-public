"""gpt-e / gpt-6-astra / gpt. Summarize reduced and full-field ASE audits."""
import json,platform
try:import tomllib
except ImportError:import tomli as tomllib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;RAW=Path('~/analytical-nl-discovery-data')/HERE.name

def read(name):return json.loads((HERE/(name+'.json')).read_text())
def compact(name):
    records=read(name)
    for i,r in enumerate(records):
        if len(r['rows'])>12:
            dest=RAW/f'{name}-case{i}-dense.json';dest.write_text(json.dumps(r,indent=2)+'\n')
            r['raw_curve_location']=str(dest)
            r['rows']=[x for x in r['rows'] if any(abs(x['tau']-v)<1e-10 for v in [1.,2.,4.,6.,12.,15.,18.,24.,r['last']])]
    (HERE/(name+'.json')).write_text(json.dumps(records,indent=2)+'\n')
    return records

main=compact('reduced-main');checks=compact('reduced-checks');compact('initial-reduced-main')
full=read('fullfield-main');fc=read('fullfield-checks');edge=read('fullfield-edge-resolution');short=read('fullfield-short')
base=next(r for r in main if abs(r['Gamma']-np.sqrt(18))<1e-8 and r['launch']=='asymptotic' and r['nsp']==1)
unchirped=next(r for r in main if abs(r['Gamma']-np.sqrt(18))<1e-8 and r['launch']=='unchirped')
def at(r,t):return next(x for x in r['rows'] if abs(x['tau']-t)<1e-10)
bc=at(base,18.)
convergence=[]
for r in checks:
    q=at(r,18.)
    convergence.append(dict(cells=r['cells'],modes=r['modes'],rtol=r['rtol'],phase_noise=r['phase_noise'],edge_cutoff=r['edge_cutoff'],
        spectral_ratio_change=q['spectral_ratio']/bc['spectral_ratio']-1,
        deficit_change=q['phase_energy_deficit']/bc['phase_energy_deficit']-1,
        n2_change=q['n2_variance']/bc['n2_variance']-1,p2_change=q['p2_variance']/bc['p2_variance']-1))
comparisons=[]
for r in full+edge:
    q=at(base if r['chirped'] else unchirped,r['tau']);factor=(.05/r['epsilon'])**2
    d={k:r[k] for k in ['epsilon','tau','chirped','smoothing','n','window','steps']}
    d.update(n2_full_over_reduced=r['full']['n2_variance']/q['n2_variance'],
        n2_intensity_only_over_reduced=r['intensity_only']['n2_variance']/q['n2_variance'],
        p2_full_over_reduced=r['full']['p2_variance']/(q['p2_variance']*factor),
        p2_intensity_only_over_reduced=r['intensity_only']['p2_variance']/(q['p2_variance']*factor),
        matched_phase_over_reduced=r['full']['matched_phase_variance']/(q['matched_phase_variance']*factor),
        deficit_over_reduced=r['full']['phase_energy_deficit']/q['phase_energy_deficit'])
    comparisons.append(d)
fullbase=next(r for r in full if r['epsilon']==.05 and r['tau']==2 and r['chirped'] and not r['smoothing'])
smoothbase=next(r for r in full if r['smoothing']==.02)
fullconv=[]
for r in fc+edge:
    if r['tau']!=2 or not r['chirped']:continue
    ref=smoothbase if r['smoothing']==.02 else fullbase
    row={k:r[k] for k in ['n','window','steps','smoothing']}
    row.update({name:r['full'][name]/ref['full'][name]-1 for name in ['n2_variance','p2_variance','matched_phase_variance','phase_energy_deficit']})
    fullconv.append(row)
rk=[tomllib.loads(p.read_text()) for p in sorted(RAW.glob('crosscheck_rk4ip_*.toml'))]
(HERE/'rk4ip.json').write_text(json.dumps(rk,indent=2)+'\n')
out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',run_id=HERE.name,
    asymptotic_base=base,reduced_family=[{k:v for k,v in r.items() if k!='rows'} for r in main],
    reduced_convergence=convergence,fullfield_vs_reduced=comparisons,fullfield_convergence=fullconv,
    fullfield_short_gain=short,independent_solver_rk4ip=rk,counterexample_search=read('optimization'),
    maximum_CAA_relative_error=max(abs(r['full']['CAA']/r['exact_CAA']-1) for r in full+fc+edge+short),
    corrected_CPP_coefficients=[dict(tau=r['tau'],CPP_over_G_Phi2=r['CPP']/np.exp(r['tau'])/r['Phi_NL']**2,
        prediction=32/9) for r in base['rows'] if r['tau']>=12],
    retained_numerical_failures=['initial-reduced-main.json: raw midpoint Legendre leakage from energy into high-gain shape modes',
        'initial-fullfield-main.json and initial-fullfield-checks.json: continuum product-rule current readout replaced by its exact discrete gradient'],
    scope='reduced fixed low-order variance envelopes and finite spectral projection; no uniform sharp-edge full-field remainder')
(HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
config=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',date='2026-10-19',seed=191010,threads=1,
    reduced_equation='finite-volume zero-flux d_x((1-x^2)d_x); Lyapunov covariance with white ASE and rescaled (G^(1/3)n,G^(-1/3)epsilon*p)',
    projection='QR-orthonormalized sampled Legendre span l=0..4',
    fullfield_equation='du/ds=-i*(epsilon*tau/Gamma)*u_tt/2+i*tau/(Gamma*epsilon)*abs(u)^2*u+tau*u/2',
    fullfield_method='positive-step Strang tangent/transpose, exact amplifier half-step ASE; exact discrete moment gradients',
    reduced_cases=[{k:r[k] for k in ['Gamma','nsp','cells','modes','launch','last','epsilon','phase_noise','edge_cutoff','rtol']} for r in main+checks],
    fullfield_cases=[{k:r[k] for k in ['epsilon','tau','chirped','smoothing','n','window','steps','nsp']} for r in full+fc+edge+short])
(HERE/'config.json').write_text(json.dumps(config,indent=2)+'\n')
wall=sum(r['seconds'] for r in main+checks+full+fc+edge+short)+sum(r['seconds'] for r in rk)
(HERE/'meta.yaml').write_text(f'''run_id: {HERE.name}
agent: gpt-e
model: gpt-6-astra
family: gpt
date: 2026-10-19
claim: C-20261008-claude-a-02
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
solver_dirty: false
solver_used: true
implementation: independent finite-volume covariance and full-field Strang ASE; unchanged pinned solver adjoint spot check
hardware: "{platform.node()} / {platform.machine()} / {platform.platform()}"
wall_time_seconds: {wall:.3f}
raw_location: ~/analytical-nl-discovery-data/{HERE.name}/
raw_storage: interim local storage
clean_context: true
''')
print(json.dumps(dict(reduced_convergence=convergence,full_convergence=fullconv,CAA_error=out['maximum_CAA_relative_error'],CPP=out['corrected_CPP_coefficients']),indent=2))
