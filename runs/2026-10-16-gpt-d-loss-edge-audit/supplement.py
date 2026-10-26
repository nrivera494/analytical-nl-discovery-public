"""Post-run comparisons using only auditor evidence. gpt-d/gpt-6-astra/gpt."""
from independent import *
import tomli
base=Path(__file__).parent

def read(slug):return json.loads((ROOT/'runs'/('2026-10-16-gpt-d-'+slug)/'summary.json').read_text())
def at(r,z,k):return float(np.interp(z,[x['z'] for x in r['records']],[x[k] for x in r['records']]))
out={**IDENTITY,'fission':[],'shape':[],'second_solver':{},'chirp':{},'relaxations':{}}
p=json.loads((base/'fission_predictions.json').read_text());r=read('fission-daughter')
for v in p['predictions']:
 z=v['z'];n=at(r,z,'Ns')/p['formation_state']['N'];lam=at(r,z,'soliton_lambda_um')
 out['fission'].append({**v,'run_id':r['run_id'],'GNLSE_N_ratio_to_formation':n,'GNLSE_lambda_um':lam,'N_error':n-v['N_ratio_to_formation'],'lambda_error_um':lam-v['lambda_um'],'alpha_z0':at(r,z,'alpha_z0'),'sech_residual':at(r,z,'sech_intensity_residual')})
r=read('cutoff-edge200-shape')
for z in [98.,282.]:out['shape'].append({'run_id':r['run_id'],'z':z,**{k:at(r,z,k) for k in ['sech_intensity_residual','fundamental_width_ratio','alpha_z0','loss_bandwidth_parameter','outside_isolation_fraction']}})
for js,py,c in [('julia-cutoff-edge','cutoff-edge','2.002'),('julia-cutoff200','cutoff-edge200-shape','2.001'),('julia-z75-window','z75-window','3.6')]:
 try:j=read(js);r=read(py)
 except FileNotFoundError:continue
 rr=j['records'];mx=max(rr,key=lambda x:x['eta']);z=rr[-1]['z'];eta=float(np.interp(z,[x['z'] for x in r['records']],[x['eta'][c] for x in r['records']]))
 out['second_solver'][js]={'Julia_run_id':j['run_id'],'Python_run_id':r['run_id'],'Julia_optimum':mx,'final_z':z,'N_difference':rr[-1]['N_ratio']-at(r,z,'N_ratio'),'lambda_difference_um':rr[-1]['lambda_um']-at(r,z,'lambda_um'),'eta_difference':rr[-1]['eta']-eta}
for slug in ['chirp-silica','chirp-convergence']:
 try:r=read(slug)
 except FileNotFoundError:continue
 out['chirp'][slug]=[{'GDD_fs2':x['GDD_fs2'],'eta_1.85':x['final']['eta']['1.85'],'photon_drift':x['final']['N_ratio']-1,**{k:x[k] for k in ['label','dt','h','n'] if k in x}} for x in r['cases']]
for slug in ['z75-sourced','z75-cubic','z75-variablearea','z75-ownheldout-extended','z75-lossless','z75-sampled']:
 r=read(slug);out['relaxations'][slug]={'run_id':r['run_id'],'optima':r['optima'],'final':{k:r['records'][-1][k] for k in ['z','N_ratio','Ns_ratio','soliton_lambda_um','alpha_z0']}}
raw=RAW/'2026-10-16-gpt-d-window-probe';mp=raw/'metrics.toml'
if mp.exists():
 rid=raw.name;rd=ROOT/'runs'/rid;m=tomli.loads(mp.read_text());m['run_id']=rid;dump(rd/'summary.json',m)
 (rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-01\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {m["wall_s"]}\nraw_location: {raw}\n')
 out['window_probe']=m
out['source_n2_sensitivity']=json.loads((base/'followup_predictions.json').read_text())['n2_sensitivity']
dump(base/'supplement_summary.json',out)
print(json.dumps({k:v for k,v in out.items() if k in ['fission','shape','second_solver','chirp','window_probe']},indent=2))
# Explicit boundary and interior-crossing probes added after their frozen runs.
for name in ['boundary','crossing']:
 pp=base/(name+'_predictions.json')
 if not pp.exists():continue
 out[name]=[]
 for pred in json.loads(pp.read_text())['cases']:
  rid=pred['run_id']
  sp=ROOT/'runs'/rid/'summary.json'
  if not sp.exists():continue
  rr=json.loads(sp.read_text());last=rr['records'][-1]
  row={**pred,'GNLSE_optima':rr['optima'],'GNLSE_final':{k:last[k] for k in ['N_ratio','Ns_ratio','soliton_lambda_um','alpha_z0','sech_intensity_residual','fundamental_width_ratio']}}
  if name=='boundary':
   first=rr['records'][0];f=Fibre(**rr['config']['fibre']);row['measured_initial_spectral_loss_factor']=first['alpha_avg']/float(f.alpha(first['omega']))
  out[name].append(row)
dump(base/'supplement_summary.json',out)
