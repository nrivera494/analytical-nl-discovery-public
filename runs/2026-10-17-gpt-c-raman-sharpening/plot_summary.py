"""Single-panel PI plot. gpt-c / gpt-6-astra / gpt."""
import json,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/gpt-c-matplotlib")
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
HERE=Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'summary.json').read_text());m=json.loads((HERE/'final_metrics.json').read_text());fit=json.loads((HERE/'training_fit.json').read_text())
    plt.rcParams.update({'font.size':10,'axes.labelsize':11,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(6,4.5),layout='constrained')
    colors={'bw':'#0072B2','hc':'#D55E00','as2s3':'#009E73'};names={'bw':'Blow–Wood','hc':'Hollenbeck–Cantrell','as2s3':'As-like oscillator'};markers={4:'o',8:'s',16:'^'}
    for response,color in colors.items():
        for N,marker in markers.items():
            pp=[p for p in m['reference_peaks'] if p['response']==response and p['shape']=='sech' and p['N']==N]
            if not pp:continue
            peak=pp[0];z=peak['zN'];rows=sorted([r for r in s['rows'] if r['response']==response and r['shape']=='sech' and r['N']==N and r['zN']==z and r['split'] in ['calibration','heldout'] and not r['invalid'] and peak['T_bracket_fs'][0]<=r['T0_fs']<=peak['T_bracket_fs'][1]],key=lambda r:r['y'])
            # Lines merely connect a duration scan; black band below is the prediction.
            ax.plot([r['y'] for r in rows],[r['scaled_share'] for r in rows],color=color,lw=.7,alpha=.6)
            for r in rows:
                ax.scatter(r['y'],r['scaled_share'],s=24,marker=marker,facecolor='white' if r['split']=='heldout' else color,edgecolor=color,linewidth=.9,zorder=3)
    n=np.linspace(3,16,200);power=fit['power_position'];yp=n**2/(power['prefactor_tau1']*n**power['exponent']);coef=fit['scaled_share_log_quadratic']['coefficients'];a=np.polynomial.polynomial.polyval(np.log(n/6),coef)
    if fit.get('selected_share_model')=='scaled_share_inverse_log':
        cc=fit['scaled_share_inverse_log']['coefficients'];a=cc[0]+cc[1]/n+cc[2]*np.log(n)
    ax.axhline(1.29,color='#666666',lw=.8,ls='--',zorder=1)
    ax.plot(yp,a,color='#222222',lw=1.5,zorder=2)
    ax.fill_between(yp,a-.006,a+.006,color='#222222',alpha=.12,lw=0)
    for p in m['reference_peaks']:
        if p['response']=='bw' and p['shape']=='sech' and p['split']=='heldout':
            tau=12.2;lo,hi=p['T_bracket_fs'];y=p['y'];xerr=[[max(0,y-p['N']**2*tau/hi)],[max(0,p['N']**2*tau/lo-y)]]
            ax.errorbar(y,p['scaled_share'],xerr=xerr,yerr=p['scaled_share_resolution_envelope'],fmt='D',ms=5,mfc='white',mec='#222222',ecolor='#555555',capsize=2,lw=.8,zorder=5)
    handles=[Line2D([0],[0],color=c,lw=1.5,label=names[r]) for r,c in colors.items()]
    handles += [Line2D([0],[0],color='#222',lw=1.5,label='BW fit ±0.006 tolerance'),Line2D([0],[0],color='#222',marker='D',mfc='white',lw=0,label='Held-out BW peaks'),Line2D([0],[0],color='#666',ls='--',lw=.8,label='Original 1.29 reference')]
    ax.legend(handles=handles,loc='lower left',frameon=False,ncol=2)
    ax.set_xlabel('Scaled inverse launch duration\n'+r'$y=N^2\tau_{\rm ref}/T_0$ (dimensionless)')
    ax.set_ylabel('Scaled leading energy share\n'+r'$f_1\sqrt{N}$ (dimensionless)')
    ax.set_title('Raman transfer: sech-pulse peak drift',fontsize=11)
    ax.grid(alpha=.15)
    ax.set_ylim(.98,max(1.34,ax.get_ylim()[1]))
    ax.text(.98,.98,'Local scans: ○ N=4   □ N=8   △ N=16\nOpen symbols: held out',ha='right',va='top',transform=ax.transAxes,fontsize=8)
    fig.savefig(HERE/'fig_summary.png',dpi=120,metadata={'Author':'gpt-c / gpt-6-astra / gpt','Description':HERE.name})
    plt.close(fig)
    print('Figure bytes:',(HERE/'fig_summary.png').stat().st_size)
if __name__=='__main__':main()
