#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt

Exploratory long-distance lead, separate from the finite-time capture claim.
An outgoing stationary ODE predicts radiation flux; a driven linear propagation
tests it without fitting the flux coefficient. This is not a zero-capture theorem.
"""
import json,sys,time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.fft import fft,ifft,fftfreq
from p002_nextorder import IDENT,ROOT,RAW,sech_integral

PREFIX='2026-10-04-gpt-a-radiation-onset'
DELTAS=(.65,.75,.85,1.05)

def stationary(delta,potential=.75):
    omega=.5-delta**2
    b0=(np.pi*delta/(2*np.sinh(np.pi*delta/2)))**2
    if omega>=0:return dict(delta=delta,Omega=omega,B0=b0,Gamma=0.,channel='closed')
    k=np.sqrt(-2*omega)
    def rhs(t,y):
        f=1/np.cosh(t);v=k*k+2*potential*f*f
        return [y[1],-v*y[0],y[3],-v*y[2]-2*f**3]
    y=solve_ivp(rhs,[0,24],[1,0,0,0],rtol=2e-11,atol=1e-13,method='DOP853').y[:,-1]
    a=(1j*k*y[2]-y[3])/(y[1]-1j*k*y[0])
    c=(a*y[0]+y[2])*np.exp(-1j*k*24)
    rate=2*k*.25**2*b0**2*abs(c)**2
    return dict(delta=delta,Omega=omega,B0=b0,k=k,Gamma=float(rate),outgoing_amplitude=[float(c.real),float(c.imag)],channel='open')

def freeze():
    cases=[stationary(d) for d in DELTAS]
    free=stationary(.85,0.);k=free['k']
    free_exact=2*.25**2*free['B0']**2*sech_integral(3,k)**2/k
    out=ROOT/'runs'/(PREFIX+'-prediction');out.mkdir(parents=True,exist_ok=True)
    result=dict(IDENT,run_id=PREFIX+'-prediction',cases=cases,
        free_ODE_rate=free['Gamma'],free_exact_rate=free_exact,
        free_relative_error=abs(free['Gamma']/free_exact-1),
        scope='Frozen-source LP03 continuum-energy growth only; no full nonlinear depletion law asserted.',
        comparison='For each open channel, slope of continuum energy over zeta 200--400 should agree with Gamma within 5%; closed channel has no secular linear growth.',
        nonlinear_pilot='One co-launched full three-mode run at r=0.006, delta=0.85 to zeta=400. Its discrepancy from frozen-source flux is exploratory, not a fitted correction.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

def propagate(delta,out,nt=16384,window=2048.,dz=.02,label=None):
    label=label or f'd{delta:g}';pred=stationary(delta);omega=pred['Omega']
    t=(np.arange(nt)-nt//2)*window/nt;dt=window/nt
    f=2*np.exp(-abs(t))/(1+np.exp(-2*abs(t)))
    k=2*np.pi*fftfreq(nt,dt);linear=-.5j*k*k;e2=np.exp(linear*dz/2);e=e2*e2
    v=.75*f*f;g=.25*pred['B0']*f**3
    nu=(np.sqrt(7)-1)/2;psi=f**nu/np.sqrt(sech_integral(2*nu))
    yh=np.zeros(nt,complex);rows=[];fields=[];start=time.time()
    saves={round(z/dz):z for z in (0.,50.,100.,150.,200.,250.,300.,350.,400.)}
    def n(z,a):return 1j*(v*a+g*np.exp(1j*omega*z))
    def save(z,a):
        energy=float(np.vdot(a,a).real*dt);ground=float(abs(np.vdot(psi,a)*dt)**2)
        rows.append(dict(zeta=z,energy=energy,ground_energy=ground,continuum_energy=energy-ground,
            edge_energy=float(np.sum(abs(a[abs(t)>.45*window])**2)*dt)))
        fields.append(a.copy())
    save(0.,ifft(yh))
    for step in range(1,max(saves)+1):
        z=(step-1)*dz
        a1=dz*fft(n(z,ifft(yh)))
        a2=dz*fft(n(z+dz/2,ifft(e2*(yh+a1/2))))/e2
        a3=dz*fft(n(z+dz/2,ifft(e2*(yh+a2/2))))/e2
        a4=dz*fft(n(z+dz,ifft(e*(yh+a3))))/e
        yh=e*(yh+(a1+2*a2+2*a3+a4)/6)
        if step in saves:save(saves[step],ifft(yh))
    q=[x for x in rows if x['zeta']>=200]
    slope=float(np.polyfit([x['zeta'] for x in q],[x['continuum_energy'] for x in q],1)[0])
    result=dict(IDENT,label=label,parameters=pred,nt=nt,window_tau=window,dzeta=dz,
        elapsed_seconds=time.time()-start,rows=rows,measured_slope=slope,
        slope_relative_error=None if pred['Gamma']==0 else abs(slope/pred['Gamma']-1))
    out.mkdir(parents=True,exist_ok=True)
    (out/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(out/(label+'.npz'),tau=t,fields=np.array(fields))
    print(label,slope,pred['Gamma'],result['slope_relative_error'],result['elapsed_seconds'],flush=True)

if __name__=='__main__':
    if sys.argv[1]=='freeze':freeze()
    elif sys.argv[1]=='propagate':
        for d in DELTAS:propagate(d,RAW/(PREFIX+'-response'))
    elif sys.argv[1]=='convergence':
        propagate(.85,RAW/(PREFIX+'-convergence'),dz=.01,label='halfstep')
        propagate(.85,RAW/(PREFIX+'-convergence'),nt=32768,window=4096.,label='doublewindow')
    else:raise ValueError(sys.argv[1])
