#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Controlled phase-only and extracted-mode tests."""
import sys,time,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from squeezing import *
from scipy.integrate import cumulative_simpson
from scipy.optimize import minimize_scalar
import mpmath as mp
mp.mp.dps=60
RUN=Path(__file__).resolve().parent;GRIN=RUN.parent/'2026-10-18-gpt-b-grin-squeezing';DATA=RAW/GRIN.name

def spm():
    memory_gate();m=Model(5);a=m.launch(.3,4201);records=[]
    ensemble=json.loads((RUN/'ensemble_summary.json').read_text())['records']
    for sigma in [.3,3]:
      for dis in range(7601,7613 if sigma==.3 else 7607):
        for sample in ([.1,.02] if sigma==.3 and dis==7601 else [.1]):
          out=m.run(a,zmax=100,dt=.02,sigma=sigma,seed=dis,block=sample,sample=sample)
          phi=cumulative_simpson(abs(out['checkpoints'][:,0])**2,x=out['z'],initial=0)
          tan=next(r for r in ensemble if r['E']==.3 and r['sigma']==sigma and r['launch']==4201 and r['disorder']==dis)
          for z in [5,10,20,50,100]:
            j=round(z/sample);r=next(r for r in tan['rows'] if r['z']==z);ph=float(phi[j])
            # Independent scalar path and tangent base must describe the same noise realization.
            snap=np.load(r['raw_file']) if 'raw_file' in r else None
            records.append(dict(sigma=sigma,disorder=dis,sample=sample,z=z,Phi_self=ph,VP=r['own'][1][1],SPM_reference_fraction=(1+4*ph*ph)/r['own'][1][1],f0=abs(out['checkpoints'][j,0])**2,tangent_f0=r['f0']))
    save_json(RUN/'spm_reference.json',dict(**IDENTITY,rows=records))

def diagonal():
    memory_gate();m=Model(5);a=m.launch(.3,4201);p=abs(a)**2;c=np.array([m.tensor[0,j,0,j] for j in range(m.M)]);rows=[]
    for n in [1e4,1e6,1e10]:
      for z in [5,10,20,50]:
        nn=mp.mpf(str(n));zz=mp.mpf(str(z));p0=mp.mpf(str(p[0]));k=zz/nn
        def mom(r):
          log=nn*p0*mp.expm1(-1j*r*k)-1j*k*r*(r-1)/2
          for j in range(1,len(p)):log+=nn*mp.mpf(str(p[j]))*mp.expm1(-2j*r*k*mp.mpf(str(c[j])))
          return (nn*p0)**(mp.mpf(r)/2)*mp.exp(log)
        def twmom(r):
          D=1+1j*r*k/2
          ans=(nn*p0)**(mp.mpf(r)/2)*D**(-r-1)*mp.exp(-1j*r*k*nn*p0/D+1j*r*k*(1+sum(mp.mpf(str(v)) for v in c[1:])))
          for jj in range(1,len(p)):
            cj=mp.mpf(str(c[jj]));dj=1+1j*r*k*cj
            ans*=dj**(-1)*mp.exp(-2j*r*k*cj*nn*mp.mpf(str(p[jj]))/dj)
          return ans
        ta=twmom(1);tb=twmom(2);twa_lambda=float(1+2*(nn*p0-abs(ta)**2)-2*abs(tb-ta*ta))
        am=mom(1);a2=mom(2);A=1+2*(nn*p0-abs(am)**2);B=(a2-am*am)*mp.exp(-2j*mp.arg(am));V=np.array([[float(A+2*mp.re(B)),float(2*mp.im(B))],[float(2*mp.im(B)),float(A-2*mp.re(B))]])
        cloud=16*z*z*p[0]*np.sum(c[1:]**2*p[1:]);L=np.array([[1,-2*z*p[0]],[-2*z*p[0],1+4*z*z*p[0]**2+cloud]])
        e,u=np.linalg.eigh(L);quad=float(u[:,0]@V@u[:,0]);rows.append(dict(n=n,z=z,exact=float(A-2*abs(B)),analytic_twa=twa_lambda,tangent=e[0],exact_fixed=quad,excess=quad-e[0],conditional_phase=1+cloud,SPM_VP=1+4*z*z*p[0]**2,full_VP=L[1,1]))
    save_json(RUN/'diagonal_mechanism.json',dict(**IDENTITY,rows=rows))

def extracted():
    memory_gate();records=[]
    cases=[(.3,.3,4201,7601,1e10,100),(.3,.3,4201,7601,1e8,100),(.6,.3,4201,7601,1e10,300),(.3,3,4202,7602,1e10,100)]
    for E,sigma,launch,dis,n,zmax in cases:
      tag=f'K5_E{E:g}_s{sigma:g}_l{launch}_d{dis}_h0.02_z{zmax:g}'
      tan=np.load(DATA/(tag+'_tangent.npz'));zs=tan['z'];x=tan['x'];batches=[np.load(DATA/(tag+f'_n{n:g}_p9_loss0_w1_b{b}.npz'))['fields'] for b in range(4)]
      for z in [10,20,50]:
        j=int(np.flatnonzero(zs==z)[0]);t=tangent_observables(x[j]);n0=n*t['f0'];nu=t['nu'];samples=[np.sqrt(n)*b[j,:,0]*np.exp(-1j*np.angle(x[j,0,0])) for b in batches]
        pred=3/(2*4**(1/3))*(nu**4/n0)**(1/3);cross=[]
        def cv(a,Phi):
          b=a*np.exp(-1j*Phi/n0*(abs(a)**2-1));d=b-b.mean();return 4*np.cov(np.array([d.real,d.imag]),ddof=1)
        for hold in range(4):
          train=np.concatenate([samples[b] for b in range(4) if b!=hold]);grid=np.r_[0,np.geomspace(.01,300,129)];vals=[np.linalg.eigvalsh(cv(train,p))[0] for p in grid];k=int(np.argmin(vals));Phi=grid[k]
          if 0<k<len(grid)-1:
            opt=minimize_scalar(lambda p:np.linalg.eigvalsh(cv(train,p))[0],bounds=(grid[k-1],grid[k+1]),method='bounded');Phi=opt.x
          ev,u=np.linalg.eigh(cv(train,Phi));v=u[:,0];test=float(v@cv(samples[hold],Phi)@v)
          cross.append(dict(Phi=Phi,train=ev[0],test=test))
        records.append(dict(E=E,sigma=sigma,launch=launch,disorder=dis,n=n,z=z,n0=n0,nu=nu,prediction=pred,Gaussian_input_ratio=t['own'][1,1]**2/(.8*t['lambda_own']*n0),crossfit=cross,
           mean=float(np.mean([c['test'] for c in cross])),se=float(np.std([c['test'] for c in cross],ddof=1)/2),raw_tag=tag))
    save_json(RUN/'extracted_stage.json',dict(**IDENTITY,rows=records))
if __name__=='__main__':getattr(sys.modules[__name__],sys.argv[1])()
