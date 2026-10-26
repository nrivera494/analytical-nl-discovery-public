#!/usr/bin/env python3
"""Explicit squared-Jost continuum formula for soliton bandpass noise.

agent: gpt-b; model: gpt-6-astra; family: gpt.
No longitudinal noise propagation. All quadratures use shot noise = 1.
The formula is exact on the line; the implementation uses finite quadrature.
"""
import argparse
import json
import os
from pathlib import Path
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
import numpy as np
from scipy.special import spence, roots_legendre
from scipy.optimize import minimize_scalar

C = np.pi / 2


def sech(x):
    return 2 * np.exp(-np.abs(x)) / (1 + np.exp(-2 * np.abs(x)))


def log_sinh_abs(x):
    y = np.abs(x)
    return y - np.log(2) + np.log(-np.expm1(-2 * y))


def int_t_coth(t):
    """Odd primitive of t*coth(pi*t/2), with value zero at the origin."""
    a = np.abs(t)
    out = a * a / 2 + a / C * np.log(-np.expm1(-2 * C * a))
    out -= (spence(1 - np.exp(-2 * C * a)) - np.pi**2 / 6) / (2 * C**2)
    return np.sign(t) * np.where(a == 0, 0.0, out)


def even_coefficient(k, edge):
    if edge <= 0:
        return np.zeros_like(k)
    a = edge
    j1 = a*a + 2*a/C*np.log1p(np.exp(-2*C*a))
    j1 -= (spence(1+np.exp(-2*C*a)) + np.pi**2/12)/C**2
    j2 = k/C * (log_sinh_abs(C*(k+a))-log_sinh_abs(C*(k-a)))
    j2 -= int_t_coth(k+a)-int_t_coth(k-a)
    return np.pi*sech(C*k)/(1+k*k) * ((k*k-1)*(abs(k)<a)-j1-j2)


def odd_coefficient(k, edge):
    if edge <= 0:
        return np.zeros_like(k)
    a = edge
    l1 = 2/C*(C*a-np.log(2)+np.log1p(np.exp(-2*C*a)))
    l2 = (2*log_sinh_abs(C*k)-log_sinh_abs(C*(k-a))-log_sinh_abs(C*(k+a)))/C
    val = np.pi*sech(C*k)/(1+k*k)*((k*k-1)*np.sign(k)*(abs(k)<a)-k*(l1+l2))
    return np.where(k == 0, 0.0, val)


def quadrature(edges, order=160, cutoff=12.0):
    breaks = sorted(set([-cutoff, 0.0, cutoff] + [v for a in edges if a>0 for v in (-a,a) if abs(v)<cutoff]))
    t,w = roots_legendre(order)
    kk,ww = [],[]
    for left,right in zip(breaks[:-1], breaks[1:]):
        kk.append((right+left)/2+(right-left)*t/2)
        ww.append((right-left)*w/2)
    return np.concatenate(kk),np.concatenate(ww)/(2*np.pi)


def continuum_grams(k):
    diff = k[:,None]-k[None,:]
    safe = np.where(abs(diff)<1e-10,1.,diff)
    h = np.where(abs(diff)<1e-10,2.,np.pi*safe/np.sinh(C*safe))
    den = (1+k[:,None]**2)*(1+k[None,:]**2)
    rd = 2*(1-k[:,None]*k[None,:])*h/den
    rs = (2/3)*(1+k[:,None]**2+k[None,:]**2+k[:,None]*k[None,:])*h/den
    return rd,rs


def white_source_gram(k):
    """Integral q(x)^2*S_k(x)*conj(S_l(x)) dx, in closed form."""
    diff=k[:,None]-k[None,:]
    midpoint=(k[:,None]+k[None,:])/2
    safe=np.where(abs(diff)<1e-10,1.,diff)
    h=np.where(abs(diff)<1e-10,2.,np.pi*safe/np.sinh(C*safe))
    moment4=midpoint**4+midpoint**2*(diff**2+4)/2+(3*diff**4+40*diff**2+112)/240
    return h*moment4/((1+k[:,None]**2)*(1+k[None,:]**2))


def colored_source_grams(k,T0_ps=None,temperature_K=300.,order=320,
                         spectrum_function=None,breakpoints=()):
    """Exact frozen-source Gram reduced to one material-frequency integral.

    Returns continuum, neutral-continuum, and neutral-frequency Grams.
    This is theory quadrature; physical runs use the fetched Julia helper.
    """
    from soliton_frozen_raman import material_spectrum
    nu,w=quadrature(breakpoints,order=order,cutoff=float(max(abs(k))+12.))
    spectrum=(material_spectrum(nu,T0_ps,temperature_K) if spectrum_function is None
              else spectrum_function(nu))
    phi=nu[None,:]**2*np.pi*sech(C*(nu[None,:]-k[:,None]))/(1+k[:,None]**2)
    safe=np.where(abs(nu)<1e-12,1.,nu)
    h=np.where(abs(nu)<1e-12,2.,np.pi*safe/np.sinh(C*safe))
    weighted=w*spectrum
    with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
        gram=(phi*weighted[None,:])@phi.T
        cross=phi@(weighted*nu*h/2)
    neutral=float(np.sum(weighted*nu**2*h*h/4))
    return gram,cross,neutral


def integrated_trig(k,z):
    energy=(1+k*k)/2
    minus=np.sinc((energy[:,None]-energy[None,:])*z/np.pi)
    plus=np.sinc((energy[:,None]+energy[None,:])*z/np.pi)
    return z/2*(minus-plus),z/2*(minus+plus)


def bandpass(z, edge, order=160, cutoff=12., include_checks=False,rho=0.,T0_ps=None,temperature_K=300.):
    k,w = quadrature([edge],order,cutoff)
    cc = even_coefficient(k,edge)
    ca = np.tanh(C*edge)-C*edge*sech(C*edge)**2
    energy = 2*np.tanh(C*edge)
    rd,rs=continuum_grams(k)
    phase=(1+k*k)*z/2
    vc=w*cc*np.cos(phase); vs=w*cc*np.sin(phase)
    neutral=2*ca*ca
    cross=-2*ca*np.sum(vc*np.pi*sech(C*k))
    diagonal=np.sum(w*cc*cc)
    v0=w*cc
    with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
        continuum=vc@rd@vc+vs@rs@vs
        continuum0=v0@rd@v0
    cross0=-2*ca*np.sum(v0*np.pi*sech(C*k))
    raw0=(neutral+cross0+diagonal+continuum0)/energy
    # Completeness gives F(0)=1 exactly. Evaluate its difference, cancelling
    # the distance-independent integral of the logarithmic edge singularity.
    value=1+(cross-cross0+continuum-continuum0)/energy
    bath_per_rho=0.
    if rho != 0 or include_checks or T0_ps is not None:
        lss=white_source_gram(k)
        iss,_=integrated_trig(k,z)
        with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
            bath_per_rho=4*(v0@(lss*iss)@v0)/energy
        value+=rho*bath_per_rho
    colored_bath=0.
    if T0_ps is not None:
        if rho!=0:raise ValueError('Choose either white or colored source, not both.')
        lcolored,_,_=colored_source_grams(k,T0_ps,temperature_K)
        with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
            colored_bath=float(4*(v0@(lcolored*iss)@v0)/energy)
        value+=colored_bath
    if not np.isfinite(value):
        raise FloatingPointError('nonfinite continuum quadrature')
    if include_checks:
        return {"F":float(value),"F_Kerr":float(value-rho*bath_per_rho-colored_bath),"Raman_per_rho":float(bath_per_rho),"F_Raman_colored":colored_bath,"T0_ps":T0_ps,"temperature_K":temperature_K,"rho":rho,"uncorrected_F":float((neutral+cross+diagonal+continuum)/energy),"raw_completeness_error":float(raw0-1),"neutral":float(neutral/energy),"neutral_continuum_cross":float(cross/energy),"continuum_diagonal":float(diagonal/energy),"continuum_regular":float(continuum/energy),"edge":edge,"z_over_LD":z,"order_per_segment":order,"continuum_cutoff":cutoff}
    return float(value)


def band_covariances(z,edges,order=40,cutoff=12.,rho=0.,
                     spectrum_function=None,source_breakpoints=(),source_order=320):
    k,w=quadrature(edges,order,cutoff)
    ce=np.column_stack([even_coefficient(k,a) for a in edges])
    co=np.column_stack([odd_coefficient(k,a) for a in edges])
    ce=np.diff(ce,axis=1);co=np.diff(co,axis=1)
    ca=np.diff(np.tanh(C*np.array(edges))-C*np.array(edges)*sech(C*np.array(edges))**2)
    cv=np.diff(np.pi/2*np.tanh(C*np.array(edges))**2)
    energy=2*np.diff(np.tanh(C*np.array(edges)))
    rd,rs=continuum_grams(k)
    phase=(1+k*k)*z/2
    ec=w[:,None]*ce*np.cos(phase[:,None]);es=w[:,None]*ce*np.sin(phase[:,None])
    oc=w[:,None]*co*np.cos(phase[:,None]);oss=w[:,None]*co*np.sin(phase[:,None])
    qhat=np.pi*sech(C*k)
    e_cross=np.einsum('ij,i->j',ec,qhat)
    o_cross=np.einsum('ij,i->j',oc,k*qhat)
    e0=w[:,None]*ce;o0=w[:,None]*co
    e_cross-=np.einsum('ij,i->j',e0,qhat);o_cross-=np.einsum('ij,i->j',o0,k*qhat)
    with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
        ve=np.diag(energy)-np.outer(ca,e_cross)-np.outer(e_cross,ca)
        ve+=ec.T@rd@ec+es.T@rs@es-e0.T@rd@e0
        vo=np.diag(energy)+(np.outer(cv,o_cross)+np.outer(o_cross,cv))/3
        vo+=oc.T@rs@oc+oss.T@rd@oss-o0.T@rs@o0
    if rho != 0 or spectrum_function is not None:
        if rho != 0 and spectrum_function is not None:
            raise ValueError('Choose a white source or a supplied spectrum, not both.')
        iss,icc=integrated_trig(k,z)
        ek=(1+k*k)/2
        if spectrum_function is None:
            lss=rho*white_source_gram(k)
            j=rho*k*(3*k*k+7)/30*qhat
            neutral_source=rho*4/15
        else:
            lss,j,neutral_source=colored_source_grams(k,order=source_order,
                spectrum_function=spectrum_function,breakpoints=source_breakpoints)
        cross_r=np.einsum('ij,i->j',o0,j*np.sin(ek*z)/ek)
        with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
            re=4*(e0.T@(lss*iss)@e0)
            ro=4*(z*neutral_source*np.outer(cv,cv)+np.outer(cv,cross_r)+np.outer(cross_r,cv)+o0.T@(lss*icc)@o0)
        ve+=re;vo+=ro
    norm=np.sqrt(energy[:,None]*energy[None,:])
    return ve/norm,vo/norm,energy


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--z',type=float,default=3*np.pi/2)
    ap.add_argument('--edge',type=float,default=.75);ap.add_argument('--order',type=int,default=160)
    ap.add_argument('--rho',type=float,default=0.)
    ap.add_argument('--optimize',action='store_true');ap.add_argument('--output')
    args=ap.parse_args()
    if args.optimize:
        opt=minimize_scalar(lambda edge:bandpass(args.z,edge,args.order,rho=args.rho),bounds=(.2,1.8),method='bounded',options={'xatol':1e-7})
        args.edge=float(opt.x)
    result=bandpass(args.z,args.edge,args.order,include_checks=True,rho=args.rho)
    result.update(agent='gpt-b',model='gpt-6-astra',family='gpt',F_dB=float(10*np.log10(result['F'])),F_at_zero=bandpass(0,args.edge,args.order))
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
