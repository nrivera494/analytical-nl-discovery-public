"""Single-panel PI figures from recorded peaks. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent

def main():
    a=json.loads((HERE/'analysis.json').read_text())
    old=json.loads((HERE.parent/'2026-10-17-gpt-c-raman-sharpening/final_metrics.json').read_text())
    plt.rcParams.update({'font.size':11,'axes.labelsize':12,'legend.fontsize':9.5,
                         'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(6,4.5),dpi=120)
    x=np.linspace(10,70,300);ax.fill_between(x,.85*x,1.15*x,color='.91',label='Frozen null ±15%')
    ax.plot(x,x,color='.25',lw=1.3,label='Exit width = overlap optimum')
    for response,label,color,marker in [('bw','Silica BW','#1874b4','o'),('hc','Silica HC','#cc6b20','s'),
                                        ('as2s3','As-like oscillator','#8855a3','D')]:
        ps=[p for p in old['reference_peaks'] if p['response']==response and p['shape']=='sech' and p['N'] in [4,8,16]]
        xx=np.array([p['overlap_max_width_fs'] for p in ps]);yy=np.array([p['fit_width_fs'] for p in ps])
        lo=np.array([p['fit_width_resolution_interval_fs'][0] for p in ps]);hi=np.array([p['fit_width_resolution_interval_fs'][1] for p in ps])
        ax.errorbar(xx,yy,yerr=[yy-lo,hi-yy],fmt=marker,color=color,ms=5,capsize=2,lw=.9,label=label)
    upper=56.
    for model,label,color,marker in [('reference','ZBLAN reference (held out)','#087d62','o'),
                                     ('physical','ZBLAN physical (held out)','#111111','^')]:
        ps=[p for p in a['peaks'] if p['model']==model and p['bracketed']]
        xx=np.array([p['scores']['width_fit']['prediction'] for p in ps]);yy=np.array([p['fit_width_fs'] for p in ps])
        lo=np.array([p['scores']['width_fit']['measurement_interval'][0] for p in ps]);hi=np.array([p['scores']['width_fit']['measurement_interval'][1] for p in ps])
        if len(hi):upper=max(upper,float(max(hi))+1)
        ax.errorbar(xx,yy,yerr=[yy-lo,hi-yy],fmt=marker,mfc='white',mec=color,color=color,ms=6,capsize=2,lw=1,label=label)
    ax.set(xlim=(10,upper),ylim=(10,upper),xlabel=r'Overlap-maximizing sech width $T_R^*$ (fs)',
           ylabel=r'Exit sech-fit width at share optimum $T_1$ (fs)')
    ax.set_aspect('equal',adjustable='box');ax.legend(loc='lower right',frameon=True,framealpha=.96)
    ax.grid(alpha=.18);fig.tight_layout();fig.savefig(HERE/'fig_summary.png',metadata={'Author':'gpt-c / gpt-6-astra / gpt'});plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,4.5),dpi=120)
    x=np.linspace(60,650,300);ax.fill_between(x,.7*x,1.3*x,color='.91',label='Frozen position tolerance ±30%')
    ax.plot(x,x,color='.25',lw=1.3,label='Prediction = measurement')
    for model,color,marker in [('reference','#087d62','o'),('physical','#111111','^')]:
        ps=[p for p in a['peaks'] if p['model']==model and p['bracketed']]
        xx=np.array([p['scores']['position']['prediction'] for p in ps]);yy=np.array([p['T0_fs'] for p in ps])
        lo=np.array([p['T0_bracket_fs'][0] for p in ps]);hi=np.array([p['T0_bracket_fs'][1] for p in ps])
        ax.errorbar(xx,yy,yerr=[yy-lo,hi-yy],fmt=marker,mfc='white',mec=color,color=color,ms=6,capsize=3,label=f'ZBLAN {model}: held out')
        for p,xp,yp in zip(ps,xx,yy):ax.annotate(f"N={p['N']}",(xp,yp),xytext=(5,3),textcoords='offset points',fontsize=9,color=color)
    ax.set(xlim=(60,330),ylim=(50,650),xlabel=r'Frozen predicted input width $T_0^*$ (fs)',
           ylabel=r'Bracketed share-optimal input width $T_0^*$ (fs)')
    ax.grid(alpha=.18);ax.legend(loc='upper left',frameon=True);fig.tight_layout();fig.savefig(HERE/'fig_position.png',metadata={'Author':'gpt-c / gpt-6-astra / gpt'});plt.close(fig)
    print('Figure sizes:',[(p.name,p.stat().st_size) for p in HERE.glob('fig_*.png')])
if __name__=='__main__':main()
