#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt.
Full-grid nonnegative dual multipliers via a smooth minimum eigenvalue.
The optimizer is heuristic; its returned lower bound is reconstructed and
checked on the full covariance independently of optimizer termination.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import argparse
import json
import time
import itertools
from pathlib import Path
import numpy as np
from scipy import linalg as la, optimize, special


def smooth_dual(a, n, betas=(20., 100., 500.), maxiter=150, start=None, triangle_core=0):
    begun = time.time()
    m = len(n)
    ii, jj = np.triu_indices(m, 1)
    b = np.sqrt(n/max(n))
    scale = np.maximum(np.maximum(b[ii], b[jj]), 1e-300)
    ci, cj = b[ii]/scale, b[jj]/scale
    count = len(ii)
    triangles=[]
    core=np.argsort(n)[-min(triangle_core,m):] if triangle_core else []
    for i,j,k in itertools.combinations(core,3):
        triangles.extend(((i,j,k),(j,i,k),(k,i,j)))
    tc=np.asarray(triangles,dtype=int).reshape(-1,3)
    ti,tj,tk=tc.T
    td=b[tj]*b[tk];tij=-b[ti]*b[tk];tik=-b[ti]*b[tj];tjk=b[ti]**2
    ts=np.maximum.reduce([td,-tij,-tik,tjk]) if len(tc) else np.array([])
    td,tij,tik,tjk=(v/np.maximum(ts,1e-300) for v in (td,tij,tik,tjk))
    x = np.zeros(3*count+len(tc))
    if start is not None: x[:len(start)]=np.maximum(start,0)
    history = []

    def make_k(x):
        pos, rij, rji = x[:3*count].reshape(3, count)
        k = np.zeros_like(a)
        off = (pos-rij*ci-rji*cj)/2
        k[ii, jj] = off
        k[jj, ii] = off
        diag = np.bincount(ii, weights=rij*cj, minlength=m)+np.bincount(jj, weights=rji*ci, minlength=m)
        k.flat[::m+1] = diag
        if len(tc):
            multipliers=x[3*count:]
            np.add.at(k,(ti,ti),multipliers*td)
            for left,right,coef in ((ti,tj,tij),(ti,tk,tik),(tj,tk,tjk)):
                np.add.at(k,(left,right),multipliers*coef/2)
                np.add.at(k,(right,left),multipliers*coef/2)
        return k

    best_x=x.copy()
    best_raw=float(la.eigh(a-make_k(x),subset_by_index=(0,0),eigvals_only=True,check_finite=False)[0])
    for beta in betas:
        def objective(x):
            ev, q = la.eigh(a-make_k(x), check_finite=False, driver="evr")
            w = np.exp(-beta*(ev-ev[0]))
            w /= w.sum()
            # Omitting exponentially tiny weights changes only optimization,
            # never the independently reconstructed certificate.
            keep = w > 1e-13
            r = (q[:, keep]*w[keep])@q[:, keep].T
            rd = np.diag(r)
            ro = r[ii, jj]
            grad = np.r_[ro, cj*rd[ii]-ci*ro, ci*rd[jj]-cj*ro]
            if len(tc): grad=np.r_[grad,td*rd[ti]+tij*r[ti,tj]+tik*r[ti,tk]+tjk*r[tj,tk]]
            val = -float(ev[0])+float(special.logsumexp(-beta*(ev-ev[0])))/beta
            return val, grad
        result = optimize.minimize(objective, x, jac=True, method="L-BFGS-B",
            bounds=optimize.Bounds(np.zeros_like(x), np.full_like(x, np.inf)),
            options={"maxiter": maxiter, "maxcor": 6, "ftol": 1e-10, "gtol": 2e-7, "maxls": 30})
        x = np.maximum(result.x, 0)
        k = make_k(x)
        raw = float(la.eigh(a-k, subset_by_index=(0, 0), eigvals_only=True, check_finite=False)[0])
        if raw>best_raw: best_raw,best_x=raw,x.copy()
        history.append({"beta": beta, "iterations": int(result.nit), "evaluations": int(result.nfev),
            "optimizer_success": bool(result.success), "message": str(result.message),
            "raw_dual_bound": raw, "seconds": time.time()-begun})
        print(json.dumps(history[-1]), flush=True)
    x=best_x
    k = make_k(x)
    margin = 1e-8*max(1, la.norm(a-k, np.inf))
    lower = float(la.eigh(a-k, subset_by_index=(0, 0), eigvals_only=True, check_finite=False)[0])-margin
    la.cholesky(a-k-lower*np.eye(m), lower=True, check_finite=False)
    return lower, k, x, {"history": history, "certificate_margin": margin,
                          "elapsed_seconds": time.time()-begun, "multipliers": len(x),
                          "triangle_core_bins":len(core),"triangle_cuts":len(tc)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--maxiter", type=int, default=150)
    ap.add_argument("--betas", default="20,100,500")
    ap.add_argument("--triangles",type=int,default=0)
    ap.add_argument("--warm-start",action="store_true")
    args = ap.parse_args()
    data = np.load(args.path)
    n = data["nbar"]; a = data["V"][:len(n), :len(n)]
    start=np.load(Path(args.path).with_suffix('.smooth.npz'))['multipliers'] if args.warm_start else None
    lower, k, multipliers, info = smooth_dual(a, n, tuple(map(float,args.betas.split(','))), args.maxiter,start,args.triangles)
    info.update(agent="gpt-a", model="gpt-6-astra", family="gpt", bound=lower)
    suffix='.triangles' if args.triangles else '.smooth'
    Path(args.path).with_suffix(suffix+'.json').write_text(json.dumps(info, indent=2)+'\n')
    np.savez_compressed(Path(args.path).with_suffix(suffix+'.npz'), dual_K=k, multipliers=multipliers)
    print(json.dumps(info), flush=True)
