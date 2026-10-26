#!/usr/bin/env python3
"""Fast independent crosscheck of Phi=3,y=1e-4 with the strong-lane solver."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator,eigsh
from verify_strong import TangentFlow

f=TangentFlow(300,.01,2048,12.,100)
p0=np.exp(-f.t**2/(2*.07**2))*f.out_phase
v0=np.r_[p0.real,p0.imag]
op=LinearOperator((4096,4096),matvec=f.covariance,dtype=float)
start=time.time()
val,vec=eigsh(op,k=1,which='LA',tol=1e-11,v0=v0,ncv=30)
low=np.r_[vec[2048:,0],-vec[:2048,0]]
result=dict(Phi=3.,y=.0001,N=300,Z=.01,n=2048,window=12.,steps=100,
            lambda_min=float(1/val[0]),direct_rayleigh=float(low@f.covariance(low)),
            elapsed=time.time()-start,diagnostics=f.diagnostics())
Path(__file__).with_name('weak_cross_N300_Z001_n2048_w12_s100.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
