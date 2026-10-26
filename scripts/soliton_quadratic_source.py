#!/usr/bin/env python3
"""Sharper polynomial-coth material minorant in the frozen soliton model.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from soliton_fano_theory import grid_operators,score_covariance
from soliton_frozen_raman import frozen_covariance,material_spectrum,KB,HBAR


def quadratic_lower(k,T0,temp):
    ar=1/.032;br=1/.0122;d=ar*ar+br*br;fr=.18
    tr=2*fr*ar/d;cr=2*(br*br-ar*ar)/(d*d)
    if cr*d<=1:raise ValueError('The quadratic minorant requires tau2 > sqrt(3)*tau1')
    cutoff=np.sqrt((cr*cr*d*d-1)/cr)
    omega=abs(k)/T0
    linear=tr*omega
    if temp>0:
        arg=HBAR*omega*1e12/(2*KB*temp)
        nonzero=arg>0
        linear[nonzero]/=np.tanh(arg[nonzero])
        linear[~nonzero]=2*KB*temp*tr*1e-12/HBAR
    return linear*(1+cr*omega*omega)*(omega<=cutoff),dict(cR_ps2=cr,cutoff_per_ps=cutoff,cutoff_k=T0*cutoff)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--T0',type=float,required=True)
    ap.add_argument('--temperature',type=float,required=True);ap.add_argument('--z',type=float,required=True)
    ap.add_argument('--n',type=int,default=256);ap.add_argument('--window',type=float,default=40.)
    ap.add_argument('--output',required=True);args=ap.parse_args();started=time.monotonic()
    x,k,q,a,ft=grid_operators(args.n,args.window);rows=[]
    for name in ['quadratic_cutoff','full_oscillator']:
        spec,material=quadratic_lower(k,args.T0,args.temperature)
        if name=='full_oscillator':spec=material_spectrum(k,args.T0,args.temperature)
        cov=np.fft.ifft(np.fft.ifftshift(spec)[:,None]*np.fft.fft(np.eye(args.n),axis=0),axis=0).real
        source=np.zeros((2*args.n,2*args.n));source[args.n:,args.n:]=4*q[:,None]*cov*q[None,:]
        v,_,_=frozen_covariance(a,source,args.z);row,_,_=score_covariance(v,q.astype(complex),ft)
        row['source_model']=name;rows.append(row)
    checkk=np.r_[0.,np.geomspace(1e-8,1000,10000)]
    low,_=quadratic_lower(checkk,args.T0,args.temperature)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',T0_ps=args.T0,temperature_K=args.temperature,
        z_over_LD=args.z,n=args.n,window=args.window,material=material,points=rows,
        minimum_source_residual=float(np.min(material_spectrum(checkk,args.T0,args.temperature)-low)),
        scope='Exact material-source ordering in the frozen model; regular fixed-readout source error O(T0^-4) at positive temperature, O(T0^-5) at zero temperature. No physical one-sided remainder or continuum eigenvalue enclosure.',
        wall_time_s=time.monotonic()-started)
    Path(args.output).write_text(json.dumps(out,indent=2))
    print(json.dumps({**out,'points':[{k:v for k,v in row.items() if not k.endswith('_indices')} for row in rows]}),flush=True)


if __name__=='__main__':main()
