#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Independent finite-dimensional checks of the readout algebra and gates."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse
import json
from pathlib import Path
import numpy as np
from scipy import linalg as la
from readout_bounds import passive_eigenvalue, loweig, eigenvector_bound, fano

def realification(u):
    return np.block([[u.real,-u.imag],[u.imag,u.real]])

def check_algebra():
    rng=np.random.default_rng(2026101003)
    rows=[]
    for case in range(24):
        m=6
        u,_=la.qr(rng.normal(size=(m,m))+1j*rng.normal(size=(m,m)))
        r=rng.uniform(-1.4,1.4,m)
        nu=rng.uniform(1,2.5,m)
        s=realification(u)@np.diag(np.r_[np.exp(r),np.exp(-r)])
        v=(s*np.r_[nu,nu])@s.T
        alpha=(rng.normal(size=m)+1j*rng.normal(size=m))*1e5
        phase=np.diag(np.exp(1j*np.angle(alpha)))
        rot=realification(phase)
        vl=rot.T@v@rot
        n=np.abs(alpha)**2
        lmin=float(loweig(v)[0]);lp,_,_=passive_eigenvalue(vl,n)
        lg=float(loweig(vl[:m,:m])[0])
        assert lmin<=lp+1e-10 and lp<=lg+1e-10
        # Three populated frequency blocks, each with two signal modes.
        qb=np.zeros((2*m,m+m//2));qb[:m,:m]=np.eye(m)
        for block in range(m//2):
            i,j=2*block,2*block+1
            qb[m+i,m+block]=np.sqrt(n[j]/(n[i]+n[j]))
            qb[m+j,m+block]=-np.sqrt(n[i]/(n[i]+n[j]))
        block_limit=float(loweig(qb.T@vl@qb)[0])
        assert lp<=block_limit+1e-10 and block_limit<=lg+1e-10
        # Construct an arbitrary reachable direction, including exactly
        # dark-to-one-port directions in half the cases.
        h=rng.normal(size=m)+1j*rng.normal(size=m)
        h-=1j*alpha*(np.vdot(alpha,h).imag/np.vdot(alpha,alpha).real)
        if case%2==0:
            h-=alpha*(np.vdot(alpha,h).real/np.vdot(alpha,alpha).real)
        h/=la.norm(h)
        n0=np.vdot(alpha,alpha).real
        H=(np.outer(h,alpha.conj())+np.outer(alpha,h.conj()))/n0-np.vdot(alpha,h).real*np.outer(alpha,alpha.conj())/n0**2
        w,uu=la.eigh(H)
        beta=uu.conj().T@alpha
        reconstructed=uu@(w*beta)
        error=la.norm(reconstructed-h)
        shot=float(np.sum(w*w*np.abs(beta)**2))
        assert error<1e-10 and abs(shot-1)<1e-10
        # Explicit one-port construction for a bright direction.
        hb=h if abs(np.vdot(h,alpha))>1e-3 else h+.02*alpha/la.norm(alpha)
        hb/=la.norm(hb)
        if np.vdot(hb,alpha).real<0: hb=-hb
        bmean=np.vdot(hb,alpha)
        q=hb*np.exp(1j*np.angle(bmean))
        assert abs(np.vdot(q,alpha).imag)<1e-8
        rows.append(dict(case=case,lambda_min=lmin,lambda_pass=lp,lambda_gen=lg,
            frequency_preserving_block_limit=block_limit,
            multiport_reconstruction_error=float(error),weighted_shot_noise=shot,
            one_port_mean_photons=float(abs(bmean)**2),dark_target=case%2==0))
    # Exactly diagonal and arbitrarily disconnected covariance examples.
    diagonal=np.diag([.3,.7,1.2,2.0]);n=np.array([2.,5.,9.,13.])
    be,_,_,_=eigenvector_bound(diagonal,n)
    assert abs(be-.3)<1e-8
    m=12;mask=(np.arange(m)%2==0);v=mask/la.norm(mask)
    a=1.5*np.eye(m)-1.2*np.outer(v,v)
    masks=((np.arange(1,2**m)[:,None]>>np.arange(m))&1)
    values=np.einsum('bi,ij,bj->b',masks,a,masks)/np.sum(masks,axis=1)
    best=masks[np.argmin(values)].astype(bool)
    assert np.array_equal(best,mask)
    # Noisy single-mode signal with an ancillary vacuum: attenuation lowers
    # F toward one, refuting an unqualified signal-only passive bound of two.
    thermal=dict(signal_only_passive=2.,attenuated_F_at_half_transmission=1.5,
                 vacuum_augmented_passive=1.)
    return dict(mixed_gaussian_cases=rows,diagonal_bound=be,
        disconnected_example=dict(bins=m,intervals=6,exact_binary_F=float(values.min())),
        vacuum_ancilla_example=thermal)

def covariance_checks(raw,labels):
    rows=[]
    for label in labels:
        d=np.load(raw/(label+'.npz'))
        v=d['V'];n=len(d['nbar']);identity=np.eye(n)
        J=np.block([[np.zeros((n,n)),identity],[-identity,np.zeros((n,n))]])
        uncertainty=float(la.eigh(v+1j*J,subset_by_index=(0,0),eigvals_only=True,check_finite=False)[0])
        symplectic=float(la.norm(v@J@v-J,'fro')/la.norm(J,'fro'))
        normal=float(np.sqrt(d['nbar'])@v[:n,:n]@np.sqrt(d['nbar'])/sum(d['nbar']))
        finite=bool(np.all(np.isfinite(v)))
        # Cross-check the BLAS multiplication with unoptimized explicit
        # contractions on small sampled submatrices (including tiny entries).
        sub=v[np.ix_(np.arange(0,2*n,max(1,n//16)),np.arange(0,2*n,max(1,n//16)))]
        direct=np.einsum('ik,kj->ij',sub,sub,optimize=False)
        multiplication_error=float(np.max(np.abs(sub@sub-direct))/max(1.,np.max(np.abs(direct))))
        rows.append(dict(label=label,uncertainty_min_eigenvalue=uncertainty,
            pure_covariance_symplectic_relative_defect=symplectic,full_count_F=normal,
            all_finite=finite,BLAS_vs_explicit_relative_error=multiplication_error))
        assert finite and multiplication_error<1e-11
    return rows

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('raw');ap.add_argument('labels',nargs='*');args=ap.parse_args()
    raw=Path(args.raw)
    result=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',seed=2026101003,
        algebra=check_algebra(),covariance_checks=covariance_checks(raw,args.labels))
    (raw/'algebra-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
