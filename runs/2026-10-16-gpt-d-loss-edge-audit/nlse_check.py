"""Independent integrator check against the exact unperturbed soliton. gpt-d/gpt-6-astra/gpt."""
from independent import *
memory_ok();t0=time.monotonic();f=Fibre('S28',dispersion='quadratic',loss_scale=0.);f.fR=0.;T=.1
s=GNLSE(f,n=4096,dt=.003,shock=False);P,_=f.launch(T);L=2*T*T/abs(f.b2)
out,arr=s.run(T,L,L/2000,progress=False);q0=arr['Q0'];qf=arr['Qfinal'];phase=np.angle(np.vdot(q0,qf));err=np.linalg.norm(qf-q0*np.exp(1j*phase))/np.linalg.norm(q0)
rid='2026-10-16-gpt-d-nlse-limit';rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True);raw=RAW/rid;raw.mkdir(exist_ok=True)
dump(rd/'config.yaml',{**IDENTITY,'T_ps':T,'L_m':L,'n':4096,'dt_ps':.003,'steps':2000,'fR':0.,'shock':False,'loss':0.,'dispersion':'quadratic','script':'../2026-10-16-gpt-d-loss-edge-audit/nlse_check.py'})
summary={**IDENTITY,'run_id':rid,'relative_field_error':float(err),'global_phase':float(phase),'predicted_phase':float(f.g0*P*L/2),'energy_ratio':out['records'][-1]['E_pJ']/out['records'][0]['E_pJ'],'wall_s':time.monotonic()-t0}
dump(rd/'summary.json',summary);(rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-01\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {summary["wall_s"]}\nraw_location: {raw}\n')
print(json.dumps(summary))
