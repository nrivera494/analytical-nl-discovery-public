"""Independent Fourier-domain dispersionless Raman covariance.
Agent gpt-a; model gpt-6-astra; family gpt. Analytic causal kernel,
symmetrized coth spectrum, physical sampling <= 3 fs. No proposer imports.
"""
import json,time,gc
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
PROVENANCE=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')
def calculate(T0=1000.,Phi=10.,temp=300.,band=None,refine=1,fR=.18,padding=16.):
 start=time.time();nt=2**int(np.ceil(np.log2(padding*T0/2.5)))*refine;dt=padding*T0/nt
 t=(np.arange(nt)-nt//2)*dt;w=2*np.pi*np.fft.fftfreq(nt,dt);p=np.exp(-(t/T0)**2);e=np.sqrt(p)
 a,b=1/32.,1/12.2;h=(a*a+b*b)/(a*a+b*b-w*w+2j*a*w);R=1-fR+fR*h
 def conv(v,k): return np.fft.ifft(np.fft.fft(v,axis=0)*k.reshape((-1,)+(1,)*(v.ndim-1)),axis=0).real
 theta=Phi*conv(p,R);rot=np.exp(1j*theta);u=e*rot
 H=2*np.abs(h.imag)
 if temp>0:
  nz=abs(w)>0;H[nz]/=np.tanh(1.054571817e-34*abs(w[nz])*1e15/(2*1.380649e-23*temp))
  H[0]=8*a*1.380649e-23*temp/(1.054571817e-34*1e15*(a*a+b*b))
 trms=np.sqrt(np.sum(t*t*p)/p.sum());Wb=(1.2*max(abs(np.gradient(theta,dt)))+3/trms) if band is None else band/T0
 ks=np.flatnonzero(abs(w)<=Wb);B=np.exp(1j*np.outer(np.arange(nt),w[ks]*dt))/np.sqrt(nt)
 Q=np.c_[B,1j*B]*rot.conj()[:,None];qr,qi=Q.real,Q.imag
 Ktqi=2*Phi*e[:,None]*conv(e[:,None]*qi,R.conj())
 X=qr+Ktqi;C=X.T@X+qi.T@qi+qi.T@(2*Phi*fR*e[:,None]*conv(e[:,None]*qi,H))
 C=(C+C.T)/2
 ev=eigh(C,subset_by_index=[0,0],check_finite=True)[0][0]
 noise=2*Phi*fR*H[0];slice_value=float(eigh(np.array([[1,2*Phi],[2*Phi,1+4*Phi*Phi+noise]]),eigvals_only=True)[0])
 # Independently evaluate the centroid from the full map and Raman formula.
 alpha=np.fft.fft(u,norm='ortho');q=np.fft.ifft(w*alpha,norm='ortho')*rot.conj();qx=q.real+2*Phi*e*conv(e*q.imag,R.conj());qy=q.imag
 variance=float(np.sum(qx*qx+qy*qy)+np.sum(qy*(2*Phi*fR*e*conv(e*qy,H))))
 shot=float(np.sum(w*w*abs(alpha)**2));pp=np.fft.ifft(1j*w*np.fft.fft(p)).real
 I1=float(np.sum((t/T0**2*e)**2));I2R=float(np.sum(p*conv(pp,R)**2));DR=float(np.sum(p*(conv(pp,R.conj())-conv(pp,R))**2));SR=float(np.sum(pp*conv(pp,H)))
 formula=(I1+Phi**2*DR+Phi*fR*SR/2)/(I1+Phi**2*I2R)
 # Symmetric covariance must satisfy the quantum uncertainty inequality.
 nb=len(ks);Omega=np.block([[np.zeros((nb,nb)),np.eye(nb)],[-np.eye(nb),np.zeros((nb,nb))]])
 qmin=float(eigh(C+1j*Omega,subset_by_index=[0,0],check_finite=True)[0][0])
 row=dict(T0_fs=T0,Phi=Phi,temp_K=temp,nt=nt,dt_fs=dt,window_fs=padding*T0,fR=fR,band_WbT0=float(Wb*T0),spectral_modes=len(ks),lambda_band=float(ev),thermal_slice=slice_value,ratio_to_slice=float(ev/slice_value),H0=float(H[0]),centroid=float(variance/shot),centroid_formula=float(formula),centroid_relative_error=float(variance/shot/formula-1),uncertainty_min_eigenvalue=qmin,wall_seconds=time.time()-start)
 print(json.dumps(row),flush=True);return row
if __name__=='__main__':
 out=dict(provenance=PROVENANCE,rows=[])
 cases=[dict(T0=1000.,Phi=phi,temp=300.) for phi in [5.,10.]]
 cases += [dict(T0=T0,Phi=10.,temp=300.,band=B) for T0 in [200.,1000.] for B in [30.,44.]]
 cases += [dict(T0=1000.,Phi=10.,temp=T) for T in [0.,77.,150.]]
 cases += [dict(T0=1000.,Phi=10.,temp=300.,refine=2)]
 for case in cases:
  out['rows'].append(calculate(**case));Path(__file__).with_name('raman_band.json').write_text(json.dumps(out,indent=2));gc.collect()
