#!/usr/bin/env python3
"""Register round-one outputs and compute transparent summaries.
agent: gpt-a; model: gpt-6-astra; family: gpt
"""
import json, platform, subprocess, sys
from pathlib import Path
import tomli, yaml, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
RAW=Path('~/analytical-nl-discovery-data')
IDENT=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')
SOLVER=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
DIRTY=bool(subprocess.check_output(['git','-C',str(ROOT/'solver'),'status','--porcelain'],text=True).strip())
HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()

def register(suffix,config,extra=None):
    rid='2026-10-04-gpt-a-'+suffix;raw=RAW/rid;dest=ROOT/'runs'/rid;dest.mkdir(parents=True,exist_ok=True)
    rows=[]
    for f in sorted(raw.glob('*.toml')):
        if not f.name.startswith('attempt'):
            rows.append(tomli.loads(f.read_text()))
    for f in sorted(raw.glob('*.json')):
        rows.append(json.loads(f.read_text()))
    summary=dict(IDENT,run_id=rid,cases=rows)
    if extra:summary.update(extra)
    (dest/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    source_commits={'capture':'9800bba','capture-small':'9800bba','passive':'37533f3',
        'noise':'ea01cd9','three-scaling':'57db513','noise-convergence':'ea01cd9','noise-small':'ea01cd9','noise-cw':'444c177'}
    meta=dict(IDENT,run_id=rid,solver_commit=SOLVER,solver_dirty=DIRTY,harness_commit=source_commits.get(suffix,HEAD),analysis_commit=HEAD,
        prediction_commit='43bc96d',hardware=platform.node(),julia_threads=2,blas_threads=1,fft_threads=1,
        raw_location=str(raw),wall_time_seconds=sum(r.get('elapsed_seconds',0) for r in rows),
        randomness='none; deterministic propagation',status='completed',task='T-20261004-claude-interactive-02')
    if suffix=='noise':
        meta['harness_commit']='ea01cd9'
        meta['execution_history']=[
            'First nine completed cases (none all; agarwal delta=0): b34213c, sequential adjoints.',
            'Remaining nine: ea01cd9, two concurrent adjoints. Completed checkpoint files were checked and reused.',
            'Initial in-progress agarwal physical-delta case was interrupted to change scheduling; no completed output was overwritten. Both logs are retained in the material raw folder.']
    (dest/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
    (dest/'config.yaml').write_text(yaml.safe_dump(dict(IDENT,**config),sort_keys=False))
    return rows,dest

def capture():
    rows,dest=register('capture',dict(script='scripts/p002_capture.jl',mode='main',r=[.003,.01,.03,.1],nt=4096,window_tau=320.,dzeta=.01,zeta=20.))
    small,_=register('capture-small',dict(script='scripts/p002_capture.jl',mode='small',r=[.0001,.0003,.001],nt=4096,window_tau=320.,dzeta=.01,zeta=20.))
    passive,pdest=register('passive',dict(script='scripts/p002_independent.py',modes=['passive','long','vector','refine'],method='Yoshida fourth-order split-step',threads=1))
    fits=[]
    for j in range(1,8):
        base=next(x for x in passive if x['label']==f'passive_refined_d{j}')
        cbase=base['rows'][-1]['capture_fixed_5'];c0=base['C0']
        allrows=sorted([x for x in rows+small if x['label'].startswith(f'd{j}_')],key=lambda x:x['r'])
        r=np.array([x['r'] for x in allrows]);window=np.array([x['rows'][-1]['capture_fixed_5'] for x in allrows]);proj=np.array([x['rows'][-1]['bound_projection'] for x in allrows])
        p0=json.loads((ROOT/'runs/2026-10-04-gpt-a-material'/'summary.json').read_text())['P0_W']
        v0=np.load(RAW/'2026-10-04-gpt-a-passive'/f'passive_refined_d{j}.npz')['fields'][-1,:,0]
        field=[]
        for x in allrows:
            folder='2026-10-04-gpt-a-capture-small' if x['r']<.003 else '2026-10-04-gpt-a-capture'
            v=np.load(RAW/folder/(x['label']+'.npz'))['fields'][:,1,0,-1]/np.sqrt(p0*x['r'])
            field.append(float(np.linalg.norm(v-v0)/np.linalg.norm(v0)))
        slope=lambda v,ids:float(np.polyfit(np.log(np.sqrt(r[ids])),np.log(abs(v[ids])),1)[0])
        fits.append(dict(delta=base['delta'],C0=c0,passive_window20=cbase,r=r.tolist(),window20=window.tolist(),projection20=proj.tolist(),
            exponent_epsilon_raw_small=slope(window-c0,slice(0,3)),exponent_epsilon_baseline_subtracted_small=slope(window-cbase,slice(0,3)),
            exponent_epsilon_projection_small=slope(proj-c0,slice(0,3)),minority_relative_field_error=field,
            exponent_epsilon_minority_field_small=slope(np.array(field),slice(0,3)),
            exponent_epsilon_raw_prescribed=slope(window-c0,slice(3,6)),exponent_epsilon_baseline_subtracted_prescribed=slope(window-cbase,slice(3,6))))
    sc=np.load(RAW/'2026-10-04-gpt-a-capture'/'scalar_control.npz');a=sc['fields'][:,0,0,:];z=sc['zeta']
    control=float(np.linalg.norm(a[:,-1]-a[:,0]*np.exp(1j*z[-1]/2))/np.linalg.norm(a[:,0]))
    cross=[]
    for j,r,didx in ((1,.01,3),(2,.1,6),(3,.01,7)):
        a=next(x for x in passive if x['label']==f'vector{j}')
        b=next(x for x in rows if x['label']==f'd{didx}_r{r}')
        cross.append(dict(case=j,window_abs_error=abs(a['rows'][-1]['capture_fixed_5']-b['rows'][-1]['capture_fixed_5']),projection_abs_error=abs(a['rows'][-1]['bound_projection']-b['rows'][-1]['bound_projection'])))
    summary=json.loads((dest/'summary.json').read_text());summary.update(fits=fits,scalar_complex_field_relative_error=control,independent_solver_comparison=cross,
        max_two_mode_energy_relative_error=max(abs(y['mode2_energy_ratio']-1) for x in rows if x['nm']==2 for y in x['rows']))
    (dest/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    fig,axs=plt.subplots(1,3,figsize=(12,3.5))
    dd=np.linspace(0,3,400);cc=np.ones_like(dd);cc[1:]=(np.pi*dd[1:]/(2*np.sinh(np.pi*dd[1:]/2)))**2
    axs[0].plot(dd,cc,color='k',label='Frozen bound fraction')
    axs[0].plot([x['delta'] for x in fits],[x['passive_window20'] for x in fits],'o',label='Passive window, z=20')
    axs[0].set(xlabel='Walk-off δ',ylabel='Minority-normalized capture');axs[0].legend(fontsize=8)
    for f in fits[1:4]:
        r=np.array(f['r']);e=np.sqrt(r)
        axs[1].loglog(e,abs(np.array(f['window20'])-f['C0']),'--',alpha=.6)
        axs[1].loglog(e,abs(np.array(f['window20'])-f['passive_window20']),'o-',label=f"δ={f['delta']:g}")
    axs[1].set(xlabel='ε = √r',ylabel='Absolute window error');axs[1].legend(fontsize=8);axs[1].set_title('Dashed: raw; solid: passive-subtracted',fontsize=9)
    for j in (2,3,4,7):
        v=next(x for x in passive if x['label']==f'passive_long_d{j}')
        zs=np.array([x['zeta'] for x in v['rows'] if x['zeta']>0]);cs=np.array([x['capture_fixed_5'] for x in v['rows'] if x['zeta']>0])
        axs[2].loglog(zs,abs(cs-v['C0']),'o-',label=f"δ={v['delta']:.3g}")
    axs[2].set(xlabel='Propagation ζ',ylabel='Passive window error');axs[2].set_xticks([10,20,40,80],['10','20','40','80']);axs[2].legend(fontsize=8)
    fig.tight_layout();fig.savefig(dest/'capture.png',dpi=170);plt.close(fig)
    print(json.dumps(dict(fits=fits,scalar_error=control,second_solver=cross),indent=2))

def convergence():
    rows,dest=register('capture-convergence',dict(script='scripts/p002_capture.jl',mode='convergence',checks=['half step','double window','double temporal resolution','double distance','three modes','physical beta2 and beta0 mismatch']))
    ref=json.loads((ROOT/'runs/2026-10-04-gpt-a-capture'/'summary.json').read_text())['cases']
    tests=[]
    for j,r,didx in ((1,.01,3),(2,.1,6),(3,.01,7)):
        b=next(x for x in ref if x['label']==f'd{didx}_r{r}')['rows'][-1]
        for x in rows:
            if x['label'].startswith(f'case{j}_'):
                e=min(x['rows'],key=lambda q:abs(q['zeta']-20))
                tests.append(dict(label=x['label'],capture_window20=e['capture_fixed_5'],difference_from_base=e['capture_fixed_5']-b['capture_fixed_5'],mode3_energy=e['energies'][2] if x['nm']==3 else 0.))
    summary=json.loads((dest/'summary.json').read_text());summary['comparisons']=tests
    (dest/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(tests,indent=2))

def gate_analysis():
    """Same continuous gate, with its two boundary samples integrated correctly."""
    p0=json.loads((ROOT/'runs/2026-10-04-gpt-a-material'/'summary.json').read_text())['P0_W']
    def integrate(t,intensity,radius=5.):
        ix=(t>-radius)&(t<radius)
        x=np.r_[-radius,t[ix],radius]
        y=np.r_[np.interp(-radius,t,intensity),intensity[ix],np.interp(radius,t,intensity)]
        return float(np.trapezoid(y,x)/2)
    cases={}
    for suffix in ('capture','capture-small','capture-convergence'):
        p=ROOT/'runs'/('2026-10-04-gpt-a-'+suffix)/'summary.json';s=json.loads(p.read_text())
        for row in s['cases']:
            if row['nm']<2 or row['r']==0:continue
            a=np.load(RAW/('2026-10-04-gpt-a-'+suffix)/(row['label']+'.npz'));t=a['tau']
            for iz,plane in enumerate(row['rows']):
                power=abs(a['fields'][:,1,0,iz])**2/(p0*row['r'])
                plane['capture_gate_trapezoid_5']=integrate(t,power)
            cases[row['label']]=row
        s['gate_quadrature']='Trapezoidal integral including interpolated endpoints at tau=+-5; original grid-sum fields retained.'
        p.write_text(json.dumps(s,indent=2)+'\n')
    fits=[]
    for j in range(1,8):
        a=np.load(RAW/'2026-10-04-gpt-a-passive'/f'passive_refined_d{j}.npz')
        cpass=integrate(a['tau'],abs(a['fields'][-1,:,0])**2)
        rows=sorted([x for k,x in cases.items() if k.startswith(f'd{j}_')],key=lambda q:q['r'])
        r=np.array([x['r'] for x in rows]);vals=np.array([x['rows'][-1]['capture_gate_trapezoid_5'] for x in rows])
        fits.append(dict(delta=rows[0]['delta'],r=r.tolist(),passive20=cpass,capture20=vals.tolist(),
            exponent_epsilon_small=float(np.polyfit(np.log(np.sqrt(r[:3])),np.log(abs(vals[:3]-cpass)),1)[0])))
    checks=[]
    for j,r,didx in ((1,.01,3),(2,.1,6),(3,.01,7)):
        base=cases[f'd{didx}_r{r}']['rows'][-1]['capture_gate_trapezoid_5']
        for tag in ('halfstep','doublewindow','doubleresolution'):
            v=cases[f'case{j}_{tag}']['rows'][-1]['capture_gate_trapezoid_5']
            checks.append(dict(case=j,check=tag,base=base,refined=v,difference=v-base))
    dest=ROOT/'runs/2026-10-04-gpt-a-capture-convergence'/'summary.json';s=json.loads(dest.read_text());s['gate_quadrature_checks']=checks;s['gate_scaling']=fits
    dest.write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(dict(checks=checks,fits=fits),indent=2))

def noise(suffix='noise',mode='main'):
    rows,dest=register(suffix,dict(script='scripts/p002_noise.jl',mode=mode,filters=['abs(ΩT0)<=1','ΩT0>=0','all'],temperature_K=300.,photon_convention='constant carrier weight; no shock',raman_reservoir='symmetric Wigner, analytic causal kernels, RWA pair Gram'))
    summary=json.loads((dest/'summary.json').read_text())
    summary.update(max_total_count_F_error=max(abs(x['total_count_F']-1) for x in rows),max_total_count_Raman_F=max(x['total_count_Raman_F'] for x in rows),max_Kerr_mode_count_F_error=max([abs(y['F02']-1) for x in rows if x['response']=='none' for y in x['rows'] if y['filter']=='all'] or [0.]),
        min_optical_covariance_eigenvalue=min(x['min_optical_covariance_eigenvalue'] for x in rows),
        min_Raman_covariance_eigenvalue=min(x['min_Raman_covariance_eigenvalue'] for x in rows),
        max_temporal_edge_fraction=max(x['mean_diagnostics']['temporal_edge_fraction'] for x in rows),
        max_spectral_edge_fraction=max(x['mean_diagnostics']['spectral_edge_fraction'] for x in rows))
    if mode=='convergence':
        base=json.loads((ROOT/'runs/2026-10-04-gpt-a-noise/summary.json').read_text())['cases']
        comparisons=[]
        for x in rows:
            b=next(y for y in base if y['response']==x['response'] and y['r']==x['r'] and y['delta']==x['delta'])
            for q in x['rows']:
                qb=next(y for y in b['rows'] if y['filter']==q['filter'])
                comparisons.append(dict(label=x['label'],filter=q['filter'],
                    changes={key:q[key]-qb[key] for key in ('F01','F02','rho','F01_optical','F02_optical','F01_Raman','F02_Raman')},
                    base={key:qb[key] for key in ('F01','F02','rho')},
                    refined={key:q[key] for key in ('F01','F02','rho')}))
        summary['comparisons']=comparisons
    (dest/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2))

def three_scaling():
    rows,dest=register('three-scaling',dict(script='scripts/p002_capture.jl',mode='three_scaling',
        r=[.0001,.0003,.001,.003,.03,.1],delta=[0.,1.],zeta=20.,dzeta=.01,nt=4096,window_tau=320.))
    scaling=[]
    for delta in (0.,1.):
        cases=sorted([x for x in rows if x['delta']==delta],key=lambda q:q['r'])
        r=np.array([x['r'] for x in cases]);energy=np.array([x['rows'][-1]['energies'][2] for x in cases])
        errors=[]
        for x in cases:
            for q in x['rows']:
                n1,n2,n3=q['energies'];errors.extend([abs(n1-n3-2),abs(n2+2*n3-2*x['r'])])
        scaling.append(dict(delta=delta,r=r.tolist(),LP03_energy=energy.tolist(),
            LP03_energy_over_r_squared=(energy/r**2).tolist(),
            LP02_projection=[x['rows'][-1]['bound_projection'] for x in cases],
            absolute_energy_exponent_epsilon=float(np.polyfit(np.log(np.sqrt(r[:3])),np.log(energy[:3]),1)[0]),
            max_Manley_Rowe_absolute_error=max(errors)))
    p=dest/'summary.json';s=json.loads(p.read_text());s['scaling']=scaling;p.write_text(json.dumps(s,indent=2)+'\n')
    print(json.dumps(scaling,indent=2))

def noise_plot():
    base=ROOT/'runs/2026-10-04-gpt-a-noise'
    rows=json.loads((base/'summary.json').read_text())['cases']
    small=ROOT/'runs/2026-10-04-gpt-a-noise-small'/'summary.json'
    if small.exists():rows+=json.loads(small.read_text())['cases']
    fig,axs=plt.subplots(2,3,figsize=(11,6),sharex='col')
    limits=[]
    for di in (1,2):
        for response,color in [('none','black'),('agarwal','tab:blue'),('anisotropic','tab:orange')]:
            cases=sorted([x for x in rows if x['label'].startswith(f'{response}_d{di}_r')],key=lambda x:x['r'])
            r=np.array([x['r'] for x in cases])
            for fi,filt in enumerate(('band','edge')):
                qs=[next(q for q in x['rows'] if q['filter']==filt) for x in cases]
                style='-' if di==2 else '--'
                label=response+(' physical δ' if di==2 else ' δ=0')
                for col,key in enumerate(('F01','F02','rho')):
                    axs[fi,col].semilogx(r,[q[key] for q in qs],'o'+style,color=color,label=label,markersize=3)
                    axs[fi,col].set_ylabel(f'{filt}: {key}')
                limits.append(dict(response=response,delta=cases[0]['delta'],filter=filt,
                    smallest_r=float(r[0]),F01=qs[0]['F01'],F02=qs[0]['F02'],rho=qs[0]['rho'],
                    change_F01_to_r003=next(q['F01'] for x,q in zip(cases,qs) if x['r']==.003)-qs[0]['F01'],
                    change_F02_to_r003=next(q['F02'] for x,q in zip(cases,qs) if x['r']==.003)-qs[0]['F02']))
    for ax in axs[-1,:]:ax.set_xlabel('Launch energy ratio r = ε²')
    axs[0,2].legend(fontsize=7,loc='best');fig.tight_layout();fig.savefig(base/'noise.png',dpi=170);plt.close(fig)
    dest=ROOT/'runs/2026-10-04-gpt-a-noise-small'/'summary.json'
    if dest.exists():
        summary=json.loads(dest.read_text());summary['smallest_r_readouts']=limits
        dest.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(limits,indent=2))

def noise_cw():
    rows,dest=register('noise-cw',dict(script='scripts/p002_noise_cw.jl',
        physical_model='Periodic CW, undepleted-pump limit',responses=['agarwal','anisotropic'],
        r=[1e-6,1e-8],zeta=[.01,.02],temperature_K=[0.,300.],
        temporal_frequency_sign=[-1,1],nt=64,window_tau=40.,harmonic=4,
        dzeta=.0001,reservoir_zspacing=.001))
    checks=rows[0]['rows'];metrics=[]
    for r in (1e-6,1e-8):
        q=[x for x in checks if x['r']==r]
        metrics.append(dict(r=r,max_relative_bath_error=max(x['relative_bath_error'] for x in q),
            max_optical_minus_gain= max(abs(x['optical_minus_gain']) for x in q),
            max_relative_gain_exponent_error=max(x['relative_gain_exponent_error'] for x in q),
            max_total_F_error=max(abs(x['F_total']-x['predicted_F_total']) for x in q),
            max_zero_temperature_attenuator_F_error=max(abs(x['F_total']-1) for x in q if x['temperature_K']==0 and x['gain']<1)))
    p=dest/'summary.json';s=json.loads(p.read_text());s['control_errors']=metrics;p.write_text(json.dumps(s,indent=2)+'\n')
    p=dest/'meta.yaml';m=yaml.safe_load(p.read_text());m['prediction_commit']='444c177';p.write_text(yaml.safe_dump(m,sort_keys=False))
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='capture':capture()
    elif mode=='convergence':convergence()
    elif mode=='gates':gate_analysis()
    elif mode=='three-scaling':three_scaling()
    elif mode=='noise-plot':noise_plot()
    elif mode=='noise-cw':noise_cw()
    elif mode.startswith('noise'):noise(mode,'main' if mode=='noise' else mode.split('-')[-1])
    else:raise ValueError(mode)
