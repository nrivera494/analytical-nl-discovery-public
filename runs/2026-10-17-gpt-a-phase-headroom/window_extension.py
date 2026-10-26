#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Bounded post-run N=5 window diagnosis; frozen coefficients, no tuning."""
from qualify import safe_case
from postprocess import *
labels=[]
for width,smooth in [(640,False),(320,True),(640,True)]:
    label=f'diagnostic_N5_window{width}_'+('C2' if smooth else 'clipped')
    safe_case(label,N=5,T0=280,mask=str(HERE/'selected_N5_coef.csv'),
              nt=65536 if width==640 else 32768,width=width,hfac=1.,smooth_mask=smooth)
    labels.append(label)
path=HERE/'readout_checks.json';data=json.loads(path.read_text())
for label in labels:
    data['cases'][label]=readout_checks(label,census=True,refine_checks=True)
    path.write_text(json.dumps(data,indent=2)+'\n')
    print('DIAGNOSTIC',label,data['cases'][label]['f_zs_extrapolated'],
          data['cases'][label]['reddest_resolved_soliton_is_tallest'],flush=True)
