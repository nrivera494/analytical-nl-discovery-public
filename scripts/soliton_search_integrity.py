#!/usr/bin/env python3
"""Recontract saved masks directly and stress-test binary-search arithmetic.
agent: gpt-b; model: gpt-6-astra; family: gpt.
Preserves original outputs; this is a numerical-integrity check, not a
global-optimality certificate for large masks.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from soliton_fano_theory import search_binary,filter_value
from soliton_fano_theory import grid_operators
from soliton_frozen_raman import source_matrix,frozen_covariance


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--output',required=True)
    args=ap.parse_args();start=time.monotonic();root=Path(args.data)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',saved_masks=[],small_exhaustive_checks=[],
        scope='Direct score integrity and small independent exhaustive comparisons; no large-mask optimality certificate.')
    for path in sorted(root.glob('2026-10-10-gpt-b-soliton-*/*.npz'))+sorted(root.glob('2026-10-10-gpt-b-soliton-*/*/*.npz')):
        with np.load(path) as data:
            if 'mask' not in data:continue
            mask=data['mask']
            if 'Vamp' in data:
                v=data['Vamp']
                if 'fs' in data:fs=data['fs']
                elif 'photons' in data:fs=np.sqrt(data['photons'])
                elif 'q' in data:
                    fs=np.fft.fftshift(np.fft.fft(np.fft.ifftshift(data['q'])))/np.sqrt(len(mask))
                else:continue
            elif 'V' in data and 'fs' in data:
                fs=data['fs'];v=data['V'][:len(fs),:len(fs)]
            else:continue
            photons=abs(fs)**2;sigma=np.sqrt(photons[:,None]*photons[None,:])*v
            direct=filter_value(mask,sigma,photons)
            lower=float(eigh(v,eigvals_only=True,subset_by_index=[0,0])[0])
            row=dict(source=str(path.relative_to(root)),transmitted_fraction=float(photons@mask/photons.sum()),
                direct_F=direct,lambda_gen=lower,nonempty=bool(np.count_nonzero(mask)),
                rayleigh_consistent=bool(direct>=lower-1e-9))
            sibling=path.with_suffix('.json')
            if sibling.exists():
                old=json.loads(sibling.read_text())
                if 'best_binary_found' in old:
                    row['stored_F']=old['best_binary_found'];row['stored_minus_direct']=old['best_binary_found']-direct
            out['saved_masks'].append(row)
    distance_path=root/'2026-10-10-gpt-b-soliton-raman/distance/summary.json'
    if distance_path.exists():
        distance=json.loads(distance_path.read_text());n=distance['n']
        x,k,q,a,ft=grid_operators(n,distance['window'])
        _,stepbath,step=frozen_covariance(a,source_matrix(k,q,1.,300.,unit=True),distance['dz'])
        prop=np.eye(2*n);bath=np.zeros_like(prop);out['distance_masks']=[]
        fs=ft@q
        for j,z in enumerate(sorted(set(r['z_over_LD'] for r in distance['points']))):
            if j:
                with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
                    prop=step@prop;bath=step@bath@step.T+stepbath
                bath=(bath+bath.T)/2
            for row in [r for r in distance['points'] if r['z_over_LD']==z]:
                mask=np.zeros(n);mask[row['binary_indices']]=1
                g=ft.conj().T@(mask*fs);gr=np.r_[g.real,g.imag]
                with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
                    direct=float((np.linalg.norm(prop.T@gr)**2+row['rho']*(gr@bath@gr))/np.vdot(g,g).real)
                out['distance_masks'].append(dict(z_over_LD=z,temperature_K=row['temperature_K'],
                    stored_F=row['best_binary_found'],direct_F=direct,nonempty=bool(mask.any()),
                    stored_minus_direct=row['best_binary_found']-direct,
                    rayleigh_consistent=bool(direct>=row['lambda_gen']-1e-9)))
    # Exhaustion is independent of the interval and incremental-flip logic.
    rng=np.random.default_rng(12341);n=10
    masks=((np.arange(1,2**n)[:,None]>>np.arange(n))&1).astype(float)
    for case in range(12):
        orth,_=np.linalg.qr(rng.normal(size=(n,n)))
        vals=np.geomspace(.03,30,n);v=(orth*vals)@orth.T
        photons=10.**rng.uniform(-11,0,n);fs=np.sqrt(photons)
        sigma=np.sqrt(photons[:,None]*photons[None,:])*v
        exact=min(filter_value(mask,sigma,photons) for mask in masks)
        mask,score=search_binary(v,fs,starts=32,anneal_steps=1000)
        direct=filter_value(mask,sigma,photons)
        out['small_exhaustive_checks'].append(dict(case=case,exhaustive_min=exact,
            search_F=score['best_binary_found'],direct_F=direct,nonempty=bool(mask.any()),
            no_false_improvement=bool(direct>=exact-1e-10),cached_score_error=score['best_binary_found']-direct))
    out['all_saved_masks_valid']=all(r['nonempty'] and r['rayleigh_consistent'] and np.isfinite(r['direct_F']) for r in out['saved_masks'])
    out['all_small_checks_valid']=all(r['nonempty'] and r['no_false_improvement'] and abs(r['cached_score_error'])<1e-12 for r in out['small_exhaustive_checks'])
    out['all_distance_masks_valid']=all(r['nonempty'] and r['rayleigh_consistent'] and abs(r['stored_minus_direct'])<1e-10 for r in out.get('distance_masks',[]))
    out['wall_time_s']=time.monotonic()-start
    Path(args.output).write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ['saved_masks','small_exhaustive_checks','distance_masks']}),flush=True)


if __name__=='__main__':main()
