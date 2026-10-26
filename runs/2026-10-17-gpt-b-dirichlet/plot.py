#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RUN=Path(__file__).resolve().parent
d=json.loads((RUN/'summary.json').read_text())
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
ax.axhline(1,color='black',lw=1.4,label='Exact Dirichlet prediction')
for sig,color,mark,label in [(.3,'#1f77b4','o',r'$\sigma=0.3$, $s=2000$--$8000$'),
                            (3.,'#c45a19','s',r'$\sigma=3$, $s=8000$--$24000$')]:
    rr=[r for r in d['groups'] if r['sigma']==sig and r['dt']==.04 and r['K']==5
        and r['end']==(8000 if sig==.3 else 24000)]
    if not rr:continue
    ax.errorbar([r['E']+(-.006 if sig==.3 else .006) for r in rr],
        [r['variance_ratio'] for r in rr],yerr=[2*r['variance_ratio_se'] for r in rr],
        fmt=mark,color=color,capsize=3,ms=6,label=label,linestyle='none')
rr=[r for r in d['groups'] if r['held_out'] and r['dt']==.04]
ax.errorbar([r['E'] for r in rr],[r['variance_ratio'] for r in rr],
    yerr=[2*r['variance_ratio_se'] for r in rr],fmt='D',mfc='white',mec='#1f77b4',
    color='#1f77b4',capsize=3,ms=7,label='Held out: 10 and 21 modes')
if d.get('phase_followup'):
    p=next(r for r in d['phase_followup']['rows'] if r['tag']=='fresh_heldout')
    ax.errorbar([p['E']],[p['pooled'][1]/p['prediction'][1]],
        yerr=[2*p['se'][1]/p['prediction'][1]],fmt='^',mfc='white',
        color='#7e4c9a',capsize=3,ms=7,label='Phase holdout: 400 launches')
ax.set(xlabel=r'Excitation energy $E^{\prime}/(\kappa N)$',
       ylabel=r'Condensate variance / Dirichlet variance',xlim=(.23,.97),ylim=(.5,1.48))
ax.legend(fontsize=9,frameon=False);ax.grid(alpha=.18)
fig.savefig(RUN/'fig_summary.png',dpi=130,metadata={'Description':json.dumps(IDENTITY)})
