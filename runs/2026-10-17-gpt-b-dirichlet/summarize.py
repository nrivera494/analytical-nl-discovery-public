#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Clustered statistical checks."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from collections import defaultdict
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def metrics(raw,M,q):
    st=unpack(raw,M);g=st['g2'];co=st['cov'][0,1:]
    cross=st['cross'][1:,1:];cross=(cross.sum()-np.trace(cross))/((M-1)*(M-2))
    group=np.array([np.mean(co[q[1:]==j]) for j in range(1,max(q)+1)])
    return np.r_[st['mean'][0],st['cov'][0,0],g[1:].mean(),cross,g[1:],group]

def aggregate(rows,start,end):
    K,E,sig=rows[0]['K'],rows[0]['E'],rows[0]['sigma'];m=Model(K)
    mats=[]
    for r in rows:
        d=np.load(r['raw_file']);mats.append(d['moments'][round(start/100):round(end/100)].sum(axis=0))
    mats=np.asarray(mats);pooled=metrics(mats,m.M,m.q)
    individual=np.array([metrics(x[None,:],m.M,m.q) for x in mats])
    jack=np.array([metrics(np.delete(mats,i,axis=0),m.M,m.q) for i in range(len(mats))])
    se=np.sqrt((len(jack)-1)*np.mean((jack-jack.mean(axis=0))**2,axis=0))
    D=dirichlet_moments(m.q,E)
    pred=np.r_[D['mean'][0],D['cov'][0,0],D['g2'],D['cross'],np.full(m.M-1,D['g2']),
               [np.mean(D['cov'][0,1:][m.q[1:]==j]) for j in range(1,K)]]
    tol=np.r_[.01,.15*pred[1],.04,.03,np.full(m.M-1,.08),np.zeros(K-1)]
    within=abs(pooled[:m.M+3]-pred[:m.M+3])<=np.maximum(tol[:m.M+3],3*se[:m.M+3])
    c=pooled[m.M+3:];cse=se[m.M+3:];cp=pred[m.M+3:]
    signs=(np.sign(c)==np.sign(cp)) | (abs(cp)<3*cse)
    return dict(K=K,M=m.M,E=E,sigma=sig,start=start,end=end,realizations=len(rows),
        pooled=pooled,se=se,individual=individual,prediction=pred,
        max_N_drift=max(r['checks'][4] for r in rows),max_E_drift=max(r['checks'][5] for r in rows),
        metric_order=['meanI0','varI0','mean_excited_g2','mean_cross_g2','all_excited_g2','group_covariances'],
        pass_moments=bool(np.all(within)),moment_pass_flags=within,
        covariance_sign_pass=bool(np.all(signs)),variance_ratio=pooled[1]/pred[1],
        variance_ratio_se=se[1]/pred[1],held_out=K!=5)

def main():
    rows=[json.loads(s) for s in (DATA/'records.jsonl').read_text().splitlines()];groups=defaultdict(list)
    for r in rows:
        if r['key'].startswith('phase_ensemble'):continue
        groups[r['K'],r['E'],r['sigma'],r['dt'],r['zmax']].append(r)
    out=[]
    for key,rr in sorted(groups.items()):
        if len(rr)<2:continue
        z=rr[0]['zmax'];d=aggregate(rr,2000 if z==8000 else 8000,z);d['dt']=rr[0]['dt'];out.append(d)
    finite=[]
    rr=[r for r in rows if r['K']==5 and r['E']==.6 and r['sigma']==.3 and r['dt']==.04 and r['zmax']==8000]
    m=Model(5);prediction=dirichlet_moments(m.q,.6)
    by_cluster=[]
    for T in [500,1000,2000,4000]:
        errors=[]
        cluster=[]
        for r in rr:
            start_index=len(errors)
            moments=np.load(r['raw_file'])['moments'][20:]
            for j in range(0,len(moments)-T//100+1,T//100):
                st=unpack(moments[j:j+T//100],m.M)
                errors.append([st['mean'][0]-prediction['mean'][0],st['g2'][1:].mean()-prediction['g2'],
                               st['cov'][0,0]/prediction['cov'][0,0]-1])
            cluster.append(np.mean(np.array(errors[start_index:])**2,axis=0))
        by_cluster.append(cluster)
        finite.append(dict(window=T,independent_disorder_realizations=len(rr),windows=len(errors),
                           bias=np.mean(errors,axis=0),rms=np.sqrt(np.mean(np.array(errors)**2,axis=0))))
    exp=np.polyfit(np.log([r['window'] for r in finite]),np.log([r['rms'] for r in finite]),1)[0]
    rng=np.random.default_rng(8311);bc=np.array(by_cluster);boot=[]
    for _ in range(2000):
        idx=rng.integers(0,len(rr),len(rr))
        rms=np.sqrt(bc[:,idx,:].mean(axis=1))
        boot.append(np.polyfit(np.log([r['window'] for r in finite]),np.log(rms),1)[0])
    phase=[r for r in rows if r['key'].startswith('phase_ensemble')]
    phase_result=None
    if phase:
        m=Model(6);clusters=defaultdict(list)
        for r in phase:clusters[r['disorder_seed']].append(abs(np.load(r['raw_file'])['checkpoints'][-1])**2)
        cluster_sums=[]
        for seed,pp in clusters.items():
            p=np.array(pp);cluster_sums.append(np.r_[len(p),p.sum(axis=0),np.einsum('ni,nj->ij',p,p).ravel()])
        cm=np.array(cluster_sums);v=metrics(cm,m.M,m.q)
        jack=np.array([metrics(np.delete(cm,i,axis=0),m.M,m.q) for i in range(len(cm))])
        se=np.sqrt((len(cm)-1)*np.mean((jack-jack.mean(axis=0))**2,axis=0))
        D=dirichlet_moments(m.q,.75)
        pred=np.r_[D['mean'][0],D['cov'][0,0],D['g2'],D['cross'],np.full(m.M-1,D['g2']),
                   [np.mean(D['cov'][0,1:][m.q[1:]==j]) for j in range(1,m.K)]]
        tol=np.r_[.01,.15*pred[1],.04,.03,np.full(m.M-1,.08)]
        flags=abs(v[:m.M+3]-pred[:m.M+3])<=np.maximum(tol,3*se[:m.M+3])
        signpass=(np.sign(v[m.M+3:])==np.sign(pred[m.M+3:])) | (abs(pred[m.M+3:])<3*se[m.M+3:])
        phase_result=dict(shots=len(phase),disorder_realizations=len(cm),length=2000,pooled=v,se=se,
                          prediction=pred,moment_pass_flags=flags,pass_moments=bool(np.all(flags)),
                          covariance_sign_pass=bool(np.all(signpass)),
                          groups=[dict(disorder_seed=k,shots=len(v)) for k,v in clusters.items()])
    summary=dict(**IDENTITY,groups=out,finite_time=finite,finite_time_rms_exponents=exp,
                  finite_time_exponent_cluster_bootstrap_ci95=np.quantile(boot,[.025,.975],axis=0),
                  phase_ensemble=phase_result,
                  phase_followup=json.loads((RUN/'phase_batch_summary.json').read_text()) if (RUN/'phase_batch_summary.json').exists() else None,
                  mc=json.loads((RUN/'mc_summary.json').read_text()),
                  normal_form=json.loads((RUN/'normal_form_summary.json').read_text()) if (RUN/'normal_form_summary.json').exists() else None)
    save_json(RUN/'summary.json',summary)
    for r in out:
        print(r['K'],r['E'],r['sigma'],r['dt'],r['end'],'g2',round(r['pooled'][2],4),
            'varratio',round(r['variance_ratio'],3),'+/-',round(r['variance_ratio_se'],3),
            'pass',r['pass_moments'],r['covariance_sign_pass'])
    print('finite-time RMS exponents',exp)

if __name__=='__main__':main()
