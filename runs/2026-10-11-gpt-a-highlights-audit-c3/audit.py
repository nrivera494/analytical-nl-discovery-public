"""Independent dispersion/parity/polarization checks; gpt-a, gpt-6-astra, gpt."""
import argparse,json,sys,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'2026-10-11-gpt-a-highlights-audit-c1'))
from audit import Map,PROVENANCE,realify

def vmin(phi):return 1/(np.sqrt(1+phi*phi)+phi)**2

def dispersion():
    destination=Path(__file__).with_name('dispersion.json')
    out=json.loads(destination.read_text()) if destination.exists() else dict(provenance=PROVENANCE,rows=[])
    done={(r['shape'],r['Phi'],r['y'],r['nt'],r['phase_step']) for r in out['rows']}
    cases=[(shape,phi,y,4096 if y<=1e-4 else 1024,.025) for shape in ['gaussian','quartic'] for phi in [2,5,10,20] for y in [1e-6,4e-6,1e-5,4e-5,1e-4,.001,.01]]
    cases += [('gaussian',5,1e-6,8192,.0125),('gaussian',5,.01,2048,.0125),('quartic',5,1e-6,8192,.0125)]
    for shape,phi,y,nt,step in cases:
        if (shape,phi,y,nt,step) in done: continue
        start=time.time();Z=np.sqrt(y);N=phi/Z
        m=Map(N,Z,nt=nt,window=16.,phase_step=step,shape=shape,dispersion_step=.25)
        r=m.diagnostics();ratio=r['lambda_min']/vmin(phi)-1
        pref=phi/np.sqrt(1+phi*phi)*(np.sqrt(2/3) if shape=='gaussian' else .64226)
        power=.5 if shape=='gaussian' else 2/3
        row=dict(shape=shape,Phi=phi,y=y,nt=nt,phase_step=step,lambda_min=r['lambda_min'],
                 relative_excess=ratio,predicted_excess=pref*y**power,
                 prefactor_ratio=ratio/(pref*y**power),eigen_residual=r['eigen_residual'],steps=m.steps,
                 wall_seconds=time.time()-start)
        out['rows'].append(row);Path(__file__).with_name('dispersion.json').write_text(json.dumps(out,indent=2));print(json.dumps(row),flush=True)

def algebra():
    rng=np.random.default_rng(20261011);out=dict(provenance=PROVENANCE)
    # Complete enumeration of binary masks plus random nonnegative weights.
    misses=[];minmargin=float('inf');ncase=500
    for case in range(ncase):
        n=8;P=np.eye(n)[::-1];X=rng.normal(size=(n,n));A=X@X.T+.01*np.eye(n);A=(A+P@A@P)/2
        even=(np.eye(n)[:,:n//2]+np.eye(n)[:,::-1][:,:n//2])/np.sqrt(2)
        odd=(np.eye(n)[:,:n//2]-np.eye(n)[:,::-1][:,:n//2])/np.sqrt(2)
        le=float(eigh(even.T@A@even,eigvals_only=True)[0]);lo=float(eigh(odd.T@A@odd,eigvals_only=True)[0])
        bound=(lo+le)/2 if lo<=le else le
        Y=np.array([[(k>>j)&1 for j in range(n)] for k in range(1,2**n)],float).T
        Y=np.c_[Y,np.exp(rng.normal(size=(n,100)))]
        f=np.sum(Y*(A@Y),axis=0)/np.sum(Y*Y,axis=0)
        margin=float(f.min()-bound);minmargin=min(minmargin,margin)
        if margin < -1e-10:misses.append([case,margin])
    out['parity_rayleigh']=dict(covariances=ncase,binary_masks_per_covariance=255,nonnegative_weights_per_covariance=100,min_margin=minmargin,violations=misses)
    # Physical attenuator adds independent port vacuum; its denominator is linear in T.
    v=np.array([1.,-2.,1.])/np.sqrt(6);A=np.eye(3)+6*np.outer(v,v)
    B=A[np.ix_([0,2],[0,2])];T=np.array([.25,0.]);le,lo=3.,1.
    F=1+float(T@(B-np.eye(2))@T/T.sum())
    V=np.block([[A,np.zeros_like(A)],[np.zeros_like(A),np.linalg.inv(A)]])
    Omega=np.block([[np.zeros_like(A),np.eye(3)],[-np.eye(3),np.zeros_like(A)]])
    out['physical_attenuator_counterexample']=dict(A=A.tolist(),mean_photons=[1000000]*3,B=[0,2],T=T.tolist(),lambda_even=le,lambda_odd=lo,F_par=2.,physical_F=F,
      total_count_F=float(np.ones(3)@A@np.ones(3)/3),uncertainty_min_eig=float(eigh(V+1j*Omega,eigvals_only=True)[0]),corrected_bound='min(1,F_par)')
    actual_kerr=[]
    for nt in [256,512,1024]:
        window=24.;phi=5.;t=(np.arange(nt)-nt//2)*window/nt;u0=np.exp(-t*t/2)
        rot=np.exp(1j*phi*u0*u0);u=u0*rot;a=rot*(1+1j*phi*u0*u0);b=rot*1j*phi*u0*u0
        J=np.fft.fft(np.c_[np.diag(a+b),1j*np.diag(a-b)],axis=0,norm='ortho');alpha=np.fft.fft(u,norm='ortho')
        idx=[1,nt-1];Q=(alpha[idx].conj()[:,None]*J[idx]/np.abs(alpha[idx,None])).real;B=Q@Q.T
        le=float((B[0,0]+B[1,1]+2*B[0,1])/2);lo=float((B[0,0]+B[1,1]-2*B[0,1])/2)
        bound=(le+lo)/2 if lo<=le else le;physical=1+.25*(B[0,0]-1)
        actual_kerr.append(dict(nt=nt,window=window,Phi=phi,bin_detunings=[2*np.pi/window,-2*np.pi/window],
          relative_bin_brightness=float(abs(alpha[1])**2/max(abs(alpha)**2)),T=[.25,0.],V_amp=B.tolist(),lambda_even=le,lambda_odd=lo,F_par=bound,physical_F=float(physical)))
    out['physical_attenuator_Kerr_counterexample']=actual_kerr
    shear=[]
    for n in [2,7,19]:
        K=rng.normal(size=(n,n));S=np.block([[np.eye(n),np.zeros((n,n))],[K,np.eye(n)]]);V=S@S.T
        s=np.linalg.svd(K,compute_uv=False)[0];actual=eigh(V,eigvals_only=True)[0]
        shear.append(dict(n=n,actual=float(actual),formula=vmin(s/2),relative_error=float(actual/vmin(s/2)-1)))
    out['arbitrary_shear']=shear
    polarization=[]
    for regime in ['isotropic','birefringent']:
      for phi in [1,5,20]:
       for angle in [0,np.pi/8,np.pi/4]:
        if regime=='isotropic':
            u=np.array([(np.cos(angle)+np.sin(angle))/np.sqrt(2),(np.cos(angle)-np.sin(angle))/np.sqrt(2)],complex)
            alpha=2/3;cross=2.;eff=phi/3*(1+np.sqrt(1+3*np.cos(2*angle)**2))
        else:
            u=np.array([np.cos(angle),np.sin(angle)],complex);alpha=1.;cross=2/3
            eff=phi/2*(1+np.sqrt(1-20/9*abs(u[0]*u[1])**2))
        def flow(a):return a*np.exp(1j*phi*alpha*(np.abs(a)**2+cross*np.abs(a[::-1])**2))
        ds=[np.array([1,0]),np.array([0,1]),np.array([1j,0]),np.array([0,1j])]
        J=np.column_stack([realify((flow(u+1e-6*d)-flow(u-1e-6*d))/2e-6) for d in ds])
        actual=1/np.linalg.svd(J,compute_uv=False)[0]**2
        polarization.append(dict(regime=regime,Phi=phi,angle=float(angle),effective_Phi=float(eff),lambda_min=float(actual),relative_error=float(actual/vmin(eff)-1)))
    out['polarization']=polarization
    Path(__file__).with_name('algebra.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode');args=p.parse_args()
    {'dispersion':dispersion,'algebra':algebra}[args.mode]()
