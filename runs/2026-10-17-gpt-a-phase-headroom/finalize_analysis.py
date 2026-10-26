#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Assemble auditable paired comparisons and the PI's single-panel plot."""
from independent import *
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-a-phase-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from summarize import build

def main():
    summary=build();cases=summary['cases']
    readouts=json.loads((HERE/'readout_checks.json').read_text())['cases']
    selection=json.loads((HERE/'selected_masks.json').read_text())
    training=json.loads((HERE/'training_selection.json').read_text())
    peaks=json.loads((HERE/'tl_duration_peaks.json').read_text())['peaks']
    def fraction(label):
        result=readouts.get(label,{})
        rows=result.get('gate_checks',{}).get('1.0',{}).get('rows',[cases[label]])
        if not all(r.get('root_ok') and r.get('eta',0)>0 and r.get('evans_residual',1)<1e-8 for r in rows):
            raise ValueError('Unresolved nominal-gate ZS root; do not report a fraction: '+label)
        return result.get('f_zs_extrapolated',cases[label]['f_zs'])
    def paired(mask,tl):
        a,b=cases[mask],cases[tl];fa,fb=fraction(mask),fraction(tl)
        return dict(masked=mask,baseline=tl,f_mask=fa,f_TL=fb,H_zs=fa/fb,
                    f_gate_mask=a['f_gate'],f_gate_TL=b['f_gate'],H_gate=a['f_gate']/b['f_gate'],
                    input_energy_nJ=a['input_energy_nJ'],zs_energy_mask_nJ=fa*a['input_energy_nJ'],
                    zs_energy_TL_nJ=fb*b['input_energy_nJ'],gate_energy_mask_nJ=a['gated_energy_nJ'],
                    gate_energy_TL_nJ=b['gated_energy_nJ'],redshift_mask_THz=a['red_THz'],
                    redshift_TL_THz=b['red_THz'],shift_ratio=a['red_THz']/b['red_THz'],
                    gate_share_of_output_mask=a['f_gate']*a['input_mass']/a['output_mass'],
                    gate_share_of_output_TL=b['f_gate']*b['input_mass']/b['output_mass'],
                    original_root_failure_mask=not a.get('root_ok',False),original_root_failure_TL=not b.get('root_ok',False),
                    photon_gate_ratio=a['photon_fraction_gate']/b['photon_fraction_gate'])
    pairs={}
    for T,m in [(100,'A2'),(100,'A'),(200,'B')]:
        pairs[f'core_{T}_{m}']=paired(f'core_{T}_{m}',f'core_{T}_TL')
        errors=[]
        for label in [f'core_{T}_{m}',f'core_{T}_TL']:
            rr=readouts[label]
            errors.append(max(rr['gate_systematic_range'],rr['shooting_remaining_estimate'],1e-5))
        pair=pairs[f'core_{T}_{m}']
        pair['numerical_uncertainty_mask'],pair['numerical_uncertainty_TL']=errors
        pair['H_numerical_uncertainty']=errors[0]/pair['f_TL']+pair['f_mask']*errors[1]/pair['f_TL']**2
    for T,m in [(100,'A2'),(200,'B')]:
        pairs[f'cutoff_smooth_{T}_{m}']=paired(f'cutoff_smooth_{T}_{m}',f'core_{T}_TL')
    for label,d in cases.items():
        if d['mask']=='TL':continue
        base=label.rsplit('_',1)[0]+'_TL'
        if label not in pairs and base in cases and cases[base]['mask']=='TL':pairs[label]=paired(label,base)
    for key in list(pairs):
        if key.endswith('_fine_mask'):
            original=key.replace('_fine_mask','_mask')
            if original in pairs:pairs[original]=dict(pairs[key],coarse_comparison=pairs[original])
    points=[]
    for key,item in selection['masks'].items():
        N=item['N'];prefix=f'qualified_N{N}';label=prefix+'_main';baseline=f'train_TL_N{N}'
        pair=paired(label,baseline)
        tol=[abs(fraction(prefix+'_'+test)-fraction(label)) for test in ['grid','window']]
        diagnostic_labels=[x for x in readouts if x.startswith(f'diagnostic_N{N}_window')]
        for other in diagnostic_labels:
            if other.endswith('_clipped'):tol.append(abs(fraction(other)-fraction(label)))
        tol.append(abs(cases[prefix+'_step025']['f_zs']-cases[label]['f_zs']))
        checks=readouts[label]
        uncertainty=max(tol+[checks['gate_systematic_range'],checks['shooting_remaining_estimate'],1e-5])
        baseline_checks=readouts[baseline]
        baseline_uncertainty=max(baseline_checks['gate_systematic_range'],baseline_checks['shooting_remaining_estimate'],1e-5)
        starts=[r for r in training['candidates'] if r['N']==N and '_polish' not in r['optimizer']]
        fields=[np.load(RAW/(prefix+'_'+part+'.npz'))['u'] for part in ['step2','step1','main','step025']]
        field_differences=[float(np.linalg.norm(a-b)/np.linalg.norm(b)) for a,b in zip(fields[:-1],fields[1:])]
        field_orders=[float(np.log2(field_differences[j]/field_differences[j+1])) for j in range(2)]
        grid_field=np.load(RAW/(prefix+'_grid.npz'))['u'][::2]
        wide=np.load(RAW/(prefix+'_window.npz'))['u'];offset=(len(wide)-len(fields[1]))//2
        grid_field_difference=float(np.linalg.norm(grid_field-fields[1])/np.linalg.norm(fields[1]))
        window_field_difference=float(np.linalg.norm(wide[offset:offset+len(fields[1])]-fields[1])/np.linalg.norm(fields[1]))
        point=dict(N=N,T0_fs=item['T0_fs'],**pair,numerical_uncertainty=uncertainty,
                   H_numerical_uncertainty=uncertainty/pair['f_TL']+pair['f_mask']*baseline_uncertainty/pair['f_TL']**2,
                   TL_peak=peaks[key]['best']['f_zs_extrapolated'],TL_peak_T0_fs=peaks[key]['best']['T0_fs'],
                   H_above_TL_duration_peak=pair['f_mask']/peaks[key]['best']['f_zs_extrapolated'],
                   step_field_differences=field_differences,step_field_orders=field_orders,
                   grid_field_difference=grid_field_difference,window_central_field_difference=window_field_difference,
                   step_f_zs_changes=[cases[prefix+'_'+part]['f_zs']-cases[label]['f_zs'] for part in ['step2','step1','step025']],
                   C2_phase_H_zs_native=cases[prefix+'_smooth']['f_zs']/cases[baseline]['f_zs'],
                   C2_phase_H_zs=fraction(prefix+'_smooth')/fraction(baseline),
                   C2_phase_H_gate=cases[prefix+'_smooth']['f_gate']/cases[baseline]['f_gate'],
                   postrun_window_diagnostics={x:dict(f_zs=fraction(x),difference_from_original=fraction(x)-fraction(label),
                       f_gate=cases[x]['f_gate'],redshift_THz=cases[x]['red_THz'],
                       fraction_tolerance_passed=abs(fraction(x)-fraction(label))<.002) for x in diagnostic_labels},
                   length6_change=fraction(prefix+'_length6')-fraction(label),
                   length6_pair=paired(prefix+'_length6',prefix+'_length6_TL'),
                   start_values=[r['f_zs_extrapolated'] for r in starts],
                   start_labels=[r['optimizer'] for r in starts],selected_mask=item)
        points.append(point);pairs[label]=pair
    held=pairs['heldout_N6_transfer_mask']
    tests=[]
    def check(name,value,relation,threshold):
        passed={'<':value<threshold,'>':value>threshold,'>=':value>=threshold}[relation]
        tests.append(dict(name=name,value=float(value),relation=relation,threshold=threshold,passed=bool(passed)))
    for T,m,minimum in [(100,'A2',1.085),(100,'A',1.055),(200,'B',1.065)]:
        label=f'core_{T}_{m}'
        check('V1 '+label,pairs[label]['H_zs'],'>=',minimum)
        check('V2 gate agreement '+label,abs(cases[label]['f_gate']-fraction(label)),'<',.01)
        check('V2 gate sensitivity '+label,readouts[label]['gate_systematic_range'],'<',.003)
    for T,m in [(100,'A2'),(200,'B')]:
        check('V2 saturation '+m,abs(fraction(f'length6_{T}_{m}')-fraction(f'core_{T}_{m}')),'<',.005)
        check('C2 published phase extension '+m,abs(cases[f'cutoff_smooth_{T}_{m}']['f_zs']-cases[f'core_{T}_{m}']['f_zs']),'<',.002)
        for r in [.9,1.1]:
            label=f'detuneE_{int(T*r)}_{m}'
            check('V4 '+label,pairs[label]['H_zs'],'>=',1.02)
        for model in ['shock','tod','loss']:
            label=f'{model}_{T}_{m}'
            check('V5 '+label,pairs[label]['H_gate'],'>',1.)
    for T,m in [(100,'TL'),(100,'A2'),(200,'TL'),(200,'B')]:
        base=f'core_{T}_{m}'
        for attack in ['grid','window','step0.5','step0.25']:
            check('V3 '+attack+' '+base,abs(cases[f'{attack}_{T}_{m}']['f_zs']-cases[base]['f_zs']),'<',.002)
        orders=summary['convergence'][f'{T}_{m}']['orders']
        check('V3 field order lower '+base,min(orders),'>=',3.3)
        check('V3 field order upper '+base,max(orders),'<',4.7)
    check('V4 closest margin at finer resolution',pairs['detune90_fine_A2']['H_zs'],'>=',1.02)
    for point in points:
        N=point['N'];prefix=f'qualified_N{N}'
        check('New-mask saturation '+str(N),abs(point['length6_change']),'<',.005)
        check('New-mask longer-length headroom '+str(N),point['length6_pair']['H_zs'],'>=',1.01)
        check('New-mask gate agreement '+str(N),abs(point['f_gate_mask']-point['f_mask']),'<',.01)
        check('New-mask gate sensitivity '+str(N),readouts[prefix+'_main']['gate_systematic_range'],'<',.003)
        check('New-mask step stability '+str(N),max(abs(x) for x in point['step_f_zs_changes']),'<',.002)
        check('New-mask step order lower '+str(N),min(point['step_field_orders']),'>=',3.3)
        check('New-mask step order upper '+str(N),max(point['step_field_orders']),'<',4.7)
        for attack in ['grid','window']:
            check('New-mask '+attack+' stability '+str(N),abs(fraction(prefix+'_'+attack)-point['f_mask']),'<',.002)
        check('C2 phase extension '+str(N),abs(cases[prefix+'_smooth']['f_zs']-cases[prefix+'_main']['f_zs']),'<',.002)
        for r in [95,105]:
            check(f'New-mask held-out duration N={N}, {r}%',pairs[prefix+f'_hold{r}_mask']['H_zs'],'>=',1.01)
        for model in ['shock','tod','loss']:
            check(f'New-mask material N={N}, {model}',pairs[prefix+'_'+model+'_mask']['H_gate'],'>',1.)
        check('New-mask at TL duration peak '+str(N),pairs[prefix+'_TLpeak_mask']['H_gate'],'>',1.)
    check('Held-out N=6 transfer',held['H_zs'],'>=',1.05)
    check('Phase-only input energy',max(abs(d['phase_only_input_error']) for d in cases.values()),'<',1e-12)
    ideal=[d for d in cases.values() if not d['shock'] and not d.get('gamma_curve') and not d['loss_dB_km']]
    check('Ideal-model mass drift',max(abs(d['mass_drift']) for d in ideal),'<',2e-4)
    check('Output time-edge energy',max(d['edge_mass'] for d in cases.values()),'<',1e-6)
    check('Output spectral-edge energy',max(d['alias_mass'] for d in cases.values()),'<',1e-6)
    raman=[d for label,d in cases.items() if label!='integrable_N1' and d.get('fR',.18)>0]
    check('Raman time resolution (fs)',max(d['dt_fs'] for d in raman),'<',3.000001)
    census_labels=[label for label in readouts if 'census' in readouts[label]]
    for label in census_labels:
        check('Tallest is reddest resolved soliton '+label,int(readouts[label].get('reddest_resolved_soliton_is_tallest') is True),'>=',1)
    for label,item in readouts.items():
        if 'all_ZS_roots_resolved' in item:
            check('Gate/refinement ZS roots resolved '+label,int(item['all_ZS_roots_resolved']),'>=',1)
    stationarity=json.loads((HERE/'stationarity.json').read_text())
    for row in stationarity['checks']:
        check(f"Stationarity N={row['N']} nt={row['nt']}",row['gradient_norm'],'<',1e-5)
        if 'directional_check' in row:
            d=row['directional_check']
            check(f"Final directional derivative N={row['N']}",d['absolute_error'],'<',d['tolerance'])
    shock_cases=[d for d in cases.values() if d['shock'] and not d.get('gamma_curve')]
    photon_error=max(abs(1+d['physical_photon_drift']-np.exp(-d['loss_dB_km']*np.log(10)/10*d['length_m']/1000)) for d in shock_cases)
    result=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=HERE.name,
                pairs=pairs,optimized_points=points,heldout_N6=held,frozen_test_results=tests,stationarity=stationarity,
                shock_model_max_photon_invariant_error=photon_error,
                uncertainty_note='Maximum absolute grid/window/gate/readout discrepancy, with floor 1e-5; not a confidence interval.',
                interpretation='Achievable lower bounds and finite-basis stationary points where gradient checks pass; no global upper certificate.')
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    plt.rcParams.update({'font.size':11,'axes.labelsize':12,'legend.fontsize':9.5,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(6.5,4.7));N=np.linspace(2.85,6.15,300)
    ax.plot(N,1.29/np.sqrt(N),color='#6a7484',lw=1.7,label=r'TL reference $1.29/\sqrt{N}$')
    xx=[r['N'] for r in points];yy=[r['f_mask'] for r in points]
    ax.plot(xx,[r['f_TL'] for r in points],'s',color='#273f5b',ms=6,label='TL at matched N and duration')
    ax.errorbar(xx,yy,yerr=[r['numerical_uncertainty'] for r in points],fmt='o',color='#bc3f32',ms=7,capsize=4,label='Selected phase masks')
    for j,r in enumerate(points):
        if r['start_values']:
            ax.vlines(r['N'],min(r['start_values']),max(r['start_values']),color='#bc3f32',alpha=.35,lw=5,zorder=1,label='Finite-effort start range' if j==0 else None)
        ax.annotate(f"{r['T0_fs']:g} fs",(r['N'],r['f_mask']),xytext=(5,7),textcoords='offset points',fontsize=9,color='#963c34')
    # Published lower bounds at the corresponding N=4,5 training durations.
    claims=[(4,1.082),(5,1.056)]
    for j,(n,h) in enumerate(claims):
        r=next(v for v in points if v['N']==n)
        ax.plot(n,h*r['f_TL'],marker='_',ms=18,mew=2.4,color='#af8400',ls='',label='Original claimed lower bounds' if j==0 else None)
    four=next(r for r in points if r['N']==4);ceiling=1.05*four['f_TL']
    ax.plot([3.88,4.12],[ceiling,ceiling],ls=':',lw=1.6,color='#333333')
    ax.annotate('5% ceiling',(4.12,ceiling),xytext=(4,0),va='center',textcoords='offset points',fontsize=8.5,color='#333333')
    ax.plot(6,held['f_mask'],'o',mfc='white',mec='#bc3f32',mew=1.8,ms=8,label='Held-out N=6 mask transfer')
    ax.plot(6,held['f_TL'],'s',mfc='white',mec='#273f5b',mew=1.5,ms=6)
    ax.annotate('380 fs',(6,held['f_mask']),xytext=(-8,9),ha='right',textcoords='offset points',fontsize=9,color='#963c34')
    ax.set(xlabel='Soliton order N (dimensionless)',ylabel='Leading-soliton energy / laser energy',xlim=(2.8,6.2),xticks=[3,4,5,6])
    ax.grid(axis='y',alpha=.18);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.22),ncol=2,frameon=False,fontsize=9,columnspacing=1.)
    fig.tight_layout();fig.subplots_adjust(bottom=.34)
    fig.savefig(HERE/'fig_summary.png',dpi=150,metadata={'Author':'gpt-a; gpt-6-astra; gpt','Run':HERE.name});plt.close(fig)
    print(json.dumps({'optimized_points':points,'heldout_N6':held},indent=2))

if __name__=='__main__':main()
