#!/usr/bin/env python3
"""Independent scalar GNLSE and two-sided ZS shooting. gpt-a/gpt-6-astra/gpt."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import argparse, json, time, pathlib, math
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.optimize import root
from scipy.signal import find_peaks, resample
from scipy.integrate import cumulative_trapezoid
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('~/analytical-nl-discovery-data')/HERE.name
SOURCE=HERE.parent/'2026-10-16-claude-a-raman-soliton-frontier'
MASKS={'A2':'h4grad_N4_T100_maskA2_coef.csv','A':'h4grad_N4_T100_maskA_coef.csv','B':'h4_adjoint_N4_T200_bestmask_coef.csv'}

def coefficients(name):
    if name=='TL': return np.zeros(1)
    if name in MASKS:
        c=np.loadtxt(SOURCE/MASKS[name]).reshape(-1)
        if name=='B': c=c*(-1.)**np.arange(2,len(c)+2)
        return c
    return np.loadtxt(name,delimiter=',').reshape(-1)

def basis(k,n,cutoff,smooth=False):
    x=k/cutoff
    if smooth:
        # C2 continuation: identity below .95, constant beyond 1.05.
        # The transition matches value, first and second derivatives at both ends.
        a=abs(x);r=np.clip((a-.95)/.1,0,1)
        y=.95+.1*r-.1*r**3+.05*r**4
        x=np.sign(x)*np.where(a<.95,a,np.where(a>1.05,1.,y))
    else:x=np.clip(x,-1,1)
    return np.polynomial.legendre.legvander(x,n+1)[:,2:]

def initial(t,N,mask='TL',T0=200.,Tref=None,smooth_mask=False):
    dt=t[1]-t[0]; k=2*np.pi*fftfreq(len(t),dt)
    c=coefficients(mask); base=1/np.cosh(t); Q=fft(base)
    # Discrete support matches the operational definition in the claim.
    cutoff=np.max(abs(k)[abs(Q)>1e-4*np.max(abs(Q))])
    if mask != "TL": cutoff=2*np.pi  # source width 160 and optimization width 80
    if Tref is not None: cutoff*=T0/Tref
    u=ifft(Q*np.exp(1j*np.sum(basis(k,len(c),cutoff,smooth=smooth_mask)*c,axis=1)))
    return u, cutoff

def dispersion(k,T0,d3=0.,curve=False,published=False):
    if published:
        Tps=T0*.001
        betas={2:-21.61,3:.125,4:-3.99e-4,5:1.99e-6}
        return sum(v*(-k/Tps)**j/math.factorial(j)*Tps*Tps/21.61 for j,v in betas.items())
    if not curve: return -.5*k*k-d3*k**3
    # Representative G.652/SMF-28 zero-dispersion-slope model, not sample data.
    # D(lambda)=S0/4 (lambda-lambda_zd^4/lambda^3), lambda in nm.
    c=299792.458 # nm/ps
    w0=2*np.pi*c/1550.; w=w0-k/(T0*.001)
    lam=2*np.pi*c/np.maximum(w,w0*.1)
    D=.086/4*(lam-1310.**4/lam**3) # ps/(nm km)
    b2=-lam**2/(2*np.pi*c)*D # ps^2/km
    b20=-1550.**2/(2*np.pi*c)*(.086/4*(1550.-1310.**4/1550.**3))
    # Integrate beta2 twice and remove beta0,beta1 at the carrier.
    ii=np.argsort(k); x=k[ii]; curvature=b2[ii]/abs(b20)
    first=cumulative_trapezoid(curvature,x,initial=0); first-=np.interp(0,x,first)
    second=cumulative_trapezoid(first,x,initial=0); second-=np.interp(0,x,second)
    out=np.empty_like(k);out[ii]=second
    return out

def propagate(N=4.,T0=200.,mask='TL',nt=16384,width=160.,zfactor=4.,hfac=1.,
              shock=False,d3=0.,loss=0.,curve=False,Tref=None,fR=.18,save=None,published=False,gamma_curve=False,smooth_mask=False):
    start=time.time();dt=width/nt;t=(np.arange(nt)-nt//2)*dt
    k=2*np.pi*fftfreq(nt,dt);u,wc=initial(t,N,mask,T0,Tref,smooth_mask)
    inp=dt*np.sum(abs(u)**2); U=fft(u)
    z=zfactor/N; h0=.4/(N*(2*N-1))**2*hfac;steps=int(np.ceil(z/h0));h=z/steps
    s=1/(2*np.pi*299792.458/1550.*T0*.001) if shock else 0.
    ld_m=(T0*.001)**2/.0217;alpha=loss*np.log(10)/10/1000*ld_m
    E=np.exp((1j*dispersion(k,T0,d3,curve,published)-alpha/2)*h/2)
    a=T0/32.;b=T0/12.2; H=(a*a+b*b)/((a+1j*k)**2+b*b)
    H[nt//2]=H[nt//2].real
    gamma_ratio=1-s*k
    if gamma_curve:
        om=-k/(T0*.001)
        gamma_ratio=1+(.0029*om-1.43e-6*om**2/2-1.11e-8*om**3/6)/1.42
    pref=1j*N*N*gamma_ratio
    def nonlinear(V):
        v=ifft(V); p=abs(v)**2
        r=(1-fR)*p+fR*ifft(H*fft(p)).real
        return pref*fft(v*r)
    for j in range(steps):
        V=E*U;k1=h*E*nonlinear(U);k2=h*nonlinear(V+k1/2)
        k3=h*nonlinear(V+k2/2);k4=h*nonlinear(E*(V+k3))
        U=E*(V+(k1+2*k2+2*k3)/6)+k4/6
        if not np.isfinite(U).all(): raise FloatingPointError('propagation nonfinite')
    u=ifft(U);out=dt*np.sum(abs(u)**2)
    diag=dict(N=N,T0_fs=T0,mask=str(mask),nt=nt,width=width,dt_fs=dt*T0,zfactor=zfactor,
              xi=z,h=h,steps=steps,fR=fR,smooth_mask=smooth_mask,shock=shock,d3=d3,loss_dB_km=loss,curve=curve,published=published,gamma_curve=gamma_curve,
              input_mass=inp,output_mass=out,mass_drift=out/inp-1,cutoff=wc,
              edge_mass=dt*np.sum(abs(u[abs(t)>.45*width])**2)/inp,
              alias_mass=np.sum(abs(U[abs(k)>.8*np.pi/dt])**2)/np.sum(abs(U)**2),
              elapsed_s=time.time()-start,phase_only_input_error=inp/2-1,
              input_energy_nJ=2*N*N*21.7/(1.3*T0),LD_m=ld_m,
              length_m=z*ld_m,shock_parameter=s,
              mask_reference_duration_fs=T0 if Tref is None else Tref,
              mask_frequency_policy='normalized frequency' if Tref is None else 'fixed physical frequency')
    if save:np.savez_compressed(save,t=t,u=u,k=k,**diag)
    return t,u,diag

def zs_shoot(t,q,eta0):
    # Exact 2x2 exponential for piecewise constant midpoint q, independent
    # of the proposer's Fourier-collocation eigenproblem.
    dt=t[1]-t[0]; mid=(q[:-1]+q[1:])/2; split=len(mid)//2
    def ev(v):
        z=v[0]+1j*v[1]
        b=np.sqrt(-z*z-abs(mid)**2+0j);bd=b*dt
        cc=np.cosh(bd); ss=np.where(abs(b)>1e-14,np.sinh(bd)/b,dt+0j)
        y=np.array([1.+0j,0j]);r=np.array([0j,1.+0j])
        for j in range(split):
            yy=(cc[j]-1j*z*ss[j])*y[0]+ss[j]*mid[j]*y[1]
            y[1]=-ss[j]*mid[j].conjugate()*y[0]+(cc[j]+1j*z*ss[j])*y[1];y[0]=yy
        for j in range(len(mid)-1,split-1,-1):
            rr=(cc[j]+1j*z*ss[j])*r[0]-ss[j]*mid[j]*r[1]
            r[1]=ss[j]*mid[j].conjugate()*r[0]+(cc[j]-1j*z*ss[j])*r[1];r[0]=rr
        v=(y[0]*r[1]-y[1]*r[0])/(np.linalg.norm(y)*np.linalg.norm(r))
        return [v.real,v.imag]
    sol=root(ev,[0,eta0],tol=1e-10)
    return dict(zeta_re=float(sol.x[0]),eta=float(sol.x[1]),root_ok=bool(sol.success),
                evans_residual=float(np.linalg.norm(sol.fun)))

def zs_shoot_robust(t,q,eta0):
    first=zs_shoot(t,q,eta0)
    valid=lambda r:r['root_ok'] and 0<r['eta']<1.2*np.max(abs(q)) and r['evans_residual']<1e-8
    if valid(first):return first
    attempts=[first]+[zs_shoot(t,q,factor*eta0) for factor in [.8,1.2,.6,1.4,.4]]
    good=[r for r in attempts if valid(r)]
    chosen=dict(max(good,key=lambda r:r['eta']) if good else first)
    chosen['initial_root_failure']=first;chosen['root_attempts']=attempts
    return chosen

def measure(t,u,d,gate_scale=1.,zs=True,refine=2,peak_index=None,gate_halfwidth=None):
    N=d['N'];dt=t[1]-t[0];p=abs(u)**2;ip=int(np.argmax(p)) if peak_index is None else int(peak_index);tp=t[ip]
    width=max(1.,8/(N*np.sqrt(p[ip])))*gate_scale
    if gate_halfwidth is not None:width=gate_halfwidth
    # A hard temporal gate is operationally separate from discrete ZS mass.
    inside=abs(t-tp)<=width
    q=N*u[inside];tt=t[inside]
    # Frequency mean from a smooth (cosine edge) version of this isolated gate.
    smooth=np.ones_like(q.real);nedge=max(2,int(.1*len(q)))
    ramp=np.sin(np.linspace(0,np.pi/2,nedge))**2
    smooth[:nedge]=ramp;smooth[-nedge:]=ramp[::-1]
    kg=2*np.pi*fftfreq(len(q),dt);Q=fft(q*smooth)
    kc=float(np.sum(kg*abs(Q)**2)/np.sum(abs(Q)**2))
    localD=1+6*d.get('d3',0)*kc
    if d.get('curve') or d.get('published'):
        fullk=2*np.pi*fftfreq(len(t),dt);disp=dispersion(fullk,d['T0_fs'],curve=d.get('curve',False),published=d.get('published',False))
        ii=np.argsort(fullk);localD=-float(np.interp(kc,fullk[ii],np.gradient(np.gradient(disp[ii],fullk[ii]),fullk[ii])))
    kappa=1-d.get('shock_parameter',0)*kc
    if d.get('gamma_curve'):
        om=-kc/(d['T0_fs']*.001)
        kappa=1+(.0029*om-1.43e-6*om**2/2-1.11e-8*om**3/6)/1.42
    fgate=float(dt*np.sum(p[inside])/d['input_mass'])
    out=dict(f_gate=fgate,red_k=kc,red_THz=kc/(2*np.pi*d['T0_fs']*.001),t_peak=tp,
             gate_halfwidth=width,local_D=localD,local_kappa=kappa,
             gated_energy_nJ=fgate*d['input_energy_nJ'])
    if zs and localD>0 and kappa>0:
        # Fourier resampling before piecewise integration isolates O(dt^2) shooting error.
        q=q*np.exp(-1j*kc*tt)*np.sqrt(kappa/localD)
        # Pad a smooth decayed tail to avoid the periodic interpolation seam.
        pad=len(q)//2;qpad=np.pad(q,(pad,pad));qr=resample(qpad,len(qpad)*refine)
        tr=np.arange(len(qr))*dt/refine
        out.update(zs_shoot_robust(tr,qr,float(np.max(abs(q))*.5)))
        out['f_zs']=4*localD*out['eta']/(kappa*N*N*d['input_mass'])
        out['zs_energy_nJ']=out['f_zs']*d['input_energy_nJ']
    # Physical photon number is energy spectrum divided by optical frequency.
    ks=2*np.pi*fftfreq(len(t),dt);sp=1/(2*np.pi*299792.458/1550.*d['T0_fs']*.001)
    pos=1-sp*ks>0;den=1-sp*ks[pos]
    inputQ=fft(1/np.cosh(t));fullQ=fft(u)
    pin=np.sum(abs(inputQ[pos])**2/den)
    gate=np.zeros_like(u);gate[inside]=u[inside]
    gateQ=fft(gate)
    out['photon_fraction_gate']=float(np.sum(abs(gateQ[pos])**2/den)/pin)
    out['physical_photon_drift']=float(np.sum(abs(fullQ[pos])**2/den)/pin-1)
    out['nonpositive_frequency_energy_fraction']=float(np.sum(abs(fullQ[~pos])**2)/np.sum(abs(fullQ)**2))
    out['output_energy_nJ']=d['input_energy_nJ']*d['output_mass']/d['input_mass']
    out['output_share_gate']=fgate*d['input_mass']/d['output_mass']
    if 'f_zs' in out:out['output_share_zs']=out['f_zs']*d['input_mass']/d['output_mass']
    out['center_wavelength_nm']=float(1550/(1-sp*kc))
    peaks,_=find_peaks(p,height=p[ip]*.1,distance=max(1,int(.5/dt)))
    out['peak_count_above_10pct']=len(peaks)
    out['other_peak_times']=[float(t[j]) for j in peaks if j!=ip]
    return out

def run_case(label,**kwargs):
    RAW.mkdir(parents=True,exist_ok=True)
    t,u,d=propagate(save=RAW/(label+'.npz'),**kwargs);d.update(measure(t,u,d));d['label']=label
    (RAW/(label+'.json')).write_text(json.dumps(d,indent=2));print(json.dumps(d),flush=True)
    return d

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['core','case','measure','calibrate'])
    p.add_argument('--label',default='case');p.add_argument('--N',type=float,default=4);p.add_argument('--T0',type=float,default=200)
    p.add_argument('--mask',default='TL');p.add_argument('--nt',type=int,default=16384);p.add_argument('--width',type=float,default=160)
    p.add_argument('--zfactor',type=float,default=4);p.add_argument('--hfac',type=float,default=1);p.add_argument('--shock',action='store_true')
    p.add_argument('--d3',type=float,default=0);p.add_argument('--loss',type=float,default=0);p.add_argument('--curve',action='store_true')
    p.add_argument('--Tref',type=float);args=p.parse_args()
    if args.mode=='core':
        for T,m in [(100,'TL'),(100,'A2'),(100,'A'),(200,'TL'),(200,'B')]:
            run_case('core_'+str(T)+'_'+m,N=4,T0=T,mask=m)
    elif args.mode=='case':
        a=vars(args);a.pop('mode');label=a.pop('label');run_case(label,**a)
    elif args.mode=='measure':
        z=np.load(RAW/(args.label+'.npz'));d={k:z[k].item() for k in z.files if k not in ('t','u','k')}
        for g in [.75,1,1.25]:
            for r in [1,2,4]:print(json.dumps(dict(gate_scale=g,refine=r,**measure(z['t'],z['u'],d,g,refine=r))))
    else:
        for n in [512,1024,2048]:
            t=np.linspace(-8,8,n,endpoint=False);q=3/np.cosh(t)
            print(n,zs_shoot(t,q,2.5),flush=True)
