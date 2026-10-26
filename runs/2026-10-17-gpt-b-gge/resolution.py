#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Bounded final diagnostics."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from conditioned import diagnostic
from summarize import time_stats
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def initial(model,tag):
    if tag=='phase4103':return model.launch(.6,4103)
    a=model.launch(.6,0,aligned=True)
    if tag=='perturbed_1e-4':a[1]*=np.exp(1e-4j)
    return a

def shell():
    m=Model(5);old=json.loads((RUN/'shell_predictions.json').read_text())['rows'];rows=[]
    for ti,tag in enumerate(['phase4103','perturbed_1e-4']):
        memory_gate();a0=initial(m,tag);inv=m.invariants(a0)
        reference=next(r for r in old if r['E']==.6 and r['seed']==(4103 if ti==0 else 0))
        hs,ls=reference['shell_H_sd'],reference['shell_L_sd'];widths=[.05,.025,.0125]
        path=DATA/f'resolution_shell_{tag}.npz';steps=8000000
        if not path.exists():
            start=time.time();blocks=np.empty((3,4,steps//10000,4));accept=np.empty((3,4,6))
            for chain in range(4):
                rng=np.random.default_rng(9751+100*ti+chain)
                a=a0.copy() if chain<2 else shell_samples(m,.6,1,rng)[0]
                for w in [.8,.4,.2,.1]:
                    a,_,_=m.mcmc(a,.6,inv[2],inv[3],w*hs,w*ls,steps=200000,seed=int(rng.integers(1,2**32)))
                for wi,w in enumerate(widths):
                    a,_,_=m.mcmc(a,.6,inv[2],inv[3],w*hs,w*ls,steps=500000,seed=int(rng.integers(1,2**32)))
                    a,b,d=m.mcmc(a,.6,inv[2],inv[3],w*hs,w*ls,steps=steps,seed=int(rng.integers(1,2**32)))
                    blocks[wi,chain]=b;accept[wi,chain]=d
            np.savez_compressed(path,blocks=blocks,acceptance=accept)
            print(tag,'shell seconds',time.time()-start,flush=True)
        data=np.load(path);stats=[]
        for wi,w in enumerate(widths):
            st=diagnostic(data['blocks'][wi,:,:,0]);st.update(width=w,
                mean_H=float(data['blocks'][wi,:,:,1].mean()),mean_L=float(data['blocks'][wi,:,:,2].mean()),
                acceptance_fractions=data['acceptance'][wi,:,:2]/(steps/2))
            stats.append(st)
        shift=abs(stats[-1]['mean']-stats[-2]['mean'])
        rows.append(dict(tag=tag,initial_invariants=inv,widths=stats,bandwidth_shift=shift,
            resolved=stats[-1]['resolved'] and stats[-2]['resolved'] and shift<.01,raw_file=str(path)))
        print(tag,serializable(rows[-1]),flush=True)
        save_json(RUN/'resolution_predictions.json',dict(**IDENTITY,rows=rows))

def propagate(tag,h,zmax,sigma=0,dis=7101):
    full=Model(5);a=initial(full,tag)
    if tag=='exact_sector':m,U=reflection_sector(full);a=U.T@a
    elif tag.startswith('memory'):
        m=full;a=m.launch(.6,4101 if tag=='memory4101' else 0,aligned=tag=='memory0')
    else:m=full
    path=DATA/f'resolution_{tag}_h{h:g}_s{sigma:g}_d{dis}_z{zmax}.npz'
    if not path.exists():
        memory_gate();out=m.run(a,zmax=zmax,dt=h,sigma=sigma,seed=dis,
            block=400 if sigma else 4000,sample=4 if sigma else 40)
        np.savez_compressed(path,**out)
        row=dict(**IDENTITY,tag=tag,dt=h,zmax=zmax,sigma=sigma,disorder_seed=dis,
            initial_invariants=m.invariants(a),checks=out['checks'],wall_seconds=out['wall_seconds'],raw_file=str(path))
        with (DATA/'resolution_records.jsonl').open('a') as f:f.write(json.dumps(serializable(row))+'\n')
        print(tag,h,sigma,dis,'seconds',out['wall_seconds'],'drift',out['checks'][4:8],flush=True)

def dynamics():
    # Caller must commit resolution_predictions.json before invoking this stage.
    for tag in ['phase4103','perturbed_1e-4']:
        for h in [.01,.005]:propagate(tag,h,1200000)
    propagate('exact_sector',.01,1200000)

def memory():
    for h,seeds in [(.04,range(7101,7113)),(.02,range(7101,7105))]:
        for dis in seeds:
            for tag in ['memory4101','memory0']:propagate(tag,h,96000,sigma=3.,dis=dis)

def sector_step():
    # Additional convergence check frozen after the first long-sector result.
    propagate('exact_sector',.005,1200000)

def summarize():
    rec=[json.loads(s) for s in (DATA/'resolution_records.jsonl').read_text().splitlines()]
    pred=json.loads((RUN/'resolution_predictions.json').read_text())['rows']
    sector=json.loads((RUN/'reflection_predictions.json').read_text())['rows'];det=[]
    for r in rec:
        if r['sigma']:continue
        st=time_stats(r['raw_file'],400000)
        p=next(p for p in (sector if r['tag']=='exact_sector' else pred)
               if (p['E']==.6 if r['tag']=='exact_sector' else p['tag']==r['tag']))
        w=p['widths'][-1];tol=max(.01,3*np.hypot(st['se'],w['se']))
        det.append(dict(r,**st,prediction=w['mean'],prediction_se=w['se'],bandwidth_shift=p['bandwidth_shift'],
            shell_resolved=p.get('resolved',w['resolved']),tolerance=tol,
            pass_endpoint=bool(abs(st['mean']-w['mean'])<=tol),
            pass_precision=bool(2*st['se']<.01 and 2*w['se']+p['bandwidth_shift']<.01),
            pass_stationarity=bool(abs(st['half_shift'])<=max(.01,3*st['se'])),
            pass_invariant_drift=bool(np.max(r['checks'][4:8])<1e-5)))
    convergence=[]
    for tag in ['phase4103','perturbed_1e-4','exact_sector']:
        rr=[r for r in det if r['tag']==tag]
        if len(rr)!=2:continue
        delta=rr[0]['mean']-rr[1]['mean'];tol=max(.01,3*np.hypot(rr[0]['se'],rr[1]['se']))
        convergence.append(dict(tag=tag,difference=delta,tolerance=tol,pass_step=abs(delta)<=tol))
    step_checks={r['tag']:r['pass_step'] for r in convergence}
    for r in det:
        r['pass_all_frozen_gates']=bool(r['shell_resolved'] and r['pass_endpoint'] and
            r['pass_precision'] and r['pass_stationarity'] and r['pass_invariant_drift'] and
            step_checks.get(r['tag'],False))
    memory=[];rj=float(dirichlet_moments(Model(5).q,.6)['mean'][0])
    for h in [.04,.02]:
        rr=[r for r in rec if r['sigma']==3 and r['dt']==h]
        if not rr:continue
        for start in [32000,72000]:
            pairs=[]
            for dis in sorted(set(r['disorder_seed'] for r in rr)):
                pair=[]
                for tag in ['memory4101','memory0']:
                    r=next(r for r in rr if r['disorder_seed']==dis and r['tag']==tag)
                    data=np.load(r['raw_file']);mom=data['moments'][start//400:]
                    pair.append(float(unpack(mom,15)['mean'][0]))
                pairs.append(pair)
            pairs=np.array(pairs);means=pairs.mean(axis=0);se=pairs.std(axis=0,ddof=1)/np.sqrt(len(pairs))
            d=pairs[:,0]-pairs[:,1];delta=float(d.mean());dse=float(d.std(ddof=1)/np.sqrt(len(d)))
            memory.append(dict(dt=h,start=start,end=96000,disorder_realizations=len(pairs),means=means,se=se,
                difference=delta,difference_se=dse,RJ=rj,
                resolved_erasure=abs(delta)+2*dse<.02 and bool(np.all(abs(means-rj)+2*se<.02)),
                max_N_drift=max(r['checks'][4] for r in rr),max_E_drift=max(r['checks'][5] for r in rr)))
    base_plan_complete=len(det)>=5 and len([r for r in rec if r['sigma']==3])==32
    sector_refinement_complete=any(r['tag']=='exact_sector' and r['dt']==.005 for r in det)
    complete=base_plan_complete and len(det)==6 and sector_refinement_complete
    save_json(RUN/'resolution_summary.json',dict(**IDENTITY,complete=complete,
        base_plan_complete=base_plan_complete,sector_refinement_complete=sector_refinement_complete,
        deterministic=det,convergence=convergence,memory=memory,
        memory_resolved_all_steps_windows=len(memory)==4 and all(r['resolved_erasure'] for r in memory)))
    for r in det:print(r['tag'],r['dt'],r['mean'],r['se'],r['prediction'],r['pass_endpoint'],r['pass_stationarity'])
    for r in memory:print('memory',serializable(r))

if __name__=='__main__':globals()[sys.argv[1]]()
