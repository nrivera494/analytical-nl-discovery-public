"""Interior and beyond-regime crossing checks frozen before GNLSE. gpt-d/gpt-6-astra/gpt."""
from independent import *
out={**IDENTITY,'cases':[]};T=.2;lc=2.001;wc=float(omega(lc));f=Fibre('S28',launch_um=2.,dispersion='quadratic',edge_B=48.,edge_ref_um=2.)
_,N0=f.launch(T);ic=integrate.quad(lambda w:4*f.alpha(w)/(f.K(w)*N0**4),wc,f.w0)[0];alpha1=float(f.alpha(wc))
for qgoal in [.03,.2]:
 def vals(db):
  N=N0*(1-db*ic)**.25;Ts=float(f.width(wc,N));ep=db*alpha1/(f.K(wc)*N**4);a=np.pi*Ts/2
  return N,Ts,ep,a,ep/(2*a)
 db=optimize.brentq(lambda d:vals(d)[-1]-qgoal,1e-10,min(.999/ic,1.));f.edge_db=db
 N,Ts,ep,a,q=vals(db);delta=np.arctanh(1-ep/a)/a;term=terminal(f,N0);target=wc-delta
 r=reduced(f,T,1000,full=False,spectral_loss=False,nplanes=20001);true=assess_reduced(f,r,[lc])['optima'][str(lc)]
 Ls=float(np.interp(target,r['omega'][::-1],r['z'][::-1])) if target>term['omega_inf'] else None
 L=float(np.ceil(max(true['L_m']*1.5,(Ls*1.1 if Ls else 0))));fc={'material':'S28','launch_um':2.,'dispersion':'quadratic','edge_B':48.,'edge_ref_um':2.,'edge_db':db}
 rid=f'2026-10-16-gpt-d-cutoff-q{int(round(qgoal*100)):02d}';rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True)
 cfg={'run_id':rid,'identity':IDENTITY,'fibre':fc,'grid':{'n':16384,'dt':.003},'propagation':{'T':T,'L':L,'h':.04,'cutoffs':[lc],'save_every':1.}}
 dump(rd/'config.yaml',cfg);out['cases'].append({'run_id':rid,'q_at_cutoff':q,'closed_L_m':Ls,'closed_eta':N/N0*(1-q*(1+np.log(1/q))),'ODE_optimum':true,'terminal':term,'scope':'inside' if q<=.1 else 'outside crossing bound'})
dump(Path(__file__).parent/'crossing_predictions.json',out);print(json.dumps(out,indent=2))
