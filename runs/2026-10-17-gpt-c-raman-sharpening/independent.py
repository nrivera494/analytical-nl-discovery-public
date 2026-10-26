"""Independent Raman GNLSE and ZS measurements. gpt-c / gpt-6-astra / gpt."""
import ctypes
import json
import math
import time
import hashlib
from pathlib import Path
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.interpolate import CubicSpline
from scipy.optimize import root
from scipy.signal import find_peaks
from scipy.special import erfcx

# Adapted from gpt-c's independent audit implementation; no proposer code used.
IMPLEMENTATION_SHA256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

C_NM_FS = 299.792458
K = 2*np.pi*C_NM_FS
W0 = K/1550.
BETA2 = 21700.  # fs^2/m
GAMMA = .0013   # 1/(W m)
LZ = 1310.
D0 = BETA2*K/1550.**2
S0 = 4*D0/(1550.-LZ**4/1550.**3)
DA = S0*K*K/4
DB = S0*LZ**4/(4*K*K)
BETA3 = 3*DA/W0**4+DB
RAW = Path('~/analytical-nl-discovery-data/2026-10-17-gpt-c-raman-sharpening')

def measured_D(lam_nm):
    """Boilard et al., DOI 10.1038/s41598-022-08329-3, Table 3."""
    l=np.asarray(lam_nm)/1000.
    return (150.5*l**3-549.6*l*l+918.8*l-600)/(l*l+1.374*l-.4602)

def measured_beta2(omega):
    # The extension is numerical only; out-of-range spectral content is reported.
    lam=np.clip(K/np.maximum(omega,K/10000),800.,3000.)
    return -lam*lam/K*measured_D(lam)

def carrier_beta2(dispersion):
    return float(-measured_beta2(W0)) if dispersion=='measured' else BETA2

_measured_integral=None
def measured_residual(omega):
    global _measured_integral
    if _measured_integral is None:
        grid=np.linspace(K/10000,8*W0,65537)
        _measured_integral=CubicSpline(grid,measured_beta2(grid)).antiderivative(2)
    F=_measured_integral
    return F(omega)-F(W0)-F(W0,1)*(omega-W0)

def response(w, T, model='bw', scale=1.):
    v = w/T*scale
    a,b=1/32.,1/12.2
    hb=(a*a+b*b)/((a+1j*v)**2+b*b)
    if model=='off': return np.ones_like(w,dtype=complex),0.
    if model=='bw': return hb,.18
    if model=='as2s3':
        a,b=1/230.5,1/15.5
        return (a*a+b*b)/((a+1j*v)**2+b*b),.10
    if model=='bw_damped':
        a,b=1/16.,1/12.2
        return (a*a+b*b)/((a+1j*v)**2+b*b),.18
    if model=='la':
        z=1+1j*v*96
        return .79*hb+.21*(2/z-1/z**2),.245
    if model!='hc': raise ValueError(model)
    pos=np.array([56.25,100,231.25,362.5,463,497,611.5,691.67,793.67,835.5,930,1080,1215])
    amp=np.array([1,11.4,36.67,67.67,74,4.5,6.8,4.6,4.2,4.5,2.7,3.1,3])
    ga=np.array([52.1,110.42,175,162.5,135.33,24.5,41.5,155,59.5,64.3,150,91,160])
    lo=np.array([17.37,38.81,58.33,54.17,45.11,8.17,13.83,51.67,19.83,21.43,50,30.33,53.33])
    conv=np.pi*2.99792458e-5 # cm/fs, table's conversion is pi*c*linewidth
    ans=np.zeros_like(w,dtype=complex); norm=0.
    for p,A,g,l in zip(pos,amp,ga,lo):
        om=2*conv*p; G=conv*g; gam=conv*l
        def integ(freq): return np.sqrt(np.pi)/G*erfcx((gam+1j*freq)/G)
        ans+=A*(integ(v-om)-integ(v+om))/(2j)
        norm+=float(np.real(A*(integ(-om)-integ(om))/(2j)))
    return ans/norm,.18

def beta2_local(wc,T,dispersion):
    if dispersion=='constant': return 1.
    om=W0-wc/T
    if dispersion=='tod': return 1+BETA3*wc/(T*BETA2)
    if dispersion=='measured': return float(-measured_beta2(om)/carrier_beta2(dispersion))
    return (DA/om**3-DB*om)/BETA2 if om>0 else np.nan

def linear(w,T,dispersion,loss_db_km=0):
    if dispersion=='constant': D=-.5*w*w
    elif dispersion=='tod': D=-.5*w*w-BETA3/(6*BETA2*T)*w**3
    elif dispersion=='measured': D=measured_residual(W0-w/T)*T*T/carrier_beta2(dispersion)
    else:
        r=-w/(T*W0)
        # Smooth extension below 0.15*carrier, never accepted as physical data.
        rr=np.maximum(r,-.85)
        d=-DA/2*(rr*rr/(W0*(1+rr)))+DB/6*W0**3*(3*rr*rr+rr**3)
        D=d*T*T/BETA2
    alpha=loss_db_km*np.log(10)/10/1000*T*T/carrier_beta2(dispersion)
    return 1j*D-alpha/2

def rk4ip(v,h,L,nonlinear):
    eh=np.exp(L*h/2)
    x=eh*v
    k1=eh*nonlinear(v)
    k2=nonlinear(x+h*k1/2)
    k3=nonlinear(x+h*k2/2)
    k4=nonlinear(eh*(x+h*k3))
    return eh*(x+h*(k1+2*k2+2*k3)/6)+h*k4/6

def propagate(case, callback):
    N=case['N']; T=case['T0_fs']; n=case.get('n',8192); width=case.get('width',96.)
    b0=carrier_beta2(case.get('dispersion','constant'))
    t=(np.arange(n)-n//2)*width/n; dt=width/n
    w=2*np.pi*fftfreq(n,dt)
    hR,fR=response(w,T,case.get('raman','bw'),case.get('raman_scale',1.))
    if case.get('raman_sampling') in ['sampled_raw','sampled_normalized']:
        if case.get('raman','bw')!='bw':raise ValueError('Sampled-kernel cross-check is defined only for Blow-Wood.')
        tt=np.arange(n)*dt*T;a,b=1/32.,1/12.2
        hR=fft((a*a+b*b)/b*np.exp(-a*tt)*np.sin(b*tt))*dt*T
        if case['raman_sampling']=='sampled_normalized':hR=hR/hR[0].real
    L=linear(w,T,case.get('dispersion','constant'),case.get('loss_db_km',0))
    shock=1-w/(W0*T) if case.get('shock',False) else np.ones(n)
    band=case.get('filter_fraction',1.)
    filt=(np.abs(w)<band*np.max(np.abs(w))) if band<1 else np.ones(n)
    if case.get('solver_filter',False):
        # Post-audit control: b9fa957 src/backend/fft_utils.jl, inspected after
        # independent verdict commit 143cc58. Reverse bins for the FFT sign.
        index=np.fft.ifftshift(np.arange(1,n+1,dtype=float))
        fc=n//2+1;f0=n*.85/(2*np.sqrt(np.log(2)))
        damp=np.exp(-.5*((index-fc)/f0)**40)**20
        damp[n//2:]=1.
        filt=filt*damp[(-np.arange(n))%n]
    def nonlinear(v):
        q=ifft(v); I=abs(q)**2
        delayed=ifft(hR*fft(I)).real
        return 1j*shock*filt*fft(q*((1-fR)*I+fR*delayed))
    q=N*launch(t,case.get('shape','sech'))
    v=fft(q); mass0=float(dt*np.vdot(q,q).real)
    phot0=float(np.sum(abs(v)**2/shock)) if case.get('shock') else float(np.sum(abs(v)**2))
    z=0.; h=case.get('fixed_step',case.get('initial_step',.002/max(1,N))); tol=case.get('tol',2e-8)
    accepted=rejected=0; start=time.monotonic(); maxedge=0.; max_timeedge=0.
    checkpoints=case.get('zN',[2,2.5,3,4])
    for zn in checkpoints:
        target=zn/N
        while z<target-1e-13:
            hs=min(h,target-z)
            full=rk4ip(v,hs,L,nonlinear)
            if 'fixed_step' in case:
                fine=full;err=0.
            else:
                half=rk4ip(v,hs/2,L,nonlinear)
                fine=rk4ip(half,hs/2,L,nonlinear)
                err=np.linalg.norm(fine-full)/(15*np.linalg.norm(fine))
            if not np.isfinite(err): raise RuntimeError('nonfinite integration error')
            if err<=tol:
                v=fine; z+=hs; accepted+=1
                if accepted%100==0:
                    maxedge=max(maxedge,float(np.sum(abs(v[np.abs(w)>.8*np.max(abs(w))])**2)/np.sum(abs(v)**2)))
                    qt=ifft(v)
                    max_timeedge=max(max_timeedge,float(np.sum(abs(qt[np.abs(t)>.45*width])**2)/np.sum(abs(qt)**2)))
            else: rejected+=1
            h=case.get('fixed_step',hs*np.clip(.9*(tol/max(err,1e-30))**.2,.25,2.))
            if accepted+rejected>2000000: raise RuntimeError('step budget exceeded')
        q=ifft(v)
        mass=float(dt*np.vdot(q,q).real)
        photon=float(np.sum(abs(v)**2/shock)) if case.get('shock') else float(np.sum(abs(v)**2))
        stats={'zN':zn,'z_LD':z,'length_m':z*T*T/b0,'mass_drift':mass/mass0-1,
               'photon_drift':photon/phot0-1,'steps':accepted,'rejected':rejected,
               'max_spectral_edge_fraction':maxedge,'max_time_edge_fraction':max_timeedge,
               'spectral_edge_fraction':float(np.sum(abs(v[np.abs(w)>.8*np.max(abs(w))])**2)/np.sum(abs(v)**2)),
               'time_edge_fraction':float(np.sum(abs(q[np.abs(t)>.45*width])**2)/np.sum(abs(q)**2)),
               'nonpositive_frequency_fraction':float(np.sum(abs(v[w>W0*T])**2)/np.sum(abs(v)**2)),
               'runtime_s':time.monotonic()-start,'dt_fs':dt*T,'energy_launch_nJ':mass0*b0/(GAMMA*T)*1e-6,
               'launch_norm':mass0, 'initial_photon_energy_equivalent_ratio':photon_launch_ratio(t,case),
               'beta2_carrier_ps2_km':-b0/1000}
        absom=W0-w/T
        for lo,hi in [(1200,2300),(800,3000)]:
            inside=(absom>=K/hi)&(absom<=K/lo)
            stats[f'global_spectral_fraction_{lo}_{hi}nm']=float(np.sum(abs(v[inside])**2)/np.sum(abs(v)**2))
        callback(t,q,stats)

_lib=None
def zs_root(t,q,guess=None,points=2048):
    global _lib
    if _lib is None:
        _lib=ctypes.CDLL('/tmp/gpt-c-zs-shoot.so')
        ptr=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
        _lib.evans.argtypes=[ctypes.c_int,ptr,ptr,ctypes.c_double,ctypes.c_double,ctypes.c_double,ptr]
    h=(t[-1]-t[0])/points
    x=t[0]+(np.arange(points)+.5)*h
    qs=CubicSpline(t,q)(x)
    qr=np.ascontiguousarray(qs.real); qi=np.ascontiguousarray(qs.imag)
    out=np.zeros(2)
    def fun(v):
        _lib.evans(points,qr,qi,h,float(v[0]),float(v[1]),out)
        return out.copy()
    if guess is None: guess=[0.,max(abs(q))*.5]
    sol=root(fun,guess,tol=1e-10)
    if np.linalg.norm(fun(sol.x))>1e-8 or sol.x[1]<=0:
        solutions=[]
        mass=np.trapezoid(abs(q)**2,t)
        for eta in [mass/4,.4*max(abs(q)),.6*max(abs(q)),.8*max(abs(q)),.25*max(abs(q))]:
            for re in [0.,-.1*max(abs(q)),.1*max(abs(q))]:
                trial=root(fun,[re,eta],tol=1e-10)
                if trial.x[1]>0 and np.linalg.norm(fun(trial.x))<1e-8: solutions.append(trial)
        if solutions: sol=max(solutions,key=lambda v:v.x[1])
    return {'real':float(sol.x[0]),'eta':float(sol.x[1]),'residual':float(np.linalg.norm(fun(sol.x))),
            'success':bool(sol.success or np.linalg.norm(fun(sol.x))<1e-8),'points':points}

def census(t,q,case,all_peaks=True):
    I=abs(q)**2; dt=t[1]-t[0]; N=case['N']; T=case['T0_fs']; E=shape_integral(case.get('shape','sech'))*N*N
    b0=carrier_beta2(case.get('dispersion','constant'))
    peaks,_=find_peaks(I,prominence=max(I)*.003,distance=3)
    peaks=sorted(peaks,key=lambda j:I[j],reverse=True)[:min(24,int(N)+6)]
    peaks=sorted(peaks)
    result=[]
    for k,j in enumerate(peaks):
        if I[j]<max(I)*.01: continue
        # The half maximum width is measured independently of the scattering result.
        a=j
        while a>0 and I[a]>.5*I[j]: a-=1
        b=j
        while b<len(t)-1 and I[b]>.5*I[j]: b+=1
        sech_width=max((t[b]-t[a])/1.762747,2*dt)
        halfwidth=max(10*sech_width,.25)
        left=max(0,np.searchsorted(t,t[j]-halfwidth)); right=min(len(t)-1,np.searchsorted(t,t[j]+halfwidth))
        if k>0: left=max(left,peaks[k-1]+np.argmin(I[peaks[k-1]:j+1]))
        if k+1<len(peaks): right=min(right,j+np.argmin(I[j:peaks[k+1]+1]))
        if right-left<12: continue
        tc=t[left:right+1]-t[j]; qc=q[left:right+1]
        # Local phase slope moment, avoiding a cropped FFT's boundary discontinuity.
        dq=ifft(1j*2*np.pi*fftfreq(len(t),dt)*fft(q))[left:right+1]
        wc=float(np.trapezoid(np.imag(np.conj(qc)*dq),tc)/np.trapezoid(abs(qc)**2,tc))
        qd=qc*np.exp(-1j*wc*tc)
        bfac=beta2_local(wc,T,case.get('dispersion','constant'))
        gfac=1-wc/(W0*T) if case.get('shock') else 1.
        if not (bfac>0 and gfac>0): continue
        qs=qd*np.sqrt(gfac/bfac)
        zs=zs_root(tc,qs,points=case.get('zs_points',2048))
        f=4*zs['eta']*bfac/gfac/E
        window=float(np.trapezoid(abs(qc)**2,tc)/E)
        om=W0-wc/T
        # Spectrum of the isolated temporal component, with zero outside its gate.
        gated=np.zeros_like(q);gated[left:right+1]=qc
        freq=2*np.pi*fftfreq(len(t),dt); spec=abs(fft(gated))**2
        absom=W0-freq/T; physical=absom>0
        fractions={}
        for lo,hi in [(1200,2300),(1300,2000),(1285,1625)]:
            inside=physical & (absom>=K/hi) & (absom<=K/lo)
            fractions[f'spectral_fraction_{lo}_{hi}nm']=float(sum(spec[inside])/sum(spec))
        ph_window=float(dt/len(t)/E*np.sum(spec[physical]*W0/absom[physical]))
        rms_w=float(np.sqrt(np.sum(spec*(freq-wc)**2)/sum(spec)))
        bp=beta2_local(wc+rms_w,T,case.get('dispersion','constant'))
        bm=beta2_local(wc-rms_w,T,case.get('dispersion','constant'))
        result.append({'index':int(j),'t_peak':float(t[j]),'peak_power_normalized':float(I[j]),
             'red_w':wc,'red_shift_THz':wc/T*1000/(2*np.pi),'lambda_nm':K/om if om>0 else None,
             'width_fs':sech_width*T, **width_diagnostics(tc,qc,T), 'area_width_fs':float(T/(2*zs['eta'])),'bounds':[float(t[left]),float(t[right])],
             'boundary_intensity_ratio':float(max(I[left],I[right])/I[j]),
             'local_beta2_ratio':float(bfac),'local_gamma_ratio':float(gfac),'zs':zs,
             'f_zs':float(f),'f_window':window,'zs_window_ratio':float(f/window),
             'f_photon_window':ph_window,'rms_bandwidth_normalized':rms_w,
             'relative_dispersion_variation_one_rms':float(max(abs(bp-bfac),abs(bm-bfac))/bfac) if np.isfinite(bp) and np.isfinite(bm) else None,
             'dispersion_variation_diagnostic_defined':bool(np.isfinite(bp) and np.isfinite(bm)),
             **fractions,
             'energy_zs_nJ':float(f*E*b0/(GAMMA*T)*1e-6)})
    valid=[p for p in result if p['zs']['success'] and p['f_zs']>.005 and p['zs']['eta']>0]
    leading=max(valid,key=lambda p:p['red_w']) if valid else None
    return {'peaks':result,'leading':leading,'largest_share':max(valid,key=lambda p:p['f_zs']) if valid else None}

def write_json(path,obj):
    path=Path(path); temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n'); temp.replace(path)


def launch(t,shape):
    if shape=='sech': return 1/np.cosh(t)
    if shape=='gaussian': return np.exp(-t*t/2)
    raise ValueError(shape)

def shape_integral(shape):
    return 2. if shape=='sech' else np.sqrt(np.pi)

def photon_launch_ratio(t,case):
    T=case['T0_fs'];N=case['N'];dt=t[1]-t[0]
    v=fft(N*launch(t,case.get('shape','sech')))
    om=W0-2*np.pi*fftfreq(len(t),dt)/T
    mask=om>0
    return float(np.sum(abs(v[mask])**2*W0/om[mask])/np.sum(abs(v)**2))

def width_diagnostics(t,q,T):
    from scipy.optimize import least_squares, brentq
    I=abs(q)**2; j=int(np.argmax(I)); ip=I[j]; dt=t[1]-t[0]
    a=j
    while a>0 and I[a]>.5*ip:a-=1
    b=j
    while b<len(t)-1 and I[b]>.5*ip:b+=1
    cs=CubicSpline(t,I)
    try:
        left=brentq(lambda x:cs(x)-ip/2,t[a],t[a+1])
        right=brentq(lambda x:cs(x)-ip/2,t[b-1],t[b])
        wf=(right-left)/1.762747174039086
    except ValueError:wf=max((t[b]-t[a])/1.762747174039086,2*dt)
    use=abs(t-t[j])<4*wf
    def resid(x):
        pred=np.exp(x[0])/np.cosh(np.clip((t[use]-x[2])/np.exp(x[1]),-300,300))**2
        return (pred-I[use])/ip
    fit=least_squares(resid,[np.log(ip),np.log(wf),t[j]],max_nfev=50)
    return {'fwhm_width_fs':float(wf*T),'fit_width_fs':float(np.exp(fit.x[1])*T),
            'sech_fit_relative_l2':float(np.linalg.norm(resid(fit.x))/np.linalg.norm(I[use]/ip))}
