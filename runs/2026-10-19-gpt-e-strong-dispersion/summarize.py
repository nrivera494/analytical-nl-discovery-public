"""gpt-e / gpt-6-astra / gpt. Independent strong-dispersion audit metrics."""
import json,platform
try:import tomllib
except ImportError:import tomli as tomllib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;RAW=Path('~/analytical-nl-discovery-data')/HERE.name
def read(n):return json.loads((HERE/(n+'.json')).read_text())
main=read('main');checks=read('checks');edges=read('edges')
hydros=[json.loads(p.read_text()) for p in sorted(HERE.glob('hydro-n*.json'))]
fine=next(x for x in hydros if x['rows'][0]['n']==512 and x['rows'][0]['window']==12.)
convergence=[]
for row in checks:
    base=next(r for r in main if r['N']==row['N'] and r['Z']==row['Z'])
    convergence.append({k:row[k] for k in ['N','Z','n','window','steps','order','chirp']})
    convergence[-1].update(relative_lambda_change=row['lambda_min']/base['lambda_min']-1,
        relative_C_change=row['C_inverse_norm_squared']/base['C_inverse_norm_squared']-1)
fits=[]
for z in [.45,.9]:
    lam=next(r['Lambda'] for r in fine['rows'] if r['Z']==z)
    rows=sorted([r for r in main if r['Z']==z],key=lambda r:r['N'])
    Ns=np.array([r['N'] for r in rows]);deficit=1-np.array([r['N2_lambda_min'] for r in rows])/lam
    fits.append(dict(Z=z,independent_hydro_Lambda=lam,Ns=Ns.tolist(),relative_deficits=deficit.tolist(),
        fitted_exponent=float(np.polyfit(np.log(Ns),np.log(deficit),1)[0]),
        c_estimates=(deficit*(Ns*z)**2).tolist(),includes_below_phi_threshold=bool(z==.45)))
corrected=[]
for r in main:
    replacements=[q for q in checks if q['N']==r['N'] and q['Z']==r['Z'] and q['n']==2048 and q['window']==24 and q['chirp']==0]
    corrected.append(replacements[0] if replacements else r)
rk=[tomllib.loads(p.read_text()) for p in sorted(RAW.glob('crosscheck_rk4ip_*.toml'))]
(HERE/'rk4ip.json').write_text(json.dumps(rk,indent=2)+'\n')
theorem=read('theorem');ep=np.array([r['epsilon'] for r in theorem]);de=np.array([r['relative_deficit'] for r in theorem])
out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',run_id=HERE.name,core=corrected,
    independent_hydro=hydros,prebreaking_fits=fits,convergence=convergence,edges=edges,
    maximum_passive_vs_second_relative_error=max(abs(r['pass_vs_second']) for r in corrected+edges+checks),
    independent_solver_rk4ip=rk,theorem_counterexample=theorem,
    theorem_counterexample_relative_exponent=float(np.polyfit(np.log(ep),np.log(de),1)[0]),
    output_loss=[dict(N=r['N'],Z=r['Z'],eta=.95,lambda_before=r['lambda_min'],lambda_after=.95*r['lambda_min']+.05)
        for r in corrected if r['N']==20 and r['Z'] in [.9,2.3]])
if (HERE/'optimization.json').exists():out['counterexample_search']=read('optimization')
(HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
config=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',date='2026-10-19',seeds=[191004,191005,191007],
    equation='du/ds=-i*(Z/N)/2*u_tt+i*N*Z*abs(u)^2*u',
    readout='unrestricted homodyne; exact compression orthogonal to i*mean for passive readout',
    numerical_method='fourth-order Fourier symplectic tangent; independent epsilon=0 pseudospectral DOP853 hydro; pinned solver discrete RK4IP adjoint',
    threads=1,actual_cases=[{k:r[k] for k in ['N','Z','n','window','steps','chirp','order']} for r in main+checks+edges],
    hydro_cases=[dict(n=x['rows'][0]['n'],window=x['rows'][0]['window'],rtol=x['rows'][0]['rtol']) for x in hydros])
(HERE/'config.json').write_text(json.dumps(config,indent=2)+'\n')
wall=sum(r['seconds'] for r in main+checks+edges)+sum(x['seconds'] for x in hydros)+sum(x['seconds'] for x in rk)
(HERE/'meta.yaml').write_text(f'''run_id: {HERE.name}
agent: gpt-e
model: gpt-6-astra
family: gpt
date: 2026-10-19
claim: C-20261010-claude-b-01
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
solver_dirty: false
solver_used: true
implementation: independent Fourier tangent and zero-dispersion hydrodynamics; unchanged pinned solver spot check
hardware: "{platform.node()} / {platform.machine()} / {platform.platform()}"
wall_time_seconds: {wall:.3f}
raw_location: ~/analytical-nl-discovery-data/{HERE.name}/
raw_storage: interim local storage
clean_context: true
''')
print(json.dumps(dict(fits=fits,convergence=convergence,passive_error=out['maximum_passive_vs_second_relative_error'],rk4ip=rk),indent=2))
