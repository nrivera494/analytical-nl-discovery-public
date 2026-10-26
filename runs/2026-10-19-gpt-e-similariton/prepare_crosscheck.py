"""gpt-e / gpt-6-astra / gpt. Export matched modes for independent RK4IP ASE contraction."""
import json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;RAW=Path('~/analytical-nl-discovery-data')/HERE.name
rows=json.loads((HERE/'fullfield-main.json').read_text())
r=next(r for r in rows if r['epsilon']==.05 and r['tau']==2 and r['chirped'] and r['smoothing']==0)
data=np.load(RAW/'full_eps0.05_tau2.0_chirpTrue_s0.0_n1024_w16.0_steps1024_discrete_readout.npz')
t=data['t'];n=len(t);dt=t[1]-t[0];Gamma=np.sqrt(18);epsilon=.05;tau=2.
p=np.maximum(1-t*t,0);p*=(4/3)/(sum(p)*dt)
initial=np.sqrt(p)*np.exp(-1j*Gamma/3*t*t/(2*epsilon))
mode=data['mean']/np.linalg.norm(data['mean']);q=np.column_stack([mode,1j*mode,(1+1j)*mode/np.sqrt(2)])
s=r['full'];variances=[s['CAA'],s['CPP'],(s['CAA']+s['CPP']+2*s['CAP'])/2]
np.savez(RAW/'crosscheck.npz',t=t,initial=initial,mean=data['mean'],readouts=q,
    variances=np.array(variances),phi=np.array([tau/(Gamma*epsilon)]),dispersion=np.array([epsilon*tau/Gamma]),gain=np.array([tau]))
