"""Independent analysis of a permitted RK4IP paired-perturbation rerun.
gpt-a, gpt-6-astra, gpt. The launch/readout script is Claude-family;
this ODE integration and rate extraction are independently implemented.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import logm
from gain import PROVENANCE
raw=Path('~/analytical-nl-discovery-data/2026-10-11-gpt-a-highlights-audit-c2/c2-shape-e05-u6.json')
d=json.loads(raw.read_text());tau=np.array(d['ref']['tau']);eps=d['eps0'];Gamma=d['params']['Gamma']
kE=d['ref']['E'][0]/(4*d['params']['P0']/3)
a0=np.sqrt(5*d['ref']['varT'][0]);ap0=eps*np.sqrt(5)*d['ref']['cov'][0]/np.sqrt(d['ref']['varT'][0])
out=dict(provenance=PROVENANCE,raw=str(raw),eps=eps,gL=d['gL'],nt=d['Nt'],steps=d['nsteps'],
         forward_wall_seconds=d['t_total_s'],energy_error=d['energy_balance_rel_err'],edge_time=d['edge_time'],edge_freq=d['edge_freq'],modes=[])
for l in range(5):
    ph=np.array(d['readouts_p0to4_n0to4']['ph'+str(l)]);it=np.array(d['readouts_p0to4_n0to4']['int'+str(l)])
    X=np.stack([np.stack([ph[:,l],it[:,l]],axis=1),np.stack([ph[:,5+l]/eps,it[:,5+l]/eps],axis=1)],axis=1)
    M=X@np.linalg.inv(X[0])
    def fun(U,y):
        a,ap=y[:2];H=np.array([[0,kE*np.exp(U)/a/Gamma],[-l*(l+1)/a**2/Gamma,0]])
        return np.r_[ap/Gamma,2*kE*np.exp(U)/a**2/Gamma,(H@y[2:].reshape(2,2)).ravel()]
    sol=solve_ivp(fun,[0,tau[-1]],np.r_[a0,ap0,np.eye(2).ravel()],t_eval=tau,rtol=3e-12,atol=1e-13)
    theory=sol.y[2:].T.reshape(-1,2,2)
    error=np.linalg.norm(M-theory,axis=(1,2))/np.linalg.norm(theory,axis=(1,2))
    row=dict(l=l,max_block_relative_error=float(max(error)),endpoint_block_relative_error=float(error[-1]),
             endpoint_determinant=float(np.linalg.det(M[-1])),endpoint_map=M[-1].tolist(),endpoint_prediction=theory[-1].tolist())
    if l>=2:
        i=np.argmin(abs(tau-3));Q=np.array([np.diag([np.exp(-2*u/3),1])@mm for u,mm in zip(tau,M)])
        gen=logm(Q[-1]@np.linalg.inv(Q[i]))/(tau[-1]-tau[i]);ev=np.linalg.eigvals(gen)
        row.update(measured_decay=float(-ev.real.mean()),measured_frequency=float(max(abs(ev.imag))),
                   predicted_decay=1/3,predicted_frequency=float(np.sqrt(l*(l+1)/2-1)/3))
    out['modes'].append(row)
Path(__file__).with_name('shape.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
