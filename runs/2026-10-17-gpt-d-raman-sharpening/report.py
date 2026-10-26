#!/usr/bin/env python3
"""Aggregate frozen runs and draw PI figures; gpt-d/gpt-6-astra/gpt."""
from pathlib import Path
import json, platform, time
try:
    import tomllib
except ImportError:
    import tomli as tomllib
import numpy as np
from scipy.signal import find_peaks
from scipy.fft import fft
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import HERE,RAW,IDENTITY,exact_mp

ROOT=HERE.parents[1]
PROP=HERE.parent/'2026-10-17-gpt-d-raman-propagation'
PRAW=RAW.parent/PROP.name
COND=HERE.parent/'2026-10-17-gpt-d-raman-conditional'
CRAW=RAW.parent/COND.name

def dump(path,obj):path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def main():
    started=time.time(); COND.mkdir(exist_ok=True); CRAW.mkdir(parents=True,exist_ok=True)
    config=json.loads((PROP/'config.yaml').read_text());cfgs={c['name']:c for c in config['cases']}
    cases={p.stem.replace('_summary',''):json.loads(p.read_text()) for p in PRAW.glob('*_summary.json')}
    planes={name:np.genfromtxt(PRAW/(name+'_planes.csv'),delimiter=',',names=True) for name in cases}
    primary=[c['name'] for c in config['cases'] if 'convergence_of' not in c and 'relaxation' not in c]
    for name,s in cases.items():
        p=planes[name];c=cfgs[name]
        s['max_accepted_photon_drift']=float(np.max(abs(p['photon_norm']/p['photon_norm'][0]*np.exp(c['alpha_m']*p['z_m'])-1)))
        s['accepted_plane_count']=len(p);s['rhs_stage_evaluation_count']=4*c['steps']+1
        s['min_accepted_rho']=float(np.min(p['rho_rhs']))
        s['accepted_bound_violations']=int(np.sum(p['rho_rhs']>1+1e-6))
        s['accepted_conditional_violations']=int(np.sum(p['rho_rhs']>p['F_Q']+1e-6))
        s['max_accepted_conditional_ratio']=float(np.max(p['rho_rhs']/p['F_Q']))
        s['max_Q_at_accepted_planes']=float(np.max(p['Q_psinv']))
        s['photon_diagnostic_note']='max_photon_drift includes RK stages; accepted-plane invariant drift is reported separately. Original raw summary retained.'
        s['accepted_plane_checks_pass']=bool(s['max_rho']<=1+1e-6 and
            s['min_lossaware_margin']>=-1e-6 and s['max_identity_residual_over_bound']<1e-5 and
            s['integrated_identity_relative_mismatch']<1e-3 and s['max_accepted_photon_drift']<1e-5 and
            s['max_time_edge_fraction']<1e-6 and s['max_spectral_edge_fraction']<1e-6)
        if len(c['oscillators'])==1:
            osc=c['oscillators'][0]
            s['launch_T_over_tau1']=c['T_ps']/osc['tau1_ps']
            s['launch_omega0_T']=2*np.pi*299.792458/c['lambda_um']*c['T_ps']
            ex=float(exact_mp(s['launch_T_over_tau1'],osc['tau1_ps']/osc['tau2_ps']))
            s['launch_rho_exact']=ex
            s['launch_RHS_relative_difference']=float(abs(p['rho_rhs'][0]/ex-1))
        fields=np.load(PRAW/(name+'_fields.npz'))
        I=abs(fft(fields['aw_final']))**2
        peaks,_=find_peaks(I,height=.1*max(I),distance=max(2,round(c['T_ps']/(3*c['dt_ps']))))
        s['final_prominent_intensity_lobes']=len(peaks)
        s['lobe_diagnostic_definition']='Local maxima above 10% of final peak, separated by at least launch T/3; not a nonlinear-eigenvalue soliton count.'
    conv={}
    for key in ['integrated_identity_relative_mismatch','max_accepted_photon_drift']:
        seq=[cases[n] for n in ['core','core_half','core_quarter']]
        conv['core_'+key+'_slope']=float(np.polyfit(np.log([s['h_m'] for s in seq]),np.log([s[key] for s in seq]),1)[0])
    for name in ['h6_100_half','h6_100_fine','h6_100_wide']:
        s=cases[name];base=cases['h6_100']
        conv[name]=dict(rho_relative_change=abs(s['max_accepted_rho']/base['max_accepted_rho']-1),
            retention_absolute_change=abs(s['Eout_over_E0']-base['Eout_over_E0']))
    julia={}
    for name in ['core','h6_100']:
        path=PRAW/('julia_'+name+'.toml')
        if not path.exists():continue
        j=tomllib.loads(path.read_text());base=cases['h6_100_fine' if name=='h6_100' else name]
        j['retention_absolute_difference']=abs(j['Eout_over_E0']-base['Eout_over_E0'])
        j['rho_relative_difference']=abs(j['max_accepted_rho']/base['max_accepted_rho']-1)
        julia[name]=j
    analysis=dict(primary_cases=primary,primary_case_count=len(primary),held_out_primary_count=sum(cfgs[n]['held_out'] for n in primary),
        primary_accepted_plane_count=sum(cases[n]['accepted_plane_count'] for n in primary),
        primary_rhs_evaluations=sum(cases[n]['rhs_stage_evaluation_count'] for n in primary),
        max_primary_rho_case=max(primary,key=lambda n:cases[n]['max_accepted_rho']),
        max_primary_accepted_rho=max(cases[n]['max_accepted_rho'] for n in primary),
        all_accepted_checks_pass=all(s['accepted_plane_checks_pass'] for s in cases.values()),
        max_primary_photon_drift=max(cases[n]['max_accepted_photon_drift'] for n in primary),
        max_primary_identity_residual=max(cases[n]['max_identity_residual_over_bound'] for n in primary),
        max_primary_integrated_identity_mismatch=max(cases[n]['integrated_identity_relative_mismatch'] for n in primary),
        convergence=conv,julia=julia)
    dump(PROP/'summary.json',dict(**IDENTITY,run_id=PROP.name,freeze_commit=config['freeze_commit'],cases=cases,analysis=analysis))
    mathsum=json.loads((HERE/'summary.json').read_text());curves=np.load(RAW/'analytic_curves.npz')
    plt.rcParams.update({'font.size':11,'axes.labelsize':12,'legend.fontsize':10,'axes.spines.top':False,
        'axes.spines.right':False,'savefig.facecolor':'white'})
    fig,ax=plt.subplots(figsize=(7.4,4.8),layout='constrained')
    x=curves['x'];r=12.2/32;c3=16*r/(15*(1+r*r)**2)
    ax.loglog(x,curves['rho'][0],color='#175783',lw=2,label='Silica oscillator: exact')
    ax.loglog(x,curves['rho'][1],color='#8055a0',lw=1.7,ls='-.',label='ZBLAN oscillator: exact')
    xl=x[x>2];ax.loglog(xl,c3/xl**3,color='#d07a16',ls='--',lw=1.7,label=r'Long pulse: $C_3(T/\tau_1)^{-3}$')
    xs=x[x<.5];ax.loglog(xs,1-2*r*xs,color='#34865c',ls=':',lw=2,label=r'Short pulse: $1-2T/\tau_2$')
    for i,rv in enumerate(curves['r'][:2]):
        rows=[v for v in mathsum['quadrature'] if abs(v['r']-rv)<1e-12]
        ax.plot([v['x'] for v in rows],[v['quadrature'] for v in rows],ls='none',marker='o',ms=4,
            mec='#175783' if i==0 else '#8055a0',mfc='white',mew=1,
            label='Independent quadrature' if i==0 else None)
    for name in primary:
        c=cfgs[name];s=cases[name];fl=name=='fluoride'
        label='GNLSE: core' if name=='core' else ('GNLSE: held-out silica' if name=='h1_30' else ('GNLSE: held-out ZBLAN' if fl else None))
        ax.plot(s['launch_T_over_tau1'],s['max_accepted_rho'],marker='D' if fl else '^',ms=7.5,
            mec='#8055a0' if fl else '#b34338',mfc='#b34338' if name=='core' else 'white',mew=1.5,
            ls='none',label=label,zorder=5)
    ax.axhline(1,color='0.3',lw=.8,ls='--');ax.text(.003,1.2,r'Universal ceiling $\rho=1$',fontsize=10)
    ax.set(xlim=(.0015,200),ylim=(2e-8,1.8),xlabel=r'Sech width / Raman time, $T/\tau_1$ (dimensionless)',
        ylabel=r'Raman loss rate / energy ceiling, $\rho$')
    ax.grid(True,which='major',color='0.9',lw=.6);ax.legend(loc='lower left',framealpha=.96,ncol=1)
    fig.savefig(HERE/'fig_summary.png',dpi=160,metadata={'Author':'gpt-d; gpt-6-astra; gpt','Run':HERE.name});plt.close(fig)
    # The conditional improvement gets its own derived analysis run and one panel.
    condpts=[]
    for name in primary:
        c=cfgs[name];s=cases[name];p=planes[name];idx=np.argmax(p['rho_rhs']);tau2=c['oscillators'][0]['tau2_ps']
        condpts.append(dict(case=name,tau2_Q=float(tau2*p['Q_psinv'][idx]),rho=float(p['rho_rhs'][idx]),
            F_Q=float(p['F_Q'][idx]),held_out=c['held_out']))
    profiles=mathsum['profiles'];r=12.2/32
    fig,ax=plt.subplots(figsize=(7.4,4.6),layout='constrained')
    u=np.geomspace(.001,100,501)
    ax.loglog(u,2/np.pi*np.arctan(np.pi*u/2),color='#175783',lw=2.2,label='Conditional ceiling')
    ax.loglog(u,np.minimum(1,u),color='0.5',ls='--',lw=1.5,label='Energy / supremum-weight ceiling')
    ax.scatter([p['Q']/r for p in profiles],[p['rho'] for p in profiles],s=18,facecolors='none',edgecolors='0.6',label='Profile checks')
    for p in condpts:
        ax.plot(p['tau2_Q'],p['rho'],marker='D' if p['case']=='fluoride' else '^',ms=8,ls='none',
            mec='#b34338',mfc='white' if p['held_out'] else '#b34338',mew=1.5,
            label='GNLSE: core' if p['case']=='core' else ('GNLSE: held out' if p['case']=='h1_30' else None))
    ax.set(xlim=(.001,100),ylim=(1e-5,1.5),xlabel=r'Intensity concentration, $\tau_2 Q$ (dimensionless)',
        ylabel=r'Raman loss rate / energy ceiling, $\rho$')
    ax.grid(True,which='major',color='0.9',lw=.6);ax.legend(loc='lower right',framealpha=.96)
    fig.savefig(COND/'fig_summary.png',dpi=160,metadata={'Author':'gpt-d; gpt-6-astra; gpt','Run':COND.name});plt.close(fig)
    dump(COND/'config.yaml',dict(**IDENTITY,run_id=COND.name,claim='C-20261017-gpt-d-02',
        source_runs=[HERE.name,PROP.name],predictions='../'+HERE.name+'/predictions.md',freeze_commit=config['freeze_commit'],
        reproduction='../'+HERE.name+'/report.py',seeds=[20261017]))
    dump(COND/'summary.json',dict(**IDENTITY,run_id=COND.name,source_runs=[HERE.name,PROP.name],
        maximum_profile_rho_over_F=mathsum['max_profile_ratio_to_conditional_bound'],
        profile_count=len(profiles),primary_propagation_max_ratio=max(cases[n]['max_accepted_conditional_ratio'] for n in primary),
        primary_propagation_violations=sum(cases[n]['accepted_conditional_violations'] for n in primary),
        levelset_max_relative_error=mathsum['max_levelset_relative_difference'],
        core_energy_only_retention=cases['core']['retention_lower_bound'],
        core_Qmax_conditional_retention=cases['core']['Qmax_conditional_retention_bound'],
        core_path_conditional_retention=cases['core']['path_conditional_retention_bound'],
        core_observed_retention=cases['core']['Eout_over_E0'],points=condpts))
    dump(COND/'meta.yaml',dict(**IDENTITY,run_id=COND.name,solver_commit=cases['core']['solver_commit'],solver_dirty=False,
        solver_note='Derived analysis of cited propagation and quadrature runs; no new forward simulation.',
        hardware=platform.node(),raw_location=str(CRAW),wall_time_s=time.time()-started,seeds=[20261017]))
    dump(CRAW/'plot_points.json',dict(propagation=condpts,profiles=profiles))
    print(json.dumps(analysis,indent=2))
    print('Figure bytes:',(HERE/'fig_summary.png').stat().st_size,(COND/'fig_summary.png').stat().st_size)

if __name__=='__main__':main()
