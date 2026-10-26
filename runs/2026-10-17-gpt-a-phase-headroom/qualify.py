#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
from independent import *
import subprocess,sys
from scipy.optimize import minimize_scalar

def safe_case(label,**kw):
    path=RAW/(label+'.json')
    if path.exists():return json.loads(path.read_text())
    pressure=subprocess.check_output(['memory_pressure'],text=True)
    pct=int(pressure.split('free percentage:')[1].split('%')[0])
    if pct<35:raise RuntimeError('Memory launch deferred')
    return run_case(label,**kw)

def refine_record(label):
    data=np.load(RAW/(label+'.npz'));d=json.loads((RAW/(label+'.json')).read_text())
    a=measure(data['t'],data['u'],d,refine=2);b=measure(data['t'],data['u'],d,refine=4)
    d['f_zs_extrapolated']=(4*b['f_zs']-a['f_zs'])/3
    d['shooting_remaining_estimate']=abs(d['f_zs_extrapolated']-b['f_zs'])
    return d

def safe_pair(prefix,mask,minimum,metric='f_zs',**args):
    rows={name:safe_case(prefix+'_'+name,mask=m,**args) for name,m in [('mask',mask),('TL','TL')]}
    ratio=rows['mask'][metric]/rows['TL'][metric]
    invariant_or_alias=any(r['alias_mass']>1e-6 or
                          (not r['shock'] and not r.get('gamma_curve') and not r['loss_dB_km'] and abs(r['mass_drift'])>2e-4)
                          for r in rows.values())
    edge_failure=any(r['edge_mass']>1e-6 for r in rows.values())
    if (minimum is not None and abs(ratio-minimum)<.002) or invariant_or_alias or edge_failure:
        fine=dict(args,nt=min(32768,2*args.get('nt',16384)),hfac=args.get('hfac',1.)/2)
        if edge_failure:
            fine['width']=2*args.get('width',160.)
            if fine['width']/fine['nt']*args['T0']>3:
                raise RuntimeError('Window refinement requires a separately recorded convergence-grid exception')
        for name,m in [('mask',mask),('TL','TL')]:safe_case(prefix+'_fine_'+name,mask=m,**fine)
        print('REFINED PAIR',prefix,ratio,minimum,'invariant_or_alias',invariant_or_alias,'edge',edge_failure,flush=True)
    return rows

def training():
    rows=[]
    for path in sorted(RAW.glob('pyopt_*_summary.json')):
        opt=json.loads(path.read_text());tag=path.stem.replace('_summary','');mask=RAW/(tag+'_bestcoef.csv')
        if opt.get('failed'):continue
        label='train_'+tag
        safe_case(label,N=opt['N'],T0=opt['T0_fs'],mask=str(mask),nt=16384,width=160,hfac=1.)
        d=refine_record(label)
        history=[json.loads(line) for line in (RAW/(tag+'_history.jsonl')).read_text().splitlines() if line.strip()]
        best_record=max(history,key=lambda row:row['f_zs'])
        d.update(optimizer=tag,optimizer_final_gradient_norm=opt['gradient_norm'],
                 optimizer_best_gradient_norm=best_record['gradient_norm'],mask_source=str(mask))
        rows.append(d)
    best={}
    for N,T in [(3,140),(4,200),(5,280)]:
        label=f'train_TL_N{N}'
        safe_case(label,N=N,T0=T,mask='TL',nt=16384,width=160,hfac=1.)
        baseline=refine_record(label)
        candidates=[r for r in rows if r['N']==N and r['edge_mass']<1e-6 and r['alias_mass']<1e-6
                    and abs(r['mass_drift'])<2e-4 and r.get('root_ok')]
        if candidates:
            stationary=[r for r in candidates if r['optimizer_best_gradient_norm']<=1e-5]
            chosen=max(stationary or candidates,key=lambda x:x['f_zs_extrapolated'])
            best[str(N)]={'N':N,'T0_fs':T,'mask':chosen['mask_source'],'optimizer':chosen['optimizer'],
                          'stationarity_preference_satisfied':bool(stationary),
                          'largest_training_f_including_unconverged':max(r['f_zs_extrapolated'] for r in candidates),
                          'training_f_zs':chosen['f_zs_extrapolated'],'training_H':chosen['f_zs_extrapolated']/baseline['f_zs_extrapolated'],
                          'baseline':baseline,'training':chosen}
    result={'agent':'gpt-a','model':'gpt-6-astra','family':'gpt','run_id':HERE.name,'candidates':rows,'best':best,
            'selection_uses':'training-point independent repropagation only; prefer candidates meeting raw gradient <=1e-5, and report any larger unconverged candidate separately; no held-out output'}
    (HERE/'training_selection.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SELECTED',[(N,x['optimizer'],x['training_H']) for N,x in best.items()],flush=True)

def tl_peak():
    results={}
    for N,lo,hi in [(3,112,140),(4,180,220),(5,252,308)]:
        evaluated=[]
        def fun(T):
            label=f'tlpeak_N{N}_T{T:.6f}'
            d=safe_case(label,N=N,T0=T,nt=16384,width=160,hfac=1.)
            d=refine_record(label);evaluated.append(d);return -d['f_zs_extrapolated']
        res=minimize_scalar(fun,bounds=(lo,hi),method='bounded',options={'xatol':.2,'maxiter':18})
        best=max(evaluated,key=lambda r:r['f_zs_extrapolated'])
        results[str(N)]={'best':best,'bracket_fs':[lo,hi],'success':bool(res.success),'evaluations':evaluated}
        (HERE/'tl_duration_peaks.json').write_text(json.dumps({'agent':'gpt-a','model':'gpt-6-astra','family':'gpt','run_id':HERE.name,'peaks':results},indent=2)+'\n')
        print('TL PEAK',N,best['T0_fs'],best['f_zs_extrapolated'],flush=True)

def final():
    selected=json.loads((HERE/'selected_masks.json').read_text())
    peaks=json.loads((HERE/'tl_duration_peaks.json').read_text())['peaks']
    for key,item in selected['masks'].items():
        N=item['N'];T=item['T0_fs'];mask=str(HERE/item['coefficient_file']);prefix=f'qualified_N{N}'
        for label,kw in [('main',{}),('step2',dict(hfac=2)),('step1',dict(hfac=1)),('step025',dict(hfac=.25)),
                         ('smooth',dict(smooth_mask=True,hfac=1)),('grid',dict(nt=32768,hfac=1)),('window',dict(nt=32768,width=320,hfac=1)),
                         ('length6',dict(nt=32768,width=320,zfactor=6,hfac=1))]:
            args=dict(N=N,T0=T,mask=mask,nt=16384,width=160,hfac=.5);args.update(kw)
            safe_case(prefix+'_'+label,**args)
        safe_case(prefix+'_length6_TL',N=N,T0=T,mask='TL',nt=32768,width=320,zfactor=6,hfac=1.)
        peak_T=peaks[key]['best']['T0_fs']
        safe_pair(prefix+'_TLpeak',mask,1.,metric='f_gate',N=N,T0=peak_T,Tref=T,nt=16384,width=160,hfac=1.)
        for r in [.95,1.05]:
            safe_pair(prefix+f'_hold{int(100*r)}',mask,1.01,N=N,T0=T*r,Tref=T,nt=16384,width=160,hfac=1.)
        for kind,kw in [('shock',dict(shock=True)),('tod',dict(d3=.12/(6*21.7*T*.001))),
                        ('loss',dict(loss=.2)),('published',dict(published=True,shock=True,loss=.2))]:
            safe_pair(prefix+'_'+kind,mask,1.,metric='f_gate',N=N,T0=T,nt=16384,width=160,hfac=1.,**kw)
        for r in [.9,1.1]:
            safe_pair(prefix+f'_detuneE{int(100*r)}',mask,1.,metric='f_gate',N=N*np.sqrt(r),T0=T*r,Tref=T,
                      zfactor=4*r**(-1.5),nt=32768 if T*r>307 else 16384,width=160,hfac=1.)
    # Cross-N transfer is held out from all mask selection and optimization.
    five=selected['masks']['5'];transfer_mask=str(HERE/five['coefficient_file'])
    safe_pair('heldout_N6_transfer',transfer_mask,1.05,N=6,T0=380,nt=32768,width=160,hfac=.5)
    # Resolve the closest pre-registered published-mask held-out margin and
    # qualify the material model at finer step and grid as well.
    for mask in ['TL','A2']:
        safe_case('detune90_fine_'+mask,N=4*np.sqrt(.9),T0=90,mask=mask,Tref=100,
                  zfactor=4*.9**(-1.5),nt=32768,hfac=.5)
    for T,mask in [(100,'A2'),(200,'B')]:
        safe_case(f'cutoff_smooth_{T}_{mask}',N=4,T0=T,mask=mask,nt=16384,hfac=.5,smooth_mask=True)
        for m in ['TL',mask]:
            safe_case(f'published_fine_{T}_{m}',N=4,T0=T,mask=m,nt=32768,hfac=.5,published=True,shock=True,loss=.2)

if __name__=='__main__':
    {'training':training,'tl_peak':tl_peak,'final':final}[sys.argv[1]]()
