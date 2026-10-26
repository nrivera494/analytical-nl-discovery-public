#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt

Triangular weak-admixture response hierarchy. This evaluates predictions without
using finite-admixture solutions or fitting their outputs.
"""
import json, sys, time, subprocess
from pathlib import Path
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.special import loggamma
from scipy.optimize import brentq
import sympy as sy

IDENT=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')
ROOT=Path(__file__).resolve().parents[1]
RAW=Path('~/analytical-nl-discovery-data')
MAT=json.loads((ROOT/'runs/2026-10-04-gpt-a-material/summary.json').read_text())

def sech_integral(a,k=0.):
    return float(np.exp((a-1)*np.log(2)+2*loggamma((a+1j*k)/2).real-loggamma(a)))

def model(delta=0.,kind='ideal'):
    p=dict(delta=delta,delta3=2*delta,b2=1.,b3=1.,mu=0.,sigma=1.,sigma13=.75,kappa=.25,alpha2=.5)
    if kind=='perturbed':
        p.update(delta3=2.1*delta,b2=1.015,b3=1.03,mu=-10.,sigma=.98)
    elif kind=='physical':
        beta1=MAT['beta1_ps_m'];beta2=MAT['beta2_ps2_m']
        p.update(delta=MAT['delta_physical'],delta3=(beta1[2]-beta1[0])*MAT['T0_ps']/abs(beta2[0]),
                 b2=beta2[1]/beta2[0],b3=beta2[2]/beta2[0],mu=MAT['beta0_residual_03_dimensionless'])
    elif kind!='ideal':raise ValueError(kind)
    return p

def bound(p,t):
    nu=(np.sqrt(1+8*p['sigma']/p['b2'])-1)/2
    psi=np.exp(-1j*p['delta']*t/p['b2'])/np.cosh(t)**nu/np.sqrt(sech_integral(2*nu))
    c0=sech_integral(nu+1,p['delta']/p['b2'])**2/(2*sech_integral(2*nu))
    return psi,c0,nu

def integrate(label,p,out,nt=4096,window=320.,dz=.005,zs=(0.,7.,13.,19.),ablation='none'):
    t=(np.arange(nt)-nt//2)*window/nt;dt=window/nt;f=1/np.cosh(t);k=2*np.pi*fftfreq(nt,dt)
    # Columns: leading minority v, pump response U, generated mode w, minority V.
    y=np.zeros((nt,4),complex);y[:,0]=f
    linear=-.5j*k[:,None]**2*np.array([p['b2'],1.,p['b3'],p['b2']])
    linear-=1j*k[:,None]*np.array([p['delta'],0.,p['delta3'],p['delta']])
    linear+=1j*np.array([0.,0.,p['mu'],0.])
    e2=np.exp(linear*dz/2);e=e2**2
    psi,c0,nu=bound(p,t);fsq=f*f
    sigma=p['sigma'];spm=0. if ablation=='no_self' else p['alpha2']
    pump=0. if ablation=='no_backaction' else 1.
    mix=0. if ablation=='no_LP03' else p['kappa']
    def n(z,a):
        v,U,w,V=a.T;u=f*np.exp(.5j*z)
        ans=np.empty_like(a)
        ans[:,0]=sigma*fsq*v
        ans[:,1]=2*fsq*U+u*u*U.conj()+pump*sigma*abs(v)**2*u
        ans[:,2]=p['sigma13']*fsq*w+mix*v*v*u.conj()
        ans[:,3]=sigma*fsq*V+sigma*(u.conj()*U+u*U.conj())*v+spm*abs(v)**2*v+2*mix*u*w*v.conj()
        return 1j*ans
    def gate_cross(v,V):
        ix=(t>-5)&(t<5);tt=np.r_[-5,t[ix],5]
        power=abs(v)**2;cross=(v.conj()*V).real
        yy=np.r_[np.interp(-5,t,power),power[ix],np.interp(5,t,power)]
        cc=np.r_[np.interp(-5,t,cross),cross[ix],np.interp(5,t,cross)]
        return float(np.trapezoid(yy,tt)/2),float(np.trapezoid(cc,tt))
    rows=[];fields=[];start=time.time()
    def save(z,a):
        v,U,w,V=a.T;q0=np.vdot(psi,v)*dt;q1=np.vdot(psi,V)*dt
        w0,w1=gate_cross(v,V)
        rows.append(dict(zeta=z,B0=float(abs(q0)**2/2),B1=float((q0.conjugate()*q1).real),
            W0=w0,W1=w1,LP03_coefficient=float(np.vdot(w,w).real*dt),
            minority_norm_correction=float(np.vdot(v,V).real*dt),
            pump_norm_first_correction=float(2*np.vdot(f*np.exp(.5j*z),U).real*dt),
            boundary_fraction=float(np.sum(abs(a[abs(t)>.45*window])**2)/np.sum(abs(a)**2))))
        fields.append(a.copy())
    save(0.,y);yh=fft(y,axis=0);steps={round(z/dz):z for z in zs if z>0}
    for step in range(1,max(steps)+1):
        z=(step-1)*dz
        a1=dz*fft(n(z,ifft(yh,axis=0)),axis=0)
        a2=dz*fft(n(z+dz/2,ifft(e2*(yh+a1/2),axis=0)),axis=0)/e2
        a3=dz*fft(n(z+dz/2,ifft(e2*(yh+a2/2),axis=0)),axis=0)/e2
        a4=dz*fft(n(z+dz,ifft(e*(yh+a3),axis=0)),axis=0)/e
        yh=e*(yh+(a1+2*a2+2*a3+a4)/6)
        if step in steps:save(steps[step],ifft(yh,axis=0))
    result=dict(IDENT,label=label,parameters=p,nt=nt,window_tau=window,dzeta=dz,ablation=ablation,
        nu=nu,C0_analytic=c0,elapsed_seconds=time.time()-start,rows=rows)
    out.mkdir(parents=True,exist_ok=True)
    (out/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(out/(label+'.npz'),tau=t,fields=np.array(fields))
    print(label,rows[-1],f'{time.time()-start:.1f}s',flush=True)
    return result

def symbolic(out):
    e=sy.symbols('epsilon',real=True)
    u,uc,v,vc,U,Uc,V,Vc,w,wc=sy.symbols('u uc v vc U Uc V Vc w wc')
    s,g,k,a,b,c=sy.symbols('sigma sigma13 kappa alpha2 sigma23 alpha3',real=True)
    A=u+e**2*U;Ac=uc+e**2*Uc;B=e*v+e**3*V;Bc=e*vc+e**3*Vc;C=e**2*w;Cc=e**2*wc
    n1=sy.expand(A*Ac*A+s*B*Bc*A+g*C*Cc*A+k*B*B*Cc)
    n2=sy.expand(s*A*Ac*B+a*B*Bc*B+b*C*Cc*B+2*k*A*C*Bc)
    n3=sy.expand(g*A*Ac*C+b*B*Bc*C+c*C*Cc*C+k*B*B*Ac)
    expected=[2*u*uc*U+u*u*Uc+s*v*vc*u,
        s*u*uc*V+s*(uc*U+u*Uc)*v+a*v*vc*v+2*k*u*w*vc,g*u*uc*w+k*v*v*uc]
    residuals=[str(sy.simplify(actual.coeff(e,power)-target)) for actual,power,target in zip((n1,n2,n3),(2,3,2),expected)]
    assert residuals==['0','0','0']
    d=dict(IDENT,formal_coefficient_residuals=residuals,epsilon_orders=[2,3,2],
        scope='Exact polynomial expansion of the three-mode rotating-wave Kerr nonlinearity.')
    out.mkdir(parents=True,exist_ok=True);(out/'symbolic.json').write_text(json.dumps(d,indent=2)+'\n')

if __name__=='__main__':
    out=Path(sys.argv[1]);mode=sys.argv[2]
    if mode=='symbolic':symbolic(out)
    elif mode=='prediction':
        out.mkdir(parents=True,exist_ok=True)
        nu3=(np.sqrt(7)-1)/2;lambda3=nu3**2/2
        overlap=sech_integral(nu3+1)**2/sech_integral(2*nu3)
        zero=dict(IDENT,nu3=nu3,lambda3=lambda3,ground_overlap_squared=overlap,
            beat_gap=.5-lambda3,K_range=[0.,8.],ground_only_absolute_K_error_bound=2*(2-overlap),
            rows=[dict(zeta=z,K_ground_only=4-2*overlap*np.cos((.5-lambda3)*z)) for z in (0.,7.,13.,19.)])
        (out/'zero_walkoff_formula.json').write_text(json.dumps(zero,indent=2)+'\n')
        for j,d in enumerate((0.,.35,.85,1.35),1):integrate(f'ideal_d{j}',model(d),out)
        integrate('perturbed',model(.85,'perturbed'),out)
        integrate('physical',model(kind='physical'),out,dz=.0025)
        root=brentq(lambda d:sech_integral(2,d)**2/4-.5,.1,2.)
        p=model(root);row=integrate('boundary',p,out,zs=(0.,13.))['rows'][-1]
        derivative=.5*(2/root-np.pi/np.tanh(np.pi*root/2))
        info=dict(IDENT,delta_half_zeroth=root,B1_at_half=row['B1'],C0_derivative=derivative,
            delta_half_slope_r=-row['B1']/derivative,zeta=13.,criterion='reference bound-channel projection equals 1/2')
        (out/'boundary_prediction.json').write_text(json.dumps(info,indent=2)+'\n');print(info,flush=True)
    elif mode=='convergence':
        integrate('ideal_d3_halfstep',model(.85),out,dz=.0025)
        integrate('ideal_d3_doublewindow',model(.85),out,nt=8192,window=640.)
        integrate('ideal_d3_resolution',model(.85),out,nt=8192)
        integrate('physical_halfstep',model(kind='physical'),out,dz=.00125)
    elif mode=='ablation':
        for which in ('no_self','no_backaction','no_LP03'):
            integrate(which,model(.85),out,ablation=which)
    else:raise ValueError(mode)
