#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Check the global-phase DC reservoir contribution on stored covariances."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
import tomli
from readout_bounds import passive_eigenvalue

raw=Path('~/analytical-nl-discovery-data/2026-10-10-gpt-a-readout-reference')
rows=[]
for label in sys.argv[1:]:
    d=np.load(raw/(label+'.npz'));n=d['nbar'];m=len(n)
    with (raw/(label+'.toml')).open('rb') as f:c=tomli.load(f)['config']
    g=np.r_[np.zeros(m),np.sqrt(n/sum(n))]
    scale=4*sum(n)*c['gamma_per_W_m']**2*d['Cw'][0]*c['length_m']/(c['window_ps']*1e-12)
    dc=scale*np.outer(g,g)
    rest=d['Vbath']-dc
    rest_min=float(eigh(rest,subset_by_index=(0,0),eigvals_only=True)[0])
    full=float(eigh(d['V'],subset_by_index=(0,0),eigvals_only=True)[0])
    no_dc=float(eigh(d['V']-dc,subset_by_index=(0,0),eigvals_only=True)[0])
    passive=passive_eigenvalue(d['V'],n)[0]
    passive_no_dc=passive_eigenvalue(d['V']-dc,n)[0]
    assert rest_min>-1e-6 and abs(passive-passive_no_dc)<1e-9
    rows.append(dict(label=label,DC_phase_variance_eigenvalue=float(scale),
        remaining_reservoir_min_eigenvalue=rest_min,lambda_min_with_DC=full,
        lambda_min_without_DC=no_dc,passive_change=passive-passive_no_dc,
        amplitude_change=float(np.max(np.abs(dc[:m,:m])))))
result=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',checks=rows)
(raw/'DC-reservoir-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
