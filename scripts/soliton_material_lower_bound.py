#!/usr/bin/env python3
"""One-sided material-spectrum bound in the frozen scalar soliton model.
agent: gpt-b; model: gpt-6-astra; family: gpt.
Numerical eigenvalues still need continuum certification/convergence.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from soliton_fano_theory import grid_operators,score_covariance
from soliton_frozen_raman import frozen_covariance,source_matrix,material_spectrum,KB,HBAR


def lower_spectrum(k,T0,temp,white=False):
    tau1=.0122;tau2=.032;fr=.18
    tr=fr*2*tau1*tau1*tau2/(tau1*tau1+tau2*tau2)
    cutoff=T0*np.sqrt(2*(tau1**-2-tau2**-2))
    if white:spectrum=np.full_like(k,2*KB*temp*tr*1e-12/HBAR)
    elif temp==0:spectrum=tr/T0*abs(k)
    else:
        arg=HBAR*abs(k)*1e12/(2*KB*temp*T0)
        spectrum=np.full_like(k,2*KB*temp*tr*1e-12/HBAR)
        nz=arg>0;spectrum[nz]=(tr/T0*abs(k[nz]))/np.tanh(arg[nz])
    return spectrum*(abs(k)<=cutoff),cutoff


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--T0',type=float,required=True)
    ap.add_argument('--temperature',type=float,required=True);ap.add_argument('--z',type=float,required=True)
    ap.add_argument('--n',type=int,default=256);ap.add_argument('--window',type=float,default=40.)
    ap.add_argument('--output',required=True);args=ap.parse_args()
    x,k,q,a,ft=grid_operators(args.n,args.window);rows=[]
    for kind in ['white_cutoff','linear_coth_cutoff','full_oscillator']:
        start=time.monotonic()
        lower,cutoff=lower_spectrum(k,args.T0,args.temperature,white=kind=='white_cutoff')
        if kind=='full_oscillator':lower=material_spectrum(k,args.T0,args.temperature)
        cov=np.fft.ifft(np.fft.ifftshift(lower)[:,None]*np.fft.fft(np.eye(args.n),axis=0),axis=0).real
        source=np.zeros((2*args.n,2*args.n));source[args.n:,args.n:]=4*q[:,None]*cov*q[None,:]
        v,_,_=frozen_covariance(a,source,args.z)
        row,_,_=score_covariance(v,q.astype(complex),ft)
        row.update(source_model=kind,material_cutoff_k=cutoff,wall_time_s=time.monotonic()-start)
        rows.append(row)
    checkk=np.r_[0.,np.geomspace(1e-8,1000,10000)]
    lower,_=lower_spectrum(checkk,args.T0,args.temperature)
    residual=material_spectrum(checkk,args.T0,args.temperature)-lower
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',T0_ps=args.T0,temperature_K=args.temperature,
        z_over_LD=args.z,n=args.n,window=args.window,points=rows,
        material_spectrum_min_check=float(residual.min()),
        scope='Rigorous spectrum/covariance ordering in the frozen model; numerical Ritz values are not interval certificates.')
    Path(args.output).write_text(json.dumps(out,indent=2))
    print(json.dumps({**out,'points':[{k:v for k,v in r.items() if not k.endswith('indices')} for r in rows]}),flush=True)


if __name__=='__main__':main()
