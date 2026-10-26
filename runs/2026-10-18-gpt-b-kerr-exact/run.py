#!/usr/bin/env python3
"""gpt-b; gpt-6-astra; gpt. Frozen exact-moment/Fock/TWA benchmark."""
import sys,time,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import memory_gate,save_json,RAW,IDENTITY
from kerr_squeezing import *
from scipy.linalg import expm
from scipy.special import ndtri
from scipy.stats import qmc
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name;DATA.mkdir(exist_ok=True)
FREEZE='9db4bb6a67b640d79365810a984c3af5c6a9da92'

def main():
    memory_gate();start=time.time();rows=[]
    for nu in [1,3,10,30,100]:
      for n in [1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9,1e10,1e12]:
        ex=optimum(n,nu);tw=optimum(n,nu,True);pred=3/(2*4**(1/3))*(nu**4/n)**(1/3)
        rows.append(dict(n=n,nu=nu,exact=ex,twa=tw,prediction=pred,
          error_dB=10*np.log10(ex['lambda']/pred),twa_error_dB=10*np.log10(tw['lambda']/ex['lambda']),
          held_out=nu in [3,30] or n in [1e7,1e9,1e12]))
      print('exact optima nu',nu,flush=True)
    fits=[]
    for nu in [1,3,10,30,100]:
      r=[r for r in rows if r['nu']==nu and r['n'] in [1e6,1e8,1e10]]
      slope,intercept=np.polyfit(np.log([x['n'] for x in r]),np.log([x['exact']['lambda'] for x in r]),1)
      err=[x for x in rows if x['nu']==nu and x['n']>=1e6]
      ep=np.polyfit(np.log([x['n'] for x in err]),np.log([abs(x['exact']['lambda']/x['prediction']-1) for x in err]),1)[0]
      fits.append(dict(nu=nu,exponent=slope,prefactor=np.exp(intercept)/nu**(4/3),relative_error_exponent=ep))
    fixed=[]
    for n in [16,64,256,1024,4096,1e5,1e6,1e7,1e8,1e9]:
      for nu in [1,3]:
       for s in sorted(set([2.,4.,8.,n**(1/6),2*n**(1/6),4*n**(1/6)])):
        ex=moments(n,nu,s);tw=moments(n,nu,s,True);V=tangent(s,nu);e,u=np.linalg.eigh(V);direction=u[:,0]
        exact_dir=float(direction@ex['V']@direction);twa_dir=float(direction@tw['V']@direction)
        fixed.append(dict(n=n,nu=nu,s=s,exact=ex['lambda'],twa=tw['lambda'],linear=e[0],
          exact_fixed=exact_dir,twa_fixed=twa_dir,ratio=float((1/e[0])**3/n) if nu==1 else None,
          fixed_excess=exact_dir/e[0]-1))
    gates=[]
    for n in [1e4,1e6,1e8,1e10]:
     for R in [.08,.8,8,80]:
      sig2=(R*n)**(1/3);s=(np.sqrt(sig2)-1/np.sqrt(sig2))/2
      ex=moments(n,1,s);e,u=np.linalg.eigh(tangent(s));actual=float(u[:,0]@ex['V']@u[:,0])
      gates.append(dict(n=n,R=R,s=s,linear=e[0],exact_fixed=actual,relative_excess=actual/e[0]-1,
                        predicted_excess=R/8))
    save_json(RUN/'exact_summary.json',dict(**IDENTITY,freeze_commit=FREEZE,rows=rows,fits=fits,fixed=fixed,
              gates=gates,wall_seconds=time.time()-start))
    fock=[]
    for n in [4,16,64]:
     for nu in [1,3,10]:
      for extra in [0,30]:
       cutoff=int(n+12*np.sqrt(n*nu+nu**2)+60)+extra
       a=np.diag(np.sqrt(np.arange(1,cutoff)),1);N=np.arange(cutoff)
       D=expm(np.sqrt(n)*(a.T-a));t=(nu-1)/2
       p=(t/(1+t))**N/(1+t) if t else np.r_[1.,np.zeros(cutoff-1)]
       rho=(D*p)@D.T
       for s in [1.,(n/(16*nu))**(1/6),2*n**(1/6)]:
        phase=np.exp(-.5j*s/n*N*(N-1));r=phase[:,None]*rho*phase.conj()[None,:]
        am=np.sum(np.diag(r,1).conj()*np.sqrt(N[1:]));am2=np.sum(np.diag(r,2).conj()*np.sqrt(N[2:]*(N[2:]-1)))
        ni=float(np.sum(N*r.diagonal()).real);l=1+2*(ni-abs(am)**2)-2*abs(am2-am*am)
        ex=moments(n,nu,s)
        fock.append(dict(n=n,nu=nu,s=s,cutoff=cutoff,extra=extra,norm=float(np.trace(r).real),
            exact_fock=l,formula=ex['lambda'],error=l-ex['lambda'],mean_error=abs(am-ex['mean']),a2_error=abs(am2-ex['a2'])))
      print('Fock',n,nu,flush=True)
    save_json(RUN/'fock_summary.json',dict(**IDENTITY,rows=fock))
    qrows=[]
    for n in [16,256,4096]:
     for nu in [1,3]:
      for power in [14,16]:
       for seed in [8611,8612,8613,8614]:
        x=ndtri(qmc.Sobol(2,scramble=True,seed=seed).random_base2(power));a=np.sqrt(n)+(x[:,0]+1j*x[:,1])*np.sqrt(nu)/2
        for s in [n**(1/6),2*n**(1/6)]:
         b=a*np.exp(-1j*s/n*(abs(a)**2-1));d=b-b.mean();v=4*np.cov(np.array([d.real,d.imag]),bias=False)
         qrows.append(dict(n=n,nu=nu,shots=2**power,seed=seed,s=s,lambda_qmc=np.linalg.eigvalsh(v)[0],
               exact=moments(n,nu,s)['lambda'],analytic_twa=moments(n,nu,s,True)['lambda']))
    save_json(RUN/'twa_summary.json',dict(**IDENTITY,rows=qrows))
    print('complete exact benchmark',time.time()-start,flush=True)
if __name__=='__main__':main()
