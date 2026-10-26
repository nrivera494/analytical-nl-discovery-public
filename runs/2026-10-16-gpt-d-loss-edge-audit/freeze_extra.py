"""Additional frozen tests chosen before propagation, gpt-d/gpt-6-astra/gpt."""
from independent import *
base=Path(__file__).parent
pred={**IDENTITY,'path':{},'cutoff':{}}
for mat,launch,T,L,h,edge in [('Z75',3.6,.10,30,.002,{}),('Z75',3.6,.12,45,.002,{}),('S28',2.,.10,250,.02,{'edge_B':92.,'edge_ref_um':2.,'edge_db':.004342944819}),('S28',2.,.12,350,.02,{'edge_B':92.,'edge_ref_um':2.,'edge_db':.004342944819})]:
 name=f'{mat.lower()}-path{int(T*1000)}'; fc={'material':mat,'launch_um':launch,**edge}; f=Fibre(**fc);r=reduced(f,T,L,full=False,spectral_loss=False)
 pred['path'][name]={'fibre':fc,'T_fs':T*1000,'gordon':assess_reduced(f,r,[launch+.02,launch+.05]),'terminal':terminal(f,r['N0'])}
 cfg={'run_id':'2026-10-16-gpt-d-'+name,'identity':IDENTITY,'fibre':fc,'grid':{'n':8192,'dt':.003},'propagation':{'T':T,'L':L,'h':h,'cutoffs':[launch+.02,launch+.05],'save_every':L/200}}
 rd=ROOT/'runs'/cfg['run_id'];rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
# Edge of the stated crossing regime. Select absorption so epsilon/(2a)=0.1 at lambda_c.
T=.1;lc=2.002;wc=float(omega(lc));fc={'material':'S28','launch_um':2.,'dispersion':'quadratic','edge_B':48.,'edge_ref_um':2.}
def atcut(db):
 f=Fibre(**fc,edge_db=db);_,N0=f.launch(T)
 lam=integrate.quad(lambda w:4*f.alpha(w)/(f.K(w)*N0**4),wc,f.w0)[0]
 if lam>=1:return 1e6
 N=N0*(1-lam)**.25;Ts=float(f.width(wc,N));v=float(f.K(wc))*N**4;eps=float(f.alpha(wc))/v;a=np.pi*Ts/2
 return eps/(2*a)
db=optimize.brentq(lambda d:atcut(d)-.1,1e-8,1.)
f=Fibre(**fc,edge_db=db);r=reduced(f,T,200,full=False,spectral_loss=False,nplanes=4001);N0=r['N0']
N=N0*(1-integrate.quad(lambda w:4*f.alpha(w)/(f.K(w)*N0**4),wc,f.w0)[0])**.25
Ts=float(f.width(wc,N));eps=float(f.alpha(wc)/(f.K(wc)*N**4));a=np.pi*Ts/2;delta=np.arctanh(1-eps/a)/a
cross=eps/(2*a)*(1+np.log(2*a/eps));eta=N/N0*(1-cross)
Lstar=float(np.interp(wc-delta,r['omega'][::-1],r['z'][::-1]));true=assess_reduced(f,r,[lc])
pred['cutoff']={'fibre':{**fc,'edge_db':db},'T_fs':100,'lambda_c':lc,'N_at_cutoff_ratio':N/N0,'crossing_parameter':eps/(2*a),'closed_eta':eta,'closed_L_m':Lstar,'delta_star':delta,'gordon_ODE_optimum':true,'alpha_z0_at_cutoff':float(f.alpha(wc)*np.pi*Ts**2/(2*abs(f.b2at(wc))))}
cfg={'run_id':'2026-10-16-gpt-d-cutoff-edge','identity':IDENTITY,'fibre':{**fc,'edge_db':db},'grid':{'n':8192,'dt':.003},'propagation':{'T':T,'L':200.,'h':.02,'cutoffs':[lc],'save_every':.5}}
rd=ROOT/'runs'/cfg['run_id'];rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
dump(base/'extra_predictions.json',pred);print(json.dumps(pred['cutoff'],default=float),flush=True)
