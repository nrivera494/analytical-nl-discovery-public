#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.
Regenerate the frozen held-out prediction. This does not propagate the field.
"""
import argparse
from pathlib import Path
import numpy as np
from mm_soliton_covariance import family,readout,centre_phase_map,diffusion,polynomial,dump,IDENTITY


def main():
    ap=argparse.ArgumentParser();ap.add_argument('material');ap.add_argument('out');args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    ar=np.load(Path(args.material)/'step_257.npz');S,beta=ar['S'],ar['beta']
    s=np.array([[S[m,m,n,n]/S[0,0,0,0] for n in [0,1]] for m in [0,1]])
    C=2*s-np.diag(s.diagonal());b=beta[2,:2]/beta[2,0]
    d=(beta[1,:2]-beta[1,0])*.35/abs(beta[2,0]);p=.35
    f=family(C,[2*(1-p),2*p],b);X=readout(f,d);A=X@f['A']@np.linalg.inv(X)
    D=diffusion(f,s,d,t0=.35,temperature=77.)
    np.savez_compressed(out/'heldout_step11_p0.35.npz',**f,readout=X,d=d,s=s,t0=.35,temperature=77.)
    coeff={k:polynomial(A,X@v@X.T) for k,v in D.items()}
    L=centre_phase_map(f['N'],b,d)
    dump(out/'summary.json',{**IDENTITY,'task':'T-20261008-gpt-b-01',
        'role':'frozen prediction; no propagation of this case before independent verification',
        'case':'step-index LP01+LP11a','T0_ps':.35,'temperature_K':77.,'p2':p,
        'zeta_targets':[.5,1.,2.,3.],'energy':2.,'b':b,'d':d,'C':C,'s':s,
        'lambda':f['lam'],'K':f['K'],'q_coefficient_convention':'D and covariance divided by q',
        'coordinates':['E','theta','T','V','p2','phi'],
        'coefficients_over_q':coeff,'A':A,
        'phase_reference':'Carrier phases at a fixed time origin; nominal fraction weights',
        'pulse_centre_phase_coefficients_over_q':{k:np.einsum('ia,kab,jb->kij',L,v,L) for k,v in coeff.items()},
        'tolerances':{'secular_model_diagonal_covariance_relative':.002,
                      'relaxed_physical_model_relative':'not asserted before qualification'}})


if __name__=='__main__':main()
