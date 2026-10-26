#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
from independent import *
import tomli

def build():
    records={}
    for p in RAW.glob('*.json'):
        d=json.loads(p.read_text())
        if 'label' in d and 'N' in d and 'mask' in d:records[d['label']]=d
    # Earliest core/convergence records predate ancillary photon bookkeeping.
    # Recover missing metadata from the unchanged saved field, without a new
    # propagation or replacement of any originally recorded value.
    completed=[]
    for label,d in records.items():
        if 'photon_fraction_gate' not in d:
            with np.load(RAW/(label+'.npz')) as field:
                measured=measure(field['t'],field['u'],d,zs=False)
            for key,value in measured.items():d.setdefault(key,value)
            completed.append(label)
    summary={'run_id':HERE.name,'agent':'gpt-a','model':'gpt-6-astra','family':'gpt',
             'freeze_commit':'04cf1e92059772ef6bda543e933460698acd1ce6','cases':records,'pairs':{},'convergence':{},'optimizations':[]}
    summary['ancillary_readout_completion']={'cases':completed,'method':'Missing photon/energy metadata only, measured from unchanged raw fields with zs=False; existing values and raw records retained.'}
    summary['known_limit_control']={'case':'integrable_N1','fR':0.,'exact_field':'sech(tau) exp(i xi/2)','exact_eta':.5,'exact_fraction':1.}
    if (RAW/'integrable_N1.json').exists():
        summary['known_limit_control']['measurement']=json.loads((RAW/'integrable_N1.json').read_text())
    for T,m in [(100,'A2'),(100,'A'),(200,'B')]:
        a=records.get(f'core_{T}_{m}');b=records.get(f'core_{T}_TL')
        if a and b:summary['pairs'][f'core_{T}_{m}']={'H_zs':a['f_zs']/b['f_zs'],'H_gate':a['f_gate']/b['f_gate'],
              'shift_ratio':a['red_THz']/b['red_THz'],'masked':a['label'],'baseline':b['label']}
    for key,a in records.items():
        if a['mask']=='TL':continue
        if key.startswith(('shock_','tod_','loss_','smf_','published_','detuneE_')):
            bkey=key.rsplit('_',1)[0]+'_TL';b=records.get(bkey)
            if b:summary['pairs'][key]={'H_zs':a.get('f_zs',0)/b.get('f_zs',1),'H_gate':a['f_gate']/b['f_gate'],
                   'H_photon_gate':a.get('photon_fraction_gate',0)/b.get('photon_fraction_gate',1),
                   'shift_ratio':a['red_THz']/b['red_THz'],'masked':key,'baseline':bkey}
    for T,m in [(100,'TL'),(100,'A2'),(200,'TL'),(200,'B')]:
        labels=[f'step2.0_{T}_{m}',f'core_{T}_{m}',f'step0.5_{T}_{m}',f'step0.25_{T}_{m}']
        if all(x in records for x in labels):
            fields=[np.load(RAW/(x+'.npz'))['u'] for x in labels]
            diffs=[float(np.linalg.norm(a-b)/np.linalg.norm(b)) for a,b in zip(fields[:-1],fields[1:])]
            orders=[float(np.log2(diffs[j]/diffs[j+1])) for j in range(2)]
            summary['convergence'][f'{T}_{m}']={'labels':labels,'successive_field_differences':diffs,'orders':orders,
              'f_zs':[records[x]['f_zs'] for x in labels]}
            grid=RAW/f'grid_{T}_{m}.npz';window=RAW/f'window_{T}_{m}.npz'
            if grid.exists():
                fine=np.load(grid)['u'][::2]
                summary['convergence'][f'{T}_{m}']['grid_field_difference']=float(np.linalg.norm(fine-fields[1])/np.linalg.norm(fields[1]))
            if window.exists():
                wide=np.load(window)['u'];offset=(len(wide)-len(fields[1]))//2
                summary['convergence'][f'{T}_{m}']['window_central_field_difference']=float(np.linalg.norm(wide[offset:offset+len(fields[1])]-fields[1])/np.linalg.norm(fields[1]))
    ja=RAW/'opt_N4_T200_TL_zs_checkfield.npz';pa=RAW/'reference_python_N4_T200_TL_checkfield.npz'
    if ja.exists() and pa.exists():
        a=np.load(ja)['u'].ravel();b=np.load(pa)['u'].ravel()
        summary['second_solver_relative_field_error']=float(np.linalg.norm(a-b)/np.linalg.norm(b))
    ja=RAW/'opt_N4_T200_warmselected_zs_forwardfield.npz';pa=RAW/'stationarity_N4_nt8192_field.npz'
    if ja.exists() and pa.exists():
        a=np.load(ja)['u'].ravel();b=np.load(pa)['u'].ravel()
        summary['second_solver_selected_N4_relative_field_error']=float(np.linalg.norm(a-b)/np.linalg.norm(b))
    summary['derivative_checks']={}
    for p in RAW.glob('*_check.json'):summary['derivative_checks'][p.name]=json.loads(p.read_text())
    summary['implementation_checks']={p.name:json.loads(p.read_text()) for p in RAW.glob('*_validation.json')}
    summary['readout_diagnostics']={p.name:json.loads(p.read_text()) for p in RAW.glob('*_diagnosis.json')}
    for p in RAW.glob('*_check.toml'):
        with open(p,'rb') as f:summary['derivative_checks'][p.name]=tomli.load(f)
    for p in RAW.glob('*_summary.json'):
        d=json.loads(p.read_text());summary['optimizations'].append(d)
    summary['optimization_traces']={}
    for p in RAW.glob('pyopt_*_history.jsonl'):
        rows=[json.loads(line) for line in p.read_text().splitlines() if line.strip()]
        if not rows:continue
        best=-float('inf');trace=[]
        for j,row in enumerate(rows):
            best=max(best,row['f_zs'])
            if j%5==0 or j==len(rows)-1:trace.append([row.get('total_evaluation',row['evaluation']),best,row['gradient_norm'],row['elapsed_s']])
        summary['optimization_traces'][p.stem.replace('_history','')]=trace
    masks=HERE/'mask_candidates';masks.mkdir(exist_ok=True)
    for p in RAW.glob('pyopt_*_bestcoef.csv'):
        coeff=np.loadtxt(p,delimiter=',')
        np.savetxt(masks/p.name,coeff,delimiter=',',header='agent: gpt-a; model: gpt-6-astra; family: gpt\nLegendre orders 2-31; standard FFT convention; cutoff 2*pi; best encountered, see summary for stationarity')
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('cases',len(records),'paired comparisons',len(summary['pairs']),
          'completed optimizations',[(x['N'],x['start'],x['f_zs'],x['gradient_norm']) for x in summary['optimizations']],
          'second-solver field error',summary.get('second_solver_relative_field_error'),flush=True)
    return summary
if __name__=='__main__':build()
