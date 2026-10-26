#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Conditional full-grid certificate for an explicitly stated photon floor."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy import linalg as la,optimize,special

def conditional_bound(a,n,k,floor,betas=(100.,500.,2000.),maxiter=180):
    begun=time.time();x=np.zeros(len(n));best=-np.inf;best_x=x.copy();history=[]
    penalty=n/floor
    for beta in betas:
        def objective(v):
            h=a-k+np.diag(v)
            ev,q=la.eigh(h,check_finite=False)
            weights=np.exp(-beta*(ev-ev[0]));weights/=sum(weights)
            grad=penalty-(q*q)@weights
            val=-ev[0]+special.logsumexp(-beta*(ev-ev[0]))/beta+penalty@v
            return float(val),grad
        r=optimize.minimize(objective,x,jac=True,method='L-BFGS-B',
            bounds=optimize.Bounds(np.zeros(len(n)),np.full(len(n),np.inf)),
            options=dict(maxiter=maxiter,ftol=1e-11,gtol=1e-8,maxcor=8))
        x=np.maximum(r.x,0);eig=float(la.eigh(a-k+np.diag(x),subset_by_index=(0,0),eigvals_only=True)[0]);value=eig-penalty@x
        if value>best:best,best_x=value,x.copy()
        history.append(dict(beta=beta,bound=float(value),iterations=int(r.nit),success=bool(r.success)))
    h=a-k+np.diag(best_x);margin=1e-8*max(1,la.norm(h,np.inf));eig=float(la.eigh(h,subset_by_index=(0,0),eigvals_only=True)[0])-margin
    la.cholesky(h-eig*np.eye(len(n)),lower=True)
    return eig-penalty@best_x,best_x,dict(history=history,margin=margin,seconds=time.time()-begun)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');ap.add_argument('--floor',type=float,default=1e6);args=ap.parse_args()
    path=Path(args.path);d=np.load(path);n=d['nbar'];a=d['V'][:len(n),:len(n)]
    # Use the already saved bright-core covariance dual. It is embedded with
    # zeros into the full matrix, retaining all dark directions for the check.
    corepath=path.with_name(path.stem+'_mf_base.core.npz');cd=np.load(corepath);indices=cd['indices'].astype(int)
    ck=np.load(corepath.with_suffix('.score.npz'))['dual_K'];k=np.zeros_like(a);k[np.ix_(indices,indices)]=ck
    lower,nu,details=conditional_bound(a,n,k,args.floor)
    report=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',label=path.stem,
        photon_floor=args.floor,conditional_linearized_bound=float(lower),details=details,
        caveat='Only bounds masks with coherent photon count at least the stated floor; not the unrestricted optimum.')
    path.with_suffix('.brightness.json').write_text(json.dumps(report,indent=2)+'\n')
    np.savez_compressed(path.with_suffix('.brightness.npz'),dual_K=k,diagonal_multipliers=nu)
    print(json.dumps(report),flush=True)
