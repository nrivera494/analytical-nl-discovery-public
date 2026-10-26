#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Scope test for a nu-only post-Kerr formula."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from kerr_squeezing import optimum
from scipy.special import ndtri
from scipy.stats import qmc
from scipy.linalg import expm
RUN=Path(__file__).resolve().parent

def main():
    memory_gate();rows=[];n=1e10
    for nu in [1,10]:
     for vx0,vp0 in [(1e4,1e-4),(1,1),(1e-3,1e3)]:
      vx,vp=nu*vx0,nu*vp0;lam=min(vx,vp);pred=3/(2*4**(1/3))*(nu**4/n)**(1/3)
      for power in [16,18]:
       for seed in [8841,8842,8843,8844]:
        x=ndtri(qmc.Sobol(2,scramble=True,seed=seed).random_base2(power));a=np.sqrt(n)+(np.sqrt(vx)*x[:,0]+1j*np.sqrt(vp)*x[:,1])/2
        phis=np.r_[0,np.geomspace(.001,10000,129)];values=[]
        for Phi in phis:
          b=a*np.exp(-1j*Phi/n*(abs(a)**2-1));d=b-b.mean();V=4*np.cov(np.array([d.real,d.imag]),ddof=1);values.append(np.linalg.eigvalsh(V)[0])
        j=int(np.argmin(values));rows.append(dict(n=n,nu=nu,VX=vx,VP=vp,shots=2**power,seed=seed,
           initial_exact=lam,prediction=pred,card_gaussian_bound=vp**2/(.8*lam*n),card_VP_bound=vp/(4*n*nu**2)**(1/3),
           best=values[j],Phi=phis[j],zero_qmc=values[0]))
      print('Gaussian edge',nu,vx,vp,flush=True)
    save_json(RUN/'gaussian_edges.json',dict(**IDENTITY,rows=rows,freeze='e221a59c026e933deafe1ba16a12123eaca4f110'))
    rows=[];n=16
    for vx,vp in [(4,.25),(.25,4)]:
     for extra in [0,40]:
      cut=int(n+12*np.sqrt(n*max(vx,vp))+60)+extra;a=np.diag(np.sqrt(np.arange(1,cut)),1);N=np.arange(cut);r=-.5*np.log(vx)
      D=expm(np.sqrt(n)*(a.T-a));S=expm(.5*r*(a@a-a.T@a.T));psi=D@S[:,0]
      for s in [0,.5,1,2,4]:
        v=psi*np.exp(-.5j*s/n*N*(N-1));am=np.sum(v[:-1].conj()*v[1:]*np.sqrt(N[1:]));a2=np.sum(v[:-2].conj()*v[2:]*np.sqrt(N[2:]*(N[2:]-1)));mean=float(N@abs(v)**2)
        rows.append(dict(n=n,VX=vx,VP=vp,extra=extra,cutoff=cut,s=s,norm=float(np.vdot(v,v).real),lambda_fock=float(1+2*(mean-abs(am)**2)-2*abs(a2-am*am))))
    save_json(RUN/'gaussian_edges_fock.json',dict(**IDENTITY,rows=rows))
if __name__=='__main__':main()
