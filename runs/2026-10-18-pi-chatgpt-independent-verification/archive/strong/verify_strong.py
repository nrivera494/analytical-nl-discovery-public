#!/usr/bin/env python3
"""Independent all-grid Bogoliubov propagation for semiclassical defocusing NLS.

Equation: u_Z = -i/(2N) u_tt + i N |u|^2 u, u(0,t)=exp(-t^2/2).
Method: fourth-order Yoshida composition of exact dispersion and Kerr flows.
The exact derivative and its real Euclidean adjoint are applied, never finite
differences of perturbed means. Every discrete tangent map is symplectic.
Vacuum covariance is I in real/imaginary grid quadratures; the common dt norm
factor cancels from singular values. FFTs are unitary (norm='ortho').

The smallest covariance eigenvalues are obtained as reciprocals of the largest
ones, using symplectic reciprocity. This avoids cancellation when squeezing is
strong. The optional dense check directly diagonalizes S S^T and verifies this.
"""
import argparse
import json
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import time
from pathlib import Path
import numpy as np
from scipy.fft import fft, ifft
from scipy.sparse.linalg import LinearOperator, eigsh


class TangentFlow:
    def __init__(self, N, Z, n=256, window=16.0, steps=200):
        self.N, self.Z, self.n, self.window, self.steps = N,Z,n,window,steps
        self.t = np.arange(n)*window/n-window/2
        self.k = 2*np.pi*np.fft.fftfreq(n,d=window/n)
        self.u0 = np.exp(-self.t**2/2).astype(complex)
        self.stages = []
        u = self.u0.copy()
        h=Z/steps
        w=1/(2-2**(1/3)); weights=(w, -2**(1/3)*w, w)
        # Store individual exact stages. Means are stored only for Kerr maps.
        for _ in range(steps):
            for weight in weights:
                ds=weight*h
                phase=np.exp(1j*self.k**2*ds/(4*N))
                self.stages.append(('L',phase))
                u=ifft(phase*fft(u,norm='ortho'),norm='ortho')
                a=N*ds
                rotation=np.exp(1j*a*np.abs(u)**2)
                self.stages.append(('K',(u.copy(),a,rotation)))
                u=rotation*u
                self.stages.append(('L',phase))
                u=ifft(phase*fft(u,norm='ortho'),norm='ortho')
        self.u=u
        self.out_phase=np.exp(1j*np.angle(u))

    @staticmethod
    def _expand(v,ndim):
        return v if ndim==1 else v[:,None]

    def forward(self,du):
        du=np.asarray(du,dtype=complex).copy()
        ndim=du.ndim
        for kind,data in self.stages:
            if kind=='L':
                p=self._expand(data,ndim)
                du=ifft(p*fft(du,axis=0,norm='ortho'),axis=0,norm='ortho')
            else:
                u,a,r=data
                u=self._expand(u,ndim);r=self._expand(r,ndim)
                du=r*(du+2j*a*u*np.real(u.conj()*du))
        return du

    def adjoint(self,w):
        w=np.asarray(w,dtype=complex).copy()
        ndim=w.ndim
        for kind,data in reversed(self.stages):
            if kind=='L':
                p=self._expand(data,ndim)
                w=ifft(p.conj()*fft(w,axis=0,norm='ortho'),axis=0,norm='ortho')
            else:
                u,a,r=data
                u=self._expand(u,ndim);r=self._expand(r,ndim)
                w=r.conj()*w
                w=w+2*a*u*np.imag(u.conj()*w)
        return w

    def real_forward(self,v):
        u=self.forward(v[:self.n]+1j*v[self.n:])
        return np.concatenate((u.real,u.imag),axis=0)

    def real_adjoint(self,v):
        u=self.adjoint(v[:self.n]+1j*v[self.n:])
        return np.concatenate((u.real,u.imag),axis=0)

    def covariance(self,v):
        return self.real_forward(self.real_adjoint(v))

    def c_forward(self,x):
        return np.imag(self.out_phase.conj()*self.forward(x))/self.N

    def c_adjoint(self,y):
        return self.adjoint(1j*self.out_phase*y).real/self.N

    def a_forward(self,x):
        return np.real(self.out_phase.conj()*self.forward(x))

    def a_adjoint(self,y):
        return self.adjoint(self.out_phase*y).real

    def diagnostics(self):
        rng=np.random.default_rng(21010)
        p=rng.normal(size=self.n)+1j*rng.normal(size=self.n)
        q=rng.normal(size=self.n)+1j*rng.normal(size=self.n)
        fp,fq=self.forward(p),self.forward(q)
        aq=self.adjoint(q)
        adjerr=abs(np.vdot(q,fp).real-np.vdot(aq,p).real)/(np.linalg.norm(q)*np.linalg.norm(fp))
        symerr=abs(np.vdot(fp,fq).imag-np.vdot(p,q).imag)/(np.linalg.norm(p)*np.linalg.norm(q))
        # Exact number conservation implies S^T u_out = u_in.
        numerr=np.linalg.norm(self.adjoint(self.u)-self.u0)/np.linalg.norm(self.u0)
        fhat=fft(self.u,norm='ortho')
        edge=abs(self.k)>0.8*np.max(abs(self.k))
        return dict(adjoint_relative_error=float(adjerr),symplectic_bilinear_error=float(symerr),
                    number_gradient_error=float(numerr),mean_norm_error=float(abs(np.vdot(self.u,self.u).real/np.vdot(self.u0,self.u0).real-1)),
                    spectral_edge_energy_fraction=float(np.sum(abs(fhat[edge])**2)/np.sum(abs(fhat)**2)))


def calculate(N,Z,n,window,steps,neigs=3,dense=False):
    start=time.time()
    flow=TangentFlow(N,Z,n,window,steps)
    op=LinearOperator((2*n,2*n),matvec=flow.covariance,dtype=float)
    seed=np.random.default_rng(733).normal(size=2*n)
    vals,vecs=eigsh(op,k=neigs,which='LA',tol=1e-10,v0=seed,ncv=min(40,2*n))
    order=np.argsort(vals)[::-1];vals=vals[order];vecs=vecs[:,order]
    # J maps every anti-squeezed eigenvector to its reciprocal eigenvector.
    low=np.concatenate((vecs[n:],-vecs[:n]),axis=0)
    lambdas=1/vals
    # Grid parity is t -> -t, with index zero its periodic partner.
    parity=np.mod(-np.arange(n),n)
    pvals=np.sum(low[:n]*low[:n][parity]+low[n:]*low[n:][parity],axis=0)
    phase_dir=np.r_[-flow.u.imag,flow.u.real]
    phase_dir/=np.linalg.norm(phase_dir)
    gphase_overlaps=phase_dir@low
    cop=LinearOperator((n,n),matvec=lambda x:flow.c_adjoint(flow.c_forward(x)),dtype=float)
    csq,cvecs=eigsh(cop,k=neigs,which='LA',tol=1e-10,v0=seed[:n],ncv=min(30,n))
    corder=np.argsort(csq)[::-1];csq=csq[corder];cvecs=cvecs[:,corder]
    aop=LinearOperator((n,n),matvec=lambda x:flow.a_adjoint(flow.a_forward(x)),dtype=float)
    asq=eigsh(aop,k=1,which='LA',tol=1e-8,v0=seed[:n],return_eigenvectors=False)[0]
    res=dict(N=N,Z=Z,Phi=N*Z,n=n,window=window,steps=steps,
             lambda_min=float(lambdas[0]),lambda_2=float(lambdas[1]),
             N2_lambda_min=float(N*N*lambdas[0]),N2_lambda_2=float(N*N*lambdas[1]),
             Lambda_C=float(1/csq[0]),Pi_C=float(1/csq[1]),
             delta_to_C=float(N*N*lambdas[0]*csq[0]-1),
             largest_amplitude_singular=float(np.sqrt(asq)),
             low_eigenvector_parities=pvals.tolist(),global_phase_overlaps=gphase_overlaps.tolist(),
             most_squeezed_mode_t_rms=float(np.sqrt(np.sum(flow.t**2*(low[:n,0]**2+low[n:,0]**2)))),
             c_input_t_rms=float(np.sqrt(np.sum(flow.t**2*cvecs[:,0]**2))),
             diagnostics=flow.diagnostics())
    # Direct Rayleigh verifies physical covariance, independent of reciprocation.
    res['direct_minimum_rayleigh']=float(np.dot(low[:,0],flow.covariance(low[:,0])))
    res['reciprocity_relative_error']=float(res['direct_minimum_rayleigh']/lambdas[0]-1)
    if dense:
        M=flow.real_forward(np.eye(2*n));V=M@M.T
        evals,evecs=np.linalg.eigh(V)
        # Exact orthogonal projection of the global phase hyperplane, QR basis.
        from scipy.linalg import null_space
        Q=null_space(phase_dir[None,:])
        lpass=np.linalg.eigvalsh(Q.T@V@Q)[0]
        J=np.block([[np.zeros((n,n)),np.eye(n)],[-np.eye(n),np.zeros((n,n))]])
        res.update(dense_lambda_min=float(evals[0]),dense_lambda_2=float(evals[1]),
                   lambda_pass=float(lpass),lambda_pass_over_second=float(lpass/evals[1]),
                   dense_symplectic_relative_error=float(np.linalg.norm(M.T@J@M-J,'fro')/np.linalg.norm(J,'fro')))
    res['elapsed_seconds']=time.time()-start
    return res,flow,low,cvecs


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--N',type=float,required=True);ap.add_argument('--Z',type=float,required=True)
    ap.add_argument('--n',type=int,default=256);ap.add_argument('--window',type=float,default=16.)
    ap.add_argument('--steps',type=int,default=200);ap.add_argument('--dense',action='store_true')
    ap.add_argument('--out',type=str,required=True)
    args=ap.parse_args()
    res,flow,low,cvecs=calculate(args.N,args.Z,args.n,args.window,args.steps,dense=args.dense)
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(res,indent=2)+'\n')
    np.savez_compressed(path.with_suffix('.npz'),t=flow.t,u=flow.u,low_modes=low,c_input_modes=cvecs)
    print(json.dumps(res,indent=2),flush=True)
