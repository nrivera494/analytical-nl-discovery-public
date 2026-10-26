"""gpt-e / gpt-6-astra / gpt. Audit tables derived only from this run."""
import json,platform
try:import tomllib
except ImportError:import tomli as tomllib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
def read(name):return json.loads((HERE/(name+'.json')).read_text())
main=read('main');extra=read('extra');checks=read('checks');raman=read('raman');bands=read('bands');vector=read('vector');cheap=read('cheap')
def fit(rows):
    x=np.log([r['y'] for r in rows]);e=np.log([r['excess'] for r in rows]);w=np.log([r['rms_width'] for r in rows])
    return dict(excess_exponent=float(np.polyfit(x,e,1)[0]),width_exponent=float(np.polyfit(x,w,1)[0]),
        ratio_min=float(min(r['ratio'] for r in rows)),ratio_max=float(max(r['ratio'] for r in rows)))
fits={str(phi):fit([r for r in main if r['phi']==phi and r['power']==2 and r['y']<=1e-4]) for phi in [.25,1.25,7.,17.]}
fits['quartic_phi7']=fit([r for r in main if r['power']==4 and r['y']<=1e-4])
fits['sech_phi7']=fit([r for r in extra if r.get('shape')=='sech'])
ref=next(r for r in main if r['phi']==7 and r['y']==1e-5 and r['power']==2)
convergence=[dict(n=r['n'],window=r['window'],steps=r['steps'],order=r['order'],relative_lambda_change=r['lambda_min']/ref['lambda_min']-1,
    relative_excess_change=r['excess']/ref['excess']-1) for r in checks if r['phi']==7 and r['y']==1e-5]
chirpbase=next(r for r in main if r['phi']==7 and r['y']==1e-3 and r['power']==2)
relaxed=[dict(chirp=r['chirp'],relative_lambda_change=r['lambda_min']/chirpbase['lambda_min']-1) for r in checks if r['chirp']]
loss=[dict(phi=r['phi'],y=r['y'],eta=.95,lambda_before=r['lambda_min'],lambda_after=.95*r['lambda_min']+.05)
      for r in main if r['phi']==7 and r['power']==2 and r['y'] in [1e-6,1e-2]]
out=dict(run_id=HERE.name,agent='gpt-e',model='gpt-6-astra',family='gpt',
    fits=fits,convergence=convergence,relaxed_chirp=relaxed,output_loss=loss,
    small_phi=[r for r in main+extra+checks if r['phi']<2],
    band_limits=bands,raman=raman,vector_max_relative_error=max(abs(r['relative_error']) for r in vector),
    cheap=cheap,core_and_edges=[r for r in main+extra+checks if r['phi']>=2 and not r['chirp']],
    retained_numerical_failures='initial-main.json: two split-step high-frequency resonances; corrected with explicit frequency-dependent step guard',
    numerical_wall_time_seconds=sum(r['seconds'] for r in main+extra+checks))
rk=[]
for f in sorted((Path('~/analytical-nl-discovery-data')/HERE.name).glob('crosscheck_rk4ip_*.toml')):
    rk.append(tomllib.loads(f.read_text()))
out['independent_solver_rk4ip']=rk
if (HERE/'optimization.json').exists():out['counterexample_search']=read('optimization')
(HERE/'rk4ip.json').write_text(json.dumps(rk,indent=2)+'\n')
(HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
config=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',date='2026-10-19',
    equation='du/ds = -i*(y/Phi)/2*u_tt + i*Phi*abs(u)^2*u',
    integration='Yoshida fourth-order composition; independent exact Kerr tangent and transpose; second-order Strang cross-check',
    eigensolver='ARPACK largest eigenvalues of M M^T; symplectic reciprocity and direct adjoint norm check',
    seeds=[191004,191005,191006],shot_noise=1,threads=1,
    actual_cases=[{k:r[k] for k in ['phi','y','power','n','window','steps','chirp','order']} for r in main+extra+checks],
    rerun=['run.py --suite main','run.py --suite checks','run.py --suite extra','auxiliary.py --suite raman','auxiliary.py --suite bands','auxiliary.py --suite vector','cheap_checks.py','summarize.py'])
(HERE/'config.json').write_text(json.dumps(config,indent=2)+'\n')
meta=f'''run_id: {HERE.name}
agent: gpt-e
model: gpt-6-astra
family: gpt
date: 2026-10-19
claim: C-20261010-claude-a-01
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
solver_dirty: false
solver_used: true
implementation: independent Python Fourier tangent, exact shear and Jones tangent ODE; unchanged pinned solver discrete-RK4IP adjoint cross-check
hardware: "{platform.node()} / {platform.machine()} / {platform.platform()}"
wall_time_seconds: {out['numerical_wall_time_seconds']:.3f}
raw_location: ~/analytical-nl-discovery-data/{HERE.name}/
raw_storage: interim local storage
clean_context: true
'''
(HERE/'meta.yaml').write_text(meta)
print(json.dumps({k:out[k] for k in ['fits','convergence','relaxed_chirp','vector_max_relative_error']},indent=2))
