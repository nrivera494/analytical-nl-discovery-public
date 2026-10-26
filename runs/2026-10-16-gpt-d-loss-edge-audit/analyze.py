"""Summaries derived only from the auditor's runs; gpt-d/gpt-6-astra/gpt."""
from independent import *
base=Path(__file__).parent
def read(slug):return json.loads((ROOT/'runs'/('2026-10-16-gpt-d-'+slug)/'summary.json').read_text())
def at(run,z,key):return float(np.interp(z,[r['z'] for r in run['records']],[r[key] for r in run['records']]))
out={**IDENTITY,'core':{},'convergence':{},'path':{},'rates':[],'terminal':{}}
for slug in ['z75-main','z75-window','z75-wide','z75-heldout','z75-ownheldout','z75-variablearea','z75-sourced','z75-cubic','z75-lossless','z75-sampled','cutoff-edge','cutoff-edge200','cutoff-edge300']:
 try:r=read(slug)
 except FileNotFoundError:continue
 out['core'][slug]={'run_id':r['run_id'],'optima':r['optima'],'planes':[{'z':z,'N_ratio':at(r,z,'Ns_ratio'),'lambda_um':at(r,z,'soliton_lambda_um')} for z in [2,4,6,8] if z<=r['records'][-1]['z']],'total_photon_drift':r['records'][-1]['N_ratio']-1}
 for opt in r['optima'].values():
  opt['alpha_z0']=at(r,opt['L_m'],'alpha_z0');opt['loss_bandwidth_parameter']=at(r,opt['L_m'],'loss_bandwidth_parameter');opt['raman_longness']=at(r,opt['L_m'],'raman_longness')
for slug in ['z75-step','z75-grid','z75-window','z75-wide']:
 try:r=read(slug);ref=read('z75-main')
 except FileNotFoundError:continue
 out['convergence'][slug]={k:max(abs(at(r,z,k)-at(ref,z,k)) for z in [2,4,6,8]) for k in ['Ns_ratio','soliton_lambda_um']}
 out['convergence'][slug]['max_eta_difference']=max(abs(r['optima'][c]['eta']-ref['optima'][c]['eta']) for c in ['3.5','3.6','3.7'])
for mat,ls in [('z75',[3.62,3.65,3.70]),('s28',[2.01,2.02,2.04])]:
 vals=[]
 for width in [100,120]:
  try:r=read(f'{mat}-path{width}')
  except FileNotFoundError:continue
  f=Fibre(**r['config']['fibre']);N0=r['N0'];rr=r['records'];om=np.array([x['soliton_omega'] for x in rr]);ns=np.array([x['Ns'] for x in rr]);zz=np.array([x['z'] for x in rr])
  for lam in ls:
   w=float(omega(lam))
   if not min(om)<w<max(om):continue
   z=float(np.interp(w,om[::-1],zz[::-1]));N=float(np.interp(z,zz,ns))
   lam_norm=integrate.quad(lambda q:4*f.alpha(q)/(f.K(q)*N0**4),w,f.w0,epsabs=1e-8,epsrel=1e-6,limit=100)[0]
   vals.append({'run_id':r['run_id'],'T_fs':width,'lambda_um':lam,'z':z,'N_ratio':N/N0,'Gordon_N_ratio':(1-lam_norm)**.25 if lam_norm<1 else None,'lost_N4_scaled_1e44':(N0**4-N**4)*1e-44,'Lambda_scaled_1e44':lam_norm*N0**4*1e-44,'relative_invariant_residual':(1-(N/N0)**4)/lam_norm-1,'alpha_z0':at(r,z,'alpha_z0'),'loss_bandwidth_parameter':at(r,z,'loss_bandwidth_parameter'),'raman_longness':at(r,z,'raman_longness')})
 out['path'][mat]=vals
pred=json.loads((base/'followup_predictions.json').read_text())['rate_cases']
for p in pred:
 try:r=read(p['run_id'].replace('2026-10-16-gpt-d-',''))
 except FileNotFoundError:continue
 rec=r['records'];shift=rec[0]['omega']-rec[-1]['omega'];g=p['Gordon_shift'];rate=-rec[0]['raman_domega_dz']
 out['rates'].append({**p,'GNLSE_shift':shift,'relative_shift_error':(g-shift)/shift,'GNLSE_initial_rate':rate,'relative_initial_rate_error':(p['Gordon_initial_rate']-rate)/rate,'photon_drift':rec[-1]['N_ratio']-1})
for lo,hi in [(50,200),(200,500)]:
 a=[r for r in out['rates'] if lo<=r['T_fs']<=hi]
 if len(a)>2:out[f'exponent_{lo}_{hi}']={key:float(-np.polyfit(np.log([x['T_fs'] for x in a]),np.log([abs(x[key]) for x in a]),1)[0]) for key in ['relative_shift_error','relative_initial_rate_error']}
try:
 r=read('silica-terminal');tp=json.loads((base/'predictions.json').read_text())['cases']['silica_terminal']['terminal'];wi=tp['omega_inf'];we=tp['w_eff']
 rr=r['records'];out['terminal']={'prediction':tp,'planes':[{k:x[k] for k in ['z','N_ratio','Ns_ratio','omega','soliton_omega','alpha_z0','outside_isolation_fraction','filtering_domega_dz','raman_domega_dz']} for x in rr if x['z']%50==0]}
 for tag,cond in [('in_regime',lambda x:x['alpha_z0']<=.01),('late',lambda x:x['z']>=250),('quarter_region',lambda x:0<(x['omega']-wi)/we<.1 and x['alpha_z0']<=.01)]:
  a=[x for x in rr if x['omega']>wi and cond(x) and x['z']>0]
  if len(a)>2:out['terminal'][tag]={'exponent':float(np.polyfit(np.log([x['omega']-wi for x in a]),np.log([x['N_ratio'] for x in a]),1)[0]),'z_min':a[0]['z'],'z_max':a[-1]['z'],'n_points':len(a)}
except FileNotFoundError:pass
dump(base/'summary.json',out)
print(json.dumps({k:v for k,v in out.items() if k not in ['core','terminal']},default=float),flush=True)
