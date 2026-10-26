"""Assemble traceable measured results without fitting new laws. gpt-c / gpt-6-astra / gpt."""
import json,re
from pathlib import Path
import numpy as np
from independent import write_json
HERE=Path(__file__).resolve().parent

def main():
    a=json.loads((HERE/'analysis.json').read_text());accuracy=json.loads((HERE/'accuracy.json').read_text()) if (HERE/'accuracy.json').exists() else None
    planned={};files=[HERE/'cases.json']+list(HERE.glob('*_cases.json'))
    for p in files:
        for c in json.loads(p.read_text()):planned[c['id']]=c
    inventory=[];memory=[]
    for name,c in planned.items():
        path=HERE/(name+'.json')
        if not path.exists():inventory.append({'id':name,'status':'unrun'});continue
        r=json.loads(path.read_text())
        state='complete' if r.get('complete') else ('edge-terminated' if r.get('terminated_for_edge') else ('error' if r.get('error') else 'partial'))
        inventory.append({'id':name,'status':state,'n':c['n'],'width':c['width'],'wall_seconds':r.get('wall_seconds'),
                          'grid_exception':c.get('grid_exception')})
        memory.append({'id':name,'rss':r.get('process_peak_rss_bytes',0),'free':r['free_percentage_at_start']})
    write_json(HERE/'inventory.json',{'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','cases':inventory,
        'counts':{s:sum(r['status']==s for r in inventory) for s in sorted({r['status'] for r in inventory})},
        'rejected_checkpoints':[{'id':r['id'],'zN':r['zN'],'reasons':r['rejections']} for r in a['rows'] if not r['qualified']]})
    ids={i for p in a['peaks'] if p['bracketed'] for i in p['bracket_ids']}
    rows=[r for r in a['rows'] if r['id'] in ids and r['zN']==4 and r['qualified']]
    bounds={}
    for model in ['physical','reference']:
        rs=[r for r in rows if r['model']==model];bounds[model]={}
        for k in ['dt_fs','time_edge','spectral_edge','loss_corrected_invariant_drift','global_support_1200_4000nm',
                  'leading_support_1200_4000nm','global_support_1500_3000nm','leading_support_1500_3000nm',
                  'gate_boundary_ratio','ZS_gate_ratio','local_dispersion_variation_one_rms','sech_fit_relative_l2',
                  'nonpositive_frequency_fraction']:
            v=[r[k] for r in rs if r[k] is not None]
            if v:bounds[model][k]=[float(min(v)),float(max(v))]
        if rs:
            bounds[model]['invariant_quantity']='photons' if model=='physical' else 'energy'
            bounds[model]['y_gain_peak_brackets']=[float(min(r['N']**2*9.23147929848/r['T0_fs'] for r in rs)),float(max(r['N']**2*9.23147929848/r['T0_fs'] for r in rs))]
    counts={model:{key:{verdict:sum(p['scores'][key]['verdict']==verdict for p in a['peaks'] if p['bracketed'] and p['model']==model)
                           for verdict in ['pass','fail','unresolved bracket']} for key in ['share','position','energy','width_fit','width_area']} for model in ['physical','reference']}
    core_fail=any(p['scores'][k]['verdict']=='fail' for p in a['peaks'] if p['bracketed'] and p['model']=='physical' for k in ['share','position','energy'])
    numerical_pass=bool(accuracy and len(accuracy.get('controls',[]))==17 and all(c['pass'] for c in accuracy['controls'])
        and accuracy.get('rk4ip',{}).get('pass') and accuracy.get('kernel_pass')
        and len(accuracy.get('shooting',[]))==2 and all(c['pass'] for c in accuracy['shooting'])
        and accuracy.get('strang',{}).get('pass') and accuracy.get('library',{}).get('pass'))
    maxrss=max(x['rss'] for x in memory);minfree=min(x['free'] for x in memory)
    if accuracy:
        maxrss=max(maxrss,accuracy.get('peak_rss_bytes',0))
        match=re.search(r'peak_rss_bytes=(\d+)',accuracy.get('library',{}).get('details',''))
        if match:maxrss=max(maxrss,int(match.group(1)))
    launch_path=HERE/'launch_checks.json'
    if launch_path.exists():
        minfree=min(minfree,*[r['free_percentage'] for r in json.loads(launch_path.read_text())['checks']])
    result={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','run_id':HERE.name,
        'status':('completed; proposer refutation of physical conjunction' if numerical_pass else 'proposer core refutation; numerical controls pending or failed') if core_fail else 'proposer tests in progress',
        'all_numerical_checks_pass':numerical_pass,
        'claim':'C-20261017-gpt-c-01','solver_commit':None,'freeze_commits':json.loads((HERE/'freeze.json').read_text()),
        'all_eight_peaks_bracketed':len(a['peaks'])==8 and all(p['bracketed'] for p in a['peaks']),
        'peaks':a['peaks'],'score_counts':counts,'peak_bracket_diagnostics':bounds,
        'memory':{'min_free_percentage':minfree,'max_single_process_rss_bytes':maxrss,
                  'execution':'One heavy process at a time; Python propagation, Julia and Strang checks serial.'},
        'inventory_counts':{s:sum(r['status']==s for r in inventory) for s in sorted({r['status'] for r in inventory})},
        'accuracy':accuracy,'uncertainty':'Full neighboring duration brackets; height allowance and coordinate sensitivity; numerical envelopes, not confidence intervals or material uncertainty.',
        'limitations':['finite output LN/LD=4, not saturated limiting partition','bulk response and separate published fibre model, not same spool',
                      'constant mode area and loss, cubic dispersion','local-ZS energy is operational; directly gated energy reported separately',
                      'no controlled physical remainder','proposer checks require independent Claude verification']}
    write_json(HERE/'summary.json',result)
    lines=['# Frozen material prediction scores','',f'Run `{HERE.name}`; gpt-c / gpt-6-astra / gpt. All material points held out.',
      'Intervals are numerical localization/resolution envelopes, not statistical or material confidence intervals.','',
      '| Model | N | Quantity | Frozen value (relative tolerance) | Measured [interval] | Central relative error | Verdict |',
      '|---|---:|---|---:|---|---:|---|']
    names={'share':'f1 sqrt(N)','position':'T0* (fs)','energy':'E1* (nJ)','width_fit':'T1 fit (fs)','width_area':'T1 area (fs)'}
    for p in a['peaks']:
        if not p['bracketed']:continue
        for k,s in p['scores'].items():
            lo,hi=s['measurement_interval'];lines.append(f"| {p['model']} | {p['N']} | {names[k]} | {s['prediction']:.5g} (±{100*s['tolerance_relative']:.0f}%) | {s['measured']:.5g} [{lo:.5g}, {hi:.5g}] | {100*s['relative_error']:+.2f}% | {s['verdict']} |")
    lines+=['','## Physical operating points','',
      'Widths and photon/gated observables are interpolated within the final duration bracket. Length and launch energy follow the fitted duration exactly. The ZS and gate definitions are distinct. No energy maximization under an input constraint was performed for ZBLAN.','',
      '| N | T0* (fs) | f1 ZS | f1 gate | E launch (nJ) | E1 ZS (nJ) | E1 gate (nJ) | Photon fraction | L (m) | Centroid (nm) |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in a['peaks']:
        if p['model']=='physical' and p['bracketed']:
            lines.append('| '+str(p['N'])+' | '+' | '.join(f'{p[k]:.6g}' for k in ['T0_fs','share','gated_share','launch_energy_nJ','energy_nJ','gated_energy_nJ','photon_fraction','length_m','centroid_nm'])+' |')
    lines+=['','## Controls and support','',
      'See `accuracy.json` for all control comparisons and measured numerical orders, `summary.json` for spectral-support and invariant bounds on each peak bracket, and `inventory.json` for every failed or unrun case.',
      'The reference invariant is energy; the physical model invariant is loss-corrected photon number. The legacy forward field `photon_drift` stores the energy drift when shock is disabled; the analysis labels it explicitly.','']
    (HERE/'tables.md').write_text('\n'.join(lines))
    print(json.dumps({'scores':counts,'inventory':result['inventory_counts'],'memory':result['memory'],'bounds':bounds},indent=2))
if __name__=='__main__':main()
