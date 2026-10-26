"""Scientific audit figures, gpt-d/gpt-6-astra/gpt."""
from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).parent;root=base.parent
def read(slug):return json.loads((root/('2026-10-16-gpt-d-'+slug)/'summary.json').read_text())
r=read('cutoff-edge200-window');t=read('silica-terminal');pred=json.loads((base/'predictions.json').read_text())['cases']['silica_terminal'];cp=json.loads((base/'cutoff_long_predictions.json').read_text())['cases'][0]
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,axs=plt.subplots(1,2,figsize=(10.2,4.1),layout='constrained')
ax=axs[0];ax.plot([p['z'] for p in r['records']],[p['eta']['2.001'] for p in r['records']],lw=2,color='#20679c',label='Independent GNLSE')
ax.axvline(98,color='#20679c',ls='--',lw=1.2,label='Measured optimum')
ax.axvline(cp['closed_L_m'],color='#ac422e',ls=':',lw=2,label='Closed-form prediction')
ax.set(xlabel='Fibre length (m)',ylabel='Photons beyond cutoff / launched photons',xlim=(0,310),ylim=(.35,.71),title='Silica: the length prediction fails')
ax.legend(frameon=False,fontsize=8.5,loc='lower left');ax.grid(alpha=.15)
ax=axs[1];wi=pred['terminal']['omega_inf'];we=pred['terminal']['w_eff'];N=np.array(pred['planes']['N_ratio']);om=2*np.pi*299.792458/np.array(pred['planes']['lambda_um']);z=np.array(pred['planes']['z']);valid=(z<=500)&(om>wi+1e-7)
ax.loglog((om[valid]-wi)/we,N[valid],color='#202020',lw=1.5,label='Frozen Gordon ODE')
for tag,c,mark,keep in [('GNLSE: adiabatic','#20679c','o',True),('GNLSE: outside bound','#ad7a32','x',False)]:
 p=[p for p in t['records'] if (p['alpha_z0']<=.01)==keep and p['omega']>wi]
 ax.loglog([(p['omega']-wi)/we for p in p],[p['N_ratio'] for p in p],mark,ms=3,label=tag,alpha=.8)
ax.set(xlabel=r'$(\bar\omega-\omega_\infty)/w_{\rm eff}$ (frozen terminal)',ylabel=r'$N/N_0$',title='A terminal quarter power is not verified')
ax.legend(frameon=False,fontsize=8.5,loc='lower right');ax.grid(alpha=.15,which='both')
fig.savefig(base/'audit_summary.png',dpi=200,metadata={'Software':'gpt-d; gpt-6-astra; gpt'})
fig.savefig(base/'audit_summary.svg',metadata={'Creator':'gpt-d; gpt-6-astra; gpt'})
print('Saved audit_summary.png and audit_summary.svg')
