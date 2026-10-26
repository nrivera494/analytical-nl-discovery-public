#!/usr/bin/env python3
"""Conditional common-reservoir Manakov soliton readout reduction.

agent: gpt-b; model: gpt-6-astra; family: gpt.
Algebraic covariance construction, not a simulation of a physical GRIN bath.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from soliton_fano_theory import search_binary,filter_value


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True)
    ap.add_argument('--reference',required=True);ap.add_argument('--output',required=True)
    args=ap.parse_args();started=time.monotonic();data=np.load(args.input)
    v=data['Vamp'];q=data['q'];n=len(q)
    fs=np.fft.fftshift(np.fft.fft(np.fft.ifftshift(q)))/np.sqrt(n)
    reference=json.loads(Path(args.reference).read_text())
    scalar=next(r for r in reference['points'] if r['T0_ps']==.25 and r['temperature_K']==300.)
    rows=[];rng=np.random.default_rng(77311)
    for p in [np.array([.3,.7]),np.array([.2,.3,.5])]:
        c=np.sqrt(p);cc=c[:,None]*c[None,:]
        vm=np.kron(cc,v)+np.kron(np.eye(len(p))-cc,np.eye(n))
        fm=np.kron(c,fs);photons=abs(fm)**2
        sigma=np.sqrt(photons[:,None]*photons[None,:])*vm
        mask,score=search_binary(vm,fm)
        bar=p@mask.reshape(len(p),n)
        scalarp=abs(fs)**2
        loss_formula=1+float((abs(fs)*bar)@(v-np.eye(n))@(abs(fs)*bar)/(scalarp@bar))
        common=np.tile(data['mask'],len(p))
        commonF=filter_value(common,sigma,photons)
        lgen=float(eigh(vm,eigvals_only=True,subset_by_index=[0,0])[0])
        score.update(mode_fractions=p.tolist(),lambda_min=min(1.,scalar['lambda_min']),
            lambda_pass=min(1.,scalar['lambda_pass']),lambda_gen=lgen,
            common_mask_F=commonF,scalar_best_binary_found=scalar['best_binary_found'],
            effective_transmission_formula_F=loss_formula,
            formula_minus_direct=loss_formula-score['best_binary_found'],
            covariance_constructed_from_bright_scalar_and_vacuum_dark=True)
        material=json.loads((Path(args.reference).parent.parent/'material_pilot_n256_w40.json').read_text())
        bound=next(r['lambda_gen'] for r in material['points'] if r['source_model']=='linear_coth_cutoff')
        score['formula_lower_value']=min(1.,bound)
        score['gap_formula_to_binary_dB']=float(10*np.log10(score['best_binary_found']/score['formula_lower_value']))
        for key in ['lambda_min','lambda_pass','lambda_gen','best_binary_found']:
            score[key+'_dB']=float(10*np.log10(score[key]))
        score['gap_gen_to_binary_dB']=float(10*np.log10(score['best_binary_found']/lgen))
        score['gap_min_to_binary_dB']=float(10*np.log10(score['best_binary_found']/score['lambda_min']))
        errors=[]
        for j in range(10):
            trial=(rng.random((len(p),n))<rng.uniform(.1,.9)).astype(float)
            effective=p@trial
            reduced=1+float((abs(fs)*effective)@(v-np.eye(n))@(abs(fs)*effective)/(scalarp@effective))
            errors.append(abs(reduced-filter_value(trial.ravel(),sigma,photons)))
        score['max_random_mask_reduction_error']=max(errors)
        rows.append(score)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',input=args.input,
        scope='Frozen ideal Manakov soliton with one common scalar Raman reservoir, vacuum dark modes and constant mode fractions. Not a physical GRIN reservoir model or an audit of C-20261008-claude-b-01.',
        prior_claim='C-20261008-claude-b-01 is proposed and unverified; read at commit 6c16dc1a0d8ecc348351dbe56a01d28249e1b8ff.',
        points=rows,wall_time_s=time.monotonic()-started)
    Path(args.output).write_text(json.dumps(out,indent=2))
    print(json.dumps({**out,'points':[{k:v for k,v in r.items() if not k.endswith('_indices')} for r in rows]}),flush=True)


if __name__=='__main__':main()
