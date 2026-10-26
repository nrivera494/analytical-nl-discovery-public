"""gpt-e / gpt-6-astra / gpt: factors, physical covariance, oscillator constants."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft,fftfreq
from scipy.linalg import expm,eigh_tridiagonal,eigvalsh
from tangent import kerr_anchor
HERE=Path(__file__).resolve().parent
cw=[]
for phi in [.03,.25,2.,7.,40.]:
    for detuning in [1e-7,1e-6]:
        S=expm(np.array([[0.,-detuning],[detuning+2*phi,0.]]))
        lam=np.linalg.svd(S,compute_uv=False)[-1]**2
        expected=2/3*detuning*phi**2/np.sqrt(1+phi**2)
        cw.append(dict(phi=phi,aL=detuning,excess=lam/kerr_anchor(phi)-1,prediction=expected))
osc=[]
for n in [2048,4096]:
    dx=20/(n+1);x=-10+np.arange(1,n+1)*dx
    for m in [1,2,3]:
        e=eigh_tridiagonal(2/dx**2+x**(2*m),np.full(n-1,-1/dx**2),select='i',select_range=(0,0),eigvals_only=True)[0]
        osc.append(dict(n=n,peak_order=2*m,ground_energy=float(e)))
quantum=[]
n=128;window=12.;T0=200.;phi=7.;fr=.18;t=(np.arange(n)-n//2)*window/n
w=2*np.pi*fftfreq(n,window/n)/T0;a=1/32.;b=1/12.2
h=(a*a+b*b)/((a+1j*w)**2+b*b);R=1-fr+fr*h
p=np.exp(-t*t);root=np.sqrt(p);I=np.eye(n)
K=2*phi*root[:,None]*ifft(fft(root[:,None]*I,axis=0)*R[:,None],axis=0).real
J=np.block([[np.zeros_like(I),I],[-I,np.zeros_like(I)]])
for temp in [0.,300.]:
    H=2*abs(h.imag)
    if temp:
        kth=1.380649e-23*temp/1.054571817e-34*1e-15
        H[1:]/=np.tanh(abs(w[1:])/(2*kth));H[0]=8*a*kth/(a*a+b*b)
    noise=2*phi*fr*root[:,None]*ifft(fft(root[:,None]*I,axis=0)*H[:,None],axis=0).real
    V=np.block([[I,K.T],[K,I+K@K.T+noise]])
    quantum.append(dict(T_K=temp,min_uncertainty_eigenvalue=float(eigvalsh(V+1j*J,subset_by_index=[0,0])[0]),
        min_covariance_eigenvalue=float(eigvalsh(V,subset_by_index=[0,0])[0])))
out=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',cw=cw,oscillators=osc,quantum=quantum)
(HERE/'cheap.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out),flush=True)
