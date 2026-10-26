#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt."""
import json, os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-a-mpl')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
folder=Path(__file__).resolve().parent
raw=Path('~/analytical-nl-discovery-data')/folder.name
s=json.loads((folder/'summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
maincase='precompression' if 'precompression' in s['cases'] else 'primary'
d=np.loadtxt(raw/(maincase+'_spectrum.tsv'));w=d[:,0]
for offset,label,color in [(3,'Gate 15: claimed band observable','#2166ac'),(5,'Gate 20','#d95f02')]:
    power=d[:,offset]**2+d[:,offset+1]**2
    axes[0].semilogy(w[w>0],power[w>0],label=label,color=color)
if maincase=='primary' and (raw/'propagated_null_spectrum.tsv').exists():
    n=np.loadtxt(raw/'propagated_null_spectrum.tsv')
    keep=n[:,0]>0
    axes[0].semilogy(n[keep,0],n[keep,3]**2+n[keep,4]**2,'--',color='.4',label='TOD-free propagated core, gate 15')
axes[0].axvline(1/(6*.003),color='black',linestyle=':',label='Normal-dispersion band edge')
axes[0].axvline(1/(2*.003),color='.6',linestyle=':')
axes[0].set(xlim=(45,195),ylim=(1e-65,1e-41),xlabel='Dimensionless blue frequency w',ylabel='Squared spectral coefficient',title=f"Fixed-gate core leakage at xi={s['cases'][maincase]['xi']:.4g}")
axes[0].legend(fontsize=8,loc='upper right')
rows=sorted([s['cases'][k] for k in ['lower','middle','primary','upper'] if k in s['cases']],key=lambda c:c['delta3'])
for key,label,color in [('eta_gate15','Claimed gate-15 band yield','#2166ac'),('eta_resonant_gate20','Separated DW: resonant band, gate 20','#d95f02')]:
    axes[1].plot([1/c['delta3'] for c in rows],[np.log(c['metrics'][key]) for c in rows],'o-',color=color,label=label)
axes[1].set(xlabel=r'$1/\delta_3$',ylabel=r'$\ln\eta$',title=r'Recompression-end diagnostic: $\xi=3\pi/4$')
axes[1].legend(fontsize=8)
for ax in axes:ax.grid(alpha=.16)
fig.savefig(folder/'fixed_gate_counterexample.png',dpi=160,metadata={'Author':'gpt-a; gpt-6-astra; family gpt','Description':folder.name})
