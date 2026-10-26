#!/usr/bin/env python3
"""Frozen cancellation, direct RHS, and kernel checks; gpt-d/gpt-6-astra/gpt."""
from pathlib import Path
import json, time
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import mpmath as mp
from analyze import HERE, RAW, IDENTITY, exact_mp, exponent

def main():
    started=time.time()
    r=mp.mpf('0.6');xs=np.array([.00025,.0005,.001,.002])
    quadcoef=mp.pi**2*(3*r*r-1)/12
    cubic=2*r*(1-r*r)*mp.zeta(3)
    res1=[];res2=[]
    for x0 in xs:
        x=mp.mpf(str(x0));rho=exact_mp(x,r)
        res1.append(float(rho-1+2*r*x))
        res2.append(float(rho-1+2*r*x-quadcoef*x*x))
    estimate=np.polyfit(xs,np.array(res2)/xs**3,1)[-1]
    cancellation=dict(freeze_commit="3259dd5be15c597202b52436ff7d5d1918c702dc",
        r=float(r),x=xs.tolist(),linear_residual=res1,quadratic_residual=res2,
        linear_residual_exponent=exponent(xs,res1),quadratic_residual_exponent=exponent(xs,res2),
        cubic_predicted=float(cubic),cubic_extrapolated=float(estimate),
        cubic_relative_difference=float(abs(estimate/float(cubic)-1)),
        classification="Adaptive follow-up of a retained finite-window slope failure; not held out")
    rhs=[];a,b=1/.032,1/.0122;q=a*a+b*b
    for x in [.04,.1,.25,.5,1.,2.,4.,8.,40.,80.,160.]:
        T=x/b;n=32768;window=max(40*T,40/a);dt=window/n
        t=(np.arange(n)-n//2)*dt;O=2*np.pi*fftfreq(n,dt);w0=50/T
        u=t/T;A=2*np.exp(-abs(u))/(1+np.exp(-2*abs(u)))
        aw=ifft(A);aw*=w0+O>0;A=fft(aw);I=abs(A)**2;E=dt*sum(I)
        H=q/((a-1j*O)**2+b*b);fr=.18;gamma=1.
        V=(1-fr)*I+fr*fft(H*ifft(I)).real
        nl=1j*gamma*(1+O/w0)*ifft(A*V)
        rate=-2*window*np.real(np.vdot(aw,nl));kappa=gamma*fr/w0*q/2
        rho=rate/(kappa*E*E);exact=float(exact_mp(x,a/b))
        rhs.append(dict(x=x,T_ps=T,dt_fs=dt*1000,omega0_T=50.,rho_rhs=float(rho),rho_exact=exact,
            relative_difference=float(abs(rho/exact-1))))
    kernel=[]
    for dt in [.003,.0015,.00075,.000375]:
        window=1.536;n=round(window/dt);t=np.arange(n)*dt;O=2*np.pi*fftfreq(n,dt)
        h=q/b*np.exp(-a*t)*np.sin(b*t);sampled=window*ifft(h)
        exact=q/((a-1j*O)**2+b*b)
        u=(t-window/2)/.0567;I=(2*np.exp(-abs(u))/(1+np.exp(-2*abs(u))))**2
        iw=ifft(I)
        R_s=window*np.sum(O*sampled.imag*abs(iw)**2)
        R_e=window*np.sum(O*exact.imag*abs(iw)**2)
        kernel.append(dict(dt_fs=dt*1000,n=n,integral=float(sampled[0].real),
            normalization_gap=float(1-sampled[0].real),normalization_prediction=q*dt*dt/12,
            rate_relative_error=float(abs(R_s/R_e-1))))
    out=dict(**IDENTITY,run_id=HERE.name,cancellation=cancellation,
        rhs_freeze_commit="ca03c40b69e09530f57de96863bab3d048df06ea",rhs=rhs,
        rhs_max_relative_difference=max(x["relative_difference"] for x in rhs),
        rhs_long_decay_exponent=-exponent([40,80,160],[x["rho_rhs"] for x in rhs[-3:]]),
        kernel=kernel,kernel_normalization_exponent=exponent([v["dt_fs"] for v in kernel],
            [v["normalization_gap"] for v in kernel]),
        kernel_rate_error_exponent=exponent([v["dt_fs"] for v in kernel],
            [v["rate_relative_error"] for v in kernel]),wall_time_s=time.time()-started)
    (HERE/"followup_summary.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
