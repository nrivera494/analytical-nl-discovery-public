#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Actual bright-port two-mode counting observable."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from scipy.special import gammaln,ndtri
from scipy.stats import qmc
RUN=Path(__file__).resolve().parent

def matrix(n,Phi):
    tau=Phi/n
    C=-2*n*np.sin(tau)*np.exp(-4*n*np.sin(tau/2)**2)
    P=1-n*np.expm1(-4*n*np.sin(tau)**2)
    return np.array([[np.ones_like(C),C],[C,P]])

def fixed_number_matrix(N,tau):
    # This stable branch is used only at the very small tau of the high-N mixture.
    C=-(N-1)*np.sin(tau)*np.exp((N-2)*np.log1p(-2*np.sin(tau/2)**2))
    P=1-(N-1)/2*np.expm1((N-2)*np.log1p(-2*np.sin(tau)**2))
    return np.array([[np.ones_like(C),C],[C,P]])

def main():
    memory_gate();fock=[]
    for n in [4,16,64]:
      cut=int(n+12*np.sqrt(n)+30);k=np.arange(cut+1,dtype=float)
      for Phi in [3,10,30,60]:
        a=np.exp(-n/2+k*np.log(n)/2-gammaln(k+1)/2-1j*Phi/n*k*(k-1)/2)
        psi=a[:,None]*a[None,:];psi/=np.linalg.norm(psi)
        Z=(k[:,None]-k[None,:])*psi;Y=np.zeros_like(psi);factor=np.sqrt(k[1:,None]*k[None,1:])
        Y[1:,:-1]+=1j*factor*psi[:-1,1:];Y[:-1,1:]-=1j*factor*psi[1:,:-1]
        V=np.array([[np.vdot(Z,Z).real,np.vdot(Z,Y).real],[np.vdot(Y,Z).real,np.vdot(Y,Y).real]])/(2*n)
        predicted=matrix(n,Phi);fock.append(dict(n_per_arm=n,Phi=Phi,cutoff=cut,matrix=V,exact_formula=predicted,max_error=float(np.max(abs(V-predicted)))))
    fixed=[]
    for N in [8,32,128]:
      k=np.arange(N+1,dtype=float);coef=np.sqrt(k[1:]*(N-k[1:]+1))
      for Phi in [3,10,30,60]:
        tau=2*Phi/N;psi=np.exp(.5*(gammaln(N+1)-gammaln(k+1)-gammaln(N-k+1)-N*np.log(2))-1j*tau/2*(k*(k-1)+(N-k)*(N-k-1)))
        Z=(2*k-N)*psi;Y=np.zeros_like(psi);Y[1:]+=1j*coef*psi[:-1];Y[:-1]-=1j*coef*psi[1:]
        V=np.array([[np.vdot(Z,Z).real,np.vdot(Z,Y).real],[np.vdot(Y,Z).real,np.vdot(Y,Y).real]])/N
        C=-(N-1)*np.sin(tau)*np.cos(tau)**(N-2);P=1+(N-1)/2*(1-np.cos(2*tau)**(N-2));pred=np.array([[1,C],[C,P]])
        fixed.append(dict(N=N,Phi=Phi,matrix=V,formula=pred,max_error=float(np.max(abs(V-pred))),lambda_count=float(np.linalg.eigvalsh(V)[0])))
    rows=[];q=np.array([1,1,2,2,2,3,3,3,3,4,4,4,4,4])
    for n in [1e10,5e9]:
     for kind in ['none','gaussian052','dirichlet']:
      for power in [14,16]:
       for seed in [8891,8892,8893,8894]:
        u=qmc.Sobol(18,scramble=True,seed=seed).random_base2(power)
        if kind=='none':p=np.ones(len(u))
        elif kind=='gaussian052':p=1+np.sqrt(.0026)*ndtri(u[:,0])
        else:
          x=-np.log(u[:,:14]);x/=x.sum(axis=1,keepdims=True);p=(1-.6*np.sum(x/q,axis=1))/(1-.6*np.mean(1/q))
        eps2=float(np.var(p,ddof=1)/np.mean(p)**2);g=ndtri(u[:,14:])
        a=np.sqrt(2*n*p)+(g[:,0]+1j*g[:,1])/2;b=(g[:,2]+1j*g[:,3])/2
        c=(a+b)/np.sqrt(2);d=(a-b)/np.sqrt(2);shot=float(np.mean(abs(c)**2+abs(d)**2)-1)
        for Phi in [3,10,30,60]:
          cp=c*np.exp(-1j*Phi/n*(abs(c)**2-1));dp=d*np.exp(-1j*Phi/n*(abs(d)**2-1))
          Z=abs(cp)**2-abs(dp)**2;Y=-2*np.imag(np.conj(cp)*dp)
          V=(np.cov(np.array([Z,Y]),ddof=1)-np.eye(2)/2)/shot
          V_rescaled=(np.cov(np.array([Z,Y])/np.sqrt(p),ddof=1)-np.eye(2)*np.mean(1/p)/2)/(2*n)
          baseline=matrix(n,Phi);_,vec=np.linalg.eigh(baseline);v=vec[:,0]
          expected=np.mean(matrix(n*p,Phi*p)*p,axis=2)/np.mean(p)
          expected_rescaled=np.mean(matrix(n*p,Phi*p),axis=2)
          NN=np.rint(2*n*p);fixed_N=np.mean(fixed_number_matrix(NN,Phi/n)*NN,axis=2)/np.mean(NN)
          exact=float(v@expected@v);zero=float(np.linalg.eigvalsh(baseline)[0]);observed=float(v@V@v)
          rows.append(dict(n_per_arm=n,n_total_pump=2*n,kind=kind,shots=len(p),seed=seed,Phi=Phi,
            epsilon2=eps2,exact_zero_jitter=zero,exact_mixture_fixed=exact,exact_mixture_optimal=float(np.linalg.eigvalsh(expected)[0]),
            twa_fixed=observed,twa_optimal=float(np.linalg.eigvalsh(V)[0]),expected_floor=zero+eps2,
            exact_shot_rescaled=float(v@expected_rescaled@v),twa_shot_rescaled=float(v@V_rescaled@v),
            fixed_N_shot_rescaled=float(v@np.mean(fixed_number_matrix(NN,Phi/n),axis=2)@v),
            fixed_N_mixture=float(v@fixed_N@v),power_third_central=float(np.mean((p/np.mean(p)-1)**3)),
            jitter_increment_ratio=(exact-zero)/eps2 if eps2 else None))
    save_json(RUN/'sagnac_quantum_reference.json',dict(**IDENTITY,complete=True,observable='Q=cos(theta)(Nc-Nd)+sin(theta)i(cdag d-ddag c), normalized to total shot noise',fock=fock,fixed_number=fixed,rows=rows))
if __name__=='__main__':main()
