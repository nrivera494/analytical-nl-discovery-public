"""Independent exact Kerr moments. gpt-b / gpt-6-astra / gpt / 2026-10-18.
Vacuum quadrature variance one. n denotes displacement photons, not total.
"""
import mpmath as mp
import numpy as np
from scipy.optimize import minimize_scalar
mp.mp.dps=60

def moments(n,nu,s,twa=False):
    n,nu,s=map(mp.mpf,map(str,(n,nu,s)));k=s/n
    if twa:
        v=nu/2
        def moment(r):
            D=1+1j*r*k*v
            return n**(mp.mpf(r)/2)*mp.exp(1j*r*k)*D**(-r-1)*mp.exp(-1j*r*k*n/D)
    else:
        t=(nu-1)/2
        def moment(r):
            u=mp.expm1(-1j*r*k);D=1-t*u
            return n**(mp.mpf(r)/2)*mp.exp(-1j*k*r*(r-1)/2)*D**(-r-1)*mp.exp(n*u/D)
    a=moment(1);b=moment(2);N=n+(nu-1)/2
    central=b-a*a;isotropic=1+2*(N-abs(a)**2)
    # Rotate to the exact mean field, without subtracting huge double moments.
    centered=central*mp.exp(-2j*mp.arg(a))
    V=np.array([[float(isotropic+2*mp.re(centered)),float(2*mp.im(centered))],
                [float(2*mp.im(centered)),float(isotropic-2*mp.re(centered))]])
    return {'lambda':float(isotropic-2*abs(central)),'V':V,'phase':float(mp.arg(a)),
            'mean':complex(a),'a2':complex(b),'N':float(N),
            'dark_photons':float(N-abs(a)**2)}

def optimum(n,nu,twa=False):
    # Leading optimum, broad log interval around it; earliest Kerr-shear branch.
    guess=(n/(16*nu))**(1/6)
    opt=minimize_scalar(lambda x:moments(n,nu,np.exp(x),twa)['lambda'],
                        bounds=(np.log(guess)-3,np.log(guess)+2),method='bounded',
                        options={'xatol':2e-10})
    s=float(np.exp(opt.x));r=moments(n,nu,s,twa);r.pop('mean');r.pop('a2')
    return dict(s=s,**r)

def tangent(s,nu=1):
    S=np.array([[1.,0],[-2*s,1.]])
    return nu*S@S.T
