#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Summarize frozen exact-Kerr tests and plot."""
import json,sys,os
from pathlib import Path
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-b-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RUN=Path(__file__).resolve().parent
def read(name):return json.loads((RUN/name).read_text())
def main():
    exact=read('exact_summary.json');fock=read('fock_summary.json');qmc=read('twa_summary.json')
    sag=read('sagnac_exact.json');sagt=read('sagnac_twa.json');edges=read('gaussian_edges.json')
    finished=all((RUN/f).exists() and read(f).get('complete',False) for f in ['sagnac_resolution.json','sagnac_quantum_reference.json','no_go_smooth.json']) and qmc.get('complete_original_occupation_grid',False)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',run_id=RUN.name,complete=finished,
      definition='n is displacement photons; Sagnac n is per arm; vacuum quadrature variance=1',
      freeze_commit=exact['freeze_commit'],asymptotic_prefactor=3/(2*4**(1/3)),fits=exact['fits'])
    held=[r for r in exact['rows'] if r['nu'] in [3,10,30] and r['n'] in [1e4,1e5,1e6]]
    out['original_displaced_thermal_prediction']=dict(cases=len(held),max_abs_error_dB=max(abs(r['error_dB']) for r in held),passed=all(abs(r['error_dB'])<=1 for r in held))
    large=[r for r in exact['rows'] if r['nu']<=30 and r['n']>=1e8]
    out['large_n_prefactor']=dict(max_relative_error=max(abs(r['exact']['lambda']/r['prediction']-1) for r in large),passed=all(abs(r['exact']['lambda']/r['prediction']-1)<.03 for r in large))
    out['mixedness_scaling_diagnostic']=[]
    for n in [1e8,1e10,1e12]:
      train=[r for r in exact['rows'] if r['n']==n and r['nu'] in [1,10,100]]
      held_nu=[r for r in exact['rows'] if r['n']==n and r['nu'] in [3,30]]
      fit=np.polyfit(np.log([r['nu'] for r in train]),np.log([r['exact']['lambda'] for r in train]),1)
      out['mixedness_scaling_diagnostic'].append(dict(n=n,nu_training=[1,10,100],nu_held_out=[3,30],power=float(fit[0]),
        max_held_out_relative_error=max(abs(r['exact']['lambda']/np.exp(np.polyval(fit,np.log(r['nu'])))-1) for r in held_nu),
        note='Additional diagnostic of the already frozen nu^(4/3) law; nu100 is an edge test, outside the signed-off nu<=30 coefficient domain.'))
    out['fock_oracle']=dict(max_absolute_variance_error=max(abs(r['error']) for r in fock['rows']),max_mean_error=max(r['mean_error'] for r in fock['rows']),max_second_moment_error=max(r['a2_error'] for r in fock['rows']))
    out['fixed_shear_error_exponents']=[]
    for s in [2,4,8]:
      rows=[r for r in exact['fixed'] if r.get('nu')==1 and r.get('s')==s and r.get('n',0)>=1e5 and r.get('n',0)<=1e9]
      # Field definitions are checked below rather than silently inferring a residual.
      if rows and 'fixed_excess' in rows[0]:
        out['fixed_shear_error_exponents'].append(dict(s=s,power=float(np.polyfit(np.log([r['n'] for r in rows]),np.log([r['fixed_excess'] for r in rows]),1)[0])))
    out['curvature_gate']=dict(max_relative_excess_at_R_point8=max(r['relative_excess'] for r in exact['gates'] if r['R']==.8),one_mode_only=True)
    out['twa_exact_optimum_errors']=[dict(n=r['n'],nu=r['nu'],error_dB=r['twa_error_dB']) for r in exact['rows']]
    valid=[r for r in exact['fixed'] if r['n']>=4096 and r['s']<=2*r['n']**(1/6)]
    out['twa_high_occupation_gate']=dict(cases=len(valid),max_abs_error_dB=max(abs(10*np.log10(r['twa']/r['exact'])) for r in valid),
      passed=all(abs(10*np.log10(r['twa']/r['exact']))<.3 for r in valid),observable='optimized single-mode quadrature variance; nu=1,3')
    out['qmc_twa_convergence']=[]
    for n,nu,s in sorted(set((r['n'],r['nu'],r['s']) for r in qmc['rows'])):
      rr=[r for r in qmc['rows'] if (r['n'],r['nu'],r['s'])==(n,nu,s) and r['shots']==65536]
      vals=np.array([r['lambda_qmc'] for r in rr]);out['qmc_twa_convergence'].append(dict(n=n,nu=nu,s=s,mean=float(vals.mean()),se=float(vals.std(ddof=1)/np.sqrt(len(vals))),exact=rr[0]['exact'],analytic_twa=rr[0]['analytic_twa'],analytic_twa_error_dB=float(10*np.log10(rr[0]['analytic_twa']/rr[0]['exact']))))
    out['sagnac_Phi30']=[r for r in sag['rows'] if r['Phi']==30]
    out['sagnac_qmc_Phi30']=[]
    for kind in sorted(set(r['kind'] for r in sagt['rows'])):
      rr=[r for r in sagt['rows'] if r['kind']==kind and r['Phi']==30 and r['shots']==65536]
      vals=np.array([r['tracking_fixed'] for r in rr]);out['sagnac_qmc_Phi30'].append(dict(kind=kind,mean=float(vals.mean()),se=float(vals.std(ddof=1)/2),dB=float(10*np.log10(vals.mean()))))
    out['no_go']=read('no_go.json')['rows']
    if (RUN/'sagnac_resolution.json').exists():out['sagnac_power_integral_refinement']=read('sagnac_resolution.json')
    if (RUN/'sagnac_quantum_reference.json').exists():
      quantum=read('sagnac_quantum_reference.json');out['bright_reference_fock_max_error']=max(r['max_error'] for r in quantum['fock']);out['bright_reference_Phi30']=[]
      out['fixed_number_reference_fock_max_error']=max(r['max_error'] for r in quantum['fixed_number'])
      out['bright_reference_gates']=[]
      for n in [1e10,5e9]:
       for kind in ['none','gaussian052','dirichlet']:
        for Phi in [3,10,30,60]:
          rr=[r for r in quantum['rows'] if r['n_per_arm']==n and r['kind']==kind and r['Phi']==Phi and r['shots']==65536]
          exact_vals=np.array([r['exact_mixture_fixed'] for r in rr]);pred=np.array([r['expected_floor'] for r in rr]);tw=np.array([r['twa_fixed'] for r in rr]);fixed=np.array([r['fixed_N_mixture'] for r in rr])
          out['bright_reference_gates'].append(dict(n_per_arm=n,kind=kind,Phi=Phi,exact_mean=float(exact_vals.mean()),twa_mean=float(tw.mean()),twa_SE=float(tw.std(ddof=1)/2),
            twa_error_dB=float(10*np.log10(tw.mean()/exact_vals.mean())),relative_floor_formula_error=float(exact_vals.mean()/pred.mean()-1),
            one_percent_gate=bool(abs(exact_vals.mean()/pred.mean()-1)<.01),five_percent_gate=bool(abs(exact_vals.mean()/pred.mean()-1)<.05),
            fixed_N_mixture_difference_dB=float(10*np.log10(fixed.mean()/exact_vals.mean())),
            jitter_increment_ratio=float(np.mean([r['jitter_increment_ratio'] for r in rr])) if kind!='none' else None,
            increment_five_percent_gate=bool(abs(np.mean([r['jitter_increment_ratio'] for r in rr])-1)<.05) if kind!='none' else None,
            increment_one_percent_gate=bool(abs(np.mean([r['jitter_increment_ratio'] for r in rr])-1)<.01) if kind!='none' else None,
            exact_shot_rescaled=float(np.mean([r['exact_shot_rescaled'] for r in rr])),
            twa_shot_rescaled=float(np.mean([r['twa_shot_rescaled'] for r in rr])),
            shot_rescaled_one_percent_gate=bool(abs(np.mean([r['exact_shot_rescaled'] for r in rr])/pred.mean()-1)<.01),
            shot_rescaled_relative_formula_error=float(np.mean([r['exact_shot_rescaled'] for r in rr])/pred.mean()-1)))
      for n in [1e10,5e9]:
       for kind in ['none','gaussian052','dirichlet']:
        rr=[r for r in quantum['rows'] if r['n_per_arm']==n and r['kind']==kind and r['Phi']==30 and r['shots']==65536];vv=np.array([r['twa_fixed'] for r in rr]);exact_vals=np.array([r['exact_mixture_fixed'] for r in rr])
        out['bright_reference_Phi30'].append(dict(n_per_arm=n,kind=kind,twa_mean=float(vv.mean()),twa_SE=float(vv.std(ddof=1)/2),exact_mean=float(exact_vals.mean()),exact_zero_jitter=rr[0]['exact_zero_jitter'],epsilon2_mean=float(np.mean([r['epsilon2'] for r in rr])),dB=float(10*np.log10(exact_vals.mean()))))
    out['orientation_edge']=[]
    if (RUN/'no_go_smooth.json').exists():out['unimodal_positive_P_counterexample']=read('no_go_smooth.json')
    for vx in [1e4,1e5]:
      rr=[r for r in edges['rows'] if r['VX']==vx and r['shots']==262144]
      if rr:out['orientation_edge'].append(dict(VX=vx,VP=rr[0]['VP'],nu=rr[0]['nu'],mean_best=float(np.mean([r['best'] for r in rr])),prediction=rr[0]['prediction'],card_gaussian_bound=rr[0]['card_gaussian_bound']))
    out['components']=[p.name for p in sorted(RUN.glob('*.json')) if p.name!='summary.json']
    (RUN/'summary.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
    colors=['#3366aa','#c45d16','#23875b']
    for nu,col in zip([1,10,30],colors):
      rows=[r for r in exact['rows'] if r['nu']==nu and r['n']>=1e4]
      ns=np.array([r['n'] for r in rows]);pred=out['asymptotic_prefactor']*(nu**4/ns)**(1/3)
      ax.loglog(ns,pred,color=col,lw=1.4,label=fr'$\nu={nu}$, asymptotic')
      for r in rows:ax.plot(r['n'],r['exact']['lambda'],'o',ms=5,color=col,mfc='white' if r['held_out'] else col,mew=1.2)
    ax.plot([],[],'o',color='0.2',label='Exact evolution',ms=5)
    ax.plot([],[],'o',color='0.2',mfc='white',label='Frozen held-out case',ms=5)
    ax.set(xlabel=r'Displacement photons per mode $n_d$',ylabel=r'Best quadrature variance (vacuum = 1)')
    ax.legend(fontsize=8,frameon=False,ncol=1);ax.grid(alpha=.15,which='major')
    fig.savefig(RUN/'fig_summary.png',dpi=100,metadata={'Author':'gpt-b / gpt-6-astra / gpt'});plt.close(fig)
if __name__=='__main__':main()
