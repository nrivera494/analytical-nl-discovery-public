"""gpt-e / gpt-6-astra / gpt. Independent epsilon=0 hydro tangent map.

rho_Z=-(rho*v)_t, v_Z=-(rho+v^2/2)_t.
dr_Z=-(v*dr)_t+(rho*dtheta_t)_t, dtheta_Z=dr-v*dtheta_t.
Full collocation input basis, without Hermite or peak-mode assumptions.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json,time,argparse
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft,fftfreq
from scipy.integrate import solve_ivp
from scipy.linalg import svdvals
HERE=Path(__file__).resolve().parent;RAW=Path('~/analytical-nl-discovery-data')/HERE.name

def case(n=256,window=12.,rtol=3e-10):
    start=time.time();x=(np.arange(n)-n//2)*window/n;k=2*np.pi*fftfreq(n,window/n)
    rho0=np.exp(-x*x)
    def derivative(f):return ifft(1j*k[(...,)+(None,)*(f.ndim-1)]*fft(f,axis=0),axis=0).real
    dr0=np.diag(2*np.sqrt(rho0));theta0=np.zeros_like(dr0)
    initial=np.r_[rho0,np.zeros(n),dr0.ravel(),theta0.ravel()]
    def rhs(z,y):
        rho=y[:n];v=y[n:2*n];dr=y[2*n:2*n+n*n].reshape(n,n);theta=y[2*n+n*n:].reshape(n,n)
        dtheta=derivative(theta)
        return np.r_[-derivative(rho*v),-derivative(rho+v*v/2),
                     (-derivative(v[:,None]*dr)+derivative(rho[:,None]*dtheta)).ravel(),
                     (dr-v[:,None]*dtheta).ravel()]
    zs=[.1,.45,.9]
    sol=solve_ivp(rhs,(0,zs[-1]),initial,method='DOP853',rtol=rtol,atol=rtol*.05,t_eval=zs)
    if not sol.success:raise RuntimeError(sol.message)
    rows=[]
    for z,y in zip(sol.t,sol.y.T):
        rho=y[:n];v=y[n:2*n];theta=y[2*n+n*n:].reshape(n,n)
        C=np.sqrt(np.maximum(rho,0))[:,None]*theta
        s=svdvals(C)
        row=dict(Z=float(z),n=n,window=window,rtol=rtol,Lambda=float(1/s[0]**2),Pi=float(1/s[1]**2),
            min_density=float(min(rho)),mass_error=float(sum(rho)/sum(rho0)-1),
            max_velocity_gradient=float(max(abs(derivative(v)))))
        rows.append(row)
        np.savez_compressed(RAW/f'hydro_n{n}_w{window}_Z{z}.npz',x=x,rho=rho,v=v,C=C)
    out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',rows=rows,seconds=time.time()-start,nfev=sol.nfev)
    print(json.dumps(out),flush=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=256);p.add_argument('--window',type=float,default=12.);a=p.parse_args()
    result=case(a.n,a.window)
    (HERE/f'hydro-n{a.n}-w{a.window}.json').write_text(json.dumps(result,indent=2)+'\n')
