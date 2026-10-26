#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt"""
import json, platform, subprocess, sys
from pathlib import Path
import numpy as np
import tomli, yaml
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from p002_nextorder import ROOT, RAW, IDENT, MAT, bound

PREFIX='2026-10-04-gpt-a-'
HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
SOLVER=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
SOLVER_DIRTY=bool(subprocess.check_output(['git','-C',str(ROOT/'solver'),'status','--porcelain'],text=True).strip())
FULL_HARNESS='75ca4e5'

def read(suffix):
    return json.loads((ROOT/'runs'/(PREFIX+suffix)/'summary.json').read_text())

def write(suffix,s):
    (ROOT/'runs'/(PREFIX+suffix)/'summary.json').write_text(json.dumps(s,indent=2,allow_nan=False)+'\n')

def register(suffix,script,mode,source):
    raw=RAW/(PREFIX+suffix);dest=ROOT/'runs'/(PREFIX+suffix);dest.mkdir(parents=True,exist_ok=True)
    cases=[json.loads(p.read_text()) for p in sorted(raw.glob('*.json'))]
    cases += [tomli.loads(p.read_text()) for p in sorted(raw.glob('*.toml'))]
    s=dict(IDENT,run_id=PREFIX+suffix,cases=cases)
    write(suffix,s)
    prediction_file='runs/'+PREFIX+'nextorder-prediction/summary.json'
    freeze=subprocess.check_output(['git','log','-1','--format=%H','--',prediction_file],cwd=ROOT,text=True).strip()
    meta=dict(IDENT,run_id=PREFIX+suffix,task='T-20261004-claude-interactive-07',
        claim='C-20261004-gpt-a-01',solver_commit=SOLVER,solver_dirty=SOLVER_DIRTY,
        harness_commit=source,analysis_commit=HEAD,prediction_commit=freeze or 'functional freeze 751cddf; numerical freeze follows this registration',
        hardware=platform.node(),raw_location=str(raw),wall_time_seconds=sum(x.get('elapsed_seconds',0.) for x in cases),
        julia_threads=2 if script.endswith('.jl') else 0,blas_threads=1,fft_threads=1,
        randomness='none; deterministic equations and fixed phases',status='completed')
    meta_file=dest/'meta.yaml'
    if meta_file.exists():
        previous=yaml.safe_load(meta_file.read_text())
        for key in ('failed_attempts','successful_case_sources'):
            if key in previous:meta[key]=previous[key]
    meta_file.write_text(yaml.safe_dump(meta,sort_keys=False))
    (dest/'config.yaml').write_text(yaml.safe_dump(dict(IDENT,script=script,mode=mode,
        full_parameters='Retained per case in summary.json and in the frozen script.'),sort_keys=False))
    return s,dest

def prediction():
    s,dest=register('nextorder-prediction','scripts/p002_nextorder.py','symbolic and prediction','751cddf')
    boundary=next(x for x in s['cases'] if 'delta_half_zeroth' in x)
    (dest/'boundary.toml').write_text('\n'.join([f'{k} = "{v}"' for k,v in IDENT.items()]+[
        f'delta_half_zeroth = {boundary["delta_half_zeroth"]:.17g}',
        f'delta_half_slope_r = {boundary["delta_half_slope_r"]:.17g}',
        'zeta = 13.0'])+'\n')
    preds=[]
    for x in s['cases']:
        if 'C0_analytic' not in x:continue
        for row in x['rows'][1:]:
            for r in (.0002,.0006,.002):
                preds.append(dict(label=x['label'],r=r,zeta=row['zeta'],
                    B_pred=x['C0_analytic']+r*row['B1'],W_pred=row['W0']+r*row['W1'],
                    LP03_energy_pred=r*r*row['LP03_coefficient']))
    s['frozen_predictions']=preds;write('nextorder-prediction',s)
    print(json.dumps(boundary,indent=2))

def response_checks():
    s,_=register('nextorder-response-checks','scripts/p002_nextorder.py','convergence and ablation','751cddf')
    base=read('nextorder-prediction')['cases'];comparisons=[]
    for x in s['cases']:
        if x['ablation']!='none':continue
        ref=next(y for y in base if y.get('label')==('physical' if x['label'].startswith('physical') else 'ideal_d3'))
        for row,b in zip(x['rows'],ref['rows']):
            comparisons.append(dict(label=x['label'],zeta=row['zeta'],
                changes={k:row[k]-b[k] for k in ('B0','B1','W0','W1','LP03_coefficient')}))
    s['comparisons']=comparisons
    if (ROOT/'runs'/(PREFIX+'nextorder-full')/'summary.json').exists():
        full_cases=[x for x in read('nextorder-full')['cases'] if x['label'].startswith('ideal_d3_r')]
        base_case=next(x for x in base if x.get('label')=='ideal_d3')
        ablation_errors=[];ablation_fits=[]
        for case in s['cases']:
            if case['ablation']=='none':continue
            response=np.load(RAW/(PREFIX+'nextorder-response-checks')/(case['label']+'.npz'))['fields']
            for full_case in full_cases:
                r=full_case['r']
                fields=np.load(RAW/(PREFIX+'nextorder-full')/(full_case['label']+'.npz'))['fields']
                for j,row in enumerate(full_case['rows'][1:],1):
                    v,U,w,V=response[j].T
                    minority=fields[:,1,0,j]/np.sqrt(MAT['P0_W']*r)
                    ablation_errors.append(dict(ablation=case['ablation'],r=r,zeta=case['rows'][j]['zeta'],
                        minority_field_error=float(np.linalg.norm(minority-v-r*V)/np.linalg.norm(v)),
                        B_error=row['reference_projection']-base_case['C0_analytic']-r*case['rows'][j]['B1']))
            for z in (7.,13.,19.):
                q=sorted([x for x in ablation_errors if x['ablation']==case['ablation'] and x['zeta']==z],key=lambda x:x['r'])
                exponents={key:float(np.polyfit(np.log(np.sqrt([x['r'] for x in q])),np.log(np.abs([x[key] for x in q])),1)[0])
                    for key in ('minority_field_error','B_error')}
                ablation_fits.append(dict(ablation=case['ablation'],zeta=z,exponents_epsilon=exponents))
        s.update(ablation_errors=ablation_errors,ablation_exponents=ablation_fits)
    write('nextorder-response-checks',s)
    print(json.dumps(comparisons[-3:],indent=2))

def gate(t,v):
    ids=(t>-5)&(t<5);xx=np.r_[-5,t[ids],5];yy=abs(v)**2
    return float(np.trapezoid(np.r_[np.interp(-5,t,yy),yy[ids],np.interp(5,t,yy)],xx)/2)

def full():
    s,dest=register('nextorder-full','scripts/p002_nextorder_full.jl','main',FULL_HARNESS)
    preds={x['label']:x for x in read('nextorder-prediction')['cases'] if 'C0_analytic' in x}
    comp=[];p0=MAT['P0_W']
    for x in s['cases']:
        key=x['label'].split('_r')[0];pred=preds[key];r=x['r']
        fp=np.load(RAW/(PREFIX+'nextorder-prediction')/(key+'.npz'))
        ff=np.load(RAW/(PREFIX+'nextorder-full')/(x['label']+'.npz'))
        for j,row in enumerate(x['rows']):
            if j==0:continue
            b=pred['rows'][j];v,U,w,V=fp['fields'][j].T
            a=ff['fields'][:,:,0,j]/np.sqrt(p0);t=ff['tau']
            val=a[:,1]/np.sqrt(r);bp=pred['C0_analytic']+r*b['B1'];wp=b['W0']+r*b['W1']
            f=1/np.cosh(t)*np.exp(.5j*row['zeta'])
            comp.append(dict(label=key,r=r,zeta=row['zeta'],B=row['reference_projection'],B0=pred['C0_analytic'],
                B_pred=bp,B_error=row['reference_projection']-bp,
                W=gate(t,val),W_pred=wp,W_error=gate(t,val)-wp,
                minority_field_error=float(np.linalg.norm(val-v-r*V)/np.linalg.norm(v)),
                first_order_field_error=float(np.linalg.norm(val-v)/np.linalg.norm(v)),
                pump_field_error=float(np.linalg.norm(a[:,0]-f-r*U)/np.linalg.norm(f)),
                LP03_field_error=float(np.linalg.norm(a[:,2]-r*w)/np.linalg.norm(f)),
                LP03_energy=row['energies'][2],LP03_pred=r*r*b['LP03_coefficient'],
                LP03_energy_error=row['energies'][2]-r*r*b['LP03_coefficient']))
    fits=[]
    for key in preds:
        for z in (7.,13.,19.):
            points=sorted([x for x in comp if x['label']==key and abs(x['zeta']-z)<1e-8],key=lambda x:x['r'])
            if len(points)!=3:continue
            rr=np.array([x['r'] for x in points])
            powers={k:float(np.polyfit(np.log(np.sqrt(rr)),np.log(np.abs([x[k] for x in points])),1)[0])
                for k in ('B_error','W_error','minority_field_error','first_order_field_error','pump_field_error','LP03_field_error','LP03_energy_error')}
            fits.append(dict(label=key,zeta=z,exponent_epsilon=powers))
    diagnostics=dict(max_total_energy_drift=0.,max_MR_N1_minus_N3_drift=0.,
        max_MR_N2_plus_2N3_drift=0.,max_temporal_edge_fraction=0.,max_spectral_edge_fraction=0.)
    for case in s['cases']:
        start=np.array(case['rows'][0]['energies'])
        for row in case['rows']:
            en=np.array(row['energies'])
            diagnostics['max_total_energy_drift']=max(diagnostics['max_total_energy_drift'],float(abs(en.sum()-start.sum())))
            diagnostics['max_MR_N1_minus_N3_drift']=max(diagnostics['max_MR_N1_minus_N3_drift'],float(abs(en[0]-en[2]-start[0]+start[2])))
            diagnostics['max_MR_N2_plus_2N3_drift']=max(diagnostics['max_MR_N2_plus_2N3_drift'],float(abs(en[1]+2*en[2]-start[1]-2*start[2])))
            for key in ('temporal_edge_fraction','spectral_edge_fraction'):
                diagnostics['max_'+key]=max(diagnostics['max_'+key],row[key])
    diagnostics['exponent_ranges_epsilon']={key:[min(x['exponent_epsilon'][key] for x in fits),
        max(x['exponent_epsilon'][key] for x in fits)] for key in fits[0]['exponent_epsilon']}
    s.update(comparisons=comp,error_exponents=fits,diagnostics=diagnostics);write('nextorder-full',s)
    fig,axs=plt.subplots(1,3,figsize=(12,4.2))
    labels={'ideal_d1':'ideal δ=0','ideal_d2':'ideal δ=0.35','ideal_d3':'ideal δ=0.85',
        'ideal_d4':'ideal δ=1.35','perturbed':'perturbed δ=0.85','physical':'archive dispersion'}
    for j,(key,label) in enumerate(labels.items()):
        q=sorted([x for x in comp if x['label']==key and abs(x['zeta']-19)<1e-8],key=lambda x:x['r'])
        rr=np.sqrt([x['r'] for x in q])
        color=f'C{j}'
        axs[0].loglog(rr,[x['first_order_field_error'] for x in q],'--',alpha=.5,color=color)
        axs[0].loglog(rr,[x['minority_field_error'] for x in q],'o-',label=label,color=color)
        axs[1].loglog(rr,np.abs([x['B_error'] for x in q]),'o-',label=label,color=color)
    guide=np.array([.014,.045]);axs[1].loglog(guide,3*guide**4,':',color='black',label='ε⁴ guide')
    axs[1].legend(fontsize=8,handles=[axs[1].lines[-1]])
    zero=preds['ideal_d1'];zs=[x['zeta'] for x in zero['rows']]
    axs[2].plot(zs,[x['LP03_coefficient'] for x in zero['rows']],'o',label='Response K')
    law=next(x for x in read('nextorder-prediction')['cases'] if 'ground_overlap_squared' in x)
    z=np.linspace(0,20,401);kg=4-2*law['ground_overlap_squared']*np.cos(law['beat_gap']*z)
    axs[2].plot(z,kg,label='One bound state');err=law['ground_only_absolute_K_error_bound']
    axs[2].fill_between(z,kg-err,kg+err,alpha=.2)
    axs[0].set(xlabel='ε = √r',ylabel='Minority field relative error',title='Dashed: first order; solid: corrected')
    axs[1].set(xlabel='ε = √r',ylabel='Absolute projection error')
    axs[2].set(xlabel='ζ',ylabel='LP03 coefficient K at δ=0')
    fig.legend(*axs[0].get_legend_handles_labels(),loc='upper center',ncol=3,fontsize=8)
    axs[2].legend(fontsize=8);fig.tight_layout(rect=[0,0,1,.84]);fig.savefig(dest/'nextorder.png',dpi=170);plt.close(fig)
    print(json.dumps([x for x in fits if x['zeta']==19],indent=2))

def boundary_report():
    s,_=register('nextorder-boundary','scripts/p002_nextorder_full.jl','boundary',FULL_HARNESS)
    q=sorted(s['cases'],key=lambda x:x['r'])
    error=np.array([x['rows'][-1]['reference_projection']-.5 for x in q])
    s['criterion_residuals']=[dict(r=x['r'],delta=x['parameters']['delta'],residual=float(e)) for x,e in zip(q,error)]
    s['exponent_epsilon']=float(np.polyfit(np.log(np.sqrt([x['r'] for x in q])),np.log(abs(error)),1)[0])
    write('nextorder-boundary',s);print(json.dumps({k:v for k,v in s.items() if k!='cases'},indent=2))

def convergence_report():
    s,_=register('nextorder-convergence','scripts/p002_nextorder_full.jl','convergence',FULL_HARNESS)
    base=read('nextorder-full')['cases'];comparisons=[]
    for x in s['cases']:
        b=next(y for y in base if y['label']==('physical_r0.002' if x['label'].startswith('physical') else 'ideal_d3_r0.002'))
        refined=np.load(RAW/(PREFIX+'nextorder-convergence')/(x['label']+'.npz'))
        original=np.load(RAW/(PREFIX+'nextorder-full')/(b['label']+'.npz'))
        fine_gate=gate(refined['tau'],refined['fields'][:,1,0,-1]/np.sqrt(MAT['P0_W']*x['r']))
        base_gate=gate(original['tau'],original['fields'][:,1,0,-1]/np.sqrt(MAT['P0_W']*b['r']))
        comparisons.append(dict(label=x['label'],projection_difference=x['rows'][-1]['reference_projection']-b['rows'][-1]['reference_projection'],
            endpoint_corrected_gate_difference=fine_gate-base_gate,
            LP03_energy_difference=x['rows'][-1]['energies'][2]-b['rows'][-1]['energies'][2],
            last_plane=x['rows'][-1]))
    s['comparisons']=comparisons;write('nextorder-convergence',s);print(json.dumps(comparisons,indent=2))

def phase_report():
    s,dest=register('nextorder-phase','scripts/p002_nextorder_full.jl','phase, then phase-resume',['75ca4e5','206cf23'])
    null=[x for x in s['cases'] if x['label'].startswith('null_')]
    energies=np.array([[y['energies'] for y in x['rows']] for x in null])
    s['null_max_energy_spread']=float(np.max(np.ptp(energies,axis=0)))
    field_errors=[]
    ref=np.load(RAW/(PREFIX+'nextorder-phase')/'null_p1.npz')['fields']
    for x in null:
        a=np.load(RAW/(PREFIX+'nextorder-phase')/(x['label']+'.npz'))['fields']
        rotate=np.exp(-1j*np.arange(3)*x['phase02'])[None,:,None,None]
        field_errors.append(float(np.linalg.norm(a*rotate-ref)/np.linalg.norm(ref)))
    s['null_max_symmetry_relative_field_error']=max(field_errors)
    flux=[]
    for kind in ('ideal','physical'):
        plus=next(x for x in s['cases'] if x['label']==f'flux_{kind}_p1')
        minus=next(x for x in s['cases'] if x['label']==f'flux_{kind}_p2')
        predicted=-4/3*plus['r']**2
        for a,b in zip(plus['rows'][1:],minus['rows'][1:]):
            value=(a['energies'][1]-b['energies'][1])/(2*a['zeta'])
            flux.append(dict(kind=kind,zeta=a['zeta'],predicted=predicted,measured_odd_slope=value,relative_error=abs(value-predicted)/abs(predicted)))
    s['initial_flux_checks']=flux
    spread=[]
    fig,axs=plt.subplots(1,2,figsize=(9,3.4))
    for ax,r in zip(axs,(.003,.01)):
        q=sorted([x for x in s['cases'] if x['label'].startswith(f'seed_r{r}_')],key=lambda x:x['phase03'])
        vals=np.array([x['rows'][-1]['energies'] for x in q])
        spread.append(dict(r=r,zeta=13.,LP02_energy_spread=float(np.ptp(vals[:,1])),LP02_relative_spread=float(np.ptp(vals[:,1])/(2*r))))
        for x in q:
            ax.plot([y['zeta'] for y in x['rows']],[y['energies'][1]/(2*r) for y in x['rows']],'-o',label=f"Φ/π={x['phase03']/np.pi:.1f}",markersize=3)
        ax.set(xlabel='ζ',ylabel='LP02 energy / launch LP02 energy',title=f'r={r:g}')
    axs[0].legend(fontsize=8);fig.tight_layout();fig.savefig(dest/'phase.png',dpi=170);plt.close(fig)
    s['seeded_phase_spreads']=spread;write('nextorder-phase',s)
    print(json.dumps({k:v for k,v in s.items() if k!='cases'},indent=2))

def detuning_report():
    response,_=register('nextorder-detuning-response','scripts/p002_detuning.py','response','8cb0b5b')
    full,dest=register('nextorder-detuning-full','scripts/p002_detuning_full.jl','all','8cb0b5b')
    prediction=read('nextorder-detuning-prediction');intervals=[];errors=[]
    for x in response['cases']:
        if x['label'].endswith('halfstep'):continue
        for row in x['rows'][1:]:
            ref=next(y for y in prediction['rows'] if y['mu']==x['parameters']['mu'] and y['zeta']==row['zeta'])
            value=row['LP03_coefficient']
            intervals.append(dict(label=x['label'],mu=ref['mu'],zeta=row['zeta'],K=value,
                lower=ref['K_lower'],upper=ref['K_upper'],inside=ref['K_lower']<=value<=ref['K_upper']))
    for x in full['cases']:
        key=x['label'].split('_r')[0];ref=next(y for y in response['cases'] if y['label']==key)
        for row,pred in zip(x['rows'][1:],ref['rows'][1:]):
            val=row['energies'][2];theory=x['r']**2*pred['LP03_coefficient']
            errors.append(dict(label=key,r=x['r'],mu=x['mu'],zeta=pred['zeta'],LP03_energy=val,
                prediction=theory,error=val-theory))
    fits=[]
    for key in ('mu1','mu2','mu3'):
        for z in (5.,11.,17.):
            q=sorted([x for x in errors if x['label']==key and x['zeta']==z],key=lambda x:x['r'])
            power=float(np.polyfit(np.log(np.sqrt([x['r'] for x in q])),np.log(np.abs([x['error'] for x in q])),1)[0])
            fits.append(dict(label=key,zeta=z,energy_error_exponent_epsilon=power))
    base=next(x for x in response['cases'] if x['label']=='mu3')
    fine=next(x for x in response['cases'] if x['label']=='mu3_halfstep')
    response['analytic_interval_checks']=intervals
    response['halfstep_K_differences']=[b['LP03_coefficient']-a['LP03_coefficient'] for a,b in zip(base['rows'],fine['rows'])]
    full.update(comparisons=errors,error_exponents=fits)
    write('nextorder-detuning-response',response);write('nextorder-detuning-full',full)
    for suffix in ('nextorder-detuning-response','nextorder-detuning-full'):
        file=ROOT/'runs'/(PREFIX+suffix)/'meta.yaml';meta=yaml.safe_load(file.read_text())
        meta['prediction_commit']='8cb0b5b'
        file.write_text(yaml.safe_dump(meta,sort_keys=False))
    fig,axs=plt.subplots(1,3,figsize=(11,3.3))
    for ax,key in zip(axs,('mu1','mu2','mu3')):
        q=[x for x in intervals if x['label']==key];z=[x['zeta'] for x in q]
        lo=np.array([x['lower'] for x in q]);hi=np.array([x['upper'] for x in q])
        ax.errorbar(z,(lo+hi)/2,yerr=(hi-lo)/2,fmt='none',capsize=7,elinewidth=3,alpha=.35,label='Analytic interval')
        ax.plot(z,[x['K'] for x in q],'o',label='Response')
        for r,marker in ((.0002,'+'),(.002,'x')):
            v=[x for x in errors if x['label']==key and x['r']==r]
            ax.plot([x['zeta'] for x in v],[x['LP03_energy']/r**2 for x in v],marker,label=f'Full, r={r:g}')
        ax.set(xlabel='ζ',ylabel='LP03 energy coefficient K',title=f"μ={q[0]['mu']:g}")
        ax.ticklabel_format(axis='y',style='sci',scilimits=(-2,2))
    axs[0].legend(fontsize=7);fig.tight_layout();fig.savefig(dest/'detuning.png',dpi=170);plt.close(fig)
    print(json.dumps(dict(interval_checks=intervals,error_exponents=fits,
        halfstep_K_differences=response['halfstep_K_differences']),indent=2))

if __name__=='__main__':
    {'prediction':prediction,'response-checks':response_checks,'full':full,'boundary':boundary_report,
        'convergence':convergence_report,'phase':phase_report,'detuning':detuning_report}[sys.argv[1]]()
