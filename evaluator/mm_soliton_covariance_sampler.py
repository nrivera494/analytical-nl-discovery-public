#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.
Local real transverse phonons, projected before averaging modal beat phase.
Independent of the secular complex-pair contraction implementation.
"""
import argparse
from pathlib import Path
import numpy as np
from mm_soliton_covariance import IDENTITY, dump, spectrum, diffusion, readout


def main():
    ap=argparse.ArgumentParser();ap.add_argument('profile');ap.add_argument('material');ap.add_argument('out')
    ap.add_argument('--ntraj',type=int,default=16384);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    fam=dict(np.load(args.profile));mat=np.load(args.material)
    phi=mat['fields'][:,:,:2];dx=mat['x'][1]-mat['x'][0];dy=mat['y'][1]-mat['y'][0]
    # Construct the bath directly from transverse mode samples, not S.
    spatial=np.stack([phi[:,:,0]**2,phi[:,:,1]**2,phi[:,:,0]*phi[:,:,1]],axis=-1).reshape(-1,3)
    gram=np.einsum('ra,rb->ab',spatial,spatial)*dx*dy/mat['S'][0,0,0,0]
    w,U=np.linalg.eigh(gram);root=U*np.sqrt(np.maximum(w,0))
    nt=len(fam['t']);dt=float(fam['dt']);d=fam['d'];b=fam['b']
    gauge=np.exp(-1j*fam['t'][:,None]*d/b)
    a=fam['f']*gauge;X=readout(fam,d)
    g=np.einsum('tma,ba->tmb',fam['g'],X)*gauge[:,:,None]
    rng=np.random.default_rng(2026100803)
    rows=[]
    for temperature in [0.,300.]:
        psd=spectrum(fam['k'],temperature=temperature)
        samples=np.empty((args.ntraj,6))
        for start in range(0,args.ntraj,128):
            nb=min(128,args.ntraj-start)
            white=rng.standard_normal((nt,3,nb))
            coloured=np.fft.ifft(np.fft.fft(white,axis=0)*np.sqrt(psd/dt)[:,None,None],axis=0).real
            eta=np.einsum('ab,tbq->taq',root,coloured)
            beat=np.exp(1j*rng.uniform(0,2*np.pi,size=nb))
            kick=np.empty((nt,2,nb),complex)
            kick[:,0]=1j*(a[:,0,None]*eta[:,0]+a[:,1,None]*eta[:,2]*beat)
            kick[:,1]=1j*(a[:,1,None]*eta[:,1]+a[:,0,None]*eta[:,2]*beat.conj())
            samples[start:start+nb]=dt*np.real(np.einsum('tma,tmq->qa',g.conj(),kick))
        expected=X@diffusion(fam,fam['s'],d,temperature=temperature)['raman']@X.T
        cov=np.cov(samples,rowvar=False)
        scale=np.sqrt(expected.diagonal()[:,None]*expected.diagonal()[None,:])
        normalized=np.divide(cov-expected,scale,out=np.zeros_like(cov),where=scale>1e-12)
        ratio=np.divide(cov.diagonal(),expected.diagonal(),out=np.zeros(6),where=expected.diagonal()>1e-12)
        centered=samples-samples.mean(axis=0)
        fourth=np.mean(centered**4,axis=0)
        variance=np.mean(centered**2,axis=0)
        variance_se=np.sqrt(np.maximum(fourth-variance**2,0)/args.ntraj)
        relative_se=np.divide(variance_se,variance,out=np.zeros(6),where=variance>1e-25)
        np.savez_compressed(out/f'samples_{temperature:g}K.npz',samples=samples)
        rows.append(dict(temperature_K=temperature,analytic=expected,sampled=cov,diagonal_ratios=ratio,
            empirical_variance_relative_se=relative_se,
            max_normalized_error=np.max(np.abs(normalized)),
            conserved_total_energy_max_abs=np.max(np.abs(samples[:,0]))))
    dump(out/'summary.json',dict(**IDENTITY,task='T-20261008-gpt-b-01',
        profile=args.profile,material=args.material,transverse_gram=gram,ntraj=args.ntraj,
        seed=2026100803,nominal_gaussian_variance_relative_se=np.sqrt(2/(args.ntraj-1)),rows=rows,
        note='Random real local bath and uniformly sampled longitudinal beat phase; not a multimode stochastic soliton solver'))
    for row in rows:print(row['temperature_K'],row['diagonal_ratios'],row['max_normalized_error'])


if __name__=='__main__':main()
