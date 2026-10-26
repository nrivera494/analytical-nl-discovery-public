#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Pinned-solver reference."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from scipy.integrate import solve_ivp
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name
m=Model(5,resonant=False);a=m.launch(.6,4101)
if sys.argv[1]=='prepare':
    memory_gate();np.savez(DATA/'solver_input.npz',tensor=m.tensor,initial=a,groups=m.q)
    out={}
    for kap in [10,40]:
        sol=solve_ivp(lambda t,y:-1j*kap*m.q*y+m.rhs(y),(0,4),a,method='DOP853',rtol=2e-12,atol=2e-13)
        assert sol.success
        out[f'k{kap}']=sol.y[:,-1]
    np.savez(DATA/'solver_reference.npz',**out)
else:
    ref=np.load(DATA/'solver_reference.npz');actual=np.load(DATA/'solver_output.npz');rows=[]
    for kap in [10,40]:
        for h in [.002,.001]:
            result=actual[f'k{kap}_h{h}'];err=float(np.linalg.norm(result-ref[f'k{kap}']))
            rows.append(dict(kappa=kap,step=h,field_error=err,power_error=float(np.max(abs(abs(result)**2-abs(ref[f'k{kap}'])**2))),
                             norm_drift=float(abs(np.sum(abs(result)**2)-1))))
    save_json(RUN/'solver_crosscheck_summary.json',dict(**IDENTITY,solver_commit='b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',
              rows=rows,passed=all(r['field_error']<1e-5 for r in rows)))
    print(rows)
