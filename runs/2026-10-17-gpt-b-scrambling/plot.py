#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RUN=Path(__file__).resolve().parent;d=json.loads((RUN/'summary.json').read_text())
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
for fit,color,marker in zip(d['fits'],['#1f77b4','#c45a19'],['o','s']):
    seed=fit['disorder_seed'];rr=[r for r in d['rows'] if not r['dephased'] and r['dt']==.04 and r['disorder_seed']==seed and r['crossing'] is not None]
    for held in [False,True]:
        r=[r for r in rr if (r['n'] in [1e7,1e12])==held]
        ax.errorbar(np.log([x['n'] for x in r]),[x['crossing'] for x in r],
            yerr=[2*x['crossing_se'] for x in r],fmt=marker,color=color,
            mfc='white' if held else color,capsize=2,ms=6,
            label=f'Disorder {seed-7500}'+(' (held out)' if held else ''))
    x=np.linspace(np.log(1e6),np.log(1e12),100)
    # Tangent-predicted slope; intercept fixed by the core n=1e8 crossing.
    anchor=next(r for r in rr if r['n']==1e8)
    ax.plot(x,anchor['crossing']+fit['predicted_slope']*(x-np.log(1e8)),color=color,lw=1.4,
            label=r'$1/(2\lambda_1L_{\rm NL})$ slope' if seed==7501 else None)
fine=[r for r in d['rows'] if not r['dephased'] and r['dt']==.02]
if fine:
    ax.errorbar(np.log([r['n'] for r in fine]),[r['crossing'] for r in fine],
        yerr=[2*r['crossing_se'] for r in fine],fmt='x',color='black',ms=7,
        label='Disorder 1: half step')
ax.set(xlabel=r'Log photon number $\ln n$',ylabel=r'Half-coherence length $z_{1/2}/L_{\rm NL}$')
ax.grid(alpha=.18);ax.legend(fontsize=8.5,frameon=False)
fig.savefig(RUN/'fig_summary.png',dpi=130,metadata={'Description':json.dumps(IDENTITY)})
