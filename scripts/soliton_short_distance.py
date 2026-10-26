#!/usr/bin/env python3
"""Unfitted short-distance even-filter Kerr and Raman coefficients.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from soliton_fano_theory import grid_operators,score_covariance
from soliton_frozen_raman import source_matrix,frozen_covariance


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    start=time.monotonic();n=256;window=40.;x,k,q,a,ft=grid_operators(n,window)
    edge=.7368;mask=(abs(k)<edge).astype(float);g=(ft.conj().T@(mask*(ft@q))).real
    lm=a[:n,n:];source=source_matrix(k,q,.25,300.)
    norm=float(g@g);v=lm@g
    kerr2=float(2*v@(q*q*g)/norm)
    raman3=float(v@source[n:,n:]@v/(3*norm))
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',n=n,window=window,
        edge=edge,T0_ps=.25,temperature_K=300.,kerr_z2_coefficient=kerr2,
        Raman_z3_coefficient=raman3,coefficients_fitted=False,points=[],
        scope='Fixed even mask in the frozen fundamental-soliton model. Coefficients and scores use the same declared Fourier basis.')
    gr=np.r_[g,np.zeros(n)]
    for z in [.05,.1,.2,.4]:
        cov,bath,prop=frozen_covariance(a,source,z)
        row,_,_=score_covariance(cov,q.astype(complex),ft)
        vacuum=float(np.linalg.norm(prop.T@gr)**2/norm)
        reservoir=float(gr@bath@gr/norm)
        row.update(z_over_LD=z,fixed_mask_vacuum=vacuum,fixed_mask_Raman=reservoir,
            fixed_mask_total=vacuum+reservoir,
            vacuum_residual_after_z2=vacuum-1-kerr2*z*z,
            Raman_residual_after_z3=reservoir-raman3*z**3)
        if out['points']:
            last=out['points'][-1]
            for name in ['vacuum_residual_after_z2','Raman_residual_after_z3']:
                row[name+'_power']=float(np.log2(abs(row[name]/last[name])))
        out['points'].append(row);out['wall_time_s']=time.monotonic()-start
        Path(args.output).write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='points'}),flush=True)
    for row in out['points']:
        print({k:v for k,v in row.items() if 'residual' in k or k=='z_over_LD'},flush=True)


if __name__=='__main__':main()
