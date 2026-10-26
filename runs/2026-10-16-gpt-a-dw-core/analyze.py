#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt. Independent audit analysis."""
import json
import math
import os
from pathlib import Path
import numpy as np
import yaml
from scipy.fft import fft,ifft
from scipy.special import expit

ROOT=Path(__file__).resolve().parents[2]
RUNS=ROOT/'runs'
IDENTITY=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')

def read(slug):
    p=RUNS/('2026-10-16-gpt-a-'+slug)/'summary.json'
    return json.loads(p.read_text()) if p.exists() else {}

def fit_law(delta,y,dstar=None):
    delta=np.asarray(delta);y=np.asarray(y)
    if dstar is None:
        design=np.column_stack([np.ones(len(delta)),np.log(delta),-1/delta])
        c,p,d=np.linalg.lstsq(design,np.log(y),rcond=None)[0]
    else:
        d=dstar
        design=np.column_stack([np.ones(len(delta)),np.log(delta)])
        c,p=np.linalg.lstsq(design,np.log(y)+d/delta,rcond=None)[0]
    pred=c+p*np.log(delta)-d/delta
    return dict(c=float(c),p=float(p),d=float(d),
        delta3=delta.tolist(),log_residual=(np.log(y)-pred).tolist(),
        log_rms=float(np.sqrt(np.mean((np.log(y)-pred)**2))),
        fitted_parameters=['c','p','d'] if dstar is None else ['c','p'])

def logpredict(fit,delta):
    return fit['c']+fit['p']*math.log(delta)-fit['d']/delta

def slope_error(delta,y,dstar):
    delta=np.asarray(delta);logs=np.log(y)
    slopes=np.diff(logs)/(1/delta[:-1]-1/delta[1:])
    mids=(delta[:-1]+delta[1:])/2
    err=abs(slopes-dstar)/dstar
    p,c=np.polyfit(np.log(mids),np.log(err),1)
    predicted=c+p*np.log(mids)
    ss=sum((np.log(err)-np.mean(np.log(err)))**2)
    return dict(delta_mid=mids.tolist(),local_slopes=slopes.tolist(),
        relative_errors=err.tolist(),measured_exponent=float(p),predicted_exponent=1,
        r_squared=float(1-sum((np.log(err)-predicted)**2)/ss),
        fit_interval=[float(min(mids)),float(max(mids))])

def eq6(delta,N=2):
    return (5*np.pi*N/(4*delta))**2*(1-2*np.pi/5*(2*N-1)*delta)**2*np.exp(-np.pi/(2*(2*N-1)*delta))

def analyze_roy():
    sources={name:('dw-roy',case) for name,case in read('dw-roy').get('cases',{}).items()}
    sources.update({name:('dw-convergence',case) for name,case in read('dw-convergence').get('cases',{}).items()
        if name.startswith('roy_s')})
    strips=read('dw-strips').get('cases',{})
    reference=read('roy-reference').get('figure3b_full',[])
    ref={round(r['delta3'],6):r['peak_db'] for r in reference}
    frequency_reference={round(r['delta3'],6):r['peak_cycles'] for r in read('roy-reference').get('figure3a_full',[])}
    results={}
    for shock in [1,2,0]:
        rows=[]
        for name,(source,case) in sources.items():
            if not name.startswith(f'roy_s{shock}_'):continue
            r=case['outputs']['4'];delta=case['config']['delta3']
            field=np.load(Path('~/analytical-nl-discovery-data')/('2026-10-16-gpt-a-'+source)/(name+'_z4.npz'))
            w=field['w'];q=field['q'];q0=field['q0'];t=field['t']
            weight=1+835/(2*np.pi*299.792458*50)*w;positive=weight>0
            photon0=sum(abs(q0[positive])**2/weight[positive])
            resonant=(w>=.75*r['w_roy'])&(w<=1.5*r['w_roy'])
            photon_res=sum(abs(q[resonant])**2/weight[resonant])/photon0
            gated=ifft(fft(q)*(expit(2*(t-20))+expit(-2*(t+20))))
            blue=w>=r['w_z']
            photon_gate=sum(abs(gated[blue])**2/weight[blue])/photon0
            alternative_bands={}
            for low,high in [(.65,1.8),(.85,1.25)]:
                band=(w>=low*r['w_roy'])&(w<=high*r['w_roy'])
                alternative_bands[f'{low}_{high}']=dict(
                    energy=float(sum(abs(q[band])**2)/sum(abs(q0)**2)),
                    photon=float(sum(abs(q[band])**2/weight[band])/photon0))
            rows.append(dict(source_run='2026-10-16-gpt-a-'+source,delta3=delta,peak_db=r['peak_db'],peak_ratio=r['peak_ratio'],
                peak_cycles=r['peak_cycles'],figure_peak_cycles=frequency_reference.get(round(delta,6)),
                eta_gate15=r['eta_gate15'],eta_gate20=r['eta_gate20'],
                eta_band=r['eta_band'],eta_resonant=r['eta_resonant'],
                photon_band=r['eta_band_photon'],eq6_db=10*np.log10(eq6(delta)),
                eta_photon_resonant=float(photon_res),eta_photon_gate20=float(photon_gate),
                alternative_resonant_bands=alternative_bands,
                figure_db=ref.get(round(delta,6)),
                norm_drift=r['formal_norm_relative_drift']))
        rows.sort(key=lambda r:r['delta3'])
        if len(rows)<3:continue
        strip=strips[f'sech2_roy_s{shock}']['strip_min']['blue_-5_-10']
        # Account for algebraic Fourier-tail factors, without looking at TOD yields.
        dstar=strip['d_log']
        calibration=[r for r in rows if r['delta3'] in [.01,.012,.014]]
        if len(calibration)!=3:continue
        fits={}
        for key in ['peak_ratio','eta_gate20','eta_photon_gate20']:
            fits[key]=fit_law([r['delta3'] for r in calibration],[r[key] for r in calibration],dstar)
            fits[key+'_free_d_diagnostic']=fit_law([r['delta3'] for r in calibration],[r[key] for r in calibration])
        for r in rows:
            r['strip_peak_db']=10/math.log(10)*logpredict(fits['peak_ratio'],r['delta3'])
            r['strip_log_yield']=logpredict(fits['eta_gate20'],r['delta3'])
            r['strip_log_photon_yield']=logpredict(fits['eta_photon_gate20'],r['delta3'])
            r['strip_peak_error_db']=r['strip_peak_db']-r['peak_db']
            r['eq6_peak_error_db']=r['eq6_db']-r['peak_db']
            r['strip_yield_log_error']=r['strip_log_yield']-math.log(r['eta_gate20'])
            r['strip_resonant_yield_log_error']=r['strip_log_yield']-math.log(r['eta_resonant'])
            r['strip_photon_yield_log_error']=r['strip_log_photon_yield']-math.log(r['eta_photon_resonant'])
            r['card_gate_clearance_condition']=(4-strip['z'])/(4*r['delta3'])>=25
            r['figure_error_db']=None if r['figure_db'] is None else r['peak_db']-r['figure_db']
            r['figure_frequency_relative_error']=None if r['figure_peak_cycles'] is None else r['peak_cycles']/r['figure_peak_cycles']-1
            r['observable']=r['peak_db']>-80
            r['calibration']=r['delta3'] in [.01,.012,.014]
        groups={}
        for name,selection in {
            'below_visibility_calibration':[r for r in rows if not r['observable'] and r['calibration']],
            'below_visibility_heldout':[r for r in rows if not r['observable'] and not r['calibration']],
            'observable_all':[r for r in rows if r['observable']],
            'observable_delta_le_003':[r for r in rows if r['observable'] and r['delta3']<=.03],
            'delta_002_to_003':[r for r in rows if .02<=r['delta3']<=.03],
            'delta_ge_004':[r for r in rows if r['delta3']>=.04],
            'figure_overlap':[r for r in rows if r['figure_db'] is not None],
        }.items():
            if not selection:continue
            groups[name]=dict(count=len(selection),
                delta3=[r['delta3'] for r in selection],
                strip_peak_rmse_db=float(np.sqrt(np.mean([r['strip_peak_error_db']**2 for r in selection]))),
                eq6_peak_rmse_db=float(np.sqrt(np.mean([r['eq6_peak_error_db']**2 for r in selection]))))
            if name=='figure_overlap':
                groups[name]['simulation_vs_figure_rmse_db']=float(np.sqrt(np.mean([r['figure_error_db']**2 for r in selection])))
                groups[name]['simulation_vs_figure_max_abs_db']=max(abs(r['figure_error_db']) for r in selection)
                groups[name]['simulation_vs_figure_max_frequency_relative_error']=max(abs(r['figure_frequency_relative_error']) for r in selection if r['figure_frequency_relative_error'] is not None)
        small=[r for r in rows if dstar/r['delta3']>=30]
        errors={key:slope_error([r['delta3'] for r in small],[r[key] for r in small],dstar)
            for key in ['peak_ratio','eta_gate20','eta_photon_gate20']}
        estimates=strips[f'sech2_roy_s{shock}']['strip_min']
        if shock==1:
            refined=read('dw-convergence').get('cases',{}).get('roy_strip_grid')
            if refined is not None:estimates=refined['strip_min']
        sensitivity=[]
        for band,estimate in estimates.items():
            if not band.startswith('blue'):continue
            f=fit_law([r['delta3'] for r in calibration],[r['peak_ratio'] for r in calibration],estimate['d_log'])
            chosen=[r for r in rows if r['observable'] and r['delta3']<=.03]
            residual=[10/math.log(10)*logpredict(f,r['delta3'])-r['peak_db'] for r in chosen]
            sensitivity.append(dict(tail_window=band,dstar=estimate['d_log'],peak_fit=f,
                observable_to_003_peak_rmse_db=float(np.sqrt(np.mean(np.asarray(residual)**2)))))
        results[f'shock_{shock}']=dict(dstar=dstar,strip_fit=strip,fits=fits,rows=rows,groups=groups,
            local_error_scaling=errors,independent_tail_window_sensitivity=sensitivity)
    return results

def analyze_core():
    cases=read('dw-law').get('cases',{})
    dstar=.5*math.acos(math.sqrt(3)-1)
    result={}
    for z in ['2','4']:
        rows=[]
        for case in cases.values():
            if z not in case['outputs']:continue
            r=case['outputs'][z]
            rows.append(dict(delta3=case['config']['delta3'],eta=r['eta_gate15'],
                peak_db=r['peak_db'],eta20=r['eta_gate20'],energy_drift=r['energy_relative_drift'],
                hamiltonian_drift=r['hamiltonian_relative_drift'],momentum_drift=r['momentum_drift_per_initial_energy']))
        rows.sort(key=lambda r:r['delta3'])
        construction=[r for r in rows if r['delta3'] in [.008,.009,.01,.011]]
        if len(construction)!=4:continue
        ds=[r['delta3'] for r in construction];ys=[r['eta'] for r in construction]
        fit=fit_law(ds,ys,dstar)
        for r in rows:r['fixed_strip_log_error']=logpredict(fit,r['delta3'])-math.log(r['eta'])
        result['xi_'+z]=dict(exact_dstar=dstar,free_fit=fit_law(ds,ys),fixed_fit=fit,
            local_error_scaling=slope_error(ds,ys,dstar),rows=rows,
            own_heldout=[r for r in rows if r['delta3'] in [.0095,.0105]])
    return result

def analyze_heldout():
    cases=read('dw-heldout').get('cases',{})
    strips=read('dw-heldout-strips').get('cases',{})
    grouped={}
    for name,case in cases.items():
        cfg=case['config'];key=f"{cfg['shape']}{cfg['N']}_{cfg['raman']}_z{cfg['zmax']}"
        r=next(iter(case['outputs'].values()))
        grouped.setdefault(key,[]).append(dict(delta3=cfg['delta3'],eta=r['eta_gate15'],eta20=r['eta_gate20'],peak_db=r['peak_db'],
            frozen_role=cfg.get('frozen_role'),dstar_ratio=cfg.get('dstar_ratio')))
    result={}
    anchors={'sech3_none_z2':.1997,'gauss4_none_z1':.1322,'gauss3_none_z1':.2015,
             'gauss3_none_z2':.1923,'gauss3_M1_z2':.2346}
    for key,rows in grouped.items():
        rows.sort(key=lambda r:r['delta3'])
        if len(rows)<4:continue
        stripkey=key.rsplit('_z',1)[0]
        dstar=anchors.get(key)
        if stripkey in strips:
            # Only restrict z for the separate length check.
            raw=Path('~/analytical-nl-discovery-data/2026-10-16-gpt-a-dw-heldout-strips')/(stripkey+'_strip.json')
            records=json.loads(raw.read_text())
            zmax=float(key.rsplit('_z',1)[1])
            candidates=[(r['fits']['blue_-4_-9']['d'],r['z']) for r in records
                if r['z']<=zmax and r['fits']['blue_-4_-9'] is not None and r['fits']['blue_-4_-9']['rms']<.05 and r['fits']['blue_-4_-9']['d']>0]
            dstar,zstar=min(candidates)
        else:zstar=None
        construction=rows[:4];ds=[r['delta3'] for r in construction];ys=[r['eta'] for r in construction]
        fit=fit_law(ds,ys)
        result[key]=dict(dstar=dstar,zstar=zstar,card_anchor=anchors.get(key),
            free_fit=fit,fixed_fit=fit_law(ds,ys,dstar),
            free_fit_gate20=fit_law(ds,[r['eta20'] for r in construction]),
            exponent_relative_error=fit['d']/dstar-1,
            local_error_scaling=slope_error(ds,ys,dstar),rows=rows)
        training=[r for r in rows if r['frozen_role']=='train']
        if len(training)==2:
            ownfit=fit_law([r['delta3'] for r in training],[r['eta'] for r in training],dstar)
            held=[dict(r,log_prediction_error=logpredict(ownfit,r['delta3'])-math.log(r['eta'])) for r in rows if r['frozen_role']=='test']
            result[key]['frozen_two_point_fit']=ownfit
            result[key]['frozen_heldout_results']=held
    return result

def analyze_null_background():
    from scipy.fft import fft,ifft
    from scipy.special import expit
    out={}
    base=Path('~/analytical-nl-discovery-data/2026-10-16-gpt-a-dw-strips')
    for name in ['sech2_M0','sech2_roy_s1','sech2_roy_s2','sech2_roy_s0']:
        path=base/(name+'_z4.npz')
        if not path.exists():continue
        field=np.load(path);u=fft(field['q']);w=field['w'];t=field['t'];den=sum(abs(field['q0'])**2)
        rows=[]
        for delta in [.004,.005,.006,.007,.008,.009,.01,.012,.014,.02]:
            band=w>=1/(6*delta);row=dict(delta3_band_parameter=delta)
            for radius in [15,20,25]:
                g=expit(2*(t-radius))+expit(-2*(t+radius))
                row[f'eta_null_gate{radius}']=float(sum(abs(ifft(u*g))[band]**2)/den)
            rows.append(row)
        out[name]=dict(note='TOD-free final field; delta3 labels only the measuring band. Deep values may be limited by Float64 noise.',rows=rows)
    return out

def analyze_length():
    cases=read('dw-length').get('cases',{})
    dstar=.5*math.acos(math.sqrt(3)-1)
    result={}
    short=read('dw-law').get('cases',{})
    construction_short=[short.get(f'sech2_d{d:g}') for d in [.008,.009,.01,.011]]
    short_fit=None if any(c is None for c in construction_short) else fit_law(
        [.008,.009,.01,.011],[c['outputs']['4']['eta_gate15'] for c in construction_short],dstar)
    for z in ['8','12']:
        rows=[]
        for name,case in cases.items():
            if 'window' in name or z not in case['outputs']:continue
            r=case['outputs'][z];delta=case['config']['delta3']
            anchor=short.get(f'sech2_d{delta:g}',{}).get('outputs',{}).get('4')
            rows.append(dict(delta3=delta,eta=r['eta_gate15'],eta20=r['eta_gate20'],
                peak_db=r['peak_db'],energy_drift=r['energy_relative_drift'],
                time_edge_fraction=r['time_edge_fraction'],spectral_edge_fraction=r['spectral_edge_fraction'],
                ratio_to_xi4=None if anchor is None else r['eta_gate15']/anchor['eta_gate15'],
                log_error_using_xi4_constants=None if short_fit is None else logpredict(short_fit,delta)-math.log(r['eta_gate15'])))
        rows.sort(key=lambda r:r['delta3'])
        construction=[r for r in rows if r['delta3'] in [.008,.009,.01,.011]]
        if len(construction)!=4:continue
        ds=[r['delta3'] for r in construction];ys=[r['eta'] for r in construction]
        fit=fit_law(ds,ys,dstar)
        result['xi_'+z]=dict(dstar=dstar,free_fit=fit_law(ds,ys),fixed_fit=fit,
            local_error_scaling=slope_error(ds,ys,dstar),rows=rows)
    variants=[]
    for name,case in cases.items():
        if 'window' not in name:continue
        baseline=next((c for n,c in cases.items() if 'window' not in n and c['config']['delta3']==case['config']['delta3']),None)
        if baseline is None:continue
        for z,r in case['outputs'].items():
            b=baseline['outputs'][z]
            variants.append(dict(case=name,xi=float(z),relative_gate15=r['eta_gate15']/b['eta_gate15']-1,
                peak_difference_db=r['peak_db']-b['peak_db'],time_edge_fraction=r['time_edge_fraction']))
    result['window_checks']=variants
    return result

def analyze_guardrails():
    records=[]
    for slug in ['dw-law','dw-roy','dw-heldout','dw-length','dw-convergence','dw-followup']:
        for name,case in read(slug).get('cases',{}).items():
            for z,m in case['outputs'].items():
                if 'eta_gate15' not in m:continue
                records.append(dict(run=slug,case=name,z=z,
                    delta3=case['config']['delta3'],N=case['config']['N'],
                    raman=case['config'].get('raman','none'),shock=case['config'].get('shock',0),
                    eta_gate15=m['eta_gate15'],eta_gate20=m['eta_gate20'],
                    gate20_vs15=m['eta_gate20']/m['eta_gate15']-1,
                    gate25_vs20=m['eta_gate25']/m['eta_gate20']-1,
                    gate_resonant_vs_broad=m['eta_resonant_gate20']/m['eta_gate20']-1,
                    energy_drift=m['energy_relative_drift'],formal_norm_drift=m['formal_norm_relative_drift'],
                    physical_photon_drift=m['physical_norm_relative_drift'],
                    physical_negative_frequency_energy=m['physical_negative_frequency_energy'],
                    momentum_drift=m['momentum_drift_per_initial_energy'],
                    hamiltonian_drift=m['hamiltonian_relative_drift'],
                    time_edge_fraction=m['time_edge_fraction'],spectral_edge_fraction=m['spectral_edge_fraction']))
    return records

def analyze_collapse():
    cases=read('dw-convergence').get('cases',{})
    strip=cases.get('collapse_gauss5_strip')
    strip_source='dw-convergence:collapse_gauss5_strip'
    follow=read('dw-followup').get('cases',{})
    refined=follow.get('collapse_gauss5_strip_halfstep')
    if refined is not None:
        strip=refined;strip_source='dw-followup:collapse_gauss5_strip_halfstep'
    dstar=None if strip is None else strip['strip_min']['blue_-4_-9']['d']
    rows=[]
    for name,c in cases.items():
        if not name.startswith('collapse_') or c['config']['delta3']==0:continue
        cfg=c['config'];r=c['outputs']['2'];prediction=cfg['frozen_band_yield']
        actual_d=dstar if cfg['N']==5 else .19231891317462974
        rows.append(dict(case=name,N=cfg['N'],delta3=cfg['delta3'],design_x=cfg['design_x'],
            actual_x=None if actual_d is None else actual_d/cfg['delta3'],dstar=actual_d,
            eta_band=r['eta_band'],eta_gate15=r['eta_gate15'],frozen_prediction=prediction,
            log_error=math.log(r['eta_band']/prediction),frozen_log_tolerance=cfg['frozen_log_tolerance'],
            energy_drift=r['energy_relative_drift'],hamiltonian_drift=r['hamiltonian_relative_drift'],
            time_edge_fraction=r['time_edge_fraction'],spectral_edge_fraction=r['spectral_edge_fraction']))
    variants={name:c['strip_min'] for name,c in {**cases,**follow}.items()
        if name.startswith('collapse_gauss5_strip')}
    return dict(dstar_N5=dstar,dstar_source=strip_source,strip_variants=variants,rows=rows)

def analyze_integrator_order():
    rows=[]
    for name,c in read('dw-core').get('cases',{}).items():
        if not name.startswith('breather_'):continue
        m=next(iter(c['outputs'].values()))
        rows.append(dict(case=name,h=c['actual_h'],relative_l2_error=m['breather_relative_l2_error']))
    rows.sort(key=lambda r:r['h'],reverse=True)
    powers=[math.log(a['relative_l2_error']/b['relative_l2_error'])/math.log(a['h']/b['h'])
        for a,b in zip(rows[:-1],rows[1:])]
    return dict(source_run='2026-10-16-gpt-a-dw-core',rows=rows,measured_orders=powers,predicted_order=4)

def analyze_frozen_p5():
    cases=read('dw-followup').get('cases',{})
    rows=[]
    for name,c in cases.items():
        if not name.startswith('frozenP5_'):continue
        m=c['outputs']['1']
        rows.append(dict(delta3=c['config']['delta3'],eta=m['eta_gate15']))
    rows.sort(key=lambda r:r['delta3'])
    if len(rows)!=4:return dict(rows=rows,status='pending')
    f=fit_law([r['delta3'] for r in rows],[r['eta'] for r in rows])
    # Independently measured first-compression strip, not fitted to these yields.
    dstar=.20150577816995457
    other=analyze_heldout()['gauss3_none_z2']['free_fit']['d']
    return dict(rows=rows,free_fit=f,dstar=dstar,card_anchor=.2015,
        relative_error=f['d']/dstar-1,relative_to_length2=f['d']/other-1,
        local_error_scaling=slope_error([r['delta3'] for r in rows],[r['eta'] for r in rows],dstar),
        status='complete')

def compare_permitted_summary():
    path=RUNS/'2026-10-16-claude-b-dw-oracle/summary.json'
    reference=json.loads(path.read_text())
    cases=read('dw-heldout').get('cases',{})
    rows=[]
    for key in ['rk4ip_heldout_gauss4','rk4ip_heldout_sech3']:
        for r in reference[key]:
            name=f"{r['kind']}{int(r['N'])}_none_z{1 if r['kind']=='gauss' else 2}_d{r['d3']}"
            if name not in cases:continue
            value=next(iter(cases[name]['outputs'].values()))['eta_gate15']
            rows.append(dict(case=name,own_eta=value,proposer_rk4ip_eta=r['eta_DW_rk4ip'],
                relative_difference=value/r['eta_DW_rk4ip']-1))
    return dict(source_run='2026-10-16-claude-b-dw-oracle',source_file='summary.json',
        access='Only permitted summary data, after independent results; no proposer implementation read.',rows=rows)

def analyze_relaxed_assumptions():
    series={key:{} for key in ['M0','Raman_only','Roy_paper','Roy_double_shock']}
    for name,c in read('dw-law').get('cases',{}).items():
        series['M0'][c['config']['delta3']]=c['outputs']['4']
    for name,c in read('dw-roy').get('cases',{}).items():
        if not name.startswith('roy_s'):continue
        key={0:'Raman_only',1:'Roy_paper',2:'Roy_double_shock'}[c['config']['shock']]
        series[key][c['config']['delta3']]=c['outputs']['4']
    rows=[]
    for delta in sorted(set().union(*(set(s) for s in series.values()))):
        values={key:dict(peak_db=s[delta]['peak_db'],eta_gate20=s[delta]['eta_gate20'],
            energy_drift=s[delta]['energy_relative_drift'],physical_photon_drift=s[delta]['physical_norm_relative_drift'])
            for key,s in series.items() if delta in s}
        row=dict(delta3=delta,models=values)
        if 'M0' in values and 'Raman_only' in values:
            row['raman_peak_change_db']=values['Raman_only']['peak_db']-values['M0']['peak_db']
        if 'Raman_only' in values and 'Roy_paper' in values:
            row['paper_shock_peak_change_db']=values['Roy_paper']['peak_db']-values['Raman_only']['peak_db']
        rows.append(row)
    return dict(sources=['2026-10-16-gpt-a-dw-law','2026-10-16-gpt-a-dw-roy'],rows=rows)

def main():
    destination=RUNS/'2026-10-16-gpt-a-dw-analysis';destination.mkdir(exist_ok=True)
    results=dict(**IDENTITY,run_id=destination.name,core=analyze_core(),roy=analyze_roy(),heldout=analyze_heldout(),
                 null_background=analyze_null_background(),length=analyze_length(),guardrails=analyze_guardrails(),
                 collapse=analyze_collapse(),integrator_order=analyze_integrator_order(),
                 frozen_p5=analyze_frozen_p5(),permitted_summary_comparison=compare_permitted_summary(),
                 relaxed_assumptions=analyze_relaxed_assumptions())
    (destination/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
    (destination/'config.yaml').write_text(yaml.safe_dump(dict(**IDENTITY,
        sources=['dw-core','dw-law','dw-roy','dw-strips','dw-heldout','dw-heldout-strips','roy-reference','dw-length','dw-convergence','dw-followup'],
        comparison_source='2026-10-16-claude-b-dw-oracle/summary.json; only permitted summary values, inspected after independent results',
        roy_calibration_delta3=[.01,.012,.014],roy_strip_method='blue log-tail regression with linear and log-frequency terms, amplitudes 1e-5 to 1e-10',
        core_calibration_delta3=[.008,.009,.01,.011],own_heldout_delta3=[.0095,.0105]),sort_keys=False))
    (destination/'meta.yaml').write_text(yaml.safe_dump(dict(**IDENTITY,run_id=destination.name,
        solver_commit='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',solver_dirty=False,
        claim='C-20261016-claude-b-01',raw_location='source runs; derived summary only',
        implementation='independent regression; d fixed before evaluating Roy yields'),sort_keys=False))
    for k,v in results['roy'].items():
        print(k,'d=',v['dstar'],'peak fit=',v['fits']['peak_ratio'],'groups=',v['groups'])
    for k,v in results['core'].items():print(k,'fit=',v['free_fit'],'error scaling=',v['local_error_scaling'])
    for k,v in results['heldout'].items():print(k,'d=',v['dstar'],'fit=',v['free_fit'])


if __name__=='__main__':main()
