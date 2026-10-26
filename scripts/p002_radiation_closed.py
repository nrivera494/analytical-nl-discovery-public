#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt

Closed-form evaluation of the already frozen outgoing-wave coefficient.
Derived after the propagation checks; no prediction table is replaced.
"""
import json,time
import numpy as np
from scipy.special import loggamma
from p002_nextorder import IDENT,RAW
from p002_radiation_onset import stationary

def closed_rate(delta):
    k2=2*delta*delta-1
    if k2<=0:return 0.
    k=np.sqrt(k2);nu=(np.sqrt(7)-1)/2;a=(1-nu)/2;b=1+nu/2
    b0=(np.pi*delta/(2*np.sinh(np.pi*delta/2)))**2
    logj=2*np.log(np.pi/np.cosh(np.pi*k/2))+2*np.log(np.pi)+2*loggamma(1-1j*k).real
    logj-=2*(loggamma(a).real+loggamma(b).real+loggamma(b-.5j*k).real+loggamma(a-.5j*k).real)
    transmission=np.sinh(np.pi*k)**2/(np.sinh(np.pi*k)**2+np.sin(np.pi*nu)**2)
    return float(.5*b0*b0*(1+k*k)**2/k*transmission*np.exp(logj))

if __name__=='__main__':
    start=time.time();rows=[]
    for delta in (.75,.85,1.05,1.35):
        ode=stationary(delta)['Gamma'];value=closed_rate(delta)
        rows.append(dict(delta=delta,Gamma_ODE=ode,Gamma_closed=value,relative_difference=value/ode-1))
    nu=(np.sqrt(7)-1)/2;a=(1-nu)/2;b=1+nu/2
    j0=np.pi**2/np.exp(2*loggamma(a)+2*loggamma(b))
    constant=float(.5*np.pi**2*j0*j0/np.sin(np.pi*nu)**2)
    threshold=[]
    for k in (.005,.01,.02,.04):
        delta=np.sqrt((1+k*k)/2);b0=(np.pi*delta/(2*np.sinh(np.pi*delta/2)))**2
        value=closed_rate(delta);ode=stationary(delta)['Gamma']
        threshold.append(dict(k=k,delta=delta,Gamma=value,Gamma_ODE=ode,
            ratio_to_threshold_law=value/(constant*b0*b0*k)))
    result=dict(IDENT,run_id='2026-10-04-gpt-a-radiation-onset-closed-form',rows=rows,
        threshold_prefactor_excluding_B0_squared=constant,threshold_checks=threshold,
        elapsed_seconds=time.time()-start,
        provenance='Derived after seeing the stationary and driven-response results; evaluates the same coefficient, without a fitted parameter.')
    out=RAW/result['run_id'];out.mkdir(parents=True,exist_ok=True)
    (out/'closed_form.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
