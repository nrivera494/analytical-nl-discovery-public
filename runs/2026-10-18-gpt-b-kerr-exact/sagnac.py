#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Exact conditional-arm Sagnac and Wigner check."""
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from kerr_squeezing import moments,tangent
from scipy.special import ndtri,gammaln
from scipy.stats import qmc,poisson,binom
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def main():
    memory_gate();rows=[];n=1e10
    # Deterministic quadrature of classical shot distribution, preserving vacuum quantum covariance exactly.
    for kind in ['none','gaussian02','gaussian052','gaussian10','dirichlet']:
      u=qmc.Sobol(14,scramble=True,seed=8801).random_base2(10)
      if kind=='dirichlet':
        x=-np.log(u);x/=x.sum(axis=1,keepdims=True);q=np.array([1,1,2,2,2,3,3,3,3,4,4,4,4,4]);power=1-.6*np.sum(x/q,axis=1);power/=1-.6*np.mean(1/q)
      elif kind=='none':power=np.ones(len(u))
      else:power=1+float(kind[8:])/100*ndtri(u[:,0]) if kind!='gaussian052' else 1+np.sqrt(.0026)*ndtri(u[:,0])
      eps2=float(np.var(power,ddof=1))
      for Phi in [3,10,30,60]:
        reference=moments(n,1,Phi);_,vec=np.linalg.eigh(reference['V']);v=vec[:,0]
        covs=[];fixed=[]
        for p in power:
          r=moments(n*p,1,Phi*p);covs.append(r['V'])
          angle=r['phase']-reference['phase'];R=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
          fixed.append(R@r['V']@R.T)
        V=np.mean(covs,axis=0);F=np.mean(fixed,axis=0)
        rows.append(dict(kind=kind,Phi=Phi,n_per_arm=n,epsilon2=eps2,exact_coherent=reference['lambda'],
          tangent_coherent=np.linalg.eigvalsh(tangent(Phi))[0],tracking_fixed=float(v@V@v),tracking_optimized=np.linalg.eigvalsh(V)[0],
          laboratory_fixed=float(v@F@v),laboratory_optimized=np.linalg.eigvalsh(F)[0],
          predicted=reference['lambda']+eps2,global_phase_average=float(np.trace(V)/2),
          exact_average_dark_photons=float((np.trace(V)-2)/4)))
      print('exact Sagnac',kind,flush=True)
    save_json(RUN/'sagnac_exact.json',dict(**IDENTITY,rows=rows))
    qrows=[]
    for kind in ['none','gaussian052','dirichlet']:
     for pp in [14,16]:
      for seed in [8811,8812,8813,8814]:
       u=qmc.Sobol(18,scramble=True,seed=seed).random_base2(pp)
       if kind=='none':power=np.ones(len(u))
       elif kind=='gaussian052':power=1+np.sqrt(.0026)*ndtri(u[:,0])
       else:
        x=-np.log(u[:,:14]);x/=x.sum(axis=1,keepdims=True);q=np.array([1,1,2,2,2,3,3,3,3,4,4,4,4,4]);power=(1-.6*np.sum(x/q,axis=1))/(1-.6*np.mean(1/q))
       g=ndtri(u[:,14:]);a=np.sqrt(2*n*power)+(g[:,0]+1j*g[:,1])/2;b=(g[:,2]+1j*g[:,3])/2
       c=(a+b)/np.sqrt(2);d=(a-b)/np.sqrt(2)
       for Phi in [3,30,60]:
        cp=c*np.exp(-1j*Phi/n*(abs(c)**2-1));dp=d*np.exp(-1j*Phi/n*(abs(d)**2-1));dark=(cp-dp)/np.sqrt(2)
        # LO follows classical shot mean; quantum mean phase shift is O(Phi/n).
        dark*=np.exp(1j*Phi*power);r=2*np.column_stack([dark.real,dark.imag]);V=np.cov(r,rowvar=False,ddof=1)
        ref=moments(n,1,Phi);_,vec=np.linalg.eigh(ref['V']);v=vec[:,0]
        qrows.append(dict(kind=kind,shots=2**pp,seed=seed,Phi=Phi,tracking_fixed=float(v@V@v),optimized=np.linalg.eigvalsh(V)[0]))
    save_json(RUN/'sagnac_twa.json',dict(**IDENTITY,rows=qrows))
    # No-go checks, exact diagonal unitary: arbitrary populations, all phases/angles.
    k=np.arange(251);distributions={'poisson':poisson.pmf(k,10),'thermal':.9**k/10,
      'number_mixture':.5*(k==0)+.5*(k==10),'smooth_superpoisson':.5*poisson.pmf(k,1)+.5*binom.pmf(k,50,.6)}
    no=[]
    for name,p in distributions.items():
      p/=p.sum();mean=float(k@p);var=float((k*k)@p-mean**2)
      residual=(k[1:-1]+1)*p[:-2]*p[2:]-k[1:-1]*p[1:-1]**2
      no.append(dict(name=name,mean=mean,number_variance=var,quadrature_variance=1+2*mean,
                     minimum_mixed_poisson_logconvex_residual=float(residual.min()),
                     violates_positive_P_necessary_condition=bool(residual.min()<-1e-12)))
    save_json(RUN/'no_go.json',dict(**IDENTITY,rows=no))
if __name__=='__main__':main()
