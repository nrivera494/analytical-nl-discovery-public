#!/usr/bin/env python3
"""Half-line Zakharov-Shabat shooting for real even single-hump launches.
agent: gpt-b; model: gpt-6-astra; family: gpt.
This computes classical soliton content, not its quantum covariance.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def discrete_spectrum(N,shape='gaussian',half_window=12.,max_step=.04):
    def potential(x):
        return N*(np.exp(-x*x/2) if shape=='gaussian' else 1/np.cosh(x))
    area_half=N*(np.sqrt(2*np.pi)/2 if shape=='gaussian' else np.pi/2)
    def angle(eta):
        sol=solve_ivp(lambda x,y:[potential(x)-eta*np.sin(2*y[0])],(-half_window,0),[0.],rtol=1e-10,atol=1e-12,max_step=max_step)
        return sol.y[0,-1]
    targets=np.arange(np.pi/4,area_half,np.pi/2)
    roots=[brentq(lambda e:angle(e)-v,1e-9,N,xtol=1e-11) for v in targets]
    input_energy=N*N*(np.sqrt(np.pi) if shape=='gaussian' else 2)
    return {'N':N,'launch':shape,'eigenvalue_imaginary_parts':roots,'soliton_amplitudes':[2*v for v in roots],
        'number':len(roots),'soliton_energy_fraction':4*sum(roots)/input_energy,
        'half_window':half_window,'max_step':max_step}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    rows=[discrete_spectrum(n) for n in [1.,1.25,1.5,1.75,2.,3.]]
    controls=[discrete_spectrum(n,'sech',half_window=20) for n in [1.,1.25,2.,2.7]]
    for row in controls:
        n=row['N'];exact=[2*n-(2*j+1) for j in range(row['number'])]
        row['exact_sech_amplitudes']=exact
        row['max_absolute_error']=float(np.max(abs(np.array(row['soliton_amplitudes'])-exact)))
    refinements=[discrete_spectrum(n,max_step=.02,half_window=16) for n in [1.25,2.]]
    out={'agent':'gpt-b','model':'gpt-6-astra','family':'gpt','points':rows,'sech_controls':controls,'refinements':refinements,
         'Gaussian_second_soliton_threshold_N':1.5*np.sqrt(np.pi/2)}
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
