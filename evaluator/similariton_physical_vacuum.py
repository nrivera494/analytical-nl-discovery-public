#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Physical-vacuum Lagrangian collocation, conditional smooth-flow checks."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import argparse,json,platform,subprocess,time
import numpy as np
from numpy.polynomial.legendre import leggauss,Legendre
from scipy.integrate import solve_ivp
import yaml
from similariton_summarize import fit_mode
ap=argparse.ArgumentParser();ap.add_argument('--direct',action='store_true');args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1];RUN='2026-10-08-gpt-a-similariton-physical-vacuum'+('-direct' if args.direct else '')
def mm(A,B):
 return np.einsum('ij,j...->i...',A,B,optimize=False) if args.direct else A@B
OUT=ROOT/'runs'/RUN;RAW=Path.home()/'analytical-nl-discovery-data'/RUN
OUT.mkdir(exist_ok=True);RAW.mkdir(exist_ok=True)
config=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',task='T-20261008-gpt-a-01',
    method='Chebyshev Lagrangian physical-vacuum collocation; DOP853',
    degrees=[32,64],rtol=2e-11,atol=2e-13,gain_length=24,quadrature_nodes=256,
    cases=['linear_l3','linear_l4','finite_mixed','heldout_asymmetric'],
    contraction='direct einsum without BLAS' if args.direct else 'numpy matmul; backend emitted floating-point flags despite finite results')
(OUT/'config.yaml').write_text(yaml.safe_dump(config,sort_keys=False))
started=time.monotonic();cases=[]
for degree in config['degrees']:
 a=np.cos(np.pi*np.arange(degree+1)/degree)
 bary=(-1.)**np.arange(degree+1);bary[[0,-1]]*=.5
 dif=a[:,None]-a[None,:];np.fill_diagonal(dif,1)
 D=bary[None,:]/bary[:,None]/dif;np.fill_diagonal(D,0);np.fill_diagonal(D,-D.sum(axis=1))
 D2=mm(D,D);r=(1-a*a)/18;rp=-a/9
 aq,wq=leggauss(config['quadrature_nodes']);rq=(1-aq*aq)/18
 B=bary[None,:]/(aq[:,None]-a[None,:]);B/=B.sum(axis=1)[:,None]
 assert np.max(np.abs(mm(D,a)-1))<1e-10
 modes={l:Legendre.basis(l).deriv()(a)/(l*(l+1)/2) for l in range(2,6)}
 modq={l:Legendre.basis(l).deriv()(aq)/(l*(l+1)/2) for l in range(2,6)}
 def rhs(t,y):
  Y,V=y[:degree+1],y[degree+1:];Ya=mm(D,Y);J=1+Ya
  if np.min(J)<=0:raise RuntimeError('Mass map lost monotonicity')
  grad=Y/9-rp*Ya*(2+Ya)/(J*J)-r*mm(D2,Y)/(J**3)
  return np.r_[V,-2*V/3-grad]
 for name in config['cases']:
  Y=np.zeros_like(a);V=np.zeros_like(a)
  if name=='linear_l3':Y=1e-4*modes[3]
  if name=='linear_l4':Y=1e-4*modes[4]
  if name=='finite_mixed':Y=.03*modes[2]+.015*modes[4];V=.02*modes[3]
  if name=='heldout_asymmetric':Y=.06*modes[3]-.025*modes[5];V=.04*modes[4]
  ts=np.linspace(0,24,481)
  sol=solve_ivp(rhs,[0,24],np.r_[Y,V],t_eval=ts,method='DOP853',rtol=config['rtol'],atol=config['atol'])
  if not sol.success:raise RuntimeError(sol.message)
  Y=sol.y[:degree+1];V=sol.y[degree+1:];Ya=mm(D,Y);Yaa=mm(D2,Y);J=1+Ya
  Yq=mm(B,Y);Vq=mm(B,V);Yaq=mm(B,Ya);Jq=1+Yaq
  Fgap=np.sum(wq[:,None]*(rq[:,None]**2*Yaq**2/(2*Jq)+rq[:,None]*Yq**2/18),axis=0)
  H=Fgap+.5*np.sum((wq*rq)[:,None]*(Vq+Yq/3)**2,axis=0)
  grad=Y/9-rp[:,None]*Ya*(2+Ya)/(J*J)-r[:,None]*Yaa/(J**3)
  Gq=mm(B,grad)
  Hd=np.sum((wq*rq)[:,None]*(Gq*Vq+(Vq+Yq/3)*(-Vq/3-Gq)),axis=0)
  ff={}
  if name.startswith('linear'):
   l=int(name[-1]);mu=modq[l];den=np.sum(wq*rq*mu*mu)
   yy=np.sum((wq*rq*mu)[:,None]*Yq,axis=0)/den
   vv=np.sum((wq*rq*mu)[:,None]*Vq,axis=0)/den
   for lo,hi in [(2,10),(8,16),(12,20)]:
    ix=(ts>=lo)&(ts<=hi);ff[f'{lo}-{hi}']=fit_mode(ts[ix],yy[ix],vv[ix],frequency_guess=np.sqrt(l*(l+1)/18-1/9))
  lab=f'{name}_degree{degree}'
  np.savez(RAW/f'{lab}.npz',tau=ts,a=a,displacement=Y,velocity=V,H=H,Hdot=Hd)
  row=dict(label=lab,degree=degree,minimum_jacobian=float(np.min(J)),H_initial=float(H[0]),H_final=float(H[-1]),
   largest_bound_ratio=float(np.max(H*np.exp(ts/3)/H[0])),largest_inequality_residual=float(np.max(Hd+H/3)),
   maximum_force_evaluations=int(sol.nfev),fits=ff)
  cases.append(row);print(json.dumps(row),flush=True)
summary=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',cases=cases,
 caveat='Numerical smooth physical-vacuum flows; not a global-existence theorem or independent verification.')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
commit=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
meta=dict(run_id=RUN,agent='gpt-a',model='gpt-6-astra',family='gpt',task='T-20261008-gpt-a-01',
 exploration='explorations/2026-10-08-gpt-a-similariton-attraction.md',
 solver_commit=commit,solver_dirty=False,solver_used=False,hardware=platform.platform(),hostname=platform.node(),
 raw_location=str(RAW),wall_seconds=time.monotonic()-started,evaluator='evaluator/similariton_physical_vacuum.py')
(OUT/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
