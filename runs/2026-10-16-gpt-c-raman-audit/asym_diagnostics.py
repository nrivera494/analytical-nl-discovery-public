"""Separate weak edge radiation from leading-pulse convergence. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
import numpy as np
from independent import RAW,census,write_json
HERE=Path(__file__).resolve().parent
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',comparisons=[],N2_clean64=[],N2_late128=[])
TR=.18*2*(1/32)/((1/32)**2+(1/12.2)**2)
for N,T in [(2,800),(2,1600),(2,3200),(2,6400),(4,6400)]:
    paths=[HERE/f'asym{mid}_N{N}_T{T}.json' for mid in ['', '_wide']]
    if not all(p.exists() for p in paths):continue
    a,b=[json.loads(p.read_text()) for p in paths]
    for cp in b['checkpoints']:
        zn=cp['zN'];old=next((v for v in a['checkpoints'] if v['zN']==zn),None)
        if old is None:continue
        results=[];fields=[]
        for report in [a,b]:
            case=dict(report['case'],zs_points=8192)
            d=np.load(RAW/(case['id']+'_zN'+str(zn)+'.npz'));t,q=d['t'],d['q']
            lead=census(t,q,case)['leading'];results.append(lead);fields.append((t,q))
        ta,qa=fields[0];tb,qb=fields[1];lead=results[0]
        mask=(ta>=lead['bounds'][0])&(ta<=lead['bounds'][1]);idx=np.searchsorted(tb,ta[mask])
        va=qa[mask];vb=qb[idx];phase=np.vdot(va,vb);aligned=vb*np.exp(-1j*np.angle(phase))
        item=dict(N=N,T0_fs=T,zN=zn,cases=[a['case']['id'],b['case']['id']],
            f1_narrow=results[0]['f_zs'],f1_wide=results[1]['f_zs'],
            fraction_difference=results[1]['f_zs']-results[0]['f_zs'],
            leading_field_relative_error=float(np.linalg.norm(vb-va)/np.linalg.norm(va)),
            leading_field_phase_aligned_relative_error=float(np.linalg.norm(aligned-va)/np.linalg.norm(va)),
            edge_narrow=old['max_time_edge_fraction'],edge_wide=cp['max_time_edge_fraction'])
        out['comparisons'].append(item)
        if N==2 and zn in [64,128]:
            f=results[1]['f_zs'];row=dict(item,excess=f/.75-1,cN=(f/.75-1)*T/TR)
            out['N2_clean64' if zn==64 else 'N2_late128'].append(row)
# Two fits make the saturation/edge sensitivity explicit. Late data keep their edge flags.
for key in ['N2_clean64','N2_late128']:
    points=sorted(out[key],key=lambda x:x['T0_fs'])
    if key=='N2_late128':
        byT={r['T0_fs']:r for r in out['N2_clean64']}
        byT.update({r['T0_fs']:r for r in points});points=sorted(byT.values(),key=lambda x:x['T0_fs'])
    if len(points)>1:
        tau=np.array([TR/r['T0_fs'] for r in points]);eps=np.array([r['excess'] for r in points])
        out[key+'_fit']=dict(exponent=float(np.polyfit(np.log(tau),np.log(eps),1)[0]),
            local=(np.diff(np.log(eps))/np.diff(np.log(tau))).tolist(),points=points,
            note='Late 128 checkpoints retain weak-radiation edge flags; compare with the clean64 fit and matched-window pulse differences.')
write_json(HERE/'asym_diagnostics.json',out)
print([(r['N'],r['T0_fs'],r['zN'],r['fraction_difference']) for r in out['comparisons']])
print([(k,out[k]['exponent']) for k in out if k.endswith('_fit')])
