"""Long-pulse cutoff attacks; all predictions frozen before their GNLSE. gpt-d/gpt-6-astra/gpt."""
from independent import *
out={**IDENTITY,'cases':[]}
for T,lc in [(.2,2.001),(.3,2.+.002/3)]:
 wc=float(omega(lc));f=Fibre('S28',launch_um=2.,dispersion='quadratic',edge_B=48.,edge_ref_um=2.)
 _,N0=f.launch(T);ic=integrate.quad(lambda w:4*f.alpha(w)/(f.K(w)*N0**4),wc,f.w0)[0]
 alpha1=float(f.alpha(wc))
 def vals(db):
  N=N0*(1-db*ic)**.25;Ts=float(f.width(wc,N));eps=db*alpha1/(f.K(wc)*N**4);a=np.pi*Ts/2
  return N,Ts,eps,a,eps/(2*a)
 db=optimize.brentq(lambda d:vals(d)[-1]-.1,1e-10,min(.999/ic,1.))
 f.edge_db=db;N,Ts,eps,a,q=vals(db);delta=np.arctanh(1-eps/a)/a
 # Restore alpha1 semantics: vals uses alpha1 independently of mutable edge_db.
 L=100*(T/.1)**3;r=reduced(f,T,L,full=False,spectral_loss=False,nplanes=10001)
 target=wc-delta;Ls=float(np.interp(target,r['omega'][::-1],r['z'][::-1]));true=assess_reduced(f,r,[lc])['optima'][str(lc)]
 Nstar=float(np.interp(Ls,r['z'],r['N']));Tstar=float(f.width(target,Nstar))
 fc={'material':'S28','launch_um':2.,'dispersion':'quadratic','edge_B':48.,'edge_ref_um':2.,'edge_db':db}
 slug=f'cutoff-edge{int(T*1000)}';rid='2026-10-16-gpt-d-'+slug
 out['cases'].append({'run_id':rid,'fibre':fc,'T_fs':T*1000,'cutoff_um':lc,'q_at_cutoff':q,'closed_eta':N/N0*(1-q*(1+np.log(1/q))),'closed_L_m':Ls,'ODE_optimum':true,'alpha_z0_at_closed_L':float(f.alpha(target)*np.pi*Tstar*Tstar/(2*abs(f.b2at(target)))),'loss_bandwidth_at_closed_L':1/(f.wedge*Tstar)**2,'terminal':terminal(f,N0)})
 # Go beyond both predicted maxima, but avoid a pointless terminal tail.
 length=float(np.ceil(max(Ls,true['L_m'])*1.25))
 cfg={'run_id':rid,'identity':IDENTITY,'fibre':fc,'grid':{'n':8192,'dt':.003},'propagation':{'T':T,'L':length,'h':.02*(T/.1)**2,'cutoffs':[lc],'save_every':.5*(T/.1)**2}}
 rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
dump(Path(__file__).parent/'cutoff_long_predictions.json',out);print(json.dumps(out),flush=True)
