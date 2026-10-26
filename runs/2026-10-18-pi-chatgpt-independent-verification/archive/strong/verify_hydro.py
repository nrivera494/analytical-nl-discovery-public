#!/usr/bin/env python3
"""Direct epsilon=0 Hamiltonian mean and exact tangent hydrodynamics.

This integrates rho_Z=-(rho S_t)_t, S_Z=-rho-S_t^2/2 and its exact
linearization, with DOP853, a complete odd-sized Fourier grid, no filter,
no perturbed-mean finite differences and no Hermite input truncation.
The conjugate-field phase convention changes C's sign only.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft
from scipy.integrate import solve_ivp
from scipy.linalg import svdvals

def run(n=225,window=16.,targets=(.1,.2,.3,.5,.75),tol=1e-10):
    assert n%2==1,'An odd Fourier grid avoids an unresolved Nyquist derivative.'
    t=(np.arange(n)-(n-1)/2)*window/n
    k=2*np.pi*np.fft.fftfreq(n,d=window/n)
    def D(q):
        return ifft(1j*k[:,None]*fft(q,axis=0),axis=0).real
    r0=np.exp(-t*t);s0=np.zeros(n)
    y0=np.empty((n,2+2*n))
    y0[:,0]=r0;y0[:,1]=s0
    y0[:,2:2+n]=np.diag(2*np.sqrt(r0))
    y0[:,2+n:]=0.
    def rhs(z,y):
        y=y.reshape(n,2+2*n)
        r=y[:,0:1];s=y[:,1:2]
        eta=y[:,2:2+n];psi=y[:,2+n:]
        vel=D(s);dpsi=D(psi)
        out=np.empty_like(y)
        out[:,0:1]=-D(r*vel)
        out[:,1:2]=-r-.5*vel*vel
        out[:,2:2+n]=-D(vel*eta+r*dpsi)
        out[:,2+n:]=-vel*dpsi-eta
        return out.ravel()
    start=time.time()
    sol=solve_ivp(rhs,(0,max(targets)),y0.ravel(),method='DOP853',t_eval=targets,
                  rtol=tol,atol=tol*.1,max_step=.02)
    if not sol.success:raise RuntimeError(sol.message)
    rows=[]
    for j,z in enumerate(sol.t):
        y=sol.y[:,j].reshape(n,2+2*n)
        r=y[:,0]
        C=np.sqrt(np.maximum(r,0))[:,None]*y[:,2+n:]
        sigma=svdvals(C)
        row=dict(Z=float(z),Lambda=float(1/sigma[0]**2),Pi=float(1/sigma[1]**2),
                 sigma1=float(sigma[0]),sigma2=float(sigma[1]),min_rho=float(r.min()))
        if window>=32:
            H=np.empty((n,80));H[:,0]=np.pi**(-.25)*np.exp(-t*t/2)
            H[:,1]=np.sqrt(2)*t*H[:,0]
            for m in range(1,79):
                H[:,m+1]=np.sqrt(2/(m+1))*t*H[:,m]-np.sqrt(m/(m+1))*H[:,m-1]
            H*=np.sqrt(window/n)
            hp=svdvals(C@H)
            row['Hermite80_Lambda']=float(1/hp[0]**2)
            row['Hermite80_Pi']=float(1/hp[1]**2)
            row['Hermite80_Gram_error']=float(np.linalg.norm(H.T@H-np.eye(80),2))
        rows.append(row)
    return dict(n=n,window=window,tolerance=tol,nfev=sol.nfev,elapsed=time.time()-start,rows=rows)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=225)
    ap.add_argument('--window',type=float,default=16.);ap.add_argument('--out',required=True)
    args=ap.parse_args();result=run(args.n,args.window)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
