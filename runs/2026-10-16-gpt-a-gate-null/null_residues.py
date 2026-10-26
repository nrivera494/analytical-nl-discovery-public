#!/usr/bin/env python3
"""agent=gpt-a; model=gpt-6-astra; family=gpt.
Exact Fourier transform of an analytically gated, TOD-free N=2 breather.
This tests leakage of the observable, not a TOD propagation or radiation yield.
"""
from pathlib import Path
import json
import mpmath as mp
import yaml
import numpy as np
from scipy.fft import ifft
from scipy.special import expit

mp.mp.dps=100
folder=Path(__file__).resolve().parent
identity=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',run_id=folder.name)
z=3*mp.pi/4
d=mp.acos(mp.sqrt(3)-1)/2
a=mp.acosh(1+mp.sqrt(3))/2
poles=[1j*d,1j*(mp.pi-d),a+1j*mp.pi/2,-a+1j*mp.pi/2]

def numerator(t):
    return 2*mp.exp(.5j*z)*(mp.cosh(3*t)+3*mp.exp(4j*z)*mp.cosh(t))

def u(t):
    return numerator(t)/(mp.cosh(4*t)+4*mp.cosh(2*t)+3*mp.cos(4*z))

def gate(t,R):
    return 1/(1+mp.exp(-2*(t-R)))+1/(1+mp.exp(2*(t+R)))

def poles_residues(R):
    loc=list(poles)
    residues=[numerator(t)/(4*mp.sinh(4*t)+8*mp.sinh(2*t))*gate(t,R) for t in poles]
    # Gate residues, multiplied by the regular breather.
    for t,sgn in [(R+1j*mp.pi/2,1),(-R+1j*mp.pi/2,-1)]:
        loc.append(t);residues.append(sgn*u(t)/2)
    return loc,residues

def spectrum(w,R):
    loc,res=poles_residues(R)
    # u(t+i*pi)=-u(t), g(t+i*pi)=g(t): rectangular contour identity.
    return 2*mp.pi*1j*sum(c*mp.exp(1j*w*t) for t,c in zip(loc,res))/(1+mp.exp(-mp.pi*w))

def band_fraction(delta,R):
    wmin=1/(6*delta)
    loc,res=poles_residues(R)
    total=0
    # Expand (1+exp(-pi*w))^-2. At smallest wmin used, neglected terms < 1e-100.
    for m in range(10):
        subtotal=0
        for j,t in enumerate(loc):
            for k,v in enumerate(loc):
                lam=-1j*(t-mp.conj(v))+m*mp.pi
                subtotal+=res[j]*mp.conj(res[k])*mp.exp(-lam*wmin)/lam
        total+=(-1)**m*(m+1)*subtotal
    # Parseval, and total launched norm E0=2: (2*pi)^2/(2*pi*2)=pi.
    return mp.pi*mp.re(total)

rows=[]
for R in [15,20]:
    for delta_text in ['0.01','0.007','0.005','0.004','0.003','0.002','0.001','0.0005','0.0001']:
        delta=mp.mpf(delta_text);value=band_fraction(delta,R)
        rows.append(dict(gate_radius=R,delta3=float(delta),eta=mp.nstr(value,25),
            log_eta=float(mp.log(value)),delta_log_eta=float(delta*mp.log(value))))
summary=dict(**identity,precision_decimal_digits=mp.mp.dps,
    experiment='TOD-free null: parameter delta3 only sets the moving band edge; no radiation exists',
    z_final=float(z),exact_strip=float(d),card_printed_decimal=.374664,
    null_limit_delta_log_eta=float(-d/3),rows=rows,
    complex_gate_at_nearest_pole={str(R):[float(mp.re(gate(1j*d,R))),float(mp.im(gate(1j*d,R)))] for R in [15,20]},
    derivation='For fixed R, the gate leaves the breather pole at i*d. Its squared Fourier tail decays as exp(-2*d*w). Integrating w >= 1/(6*delta3) gives exp(-d/(3*delta3)).',
    limitation='A null-background obstruction to interpreting the fixed-gate observable as a radiation asymptotic; not by itself a full-TOD counterexample.')
# Independent direct Fourier check in a region where Float64 resolves the tiny
# gated field. The 100-digit residue result is used for the much deeper tail.
window=160.;n=16384;t=(np.arange(n)-n//2)*window/n
zf=float(z)
field=2*np.exp(.5j*zf)*(np.cosh(3*t)+3*np.exp(4j*zf)*np.cosh(t))/(np.cosh(4*t)+4*np.cosh(2*t)+3*np.cos(4*zf))
g=expit(2*(t-15))+expit(-2*(t+15))
fourier=ifft(field*g)*window
checks=[]
for k in [50,100,200]:
    omega=2*np.pi*k/window
    direct=fourier[k]*np.exp(-1j*omega*window/2)
    contour=complex(spectrum(mp.mpf(str(omega)),15))
    checks.append(dict(w=omega,absolute_error=abs(direct-contour),relative_error=abs(direct/contour-1)))
summary['fourier_crosscheck']=checks
(folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(folder/'config.yaml').write_text(yaml.safe_dump(dict(**identity,z_final='3*pi/4',precision=100,
    gates=[15,20],observable='integral of gated exact NLSE spectrum at w>=1/(6*delta3), divided by 2'),sort_keys=False))
(folder/'meta.yaml').write_text(yaml.safe_dump(dict(**identity,solver_commit='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',
    solver_dirty=False,implementation='mpmath contour residues; no propagation',raw_location='none; exact formulas and summary only',
    claim='C-20261016-claude-b-01'),sort_keys=False))
for r in rows: print(r)
