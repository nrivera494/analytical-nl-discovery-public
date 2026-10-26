"""Independent forward validation of the completed adjoint mask, gpt-d/gpt-6-astra/gpt."""
from independent import *
import tomli
memory_ok();t0=time.monotonic();rid=sys.argv[1] if len(sys.argv)>1 else '2026-10-16-gpt-d-mask-validation';rd=ROOT/'runs'/rid;raw=RAW/rid;raw.mkdir(exist_ok=True)
cfg=json.loads((rd/'config.yaml').read_text());search=tomli.loads((RAW/cfg['search_run']/'metrics.toml').read_text());v=np.array(search['best_coefficients']);fc=json.loads((ROOT/'runs'/'2026-10-16-gpt-d-cutoff-edge200'/'config.yaml').read_text())['fibre'];f=Fibre(**fc);T=.2;P,_=f.launch(T);rows=[]
for case in cfg['cases']:
 memory_ok();s=GNLSE(f,n=case['n'],dt=case['dt']);Q=ifft(np.sqrt(P)*sech(s.t/T));iw=np.where(s.valid,1/(HBAR*np.maximum(s.w,1.)),0.);Nbase=s.dt*s.n*np.sum(abs(Q)**2*iw)
 x=np.clip(s.Om*T,-5,5);B=np.column_stack([x*x/2,x**3/6,x**4/24,np.exp(-((x-1.5)/.8)**2),np.exp(-((x+1.5)/.8)**2)]);Cmask=np.column_stack([np.exp(-((x-q)/.8)**2) for q in [-2,-.7,.7,2]])
 mask=np.exp(1j*np.sum(B*v[:5],axis=1)-np.sum(Cmask*np.logaddexp(0,v[5:]),axis=1));dw=2*np.pi/(s.n*s.dt);filt=np.clip((omega(2.001)-s.w)/dw+.5,0,1)
 assert np.all(np.isfinite(mask)) and np.max(abs(mask))<=1+1e-14
 for shaped in [False,True]:
  q=Q*mask if shaped else Q
  out,arr=s.run(T,100.,case['h'],cutoffs=[2.001],Q0=q,save_every=10.,progress=False)
  eta=s.dt*s.n*np.sum(abs(arr['Qfinal'])**2*iw*filt)/Nbase;last=out['records'][-1]
  row={**case,'shaped':shaped,'eta_fractional_bin':float(eta),'eta_hard_bin':last['eta']['2.001']*out['N0']/Nbase,'input_photon_fraction':out['N0']/Nbase,'mask_max':float(abs(mask).max()),'final':last,'wall_s':out['wall_s']};rows.append(row);print(json.dumps({k:row[k] for k in ['label','shaped','eta_fractional_bin','eta_hard_bin','input_photon_fraction']}),flush=True)
  np.savez_compressed(raw/f"fields_{case['label']}_{shaped}.npz",**arr)
out={**IDENTITY,'run_id':rid,'search_run':cfg['search_run'],'best_coefficients':v,'cases':rows,'wall_s':time.monotonic()-t0};dump(rd/'summary.json',out)
(rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-01\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {out["wall_s"]}\nraw_location: {raw}\n')
