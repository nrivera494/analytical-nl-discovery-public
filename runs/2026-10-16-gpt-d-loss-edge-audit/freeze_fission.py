"""Conditional fission prediction after short prefix, before full trajectory; gpt-d/gpt-6-astra/gpt."""
from independent import *
base=Path(__file__).parent
p=json.loads((ROOT/'runs/2026-10-16-gpt-d-z75-fission-prefix/summary.json').read_text())
last=None;chosen=None
for row in p['records']:
 s=row['fission']['selected'];good=s and s['isolated'] and s['N_ratio']<.95 and len(row['fission']['candidates'])>=2
 if good and last is not None:
  chosen=row;break
 last=row if good else None
if chosen is None:raise RuntimeError('Frozen isolation criterion not met by prefix')
s=chosen['fission']['selected'];zs=chosen['z'];f=Fibre();r=reduced(f,.04,8-zs,order=2,initial=[s['omega'],s['N']],full=True,spectral_loss=True,nplanes=1001)
out={**IDENTITY,'prefix_run_id':p['run_id'],'formation_z':zs,'formation_state':s,'predictions':[]}
for z in [2,4,6,8]:
 out['predictions'].append({'z':z,'N_ratio_to_formation':float(np.interp(z-zs,r['z'],r['N'])/s['N']),'lambda_um':float(wavelength(np.interp(z-zs,r['z'],r['omega'])))})
rr=reduced(f,.04,18,full=True,spectral_loss=True,nplanes=721)
out['ownheldout_extended']=assess_reduced(f,rr,[3.3,3.4])
dump(base/'fission_predictions.json',out);print(json.dumps(out),flush=True)
