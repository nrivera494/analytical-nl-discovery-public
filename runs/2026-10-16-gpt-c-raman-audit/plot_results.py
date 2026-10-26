"""Figures of independent audit measurements. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
import re
import os
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/tmp/gpt-c-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150})
def rows(pattern,zn=4):
    result=[]
    for path in HERE.glob(pattern):
        r=json.loads(path.read_text())
        if not r.get('complete'):continue
        if not re.search(r'_T[0-9.]+$',r['case']['id']):continue
        cps=[c for c in r['checkpoints'] if c['zN']==zn and c['leading'] is not None]
        if cps:result.append((r['case'],cps[0]))
    return sorted(result,key=lambda row:row[0]['T0_fs'])
fig,ax=plt.subplots(1,2,figsize=(10,3.8))
for N in [3,4,4.5,6,8]:
    r=rows(f'bw_N{N}_T*.json',zn=3 if N>=7 else 4)
    r=[x for x in r if x[0]['T0_fs']<1000 and x[1]['max_time_edge_fraction']<1e-6 and x[1]['max_spectral_edge_fraction']<1e-6]
    if not r:continue
    T=np.array([c['T0_fs'] for c,s in r]);f=np.array([s['leading']['f_zs'] for c,s in r])
    ax[0].plot(T,f,'o-',ms=3,label=f'N={N}')
    ax[1].plot(N*N*12.2/T,f*np.sqrt(N),'o-',ms=3,label=f'N={N}')
ax[0].set(xlabel='Launch sech duration T₀ (fs)',ylabel='Leading ZS energy fraction',xscale='log')
ax[1].axhline(1.29,color='black',ls='--',lw=1,label='Claim: 1.29')
ax[1].set(xlabel='N² τ₁ / T₀',ylabel='√N × leading energy fraction',xscale='log')
ax[0].legend(frameon=False,ncol=2);ax[1].legend(frameon=False,ncol=2)
fig.suptitle('Independent peak-share scan: zN=4 for N≤6; zN=3 for N=8')
fig.tight_layout();fig.savefig(HERE/'reference_share.png',metadata={'Author':'gpt-c; gpt-6-astra; gpt','Description':HERE.name});plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(10,3.8))
for patt,label in [('bw_N3_T*.json','Reference: β₂ only, Blow–Wood'),('smf_hc_s1_N3_T*.json','Telecom D(λ), HC + shock + loss'),('measured_hc_s1_N3_T*.json','Published broadband D(λ), HC + shock + loss')]:
    r=rows(patt);r=[x for x in r if x[0]['T0_fs']<=180]
    if not r:continue
    T=[c['T0_fs'] for c,s in r];f=[s['leading']['f_zs'] for c,s in r];e=[s['leading']['energy_zs_nJ'] for c,s in r]
    ax[0].plot(T,f,'o-',ms=3,label=label);ax[1].plot(T,e,'o-',ms=3,label=label)
ax[0].set(xlabel='Launch sech duration T₀ (fs)',ylabel='Leading energy fraction')
ax[1].axhspan(1.7,1.8,color='0.7',alpha=.4,label='Claimed 1.7–1.8 nJ scale')
ax[1].set(xlabel='Launch sech duration T₀ (fs)',ylabel='Leading local-ZS energy (nJ)')
ax[0].legend(frameon=False,fontsize=8);ax[1].legend(frameon=False,fontsize=8)
fig.suptitle('A maximum in share is not a maximum in energy (N=3, z=4 Lᴅ/N)')
fig.tight_layout();fig.savefig(HERE/'energy_counterexample.png',metadata={'Author':'gpt-c; gpt-6-astra; gpt','Description':HERE.name});plt.close(fig)
