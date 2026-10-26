"""gpt-e / gpt-6-astra / gpt. Independent semiclassical audit.

Uses only the auditor's sibling run's new solver, never a cited prior run.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import sys,json,time,argparse
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator,eigsh

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'2026-10-19-gpt-e-weak-dispersion'))
from tangent import Flow,pack,unpack
RAW=Path('~/analytical-nl-discovery-data')/HERE.name
RAW.mkdir(parents=True,exist_ok=True)

def J(x):
    n=len(x)//2
    return np.concatenate([-x[n:],x[:n]])

def passive(flow):
    h=pack(1j*flow.mean);h/=np.linalg.norm(h)
    def inverse(x):return -J(flow.covariance(J(x)))
    vh=inverse(h);denom=h@vh
    def mv(x):return inverse(x)-vh*(vh@x)/denom
    val,vec=eigsh(LinearOperator((len(h),len(h)),matvec=mv,dtype=float),k=1,which='LA',
                  tol=2e-10,v0=np.random.default_rng(191007).normal(size=len(h)))
    return float(1/val[0]),float(abs(h@vec[:,0]))

def case(N,Z,n=1024,window=24.,steps=None,chirp=0.,order=4,compute_passive=True,compute_C=True):
    start=time.time();phi=N*Z;d=Z/N
    if steps is None:
        steps=max(64,int(np.ceil(phi/.15)),int(np.ceil(1.703*d*(np.pi*n/window)**2/2)))
    f=Flow(phi,d,n,window,steps,chirp=chirp,order=order)
    vals,modes,direct=f.spectrum(3)
    ref=np.r_[0,np.arange(n-1,0,-1)]
    parity=[float(np.vdot(unpack(modes[:,j]),unpack(modes[:,j])[ref]).real) for j in range(3)]
    C=f.scaled_phase_spectrum(N) if compute_C else [None,None]
    lp,overlap=passive(f) if compute_passive else (np.nan,np.nan)
    row=dict(N=N,Z=Z,phi=phi,n=n,window=window,steps=steps,chirp=chirp,order=order,
        lambda_min=vals[0],lambda_2=vals[1],lambda_3=vals[2],N2_lambda_min=N*N*vals[0],N2_lambda_2=N*N*vals[1],
        C_inverse_norm_squared=C[0],C_second_inverse_squared=C[1],lambda_pass=lp,pass_vs_second=lp/vals[1]-1,
        passive_constraint_residual=overlap,parity=parity,reciprocal_check=float(max(abs(vals-direct)/vals)),
        seconds=time.time()-start,**f.diagnostics())
    print(json.dumps(row),flush=True)
    np.savez_compressed(RAW/f'N{N}_Z{Z}_n{n}_w{window}_s{steps}_c{chirp}_o{order}.npz',t=f.t,mean=f.mean,modes=modes)
    return row

def theorem_counterexample():
    # All blocks have regular limits; C(eps)=1+eps, so the claimed O(eps^2)
    # relative remainder does not follow merely from existence of those limits.
    rows=[]
    for N in [10.,20.,40.,80.,160.]:
        eps=1/N;M=np.array([[1.,0.],[(1+eps)/eps,1.]])
        lam=np.linalg.svd(M,compute_uv=False)[-1]**2
        rows.append(dict(N=N,epsilon=eps,determinant=float(np.linalg.det(M)),lambda_min=lam,
            scaled_lambda=lam/eps**2,relative_deficit=1-lam/eps**2))
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--suite',default='pilot');a=p.parse_args()
    if a.suite=='pilot':cases=[dict(N=10.,Z=.75,n=512)]
    elif a.suite=='main':
        cases=[dict(N=N,Z=Z) for Z in [.45,.9,1.8,2.3] for N in [10.,20.,40.]]
    elif a.suite=='edges':
        cases=[dict(N=N,Z=Z) for N,Z in [(50.,.1),(5.,1.),(10.,3.2),(10.,3.6),(5.,.45)]]
    elif a.suite=='checks':
        cases=[dict(N=20.,Z=2.3,n=2048),dict(N=20.,Z=2.3,n=2048,window=48.),
               dict(N=20.,Z=2.3,steps=4000),dict(N=20.,Z=2.3,steps=4000,order=2),
               dict(N=20.,Z=.9,chirp=.5),dict(N=20.,Z=.9,chirp=-.5),
               dict(N=40.,Z=1.8,n=2048),dict(N=40.,Z=2.3,n=2048)]
    elif a.suite=='theorem':
        (HERE/'theorem.json').write_text(json.dumps(theorem_counterexample(),indent=2)+'\n');return
    else:raise ValueError(a.suite)
    rows=[]
    for kw in cases:
        rows.append(case(**kw));(HERE/f'{a.suite}.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
