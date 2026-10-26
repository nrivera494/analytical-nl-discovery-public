#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Summarize reproducible Julia outputs; no raw arrays are copied into git."""
from pathlib import Path
import argparse, json, platform, subprocess
import numpy as np
import tomli, yaml
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parents[1]

def fit_mode(t,y,yp,frequency_guess=np.sqrt(2)/3):
    t=np.asarray(t); y=np.asarray(y); yp=np.asarray(yp); t=t-t[0]
    scale=max(np.max(np.abs(y)),1e-14)
    def residual(p):
        d,w,A,B=p; e=np.exp(-d*t); c=np.cos(w*t); s=np.sin(w*t)
        f=e*(A*c+B*s); fp=e*(w*(-A*s+B*c)-d*(A*c+B*s))
        return np.r_[(f-y)/scale,(fp-yp)/scale]
    f=least_squares(residual,[1/3,frequency_guess,y[0],(yp[0]+y[0]/3)/frequency_guess],
        bounds=([0,0,-np.inf,-np.inf],[2,2,np.inf,np.inf]),
        xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=10000)
    return dict(decay_per_gain_length=float(f.x[0]),frequency_per_gain_length=float(f.x[1]),
                relative_joint_rms=float(np.sqrt(np.mean(f.fun*f.fun))))

def load_run(run):
    p=ROOT/'runs'/run
    with (p/'config.toml').open('rb') as f: config=tomli.load(f)
    raw=Path(config['raw_location'])
    records={}
    for case in config['cases']:
        f=raw/(case['label']+'.toml')
        if f.exists():
            with f.open('rb') as h: records[case['label']]=tomli.load(h)
    return p,config,records

def summarize(run,status):
    p,c,recs=load_run(run); cases=[]
    for label,r in recs.items():
        rows=r['rows']; final=rows[-1]
        passed=np.array([row['density_l1']<.10 and abs(row['width_ratio']-1)<.05
            and abs(row['chirp_ratio']-1)<.05 and row['core_scaled_velocity_rms']<.02 for row in rows])
        onward=np.logical_and.accumulate(passed[::-1])[::-1]
        entrance=next((row['gain_length'] for row,ok in zip(rows,onward) if ok),None)
        out={k:v for k,v in r.items() if k not in ['rows']}
        for cap in ['linear_phase_cap','nonlinear_phase_cap']:
            if cap in out and np.isinf(out[cap]): out[cap]='unbounded'
        out.update(final=final,maximum_mass_error=max(abs(t['mass_relative_error']) for t in rows),
                   maximum_time_guard=max(t['time_guard_fraction'] for t in rows),
                   maximum_frequency_guard=max(t['frequency_guard_fraction'] for t in rows),
                   final_pass=bool(passed[-1]),sampled_permanent_entrance=entrance)
        if 'lens_energy' in final:
            z=np.array([t['gain_length'] for t in rows]); en=np.array([t['lens_energy'] for t in rows]); kin=np.array([t['lens_kinetic_energy'] for t in rows])
            out['maximum_sampled_energy_increase']=float(np.max(np.diff(en)))
            # Trapezoidal sampling error is distinct from propagation error.
            out['sampled_energy_balance_residual']=float(en[-1]-en[0]+4/3*np.trapezoid(kin,z))
        cases.append(out)
    fits=[]
    for label,r in recs.items():
        if not label.endswith('_plus'): continue
        ml=label[:-4]+'minus'
        if ml not in recs: continue
        rp=r['rows']; rm=recs[ml]['rows']; ts=np.array([a['gain_length'] for a in rp])
        delta=abs(r['width']-recs[ml]['width']) if '_width_' in label else abs(r['chirp']-recs[ml]['chirp'])
        sp=np.array([a['width_ratio'] for a in rp]); sm=np.array([a['width_ratio'] for a in rm])
        vp=np.array([a['width_ratio']*(a['chirp_ratio']-1)/3 for a in rp]); vm=np.array([a['width_ratio']*(a['chirp_ratio']-1)/3 for a in rm])
        y=(sp-sm)/delta; yp=(vp-vm)/delta
        ff={}
        for lo,hi in [(2,8),(4,10),(6,12)]:
            mask=(ts>=lo-1e-9)&(ts<=hi+1e-9)
            if ts[0]<=lo+1e-9 and ts[-1]>=hi-1e-9: ff[f'{lo}-{hi}']=fit_mode(ts[mask],y[mask],yp[mask])
        fits.append(dict(pair=label[:-5],perturbation_separation=delta,fits=ff))
    result=dict(run_id=run,agent='gpt-a',model='gpt-6-astra',family='gpt',status=status,
        expected_cases=len(c['cases']),completed_cases=len(cases),cases=cases,paired_width_chirp_fits=fits,
        finite_length_criterion=dict(density_l1_max=.10,width_absolute_error_max=.05,chirp_absolute_error_max=.05,
            core_velocity_rms_max=.02,sampling_note='First sampled time passing at every subsequent sample; not a continuous-time or asymptotic basin claim'))
    (p/'summary.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    commit=subprocess.check_output(['git','-C',str(ROOT/'solver'),'rev-parse','HEAD'],text=True).strip()
    meta=dict(run_id=run,agent='gpt-a',model='gpt-6-astra',family='gpt',task='T-20261008-gpt-a-01',
        solver_commit=commit,solver_dirty=False,hardware=platform.platform(),hostname=platform.node(),
        wall_seconds=sum(r['elapsed_seconds'] for r in recs.values()),raw_location=c['raw_location'],
        evaluator='evaluator/similariton_lens.jl' if any('lens' in r['method'] for r in recs.values()) else 'evaluator/similariton_gain.jl',
        summary_evaluator='evaluator/similariton_summarize.py',status=status,
        solver_note='Pinned agents-copy RK4IP/gain; evaluator overrides constant Kerr cache to remove default self-steepening and spectral damping. Lens solver uses independent Strang stages, sharing only initialization/diagnostics.',
        exploration='explorations/2026-10-08-gpt-a-similariton-attraction.md')
    (p/'meta.yaml').write_text(yaml.safe_dump(meta,sort_keys=False))
    print(run,len(cases),'/',len(c['cases']),'pass',sum(a['final_pass'] for a in cases))
    for f in fits: print(json.dumps(f))
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('run');ap.add_argument('--status',default='completed');a=ap.parse_args()
    summarize(a.run,a.status)
