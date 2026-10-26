"""Thermalization ensembles E1-E5 of predictions.md (run serially). Output: ensemble_thermalization.jsonl (one line per run, appended),
raw mode-power series (every 2 L_NL, float32) in RAW. Resumable: runs already in the jsonl are skipped."""
import json, os, sys, numpy as np, warnings
warnings.filterwarnings('ignore')
import ens_model as em
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-ensemble-thermalization'); os.makedirs(RAW, exist_ok=True)
OUT = 'ensemble_thermalization.jsonl'
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['tag'])
jobs = []
for Ep in [0.3, 0.6, 0.9]:
    for i in range(12): jobs.append(dict(ens='E1', kind='deph', Ep=Ep, phase_seed=1, sigma=0.3, dis_seed=101 + i, vac_seed=None))
    for i in range(12): jobs.append(dict(ens='E2', kind='deph', Ep=Ep, phase_seed=201 + i, sigma=0.3, dis_seed=7, vac_seed=None))
    for i in range(12): jobs.append(dict(ens='E3', kind='deph', Ep=Ep, phase_seed=201 + i, sigma=0.0, dis_seed=None, vac_seed=None))
for i in range(12): jobs.append(dict(ens='E4', kind='G1', Ep=1.0, phase_seed=1, sigma=0.3, dis_seed=101 + i, vac_seed=301 + i))
for i in range(12): jobs.append(dict(ens='E4', kind='G1', Ep=1.0, phase_seed=201 + i, sigma=0.0, dis_seed=None, vac_seed=301 + i))
for Ep in [0.6, 0.9]:
    for i in range(12): jobs.append(dict(ens='E5', kind='focused', Ep=Ep, phase_seed=1, sigma=0.3, dis_seed=101 + i, vac_seed=None))
    jobs.append(dict(ens='E5', kind='focused', Ep=Ep, phase_seed=1, sigma=0.0, dis_seed=None, vac_seed=None))
if len(sys.argv) > 1 and sys.argv[1] == 'smoke':
    j = jobs[0]; dis = em.WhiteDisorder(j['sigma'], j['dis_seed'], 0.05)
    r = em.run(j['kind'], j['Ep'], j['phase_seed'], disorder=dis, zmax=60., W=(10., 60.)); print('smoke', json.dumps(r)[:400]); sys.exit()
for j in jobs:
    tag = f"{j['ens']}_{j['kind']}_E{j['Ep']}_s{j['sigma']}_ph{j['phase_seed']}_dis{j['dis_seed']}_vac{j['vac_seed']}"
    if tag in done: continue
    dis = em.WhiteDisorder(j['sigma'], j['dis_seed'], 0.05) if j['sigma'] > 0 else None
    r = em.run(j['kind'], j['Ep'], j['phase_seed'], disorder=dis, vac_seed=j['vac_seed'], raw_path=os.path.join(RAW, tag + '.npz'))
    r.update(tag=tag, ens=j['ens'], sigma=j['sigma'], dis_seed=j['dis_seed'])
    with open(OUT, 'a') as f: f.write(json.dumps(r) + '\n')
    print(f"{tag}: <I0> {r['I0']:.4f} (D {r['I0_D']:.4f}) g2 {r['g2_ex']:.3f} VarI0/D {r['VarI0']/r['VarI0_D']:.2f} D_RJ {r['D_RJ']:.3f} L_rel {r['L_rel']} z_on {r['z_on']} [{r['wall_s']:.0f}s]", flush=True)
