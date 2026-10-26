#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Check faint-mask validity and optimize exact counts of a Gaussian state.

The finite-step quadrature covariance can slightly violate uncertainty. We
record the violation and add the minimal isotropic quadrature noise (plus a
small numerical margin) to define a nearby physical Gaussian state. This is
an explicitly labeled diagnostic, not a silent change to the reference V.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse
import json
from pathlib import Path
import numpy as np
from scipy import linalg as la
from readout_bounds import binary_search, eigenvector_bound, moment_certificate, fano
from readout_smooth_dual import smooth_dual

def gaussian_count_case(path,do_bound=True):
    path=Path(path);data=np.load(path);v=data['V'];n=data['nbar'];m=len(n)
    J=np.block([[np.zeros((m,m)),np.eye(m)],[-np.eye(m),np.zeros((m,m))]])
    umin=float(la.eigh(v+1j*J,subset_by_index=(0,0),eigvals_only=True,check_finite=False)[0])
    completion=max(0.,-umin)+1e-10
    vp=v+completion*np.eye(2*m)
    xx,pp,xp,px=vp[:m,:m],vp[m:,m:],vp[:m,m:],vp[m:,:m]
    normal=(xx+pp+1j*(xp-px)-2*np.eye(m))/4
    anomalous=(xx-pp+1j*(xp+px))/4
    spontaneous=np.real(np.diag(normal))
    assert spontaneous.min()>-1e-9
    mean=n+spontaneous
    b=np.sqrt(n)
    linear=b[:,None]*xx*b[None,:]
    quadratic=np.abs(normal)**2+np.abs(anomalous)**2+np.diag(spontaneous)
    total=linear+quadratic
    ac=total/np.sqrt(np.outer(mean,mean))
    base=float(la.eigh(ac,subset_by_index=(0,0),eigvals_only=True)[0])
    _,_,_,seeds=eigenvector_bound(ac,mean)
    best,mask,search=binary_search(ac,mean,seeds)
    flinear=fano(linear,n,mask)
    lower=base;dual=np.zeros_like(ac);bd={}
    if do_bound:
        lower,dual,bd=moment_certificate(ac,mean,best,base,max_core=72)
        if best-lower>2e-5:
            sl,sk,_,sd=smooth_dual(ac,mean)
            bd['smooth']=sd
            if sl>lower: lower,dual=sl,sk
    maskfile=path.with_suffix('.bounds.npz')
    formal=np.load(maskfile)['best_mask'] if maskfile.exists() else np.load(path.with_suffix('.score.npz'))['mask']
    report=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',label=path.stem,
        counting_model='Exact photon-count moments of a nearby physical Gaussian covariance',
        uncertainty_min_eigenvalue=umin,isotropic_covariance_completion=completion,
        total_spontaneous_photons=float(sum(spontaneous)),
        original_formal_mask_coherent_photons=float(n@formal),
        original_formal_mask_spontaneous_photons=float(spontaneous@formal),
        original_formal_mask_Gaussian_F=fano(total,mean,formal),
        best_Gaussian_F=best,best_Gaussian_bound=lower,
        best_mask_coherent_photons=float(n@mask),best_mask_spontaneous_photons=float(spontaneous@mask),
        best_mask_transmitted_fraction=float(n@mask/sum(n)),
        best_mask_linearized_F_on_completed_covariance=flinear,
        best_mask_count_correction=best-flinear,
        gap_bound_dB=float(10*np.log10(best/lower)) if lower>0 else None,
        binary_search=search,bound_details=bd)
    path.with_suffix('.gaussian.json').write_text(json.dumps(report,indent=2)+'\n')
    np.savez_compressed(path.with_suffix('.gaussian.npz'),mask=mask,dual_K=dual,
                        spontaneous_photons=spontaneous)
    print(json.dumps({k:report[k] for k in ['label','original_formal_mask_coherent_photons',
        'original_formal_mask_Gaussian_F','best_Gaussian_F','best_Gaussian_bound','gap_bound_dB']}),flush=True)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('paths',nargs='+');ap.add_argument('--no-bound',action='store_true')
    args=ap.parse_args()
    for path in args.paths: gaussian_count_case(path,not args.no_bound)
