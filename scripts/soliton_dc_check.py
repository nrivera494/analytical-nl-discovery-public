#!/usr/bin/env python3
"""Shared-limit check: uniform Raman phase noise in the frozen soliton.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,null_space
from soliton_fano_theory import grid_operators,spectral_covariance,filter_value
from soliton_frozen_raman import material_spectrum


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True);args=ap.parse_args()
    data=np.load(args.input);v=data['V'];q=data['q'];n=len(q)
    x,k,_,a,ft=grid_operators(n,40.)
    phase=np.r_[np.zeros(n),q];z=3*np.pi/2
    dc=4*material_spectrum(np.array([0.]),.25,300.)[0]*z/n*np.outer(phase,phase)
    basis=null_space(phase[None,:]);rows=[]
    for name,cov in [('finite_DC',v),('DC_removed_diagnostic',v-dc)]:
        amp,fs,_=spectral_covariance(cov,q.astype(complex),ft)
        photons=abs(fs)**2
        row=dict(case=name,lambda_min=float(eigh(cov,eigvals_only=True,subset_by_index=[0,0])[0]),
            lambda_pass=float(eigh(basis.T@cov@basis,eigvals_only=True,subset_by_index=[0,0])[0]),
            lambda_gen=float(eigh(amp,eigvals_only=True,subset_by_index=[0,0])[0]),
            best_binary_found=filter_value(data['mask'],np.sqrt(photons[:,None]*photons[None,:])*amp,photons),
            mask='same previously searched scalar mask; pure DC removal leaves every amplitude mask invariant')
        for key in ['lambda_min','lambda_pass','lambda_gen','best_binary_found']:
            row[key+'_dB']=float(10*np.log10(row[key]))
        row['gap_gen_to_binary_dB']=float(10*np.log10(row['best_binary_found']/row['lambda_gen']))
        row['gap_min_to_binary_dB']=float(10*np.log10(row['best_binary_found']/row['lambda_min']))
        rows.append(row)
    _,_,embedding=spectral_covariance(v,q.astype(complex),ft)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=rows,
        max_amplitude_DC_entry=float(np.max(abs(embedding@dc@embedding.T))),
        norm_generator_phase=float(np.linalg.norm(a@phase)),
        scope='Pure uniform phase reservoir in the frozen Kerr model. DC_removed is a diagnostic, not the physical reservoir used in the task.',
        shared_limit_reference='gpt-a unverified work in progress, commit 2a406511ac1f558fdbe87080dae67d00646299e5; read only in the final hour.')
    Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
