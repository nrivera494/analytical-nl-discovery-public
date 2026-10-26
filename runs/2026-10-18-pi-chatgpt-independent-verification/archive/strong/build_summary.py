#!/usr/bin/env python3
"""Collate recorded results and produce a scientific comparison figure."""
import json,os
from pathlib import Path
import numpy as np

p=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR','/tmp/strong_matplotlib_cache')
case_names=[
    'N10_Z075_n256_s300','N20_Z075_n256_s300','N40_Z075_n512_s600',
    'N10_Z150_n256_s300','N20_Z150_n1024_w16_s1200','N40_Z150_n1024_s1200']
cases=[json.loads((p/(name+'.json')).read_text()) for name in case_names]
hydro=json.loads((p/'hydro_n441.json').read_text())
L=hydro['rows'][-1]['Lambda']
pre=cases[:3]; Ns=np.array([r['N'] for r in pre])
errors=1-np.array([r['N2_lambda_min'] for r in pre])/L
summary=dict(
    cases=cases,
    independent_hydro=hydro,
    prebreaking_reference_Lambda=L,
    prebreaking_relative_deficits=errors.tolist(),
    prebreaking_error_fitted_power=float(np.polyfit(np.log(Ns),np.log(errors),1)[0]),
    prebreaking_effective_c=(errors*(Ns*.75)**2).tolist(),
    hermite_bias=json.loads((p/'hydro_n441_w32_basis.json').read_text()),
    weak_crosscheck=json.loads((p/'weak_cross_N300_Z001_n2048_w12_s100.json').read_text()),
    interpretation='Prebreaking leading coefficient independently computed from epsilon=0 tangent hydrodynamics. Postbreaking points give finite-N covariance evidence, not a proof of a global classical hydrodynamic map.'
)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axs=plt.subplots(2,2,figsize=(10,6.3),layout='constrained')
    for row,(z,rows,ref,ref_label,npz_name) in enumerate([
        (.75,cases[:3],L,'Independent smooth hydrodynamics','N20_Z075_n256_s300.npz'),
        (1.5,cases[3:],.3625049833090736,'Repository N=200 coefficient','N20_Z150_n1024_w16_s1200.npz')]):
        ax=axs[row,0]
        ax.plot([r['N'] for r in rows],[r['N2_lambda_min'] for r in rows],'o-',color='#2266aa',label='Independent NLSE covariance')
        ax.axhline(ref,color='#b15d32',ls='--',lw=1.4,label=ref_label)
        ax.set(xlabel='$N$',ylabel=r'$N^2\lambda_{\min}$',title=f'$Z={z:g}$'+(' (before breaking)' if row==0 else ' (after breaking)'))
        ax.set_xticks([10,20,40]);ax.grid(alpha=.18)
        ax.legend(fontsize=8,loc='best')
        data=np.load(p/npz_name);t=data['t'];u=data['u'];low=data['low_modes'];n=len(t)
        intensity=abs(u)**2;mode=low[:n,0]**2+low[n:,0]**2
        ax=axs[row,1]
        ax.plot(t,intensity/intensity.max(),color='#54565a',lw=1.5,label='Mean intensity')
        ax.plot(t,mode/mode.max(),color='#2266aa',lw=1.7,ls='--',label='Optimal quadrature mode density')
        ax.set(xlabel=r'$\tau=T/T_0$',ylabel='Normalized to own maximum',xlim=(-3.5,3.5),title=f'Mean and squeezed mode, $N=20$, $Z={z:g}$')
        ax.grid(alpha=.18);ax.legend(fontsize=8,loc='upper right')
    fig.suptitle('Independent normal-dispersion verification',fontsize=14)
    fig.savefig(p/'strong_comparison.png',dpi=180)
    fig.savefig(p/'strong_comparison.pdf')
except ImportError:
    pass
print(json.dumps({'cases':len(cases),'prebreaking_error_power':summary['prebreaking_error_fitted_power'],'output':str(p/'summary.json')},indent=2))
