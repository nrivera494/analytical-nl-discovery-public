"""Scientific summary figure. gpt-d / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).parent;math=json.loads((base/'math_summary.json').read_text());agg=json.loads((base/'summary.json').read_text())
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,ax=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
d=math['responses']['S28'];r=np.array([q['T_over_tau1'] for q in d['cases']]);y=np.array([q['ratio'] for q in d['cases']])
ax[0].loglog(r,y,'o-',color='#175b8c',label='Independent oscillator quadrature',lw=1.6,ms=4)
x=np.geomspace(10,160,80);A=d['tau1_fs']/d['tau2_fs'];coef=16*A/(15*(1+A*A)**2)
ax[0].loglog(x,coef/x**3,'--',color='#da6a20',label=r'Correct $T^{-3}$ asymptote')
ax[0].loglog(x,y[list(r).index(10)]*(x/10)**-2,':',color='#a94040',label=r'Card: $T^{-2}$ (matched at 10)')
ax[0].axhline(1,color='.5',lw=.8);ax[0].set(xlabel=r'Sech width $T/\tau_1$',ylabel=r'Rate / bound, $-E^\prime/(\kappa_U E^2)$',title='The stated tightness scaling fails',ylim=(2e-8,1.8))
ax[0].legend(fontsize=8.5,loc='lower left');ax[0].text(.98,.97,'Measured decay exponent: 3.0016\nCard: 2',ha='right',va='top',transform=ax[0].transAxes,fontsize=10)
slugs=['core','heldout4','heldout6-fine','heldout6long','own'];labels=['Core','N=4','N=6','N=6, long','Pulse pair'];actual=[];bound=[]
for q in slugs:
 a=agg['runs']['2026-10-16-gpt-d-c02-'+q];actual.append(a['E_L_over_E0']);bound.append(a['retention_bound_at_L'])
xx=np.arange(len(labels));ax[1].bar(xx-.18,actual,.36,color='#175b8c',label='Independent propagation');ax[1].bar(xx+.18,bound,.36,color='#c7cdd3',label='Proved lower bound')
ax[1].set(xticks=xx,xticklabels=labels,ylim=(0,1.13),ylabel=r'Retained energy $E_L/E_0$',title='The exact retention bound holds');ax[1].legend(loc='upper left',fontsize=9)
fig.suptitle('Claim 02: valid energy bound, incorrect long-pulse scaling',fontsize=15)
for ext in ['png','svg']:fig.savefig(base/('audit_summary.'+ext),dpi=180,metadata={'Creator':'gpt-d; gpt-6-astra; gpt'})
