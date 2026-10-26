#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Additional triangle certificates for completed points with visible gaps."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse,json,time
from pathlib import Path
import numpy as np
import tomli
from readout_smooth_dual import smooth_dual

ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--wait',action='store_true');args=ap.parse_args()
with open(args.config,'rb') as f:config=tomli.load(f)
raw=Path(config['raw_location'])
for c in config['cases']:
    label=c['label'];base=raw/(label+'.bounds.json');dest=raw/(label+'.triangles.json')
    while not base.exists() and args.wait:time.sleep(5)
    if not base.exists() or dest.exists():continue
    score=json.loads(base.read_text())
    if score['gap_bound_dB']<.02:continue
    d=np.load(raw/(label+'.npz'));n=d['nbar'];a=d['V'][:len(n),:len(n)]
    start=np.load(raw/(label+'.smooth.npz'))['multipliers']
    lower,k,x,info=smooth_dual(a,n,betas=(500.,2000.,10000.),maxiter=200,start=start,triangle_core=48)
    info.update(agent='gpt-a',model='gpt-6-astra',family='gpt',label=label,bound=lower,
        rule='Refine completed baseline points whose original bound gap exceeds 0.02 dB.',
        gap_dB=float(10*np.log10(score['best_binary_F']/max(score['best_bound'],lower))))
    dest.write_text(json.dumps(info,indent=2)+'\n')
    np.savez_compressed(dest.with_suffix('.npz'),dual_K=k,multipliers=x)
    print(json.dumps(dict(label=label,bound=lower,gap_dB=info['gap_dB'])),flush=True)
