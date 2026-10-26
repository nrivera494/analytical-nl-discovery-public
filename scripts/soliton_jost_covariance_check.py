#!/usr/bin/env python3
"""Continuum-only spectral-cell checks of the explicit soliton kernels.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from scipy.linalg import eigh
from soliton_jost_filter import band_covariances
from soliton_fano_theory import search_binary


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True)
    args=ap.parse_args();dest=Path(args.raw);dest.mkdir(parents=True,exist_ok=True)
    summary=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=[])
    for z,rho in [(3*np.pi/2,0.),(3*np.pi/2,.11483961911590272),(5.25,.11483961911590272)]:
      for width,order in [(.2,12),(.1,12),(.05,12),(.1,24)]:
        start=time.monotonic();edges=np.linspace(0,6,round(6/width)+1)
        ve,vo,energy=band_covariances(z,edges,order=order,cutoff=10.,rho=rho)
        # Positive/negative half-cell amplitudes are the orthogonal sum and
        # difference of normalized even/odd quadratures.
        v=.5*np.block([[ve+vo,ve-vo],[ve-vo,ve+vo]])
        m=len(energy);perm=np.r_[np.arange(m)[::-1],np.arange(m,2*m)]
        v=v[np.ix_(perm,perm)];fs=np.sqrt(np.r_[energy,energy]/2)[perm]
        mask,row=search_binary(v,fs)
        row.update(z_over_LD=z,rho=rho,cell_width=width,quadrature_order=order,
                   output_cutoff=6.,continuum_cutoff=10.,
                   lambda_gen=float(eigh(v,eigvals_only=True,subset_by_index=[0,0])[0]),
                   lambda_even=float(eigh(ve,eigvals_only=True,subset_by_index=[0,0])[0]),
                   lambda_odd=float(eigh(vo,eigvals_only=True,subset_by_index=[0,0])[0]),
                   wall_time_s=time.monotonic()-start)
        for key in ['lambda_gen','best_binary_found','best_interval']:
            row[key+'_dB']=float(10*np.log10(row[key]))
        row['gap_gen_to_binary_dB']=row['best_binary_found_dB']-row['lambda_gen_dB']
        summary['points'].append(row)
        name=f'z{z:.8g}_rho{rho:.8g}_cell{width:g}_order{order}'
        np.savez_compressed(dest/(name+'.npz'),Vamp=v,edges=edges,mask=mask,photons=fs**2)
        (dest/'summary.json').write_text(json.dumps(summary,indent=2))
        print(json.dumps({k:v for k,v in row.items() if not k.endswith('indices')}),flush=True)


if __name__=='__main__':main()
