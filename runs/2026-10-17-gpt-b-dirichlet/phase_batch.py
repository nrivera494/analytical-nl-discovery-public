#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Fixed-length phase ensembles."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from summarize import metrics
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name
m=Model(6);rows=[]
for E,length,shots,first_dis,first_phase,tag in [(.75,2000,100,7301,5101,'enlarged'),(.5,8000,50,7401,6101,'fresh_heldout')]:
    cluster=[];check=[]
    for j in range(8):
        dis=first_dis+j;path=DATA/f'phase_batch_{tag}_d{dis}.npz'
        # First four clusters include the 50 original phase launches plus 50 new ones.
        if tag=='enlarged' and j<4:
            seeds=list(range(5101+50*j,5151+50*j))+list(range(5301+50*j,5351+50*j))
        else:
            start=5501+100*(j-4) if tag=='enlarged' else first_phase+shots*j;seeds=list(range(start,start+shots))
        initial=np.array([m.launch(E,seed) for seed in seeds])
        if not path.exists():
            memory_gate();start=time.time();out,final=m.ensemble(initial,np.inf,zmax=length,dt=.04,sample=length,sigma=.3,seed=dis)
            np.savez_compressed(path,initial=initial,final=final,moments=out,seeds=np.array(seeds))
            print(tag,dis,'seconds',round(time.time()-start,1),flush=True)
        d=np.load(path);p=abs(d['final'])**2
        cluster.append(np.r_[len(p),p.sum(axis=0),np.einsum('ni,nj->ij',p,p).ravel()])
        diff=p-abs(d['initial'])**2
        check.append(dict(disorder_seed=dis,max_N_drift=float(np.max(abs(diff.sum(axis=1)))),
                          max_E_drift=float(np.max(abs(np.sum(diff*m.q,axis=1)))),raw_file=str(path)))
    cm=np.array(cluster);v=metrics(cm,m.M,m.q)
    jack=np.array([metrics(np.delete(cm,i,axis=0),m.M,m.q) for i in range(len(cm))])
    se=np.sqrt((len(cm)-1)*np.mean((jack-jack.mean(axis=0))**2,axis=0));D=dirichlet_moments(m.q,E)
    pred=np.r_[D['mean'][0],D['cov'][0,0],D['g2'],D['cross'],np.full(m.M-1,D['g2']),
               [np.mean(D['cov'][0,1:][m.q[1:]==q]) for q in range(1,m.K)]]
    tol=np.r_[.01,.15*pred[1],.04,.03,np.full(m.M-1,.08)]
    flags=abs(v[:m.M+3]-pred[:m.M+3])<=np.maximum(tol,3*se[:m.M+3])
    signs=(np.sign(v[m.M+3:])==np.sign(pred[m.M+3:])) | (abs(pred[m.M+3:])<3*se[m.M+3:])
    rows.append(dict(tag=tag,E=E,length=length,shots=8*shots,disorder_realizations=8,
        pooled=v,se=se,prediction=pred,pass_moments=bool(np.all(flags)),moment_pass_flags=flags,
        covariance_sign_pass=bool(np.all(signs)),checks=check))
    save_json(RUN/'phase_batch_summary.json',dict(**IDENTITY,rows=rows))
    print(tag,rows[-1]['pass_moments'],rows[-1]['covariance_sign_pass'],v[:4],se[:4],flush=True)

# Post-data implementation diagnostic: enlargement must retain the original
# trajectories exactly, not silently replace their Brownian paths.
original=[json.loads(s) for s in (DATA/'records.jsonl').read_text().splitlines()]
original=[r for r in original if r['key'].startswith('phase_ensemble')]
errors=[]
for dis in range(7301,7305):
    d=np.load(DATA/f'phase_batch_enlarged_d{dis}.npz')
    for r in original:
        if r['disorder_seed']!=dis:continue
        j=int(np.flatnonzero(d['seeds']==r['phase_seed'])[0])
        a=np.load(r['raw_file'])['checkpoints'][-1]
        errors.append(float(np.linalg.norm(a-d['final'][j])))
save_json(RUN/'phase_implementation_checks.json',dict(**IDENTITY,
    original_phase_draws_checked=len(errors),max_single_vs_batched_final_field_difference=max(errors),
    pass_exact_retention=all(e==0 for e in errors)))
