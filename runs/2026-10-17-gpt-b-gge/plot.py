#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Phase-dependent endpoints."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from summarize import time_stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RUN=Path(__file__).resolve().parent
s=json.loads((RUN/'summary.json').read_text());p=json.loads((RUN/'final_predictions.json').read_text())['rows']
sector=json.loads((RUN/'reflection_summary.json').read_text())['rows']
resolution=json.loads((RUN/'resolution_summary.json').read_text()) if (RUN/'resolution_summary.json').exists() else {}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
for E,seeds,xx in [(.6,[4101,4103,4104,0],np.arange(4)),(.9,[4201,4204,0],np.arange(3)+5)]:
    observed=[];errors=[];h=[];hl=[]
    for seed in seeds:
        tag='phase4103' if seed==4103 else 'perturbed_1e-4' if seed==0 else None
        newer=[r for r in resolution.get('deterministic',[]) if r['tag']==tag] if E==.6 and resolution.get('complete') else []
        if newer:
            r=min(newer,key=lambda r:r['dt']);observed.append(r['mean']);errors.append(r['se'])
        elif seed:
            rows=[r for r in s['deterministic'] if r['case']['E']==E and r['case']['seed']==seed and r['zmax']==240000]
            r=min(rows,key=lambda r:r['dt']);observed.append(r['mean']);errors.append(r['se'])
        else:
            r=next(r for r in sector if r['E']==E and r['variant']=='perturbed_1e-4')
            st=time_stats(r['raw_file'],80000);observed.append(st['mean']);errors.append(st['se'])
        for include_L,dest in [(False,h),(True,hl)]:
            r=next(r for r in p if r['E']==E and r['seed']==seed and r['include_L']==include_L)
            dest.append(r['widths'][-1]['mean'])
    rj=dirichlet_moments(Model(5).q,E)['mean'][0]
    ax.plot([xx[0]-.3,xx[-1]+.3],[rj,rj],color='#666666',ls=':',lw=1.5,label='RJ' if E==.6 else None)
    ax.plot(xx,h,'--',color='#c45a19',lw=1.3,label='GGE: N, E, H' if E==.6 else None)
    ax.plot(xx,hl,'-',color='#1b8a72',lw=1.5,label='GGE: N, E, H, L' if E==.6 else None)
    ax.errorbar(xx,observed,yerr=2*np.array(errors),fmt='o',color='#1f4e79',
        mfc='white' if E==.9 else '#1f4e79',capsize=3,ms=6,
        label='Simulation' if E==.6 else 'Held-out geometry')
ax.axvline(4,color='#bbbbbb',lw=.8)
ax.text(1.5,.79,r'$E^{\prime}/(\kappa N)=0.6$',ha='center',fontsize=9)
ax.text(6,.79,r'$E^{\prime}/(\kappa N)=0.9$',ha='center',fontsize=9)
ax.set(xticks=[0,1,2,3,5,6,7],xticklabels=['P1','P3','P4',r'A+$\epsilon$','H1','H4',r'A+$\epsilon$'],
       xlabel='Input phase configuration (same powers within each group)',
       ylabel=r'Long-time condensate fraction $\langle I_0\rangle/N$',ylim=(.48,.81))
ax.grid(axis='y',alpha=.18);ax.legend(fontsize=8.5,frameon=False,loc='lower left',ncol=2)
fig.savefig(RUN/'fig_summary.png',dpi=130,metadata={'Description':json.dumps(IDENTITY)})
