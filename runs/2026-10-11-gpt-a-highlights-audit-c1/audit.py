"""Independent tangent/adjoint SSFM audit. agent gpt-a; model gpt-6-astra; family gpt.

No proposer implementation is imported. Float64, unitary Fourier operations,
exact differential of each nonlinear substep, no anti-alias attenuation.
"""
import argparse, json, time
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

PROVENANCE = dict(agent="gpt-a", model="gpt-6-astra", family="gpt")

def realify(v):
    return np.concatenate((v.real, v.imag), axis=0)

def complexify(v):
    return v[:v.shape[0]//2] + 1j*v[v.shape[0]//2:]

class Map:
    def __init__(self, N, Z, nt=512, window=24., phase_step=.025,
                 beta_sign=1., beta3=0., chirp=0., shift=0., loss=0.,shape='gaussian',dispersion_step=None):
        self.N, self.Z, self.nt = N, Z, nt
        self.dt = window/nt
        self.t = (np.arange(nt)-nt//2)*self.dt
        self.w = 2*np.pi*np.fft.fftfreq(nt,self.dt)
        self.steps = int(np.ceil(N*Z/phase_step))
        if dispersion_step is not None:
            self.steps=max(self.steps,int(np.ceil(Z/N*np.max(np.abs(beta_sign*self.w**2/2+beta3*self.w**3/6))/dispersion_step)))
        self.h = Z/N/self.steps
        self.L = np.exp((1j*(beta_sign*self.w**2/2+beta3*self.w**3/6)-loss/2)*self.h/2)
        amp={'gaussian':lambda:np.exp(-self.t**2/2),
             'quartic':lambda:np.exp(-self.t**4/2),
             'sech':lambda:1/np.cosh(self.t)}[shape]()
        self.u0 = amp*np.exp(1j*(chirp*self.t**2/2+shift*self.t))
        self.u = self.u0.copy()
        aa,bb=[],[]
        self.mid=[]
        for _ in range(self.steps):
            v=self.lin(self.u)
            self.mid.append(v)
            phi=N*N*self.h*np.abs(v)**2
            rot=np.exp(1j*phi)
            aa.append(rot*(1+1j*phi))
            bb.append(rot*1j*N*N*self.h*v*v)
            self.u=self.lin(rot*v)
        self.a,self.b=np.array(aa),np.array(bb)

    def lin(self,v,adj=False):
        L=self.L.conj() if adj else self.L
        return np.fft.ifft(L.reshape((-1,)+(1,)*(v.ndim-1))*np.fft.fft(v,axis=0),axis=0)

    def tangent(self,v):
        v=complexify(np.asarray(v))
        for a,b in zip(self.a,self.b):
            v=self.lin(v)
            if v.ndim==2:a,b=a[:,None],b[:,None]
            v=self.lin(a*v+b*v.conj())
        return realify(v)

    def adjoint(self,v):
        v=complexify(np.asarray(v))
        for a,b in zip(self.a[::-1],self.b[::-1]):
            v=self.lin(v,True)
            if v.ndim==2:a,b=a[:,None],b[:,None]
            v=self.lin(a.conj()*v+b*v.conj(),True)
        return realify(v)

    def diagnostics(self, eigen=True):
        f0=np.fft.fft(self.u0,norm='ortho'); f=np.fft.fft(self.u,norm='ortho')
        e0=np.vdot(f0,f0).real; e=np.vdot(f,f).real
        c=float(np.sum(self.w*np.abs(f0)**2)/e0)
        q=np.fft.ifft((self.w-c)*f,norm='ortho')
        q0=np.fft.ifft((self.w-c)*f0,norm='ortho')
        bw_in=float(np.vdot(q0,q0).real/e0);bw_out=float(np.vdot(q,q).real/e)
        g=self.adjoint(realify(q))
        F=float(np.sum(g*g)/np.vdot(q,q).real)
        K=float(np.sum(np.abs(self.u0)**4-np.abs(self.u)**4)/e0)
        r=dict(N=self.N,Z=self.Z,nt=self.nt,dt=self.dt,steps=self.steps,h=self.h,
               F_centroid=F,bandwidth_ratio=bw_in/bw_out,
               centroid_relative_error=F/(bw_in/bw_out)-1,
               hamiltonian_bandwidth_relative_error=(bw_in+self.N**2*K)/bw_out-1,
               K=K,energy_relative_error=e/e0-1,
               edge_energy=float(np.sum(np.abs(self.u[np.abs(self.t)>.45*self.nt*self.dt])**2)/e))
        r['maximum_linear_phase_step']=float(np.max(np.abs(np.angle(self.L)))*2)
        rng=np.random.default_rng(20261011)
        x,y=rng.normal(size=(2,2*self.nt))
        r['adjoint_dot_relative_error']=float(abs(np.sum(self.tangent(x)*y)-np.sum(x*self.adjoint(y)))/np.linalg.norm(x)/np.linalg.norm(y))
        if eigen:
            op=LinearOperator((2*self.nt,2*self.nt),matvec=lambda v:self.adjoint(self.tangent(v)),dtype=float)
            ev,vec=eigsh(op,k=2,which='LA',tol=2e-10,v0=x)
            r['lambda_min']=float(1/ev[-1]);r['lambda_2']=float(1/ev[-2])
            r['eigen_residual']=float(np.linalg.norm(op@vec[:,-1]-ev[-1]*vec[:,-1])/ev[-1])
        return r

    def reduced(self):
        phase=np.exp(1j*np.angle(self.u))
        def C(v):
            return (complexify(self.tangent(np.r_[v,np.zeros(self.nt)]))*phase.conj()).imag/self.N
        def CT(v):
            return self.adjoint(realify(1j*phase*v/self.N))[:self.nt]
        op=LinearOperator((self.nt,self.nt),matvec=lambda v:CT(C(v)),dtype=float)
        rng=np.random.default_rng(20261011)
        ev=eigsh(op,k=2,which='LA',tol=1e-11,v0=rng.normal(size=self.nt),return_eigenvectors=False)
        return dict(N=self.N,Z=self.Z,nt=self.nt,steps=self.steps,Lambda=1/ev[-1],Pi=1/ev[-2])

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',default='scaling');p.add_argument('--output',required=True);args=p.parse_args()
    out=dict(provenance=PROVENANCE,mode=args.mode,rows=[]);start=time.time()
    if args.mode=='scaling':
        cases=[dict(N=N,Z=Z,nt=1024 if N>=20 else 512) for Z in [.5,1.5] for N in [8,12,20,32]]
        cases += [dict(N=20,Z=.5,nt=2048,phase_step=.0125),dict(N=20,Z=1.5,nt=2048,phase_step=.0125)]
    elif args.mode=='centroid':
        cases=[dict(N=3,Z=.8,nt=512,beta_sign=s,beta3=b,chirp=.7,shift=1.3) for s in [1,-1] for b in [0,.1]]
    elif args.mode=='reduced':
        cases=[dict(N=N,Z=Z,nt=2048) for Z in [.02,.04,.08,.16] for N in [100,200]]
        cases += [dict(N=N,Z=Z,nt=4096,phase_step=.04) for Z in [.5,1.5] for N in [48,96]]
    else:
        raise ValueError(args.mode)
    for case in cases:
        t=time.time();m=Map(**case);r=m.reduced() if args.mode=='reduced' else m.diagnostics(eigen=args.mode=='scaling');r.update(case);r['wall_seconds']=time.time()-t
        out['rows'].append(r);out['wall_seconds']=time.time()-start
        Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps(r),flush=True)

if __name__=='__main__':main()
