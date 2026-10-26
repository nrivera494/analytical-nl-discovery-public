#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt

Supplemental zero-walk-off LP03 detuning corollary. Analytic intervals are frozen
before its response or finite-admixture runs; this is a later preregistration.
"""
import json, sys
from pathlib import Path
import numpy as np
from p002_nextorder import IDENT, ROOT, RAW, model, integrate, sech_integral

PREFIX='2026-10-04-gpt-a-nextorder-detuning'
MUS=(-.7,-7.,-47.)
ZS=(0.,5.,11.,17.)

def freeze():
    nu=(np.sqrt(7)-1)/2;lam=nu*nu/2;gap=.5-lam
    overlap=sech_integral(nu+1)**2/sech_integral(2*nu)
    remainder=2-overlap
    source_continuum_norm_squared=16/15-16*gap*gap*overlap
    rows=[]
    for mu in MUS:
        upper_extra=min(4*remainder,source_continuum_norm_squared/(4*(.5-mu)**2))
        for z in ZS:
            kb=4*gap*gap*overlap*np.sin((gap-mu)*z/2)**2/(gap-mu)**2
            rows.append(dict(mu=mu,zeta=z,K_lower=float(kb),K_upper=float(kb+upper_extra),
                continuum_upper=float(upper_extra)))
    d=dict(IDENT,run_id=PREFIX+'-prediction',task='T-20261004-claude-interactive-07',
        nu3=nu,lambda3=lam,gap=gap,ground_overlap_squared=overlap,
        continuum_source_norm_squared=source_continuum_norm_squared,
        ratios=[.0002,.0006,.002],output_planes=ZS,rows=rows,
        prediction='The leading LP03 energy coefficient lies in every analytic interval. Full LP03 energy is r^2 K + O(r^3); error has epsilon exponent 6.',
        prior_evidence='Designed after main and half-boundary runs; new carrier mismatches and output planes have not been evaluated.')
    out=ROOT/'runs'/(PREFIX+'-prediction');out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d,indent=2))

def response():
    out=RAW/(PREFIX+'-response')
    for j,mu in enumerate(MUS,1):
        p=model();p['mu']=mu
        integrate(f'mu{j}',p,out,zs=ZS,dz=.0025 if abs(mu)>20 else .005)
    p=model();p['mu']=MUS[-1]
    integrate('mu3_halfstep',p,out,zs=ZS,dz=.00125)

if __name__=='__main__':
    {'freeze':freeze,'response':response}[sys.argv[1]]()
