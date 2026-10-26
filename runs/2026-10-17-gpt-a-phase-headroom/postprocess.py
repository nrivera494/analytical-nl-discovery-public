#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
from independent import *

def load_case(label):
    z=np.load(RAW/(label+'.npz'))
    d={k:z[k].item() for k in z.files if k not in ('t','u','k')}
    return z['t'],z['u'],d

def readout_checks(label,census=True,refine_checks=True):
    t,u,d=load_case(label);results={};out={'label':label}
    if refine_checks:
        for g in [.75,1.,1.25]:
            rows=[measure(t,u,d,gate_scale=g,refine=r) for r in [2,4,8]]
            # Exact midpoint transfer has second-order global error.
            extrap=(4*rows[2]['f_zs']-rows[1]['f_zs'])/3
            order=np.log2(abs((rows[0]['f_zs']-rows[1]['f_zs'])/(rows[1]['f_zs']-rows[2]['f_zs'])))
            results[str(g)]={'refinements':[2,4,8],'rows':rows,'extrapolated_f_zs':extrap,'shooting_order':order}
        out.update(gate_checks=results,f_zs_extrapolated=results['1.0']['extrapolated_f_zs'],
                   gate_systematic_range=float(np.ptp([r['extrapolated_f_zs'] for r in results.values()])),
                   shooting_remaining_estimate=abs(results['1.0']['extrapolated_f_zs']-results['1.0']['rows'][-1]['f_zs']),
                   all_ZS_roots_resolved=bool(all(r['root_ok'] and r['eta']>0 and r['evans_residual']<1e-8
                                                 for g in results.values() for r in g['rows'])))
    if census:
        p=abs(u)**2;dt=t[1]-t[0];imax=np.argmax(p)
        peaks,_=find_peaks(p,height=5e-5*np.max(p),prominence=1e-5*np.max(p),distance=max(1,int(.25/dt)))
        strongest=sorted(peaks,key=lambda j:p[j],reverse=True);rows=[]
        for j in strongest:
            a=d['N']*np.sqrt(p[j]);half=max(1.,8/a)
            other=[abs(t[j]-t[k]) for k in strongest if k!=j and p[k]>.005*p[j]]
            if other:half=min(half,.45*min(other))
            isolated=bool(half>=4/a)
            result=measure(t,u,d,refine=4,peak_index=j,gate_halfwidth=half,zs=isolated)
            result['isolated_by_width']=isolated;result['tallest']=bool(j==imax)
            columns=['t_peak','f_gate','f_zs','gated_energy_nJ','photon_fraction_gate','eta','red_THz','red_k','zeta_re','evans_residual','root_ok','gate_halfwidth','isolated_by_width','tallest']
            rows.append({k:result[k] for k in columns if k in result})
        out['census']=rows
        out['census_criteria']=dict(relative_peak_height=5e-5,relative_prominence=1e-5,minimum_peak_separation=.25,
                                    resolved_soliton_input_mass_floor=.01,peaks_screened=len(rows),no_peak_count_truncation=True)
        solitons=[r for r in rows if r.get('root_ok') and r.get('eta',0)>0 and r.get('f_zs',0)>.01
                  and abs(r['f_gate']/r['f_zs']-1)<.1]
        out['reddest_resolved_soliton_is_tallest']=bool(max(solitons,key=lambda r:r['red_THz'])['tallest']) if solitons else None
        out['reddest_resolved_soliton']=max(solitons,key=lambda r:r['red_THz']) if solitons else None
    return out

if __name__=='__main__':
    labels=[f'core_{T}_{m}' for T,m in [(100,'TL'),(100,'A'),(100,'A2'),(200,'TL'),(200,'B')]]
    labels += [f'length{z}_{T}_{m}' for z in [6,8] for T,m in [(100,'TL'),(100,'A2'),(200,'TL'),(200,'B')]]
    labels += [p.stem for p in RAW.glob('qualified_*.npz')
               if p.stem.endswith(('_main','_smooth','_grid','_window','_length6','_length6_TL'))]
    labels += [p.stem for p in RAW.glob('cutoff_smooth_*.npz')]
    labels += [p.stem for p in RAW.glob('heldout_N6_*.npz')]
    labels += ['integrable_N1']
    labels += [p.stem for p in RAW.glob('train_TL_N*.npz')]
    results={}
    for label in labels:
        if not (RAW/(label+'.npz')).exists():continue
        results[label]=readout_checks(label,census=label.startswith(('core_','length','heldout_N6_','cutoff_smooth_','train_TL_')) or label.endswith(('_main','_smooth','_length6','_length6_TL')))
        print(label,'f',results[label]['f_zs_extrapolated'],'gate spread',results[label]['gate_systematic_range'],
              'reddest',results[label].get('reddest_resolved_soliton_is_tallest'),flush=True)
        (HERE/'readout_checks.json').write_text(json.dumps({'agent':'gpt-a','model':'gpt-6-astra','family':'gpt','run_id':HERE.name,'cases':results},indent=2)+'\n')
    # The leading-pulse definition applies to robustness cases too. These
    # require a census, without repeating every full resolution/gate study.
    extra=[p.stem for p in RAW.glob('*.npz') if p.stem not in results and
           (p.stem.startswith(('shock_','tod_','loss_','smf_','published_','detuneE_','detune90_fine_')) or
            (p.stem.startswith('qualified_') and p.stem.endswith(('_mask','_TL'))))]
    for label in sorted(extra):
        record=json.loads((RAW/(label+'.json')).read_text())
        disagreement=('_TLpeak_' in label or abs(record.get('f_gate',0)-record.get('f_zs',0))>.01 or
                      not record.get('root_ok',False) or record.get('evans_residual',1)>1e-8)
        results[label]=readout_checks(label,census=True,refine_checks=disagreement)
        results[label]['extra_gate_resolution_diagnostic']=bool(disagreement)
        print('ROBUSTNESS CENSUS',label,results[label]['reddest_resolved_soliton_is_tallest'],flush=True)
        (HERE/'readout_checks.json').write_text(json.dumps({'agent':'gpt-a','model':'gpt-6-astra','family':'gpt','run_id':HERE.name,'cases':results},indent=2)+'\n')
