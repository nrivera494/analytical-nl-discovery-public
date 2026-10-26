#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Run explicitly labeled Gaussian counting diagnostics as covariances arrive."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse,time
from pathlib import Path
import numpy as np
import tomli
from readout_gaussian_counting import gaussian_count_case

ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--core',action='store_true');ap.add_argument('--wait',action='store_true');args=ap.parse_args()
with open(args.config,'rb') as f:c=tomli.load(f)
raw=Path(c['raw_location'])
for case in c['cases']:
    label=case['label']
    data=raw/(label+('.core.npz' if args.core else '.npz'))
    ready=raw/(label+('.core.score.npz' if args.core else '.bounds.npz'))
    target=data.with_suffix('.gaussian.json')
    while not ready.exists() and args.wait:time.sleep(5)
    if not ready.exists() or target.exists():continue
    with np.load(data) as d:
        if 'V' not in d or d['V'].shape!=(2*len(d['nbar']),2*len(d['nbar'])):continue
    gaussian_count_case(data,do_bound=args.core)
