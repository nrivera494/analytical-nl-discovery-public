#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt, frozen independent GRIN squeezing tests."""
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from squeezing import *
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name;DATA.mkdir(exist_ok=True)
COND=RUN.parent/'2026-10-18-gpt-b-condensate-squeezing'
ZS=np.array([0,1,2,5,10,20,50,100,200,300])

def tangent_case(K,E,sigma,launch,dis,zmax=100,dt=.02):
    tag=f'K{K}_E{E:g}_s{sigma:g}_l{launch}_d{dis}_h{dt:g}_z{zmax:g}'
    path=DATA/(tag+'_tangent.npz');m=Model(K);a=m.launch(E,launch);zs=ZS[ZS<=zmax]
    if path.exists():x=np.load(path)['x']
    else:
        memory_gate();start=time.time();x=tangent_run(m,a,zs,dt,sigma,dis);np.savez_compressed(path,x=x,z=zs)
        print('tangent',tag,round(time.time()-start,2),flush=True)
    rows=[]
    for z,xi in zip(zs,x):
        r=tangent_observables(xi)
        for k in ['a','S','V','quad_direction','count_direction','P']:r.pop(k)
        r.update(z=float(z),N=float(np.sum(abs(xi[0])**2)),E=float(np.sum(m.q*abs(xi[0])**2)))
        rows.append(r)
    rec=dict(K=K,E=E,sigma=sigma,launch=launch,disorder=dis,dt=dt,zmax=zmax,rows=rows,raw_file=str(path),tag=tag)
    save_json(DATA/(tag+'_tangent.json'),rec)
    return m,a,zs,x,rec

def ensembles():
    cases=[]
    for dis in range(7601,7613):cases.append((5,.3,.3,4201,dis))
    for launch in range(4202,4213):cases.append((5,.3,.3,launch,7601))
    for sigma in [1,3,2]:
      for dis in range(7601,7607):cases.append((5,.3,sigma,4201,dis))
    for dis in range(7601,7613):cases.append((5,.45,.3,4201,dis))
    records=[]
    for case in cases:records.append(tangent_case(*case)[-1]);save_json(COND/'ensemble_summary.json',dict(**IDENTITY,records=records,complete=len(records)==len(cases)))
    # Resolution and a second mode truncation, independent held-out paths.
    extra=[]
    for case in [(5,.3,.3,4201,7601),(5,.3,3,4201,7601),(5,.45,.3,4201,7602),(5,.3,2,4201,7602)]:
      extra.append(tangent_case(*case,dt=.01)[-1])
    for case in [(4,.45,3,4202,7602),(5,.6,0,4201,7601),(5,.6,3,4202,7602)]:
      extra.append(tangent_case(*case)[-1])
    save_json(COND/'tangent_convergence.json',dict(**IDENTITY,records=extra))

def twa_case(K,E,sigma,launch,dis,n,zmax=100,dt=.02,power=9,loss=0,weyl=True):
    m,a,zs,x,tanrec=tangent_case(K,E,sigma,launch,dis,zmax,dt)
    tag=tanrec['tag']+f'_n{n:g}_p{power}_loss{loss:g}_w{int(weyl)}'
    records=[];allcov=[];allF=[];drifts=[];loss_balances=[]
    for b in range(4):
        path=DATA/(tag+f'_b{b}.npz')
        initial,noise=wigner_initial(a,n,power=power,seed=8701+b)
        if path.exists():fields=np.load(path)['fields']
        else:
            memory_gate();start=time.time();fields=ensemble_run(m,initial,n,zs,dt,sigma,dis,loss,8901+b,weyl)
            np.savez_compressed(path,fields=fields,z=zs)
            print('TWA',tag,'batch',b,'seconds',round(time.time()-start,2),flush=True)
        batch=[];cov=[];Fs=[]
        for z,xi,ff in zip(zs,x,fields):
            if z==0:continue
            t=tangent_observables(xi);r=sample_observables(ff,n,t,noise)
            cov.append(r.pop('V'));Fs.append(r.pop('F'));r.pop('mean_photons')
            r.update(z=float(z),linear_quad=t['lambda_quad'],linear_gen=t['lambda_gen'],linear_own=t['lambda_own'],
                f0=t['f0'],sigma_max=t['sigma_max'],
                ratio=t['sigma_max']**6/(n*t['f0']),own_ratio=t['own'][1,1]**2/(8*n*t['f0']*t['lambda_own']))
            batch.append(r)
        records.append(batch);allcov.append(cov);allF.append(Fs)
        inv0=np.stack([np.sum(abs(initial)**2,axis=1),np.sum(abs(initial)**2*m.q,axis=1)])
        invf=np.stack([np.sum(abs(fields[-1])**2,axis=1),np.sum(abs(fields[-1])**2*m.q,axis=1)])
        drifts.append(np.max(abs(invf-inv0),axis=1))
        eta=np.exp(-loss*zs[-1]);bath=(1-eta)*np.array([m.M,np.sum(m.q)])/(2*n)
        loss_balances.append(np.mean(invf,axis=1)-eta*np.mean(inv0,axis=1)-bath)
    cross=[]
    for j,z in enumerate(zs[zs>0]):
        vals=[];counts=[]
        for b in range(4):
            train=np.mean([allcov[k][j] for k in range(4) if k!=b],axis=0)
            _,u=np.linalg.eigh(train);v=u[:,0];vals.append(float(v@allcov[b][j]@v))
            train=np.mean([allF[k][j] for k in range(4) if k!=b],axis=0)
            _,u=np.linalg.eigh(train);v=u[:,0];counts.append(float(v@allF[b][j]@v))
        cross.append(dict(z=float(z),quad_crossfit=vals,count_crossfit=counts))
    # Realization-wise conservation of Weyl N and E, not covariance of pooled disorder.
    rec=dict(**IDENTITY,K=K,E=E,sigma=sigma,launch=launch,disorder=dis,n=n,zmax=zmax,dt=dt,
             shots=4*2**power,alpha=loss,weyl=weyl,tag=tag,records=records,crossfit=cross,
             max_N_E_drift=np.max(drifts,axis=0),mean_N_E_loss_balance_residuals=loss_balances,
             drift_note='Maximum over all four batches; for alpha>0 the raw drift includes physical loss, while the mean balance subtracts attenuation and Wigner bath vacuum.')
    save_json(RUN/(tag+'.json'),rec);return rec

def twa():
    cases=[(5,.6,.3,4201,7601,n,300 if n==1e10 else 100) for n in [3e5,1e6,3e6,1e8,1e10]]
    cases += [(5,.9,.3,4201,7601,1e10,100),(5,.3,.3,4201,7601,1e8,100),
              (5,.3,.3,4201,7601,1e6,50),(5,.3,.3,4201,7601,1e10,100),
              (5,.6,.3,4202,7602,1e10,100),(4,.45,3,4202,7602,1e10,100),
              (5,.3,3,4202,7602,1e10,100)]
    for case in cases:twa_case(*case)

def convergence():
    for case in [(5,.6,.3,4201,7601,1e10,100),(5,.3,.3,4201,7601,1e8,50),(5,.3,3,4202,7602,1e10,50)]:
        twa_case(*case,dt=.01);twa_case(*case,power=10)
    twa_case(5,.6,.3,4201,7601,1e10,100,weyl=False)

def loss():
    alpha=-np.log(.9)/50
    for dis in range(7601,7605):twa_case(5,.3,3,4201,dis,1e10,50,loss=alpha)
    twa_case(5,.3,3,4201,7601,1e10,50,dt=.01,loss=alpha)

if __name__=='__main__':getattr(sys.modules[__name__],sys.argv[1])()
