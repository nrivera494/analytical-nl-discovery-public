#!/usr/bin/env python3
"""Optimize continuous edges of symmetric disconnected binary soliton filters.
agent: gpt-b; model: gpt-6-astra; family: gpt.
This supplies achieved upper values, not a global optimality certificate.
"""
import json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from soliton_jost_filter import (quadrature,even_coefficient,continuum_grams,
    white_source_gram,integrated_trig,sech,C)
from soliton_fano_theory import grid_operators,score_covariance
from soliton_frozen_raman import source_matrix,frozen_covariance


def union_value(z,edges,rho=0.,order=32):
    edges=np.asarray(edges)
    if edges[0]<.1 or edges[-1]>6 or np.any(np.diff(edges)<.003):return 1e3
    signs=np.ones(len(edges));signs[1::2]=-1
    k,w=quadrature(edges,order=order,cutoff=10.)
    b=sum(sign*even_coefficient(k,a) for sign,a in zip(signs,edges))
    aa=float(signs@(np.tanh(C*edges)-C*edges*sech(C*edges)**2))
    energy=float(2*signs@np.tanh(C*edges))
    rd,rs=continuum_grams(k);phase=(1+k*k)*z/2
    v0=w*b;vc=v0*np.cos(phase);vs=v0*np.sin(phase)
    with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
        regular=vc@rd@vc+vs@rs@vs-v0@rd@v0
        cross=-2*aa*np.sum((vc-v0)*np.pi*sech(C*k))
        bath=0.
        if rho:
            ss,_=integrated_trig(k,z)
            bath=4*rho*(v0@(white_source_gram(k)*ss)@v0)
    result=1+(cross+regular+bath)/energy
    if not np.isfinite(result):raise FloatingPointError('union filter')
    return float(result)


def main():
    dest=Path(sys.argv[1]);out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=[])
    x,k,q,a,ft=grid_operators(256,40.)
    for z,rho in [(3*np.pi/2,0.),(3*np.pi/2,.11483961911590272),(5.25,.11483961911590272)]:
        source=source_matrix(k,q,1.,300.,unit=True)*rho
        v,_,_=frozen_covariance(a,source,z)
        reference,_,_=score_covariance(v,q.astype(complex),ft)
        for sidebands in [2,4]:
            if z<5:edges=np.array([.7,1.3,1.55,2.1,2.25,2.65,2.75,3.1,3.2])[:2*sidebands+1]
            else:edges=np.array([.65,1.15,1.5,1.95,2.1,2.5,2.6,2.9,3.0])[:2*sidebands+1]
            start=time.monotonic()
            opt=minimize(lambda p:union_value(z,p,rho,order=24),edges,method='Nelder-Mead',
                options={'maxiter':1600,'xatol':1e-5,'fatol':1e-9})
            fine=minimize(lambda p:union_value(z,p,rho,order=48),opt.x,method='Nelder-Mead',
                options={'maxiter':800,'xatol':1e-5,'fatol':1e-9})
            values={str(order):union_value(z,fine.x,rho,order=order) for order in [48,96,192]}
            row=dict(z_over_LD=z,rho=rho,sidebands_per_side=sidebands,positive_edges=fine.x.tolist(),
                F_by_quadrature_order=values,F=values['192'],F_dB=float(10*np.log10(values['192'])),
                lambda_min=reference['lambda_min'],lambda_pass=reference['lambda_pass'],
                lambda_gen=reference['lambda_gen'],matrix_reference_n=256,matrix_reference_window=40.,
                gap_formula_to_achieved_dB=float(10*np.log10(values['192']/reference['lambda_gen'])),
                gap_lambda_min_to_achieved_dB=float(10*np.log10(values['192']/reference['lambda_min'])),
                optimizer_success=bool(fine.success),global_optimality_certified=False,
                wall_time_s=time.monotonic()-start)
            out['points'].append(row);dest.write_text(json.dumps(out,indent=2));print(json.dumps(row),flush=True)


if __name__=='__main__':main()
