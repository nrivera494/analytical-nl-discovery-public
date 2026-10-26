"""gpt-e / gpt-6-astra / gpt. Exact shear, finite bands, vector tests."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import json,time,argparse
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft,fftfreq
from scipy.linalg import eigvalsh
from scipy.integrate import solve_ivp
from tangent import Flow,kerr_anchor

HERE=Path(__file__).resolve().parent

def real_band(t,B):
    n=len(t);W=(t[1]-t[0])*n
    k=np.arange(1,int(np.floor(B*W/(2*np.pi)))+1)
    return np.column_stack([np.ones(n)/np.sqrt(n),
        np.sqrt(2/n)*np.cos(2*np.pi*t[:,None]*k/W),
        np.sqrt(2/n)*np.sin(2*np.pi*t[:,None]*k/W)])

def band_covariance(flow,B):
    basis=real_band(flow.t,B);out=np.column_stack([basis,1j*basis])
    adj=flow.adjoint(out)
    gram=(adj.conj().T@adj).real
    return float(eigvalsh(gram,subset_by_index=[0,0])[0]),basis.shape[1]

def raman(phi,T0=200.,B=30.,n=2048,W=12.,T=300.,frame='physical'):
    t=(np.arange(n)-n//2)*W/n;w=2*np.pi*fftfreq(n,W/n)/T0
    a=1/32.;b=1/12.2;f=.18
    h=(a*a+b*b)/((a+1j*w)**2+b*b)
    R=1-f+f*h
    kBT_hbar=1.380649e-23*T/1.054571817e-34*1e-15
    H=np.zeros(n)
    if T:
        nz=w!=0;H[nz]=2*abs(h[nz].imag)/np.tanh(abs(w[nz])/(2*kBT_hbar));H[0]=8*a*kBT_hbar/(a*a+b*b)
    else:H=2*abs(h.imag)
    p=np.exp(-t*t);root=np.sqrt(p)
    def conv(x,transfer):return ifft(fft(x,axis=0)*transfer[(...,)+(None,)*(x.ndim-1)],axis=0).real
    def K(x,transpose=False):return 2*phi*root[:,None]*conv(root[:,None]*x,R.conj() if transpose else R)
    def noise(x):return 2*phi*f*root[:,None]*conv(root[:,None]*x,H)
    basis=real_band(t,B);q=np.column_stack([basis,1j*basis])
    if frame=='physical':q=q*np.exp(-1j*phi*conv(p,R))[:,None]
    x=q.real;y=q.imag
    adjx=x+K(y,True)
    V=adjx.T@adjx+y.T@y+y.T@noise(y)
    V=(V+V.T)/2
    lam=float(eigvalsh(V,subset_by_index=[0,0])[0])
    sliceV=np.array([[1,2*phi],[2*phi,1+4*phi*phi+2*phi*f*H[0]]])
    sli=float(np.linalg.eigvalsh(sliceV)[0])
    return dict(phi=phi,T0_fs=T0,B=B,n=n,window=W,T_K=T,frame=frame,lambda_min=lam,
                slice=sli,relative_excess=lam/sli-1,H0=float(H[0]),band_modes=basis.shape[1])

def vector(phi,chi,strong=False):
    a0=np.array([np.cos(chi),1j*np.sin(chi)])
    S=np.column_stack([np.eye(2),1j*np.eye(2)])
    y0=np.column_stack([a0,S]).ravel()
    def rhs(z,y):
        mat=y.reshape(2,5);a=mat[:,0];d=mat[:,1:];b=a[::-1];db=d[::-1]
        intensity=abs(a)**2;di=2*np.real(a.conj()[:,None]*d)
        q=intensity+2*intensity[::-1]/3
        f=q*a;df=q[:,None]*d+(di+2*di[::-1]/3)*a[:,None]
        if not strong:
            f+=b*b*a.conj()/3
            df+=(2*b[:,None]*db*a.conj()[:,None]+b[:,None]**2*d.conj())/3
        return (1j*phi*np.column_stack([f,df])).ravel()
    sol=solve_ivp(rhs,(0,1),y0,method='DOP853',rtol=2e-12,atol=2e-13)
    end=sol.y[:,-1].reshape(2,5);M=np.concatenate([end[:,1:].real,end[:,1:].imag])
    lam=np.linalg.svd(M,compute_uv=False)[-1]**2
    if strong:pe=phi/2*(1+np.sqrt(1-20*np.cos(chi)**2*np.sin(chi)**2/9))
    else:pe=phi/3*(1+np.sqrt(1+3*np.cos(2*chi)**2))
    return dict(phi=phi,chi=chi,strong_birefringence=strong,lambda_min=lam,prediction=kerr_anchor(pe),relative_error=lam/kerr_anchor(pe)-1)

def shear_random():
    rng=np.random.default_rng(191006);K=rng.normal(size=(12,12))
    I=np.eye(len(K));V=np.block([[I,K.T],[K,I+K@K.T]])
    lam=np.linalg.eigvalsh(V)[0];pred=kerr_anchor(np.linalg.svd(K,compute_uv=False)[0]/2)
    return dict(lambda_min=lam,prediction=pred,relative_error=lam/pred-1)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--suite',default='raman');args=parser.parse_args()
    rows=[]
    if args.suite=='raman':
        cases=[dict(T0=T0,B=B) for T0 in [200.,1000.,5000.] for B in [15.,30.,60.]]
        cases += [dict(T0=200.,B=30.,n=4096),dict(T0=200.,B=30.,n=4096,W=24.),
                  dict(T0=200.,B=30.,frame='local'),dict(T0=5000.,B=60.,T=0.)]
        for kw in cases:
            row=raman(10.,**kw);rows.append(row);print(json.dumps(row),flush=True)
    elif args.suite=='bands':
        for B in [8.,16.,32.]:
            for y in [0.,1e-6,1e-4,1e-2]:
                f=Flow(7.,y/7,n=1024,window=12.,steps=32)
                lam,m=band_covariance(f,B)
                row=dict(phi=7.,B=B,y=y,lambda_min=lam,relative_excess=lam/kerr_anchor(7.)-1,band_modes=m)
                rows.append(row);print(json.dumps(row),flush=True)
    elif args.suite=='vector':
        rows=[shear_random()]
        for phi in [.3,7.,17.]:
            for chi in [0.,.23,np.pi/4]:
                for strong in [False,True]:rows.append(vector(phi,chi,strong))
        print(json.dumps(rows),flush=True)
    (HERE/f'{args.suite}.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
