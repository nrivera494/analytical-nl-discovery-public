#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Small scientific figures from the archived similariton run outputs."""
import os
os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/gpt-a-matplotlib')
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from similariton_summarize import load_run

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '2026-10-08-gpt-a-similariton-'
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'savefig.dpi': 180})

def save(fig, suffix, name, sources):
    out = ROOT / 'runs' / (PREFIX + suffix)
    fig.text(.01, -.035, 'gpt-a / gpt-6-astra / gpt | Runs: ' + sources,
             fontsize=6, color='0.35')
    fig.savefig(out / name, bbox_inches='tight',
                metadata={'Author': 'gpt-a; model gpt-6-astra; family gpt',
                          'Description': 'Run prefix ' + PREFIX + '; ' + sources})
    plt.close(fig)

def basin_map():
    _, _, rec = load_run(PREFIX + 'map')
    hydro = json.loads((ROOT/'runs'/(PREFIX+'wavebreaking')/'summary.json').read_text())
    hg = {(r['shape'],r['width'],r['chirp']):r for r in hydro['shape_grid']}
    fig, ax = plt.subplots(2,3,figsize=(10.5,6.5),layout='constrained')
    for i,N in enumerate([5,10]):
        for j,shape in enumerate(['gaussian','sech','supergaussian']):
            a=ax[i,j]; vals=np.zeros((3,3)); symbols={}
            for r in rec.values():
                if r['shape']!=shape or r['Nstar']!=N: continue
                wi=[.5,1.,2.].index(r['width']); qi=np.argmin(np.abs(np.array([-.5,0,1/3])-r['chirp']))
                v=r['rows'][-1]
                vals[qi,wi]=max(v['density_l1']/.1,abs(v['width_ratio']-1)/.05,
                    abs(v['chirp_ratio']-1)/.05,v['core_scaled_velocity_rms']/.02)
                h=next((g for (ss,ww,qq),g in hg.items() if ss==shape and ww==r['width'] and abs(qq-r['chirp'])<1e-8),None)
                symbols[qi,wi]=' ×' if h and h['resolved_steepening_indicator'] else (' ○' if h and h['interpretation']=='possible steepening' else '')
            im=a.imshow(vals,origin='lower',vmin=0,vmax=3,cmap='RdYlBu_r',aspect='auto')
            for qi in range(3):
                for wi in range(3): a.text(wi,qi,f'{vals[qi,wi]:.2f}'+symbols[qi,wi],ha='center',va='center',fontsize=10)
            a.set(xticks=[0,1,2],xticklabels=['0.5','1','2'],yticks=[0,1,2],yticklabels=['−0.5','0','1/3'],
                  xlabel=r'Input duration $w$',ylabel=r'Input chirp $q$',title=f'{shape}, $N_*={N}$')
    fig.colorbar(im,ax=ax.ravel().tolist(),label='Largest error / frozen tolerance (pass < 1)',shrink=.8,extend='max')
    fig.suptitle('Finite-length profile map at $gL=8$; not an asymptotic basin\n×: Euler steepening diagnostic; ○: ambiguous, through $gL=4$',fontsize=12)
    save(fig,'comparison','finite_length_map.png','map; wavebreaking')

def response(rec, prefix):
    rp=rec[prefix+'_plus']['rows']; rm=rec[prefix+'_minus']['rows']
    h=rec[prefix+'_plus']['width']-rec[prefix+'_minus']['width']
    z=np.array([r['gain_length'] for r in rp]); yp=np.array([r['width_ratio'] for r in rp]);ym=np.array([r['width_ratio'] for r in rm])
    vp=np.array([r['width_ratio']*(r['chirp_ratio']-1)/3 for r in rp]);vm=np.array([r['width_ratio']*(r['chirp_ratio']-1)/3 for r in rm])
    return z,(yp-ym)/h,(vp-vm)/h

def rates():
    _,_,safe=load_run(PREFIX+'rates-safe'); _,_,ref=load_run(PREFIX+'rates-convergence')
    fig,ax=plt.subplots(2,2,figsize=(10,7),layout='constrained')
    z,y,v=response(safe,'N10_width');zz,yy,vv=response(ref,'grid_width')
    w=np.sqrt(2)/3; pred=np.exp(-z/3)*(y[0]*np.cos(w*z)+(v[0]+y[0]/3)/w*np.sin(w*z))
    ax[0,0].plot(z,y,label='NLSE, base grid');ax[0,0].plot(zz,yy,'--',label='NLSE, doubled grid')
    ax[0,0].plot(z,pred,':',color='k',label='Linear hydrodynamic prediction')
    ax[0,0].set(xlabel='$gL$',ylabel='Paired width response',title='$N_*=10$; nominal width perturbations ±0.01')
    ax[0,0].legend(fontsize=8)
    ax[0,1].semilogy(z,np.abs(y-pred)+1e-12,label='Difference from linear hydrodynamics')
    ax[0,1].semilogy(z,np.abs(y-yy)+1e-12,label='Change on doubled grid')
    ax[0,1].set(xlabel='$gL$',ylabel='Absolute response difference',title='Model deviation and numerical change')
    ax[0,1].legend(fontsize=8)
    ss=json.loads((ROOT/'runs'/(PREFIX+'rates-convergence')/'summary.json').read_text())
    fits={r['pair']:r['fits'] for r in ss['paired_width_chirp_fits']}
    for N,pre in [(5,'N5_grid_width'),(10,'grid_width'),(20,'N20_grid_width')]:
        if pre not in fits:continue
        xx=[5,7,9]; ff=[fits[pre][s] for s in ['2-8','4-10','6-12']]
        ax[1,0].plot(xx,[f['decay_per_gain_length'] for f in ff],'o-',label=f'$N_*={N}$')
        ax[1,1].plot(xx,[f['frequency_per_gain_length'] for f in ff],'o-',label=f'$N_*={N}$')
    first_fine=True
    for suffix in ['rates-fine','rates-lower-n-refinement']:
        fp=ROOT/'runs'/(PREFIX+suffix)/'summary.json'
        if not fp.exists():continue
        for pair in json.loads(fp.read_text())['paired_width_chirp_fits']:
            if '6-12' not in pair['fits']:continue
            fs=pair['fits']['6-12']
            for a,key in [(ax[1,0],'decay_per_gain_length'),(ax[1,1],'frequency_per_gain_length')]:
                a.plot(9,fs[key],marker='x',markersize=9,color='k',linestyle='none',
                       label='Further late grid doubling' if first_fine else None)
            first_fine=False
    for a,target,label in [(ax[1,0],1/3,'Decay / $g$'),(ax[1,1],w,'Angular frequency / $g$')]:
        a.axhline(target,color='k',linestyle=':',label='Hydrodynamic prediction')
        a.set(xticks=[5,7,9],xticklabels=['2–8','4–10','6–12'],xlabel='Fitting interval in $gL$',ylabel=label)
        a.legend(fontsize=8)
    save(fig,'comparison','width_rates.png','rates-safe; rates-convergence; rates-fine; rates-lower-n-refinement')

def long_resolution():
    _,_,base=load_run(PREFIX+'long-inputs');_,_,ref=load_run(PREFIX+'long-refinement')
    fig,ax=plt.subplots(2,2,figsize=(10,7),layout='constrained')
    cases=[(base['gaussian_w2_qm0p5'],'16384: underresolved at late distance',':')]
    for label,name,style in [('gaussian_grid32768','32768','-'),('gaussian_grid65536','65536','--'),
                              ('gaussian_step65536','65536, half step','-.'),
                              ('gaussian_window131072','131072, double window',':')]:
        if label in ref:cases.append((ref[label],name,style))
    for r,name,style in cases:
        rows=[v for v in r['rows'] if 6-1e-9<=v['gain_length']<=12+1e-9]
        z=np.array([a['gain_length'] for a in rows])
        for a,key in [(ax[0,0],'width_ratio'),(ax[0,1],'chirp_ratio'),(ax[1,0],'density_l1')]:
            a.plot(z,[v[key] for v in rows],style,label=name,linewidth=1.4)
        ax[1,1].semilogy(z,np.maximum([v['frequency_guard_fraction'] for v in rows],1e-30),style,label=name,linewidth=1.4)
    for a,title,ylabel in [(ax[0,0],'Width','Normalized rms width'),(ax[0,1],'Chirp','Normalized moment chirp'),
                          (ax[1,0],'Density error','Relative density $L^1$ error'),
                          (ax[1,1],'High-frequency guard','Mass in outer spectral guard')]:
        a.set(xlabel='$gL$',ylabel=ylabel,title=title,xlim=(6,12))
    ax[0,0].legend(fontsize=7)
    for a in [ax[0,0],ax[0,1]]:
        a.axhline(.95,color='0.5',linestyle=':',linewidth=.7);a.axhline(1.05,color='0.5',linestyle=':',linewidth=.7)
    fig.suptitle('Broad compressive Gaussian: late numerical aliasing changes the moments\n$w=2$, $q=-0.5$, $N_*=10$; refined trajectories restart at $gL=6$',fontsize=12)
    save(fig,'comparison','long_resolution.png','long-inputs; long-refinement')

def odd():
    _,cfg,rec=load_run(PREFIX+'map-convergence');r=rec['odd_grid']
    data=np.load(Path(cfg['raw_location'])/'odd_grid.npz');t=data['t'];zs=data['z'];fields=data['fields']
    fig,ax=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
    for z in [0,4,8]:
        i=np.argmin(abs(zs-z));x=t/np.exp(z/3);rr=abs(fields[:,i])**2/np.exp(2*z/3)
        ax[0].plot(x,rr,label=f'$gL={z}$',linewidth=1)
    x=np.linspace(-1.4,1.4,600);ax[0].plot(x,np.maximum(1-x*x,0),'k:',label='Parabolic reference')
    ax[0].set(xlim=(-1.4,1.4),xlabel='Similarity coordinate $x$',ylabel='Scaled intensity $R$',title='Odd field: narrowing central node')
    ax[0].legend(fontsize=8,loc='upper right')
    z=np.array([a['gain_length'] for a in r['rows']]);l1=[a['density_l1'] for a in r['rows']]
    distance=[2-2*a['even_parabolic_field_overlap'] for a in r['rows']]
    ax[1].semilogy(z,l1,label='Relative density $L^1$ error')
    ax[1].semilogy(z,distance,label='Unit-field distance squared')
    ax[1].set(xlabel='$gL$',ylabel='Error / distance',title='Topology changes the answer')
    ax[1].legend(fontsize=8)
    save(fig,'comparison','odd_obstruction.png','map-convergence (odd_grid); checks')

def vacuum_and_breaking():
    import tomli
    cfg=tomli.loads((ROOT/'runs'/(PREFIX+'wavebreaking')/'config.toml').read_text()); raw=Path(cfg['raw_location'])
    fig,ax=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
    for n in [2048,4096,8192]:
        p=raw/f'gaussian_w1_q0p3333_n{n}.toml'
        if not p.exists():continue
        r=tomli.loads(p.read_text())['rows']
        ax[0].plot([a['gain_length'] for a in r],[a['maximum_scaled_density_gradient'] for a in r],label=str(n))
    ax[0].set(xlabel='$gL$',ylabel='Maximum scaled density gradient',title='Gaussian: resolution-dependent steepening')
    ax[0].legend(title='Cells',fontsize=8)
    for n in [1024,2048,4096,8192]:
        r=tomli.loads((raw/f'shock_n{n}.toml').read_text())['rows']
        ax[1].semilogy([a['gain_length'] for a in r],[a['compressive_riemann_gradient'] for a in r],label=str(n))
    ax[1].axvline(.0750206994841893,color='k',linestyle=':',label='Proved upper time')
    ax[1].set(xlabel='$gL$',ylabel='Maximum compressive Riemann gradient',title='Protected compression counterexample')
    ax[1].legend(fontsize=7)
    vr=Path.home()/'analytical-nl-discovery-data'/(PREFIX+'physical-vacuum-direct')
    for degree in [32,64]:
        f=vr/f'heldout_asymmetric_degree{degree}.npz'
        if f.exists():
            d=np.load(f);ax[2].semilogy(d['tau'],d['H']/d['H'][0],label=f'Degree {degree}')
    tt=np.linspace(0,24,200);ax[2].semilogy(tt,np.exp(-tt/3),'k:',label='Conditional bound')
    ax[2].set(xlabel='$gL$',ylabel=r'$\mathcal{H}/\mathcal{H}(0)$',title='Smooth physical-vacuum held-out flow')
    ax[2].legend(fontsize=8)
    save(fig,'comparison','hydrodynamic_scope.png','wavebreaking; physical-vacuum-direct; checks')

if __name__=='__main__':
    basin_map();rates();odd();vacuum_and_breaking();long_resolution()
