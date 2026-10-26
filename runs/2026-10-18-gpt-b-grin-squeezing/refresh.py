#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Recompute diagnostics from cached raw snapshots only."""
import json,importlib.util,numpy as np
from pathlib import Path
p=Path(__file__).with_name('run.py');s=importlib.util.spec_from_file_location('independent_driver',p);d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
for f in sorted(p.parent.glob('K*.json')):
    r=json.loads(f.read_text())
    if 'records' not in r:continue
    for b in range(4):
      if not (d.DATA/(r['tag']+f'_b{b}.npz')).exists():raise RuntimeError('Missing cache; refusing a new production run: '+r['tag'])
    power=int(np.log2(r['shots']//4))
    d.twa_case(r['K'],r['E'],r['sigma'],r['launch'],r['disorder'],r['n'],r['zmax'],dt=r['dt'],power=power,loss=r['alpha'],weyl=r['weyl'])
print('Refreshed cached diagnostics; no trajectories generated')
