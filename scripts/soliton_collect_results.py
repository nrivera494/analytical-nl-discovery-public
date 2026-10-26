#!/usr/bin/env python3
"""Register scalar-soliton evidence without committing raw arrays.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import hashlib,json,subprocess
from pathlib import Path
import yaml
try:
    import tomllib
except ImportError:
    import tomli as tomllib

ROOT=Path(__file__).resolve().parents[1]
DATA=Path('~/analytical-nl-discovery-data')
PREFIX='2026-10-10-gpt-b-soliton-'
IDENTITY=dict(agent='gpt-b',model='gpt-6-astra',family='gpt')
SOLVER_USED='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa'


def compact(value):
    if isinstance(value,dict):
        return {k:compact(v) for k,v in value.items() if not k.endswith('_indices')}
    if isinstance(value,list):return [compact(x) for x in value]
    return value


def recorded_time(value):
    if isinstance(value,dict):
        if 'wall_time_s' in value:return float(value['wall_time_s'])
        return sum(recorded_time(x) for x in value.values())
    if isinstance(value,list):return sum(recorded_time(x) for x in value)
    return 0.


def main():
    solver=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
    dirty=bool(subprocess.check_output(['git','-C',str(ROOT/'solver'),'status','--porcelain'],text=True).strip())
    if solver != SOLVER_USED or dirty:
        raise RuntimeError('These saved runs used the clean frozen solver commit; do not relabel them from a changed checkout.')
    scripts=sorted((ROOT/'scripts').glob('soliton_*.py'))+[ROOT/'scripts/soliton_native_check.jl']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in scripts}
    scopes={
        'kerr':'Exact ideal Kerr soliton linearization; Fourier collocation and independent squared-Jost quadrature.',
        'raman':'Frozen-Kerr soliton covariance with the symmetrized oscillator reservoir; thermal asymptotes and centered-filter optima.',
        'solver':'Physical fundamental solitons: fixed-step native RK4IP/discrete adjoints and an independently checked batched scalar pullback.',
        'gaussian':'Gaussian scattering data, inherited amplitude fluctuations, and direct filtered covariance. A coherent-sech substitution is a tested candidate, not an assumed model.',
        'anchor':'Notebook N approximately 1.969 sech launch, 10 m. The original 50 ps window and archived filter are restored for the reference comparison.',
        'perturbation':'Small shock and beta3 parity/order checks without Raman, in dimensionless scalar RK4IP.'}
    for short,description in scopes.items():
        run=PREFIX+short;raw=DATA/run;dest=ROOT/'runs'/run;dest.mkdir(exist_ok=True)
        sources={}
        for p in sorted(raw.rglob('*.json')):
            if p.name.startswith('meta'):continue
            sources[str(p.relative_to(raw))]=compact(json.loads(p.read_text()))
        for p in sorted(raw.rglob('native_summary.toml')):
            sources[str(p.relative_to(raw))]=tomllib.loads(p.read_text())
        wall=sum(recorded_time(v) for v in sources.values())
        meta=dict(run_id=run,**IDENTITY,date='2026-10-10',task='T-20261010-claude-interactive-06',
            serves='explorations/2026-10-10-gpt-b-soliton-filtered-fano.md',
            solver_commit=solver,solver_dirty=dirty,hardware='Apple M5 laptop, macOS; at most two Julia threads and one Julia process',
            wall_time_s=wall,raw_location=str(raw),description=description,
            wall_time_note='Sum of available evaluator timings, not session elapsed time; some symbolic/shooting checks did not record a timer.',
            evidence_status='proposer checks only; not independent verification',
            evaluator_sha256_note='Final evaluator files at registration, not a claim that every earlier run used these exact working-tree bytes. Frozen predictions retain their committed versions. Saved masks and distance curves are rechecked after search arithmetic changes.',
            evaluator_sha256=hashes)
        (dest/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
        (dest/'summary.json').write_text(json.dumps(dict(run_id=run,**IDENTITY,sources=sources),indent=2))
        print(run,len(sources),'sources',flush=True)
    # The preregistration now also has a frozen theoretical numerical prediction.
    dest=ROOT/'runs'/(PREFIX+'freeze');meta=yaml.safe_load((dest/'meta.yaml').read_text())
    meta['raw_location']=str(DATA/(PREFIX+'freeze'))
    meta['description']='Preregistered physical held-out case and frozen theoretical predictions; physical check is in the solver run.'
    (dest/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))


if __name__=='__main__':main()
