#!/usr/bin/env python3
"""Stationary-phase test through period-averaged instantaneous Raman growth.
agent: gpt-b; model: gpt-6-astra; family: gpt.
Fixed centered mask, unit white source, frozen soliton; no physical long-z claim.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre
from soliton_jost_filter import even_coefficient,quadrature


def asymptotic_growth(z,edge,x,weights,ts,ws):
    q=1/np.cosh(x);t=np.tanh(x);c=np.pi/2
    n=2*np.tanh(c*edge);b0=float(even_coefficient(np.array([0.]),edge)[0])
    qedge=np.pi/np.cosh(c*edge)
    logarithm=qedge*edge/(c*(1+edge*edge))
    jump=qedge*(edge*edge-1)/(1+edge*edge)
    s0=2*q*q-1
    se=((edge*edge-1+2*q*q)*np.cos(edge*x)-2*edge*t*np.sin(edge*x))/(1+edge*edge)
    s=z+np.pi*(ts+1)
    h0=b0*s0[None,:]*np.sin(s[:,None]/2+np.pi/4)/np.sqrt(2*np.pi*s[:,None])
    he=-se[None,:]/(edge*s[:,None])*(logarithm*np.sin((1+edge*edge)/2*s[:,None])
                                   +jump/np.pi*np.cos((1+edge*edge)/2*s[:,None]))
    growth=4*np.sum(weights[None,:]*q[None,:]**2*(h0+he)**2,axis=1)/n
    return float(np.sum(ws*s*growth)/2)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--z',nargs='+',type=float,default=[32.,64.,128.,256.,512.,1024.])
    ap.add_argument('--orders',nargs='+',type=int)
    args=ap.parse_args();started=time.monotonic();edge=.7368
    tx,wx=roots_legendre(240);x=12*tx;wx=12*wx
    q=1/np.cosh(x);t=np.tanh(x);den=2*np.tanh(np.pi*edge/2)
    ts,ws=roots_legendre(32)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',edge=edge,
        predicted_log_coefficient=.1266035972462525,
        observable='Average of s*dB/ds over one 2pi period; B is the white-source variance per rho.',
        scope='Fixed-filter frozen model; this is a source-growth diagnostic, not a binary-optimization score.',points=[])
    for z in args.z:
      for order in (args.orders or ([2048,4096] if z<=256 else [4096,8192])):
        k,w=quadrature([edge],order=order,cutoff=6.)
        b=even_coefficient(k,edge);ek=(1+k*k)/2
        smat=(((k[:,None]**2-1+2*q[None,:]**2)*np.cos(k[:,None]*x[None,:])
                -2*k[:,None]*t[None,:]*np.sin(k[:,None]*x[None,:]))/(1+k[:,None]**2))
        s=z+np.pi*(ts+1)
        with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
            phase_readout=(np.sin(s[:,None]*ek[None,:])*(w*b)[None,:])@smat
        growth=4*np.sum(wx[None,:]*q[None,:]**2*phase_readout**2,axis=1)/den
        value=float(np.sum(ws*s*growth)/2)
        prediction=asymptotic_growth(z,edge,x,wx,ts,ws)
        row=dict(z_over_LD=z,order_per_segment=order,continuum_cutoff=6.,
            period_averaged_growth_coefficient=value,
            relative_error=value/out['predicted_log_coefficient']-1,
            stationary_plus_edge_prediction=prediction,
            residual_after_edge_correction=value-prediction)
        out['points'].append(row);out['wall_time_s']=time.monotonic()-started
        Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps(row),flush=True)


if __name__=='__main__':main()
