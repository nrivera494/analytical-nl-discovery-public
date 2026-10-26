#!/usr/bin/env python3
"""Small scientific figures for the registered soliton evidence.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import json,os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-b-soliton-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
try:
    import tomllib
except ImportError:
    import tomli as tomllib

ROOT=Path(__file__).resolve().parents[1]
DATA=Path('~/analytical-nl-discovery-data')
PREFIX='2026-10-10-gpt-b-soliton-'
META={'Author':'gpt-b; gpt-6-astra; family gpt',
      'Description':'Proposer calculations for T-20261010-claude-interactive-06; no independent verification.'}


def read(run,name):return json.loads((DATA/(PREFIX+run)/name).read_text())


def save(fig,run,name,footer):
    dest=ROOT/'runs'/(PREFIX+run)/'figures';dest.mkdir(exist_ok=True)
    fig.text(.02,.01,footer,fontsize=7,color='#555555')
    fig.savefig(dest/name,dpi=180,bbox_inches='tight',metadata=META)
    plt.close(fig);print(dest/name)


def anchor_figure():
    base=DATA/(PREFIX+'anchor');data=np.load(base/'native_50ps/batch_cells03.npz')
    kernels=np.loadtxt(base/'native_50ps/native_kernels.csv',delimiter=',');k=kernels[:,0]
    order=np.argsort(k);use=(k[order]>-20)&(k[order]<9);order=order[use]
    spectrum=abs(np.fft.ifft(data['mean'],norm='ortho'))**2
    omega0=2*np.pi*2.99792458e-4/(1550.e-9)
    spectrum[order]/=1+k[order]/(.12480519228171619*omega0)
    spectrum/=spectrum[order].max()
    archive=np.fft.ifftshift(np.loadtxt(base/'archive_masks_50ps.csv',delimiter=',')[:,1])
    new=np.fft.ifftshift(np.loadtxt(base/'native_50ps/batch_cells03_masks.csv',delimiter=',')[:,2])
    fig=plt.figure(figsize=(11,4.9));gs=fig.add_gridspec(3,2,width_ratios=[1.3,1.],hspace=.12,wspace=.3)
    ax=fig.add_subplot(gs[:2,0]);maskax=fig.add_subplot(gs[2,0],sharex=ax);barax=fig.add_subplot(gs[:,1])
    ax.semilogy(k[order],spectrum[order],color='#444444')
    ax.set(ylabel='Relative photon spectral density',ylim=(1e-5,1.4),title='Notebook output and two achieved masks')
    ax.tick_params(labelbottom=False)
    maskax.step(k[order],.72*archive[order],where='mid',color='#777777')
    maskax.step(k[order],1.1+.72*new[order],where='mid',color='#25855a')
    maskax.set(xlabel=r'Frequency offset $\Omega T_0$',yticks=[.35,1.45],yticklabels=['Archived','New'],ylim=(-.15,2),xlim=(-20,9))
    sources=[('Archived\n50 ps','native_50ps',1),('New\nsame grid','native_50ps_optimized',0),
             ('New\nfine grid','native_50ps_optimized_finest',0),('New\n100 ps','native_100ps_optimized',0)]
    rows=[tomllib.loads((base/folder/'native_summary.toml').read_text())['rows'][row] for _,folder,row in sources]
    positions=np.arange(len(rows));vac=[r['F_vacuum'] for r in rows];bath=[r['F_Raman'] for r in rows]
    barax.bar(positions,vac,color='#2865a8',label='Input vacuum')
    barax.bar(positions,bath,bottom=vac,color='#d77912',label='Raman reservoir')
    for j,r in enumerate(rows):barax.text(j,r['F_total']+.008,f"{r['dB']:.3f} dB",ha='center',fontsize=8)
    barax.set(xticks=positions,xticklabels=[x[0] for x in sources],ylabel='Fano factor (linear units)',ylim=(0,.36),title='Native discrete-adjoint checks')
    barax.legend(frameon=False,fontsize=8)
    fig.subplots_adjust(bottom=.18,top=.9)
    save(fig,'anchor','anchor_binary_masks.png',PREFIX+'anchor; symmetrized reservoir with shock. New masks are achievable; no global optimum is certified.')


def main():
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.grid':True,'grid.alpha':.17,'lines.linewidth':1.8})
    distance=read('raman','distance/summary.json')['points']
    styles=[('lambda_min_dB',r'$\lambda_{\min}(V)$','#737373','-'),
            ('lambda_pass_dB',r'$\lambda_{\rm pass}$','#25855a','--'),
            ('lambda_gen_dB',r'$\lambda_{\rm gen}$','#2865a8','-'),
            ('best_binary_found_dB','Best binary found','#d77912','-'),
            ('centered_passband_dB','Optimized centered passband','#8e559d',':')]
    fig,axes=plt.subplots(1,2,figsize=(10.8,4.7),sharex=True)
    for ax,temp,title in zip(axes,[0,300],['Ideal Kerr','300 K white Raman source']):
        rows=[r for r in distance if r['temperature_K']==temp]
        z=[r['z_over_LD'] for r in rows]
        for key,label,color,style in styles:ax.plot(z,[r[key] for r in rows],label=label,color=color,ls=style)
        ax.set(title=title,xlabel=r'Distance $z/L_D$',ylabel='Variance relative to shot noise (dB)',xlim=(0,8),ylim=(-26,1))
    axes[0].legend(frameon=False,fontsize=9,loc='lower left')
    fig.suptitle('Readout restriction retains a much tighter soliton bound',fontsize=13)
    fig.subplots_adjust(top=.86,bottom=.16,wspace=.26)
    save(fig,'raman','distance_hierarchy.png',PREFIX+'raman / distance; frozen fundamental soliton; finite-basis eigenvalues and heuristic binary search.')

    asym=read('raman','thermal_asymptote.json')
    fig,axes=plt.subplots(1,2,figsize=(10.8,4.4))
    for temp,color in [(0,'#737373'),(77,'#2865a8'),(300,'#d77912')]:
        rows=[r for r in asym['checks'] if r['temperature_K']==temp and r['observable']=='lambda_gen']
        width=np.array([r['T0_ps'] for r in rows]);excess=np.array([r['measured_excess'] for r in rows])
        predicted=np.array([r['predicted_leading_excess'] for r in rows]);residual=abs(np.array([r['residual'] for r in rows]))
        label='0 K: relative to Kerr' if temp==0 else f'{temp} K: relative to thermal limit'
        axes[0].loglog(width,excess,'o-',color=color,label=label)
        axes[0].loglog(width,predicted,'--',color=color,alpha=.6)
        axes[1].loglog(width,residual,'o-',color=color,label=f'{temp} K')
        power=3 if temp==0 else 4
        axes[1].loglog(width,residual[-1]*(width[-1]/width)**power,':',color=color,alpha=.6)
    axes[0].set(title='Leading coefficient predicted from the operator',xlabel=r'Pulse width $T_0$ (ps)',ylabel=r'Excess in $\lambda_{\rm gen}$')
    axes[1].set(title='Remainder after subtracting the expansion',xlabel=r'Pulse width $T_0$ (ps)',ylabel='Absolute eigenvalue remainder')
    axes[0].legend(frameon=False,fontsize=8);axes[1].legend(frameon=False,fontsize=8)
    axes[1].text(.03,.06,r'Dotted guides: $T_0^{-3}$ at 0 K; $T_0^{-4}$ at 77/300 K',transform=axes[1].transAxes,fontsize=8)
    fig.subplots_adjust(bottom=.18,wspace=.3,top=.88)
    save(fig,'raman','thermal_asymptote.png',PREFIX+'raman / thermal_asymptote; fixed z/LD=3π/2, oscillator 12.2/32 fs; no fitted coefficients.')

    inheritance=read('gaussian','inherited_amplitude.json')['points']
    surrogate=json.loads((ROOT/'runs'/(PREFIX+'gaussian')/'surrogate_prediction.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(10.8,4.5))
    axes[0].plot([r['N'] for r in inheritance],[r['separated_soliton_energy_Fano'] for r in inheritance],'o-',color='#2865a8')
    axes[0].axhline(1,color='#737373',ls='--',label='Fresh coherent soliton')
    axes[0].axvline(1.5*np.sqrt(np.pi/2),color='#d77912',ls=':',label='Second discrete soliton appears')
    axes[0].set(xlabel='Gaussian launch N',ylabel='Largest scattering soliton energy Fano factor',title='Inherited neutral noise is not coherent noise',ylim=(0,1.8))
    axes[0].legend(frameon=False,fontsize=8)
    # Values are loaded from the frozen forecast and matching native batch.
    rows=surrogate.get('points',[])
    for j,N in enumerate([1.25,1.5]):
        actual=read('gaussian',f'gaussian_N{N:g}/batch.json')
        candidate=next(r for r in rows if r['N']==N)
        prediction=candidate.get('prediction',candidate.get('coherent_sech_prediction',candidate))
        values=[prediction['lambda_gen'],actual['lambda_gen'],actual['best_binary_found']]
        for offset,value,color,marker,label in zip([-.15,0,.15],values,['#aa4070','#2865a8','#d77912'],['x','o','s'],['Coherent-width candidate','Propagated amplitude bound','Achieved binary filter']):
            axes[1].scatter(j+offset,10*np.log10(value),color=color,marker=marker,s=48,label=label if j==0 else None,zorder=3)
    axes[1].set(xticks=[0,1],xticklabels=['N=1.25, z/LD=3','N=1.5, z/LD=4'],ylabel='Variance relative to shot noise (dB)',title='Width substitution fails as a lower bound')
    axes[1].legend(frameon=False,fontsize=8,loc='upper left')
    fig.subplots_adjust(bottom=.2,wspace=.3,top=.88)
    save(fig,'gaussian','inherited_covariance.png',PREFIX+'gaussian; left is a scattering-coordinate diagnostic, not a binary spectral measurement; right retains physical shock.')
    anchor_figure()


if __name__=='__main__':main()
