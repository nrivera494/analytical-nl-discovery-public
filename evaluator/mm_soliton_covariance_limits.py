#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.
Known limits, weak-minority asymptotics, and quadrature convergence.
"""
import argparse
from pathlib import Path
import time
import numpy as np
from mm_soliton_covariance import family,diffusion,readout,polynomial,spectrum,dump,IDENTITY


def main():
    ap=argparse.ArgumentParser();ap.add_argument("out");args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);started=time.time()
    scalar=family([[1.]],[2.],b=[1.]);D=diffusion(scalar,[[1.]],np.array([0.]),gain=[.1])
    scalar_target=np.array([.4,.1*(np.pi**2+12)/36,.1*np.pi**2/12,.1/3])
    scalar_check=dict(gain_diagonal_over_q=np.diag(D['gain']),gain_analytic_over_q=scalar_target,
                      gain_max_relative_error=np.max(np.abs(np.diag(D['gain'])/scalar_target-1)),
                      raman_diagonal_over_q=np.diag(D['raman']),
                      raman_timing_cubic_over_q=D['raman'][3,3]/3,
                      round1_reference_run='2026-10-04-gpt-b-soliton-baselines',
                      round1_raman_frequency_diffusion_over_q=.0307109209)
    scalar_check['round1_raman_relative_error']=D['raman'][3,3]/scalar_check['round1_raman_frequency_diffusion_over_q']-1
    rows=[]
    ps=[.002,.004,.008,.016,.032,.064]
    for c in [.5,.75]:
        for p in ps:
            C=np.array([[1.,1.],[1.,c]]);s=np.array([[1.,.5],[.5,c]])
            f=family(C,[2*(1-p),2*p]); eta=c-1
            for delta in [0.,1.,3.]:
                d=np.array([0.,delta]);X=readout(f,d);A=X@f['A']@np.linalg.inv(X)
                ds=diffusion(f,s,d)
                co={k:polynomial(A,X@ds[k]@X.T) for k in ['gain','raman']}
                F=1/np.cosh(f['t'])
                FT=f['dt']*np.fft.fft(F**2*np.exp(-1j*delta*f['t']))
                J=np.sum(spectrum(f['k'])*abs(FT)**2)/(len(F)*f['dt'])
                predG=.1*eta**2*2**3*p/54
                predR=eta**2*2**2*p*J/108
                rows.append(dict(self_overlap=c,p=p,delta=delta,
                    h_p=2*np.array([-1.,1.])@f['K']@np.array([-1.,1.]),h_p_leading=eta*4/6,
                    gain_phase_cubic=co['gain'][2,5,5],gain_leading_p=predG,
                    raman_phase_cubic=co['raman'][2,5,5],raman_leading_p=predR,
                    gain_relative_error=co['gain'][2,5,5]/predG-1,
                    raman_relative_error=co['raman'][2,5,5]/predR-1))
    exponents=[]
    for c in [.5,.75]:
        for delta in [0.,1.,3.]:
            sub=[r for r in rows if r['self_overlap']==c and r['delta']==delta and r['p']<=.016]
            exponents.append(dict(self_overlap=c,delta=delta,p_max=.016,
                 gain_relative_error_power=np.polyfit(np.log([r['p'] for r in sub]),np.log(np.abs([r['gain_relative_error'] for r in sub])),1)[0],
                 raman_relative_error_power=np.polyfit(np.log([r['p'] for r in sub]),np.log(np.abs([r['raman_relative_error'] for r in sub])),1)[0]))
    conv=[]
    for nt,window in [(256,48.),(512,48.),(1024,48.),(1024,64.),(8192,48.)]:
        f=family([[1.,1.],[1.,.5]],[1.6,.4],nt=nt,halfwindow=window/2)
        ds=diffusion(f,np.array([[1.,.5],[.5,.5]]),np.array([0.,2.6848995997248095]))
        conv.append(dict(nt=nt,window=window,dt_fs=window/nt*.5*1000,
            residual_relative=f['residual_relative'],dual_identity_relative=f['dual_identity_relative'],
            gain_diagonal=np.diag(ds['gain']),raman_diagonal=np.diag(ds['raman'])))
        if nt in [1024,8192] and window==48.:
            X=readout(f,np.array([0.,2.6848995997248095]))
            np.savez_compressed(out/f'grin02_fine_{nt}.npz',**f,readout=X,d=[0.,2.6848995997248095],s=[[1.,.5],[.5,.5]])
    drift_tests=[]
    for temp in [0.,77.,300.]:
        f=family([[1.,1.],[1.,.5]],[1.6,.4])
        for delta in [0.,1.,2.,3.]:
            d=np.array([0.,delta]);X=readout(f,d)
            dr=X@diffusion(f,np.array([[1.,.5],[.5,.5]]),d,temperature=temp)['raman']@X.T
            drift_tests.append(dict(temperature_K=temp,delta=delta,Dpp_over_q=dr[4,4],
                Dvv_over_q=dr[3,3]+2*delta*dr[3,4]+delta**2*dr[4,4],
                Dvp_over_q=dr[3,4]+delta*dr[4,4]))
    dump(out/'summary.json',dict(**IDENTITY,task='T-20261008-gpt-b-01',scalar=scalar_check,
        weak_minority=rows,error_scaling=exponents,quadrature_convergence=conv,
        walkoff_temperature=drift_tests,elapsed_seconds=time.time()-started))
    print('Scalar gain error',scalar_check['gain_max_relative_error'])
    print('Scalar Raman error',scalar_check['round1_raman_relative_error'])
    print('Error exponents',exponents)


if __name__=='__main__':main()
