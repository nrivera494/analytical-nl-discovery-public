"""gpt-e / gpt-6-astra / gpt. Full-field gain tangent/ASE spot checks.

Positive-step Strang propagation. White ASE is integrated as exact linear
amplifier kicks on each half-step. Both full vacuum and amplitude-only noise
are contracted backward onto moment readouts; no random sampling is needed.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import sys,json,time,argparse
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'2026-10-19-gpt-e-weak-dispersion'))
from tangent import Flow
RAW=Path('~/analytical-nl-discovery-data')/HERE.name
RAW.mkdir(parents=True,exist_ok=True)

def background(Gamma,tau,chirped):
    def rhs(s,y):return [y[1],2*np.exp(s)/(Gamma**2*y[0]**2)]
    r=solve_ivp(rhs,(0,tau),[1.,1/3 if chirped else 0.],method='DOP853',rtol=2e-13,atol=1e-14)
    a,adot=r.y[:,-1]
    return a,Gamma*adot

def noise_covariance(f,read,nsp=1.):
    b=read.copy();total=np.zeros((b.shape[1],b.shape[1]));intensity=np.zeros_like(total)
    for op in reversed(f.ops):
        if op[0]=='L':
            _,lin,phase=op
            source=(2*nsp-1)*(abs(lin[0])**2-1)
            total += source*(b.conj().T@b).real
            amp=(phase.conj()[:,None]*b).real
            intensity += source*(amp.T@amp)
            b=ifft(fft(b,axis=0)*lin.conj()[:,None],axis=0)
        else:
            _,a,q,k=op;b=q.conj()[:,None]*b
            b += 2*k*a[:,None]*np.imag(a.conj()[:,None]*b)
    total += (b.conj().T@b).real
    amp=(np.exp(-1j*np.angle(f.input))[:,None]*b).real
    intensity += amp.T@amp
    return total,intensity

def case(epsilon=.05,tau=2.,chirped=True,smooth=0.,n=1024,window=16.,steps=1024,nsp=1.):
    start=time.time();Gamma=np.sqrt(18);dt=window/n
    def initial(t):
        w=np.maximum(1-t*t,0) if not smooth else smooth*np.logaddexp(0,(1-t*t)/smooth)
        w*= (4/3)/(np.sum(w)*dt)
        return np.sqrt(w)*np.exp(-1j*(Gamma/3 if chirped else 0)*t*t/(2*epsilon))
    f=Flow(tau/(Gamma*epsilon),epsilon*tau/Gamma,n,window,steps,order=2,initial=initial,gain=tau,save_noise_phases=True)
    a,aprime=background(Gamma,tau,chirped);E=4/3*np.exp(tau);t=f.t;u=f.mean
    ux=ifft(1j*f.w*fft(u))
    # Exact discrete derivative of the current moment. The continuum product
    # rule is unsafe when sharp-edge radiation reaches a periodic boundary.
    rE=2*u*dt;rI2=2*t*t*u*dt
    rJ=1j*epsilon*(t*ux+ifft(1j*f.w*fft(t*u)))*dt
    rn0=2*rE/(3*E);rn2=5*rI2/(a*a*E)-2.5*rn0
    rp2=-5/(3*epsilon*E)*(rJ-aprime/a*rI2)
    rpbar=1j*u*dt/E;rp0=rpbar+rp2/5
    read=np.column_stack([rn0,rn2,rp0,rp2,rpbar])
    full,amp=noise_covariance(f,read,nsp)
    full*= (4/3)/(4*dt);amp*= (4/3)/(4*dt)
    def summarize(C):
        caa=9/4*np.exp(tau)*C[0,0];cpp=4*np.exp(tau)*C[4,4];cap=3*np.exp(tau)*C[0,4]
        eigmax=(caa+cpp+np.hypot(caa-cpp,2*cap))/2
        eigmin=(caa*cpp-cap*cap)/eigmax
        return dict(n0_variance=C[0,0],n2_variance=C[1,1],p0_variance=C[2,2],p2_variance=C[3,3],
            matched_phase_variance=C[4,4],phase_energy_deficit=1-C[0,4]**2/(C[0,0]*C[4,4]),
            CAA=caa,CPP=cpp,CAP=cap,lambda_LO=eigmin)
    out=dict(epsilon=epsilon,tau=tau,chirped=chirped,smoothing=smooth,n=n,window=window,steps=steps,nsp=nsp,
        hydro_width=a,actual_width=np.sqrt(5*np.sum(t*t*abs(u)**2)/np.sum(abs(u)**2)),
        full=summarize(full),intensity_only=summarize(amp),
        exact_CAA=np.exp(tau)+(2*nsp-1)*(np.exp(tau)-1),seconds=time.time()-start,**f.diagnostics())
    print(json.dumps(out),flush=True)
    np.savez_compressed(RAW/f'full_eps{epsilon}_tau{tau}_chirp{chirped}_s{smooth}_n{n}_w{window}_steps{steps}_discrete_readout.npz',t=t,mean=u,covariance=full,intensity_covariance=amp)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--suite',default='main');a=p.parse_args()
    if a.suite=='main':
        cases=[dict(epsilon=e,tau=t,chirped=c) for e in [.1,.05,.025] for t in [2.] for c in [True,False]]
        cases += [dict(epsilon=.05,tau=4.,n=2048,window=24.,steps=2048),
                  dict(smooth=.02),dict(smooth=.05)]
    elif a.suite=='checks':
        cases=[dict(n=2048),dict(n=2048,window=32.),dict(steps=2048),dict(n=2048,steps=4096),
               dict(smooth=.02,n=2048,steps=2048),dict(epsilon=.05,tau=4.,n=2048,window=24.,steps=4096)]
    elif a.suite=='short':cases=[dict(tau=.2,steps=512)]
    elif a.suite=='edge-resolution':
        cases=[dict(n=4096,window=32.,steps=4096),dict(smooth=.02,n=2048,window=32.),
               dict(smooth=.02,chirped=False),dict(smooth=.02,tau=4.,n=2048,window=24.,steps=2048)]
    else:raise ValueError(a.suite)
    rows=[]
    for kw in cases:
        rows.append(case(**kw));(HERE/f'fullfield-{a.suite}.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
