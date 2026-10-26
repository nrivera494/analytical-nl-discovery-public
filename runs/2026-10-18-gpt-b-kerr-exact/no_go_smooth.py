#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Full-support unimodal nonclassical counterexample."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
RUN=Path(__file__).resolve().parent
memory_gate();rows=[]
for cut in [1000,2000]:
    k=np.arange(cut+1,dtype=float);t=10.;epsilon=.01
    p=np.exp(k*np.log(t/(1+t)))/(1+t)*(epsilon+(1-epsilon)*k/t)
    norm=float(p.sum());mean=float(k@p);variance=float((k*k)@p-mean**2);peak=int(np.argmax(p))
    residual=(k[1:-1]+1)*p[:-2]*p[2:]-k[1:-1]*p[1:-1]**2
    rows.append(dict(cutoff=cut,t=t,thermal_weight=epsilon,norm=norm,mean=mean,number_variance=variance,
      quadrature_variance=1+2*mean,peak=peak,strictly_positive_on_grid=bool(np.all(p>0)),
      unimodal=bool(np.all(np.diff(p[:peak+1])>0) and np.all(np.diff(p[peak:])<0)),
      n1_mixed_poisson_residual=float(2*p[0]*p[2]-p[1]**2),minimum_residual=float(residual.min())))
save_json(RUN/'no_go_smooth.json',dict(**IDENTITY,complete=True,rows=rows,
  definition='epsilon*rho_thermal(t)+(1-epsilon)*a_dag*rho_thermal(t)*a/(t+1); diagonal in number'))
