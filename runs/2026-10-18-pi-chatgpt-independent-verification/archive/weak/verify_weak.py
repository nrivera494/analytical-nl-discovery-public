#!/usr/bin/env python3
"""Independent weak-dispersion NLSE/Bogoliubov verification.

Author: /root, GPT-6 Astra Pro, 2026-10-18.
No repository solver is imported. Eighth-order periodic finite differences in
time and adaptive DOP853 in distance propagate the classical field and its
real tangent map. Input columns can be restricted to a central interval;
expanding that interval checks the resulting variational upper bound on the
minimum covariance eigenvalue. Shot-noise covariance is the identity.

Equation: u_s = -i*delta*u_xx/2 + i*Phi*abs(u)**2*u.
Usage: OPENBLAS_NUM_THREADS=1 python verify_weak.py --phi 3 --y 1e-4
"""
import argparse
import json
import os
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.integrate import solve_ivp
from scipy.linalg import eigh, eigh_tridiagonal


def laplacian(n, dx):
    coeff = [(-4, -1/560), (-3, 8/315), (-2, -1/5), (-1, 8/5),
             (0, -205/72), (1, 8/5), (2, -1/5), (3, 8/315), (4, -1/560)]
    rows = np.tile(np.arange(n), len(coeff))
    cols = np.concatenate([(np.arange(n)+offset) % n for offset, _ in coeff])
    vals = np.concatenate([np.full(n, c/dx**2) for _, c in coeff])
    return coo_matrix((vals, (rows, cols)), shape=(n,n)).tocsr()


def compute(phi=3., y=1e-4, n=768, half_window=4., support=.7, m=1,
            rtol=2e-10, full=False, save_mode=None):
    started = time.monotonic()
    dx = 2*half_window/n
    x = -half_window + dx*np.arange(n)
    delta = y/phi
    lap = laplacian(n, dx)
    profile = np.exp(-x**(2*m))
    u0 = np.sqrt(profile).astype(complex)

    def mean_rhs(s,u):
        return -.5j*delta*(lap@u) + 1j*phi*np.abs(u)**2*u

    mean = solve_ivp(mean_rhs, (0,1), u0, method='DOP853',
                     rtol=rtol/5, atol=rtol/50, dense_output=True)
    if not mean.success:
        raise RuntimeError(mean.message)
    chosen = np.arange(n) if full else np.flatnonzero(abs(x)<=support+1e-12)
    k = 2*len(chosen)
    tangent0 = np.zeros((2,n,k))
    tangent0[0,chosen,np.arange(len(chosen))] = 1
    tangent0[1,chosen,len(chosen)+np.arange(len(chosen))] = 1

    def tangent_rhs(s, flat):
        t = flat.reshape((2,n,k))
        u = mean.sol(s)
        a,b = u.real, u.imag
        ab = 2*phi*a*b
        out = np.empty_like(t)
        out[0] = .5*delta*(lap@t[1]) - ab[:,None]*t[0] - (phi*(a*a+3*b*b))[:,None]*t[1]
        out[1] = -.5*delta*(lap@t[0]) + (phi*(3*a*a+b*b))[:,None]*t[0] + ab[:,None]*t[1]
        return out.ravel()

    tangent = solve_ivp(tangent_rhs, (0,1), tangent0.ravel(), method='DOP853',
                        rtol=rtol, atol=rtol/30, t_eval=[1.])
    if not tangent.success:
        raise RuntimeError(tangent.message)
    t = tangent.y[:,-1].reshape((2*n,k))
    gram = t.T@t
    eig,v = eigh(gram, subset_by_index=[k-1,k-1], driver='evr')
    sigma2 = float(eig[0])
    lam = 1/sigma2
    vmin = 1/(np.sqrt(1+phi*phi)+phi)**2
    excess = lam/vmin-1
    if m==1:
        pref = np.sqrt(2/3)*phi/np.sqrt(1+phi*phi)
    elif m==2:
        pref = 1.06036209048418*(1/3)**(2/3)*2**(1/3)*phi/np.sqrt(1+phi*phi)
    else:
        sx=np.linspace(-7,7,10001)[1:-1]
        sh=14/10000
        ground=eigh_tridiagonal(2/sh**2+sx**(2*m),np.full(len(sx)-1,-1/sh**2),
                                select='i',select_range=(0,0),eigvals_only=True)[0]
        pref = float(ground)*(1/3)**(m/(m+1))*2**(1/(m+1))*phi/np.sqrt(1+phi*phi)
    prediction = pref*y**(m/(m+1))
    # J times the largest output singular vector is the smallest output
    # singular vector for a full symplectic map. The support error is checked.
    large = (t@v[:,0]/np.sqrt(sigma2)).reshape((2,n))
    small = np.stack([large[1],-large[0]])
    density = np.sum(small*small,axis=0)
    xrms = float(np.sqrt(np.sum(x*x*density)/np.sum(density)))
    # The restricted tangent is a symplectic embedding: T^T J T = J_k.
    jj = np.zeros((k,k))
    kk = k//2
    jj[:kk,kk:] = np.eye(kk)
    jj[kk:,:kk] = -np.eye(kk)
    jdef = t[:n].T@t[n:]-t[n:].T@t[:n]-jj
    result = dict(phi=phi,y=y,delta=delta,m=m,n=n,dx=dx,
                  half_window=half_window,support=support,full=full,input_columns=k,
                  rtol=rtol,lambda_min_upper=lam,vmin=vmin,excess=excess,
                  prediction=prediction,ratio=excess/prediction if prediction else None,
                  xrms=xrms,width_prediction=(y/24)**.25 if m==1 else None,
                  symplectic_max_abs=float(np.max(np.abs(jdef))),
                  mean_energy_relative_error=float(np.sum(np.abs(mean.y[:,-1])**2)/np.sum(profile)-1),
                  mean_nfev=mean.nfev,tangent_nfev=tangent.nfev,
                  runtime_seconds=time.monotonic()-started,
                  numpy=np.__version__,scipy=scipy.__version__)
    if full:
        # Direct minimum of T^T T is an additional check, not the reported
        # estimator; reciprocity avoids subtraction at very small eigenvalues.
        direct=eigh(gram,subset_by_index=[0,0],driver='evr',eigvals_only=True)[0]
        result['direct_lambda_min']=float(direct)
        result['reciprocity_relative_error']=float(direct*sigma2-1)
    if save_mode:
        np.savez_compressed(save_mode,x=x,mean=mean.y[:,-1],mode=small,
                            density=density,input_indices=chosen,input_mode=v[:,0])
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phi',type=float,default=3.)
    parser.add_argument('--y',type=float,default=1e-4)
    parser.add_argument('--n',type=int,default=768)
    parser.add_argument('--half-window',type=float,default=4.)
    parser.add_argument('--support',type=float,default=.7)
    parser.add_argument('--m',type=int,default=1)
    parser.add_argument('--rtol',type=float,default=2e-10)
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--save-mode')
    parser.add_argument('--output')
    args=parser.parse_args()
    opts=vars(args).copy()
    output=opts.pop('output')
    result=compute(**opts)
    txt=json.dumps(result,indent=2)
    if output:
        Path(output).write_text(txt+'\n')
    print(txt,flush=True)


if __name__=='__main__':
    main()
