#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Reproducible aggregation of independent squeezing checks."""
import json,sys,os
from pathlib import Path
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-b-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RUN=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def stats(v):
    v=np.asarray(v,float);return dict(mean=float(v.mean()),se=float(v.std(ddof=1)/np.sqrt(len(v))) if len(v)>1 else 0.,values=v.tolist())
def main():
    cases=[]
    for p in sorted(RUN.glob('K*.json')):
      d=read(p)
      if 'records' not in d:continue
      row=dict(file=p.name,**{k:d[k] for k in ['K','E','sigma','launch','disorder','n','zmax','dt','shots','alpha','weyl','max_N_E_drift']},checkpoints=[])
      for j,first in enumerate(d['records'][0]):
        rr=[b[j] for b in d['records']];r={k:first[k] for k in ['z','linear_quad','linear_gen','linear_own','ratio','own_ratio']}
        for k in ['f0','sigma_max']:
          if k in first:r[k]=first[k]
        for k in ['quad_fixed_control','quad_fixed','lambda_quad','count_frozen_weights','count_frozen_weights_control','count_fixed','lambda_gen','lambda_own','own_fixed_control','Fano_N','condensate_coherence','total_coherent_fraction','min_mean_photons']:
          if k in first:r[k]=stats([x[k] for x in rr])
        cross=next(x for x in d['crossfit'] if x['z']==r['z'])
        for k in ['quad_crossfit','count_crossfit']:r[k]=stats(cross[k])
        for obs,lin in [('quad_fixed_control','linear_quad'),('count_frozen_weights','linear_gen'),('count_fixed','linear_gen'),('lambda_gen','linear_gen'),('count_crossfit','linear_gen'),('lambda_own','linear_own')]:
          if obs in r:
            r[obs]['error_dB']=float(10*np.log10(r[obs]['mean']/r[lin]));r[obs]['se_dB']=float(10/np.log(10)*r[obs]['se']/r[obs]['mean'])
        row['checkpoints'].append(r)
      cases.append(row)
    required=['exact3_n64_extra0.json','twa3_n64.json','solver_check.json',
      'K5_E0.6_s0.3_l4203_d7603_h0.005_z100_n1e+06_p9_loss0_w1.json',
      'K5_E0.6_s0.3_l4203_d7603_h0.0025_z100_n1e+06_p9_loss0_w1.json',
      'K5_E0.6_s0_l4213_d7601_h0.01_z100_n1e+06_p9_loss0_w1.json',
      'K5_E0.6_s0_l4201_d7601_h0.02_z100_n1e+06_p10_loss0_w1.json']
    missing=[f for f in required if not (RUN/f).exists()]
    summary=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',run_id=RUN.name,complete=not missing,missing_production_files=missing,cases=cases,
      freeze_commit='9db4bb6a67b640d79365810a984c3af5c6a9da92',
      caution='TWA is a tested approximation, not exact 15-mode quantum evolution. Count fixed uses measured-mean whitening; count_frozen_weights freezes physical weights.')
    core=[d for d in cases if d['E']==.6 and d['sigma']==.3 and d['launch']==4201 and d['disorder']==7601 and d['dt']==.02 and d['shots']==2048 and d['alpha']==0 and d['n'] in [3e5,1e6,3e6]]
    powers=[];coeff=[]
    for b in range(4):
      rr=[next(r for r in d['checkpoints'] if r['z']==10) for d in core];nn=np.array([d['n'] for d in core]);yy=np.array([r['quad_fixed_control']['values'][b]/r['linear_quad']-1 for r in rr]);powers.append(np.polyfit(np.log(nn),np.log(yy),1)[0]);coeff.append(np.mean(yy/np.array([r['ratio'] for r in rr])))
    summary['core_quad_scaling']=dict(exponent=stats(powers),relative_curvature_coefficient=stats(coeff),fit_n=[3e5,1e6,3e6],z=10,coefficient_definition='(V_fixed/V_linear-1)/(sigma_max^6/n0); between-scramble SE only')
    summary['curvature_coefficient_resolution']=[]
    for d in cases:
      if d['E']==.6 and d['sigma']==.3 and d['n']==1e6 and d['launch']==4201 and d['shots']==2048 and d['alpha']==0:
        r=next(r for r in d['checkpoints'] if r['z']==10);vv=(np.array(r['quad_fixed_control']['values'])/r['linear_quad']-1)/r['ratio']
        summary['curvature_coefficient_resolution'].append(dict(dt=d['dt'],coefficient=stats(vv)))
    gates=[]
    for E,n,zsmall,zlarge in [(.9,1e10,[5,10,20],[50,100]),(.3,1e8,[5,10],[20,50])]:
      dd=[d for d in cases if d['E']==E and d['n']==n and d['sigma']==.3 and d['launch']==4201 and d['dt']==.02 and d['shots']==2048 and d['zmax']==100 and d['alpha']==0]
      if not dd:continue
      for r in dd[0]['checkpoints']:
        if r['z'] not in zsmall+zlarge:continue
        e=r['quad_fixed_control']['error_dB'];passed=abs(e)<1 if r['z'] in zsmall else e>3
        gates.append(dict(E=E,n=n,z=r['z'],error_dB=e,passed=bool(passed),gate='within1dB' if r['z'] in zsmall else 'above3dB'))
    summary['original_held_out_quadrature']=gates
    early=[r for d in cases if d['alpha']==0 and d['weyl'] for r in d['checkpoints'] if r['z']<=20 and r['ratio']<=.8]
    summary['small_curvature_gate']=dict(cases=len(early),max_abs_fixed_direction_error_dB=float(max(abs(r['quad_fixed_control']['error_dB']) for r in early)),passed=all(abs(r['quad_fixed_control']['error_dB'])<1 for r in early))
    interior=[r for d in cases if d['K']==5 and d['sigma']==.3 and d['alpha']==0 and d['weyl'] and 1e6<=d['n']<=1e10 for r in d['checkpoints'] if 5<=r['z']<=20 and r['ratio']<=.8 and .55<=r.get('f0',-1)<=.87]
    summary['original_rectangle_curvature_gate']=dict(cases=len(interior),max_abs_error_dB=max(abs(r['quad_fixed_control']['error_dB']) for r in interior) if interior else None,
      passed=bool(interior) and all(abs(r['quad_fixed_control']['error_dB'])<1 for r in interior),note='Enforces the original f0 bound; Eprime alone does not ensure it for this independent launch.')
    ceiling=[(d,r) for d in cases if d['K']==5 and d['n']==1e10 and d['alpha']==0 and d['weyl'] and d['dt']==.02 and d['shots']==2048 for r in d['checkpoints'] if 5<=r['z']<=100]
    summary['multimode_ceiling_conjecture']=dict(checkpoints=len(ceiling),minimum_optimized_dB=float(min(10*np.log10(r['lambda_quad']['mean']) for d,r in ceiling)),minimum_crossfit_dB=float(min(10*np.log10(r['quad_crossfit']['mean']) for d,r in ceiling)),passed_at_sampled_checkpoints=bool(all(r['lambda_quad']['mean']>=10**-3.5 for d,r in ceiling)),continuous_z_or_universal_bound_proved=False)
    summary['counting_long_distance']=[]
    for d in cases:
      if d['E']!=.6 or d['sigma']!=.3 or d['launch']!=4201 or d['n']!=1e10 or d['zmax']!=300 or d['alpha']!=0:continue
      for r in d['checkpoints']:
        if r['z'] not in [200,300]:continue
        summary['counting_long_distance'].append(dict(file=d['file'],dt=d['dt'],shots=d['shots'],z=r['z'],linear=r['linear_gen'],frozen_weights=r.get('count_frozen_weights'),optimized=r['lambda_gen'],crossfit=r['count_crossfit'],coherence=r.get('condensate_coherence'),crossfit_pass_1dB=bool(abs(r['count_crossfit']['error_dB'])<1)))
    summary['counting_resolution']=[]
    for launch in [4201,4203]:
      dd=[d for d in cases if d['E']==.6 and d['sigma']==.3 and d['launch']==launch and d['n']==1e6 and d['zmax']==100 and d['shots']==2048 and d['alpha']==0]
      dd=sorted(dd,key=lambda d:d['dt'],reverse=True)
      for coarse,fine in zip(dd[:-1],dd[1:]):
        a=next(r for r in coarse['checkpoints'] if r['z']==100);b=next(r for r in fine['checkpoints'] if r['z']==100)
        if 'count_frozen_weights' not in a or 'count_frozen_weights' not in b:continue
        delta=b['count_frozen_weights']['error_dB']-a['count_frozen_weights']['error_dB']
        paired=10/np.log(10)*(np.array(b['count_frozen_weights']['values'])/b['count_frozen_weights']['mean']-np.array(a['count_frozen_weights']['values'])/a['count_frozen_weights']['mean'])
        se=float(np.std(paired,ddof=1)/2)
        summary['counting_resolution'].append(dict(launch=launch,coarse=coarse['dt'],fine=fine['dt'],difference_of_discrepancy_dB=delta,paired_sampling_SE_dB=se,converged_by_frozen_gate=bool(abs(delta)<max(.3,3*se)),fine_discrepancy_dB=b['count_frozen_weights']['error_dB'],fine_discrepancy_SE=b['count_frozen_weights']['se_dB'],exceeds_original_point5_by_3SE=bool(b['count_frozen_weights']['error_dB']-3*b['count_frozen_weights']['se_dB']>.5),
          note='Common random vacuum samples require paired SE; adding the two marginal SEs in quadrature would be inappropriate.'))
    summary['counting_resolution_all_observables']=[]
    for launch in [4201,4203]:
      dd=sorted([d for d in cases if d['E']==.6 and d['sigma']==.3 and d['launch']==launch and d['n']==1e6 and d['zmax']==100 and d['shots']==2048 and d['alpha']==0],key=lambda d:d['dt'],reverse=True)
      for coarse,fine in zip(dd[:-1],dd[1:]):
        a=next(r for r in coarse['checkpoints'] if r['z']==100);b=next(r for r in fine['checkpoints'] if r['z']==100)
        for obs in ['count_frozen_weights','lambda_gen','count_crossfit']:
          if obs not in a or obs not in b:continue
          delta=b[obs]['error_dB']-a[obs]['error_dB'];paired=10/np.log(10)*(np.array(b[obs]['values'])/b[obs]['mean']-np.array(a[obs]['values'])/a[obs]['mean']);se=float(paired.std(ddof=1)/2)
          summary['counting_resolution_all_observables'].append(dict(launch=launch,observable=obs,coarse=coarse['dt'],fine=fine['dt'],difference_dB=delta,paired_SE_dB=se,
            convergence_pass=bool(abs(delta)<max(.3,3*se)),fine_error_dB=b[obs]['error_dB'],fine_sampling_SE_dB=b[obs]['se_dB'],original_point5_failure_by_3SE=bool(b[obs]['error_dB']-3*b[obs]['se_dB']>.5),
            note='Cross-fit fold SE is descriptive; optimized batch estimates have independent scrambles and downward selection bias.'))
    summary['exact_exchange']=[]
    for p in sorted(RUN.glob('exact3_n*_extra0.json')):
      d=read(p);n=d['n'];tp=RUN/f'twa3_n{n}.json'
      if not d.get('reference_valid',False) or not tp.exists():continue
      tw=read(tp)
      for r in d['rows']:
        if r['z']==0:continue
        rr=[next(x for x in b['rows'] if x['z']==r['z']) for b in tw['records'] if b['dt']==.01]
        vals={k:stats([x[k] for x in rr]) for k in ['lambda_quad','lambda_gen','lambda_own']}
        exact_own=float(np.linalg.eigvalsh(np.array(r['V'])[np.ix_([0,3],[0,3])])[0])
        summary['exact_exchange'].append(dict(n=n,z=r['z'],exact_quad=r['lambda_quad'],exact_count=r['lambda_gen'],
          exact_own=exact_own,twa_own=vals['lambda_own'],own_error_dB=float(10*np.log10(vals['lambda_own']['mean']/exact_own)),
          twa_quad=vals['lambda_quad'],twa_count=vals['lambda_gen'],quad_error_dB=float(10*np.log10(vals['lambda_quad']['mean']/r['lambda_quad'])),count_error_dB=float(10*np.log10(vals['lambda_gen']['mean']/r['lambda_gen']))))
    summary['exact_exchange_convergence']={}
    fock=[read(p) for p in RUN.glob('exact3_n*_extra*.json') if read(p).get('reference_valid',False)]
    if fock:
      a=read(RUN/'exact3_n16_extra0.json');b=read(RUN/'exact3_n16_extra20.json')
      summary['exact_exchange_convergence']=dict(max_norm_error=max(abs(r['norm']-1) for d in fock for r in d['rows']),
        max_total_Fano_error=max(abs(r['total_Fano']-1) for d in fock for r in d['rows']),
        cutoff_max_variance_change=max(abs(x[k]-y[k]) for x,y in zip(a['rows'],b['rows']) for k in ['lambda_quad','lambda_gen']),
        held_out_n64_quad_z1=next((r for r in summary['exact_exchange'] if r['n']==64 and r['z']==1),None))
    summary['deterministic_counting']=[]
    for d in cases:
      if d['sigma']!=0 or d['n']!=1e6:continue
      r=next(x for x in d['checkpoints'] if x['z']==100)
      summary['deterministic_counting'].append(dict(file=d['file'],launch=d['launch'],dt=d['dt'],shots=d['shots'],
        frozen=r.get('count_frozen_weights'),optimized=r['lambda_gen'],crossfit=r['count_crossfit'],coherence=r.get('condensate_coherence'),min_mean_photons=r.get('min_mean_photons')))
    lossless=[d for d in cases if d['alpha']==0]
    raw=Path('~/analytical-nl-discovery-data')/RUN.name
    tangent=[];projection_checks=[]
    for p in sorted(raw.glob('*_tangent.json')):
      d=read(p)
      for r in d['rows']:
        tangent.append(dict(file=p.name,z=r['z'],symplectic=r['symplectic_error'],reciprocal=r['reciprocal_error'],
          N_drift=abs(r['N']-1),E_drift=abs(r['E']-d['E']),Fano_error=abs(r['Fano_N']-1)))
      xx=np.load(p.with_suffix('.npz'))['x']
      for x,r in zip(xx,d['rows']):
        a=x[0];M=len(a);S=np.concatenate([x[1:].real,x[1:].imag],axis=1).T;phase=np.angle(a)
        P=np.zeros((M,2*M));P[np.arange(M),np.arange(M)]=np.cos(phase);P[np.arange(M),np.arange(M)+M]=np.sin(phase)
        A_blas=P@S
        A=np.einsum('ij,jk->ik',P,S,optimize=False)
        gram=np.einsum('ik,jk->ij',A,A,optimize=False)
        assert np.all(np.isfinite(S)) and np.all(np.isfinite(A_blas)) and np.all(np.isfinite(gram)),p
        stable=np.linalg.eigvalsh(gram)[0]
        projection_checks.append(dict(file=p.name,z=r['z'],stable_count=stable,recorded_count=r['lambda_gen'],error_dB=float(10*np.log10(stable/r['lambda_gen'])),
          blas_vs_direct_relative_error=float(np.max(abs(A_blas-A))/max(1.,np.max(abs(A))))))
    early=[r for r in tangent if r['z']<=20];late=[r for r in tangent if r['z']<=100]
    summary['artifacts']=dict(lossless_max_N_E_drift=np.max([d['max_N_E_drift'] for d in lossless],axis=0).tolist(),
      tangent_early_max={k:max(r[k] for r in early) for k in ['symplectic','reciprocal','N_drift','E_drift','Fano_error']},
      tangent_through100_max={k:max(r[k] for r in late) for k in ['symplectic','reciprocal','N_drift','E_drift','Fano_error']},
      tangent_overall_max={k:max(r[k] for r in tangent) for k in ['symplectic','reciprocal','N_drift','E_drift','Fano_error']},
      caution='Conserved quantities do not certify converged chaotic trajectories or optimized noise.')
    summary['artifacts']['stable_projection_max_error_dB']=max(abs(r['error_dB']) for r in projection_checks)
    summary['artifacts']['blas_projection_max_relative_error']=max(r['blas_vs_direct_relative_error'] for r in projection_checks)
    summary['artifacts']['stable_projection_worst_cases']=sorted(projection_checks,key=lambda r:abs(r['error_dB']),reverse=True)[:5]
    summary['artifacts']['total_Fano_max_departure_from_one']=max(abs(r['Fano_N']['mean']-1) for d in lossless for r in d['checkpoints'])
    summary['artifacts']['total_Fano_max_change_over_distance']=max(max(r['Fano_N']['mean'] for r in d['checkpoints'])-min(r['Fano_N']['mean'] for r in d['checkpoints']) for d in lossless)
    summary['second_solver']=read(RUN/'solver_check.json')
    summary['component_files']=[p.name for p in sorted(RUN.glob('*.json')) if p.name!='summary.json']
    (RUN/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    # A single-panel test of the narrowed curvature scaling. Open symbols are original held-out E' cases.
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(6,4),layout='constrained');col={.3:'#23875b',.6:'#3366aa',.9:'#c45d16'}
    for E in [.6,.3,.9]:
      points=[]
      for d in cases:
        if d['E']!=E or d['sigma']!=.3 or d['launch']!=4201 or d['dt']!=.02 or d['shots']!=2048 or d['alpha']!=0 or not d['weyl']:continue
        # Use z10: fixed classical trajectory, frozen n scan; avoid fitting distance-dependent coefficients.
        r=next((r for r in d['checkpoints'] if r['z']==10),None)
        if r is None or (E==.6 and d['n'] not in [3e5,1e6,3e6,1e8,1e10]):continue
        y=r['quad_fixed_control']['mean']/r['linear_quad']-1;se=r['quad_fixed_control']['se']/r['linear_quad']
        if y>0:points.append((r['ratio'],y,se))
      if points:
        x,y,err=np.array(points).T;ax.errorbar(x,y,yerr=err,fmt='o',ms=5,color=col[E],mfc=col[E] if E==.6 else 'white',capsize=2,label=fr"$E'={E}$"+(' (held out)' if E!=.6 else ''))
    xx=np.geomspace(.003,300,200);cc=summary['core_quad_scaling']['relative_curvature_coefficient']['mean']
    ax.plot(xx,cc*xx,color='0.15',label=fr'Fit: ${cc:.3f}\,\sigma_{{max}}^6/n_0$')
    ax.axvline(.8,color='0.55',ls=':',lw=1,label='Claimed validity threshold')
    ax.set(xscale='log',yscale='log',xlabel=r'Shear ratio $\sigma_{max}^6/n_0$ (dimensionless)',ylabel=r'Excess fixed-direction variance $V/V_{lin}-1$')
    ax.legend(fontsize=8,frameon=False);ax.grid(alpha=.15);fig.savefig(RUN/'fig_summary.png',dpi=100,metadata={'Author':'gpt-b / gpt-6-astra / gpt'});plt.close(fig)
if __name__=='__main__':main()
