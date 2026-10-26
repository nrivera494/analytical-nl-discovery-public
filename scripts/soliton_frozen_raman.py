#!/usr/bin/env python3
"""Stationary soliton continuum + symmetrized Raman-source covariance.

agent: gpt-b; model: gpt-6-astra; family: gpt.
This is the frozen-Kerr propagator approximation, not full Raman propagation.
The analytic material spectrum is for theory quadrature. Native solver
checks use the unchanged fetched raman_bath_spectrum.jl helper.
"""
import argparse
import json
import os
from pathlib import Path
import time
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','2')
import numpy as np
from scipy.linalg import expm
from soliton_fano_theory import grid_operators, score_covariance

HBAR=1.054571817e-34
KB=1.380649e-23


def material_spectrum(k,T0_ps,temperature_K,fr=.18,tau1_ps=.0122,tau2_ps=.032):
    omega=k/T0_ps
    h=(tau1_ps**-2+tau2_ps**-2)/((tau2_ps**-1-1j*omega)**2+tau1_ps**-2)
    tr=fr*2*tau1_ps**2*tau2_ps/(tau1_ps**2+tau2_ps**2)
    imh=fr*abs(h.imag)
    if temperature_K==0:
        return imh
    arg=HBAR*abs(omega)*1e12/(2*KB*temperature_K)
    nonzero=arg>0
    spectrum=np.empty_like(k)
    spectrum[nonzero]=imh[nonzero]/np.tanh(arg[nonzero])
    spectrum[~nonzero]=2*KB*temperature_K*tr*1e-12/HBAR
    return spectrum


def source_matrix(k,q,T0_ps,temperature_K,white=False,unit=False):
    n=len(q)
    if unit:
        cov=np.eye(n)
    elif white:
        tr=.18*2*.0122**2*.032/(.0122**2+.032**2)
        cov=np.eye(n)*(2*KB*temperature_K*tr*1e-12/HBAR)
    else:
        s=np.fft.ifftshift(material_spectrum(k,T0_ps,temperature_K))
        cov=np.fft.ifft(s[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0).real
    source=np.zeros((2*n,2*n))
    source[n:,n:]=4*q[:,None]*cov*q[None,:]
    return source


def frozen_covariance(a,source,z):
    d=len(a)
    generator=np.block([[a,source],[np.zeros_like(a),-a.T]])
    prop=expm(generator*z)
    m=prop[:d,:d]
    bath=prop[:d,d:]@m.T
    bath=(bath+bath.T)/2
    return m@m.T+bath,bath,m


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=256)
    ap.add_argument('--window',type=float,default=40.)
    ap.add_argument('--z',nargs='+',type=float,default=[3*np.pi/2])
    ap.add_argument('--T0',nargs='+',type=float,default=[.125,.25,.5,1.,2.])
    ap.add_argument('--temperature',nargs='+',type=float,default=[0.,77.,300.])
    ap.add_argument('--white',action='store_true');ap.add_argument('--raw',required=True)
    args=ap.parse_args();dest=Path(args.raw);dest.mkdir(parents=True,exist_ok=True)
    x,k,q,a,ft=grid_operators(args.n,args.window)
    summary={'agent':'gpt-b','model':'gpt-6-astra','family':'gpt','n':args.n,'window':args.window,'frozen_mean':True,'points':[]}
    for T0 in args.T0:
      for temp in args.temperature:
        source=source_matrix(k,q,T0,temp,white=args.white)
        for z in args.z:
            start=time.monotonic();v,bath,m=frozen_covariance(a,source,z)
            row,mask,va=score_covariance(v,q.astype(complex),ft)
            g=ft.conj().T@(mask*(ft@q))
            gr=np.r_[g.real,g.imag]
            row['best_binary_Raman_part']=float(gr@bath@gr/np.vdot(g,g).real)
            row.update(T0_ps=T0,temperature_K=temp,z_over_LD=z,white=args.white,wall_time_s=time.monotonic()-start)
            summary['points'].append(row)
            name=f'T{T0:g}_K{temp:g}_z{z:.8g}'
            np.savez_compressed(dest/(name+'.npz'),x=x,k=k,q=q,V=v,VR=bath,Vamp=va,mask=mask)
            (dest/'summary.json').write_text(json.dumps(summary,indent=2))
            print(json.dumps({key:val for key,val in row.items() if not key.endswith('indices')}),flush=True)


if __name__=='__main__':main()
