#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Optimize a core mask and a candidate dual; Julia checks the dual on all bins."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse
import json
from pathlib import Path
import numpy as np
from scipy import linalg as la
from readout_bounds import binary_search, eigenvector_bound, moment_certificate
from readout_smooth_dual import smooth_dual

ap=argparse.ArgumentParser();ap.add_argument('path');args=ap.parse_args()
path=Path(args.path);d=np.load(path);a=d['A'];n=d['nbar']
bound,info,rounded,seeds=eigenvector_bound(a,n)
found,mask,search=binary_search(a,n,seeds)
base=float(la.eigh(a,subset_by_index=(0,0),eigvals_only=True)[0])
relaxed,k,rd=moment_certificate(a,n,found,base,max_core=min(len(n),96))
smooth,sk,_,sd=smooth_dual(a,n)
if smooth>relaxed: relaxed,k=smooth,sk
report=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',best_binary_F=found,
    core_only_lambda_gen=base,core_only_dual_value=relaxed,
    caveat='Core lower values are not global bounds; the candidate K must be checked on the full operator.',
    eigenvector_certificate=info,search=search,moment=rd,smooth=sd,
    transmitted_photons=float(n@mask),transmitted_fraction=float(n@mask/np.sum(d['nbar_full'])))
path.with_suffix('.score.json').write_text(json.dumps(report,indent=2)+'\n')
np.savez_compressed(path.with_suffix('.score.npz'),dual_K=k,mask=mask.astype(float),best_binary_F=np.array([found]))
print(json.dumps(dict(core_bins=len(n),best_binary_F=found,core_only_dual_value=relaxed)),flush=True)
