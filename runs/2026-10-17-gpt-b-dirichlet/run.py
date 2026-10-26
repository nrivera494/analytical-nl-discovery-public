#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Independent frozen tests."""
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
import argparse
RUN=Path(__file__).resolve().parent
DATA=RAW/RUN.name
DATA.mkdir(parents=True,exist_ok=True)

def mc():
    memory_gate();rng=np.random.default_rng(8101);rows=[]
    for K in [3,4,5,6,7,8]:
        m=Model(K);prediction=dirichlet_moments(m.q,.6)
        means=[];seconds=[]
        for j in range(40):
            a=shell_samples(m,.6,25000,rng);p=abs(a)**2
            means.append(p.mean(axis=0));seconds.append(p.T@p/len(p))
        means=np.array(means);seconds=np.array(seconds)
        mean=means.mean(axis=0);second=seconds.mean(axis=0)
        g=np.diag(second)/mean**2
        gs=np.diagonal(seconds,axis1=1,axis2=2)/means**2
        cov=second-np.outer(mean,mean)
        batch_cov=seconds-means[:,:,None]*means[:,None,:]
        cov_se=batch_cov.std(axis=0,ddof=1)/np.sqrt(len(means))
        vb=seconds[:,0,0]-means[:,0]**2
        np.savez_compressed(DATA/f'mc_K{K}_batch_moments.npz',means=means,seconds=seconds)
        gmean_se=float(gs[:,1:].mean(axis=1).std(ddof=1)/np.sqrt(len(gs)))
        zmean=float(np.max(abs(mean-prediction['mean'])/(means.std(axis=0,ddof=1)/np.sqrt(40))))
        zcov=float(np.max(abs(cov-prediction['cov'])/np.maximum(cov_se,1e-30)))
        zg=float(np.max(abs(g[1:]-prediction['g2'])/(gs[:,1:].std(axis=0,ddof=1)/np.sqrt(40))))
        rows.append(dict(K=K,M=m.M,held_out=K in [6,8],n=1000000,
            g2=g,g2_se=gs.std(axis=0,ddof=1)/np.sqrt(40),mean=mean,
            mean_se=means.std(axis=0,ddof=1)/np.sqrt(40),cov=cov,
            mean_g2_se=gmean_se,max_standardized_mean_error=zmean,max_standardized_covariance_error=zcov,
            max_standardized_g2_error=zg,pass_all_moments=max(zmean,zcov,zg)<5,
            variance_se=vb.std(ddof=1)/np.sqrt(40),prediction=prediction))
        print('MC',K,'mean g2',g[1:].mean(),'target',prediction['g2'],flush=True)
    sizes=np.array([r['M'] for r in rows]);err=2-np.array([r['g2'][1:].mean() for r in rows])
    exponent=float(np.polyfit(np.log(1/sizes),np.log(err),1)[0])
    coef,covfit=np.polyfit(np.log(1/sizes),np.log(err),1,cov=True)
    edges=[]
    for K,E,d0 in [(3,1.2,1),(3,.3,2),(3,.6,2),(3,.9,2),(5,.6,2)]:
        m=Model(K);s1=np.zeros(m.M);s2=np.zeros((m.M,m.M));count=0
        for j in range(40):
            a=shell_samples(m,E,25000,rng,d0=d0);p=abs(a)**2
            count+=len(p);s1+=p.sum(axis=0);s2+=p.T@p
        mean=s1/count;second=s2/count
        edges.append(dict(K=K,E=E,d0=d0,accepted=count,draws=1000000,mean=mean,
            g2=np.diag(second)/mean**2,var0=second[0,0]-mean[0]**2,
            scalar_prediction=dirichlet_moments(m.q,E)))
    save_json(RUN/'mc_summary.json',dict(**IDENTITY,rows=rows,finite_M_exponent=exponent,
        finite_M_exponent_fit_se=float(np.sqrt(covfit[0,0])),finite_M_coefficient=float(np.exp(coef[1])),
        finite_M_coefficient_fit_se=float(np.exp(coef[1])*np.sqrt(covfit[1,1])),edges=edges))

def single(m,E,sigma,launch,dis,dt=.04,zmax=8000,aligned=False,tag='core',groups=(1,2)):
    key=f'{tag}_K{m.K}_E{E:g}_s{sigma:g}_p{launch}_d{dis}_h{dt:g}_z{zmax:g}'
    path=DATA/(key+'.npz')
    if path.exists():return
    memory_gate()
    out=m.run(m.launch(E,launch,groups=groups,aligned=aligned),zmax=zmax,dt=dt,sigma=sigma,seed=dis)
    np.savez_compressed(path,**out)
    row=dict(**IDENTITY,key=key,K=m.K,E=E,sigma=sigma,phase_seed=launch,disorder_seed=dis,
        dt=dt,zmax=zmax,aligned=aligned,groups=list(groups),raw_file=str(path),wall_seconds=out['wall_seconds'])
    s=unpack(out['moments'][int((2000 if zmax==8000 else zmax/3)/100):],m.M)
    row['last_window']=s;row['checks']=out['checks']
    with (DATA/'records.jsonl').open('a') as f:f.write(json.dumps(serializable(row))+'\n')
    print(key,'I0',s['mean'][0],'g2',s['g2'][1:].mean(),'var0',s['cov'][0,0],
          'seconds',round(out['wall_seconds'],2),flush=True)

def core():
    for K,E in [(5,.3),(5,.6),(5,.9),(4,.45),(6,.75)]:
        m=Model(K)
        for sig in ([.3,3.] if K==5 else [.3]):
            for j in range(6):single(m,E,sig,4101+j,7101+j,tag='heldout' if K!=5 else 'core')

def convergence():
    m=Model(5)
    for sig in [.3,3.]:
        for h in [.02,.01]:
            for j in range(6):single(m,.6,sig,4101+j,7101+j,dt=h,tag='stepcheck')

def strong_extension():
    m=Model(5)
    for E in [.3,.6,.9]:
        for j in range(6):single(m,E,3.,4101+j,7101+j,zmax=24000,tag='strong_extension')

def phase_ensemble():
    m=Model(6)
    # 50 independent launches per quenched realization, exactly 200 in total.
    for d in range(4):
        for j in range(50):single(m,.75,.3,5101+50*d+j,7301+d,zmax=2000,tag='phase_ensemble')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['mc','core','convergence','strong_extension','phase_ensemble'])
    getattr(sys.modules[__name__],parser.parse_args().stage)()
