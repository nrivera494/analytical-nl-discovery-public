#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Small shareable figures sourced only from the registered summary."""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-a-matplotlib')
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

run=Path(__file__).resolve().parents[1]/'runs'/'2026-10-10-gpt-a-readout-reference'
s=json.loads((run/'summary.json').read_text())
rows=[r for r in s['reference'] if r['config']['raman']]
x=np.arange(len(rows))
labels=[r['label'].replace('anom_','A ').replace('normal_','N ').replace('displess_phi','D Φ').replace('_R','').replace('_',' ') for r in rows]
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,(ax,gap)=plt.subplots(2,1,figsize=(12,8),sharex=True,gridspec_kw={'height_ratios':[2,1]})
for key,label,color,style in [('lambda_min','Field minimum','#777777','-'),
    ('lambda_pass','Passive limit','#a96a0f','--'),('lambda_gen','Generalized counting','#377eb8','-'),
    ('best_bound','Binary lower bound','#238b45','-'),('best_binary_F','Best binary found','#111111',':')]:
    ax.plot(x,10*np.log10([r[key] for r in rows]),style,color=color,marker='o',ms=3,label=label)
for i,r in enumerate(rows):
    if r['faint_formal_mask']:
        ax.axvspan(i-.3,i+.3,color='#d95f02',alpha=.12)
        ax.annotate('faint',(i,10*np.log10(r['best_binary_F'])),xytext=(0,10),textcoords='offset points',ha='center',color='#b34c00',fontsize=8)
ax.set_ylabel('Normalized variance / Fano factor (dB)')
ax.set_title('Raman at 300 K: formal finite-grid readout hierarchy',loc='left',fontweight='bold')
ax.legend(ncol=3,fontsize=9,loc='lower left')
ax.grid(axis='y',alpha=.2)
for key,label,color in [('gap_min_dB','Field gap','#777777'),('gap_gen_dB','Generalized gap','#377eb8'),('gap_bound_dB','Binary-bound gap','#238b45')]:
    gap.plot(x,np.maximum(1e-7,[r[key] for r in rows]),color=color,marker='o',ms=3,label=label)
gap.set_yscale('log');gap.set_ylabel('Gap to best mask (dB)')
gap.set_xticks(x,labels,rotation=55,ha='right');gap.grid(axis='y',alpha=.2)
gap.legend(ncol=3,fontsize=9,loc='lower right')
fig.text(.01,.005,'Run 2026-10-10-gpt-a-readout-reference · A: anomalous; N: normal; D: dispersionless. Shaded masks are too faint for a counting upper value.\nThese are discretized-model scores; see the convergence table and Gaussian-count diagnostic.',fontsize=8,color='#444444')
fig.tight_layout(rect=(0,.055,1,1))
fig.savefig(run/'readout-hierarchy.png',dpi=160)
fig.savefig(run/'readout-hierarchy.svg')
plt.close(fig)

audit=s['checks'].get('fixed-filter-step-audit')
if audit and audit.get('rows'):
    rr=audit['rows'];steps=np.array([r['steps'] for r in rr])
    fig,(ax,bx)=plt.subplots(1,2,figsize=(10,4))
    ax.semilogx(steps,[r['dark_F'] for r in rr],'o-',label='Fixed faint mask',color='#b34c00')
    ax.semilogx(steps,[r['bright_F'] for r in rr],'o-',label='Fixed bright mask',color='#238b45')
    ax.axhline(1,color='#777777',lw=.7);ax.set_xlabel('Propagation steps');ax.set_ylabel('Linearized Fano factor');ax.legend(fontsize=9)
    ax.set_title('A coarse optimum can be a step artifact',loc='left',fontsize=11)
    target=rr[-1]['bright_F']
    bx.loglog(steps[:-1],np.maximum(1e-16,[abs(r['bright_F']-target) for r in rr[:-1]]),'o-',color='#238b45')
    bx.set_xlabel('Propagation steps');bx.set_ylabel('Bright-mask error versus finest step')
    bx.set_title('Fixed-mask convergence',loc='left',fontsize=11)
    for axis in (ax,bx):axis.grid(alpha=.2)
    fig.suptitle('Anomalous N=1, z/z₀=0.75, Raman · fixed window and bath quadrature',fontsize=11)
    fig.tight_layout();fig.savefig(run/'fixed-filter-convergence.png',dpi=160);fig.savefig(run/'fixed-filter-convergence.svg');plt.close(fig)
print('Wrote reference figures from',len(rows),'Raman points.')
