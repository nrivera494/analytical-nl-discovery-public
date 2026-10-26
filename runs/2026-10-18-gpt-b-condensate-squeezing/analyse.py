#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Condensate ensemble, curvature and loss report."""
import json,os,sys
from pathlib import Path
import numpy as np
from scipy.stats import t,chi2
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/gpt-b-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RUN=Path(__file__).resolve().parent;GRIN=RUN.parent/'2026-10-18-gpt-b-grin-squeezing'
sys.path.insert(0,str(RUN.parents[1]/'evaluator'))
from kerr_squeezing import moments
def read(p):return json.loads(p.read_text())
def statistics(v):
    v=np.array(v,float);m=len(v);sd=float(v.std(ddof=1));se=sd/np.sqrt(m)
    return dict(members=m,mean=float(v.mean()),sd=sd,se=float(se),mean_95CI=[float(v.mean()-t.ppf(.975,m-1)*se),float(v.mean()+t.ppf(.975,m-1)*se)],
      sd_95CI_normal_assumption=[float(sd*np.sqrt((m-1)/chi2.ppf(.975,m-1))),float(sd*np.sqrt((m-1)/chi2.ppf(.025,m-1)))])
def row_at(record,z):return next(r for r in record['rows'] if r['z']==z)
def main():
    ensemble=read(RUN/'ensemble_summary.json')['records'];refine=read(RUN/'refinement_summary.json')['records']
    final_records=read(RUN/'final_resolution.json')['records'] if (RUN/'final_resolution.json').exists() else []
    required=['nonlinear_ensemble.json','final_resolution.json'];missing=[f for f in required if not (RUN/f).exists() or not read(RUN/f).get('complete',False)]
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',run_id=RUN.name,complete=not missing,missing_production_files=missing,freeze_commit='9db4bb6a67b640d79365810a984c3af5c6a9da92',ensembles=[],resolution=[])
    groups=[('weak-disorder', [r for r in refine if r['sigma']==.3 and r['dt']==.0025]),
      ('weak-launch', [r for r in ensemble if r['E']==.3 and r['sigma']==.3 and r['disorder']==7601]),
      ('held-out-E.45',[r for r in ensemble if r['E']==.45])]
    groups += [(f'sigma{s}-fine',[r for r in refine if r['sigma']==s and r['dt']==.0025]) for s in [1,2,3]]
    for name,records in groups:
      for z in [5,10,20,50]:
        rows=[row_at(r,z) for r in records];v=10*np.log10([r['lambda_own'] for r in rows]);f0=np.array([r['f0'] for r in rows]);approx=10*np.log10([r['own_approx']/r['lambda_own'] for r in rows])
        out['ensembles'].append(dict(name=name,z=z,**statistics(v),f0_mean=float(f0.mean()),f0_min=float(f0.min()),f0_max=float(f0.max()),max_approximation_error_dB=float(max(abs(approx))),dt=records[0]['dt']))
    for s in [.3,1,2,3]:
      for z in [10,20,50]:
       for coarse,fine in [(.02,.01),(.01,.005),(.005,.0025)]:
        a={r['disorder']:10*np.log10(row_at(r,z)['lambda_own']) for r in refine if r['sigma']==s and r['dt']==coarse}
        b={r['disorder']:10*np.log10(row_at(r,z)['lambda_own']) for r in refine if r['sigma']==s and r['dt']==fine};delta=np.array([b[d]-a[d] for d in sorted(a)])
        out['resolution'].append(dict(sigma=s,z=z,coarse=coarse,fine=fine,paired_mean_difference_dB=float(delta.mean()),max_individual_difference_dB=float(max(abs(delta))),mean_gate=bool(abs(delta.mean())<.3),individual_gate=bool(max(abs(delta))<1)))
    allrows=[r for c in ensemble+refine+final_records for r in c['rows'] if r['z']>=5];errors=[];ratios=[]
    for r in allrows:
      V=np.array(r['own']);low=r['lambda_own'];high=np.trace(V)-low;errors.append(abs((r['own_approx']/low-1)-(V[0,0]-low)/V[1,1]));ratios.append(V[0,0]/V[1,1])
    out['algebra']=dict(max_identity_residual=float(max(errors)),max_approximation_error_dB=float(max(abs(10*np.log10(r['own_approx']/r['lambda_own'])) for r in allrows)),max_VX_over_VP=float(max(ratios)),states=len(allrows))
    sc=read(RUN/'scaling_summary.json')['rows'];out['curvature_scaling']=[]
    for z in [5,10,20]:
      powers=[];coeff=[];held=[];rat=[]
      for b in range(4):
        train=[r for r in sc if r['batch']==b and r['z']==z and not r['held_out']];n=np.array([r['n'] for r in train]);y=np.array([r['own_excess'] for r in train]);p=np.polyfit(np.log(n),np.log(y),1);powers.append(p[0]);coeff.append(np.mean(n*y))
        held.extend(abs(r['own_excess']/np.exp(np.polyval(p,np.log(r['n'])))-1) for r in sc if r['batch']==b and r['z']==z and r['held_out'])
        rat.extend(r['own_excess']/r['curvature_prediction'] for r in train)
      out['curvature_scaling'].append(dict(z=z,power_mean=float(np.mean(powers)),power_SE=float(np.std(powers,ddof=1)/2),coefficient_mean=float(np.mean(coeff)),coefficient_SE=float(np.std(coeff,ddof=1)/2),max_held_out_relative_error=float(max(held)),mean_sagitta_ratio=float(np.mean(rat)),passed=bool(abs(np.mean(powers)+1)<.1 and max(held)<.1)))
    out['SPM_reference']=[]
    for s in [.3,3]:
      for z in [5,10,20,50]:
        rr=[r for r in read(RUN/'spm_reference.json')['rows'] if r['sigma']==s and r['z']==z and r['sample']==.1];vv=[r['SPM_reference_fraction'] for r in rr]
        out['SPM_reference'].append(dict(sigma=s,z=z,mean=float(np.mean(vv)),min=float(min(vv)),max=float(max(vv)),interpretation='Reference ratio, not an additive causal fraction of phase variance'))
    out['SPM_exact_reference_diagnostic']=[]
    for r in read(RUN/'spm_reference.json')['rows']:
      if r['sample']!=.1:continue
      n0=1e10*r['f0'];Phi=r['Phi_self'];exact=moments(n0,1,Phi)['lambda'];linear=(np.sqrt(1+Phi*Phi)+Phi)**-2
      out['SPM_exact_reference_diagnostic'].append(dict(sigma=r['sigma'],disorder=r['disorder'],z=r['z'],n0=n0,Phi=Phi,linear=linear,exact=exact,
        difference_dB=float(10*np.log10(exact/linear)),note='Derived oracle diagnostic at measured f0 and integrated self phase, not a separate physical trajectory'))
    out['diagonal_mechanism']=read(RUN/'diagonal_mechanism.json')['rows']
    out['extracted_stage']=read(RUN/'extracted_stage.json')['rows']
    out['loss']=[]
    for p in sorted(GRIN.glob('K*.json')):
      d=read(p)
      if not d.get('alpha',0):continue
      for z in [10,20,50]:
        rr=[next(r for r in b if r['z']==z) for b in d['records']];vv=np.array([r['lambda_own'] for r in rr]);det=.1+.9*vv
        out['loss'].append(dict(file=p.name,disorder=d['disorder'],dt=d['dt'],z=z,alpha=d['alpha'],transmission=float(np.exp(-d['alpha']*z)),lambda_mean=float(vv.mean()),lambda_SE=float(vv.std(ddof=1)/2),detector_efficiency=.9,detected_mean=float(det.mean()),detected_dB=float(10*np.log10(det.mean()))))
    out['nonlinear_ensembles']=[]
    if (RUN/'nonlinear_ensemble.json').exists():
      manifest=read(RUN/'nonlinear_ensemble.json')
      for E,sigma,held in [(.3,.3,False),(.3,3,False),(.45,.3,True)]:
        rr=[r for r in manifest['records'] if r['E']==E and r['sigma']==sigma]
        for z in [5,10,20]:
          vals=[];pred=[];formula=[];sampling=[];err=[];fractions=[];curvature=[]
          for r in rr:
            d=read(GRIN/r['file']);rows=[next(x for x in b if x['z']==z) for b in d['records']];v=np.array([x['lambda_own'] for x in rows]);lin=rows[0]['linear_own'];vals.append(10*np.log10(v.mean()));pred.append(10*np.log10(lin));err.append(vals[-1]-pred[-1]);sampling.append(10/np.log(10)*v.std(ddof=1)/2/v.mean())
            tag=d['tag'].split('_n')[0];tr=read(Path('~/analytical-nl-discovery-data')/GRIN.name/(tag+'_tangent.json'))
            state=row_at(tr,z)
            formula.append(10*np.log10(state['own_approx']))
            fractions.append(state['f0']);curvature.append(rows[0]['own_ratio'])
          if len(vals)<2:continue
          out['nonlinear_ensembles'].append(dict(E=E,sigma=sigma,held_out=held,z=z,**statistics(vals),tangent_mean_dB=float(np.mean(pred)),formula_mean_dB=float(np.mean(formula)),mean_difference_dB=float(np.mean(err)),max_individual_difference_dB=float(max(abs(np.array(err)))),max_sampling_SE_dB=float(max(sampling)),passed=bool(abs(np.mean(err))<.5 and max(abs(np.array(err)))<1),
            f0_range=[float(min(fractions)),float(max(fractions))],outside_original_f0_bounds=sum(f<.6 or f>.87 for f in fractions),max_own_curvature_ratio=float(max(curvature))))
    out['original_ensemble_predictions']=[]
    for label,records,zs in [('E.45',[r for r in ensemble if r['E']==.45],[10,20]),
                            ('sigma2',[r for r in refine if r['sigma']==2 and r['dt']==.0025 and r['disorder']<=7606],[20,50])]:
      for z in zs:
        if label=='sigma2' and z==20:
          latest=[r for r in final_records if r['sigma']==2 and r['dt']==.000625 and r['disorder']<=7606]
          if len(latest)==6:records=latest
        if label=='sigma2' and z==50:
          records=[r for r in refine if r['sigma']==2 and r['dt']==.0025 and r['disorder']<=7606]
        vv=10*np.log10([row_at(r,z)['lambda_own'] for r in records]);mean=float(vv.mean());sd=float(vv.std(ddof=1))
        out['original_ensemble_predictions'].append(dict(case=label,z=z,members=len(vv),dt=records[0]['dt'],mean_dB=mean,sd_dB=sd,
          mean_pass=bool(-11<=mean<=-6),spread_pass=bool(sd>=1.5 if label=='E.45' else sd<=1.5),
          note='sigma2 continuum resolution is unresolved; this scores the literal finite-sample prediction.'))
    out['nonlinear_ensemble_convergence']=[]
    if (RUN/'nonlinear_ensemble.json').exists():
      manifest=read(RUN/'nonlinear_ensemble.json')
      for f in manifest.get('convergence_files',[]):
        d=read(GRIN/f);base=next(r for r in manifest['records'] if r['E']==d['E'] and r['sigma']==d['sigma'] and r['disorder']==d['disorder'])
        b=read(GRIN/base['file'])
        for z in [5,10,20]:
          vals=np.array([next(x for x in block if x['z']==z)['lambda_own'] for block in d['records']]);vv=np.array([next(x for x in block if x['z']==z)['lambda_own'] for block in b['records']])
          out['nonlinear_ensemble_convergence'].append(dict(file=f,reference=base['file'],z=z,change_dB=float(10*np.log10(vals.mean()/vv.mean())),
            refined_dt=d['dt'],reference_dt=b['dt'],shots=d['shots'],reference_shots=b['shots']))
    out['loss_ensemble']=[]
    for z in [10,20,50]:
      rr=[r for r in out['loss'] if r['z']==z and r['dt']==.02]
      if rr:out['loss_ensemble'].append(dict(z=z,**statistics([r['detected_dB'] for r in rr])))
    out['final_resolution']=[];out['final_resolution_nonlinear']=[]
    if (RUN/'final_resolution.json').exists():
      final=read(RUN/'final_resolution.json')
      for sigma in [2,3]:
       for z in [10,20]:
        for coarse,fine in [(.0025,.00125),(.00125,.000625)]:
          rr=refine+final['records'];a={r['disorder']:row_at(r,z) for r in rr if r['sigma']==sigma and r['dt']==coarse};b={r['disorder']:row_at(r,z) for r in rr if r['sigma']==sigma and r['dt']==fine}
          if not a or set(a)!=set(b):continue
          delta=np.array([10*np.log10(b[d]['lambda_own']/a[d]['lambda_own']) for d in sorted(a)])
          out['final_resolution'].append(dict(sigma=sigma,z=z,coarse=coarse,fine=fine,paired_mean_difference_dB=float(delta.mean()),max_individual_difference_dB=float(max(abs(delta))),
            mean_gate=bool(abs(delta.mean())<.3),individual_gate=bool(max(abs(delta))<1),
            fine_ensemble=statistics([10*np.log10(b[d]['lambda_own']) for d in sorted(a)])))
      for f in final.get('nonlinear_files',[]):
        d=read(GRIN/f)
        for z in [10,20]:
          rr=[next(r for r in block if r['z']==z) for block in d['records']];vv=np.array([r['lambda_own'] for r in rr]);lin=rr[0]['linear_own']
          out['final_resolution_nonlinear'].append(dict(file=f,z=z,dt=d['dt'],twa_dB=float(10*np.log10(vv.mean())),linear_dB=float(10*np.log10(lin)),
            error_dB=float(10*np.log10(vv.mean()/lin)),sampling_SE_dB=float(10/np.log(10)*vv.std(ddof=1)/2/vv.mean())))
    out['weak_signoff_domain']=[]
    for z in [10,20]:
      rr=[row_at(r,z) for r in refine if r['sigma']==.3 and r['dt']==.0025]
      inside=[r for r in rr if .6<=r['f0']<=.87 and r['own'][1][1]**2/(8e10*r['f0']*r['lambda_own'])<=.1]
      out['weak_signoff_domain'].append(dict(z=z,inside_original_bounds=len(inside),outside=len(rr)-len(inside),
        mean_and_SD_dB=statistics([10*np.log10(r['lambda_own']) for r in inside]),
        max_curvature_ratio=float(max(r['own'][1][1]**2/(8e10*r['f0']*r['lambda_own']) for r in rr))))
    out['component_files']=[p.name for p in sorted(RUN.glob('*.json')) if p.name!='summary.json']
    (RUN/'summary.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if not out['nonlinear_ensembles']:return
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
    # The summary plot shows the signed-off weak-disorder regime. Strong-noise
    # pathwise agreement is recorded above, but is not a continuum certificate.
    for E,sigma,col,offset,held in [(.3,.3,'#3366aa',-.15,False),(.45,.3,'#23875b',.15,True)]:
      rr=[r for r in out['nonlinear_ensembles'] if r['E']==E and r['sigma']==sigma];z=np.array([r['z'] for r in rr]);mean=np.array([r['mean'] for r in rr]);sd=np.array([r['sd'] for r in rr]);line=[r['formula_mean_dB'] for r in rr]
      ax.plot(z,line,color=col,lw=1.4);ax.errorbar(z+offset,mean,yerr=sd,fmt='o',color=col,mfc='white' if held else col,ms=5,capsize=3,label=fr"$E'={E},\ \sigma={sigma}$"+(' held out' if held else ''))
    ax.plot([],[],color='0.2',label=r'Same-path $\det V/V_P$ prediction');ax.set(xlabel=r'Propagation distance $z/L_{NL}$',ylabel='Condensate minimum variance (dB / vacuum)',xticks=[5,10,20],title=r'$n=10^{10}$; six disorder paths per ensemble');ax.legend(fontsize=8,frameon=False);ax.grid(alpha=.15)
    fig.savefig(RUN/'fig_summary.png',dpi=100,metadata={'Author':'gpt-b / gpt-6-astra / gpt'});plt.close(fig)
if __name__=='__main__':main()
