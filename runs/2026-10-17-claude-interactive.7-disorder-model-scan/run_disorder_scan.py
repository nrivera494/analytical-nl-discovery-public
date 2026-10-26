"""Disorder-strength and correlation-length scan of predictions.md (run serially). White sigma = 0.3 with dis_seed 101-106 is not rerun:
it is ensemble E1 (E' = 0.6, first six seeds) of runs/2026-10-17-claude-interactive.7-ensemble-thermalization, identical code and seeds.
Output: disorder_scan.jsonl (appended; resumable), raw series in RAW."""
import json, os, sys, numpy as np, warnings
warnings.filterwarnings('ignore')
import ens_model as em
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-disorder-model-scan'); os.makedirs(RAW, exist_ok=True)
OUT = 'disorder_scan.jsonl'
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['tag'])
jobs = []
for sig in [0.1, 1.0, 3.0]:
    for i in range(6): jobs.append(dict(set='S1', kind='deph', model='white', sigma=sig, lc=None, dis_seed=101 + i, vac_seed=None))
for lc in [0.1, 1.0, 10.0, 100.0]:
    for i in range(6): jobs.append(dict(set='S2', kind='deph', model='piecewise', sigma=0.3, lc=lc, dis_seed=101 + i, vac_seed=None))
for lc in [0.1, 1.0, 10.0]:
    for i in range(6): jobs.append(dict(set='S3', kind='deph', model='piecewise', sigma=1.0, lc=lc, dis_seed=101 + i, vac_seed=None))
for (model, sig, lc) in [('white', 0.1, None), ('white', 1.0, None), ('white', 3.0, None), ('piecewise', 0.3, 10.0)]:
    for i in range(6): jobs.append(dict(set='G', kind='G1', model=model, sigma=sig, lc=lc, dis_seed=101 + i, vac_seed=301 + i))
def make(j, dz):
    return em.WhiteDisorder(j['sigma'], j['dis_seed'], dz) if j['model'] == 'white' else em.PiecewiseDisorder(j['sigma'], j['lc'], j['dis_seed'], dz)
if len(sys.argv) > 1 and sys.argv[1] == 'smoke':
    for j in [jobs[12], jobs[24]]:
        r = em.run(j['kind'], 0.6, 1, disorder=make(j, 0.05), zmax=60., W=(10., 60.)); print('smoke', j['model'], j['sigma'], j['lc'], round(r['I0'], 4), round(r['wall_s'], 1))
    sys.exit()
for j in jobs:
    dz = 0.02 if (j['model'] == 'white' and j['sigma'] >= 3) else 0.05
    tag = f"{j['set']}_{j['kind']}_{j['model']}_s{j['sigma']}_lc{j['lc']}_dis{j['dis_seed']}_vac{j['vac_seed']}"
    if tag in done: continue
    Ep = 1.0 if j['kind'] == 'G1' else 0.6
    r = em.run(j['kind'], Ep, 1, disorder=make(j, dz), vac_seed=j['vac_seed'], dz=dz, raw_path=os.path.join(RAW, tag + '.npz'))
    r.update(tag=tag, set=j['set'], model=j['model'], sigma=j['sigma'], lc=j['lc'], dis_seed=j['dis_seed'], dz=dz)
    with open(OUT, 'a') as f: f.write(json.dumps(r) + '\n')
    print(f"{tag}: <I0> {r['I0']:.4f} (D {r['I0_D']:.4f}) g2 {r['g2_ex']:.3f} VarI0/D {r['VarI0']/r['VarI0_D']:.2f} D_RJ {r['D_RJ']:.3f} L_rel {r['L_rel']} z_on {r['z_on']} [{r['wall_s']:.0f}s]", flush=True)
