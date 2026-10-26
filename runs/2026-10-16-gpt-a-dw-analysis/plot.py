#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt. Scientific audit figures."""
import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-a-mpl')
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

folder=Path(__file__).resolve().parent
data=json.loads((folder/'summary.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                     'savefig.dpi':170,'figure.constrained_layout.use':True})
colors=['#176b91','#d05c27','#5e4f94','#2b8655']

def save(fig,name):
    fig.savefig(folder/name,metadata={'Agent':'gpt-a','Model':'gpt-6-astra','Family':'gpt',
        'SourceRun':'2026-10-16-gpt-a-dw-analysis'})
    plt.close(fig)

if 'shock_1' in data['roy']:
    rr=data['roy']['shock_1'];rows=rr['rows']
    d=np.array([r['delta3'] for r in rows]);peak=np.array([r['peak_db'] for r in rows])
    fig,ax=plt.subplots(2,2,figsize=(10,7))
    a=ax[0,0]
    ref=json.loads((folder.parent/'2026-10-16-gpt-a-roy-reference/summary.json').read_text())['figure3b_full']
    a.scatter([r['delta3'] for r in ref],[r['peak_db'] for r in ref],facecolors='none',edgecolors='black',label='Roy Fig. 3(b) circles',s=28)
    a.plot(d,peak,'o-',color=colors[0],label='Independent full GNLSE',ms=4)
    a.plot(d,[r['eq6_db'] for r in rows],'--',color=colors[1],label='Roy Eq. 6; no fit')
    a.plot(d,[r['strip_peak_db'] for r in rows],'-',color=colors[2],label='Fixed strip; fit p,c below threshold')
    lower=min(-155,min(peak)-5,min(r['eq6_db'] for r in rows)-5)
    a.axhline(-80,color='gray',lw=.9,ls=':');a.set(xlabel=r'$\delta_3$',ylabel='Spectral peak / input peak (dB)',ylim=(lower,20),title='Roy model: sech N=2, 50 fs, xi=4')
    a.legend(fontsize=8)
    a=ax[0,1]
    observable=d[peak>-80]
    mask=peak>-80
    a.plot(d[mask],np.array([r['strip_peak_error_db'] for r in rows])[mask],'o-',color=colors[2],label='Fixed-strip extrapolation')
    a.plot(d[mask],np.array([r['eq6_peak_error_db'] for r in rows])[mask],'s--',color=colors[1],label='Eq. 6')
    a.axhline(0,color='gray',lw=.9);a.set(xlabel=r'$\delta_3$',ylabel='Prediction minus simulation (dB)',title='Observable peaks (> -80 dB)');a.legend(fontsize=8)
    a=ax[1,0]
    a.semilogy(d,[r['eta_resonant'] for r in rows],'o-',color=colors[0],label='Resonant energy fraction')
    a.semilogy(d,[r['eta_photon_resonant'] for r in rows],'s-',color=colors[3],label='Resonant photon fraction')
    a.semilogy(d,np.exp([r['strip_log_yield'] for r in rows]),'--',color=colors[0],label='Fixed-d energy fit')
    a.semilogy(d,np.exp([r['strip_log_photon_yield'] for r in rows]),'--',color=colors[3],label='Fixed-d photon fit')
    a.set(xlabel=r'$\delta_3$',ylabel='Fraction of launched energy or photons',title='Integrated yield is a separate observable');a.legend(fontsize=8)
    a=ax[1,1]
    for name,label,color in [('Roy_paper','Paper shock',colors[0]),('Roy_double_shock','Doubled shock',colors[1]),('Raman_only','No shock',colors[3])]:
        r=[x for x in data['relaxed_assumptions']['rows'] if name in x['models']]
        a.plot([x['delta3'] for x in r],[x['models'][name]['peak_db'] for x in r],'o-',color=color,ms=3,label=label)
    a.axhline(-80,color='gray',lw=.9,ls=':');a.set(xlabel=r'$\delta_3$',ylabel='Spectral peak (dB)',title='Same Raman response; varying shock');a.legend(fontsize=8)
    save(fig,'roy_comparison.png')

if data['core']:
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    for label,color in [('xi_2',colors[0]),('xi_4',colors[1])]:
        if label not in data['core']:continue
        case=data['core'][label];rows=case['rows'];fit=case['fixed_fit']
        ds=np.array([r['delta3'] for r in rows]);ys=np.array([r['eta'] for r in rows])
        x=1/ds
        ax[0].plot(x,np.log(ys),'o',ms=4,color=color,label=label.replace('_','='))
        ax[0].plot(x,fit['c']+fit['p']*np.log(ds)-fit['d']/ds,'-',color=color)
        er=case['local_error_scaling']
        ax[1].loglog(er['delta_mid'],er['relative_errors'],'o-',color=color,
                      label=f"{label}: alpha={er['measured_exponent']:.2f}")
    ax[0].set(xlabel=r'$1/\delta_3$',ylabel=r'$\ln\eta_{DW}$',title='Independent TOD-only N=2 runs')
    ax[1].set(xlabel=r'$\delta_3$ interval midpoint',ylabel='Relative local-slope error',title='Predicted error power: 1')
    for a in ax:a.legend(fontsize=8)
    save(fig,'core_law.png')

if 'xi_12' in data.get('length',{}):
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    ds0=.5*np.arccos(np.sqrt(3)-1)
    fitted=[]
    for index,z in enumerate([2,4,8,12]):
        v=(data['core'] if z<=4 else data['length'])['xi_'+str(z)]
        rows=[r for r in v['rows'] if r['delta3']<=.011]
        ds=np.array([r['delta3'] for r in rows]);ys=np.array([r['eta'] for r in rows])
        ax[0].plot(ds,np.log(ys)+ds0/ds,'o-',color=colors[index],label=f'xi={z}',ms=4)
        fitted.append(v['free_fit']['d'])
    ax[0].set(xlabel=r'$\delta_3$',ylabel=r'$\ln\eta+d_*/\delta_3$',title='Length changes the prefactor and corrections')
    ax[0].legend(fontsize=8)
    ax[1].axhspan(.96*ds0,1.04*ds0,color=colors[0],alpha=.12,label='Frozen 4% exponent tolerance')
    ax[1].axhline(ds0,color='black',ls=':',label='Exact TOD-free strip')
    ax[1].plot([2,4,8,12],fitted,'o-',color=colors[1])
    ax[1].set(xlabel=r'Fibre length $\xi_f$',ylabel='Four-point fitted exponent',title='Same d*; independent fits at each length')
    ax[1].legend(fontsize=8);save(fig,'length_law.png')

if data.get('collapse',{}).get('rows'):
    rows=data['collapse']['rows'];fig,ax=plt.subplots(figsize=(6,4))
    anchors=sorted({(r['design_x'],r['frozen_prediction']) for r in rows})
    xx=np.array([a[0] for a in anchors]);yy=np.array([a[1] for a in anchors])
    ax.plot(xx,yy,'s--',color='gray',label='Frozen card predictions')
    ax.fill_between(xx,yy*np.exp(-.21),yy*np.exp(.21),color='gray',alpha=.15,label='Frozen log tolerance 0.21')
    for order,color in [(3,colors[0]),(5,colors[1])]:
        chosen=[r for r in rows if r['N']==order and r['actual_x'] is not None]
        ax.scatter([r['actual_x'] for r in chosen],[r['eta_band'] for r in chosen],color=color,label=f'Independent Gaussian N={order}',zorder=3)
    ax.set(xlabel=r'$d_*/\delta_3$ using independent strip',ylabel='Normal-band envelope-norm fraction',title='Finite-yield collapse: held-out attack')
    ax.legend(fontsize=8);save(fig,'collapse_heldout.png')

strip_path=folder.parent/'2026-10-16-gpt-a-dw-strips/summary.json'
if strip_path.exists():
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    for name,color in [('sech2_M0',colors[0]),('sech2_roy_s1',colors[1]),('sech2_roy_s2',colors[2])]:
        path=Path('~/analytical-nl-discovery-data/2026-10-16-gpt-a-dw-strips')/(name+'_strip.json')
        if not path.exists():continue
        records=json.loads(path.read_text())
        valid=[r for r in records if r['fits']['blue_-5_-10'] is not None and r['fits']['blue_-5_-10']['rms']<.05]
        x=[r['z'] for r in valid];dd=[r['fits']['blue_-5_-10']['d_log'] for r in valid]
        ax[0].plot(x,dd,color=color,label=name.replace('sech2_',''))
        ax[1].plot(x,[r['max_intensity'] for r in valid],color=color,label=name.replace('sech2_',''))
    ax[0].set(xlabel=r'$\xi$',ylabel='Blue analyticity strip estimate',ylim=(.3,1),title='TOD-free evolution; no yield fit')
    ax[1].set(xlabel=r'$\xi$',ylabel='Peak |u| squared',title='Compression changes with Raman and shock')
    for a in ax:a.legend(fontsize=8)
    save(fig,'tod_free_strips.png')

null_path=folder.parent/'2026-10-16-gpt-a-gate-null/summary.json'
if null_path.exists():
    null=json.loads(null_path.read_text());fig,ax=plt.subplots(figsize=(6,4))
    for R,color in [(15,colors[0]),(20,colors[1])]:
        rows=[r for r in null['rows'] if r['gate_radius']==R]
        ax.semilogx([r['delta3'] for r in rows],[r['delta_log_eta'] for r in rows],'o-',color=color,label=f'Gate R={R}')
    ax.axhline(-null['exact_strip'],color=colors[2],ls='--',label='Claimed radiation limit -d*')
    ax.axhline(null['null_limit_delta_log_eta'],color='black',ls=':',label='Null-background limit -d*/3')
    ax.set(xlabel='Band-edge parameter delta3 (TOD is zero)',ylabel='delta3 ln(null band fraction)',title='Fixed gate retains an exponentially small core tail')
    ax.legend(fontsize=8);save(fig,'gate_null.png')
