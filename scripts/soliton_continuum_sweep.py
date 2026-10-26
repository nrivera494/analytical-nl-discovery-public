#!/usr/bin/env python3
"""Distance curves for the exact Kerr and white-source soliton reductions.

agent: gpt-b; model: gpt-6-astra; family: gpt.
The matrix recurrence evaluates the constant-generator semigroup, not the
nonlinear fibre equation. Jost passbands are evaluated independently.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from scipy.optimize import minimize_scalar
from soliton_fano_theory import grid_operators, score_covariance
from soliton_frozen_raman import source_matrix, frozen_covariance, KB, HBAR
from soliton_jost_filter import bandpass


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True)
    ap.add_argument('--n',type=int,default=512);ap.add_argument('--window',type=float,default=80.)
    ap.add_argument('--dz',type=float,default=.25);ap.add_argument('--max-z',type=float,default=8.)
    args=ap.parse_args();dest=Path(args.raw);dest.mkdir(parents=True,exist_ok=True)
    x,k,q,a,ft=grid_operators(args.n,args.window)
    tr=.18*2*.0122**2*.032/(.0122**2+.032**2)
    source=source_matrix(k,q,1.,300.,unit=True)
    _,stepbath,step=frozen_covariance(a,source,args.dz)
    prop=np.eye(2*args.n);bath=np.zeros_like(prop)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',n=args.n,
             window=args.window,dz=args.dz,TR_ps=tr,points=[])
    started=time.monotonic()
    for iz in range(round(args.max_z/args.dz)+1):
        z=iz*args.dz
        if iz:
            with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
                prop=step@prop;bath=step@bath@step.T+stepbath
            bath=(bath+bath.T)/2
        with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
            vac=prop@prop.T
        for temp in [0.,77.,300.]:
            rho=2*KB*temp*tr*1e-12/HBAR
            row,mask,va=score_covariance(vac+rho*bath,q.astype(complex),ft)
            if z==0:edge=6.;fedge=1.
            else:
                opt=minimize_scalar(lambda edge:bandpass(z,edge,order=80,rho=rho),
                    bounds=(.2,2.5),method='bounded',options={'xatol':2e-5})
                edge=float(opt.x);fedge=bandpass(z,edge,order=160,rho=rho)
            row.update(z_over_LD=z,temperature_K=temp,rho=rho,white_source=True,
                       optimized_centered_edge=edge,centered_passband_F=fedge,
                       centered_passband_dB=float(10*np.log10(fedge)),
                       zero_temperature_means_long_pulse_Kerr_limit=(temp==0))
            out['points'].append(row)
            print(json.dumps({key:val for key,val in row.items() if not key.endswith('indices')}),flush=True)
        out['wall_time_s']=time.monotonic()-started
        (dest/'summary.json').write_text(json.dumps(out,indent=2))
    np.savez_compressed(dest/'last_covariance.npz',q=q,k=k,Vvac=vac,W=bath)


if __name__=='__main__':main()
