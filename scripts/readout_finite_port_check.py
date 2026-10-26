#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Finite brightness approach to a squeezed, dark passive direction."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar

s=.3
nu=(s+1/s-2)/4
m=(s-1/s)/4
q0=nu*(nu+1)+m*m
c=q0-s*nu
delta=1-s
rows=[]
for photons in np.logspace(2,12,11):
    def f(log_t):
        t=np.exp(log_t);v=s+delta*t
        nf=(1-t)*nu;mf=(1-t)*m
        return (photons*t*v+nf*(nf+1)+mf*mf)/(photons*t+nf)
    optimum=minimize_scalar(f,bounds=(-40,0),method='bounded',options={'xatol':1e-12})
    leading=2*np.sqrt(delta*c/photons)
    rows.append(dict(coherent_input_photons=float(photons),port_fraction=float(np.exp(optimum.x)),
        port_coherent_photons=float(photons*np.exp(optimum.x)),best_F=float(optimum.fun),
        excess_above_lambda_pass=float(optimum.fun-s),leading_excess=float(leading),
        absolute_remainder=float(optimum.fun-s-leading)))
large=rows[-6:]
power=float(np.polyfit(np.log([r['coherent_input_photons'] for r in large]),
    np.log([r['excess_above_lambda_pass'] for r in large]),1)[0])
assert abs(power+.5)<1e-3
result=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',
    model_description='One bright coherent mode and one independent squeezed-vacuum mode; arbitrary real passive mixing followed by counting.',
    squeezed_variance=s,vacuum_variance=1.,lambda_pass=s,leading_coefficient=float(2*np.sqrt(delta*c)),
    predicted_exponent=-.5,measured_exponent=power,rows=rows)
out=Path('~/analytical-nl-discovery-data/2026-10-10-gpt-a-readout-reference/finite-port-check.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(predicted_exponent=-.5,measured_exponent=power,largest_photon_excess=rows[-1]['excess_above_lambda_pass'])))
