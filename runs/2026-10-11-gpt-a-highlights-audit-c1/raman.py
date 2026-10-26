"""Independent covariance injection; gpt-a, gpt-6-astra, gpt.

Analytic Fourier transform of the response (no sampled Raman kernel).
The mean and tangent remain Kerr-only, as in the audited reservoir-only claim.
"""
import json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from audit import Map,realify,complexify,PROVENANCE

def spectrum(w,T0=1e-12,temp=300.):
    a,b=1/32e-15,1/12.2e-15
    om=np.abs(w)/T0
    out=np.full_like(om,4*a*.18*1.380649e-23*temp/(1.054571817e-34*(a*a+b*b)))
    nz=om>0
    x=om[nz]
    im=.18*(a*a+b*b)*2*a*x/((a*a+b*b-x*x)**2+4*a*a*x*x)
    out[nz]=im/np.tanh(1.054571817e-34*x/(2*1.380649e-23*temp))
    return out

def calculate(nt,phase_step,every,T0=1e-12):
    start=time.time();N=10.;Z=N*.7/np.sqrt(4*N*N*np.exp(-1.5)-1)
    m=Map(N,Z,nt=nt,window=24,phase_step=phase_step)
    J=np.eye(2*nt);W=np.zeros_like(J);ch=spectrum(m.w,T0)
    slices=list(range(0,m.steps+1,every))
    if slices[-1]!=m.steps:slices.append(m.steps)
    weights=np.zeros(len(slices)); dz=np.diff(slices)*m.h
    weights[:-1]+=dz/2;weights[1:]+=dz/2;weight=dict(zip(slices,weights))
    def add(u,J,w):
        # Inverse of a symplectic real Jacobian, no numerical matrix inversion.
        X=np.block([[J[nt:,nt:].T,-J[:nt,nt:].T],[-J[nt:,:nt].T,J[:nt,:nt].T]])
        E=-X[:,:nt]*u.imag[None,:]+X[:,nt:]*u.real[None,:]
        ER=np.fft.ifft(ch[None,:]*np.fft.fft(E,axis=1),axis=1).real
        return 4*N*N*w*(ER@E.T)
    W+=add(m.u0,J,weight[0])
    for k,(a,b,mid) in enumerate(zip(m.a,m.b,m.mid),1):
        d=m.lin(complexify(J));J=realify(m.lin(a[:,None]*d+b[:,None]*d.conj()))
        if k in weight:
            u=m.lin(np.exp(1j*N*N*m.h*np.abs(mid)**2)*mid)
            W+=add(u,J,weight[k])
    V=J@J.T; VR=J@W@J.T
    lk=float(eigh(V,subset_by_index=[0,0],driver='evr',check_finite=False)[0][0])
    lt=float(eigh(V+VR,subset_by_index=[0,0],driver='evr',check_finite=False)[0][0])
    r=dict(N=N,Z=Z,Phi=N*Z,nt=nt,window=24,phase_step=phase_step,every=every,
           T0_fs=T0*1e15,chat0=float(ch[0]),lambda_kerr=lk,lambda_total=lt,
           rho_measured=(lt-lk)*N*Z/ch[0],wall_seconds=time.time()-start)
    raw=Path('~/analytical-nl-discovery-data/2026-10-11-gpt-a-highlights-audit-c1');raw.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(raw/f'raman_nt{nt}_step{phase_step}_every{every}.npz',V=V,VR=VR,u=m.u,t=m.t)
    return r

if __name__=='__main__':
    out=dict(provenance=PROVENANCE,rows=[])
    for spec in [(256,.025,8),(512,.0125,8),(512,.0125,4)]:
        r=calculate(*spec);out['rows'].append(r);print(json.dumps(r),flush=True)
        Path(__file__).with_name('raman.json').write_text(json.dumps(out,indent=2))
