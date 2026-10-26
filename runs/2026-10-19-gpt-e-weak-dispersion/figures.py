"""gpt-e / gpt-6-astra / gpt. Plot only the auditor's recorded numerical data."""
import os
os.environ['MPLCONFIGDIR']='/private/tmp/gpt-e-matplotlib'
os.environ['OPENBLAS_NUM_THREADS']='1'
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                     'figure.dpi':140,'savefig.dpi':170})
def read(p):return json.loads(p.read_text())
def save(fig,folder,title):
    fig.suptitle(title,fontsize=14)
    fig.text(.5,.015,f'{folder.name} | gpt-e / gpt-6-astra',ha='center',fontsize=8,color='.35')
    fig.tight_layout(rect=(0,.04,1,.94))
    fig.savefig(folder/'audit.png',facecolor='white')
    plt.close(fig)

data=read(HERE/'main.json')
fig,ax=plt.subplots(1,2,figsize=(10,4.5))
for power,label,c in [(2,'Gaussian, phase 7','C0'),(4,'Quartic, phase 7','C1')]:
    rows=sorted([r for r in data if r['phi']==7 and r['power']==power],key=lambda r:r['y'])
    xx=[r['y'] for r in rows]
    ax[0].loglog(xx,[r['excess'] for r in rows],'o-',color=c,label=label)
    ax[0].loglog(xx,[r['prediction'] for r in rows],'--',color=c,alpha=.7)
for phi in [.25,1.25,7.,17.]:
    rows=sorted([r for r in data if r['phi']==phi and r['power']==2],key=lambda r:r['y'])
    ax[1].semilogx([r['y'] for r in rows],[r['ratio'] for r in rows],'o-',label=f'Phase {phi:g}')
ax[0].set(xlabel=r'$y$',ylabel=r'$\lambda_{\min}/V_{\min}-1$',title='Peak order changes the excess power')
ax[1].set(xlabel=r'$y$',ylabel='Measured excess / leading prediction',title='Small phase gives nonuniform accuracy')
ax[1].axhline(1,color='.5',lw=.8)
for a in ax:a.legend(fontsize=8);a.grid(alpha=.2)
save(fig,HERE,'Weak normal dispersion: independent full-grid optimization')

folder=ROOT/'2026-10-19-gpt-e-strong-dispersion'
summary=read(folder/'summary.json')
data=summary['core']
fig,axs=plt.subplots(2,2,figsize=(10,7))
for a,Z,limit in zip(axs.ravel(),[.45,.9,1.8,2.3],[1.8537250316602,.67374904967587,None,None]):
    rows=sorted([r for r in data if r['Z']==Z],key=lambda r:r['N'])
    a.plot([1/r['N']**2 for r in rows],[r['N2_lambda_min'] for r in rows],'o-',label='Full NLSE tangent')
    for r in rows:a.annotate(f"N={r['N']:g}",(1/r['N']**2,r['N2_lambda_min']),xytext=(3,5),textcoords='offset points',fontsize=8)
    if limit is not None:a.axhline(limit,color='C1',ls='--',label='Independent hydrodynamic limit')
    a.set(xlabel=r'$1/N^2$',ylabel=r'$N^2\lambda_{\min}$',title=f'Z = {Z:g}'+(' (before breaking)' if limit else ' (after breaking)'))
    a.set_xlim(-.0003,.0115);a.grid(alpha=.2);a.legend(fontsize=8,loc='best')
save(fig,folder,'Strong normal dispersion: leading scaling at new distances')

folder=ROOT/'2026-10-19-gpt-e-similariton'
summary=read(folder/'summary.json')
data=read(Path(summary['asymptotic_base']['raw_curve_location']))['rows']
data=[r for r in data if r['tau']>=12]
t=np.array([r['tau'] for r in data])
fig,axs=plt.subplots(2,2,figsize=(10,7))
for j in range(3):
    axs[0,0].plot(t,[r['photon_intensity_variances'][j]/np.exp(r['tau']/3) for r in data],label=f'Order {j+2}')
    axs[0,1].plot(t,[r['photon_phase_variances'][j]/np.exp(5*r['tau']/3) for r in data],label=f'Order {j+2}')
axs[1,0].plot(t,[r['spectral_ratio']*np.exp(2*r['tau']/3) for r in data])
axs[1,1].plot(t,[r['phase_energy_deficit']*np.exp(2*r['tau']/3) for r in data])
labels=[('Intensity shape envelopes',r'$G^{-1/3}\,\mathrm{Var}(X_l)$'),
        ('Phase shape envelopes',r'$G^{-5/3}\,\mathrm{Var}(Y_l)$'),
        ('Fixed five-component spectral projection',r'$G^{2/3}\mu_2/\mu_1$'),
        ('Phase variance unexplained by energy',r'$G^{2/3}(1-r^2)$')]
for a,(title,yl) in zip(axs.ravel(),labels):a.set(title=title,xlabel=r'$\tau=\ln G$',ylabel=yl);a.grid(alpha=.2)
axs[0,0].legend(fontsize=8);axs[0,1].legend(fontsize=8)
save(fig,folder,'Reduced similariton model: bounded, oscillatory prefactors')
