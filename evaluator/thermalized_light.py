#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt; 2026-10-17.

Independent finite HG Galerkin model and reference measures. All modal
indices are Cartesian (nx,ny), ordered by nx+ny, then nx. No imported
proposer implementation. The only approximation to the tensor is a
quadrature exact for its polynomial degree, checked at doubled order.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS', '1')
os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/gpt-b-matplotlib')
from pathlib import Path
import ctypes as ct
import hashlib
import json
import math
import subprocess
import time
import numpy as np
from scipy.special import eval_hermite, factorial
from numpy.polynomial.hermite import hermgauss

ROOT=Path(__file__).resolve().parents[1]
RAW=Path('~/analytical-nl-discovery-data')
IDENTITY=dict(agent='gpt-b',model='gpt-6-astra',family='gpt')

def memory_gate():
    result=subprocess.check_output(['memory_pressure'],text=True)
    line=next(s for s in result.splitlines() if 'free percentage' in s)
    print(line,flush=True)
    percent=int(line.split(':')[-1].strip().rstrip('%'))
    if percent<35: raise RuntimeError('Less than 35% memory free; defer launch.')

def library():
    src=ROOT/'evaluator/thermalized_light_core.c'
    digest=hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    dest=Path('/private/tmp')/f'gpt-b-thermal-{digest}.dylib'
    if not dest.exists():
        subprocess.run(['clang','-O3','-std=c11','-fPIC','-shared',str(src),'-o',str(dest)],check=True)
    lib=ct.CDLL(str(dest))
    ip=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
    dp=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
    zp=np.ctypeslib.ndpointer(dtype=np.complex128,flags='C_CONTIGUOUS')
    lib.tl_rhs.argtypes=[ct.c_int,ct.c_int,ip,ip,ip,ip,dp,ct.c_int,zp,zp]
    lib.tl_run.argtypes=[ct.c_int,ct.c_int,ip,ip,ip,ip,dp,ip,zp,zp,
                         ct.c_double,ct.c_int,ct.c_int,ct.c_int,ct.c_double,
                         ct.c_uint64,dp,zp,dp]
    lib.tl_run.restype=ct.c_int
    lib.tl_mcmc.argtypes=[ct.c_int,ct.c_int,ip,ip,ip,ip,dp,ip,zp,zp,
                         ct.c_double,ct.c_double,ct.c_double,ct.c_double,ct.c_double,
                         ct.c_int,ct.c_int,ct.c_uint64,dp,dp]
    lib.tl_mcmc.restype=ct.c_int
    lib.tl_ensemble.argtypes=[ct.c_int,ct.c_int,ip,ip,ip,ip,dp,ip,zp,zp,
                         ct.c_int,ct.c_double,ct.c_int,ct.c_int,ct.c_double,ct.c_uint64,ct.c_int,dp]
    lib.tl_lyapunov.argtypes=[ct.c_int,ct.c_int,ip,ip,ip,ip,dp,ip,zp,
                         ct.c_double,ct.c_int,ct.c_int,ct.c_double,ct.c_double,ct.c_uint64,ct.c_int,dp]
    return lib

class Model:
    def __init__(self,K,quadrature=None,resonant=True):
        self.K=K
        self.modes=[(nx,q-nx) for q in range(K) for nx in range(q+1)]
        self.q=np.array([sum(t) for t in self.modes],dtype=np.int32)
        self.M=len(self.q)
        x,w=hermgauss(quadrature or (2*K+2))
        # Four normalized oscillator functions: polynomial * exp(-2 x^2).
        pol=np.array([eval_hermite(n,x/np.sqrt(2))/np.sqrt(2.**n*factorial(n))
                      for n in range(K)])
        t=np.einsum('ai,bi,ci,di,i->abcd',pol,pol,pol,pol,w,optimize=True)
        t/=np.sqrt(2)*np.pi
        ix=np.array([m[0] for m in self.modes]);iy=np.array([m[1] for m in self.modes])
        self.tensor=t[np.ix_(ix,ix,ix,ix)]*t[np.ix_(iy,iy,iy,iy)]
        self.tensor/=self.tensor[0,0,0,0]
        if resonant:
            self.tensor*=((self.q[:,None,None,None]+self.q[None,:,None,None])==
                          (self.q[None,None,:,None]+self.q[None,None,None,:]))
        self.tensor[abs(self.tensor)<2e-14]=0
        self.p,self.r=np.triu_indices(self.M)
        self.p=self.p.astype(np.int32);self.r=self.r.astype(np.int32)
        pair=self.tensor[self.p[:,None],self.r[:,None],self.p[None,:],self.r[None,:]]
        pair*=np.where(self.p==self.r,1.,2.)[None,:]
        row,col=np.nonzero(pair)
        self.column=np.asarray(col,dtype=np.int32)
        self.offset=np.r_[0,np.cumsum(np.bincount(row,minlength=len(self.p)))].astype(np.int32)
        self.value=np.asarray(pair[row,col],dtype=np.float64)
        self.L=np.zeros((self.M,self.M),complex)
        self.X=np.zeros_like(self.L);self.Y=np.zeros_like(self.L);self.B=np.zeros_like(self.L)
        lookup={t:j for j,t in enumerate(self.modes)}
        for j,(nx,ny) in enumerate(self.modes):
            if (nx+1,ny-1) in lookup:
                self.L[lookup[nx+1,ny-1],j]=-1j*np.sqrt((nx+1)*ny)
            if (nx-1,ny+1) in lookup:
                self.L[lookup[nx-1,ny+1],j]=1j*np.sqrt(nx*(ny+1))
            for mat,target,coef in [(self.X,(nx-1,ny),np.sqrt(nx)),
                                    (self.Y,(nx,ny-1),np.sqrt(ny)),
                                    (self.B,(nx-2,ny),np.sqrt(nx*max(nx-1,0))),
                                    (self.B,(nx,ny-2),np.sqrt(ny*max(ny-1,0)))]:
                if target in lookup:mat[lookup[target],j]+=coef
        self.lib=library()

    def rhs(self,a):
        a=np.ascontiguousarray(a,dtype=np.complex128)
        shape=a.shape;a=a.reshape(-1,self.M);out=np.empty_like(a)
        self.lib.tl_rhs(self.M,len(self.p),self.p,self.r,self.offset,self.column,self.value,
                        len(a),a,out)
        return out.reshape(shape)

    def invariants(self,a):
        p=abs(a)**2
        h=(np.conj(a)*1j*self.rhs(a)).sum(axis=-1).real/2
        l=np.einsum('...i,ij,...j->...',np.conj(a),self.L,a).real
        return np.stack([p.sum(axis=-1),np.sum(p*self.q,axis=-1),h,l],axis=-1)

    def launch(self,E,seed=4101,groups=(1,2),aligned=False):
        p=np.zeros(self.M)
        for q in groups:p[self.q==q]=E/(len(groups)*q*(q+1))
        p[0]=1-p.sum()
        if p[0]<0:raise ValueError('Invalid launch')
        phases=np.zeros(self.M) if aligned else np.random.default_rng(seed).uniform(0,2*np.pi,self.M)
        return np.sqrt(p)*np.exp(1j*phases)

    def run(self,a,zmax=8000,dt=.04,sigma=.3,seed=7101,block=100,sample=1):
        args=[zmax/dt,sample/dt,block/dt,zmax/block]
        if not all(abs(x-round(x))<1e-7 for x in args):raise ValueError('Noninteger grid')
        a=np.array(a,dtype=complex,order='C',copy=True)
        moments=np.zeros((round(zmax/block),1+self.M+self.M**2))
        checkpoints=np.zeros((round(zmax/block)+1,self.M),complex)
        checks=np.zeros(12)
        start=time.time()
        rc=self.lib.tl_run(self.M,len(self.p),self.p,self.r,self.offset,self.column,
             self.value,self.q,self.L,a,dt,round(zmax/dt),round(sample/dt),round(block/dt),
             sigma,seed,moments,checkpoints,checks)
        if rc:raise RuntimeError(f'Non-finite trajectory at step {rc}')
        return dict(moments=moments,checkpoints=checkpoints,checks=checks,
                    z=np.arange(round(zmax/block)+1)*block,wall_seconds=time.time()-start)

    def mcmc(self,a,E,H,L,dh,dl,steps=1000000,block=10000,seed=9101):
        a=np.array(a,dtype=complex,order='C',copy=True)
        blocks=np.zeros((steps//block,4));diagnostics=np.zeros(6)
        self.lib.tl_mcmc(self.M,len(self.p),self.p,self.r,self.offset,self.column,
            self.value,self.q,self.L,a,E,H,L,dh,dl,steps,block,seed,blocks,diagnostics)
        return a,blocks/block,diagnostics

    def ensemble(self,a,n,zmax=1200,dt=.04,sample=1,sigma=.3,seed=7501):
        if dt not in [.04,.02]:raise ValueError('Brownian grid supports 0.04 and its 0.02 refinement')
        a=np.array(a,dtype=complex,order='C',copy=True)
        out=np.zeros((round(zmax/sample)+1,6*self.M))
        linear=np.ascontiguousarray(np.einsum('pqqs->ps',self.tensor)/n,dtype=complex)
        self.lib.tl_ensemble(self.M,len(self.p),self.p,self.r,self.offset,self.column,
             self.value,self.q,linear,a,len(a),dt,round(zmax/dt),round(sample/dt),sigma,seed,round(.04/dt),out)
        return out,a

    def lyapunov(self,a,zmax=8000,dt=.04,epsilon=1e-7,sigma=.3,seed=7501):
        if dt not in [.04,.02]:raise ValueError('Brownian grid supports 0.04 and its 0.02 refinement')
        rng=np.random.default_rng(9401)
        d=rng.normal(size=self.M)+1j*rng.normal(size=self.M);d*=epsilon/np.linalg.norm(d)
        aa=np.ascontiguousarray(np.stack([a,a+d]));out=np.zeros(round(zmax))
        self.lib.tl_lyapunov(self.M,len(self.p),self.p,self.r,self.offset,self.column,
             self.value,self.q,aa,dt,round(zmax/dt),round(1/dt),epsilon,sigma,seed,round(.04/dt),out)
        return out

def dirichlet_moments(q,E,N=1):
    q=np.asarray(q)[1:];D=len(q);w=1/q
    ex=E*w/D
    cov=E*E/(D*D*(D+1))*(D*np.diag(w*w)-np.outer(w,w))
    full=np.empty((D+1,D+1));full[1:,1:]=cov
    full[0,1:]=full[1:,0]=-cov.sum(axis=0);full[0,0]=cov.sum()
    mean=np.r_[N-ex.sum(),ex]
    return dict(mean=mean,cov=full,second=full+np.outer(mean,mean),
                g2=2*D/(D+1),cross=D/(D+1))

def reflection_sector(parent):
    """Canonical isometry onto fields even under x<->y; no trajectory projection."""
    import copy
    columns=[];seen=set()
    for j,(nx,ny) in enumerate(parent.modes):
        if j in seen:continue
        k=parent.modes.index((ny,nx));v=np.zeros(parent.M)
        if j==k:v[j]=1.
        else:v[j]=v[k]=1/np.sqrt(2)
        columns.append(v);seen.update([j,k])
    U=np.array(columns).T;m=copy.copy(parent);m.M=U.shape[1]
    m.tensor=np.einsum('pi,qj,rk,sl,pqrs->ijkl',U,U,U,U,parent.tensor,optimize=True)
    m.tensor[abs(m.tensor)<2e-14]=0
    m.q=np.rint(np.einsum('pi,p,pi->i',U,parent.q,U)).astype(np.int32)
    for name in ['L','X','Y','B']:
        setattr(m,name,np.ascontiguousarray(np.einsum('pi,pq,qj->ij',U,getattr(parent,name),U),dtype=complex))
    m.p,m.r=np.triu_indices(m.M);m.p=m.p.astype(np.int32);m.r=m.r.astype(np.int32)
    pair=m.tensor[m.p[:,None],m.r[:,None],m.p[None,:],m.r[None,:]]
    pair*=np.where(m.p==m.r,1.,2.)[None,:]
    row,col=np.nonzero(pair);m.column=np.asarray(col,dtype=np.int32)
    m.offset=np.r_[0,np.cumsum(np.bincount(row,minlength=len(m.p)))].astype(np.int32)
    m.value=np.asarray(pair[row,col],dtype=float)
    return m,U

def shell_samples(model,E,n,rng,d0=1):
    x=rng.exponential(size=(n,model.M-1));x/=x.sum(axis=1,keepdims=True)
    ex=E*x/model.q[1:];i0=1-ex.sum(axis=1)
    keep=i0>=0
    if d0>1:keep &= rng.random(n)<np.maximum(i0,0)**(d0-1)
    powers=np.column_stack([i0,ex])[keep]
    return np.sqrt(powers)*np.exp(2j*np.pi*rng.random(powers.shape))

def unpack(moments,M):
    sums=np.sum(moments,axis=0);n=sums[0]
    mean=sums[1:1+M]/n;second=sums[1+M:].reshape(M,M)/n
    cov=second-np.outer(mean,mean)
    return dict(mean=mean,cov=cov,g2=np.diag(second)/mean**2,
                cross=second/np.outer(mean,mean),samples=n)

def serializable(obj):
    if isinstance(obj,np.ndarray):return obj.tolist()
    if isinstance(obj,np.generic):return obj.item()
    if isinstance(obj,dict):return {k:serializable(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [serializable(v) for v in obj]
    return obj

def save_json(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(serializable(obj),indent=2,allow_nan=False)+'\n')
