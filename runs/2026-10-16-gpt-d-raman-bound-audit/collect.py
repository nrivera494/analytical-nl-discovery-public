"""Collate independently produced evidence, gpt-d/gpt-6-astra/gpt."""
from propagate import *
import tomli
base=Path(__file__).parent;out={**IDENTITY,'runs':{},'exponents':{}}
for slug in ['c02-adjoint','c02-julia-core']:
 rid='2026-10-16-gpt-d-'+slug;rd=ROOT/'runs'/rid;raw=RAW/rid;p=raw/'metrics.toml'
 if not p.exists():continue
 m=tomli.loads(p.read_text());m['run_id']=rid;dump(rd/'summary.json',m)
 (rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-02\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {m["wall_s"]}\nraw_location: {raw}\n')
for p in sorted((ROOT/'runs').glob('2026-10-16-gpt-d-c02-*/summary.json')):
 d=json.loads(p.read_text());rid=p.parent.name
 if 'statistics' in d:out['runs'][rid]=d['statistics']
 if 'mask-' in rid:
  E=d['records'][0]['E_pJ'];L=d['records'][-1]['z'];out['runs'][rid]['integrated_loss_ratio']=(1-d['records'][-1]['E_pJ']/E)/(d['statistics']['kappa_pJinv_minv']*E*L)
for subset in [[10,20,40,80],[40,80,160]]:
 vals=[]
 for r in subset:
  d=json.loads((ROOT/'runs'/('2026-10-16-gpt-d-c02-rate'+str(r))/'summary.json').read_text());vals.append(d['records'][0]['rate_over_bound'])
 out['exponents']['GNLSE_initial_RHS_'+str(subset[0])+'_'+str(subset[-1])]=-float(np.polyfit(np.log(subset),np.log(vals),1)[0])
for stem in ['core','heldout6']:
 a=out['runs']['2026-10-16-gpt-d-c02-'+stem];b=out['runs']['2026-10-16-gpt-d-c02-'+stem+'-step']
 for key in ['max_photon_drift','rhs_relative_integrated_mismatch']:
  out['exponents'][stem+'_'+key+'_two_step_slope']=float(np.log(a[key]/b[key])/np.log(2))
dump(base/'summary.json',out)
print(json.dumps({'exponents':out['exponents'],'mask_validation':{k:v['integrated_loss_ratio'] for k,v in out['runs'].items() if 'mask-' in k}},indent=2))
