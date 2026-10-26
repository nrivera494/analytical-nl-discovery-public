"""Independent fine GDD scan of the proposer's stated shaping regime.
Post-audit supplementary test; gpt-d/gpt-6-astra/gpt. No proposer code is used.
"""
from independent import *
memory_ok();t0=time.monotonic();rid='2026-10-16-gpt-d-chirp-silica';rd=ROOT/'runs'/rid;raw=RAW/rid;raw.mkdir(exist_ok=True);cfg=json.loads((rd/'config.yaml').read_text())
f=Fibre('S28',loss_scale=0.);s=GNLSE(f,n=8192,dt=.003,carrier_um=1.75);T=.0567;P,_=f.launch(T,3)
Q=ifft(np.sqrt(P)*sech(s.t/T)*np.exp(-1j*(f.w0-s.wref)*s.t));rows=[]
for gdd in cfg['GDD_fs2']:
 memory_ok();q=Q*np.exp(.5j*gdd*1e-6*(s.w-f.w0)**2)
 out,arr=s.run(T,1.,.00025,order=3,cutoffs=[1.75,1.85],save_every=.05,Q0=q,progress=False)
 rows.append({'GDD_fs2':gdd,'final':out['records'][-1],'wall_s':out['wall_s']});print(json.dumps(rows[-1]),flush=True)
 np.savez_compressed(raw/f'fields_gdd{gdd}.npz',**arr)
summary={**IDENTITY,'run_id':rid,'cases':rows,'wall_s':time.monotonic()-t0,'proposer_metadata_read_after_report_commit':'08a7320; h4-shaping meta.yaml and summary.json only'}
dump(rd/'summary.json',summary);(rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-01 (supplementary shaping)\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {summary["wall_s"]}\nraw_location: {raw}\n')
