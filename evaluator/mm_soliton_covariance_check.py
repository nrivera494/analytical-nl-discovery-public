#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.
Contract actual full-field adjoints and compare against frozen coefficients.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
from scipy.sparse.linalg import LinearOperator, eigsh
from mm_soliton_covariance import IDENTITY, dump, spectrum, diffusion, readout, polynomial


def field_diffusion(a, g, S, groups, dt, psd, gain):
    """General complex mean/adjoints. Gram is derived before temporal projection."""
    nt, nm, nobs = g.shape
    pairs = [(m,n) for m in range(nm) for n in range(nm)]
    B = np.stack([.5j*(g[:,m,:].conj()*a[:,n,None]
                        -g[:,n,:]*a[:,m,None].conj()) for m,n in pairs], axis=1)
    gram = np.array([[S[m,n,p,q] if groups[n]-groups[m]==groups[q]-groups[p] else 0.
                      for p,q in pairs] for m,n in pairs])
    F = dt*np.fft.fft(B,axis=0)
    DR = np.real(np.einsum("kra,rs,ksb,k->ab",F.conj(),gram,F,psd,optimize=True))/(nt*dt)
    DG = dt/2*np.real(np.einsum("tma,m,tmb->ab",g.conj(),gain,g))
    return DG, DR, np.linalg.eigvalsh(gram).min()


def overlap_from_s(s):
    # Pair Gram requires only the full symmetric overlaps with even repetitions
    # after the two-mode longitudinal secular average.
    S=np.zeros((2,2,2,2))
    for i in np.ndindex(S.shape):
        if i.count(0)==4:
            S[i]=s[0,0]
        elif i.count(1)==4:
            S[i]=s[1,1]
        elif i.count(0)==2:
            S[i]=s[0,1]
    return S


def contraction(profile, propagated):
    fam=dict(np.load(profile)); data=np.load(propagated)
    t,z= data["t"],data["z"];dt=t[1]-t[0]
    fields=data["fields"][:,:,0,:]; adj=data["adjoints"]
    t0=float(fam.get("t0",.5));temperature=float(fam.get("temperature",300.))
    psd=spectrum(2*np.pi*np.fft.fftfreq(len(t),dt),t0=t0,temperature=temperature)
    S=data["S"] if "S" in data else overlap_from_s(fam["s"])
    groups=data["groups"] if "groups" in data else [0,1]
    gain=np.full(fields.shape[1],.1);source=[];mineig=0.
    for j in range(len(z)):
        DG,DR,e=field_diffusion(fields[:,:,j],adj[:,:,j,:],S,groups,dt,psd,gain)
        source.append([DG,DR]);mineig=min(mineig,e)
    cov_full=simpson(np.array(source),x=z,axis=0)
    cov=cov_full[:,:6,:6]
    ordinary={}
    if cov_full.shape[-1]>6:
        ordinary=dict(ordinary_timing_variance_over_q=cov_full[:,6,6],
            ordinary_timing_cross_covariance_over_q=cov_full[:,6,:6],
            ordinary_timing_relative_variance_difference=cov_full[:,6,6]/cov[:,2,2]-1,
            terminal_ordinary_timing_diffusion_over_q=np.asarray(source)[-1,:,6,6],
            terminal_weighted_timing_diffusion_over_q=np.asarray(source)[-1,:,2,2],
            coordinates_in_full_covariance=['E','theta','T_weighted','V','p2','phi','T_ordinary'],
            full_covariance_over_q=cov_full)
    X=readout(fam,fam["d"]);A=X@fam["A"]@np.linalg.inv(X)
    D=diffusion(fam,fam["s"],fam["d"],t0=t0,temperature=temperature)
    poly={key:polynomial(A,X@D[key]@X.T) for key in ("gain","raman")}
    expected=np.stack([np.einsum("k,kij->ij",z[-1]**np.arange(1,4),poly[key]) for key in ("gain","raman")])
    scale=np.sqrt(np.diagonal(expected,axis1=1,axis2=2)[:,:,None]*np.diagonal(expected,axis1=1,axis2=2)[:,None,:])
    normalized=np.divide(cov-expected,scale,out=np.zeros_like(cov),where=scale>1e-14)
    diag_error=np.divide(np.diagonal(cov-expected,axis1=1,axis2=2),
                         np.diagonal(expected,axis1=1,axis2=2),
                         out=np.zeros((2,6)),where=np.diagonal(expected,axis1=1,axis2=2)>1e-14)
    return dict(profile=str(profile),propagation=str(propagated),zeta=z[-1],
        time_points=len(t),time_window=len(t)*dt,dt_dimensionless=dt,**ordinary,
        covariance_over_q=cov,analytic_covariance_over_q=expected,
        relative_diagonal_errors=diag_error,max_normalized_error=np.max(np.abs(normalized)),
        predicted_zero_diagonal_absolute_over_q=np.where(np.diagonal(expected,axis1=1,axis2=2)<1e-14,
            np.diagonal(cov,axis1=1,axis2=2),0.),
        predicted_zero_scale_channels_absolute_over_q=np.where(scale<=1e-14,cov,0.),
        min_pair_gram_eigenvalue=mineig, coefficients_over_q=poly)


def stability(profile):
    fam=dict(np.load(profile));f=fam["f"];C=fam["C"];b=fam["b"]
    nt,nm=f.shape;k=fam["k"];dt=float(fam["dt"]);N=fam["N"]
    pot=f*f @ C.T
    def project(v):
        v=v.reshape(nt,nm)
        return v-f*(dt*np.sum(f*v,axis=0)/N)
    def op(v):
        y=project(v)
        pp=np.fft.ifft(-k[:,None]**2*np.fft.fft(y,axis=0),axis=0).real
        L=-b*pp/2+(fam["lam"]-pot)*y-2*f*((f*y)@C.T)
        return (project(L)+8*(v.reshape(nt,nm)-y)).ravel()
    lin=LinearOperator((nt*nm,nt*nm),matvec=op,dtype=float)
    eigen=eigsh(lin,k=5,which="SA",tol=1e-9,return_eigenvectors=False,maxiter=20000)
    return dict(profile=str(profile),constrained_Lplus_low_eigenvalues=np.sort(eigen),
                note="Fixed modal norms, translation zero mode retained; finite Fourier grid")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("profile");ap.add_argument("propagation",nargs="?")
    ap.add_argument("--out",required=True);ap.add_argument("--stability",action="store_true")
    args=ap.parse_args()
    if args.stability:
        result=stability(args.profile)
    else:
        result=contraction(args.profile,args.propagation)
    dump(args.out,{**IDENTITY,**result})
    print(json.dumps({k: v.tolist() if isinstance(v,np.ndarray) else v for k,v in result.items()
                      if k in ("relative_diagonal_errors","max_normalized_error","constrained_Lplus_low_eigenvalues")},indent=2))


if __name__=="__main__":main()
