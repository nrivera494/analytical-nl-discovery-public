#!/usr/bin/env python3
"""Unfitted pulse-width coefficients of frozen-soliton eigenvalue floors.
agent: gpt-b; model: gpt-6-astra; family: gpt.
Perturbation of isolated eigenvalues in the declared finite Fourier basis.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from soliton_fano_theory import grid_operators,spectral_covariance
from soliton_frozen_raman import frozen_covariance,source_matrix,KB,HBAR


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--reference',required=True)
    ap.add_argument('--output',required=True);args=ap.parse_args()
    start=time.monotonic();reference=json.loads(Path(args.reference).read_text())
    n=reference['n'];window=reference['window'];z=reference['points'][0]['z_over_LD']
    x,k,q,a,ft=grid_operators(n,window)
    spectra={'unit':np.ones(n),'absolute_k':abs(k),'k_squared':k*k}
    baths={};vac=None
    for key,spectrum in spectra.items():
        cov=np.fft.ifft(np.fft.ifftshift(spectrum)[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0).real
        source=np.zeros((2*n,2*n));source[n:,n:]=4*q[:,None]*cov*q[None,:]
        total,bath,m=frozen_covariance(a,source,z);baths[key]=bath
        if vac is None:vac=m@m.T
    _,_,amp=spectral_covariance(vac,q.astype(complex),ft)
    tr=.18*2*.0122**2*.032/(.0122**2+.032**2)
    ar=1/.032;br=1/.0122;cr=2*(br*br-ar*ar)/(ar*ar+br*br)**2
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',n=n,window=window,z_over_LD=z,
        TR_ps=tr,cR_ps2=cr,coefficients=[],checks=[],
        scope='Unfitted isolated-eigenvalue coefficients in the frozen finite basis; not a physical GNLSE remainder.')
    for temp in [0.,77.,300.]:
      rho=2*KB*temp*tr*1e-12/HBAR
      base=vac+rho*baths['unit']
      perturb=(tr*baths['absolute_k'] if temp==0 else
               rho*(cr+(HBAR*1e12/(KB*temp))**2/12)*baths['k_squared'])
      for name,projector in [('lambda_min',np.eye(2*n)),('lambda_gen',amp)]:
        with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
            matrix=projector@base@projector.T;delta=projector@perturb@projector.T
            vals,vecs=eigh(matrix);couplings=vecs.T@delta@vecs[:,0]
        first=float(couplings[0]);second=float(np.sum(couplings[1:]**2/(vals[0]-vals[1:])))
        coefficient=dict(temperature_K=temp,observable=name,limit=float(vals[0]),
            spectral_gap=float(vals[1]-vals[0]),leading_power=1 if temp==0 else 2,
            leading_coefficient=first,
            eigenvector_second_order_coefficient=second,
            second_coefficient_complete=(temp==0))
        out['coefficients'].append(coefficient)
        for row in reference['points']:
            if row['temperature_K']!=temp:continue
            width=row['T0_ps'];power=coefficient['leading_power']
            prediction=float(vals[0]+first/width**power)
            if temp==0:prediction+=second/width**2
            actual=row[name]
            out['checks'].append(dict(temperature_K=temp,T0_ps=width,observable=name,
                prediction=prediction,actual=actual,residual=actual-prediction,
                predicted_leading_excess=first/width**power,
                measured_excess=actual-float(vals[0])))
    out['wall_time_s']=time.monotonic()-start
    Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
