#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Frozen shell tests."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def time_stats(path,start):
    d=np.load(path);mom=d['moments'];block=float(d['z'][1]);v=mom[round(start/block):,1]/mom[round(start/block):,0]
    se=[]
    for width in [1000,2000,5000,10000,20000,40000,80000,160000,200000]:
        size=max(1,round(width/block));nb=len(v)//size
        if nb>=4:
            b=v[:nb*size].reshape(nb,size).mean(axis=1)
            se.append(float(b.std(ddof=1)/np.sqrt(nb)))
    n=len(v)//2
    return dict(mean=float(v.mean()),se=max(se),half_shift=float(v[-n:].mean()-v[:n].mean()),
                last_half_mean=float(v[-n:].mean()),block=block)

def main():
    rec=[json.loads(s) for s in (DATA/'records.jsonl').read_text().splitlines()]
    pred=json.loads((RUN/'final_predictions.json').read_text())['rows'];m=Model(5);det=[]
    for r in rec:
        if r['sigma']!=0:continue
        t=r['case'];row=dict({k:v for k,v in r.items() if k!='last_window'},
                            **time_stats(r['raw_file'],4000 if r['zmax']==24000 else r['zmax']/3))
        row['RJ']=float(dirichlet_moments(m.q,t['E'])['mean'][0]);row['shells']=[]
        for L in [False,True]:
            p=next(p for p in pred if p['E']==t['E'] and p['seed']==t['seed'] and p['include_L']==L)
            w=p['widths'][-1];combined=np.hypot(row['se'],w['se'])
            row['shells'].append(dict(include_L=L,mean=w['mean'],se=w['se'],bandwidth_shift=p['bandwidth_shift'],
                residual=row['mean']-w['mean'],tolerance=max(.01,3*combined),
                pass_endpoint=bool(abs(row['mean']-w['mean'])<=max(.01,3*combined)),
                pass_stationarity=bool(abs(row['half_shift'])<=max(.01,3*row['se']))))
        d=np.load(r['raw_file']);a=d['checkpoints']
        perm=[m.modes.index((y,x)) for x,y in m.modes]
        odd=np.linalg.norm((a-a[:,perm])/2,axis=1)
        row['reflection_antisymmetric_norm_max']=float(np.max(odd))
        indices=np.flatnonzero(odd>1e-8)
        row['reflection_first_above_1e-8']=float(d['z'][indices[0]]) if len(indices) else None
        row['pass_invariant_drift']=bool(np.max(r['checks'][4:8])<1e-5)
        for name,mat in [('X',m.X),('Y',m.Y),('B',m.B)]:
            vals=np.einsum('ni,ij,nj->n',np.conj(a),mat,a)
            row[name+'_max_drift']=float(np.max(abs(vals-vals[0])))
        det.append(row)
    memory=[]
    for sig,zmax in sorted(set((r['sigma'],r['zmax']) for r in rec if r['sigma']>0)):
        rows=[r for r in rec if r['sigma']==sig and r['zmax']==zmax]
        windows=[(2000,8000),(6000,8000)] if zmax==8000 else [(8000,24000),(18000,24000)]
        for start,end in windows:
            paired=[]
            for dis in sorted(set(r['disorder_seed'] for r in rows)):
                p=[]
                for seed in [4101,0]:
                    r=next(r for r in rows if r['disorder_seed']==dis and r['case']['seed']==seed)
                    d=np.load(r['raw_file']);v=d['moments'][start//100:end//100]
                    p.append(float(unpack(v,m.M)['mean'][0]))
                paired.append(p)
            paired=np.array(paired);means=paired.mean(axis=0);se=paired.std(axis=0,ddof=1)/np.sqrt(len(paired))
            dif=paired[:,0]-paired[:,1];delta=float(dif.mean());dse=float(dif.std(ddof=1)/np.sqrt(len(dif)))
            rj=float(dirichlet_moments(m.q,.6)['mean'][0])
            memory.append(dict(sigma=sig,Ld=1/sig**2,start=start,end=end,means=means,se=se,
                differences=dif,difference=delta,difference_se=dse,RJ=rj,
                compatible_with_erasure=abs(delta)<=max(.01,3*dse) and bool(np.all(abs(means-rj)<=np.maximum(.01,3*se))),
                resolved_erasure=abs(delta)+2*dse<.02 and bool(np.all(abs(means-rj)+2*se<.02))))
    reflection=[]
    if (RUN/'reflection_summary.json').exists():
        rp=json.loads((RUN/'reflection_predictions.json').read_text())['rows']
        for original in json.loads((RUN/'reflection_summary.json').read_text())['rows']:
            row=dict(original)
            row['se_fixed_10000_block']=row.pop('se')
            row.update(time_stats(row['raw_file'],80000))
            if row['variant']=='exact_sector':
                p=next(p for p in rp if p['E']==row['E'])
                row['reference']='reflection-even reduced Hamiltonian shell'
            else:
                p=next(p for p in pred if p['E']==row['E'] and p['seed']==0 and p['include_L'])
                row['reference']='unperturbed full (H,L) shell; actual perturbed charges recorded'
            w=p['widths'][-1]
            row['prediction']=dict(mean=w['mean'],se=w['se'],bandwidth_shift=p['bandwidth_shift'])
            row['tolerance']=max(.01,3*np.hypot(row['se'],w['se']))
            row['pass_endpoint']=bool(abs(row['mean']-w['mean'])<=row['tolerance'])
            row['pass_stationarity']=bool(abs(row['half_shift'])<=max(.01,3*row['se']))
            row['pass_invariant_drift']=bool(np.max(row['checks'][4:8])<1e-5)
            reflection.append(row)
    resolution=json.loads((RUN/'resolution_summary.json').read_text()) if (RUN/'resolution_summary.json').exists() else None
    save_json(RUN/'summary.json',dict(**IDENTITY,deterministic=det,memory=memory,reflection=reflection,resolution=resolution,
        prediction_commit='925e15923f30798e64e263537490a59978157353'))
    for r in det:
        print(r['case']['E'],r['case']['seed'],r['dt'],round(r['mean'],5),round(r['se'],5),
              'shift',round(r['half_shift'],5),'HL',round(r['shells'][1]['mean'],5),
              r['shells'][1]['pass_endpoint'],r['shells'][1]['pass_stationarity'])
    for r in memory:
        if r['start']==2000:print('memory',r['sigma'],r['means'],r['difference'],r['difference_se'],r['resolved_erasure'])

if __name__=='__main__':main()
