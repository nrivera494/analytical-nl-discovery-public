#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.
Check the conditional adiabatic gain formula against its covariance ODE.
This does not verify the physical adiabatic reduction.
"""
import argparse
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from mm_soliton_covariance import IDENTITY,family,diffusion,readout,polynomial,dump


def closed(Gamma,z,K,D):
    G=np.exp(Gamma*z);m=K.shape[0];S=np.zeros_like(D)
    S[:m,:m]=D[:m,:m]*G*(G-1)/Gamma
    S[:m,m:2*m]=D[:m,:m]@K*G*(G-1)**2/(2*Gamma**2)
    S[m:2*m,:m]=S[:m,m:2*m].T
    S[m:2*m,m:2*m]=(D[m:2*m,m:2*m]*(1-1/G)/Gamma
        +(K@D[:m,:m]@K)*(G**4-8/3*G**3+2*G**2-1/3)/(4*Gamma**3))
    S[-1,-1]=D[-1,-1]*(G-1)/Gamma
    S[-2,-1]=S[-1,-2]=D[-1,-1]*(G-1-Gamma*z)/Gamma**2
    S[-2,-2]=D[-2,-2]*(1-G**-3)/(3*Gamma)+2*D[-1,-1]*(G-1-Gamma*z-(Gamma*z)**2/2)/Gamma**3
    return S


def main():
    ap=argparse.ArgumentParser();ap.add_argument('profiles');ap.add_argument('out');args=ap.parse_args()
    rows=[];probe=[]
    for pair in ('grin02','grin11','step11'):
        f=dict(np.load(Path(args.profiles)/(pair+'_p0.2_physical.npz')))
        D=diffusion(f,f['s'],f['d'])['gain'];K=f['K']
        for Gamma in (-.1,.03,.1,.3):
            def rhs(z,s):
                G=np.exp(Gamma*z);A=np.zeros((6,6));A[:2,:2]=Gamma*np.eye(2)
                A[2:4,:2]=G*K;A[4,5]=1
                noise=np.zeros((6,6));noise[:2,:2]=G*D[:2,:2];noise[2:4,2:4]=D[2:4,2:4]/G
                noise[4,4]=D[4,4]/G**3;noise[5,5]=G*D[5,5]
                s=s.reshape(6,6)
                return (A@s+s@A.T+noise).ravel()
            sol=solve_ivp(rhs,(0.,4.),np.zeros(36),t_eval=[.5,2.,4.],rtol=2e-11,atol=2e-13)
            for j,z in enumerate(sol.t):
                expected=closed(Gamma,z,K,D);actual=sol.y[:,j].reshape(6,6)
                scale=np.sqrt(expected.diagonal()[:,None]*expected.diagonal()[None,:])
                rows.append(dict(pair=pair,Gamma=Gamma,zeta=z,
                    quantum_gain_noise_bound_satisfied=.1>=abs(Gamma)/2,
                    max_normalized_covariance_difference=float(np.max(abs(actual-expected)/scale))))
        b=float(f['b'][1]);cross=float(f['C'][0,1]);nu=(np.sqrt(1+8*cross/b)-1)/2
        mu=b*nu**2-1;target=.1*2**3*mu**2/24
        for p in (1e-4,1e-5,1e-6,1e-7):
            try:
                ff=family(f['C'],[2*(1-p),2*p],f['b'],scaled_sensitivities=True)
            except RuntimeError as err:
                probe.append(dict(pair=pair,p2=p,status='failed',error=str(err)))
                print(pair,p,str(err),flush=True)
                continue
            X=readout(ff,f['d']);A=X@ff['A']@np.linalg.inv(X)
            Dg=diffusion(ff,f['s'],f['d'])['gain'];c=polynomial(A,X@Dg@X.T)[2,5,5]
            probe.append(dict(pair=pair,p2=p,status='completed',scaled_sensitivities=True,sech_power_exponent=nu,
                probe_lambda=ff['lam'][1],probe_lambda_limit=b*nu**2/2,
                gain_carrier_referenced_phase_cubic_over_q=c,
                gain_phase_cubic_probe_limit=target,relative_error=c/target-1,
                K_symmetry_error=ff['K_symmetry_error']))
            print(pair,p,'relative error',c/target-1,flush=True)
    powers=[]
    for pair in ('grin02','grin11','step11'):
        rr=[r for r in probe if r['pair']==pair and r['status']=='completed' and r['p2']<=1e-5]
        if len(rr)>1:powers.append(dict(pair=pair,relative_error_power=np.polyfit(
            np.log([r['p2'] for r in rr]),np.log(np.abs([r['relative_error'] for r in rr])),1)[0]))
    dump(args.out,dict(**IDENTITY,rows=rows,unequal_GVD_probe_limit=probe,probe_error_scaling=powers,
        initial_failed_attempt=dict(scaled_sensitivities=False,trial_fractions=[1e-4,1e-5,1e-6,1e-7],
            error='Sensitivity BVP exceeded 30000 mesh nodes; original failure did not print the current fraction',
            disposition='Preserved failure; norm-scaled sensitivity variables used for the follow-up'),
        scope='Algebra check of the stipulated adiabatic covariance ODE; no full-field gain verification'))
    print(max(r['max_normalized_covariance_difference'] for r in rows))


if __name__=='__main__':main()
