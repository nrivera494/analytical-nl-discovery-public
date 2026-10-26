#!/usr/bin/env python3
"""Independent continuum-cell evaluation of the material cutoff bound.

agent: gpt-b; model: gpt-6-astra; family: gpt.
These are spectral-amplitude Ritz values, not continuum lower enclosures.
The full-quadrature reference at each point is in the Fourier evaluator.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from scipy.linalg import eigh
from soliton_jost_filter import band_covariances,colored_source_grams,white_source_gram
from soliton_material_lower_bound import lower_spectrum
from soliton_frozen_raman import material_spectrum
from soliton_fano_theory import search_binary


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--widths',nargs='+',type=float,default=[.2,.1,.05])
    ap.add_argument('--order',type=int,default=12)
    args=ap.parse_args();start_all=time.monotonic()
    k=np.linspace(-8,8,101)
    gram,cross,neutral=colored_source_grams(k,spectrum_function=lambda nu:np.ones_like(nu))
    expected_cross=k*(3*k*k+7)/30*np.pi/np.cosh(np.pi*k/2)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=[],
        controls=dict(white_gram_error=float(np.max(abs(gram-white_source_gram(k)))),
            white_cross_error=float(np.max(abs(cross-expected_cross))),
            white_neutral_error=float(abs(neutral-4/15))),
        scope='Convergence checks for the amplitude Ritz restriction; full-field eigenvalues are in matching Fourier runs.')
    for T0,temp,z in [(.2,150.,4.25),(.25,300.,3*np.pi/2),(.35,77.,3.7)]:
      for width in args.widths:
        edges=np.linspace(0,6,round(6/width)+1);point_start=time.monotonic()
        lower,cutoff=lower_spectrum(np.zeros(1),T0,temp)
        matrices={};rows=[]
        for kind in ['linear_coth_cutoff','full_oscillator']:
            spectrum=(lambda nu:lower_spectrum(nu,T0,temp)[0]) if kind=='linear_coth_cutoff' else (lambda nu:material_spectrum(nu,T0,temp))
            ve,vo,energy=band_covariances(z,edges,order=args.order,cutoff=10.,
                spectrum_function=spectrum,source_breakpoints=[cutoff],source_order=320)
            v=.5*np.block([[ve+vo,ve-vo],[ve-vo,ve+vo]])
            m=len(energy);perm=np.r_[np.arange(m)[::-1],np.arange(m,2*m)]
            v=v[np.ix_(perm,perm)];fs=np.sqrt(np.r_[energy,energy]/2)[perm]
            mask,row=search_binary(v,fs)
            row.update(source_model=kind,lambda_gen=float(eigh(v,eigvals_only=True,subset_by_index=[0,0])[0]),
                lambda_even=float(eigh(ve,eigvals_only=True,subset_by_index=[0,0])[0]),
                lambda_odd=float(eigh(vo,eigvals_only=True,subset_by_index=[0,0])[0]))
            for name in ['lambda_gen','best_binary_found','best_interval']:
                row[name+'_dB']=float(10*np.log10(row[name]))
            row['gap_gen_to_binary_dB']=row['best_binary_found_dB']-row['lambda_gen_dB']
            matrices[kind]=v;rows.append(row)
        point=dict(T0_ps=T0,temperature_K=temp,z_over_LD=z,cell_width=width,
            quadrature_order=args.order,material_cutoff_k=cutoff,points=rows,
            source_ordering_min_eigenvalue=float(eigh(matrices['full_oscillator']-matrices['linear_coth_cutoff'],eigvals_only=True)[0]),
            wall_time_s=time.monotonic()-point_start)
        out['points'].append(point);out['wall_time_s']=time.monotonic()-start_all
        Path(args.output).write_text(json.dumps(out,indent=2))
        print(json.dumps({**point,'points':[{k:v for k,v in row.items() if not k.endswith('indices')} for row in rows]}),flush=True)


if __name__=='__main__':main()
