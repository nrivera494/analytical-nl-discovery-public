#!/usr/bin/env python3
"""First Born correction for a Gaussian launch near its dominant Kerr soliton.

agent: gpt-b; model: gpt-6-astra; family: gpt.
Uses the soliton propagator and its explicit mean-dependent generator
derivative. This does not reset the inherited covariance. The O(epsilon^2)
statement is at fixed length and finite basis, not a one-sided bound.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from soliton_fano_theory import grid_operators,score_covariance
from soliton_batch_adjoint import ScalarRK


def born_map(generator,q,delta,z,interval=.08):
    """Composite four-point Gauss integration of the Duhamel derivative."""
    n=len(q);count=int(np.ceil(z/interval));h=z/count
    nodes,weights=np.polynomial.legendre.leggauss(4)
    nodes=(nodes+1)/2;weights=weights/2
    offsets=np.r_[nodes[0],np.diff(nodes),1-nodes[-1]]*h
    forward=[expm(generator*d) for d in offsets]
    backward=[expm(-generator*d) for d in offsets]
    pos=np.eye(2*n);neg=np.eye(2*n);integral=np.zeros_like(pos)
    for step in range(count):
      for j in range(4):
        pos=forward[j]@pos;neg=backward[j]@neg
        mean=pos@delta;r=mean[:n];im=mean[n:]
        # A1=[[-2q Im(m),-2q Re(m)],[6q Re(m),2q Im(m)]].
        am=np.vstack([-2*q[:,None]*(im[:,None]*pos[:n]+r[:,None]*pos[n:]),
                       2*q[:,None]*(3*r[:,None]*pos[:n]+im[:,None]*pos[n:])])
        integral+=h*weights[j]*(neg@am)
      pos=forward[4]@pos;neg=backward[4]@neg
    base=expm(generator*z)
    return base,base@integral,base@delta


def direct_covariance(x,launch,z,steps):
    """Ideal Kerr RK4IP and its exact discrete pullback in this same basis."""
    n=len(x);dx=x[1]-x[0]
    rk=ScalarRK.__new__(ScalarRK);rk.n=n;rk.x=x;rk.k=2*np.pi*np.fft.fftfreq(n,dx)
    rk.R=np.ones(n);rk.shock=np.ones(n);rk.S=np.zeros(n);rk.p=np.ones(n)
    rk.h=z/steps;rk.D=np.exp(-.25j*rk.k*rk.k*rk.h)
    history=np.empty((steps+1,n),complex);history[0]=launch
    for j in range(steps):history[j+1]=rk.stages(history[j])[0]
    lam=np.concatenate([np.eye(n),1j*np.eye(n)],axis=1)
    for j in range(steps-1,-1,-1):lam=rk.pullback(rk.stages(history[j])[1],lam)
    return (lam.conj().T@lam).real,history[-1]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--N',type=float,required=True)
    ap.add_argument('--amplitude',type=float,required=True);ap.add_argument('--z',type=float,required=True)
    ap.add_argument('--n',type=int,default=128);ap.add_argument('--window',type=float,default=40.)
    ap.add_argument('--interval',type=float,default=.08);ap.add_argument('--steps',type=int,default=2400)
    ap.add_argument('--epsilons',nargs='+',type=float,default=[0.,.05,.1,.2,1.])
    ap.add_argument('--prediction-only',action='store_true');ap.add_argument('--output',required=True)
    args=ap.parse_args();start=time.monotonic()
    x,k,q,a,ft=grid_operators(args.n,args.window);amplitude=args.amplitude
    delta_real=args.N/amplitude*np.exp(-.5*(x/amplitude)**2)-q
    delta=np.r_[delta_real,np.zeros(args.n)];z=amplitude**2*args.z
    base,first,mean_first=born_map(a,q,delta,z,args.interval)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',N=args.N,
        soliton_amplitude=amplitude,z_over_launch_LD=args.z,z_over_soliton_LD=z,
        n=args.n,window_in_soliton_widths=args.window,gauss_interval=args.interval,
        direct_steps=args.steps,relative_launch_mismatch=float(np.linalg.norm(delta_real)/np.linalg.norm(q)),
        points=[],scope='First-order launch perturbation in the finite ideal Kerr basis; no bound property asserted.')
    np.savez_compressed(Path(args.output).with_suffix('.npz'),x=x,q=q,delta=delta,base=base,first=first,mean_first=mean_first)
    for eps in args.epsilons:
        mean=q+eps*(mean_first[:args.n]+1j*mean_first[args.n:])
        prop=base+eps*first
        predicted,mask,_=score_covariance(prop@prop.T,mean,ft)
        row=dict(epsilon=eps,prediction=predicted)
        if not args.prediction_only:
            cov,actual_mean=direct_covariance(x,q+eps*delta_real,z,args.steps)
            actual,actual_mask,actual_vamp=score_covariance(cov,actual_mean,ft)
            np.savez_compressed(Path(args.output).with_name(Path(args.output).stem+f'_eps{eps:g}.npz'),
                V=cov,Vamp=actual_vamp,mean=actual_mean,fs=ft@actual_mean,mask=actual_mask)
            row['actual']=actual
            row['mean_relative_error']=float(np.linalg.norm(actual_mean*np.exp(-.5j*z)-mean)/np.linalg.norm(actual_mean))
            row['lambda_gen_error']=predicted['lambda_gen']-actual['lambda_gen']
        out['points'].append(row);out['wall_time_s']=time.monotonic()-start
        Path(args.output).write_text(json.dumps(out,indent=2))
        print(json.dumps({**row,'prediction':{k:v for k,v in predicted.items() if not k.endswith('indices')}}),flush=True)


if __name__=='__main__':main()
