"""Prepare and record independent Julia runs, gpt-d/gpt-6-astra/gpt."""
from independent import *
import tomli as tomllib
import hashlib
base=Path(__file__).parent
for slug,source,L,h,n,dt,opt in [('julia-cutoff200','cutoff-edge200',282.,.04,16384,.003,False),('adjoint-cutoff200','cutoff-edge200',100.,.08,4096,.003,True)]:
 cfg=json.loads((ROOT/'runs'/('2026-10-16-gpt-d-'+source)/'config.yaml').read_text());f=Fibre(**cfg['fibre']);s=GNLSE(f,n=n,dt=dt)
 T=cfg['propagation']['T'];P,_=f.launch(T);A=np.sqrt(P)*sech(s.t/T);ww=np.clip(s.w,omega(4.4),omega(.46));al=np.minimum(f.alpha(ww),1e6);al[~s.valid]=1e6
 rid='2026-10-16-gpt-d-'+slug;raw=RAW/rid;raw.mkdir(exist_ok=True);rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True)
 np.savez(raw/'inputs.npz',A=A,Om=np.fft.fftshift(s.Om),beta=np.fft.fftshift(f.b(ww)),alpha=np.fft.fftshift(al),omega0=s.wref,Aeff=f.A0*1e-12,n2=f.n2,dt=dt,window=n*dt,fR=f.fR,t1=f.t1,t2=f.t2,cutoff=cfg['propagation']['cutoffs'][0],L=L,h=h,T=T)
 out={**cfg,'run_id':rid,'grid':{'n':n,'dt':dt},'L_m':L,'dz_m':h,'implementation':'adjoint_search.jl' if opt else 'julia_check.jl','precision':'float64','method':'RK4IP','raw_input_sha256':hashlib.sha256((raw/'inputs.npz').read_bytes()).hexdigest()}
 if opt:out.update({'adjoint_mode':'discrete_rk4ip','checkpoint_stride':32,'adjoint_dz_m':h,'optimizer':'LBFGS','max_iterations':12,'seeds':[101,203,307],'mask':'exp(i B phi - C softplus(a)); positive Gaussian attenuation, |m|<=1','scope':'relaxed shaped-input search; not a proof over all masks','objective':'cutoff photons / unmasked launch photons; fractional cutoff bin'})
 dump(rd/'config.yaml',out)
# Register the already completed API cross-check without inventing elapsed time.
for slug in ['julia-cutoff-edge','julia-z75-window','julia-cutoff200','adjoint-cutoff200','adjoint-cutoff200-retry','adjoint-cutoff200-complete']:
 rid='2026-10-16-gpt-d-'+slug;raw=RAW/rid;metrics=raw/'metrics.toml'
 if not metrics.exists():continue
 rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True);m=tomllib.loads(metrics.read_text());m['run_id']=rid;dump(rd/'summary.json',m)
 if not (rd/'config.yaml').exists():
  inp=np.load(raw/'inputs.npz');dump(rd/'config.yaml',{**IDENTITY,'run_id':rid,'input_data':str(raw/'inputs.npz'),'script':'../2026-10-16-gpt-d-loss-edge-audit/julia_check.jl','nt':len(inp['A']),'dt_ps':float(inp['dt']),'L_m':float(inp['L']),'dz_m':float(inp['h']),'method':'RK4IP','precision':'float64','source_config':'../2026-10-16-gpt-d-cutoff-edge/config.yaml' if slug=='julia-cutoff-edge' else '../2026-10-16-gpt-d-z75-window/config.yaml'})
 (rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-01\nsolver_commit: {SOLVER}\nsolver_dirty: false\nhardware: {socket.gethostname()}\nwall_time_s: {m["wall_s"]}\nraw_location: {raw}\n')
print('Prepared and registered Julia runs.',flush=True)
