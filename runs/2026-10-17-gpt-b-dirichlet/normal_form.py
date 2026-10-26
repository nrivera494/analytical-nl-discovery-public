#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Full-tensor normal-form check."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from scipy.integrate import solve_ivp
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def main():
    memory_gate();res=Model(5);full=Model(5,resonant=False);rows=[]
    t=np.linspace(0,4,401)
    for seed in [4101,4102,4103]:
        a=res.launch(.6,seed)
        rr=solve_ivp(lambda t,y:res.rhs(y),(0,4),a,t_eval=t,method='DOP853',rtol=2e-11,atol=2e-12).y.T
        for kap in [10,20,40,80]:
            def rhs(t,y):
                u=np.exp(-1j*kap*res.q*t)
                return np.conj(u)*full.rhs(u*y)
            sol=solve_ivp(rhs,(0,4),a,t_eval=t,method='DOP853',rtol=2e-11,atol=2e-12)
            y=sol.y.T;u=y*np.exp(-1j*kap*t[:,None]*res.q)
            inv=full.invariants(u);htot=kap*inv[:,1]+inv[:,2]
            rows.append(dict(seed=seed,kappa=kap,epsilon=1/kap,
                field_error_rms=float(np.sqrt(np.mean(np.sum(abs(y-rr)**2,axis=1)))),
                field_error_max=float(np.max(np.linalg.norm(y-rr,axis=1))),
                power_error_rms=float(np.sqrt(np.mean((abs(y)**2-abs(rr)**2)**2))),
                max_N_drift=float(np.max(abs(inv[:,0]-inv[0,0]))),
                max_E_drift=float(np.max(abs(inv[:,1]-inv[0,1]))),
                max_Htotal_drift=float(np.max(abs(htot-htot[0]))),evaluations=sol.nfev))
    exps=[]
    for seed in [4101,4102,4103]:
        r=[x for x in rows if x['seed']==seed]
        exps.append(dict(seed=seed,exponent=float(np.polyfit(np.log([x['epsilon'] for x in r]),
                                      np.log([x['field_error_rms'] for x in r]),1)[0])))
    # Cutoff breaks the Kohn/breathing identities at populated high groups.
    rng=np.random.default_rng(8123);a=shell_samples(res,.6,1,rng)[0];f=res.rhs(a)
    deriv={name:[float(v.real),float(v.imag)] for name,mat in [('L',res.L),('X',res.X),('Y',res.Y),('B',res.B)]
           for v in [np.vdot(f,mat@a)+np.vdot(a,mat@f)]}
    # Check the host BLAS warning against a contraction without BLAS.
    test=rng.random((2000,15));blas=test.T@test;reference=np.einsum('ni,nj->ij',test,test,optimize=False)
    save_json(RUN/'normal_form_summary.json',dict(**IDENTITY,rows=rows,exponents=exps,
        cutoff_bilinear_derivatives=deriv,blas_check_max_abs_error=float(np.max(abs(blas-reference))),
        note='Same conservative sign for full and averaged equations; no assertion of long-distance averaging.'))
    print(serializable(exps),flush=True)

if __name__=='__main__':main()
