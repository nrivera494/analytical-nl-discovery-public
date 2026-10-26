"""Explicit initial-boundary probes, frozen before propagation; gpt-d/gpt-6-astra/gpt."""
from independent import *
out={**IDENTITY,'cases':[]}
for label,band,ad in [('width-bound',.25,None),('width-beyond',.5,None),('adiab-bound',None,.01),('adiab-beyond',None,.03)]:
 f=Fibre('S28',launch_um=2.,dispersion='quadratic',edge_B=92. if band else 48.,edge_ref_um=2.,edge_db=.004342944819)
 T=1/(f.wedge*np.sqrt(band)) if band else .2
 if ad:f.edge_db=ad/(np.pi*T*T/(2*abs(f.b2)))/(np.log(10)/10)
 LD=T*T/abs(f.b2);L=100. if band else 20*LD;h=min(.01,LD/100);_,N0=f.launch(T)
 fc={'material':'S28','launch_um':2.,'dispersion':'quadratic','edge_B':f.edge_B,'edge_ref_um':2.,'edge_db':f.edge_db};rid='2026-10-16-gpt-d-'+label;rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True)
 cfg={'run_id':rid,'identity':IDENTITY,'fibre':fc,'grid':{'n':8192,'dt':.003},'propagation':{'T':T,'L':L,'h':h,'cutoffs':[2.02],'save_every':L/100}};dump(rd/'config.yaml',cfg)
 g=reduced(f,T,L,full=False,spectral_loss=False,nplanes=501);full=reduced(f,T,L,full=True,spectral_loss=True,nplanes=501);x=1/(f.wedge*T)
 out['cases'].append({'run_id':rid,'T_fs':T*1000,'initial_loss_width':x*x,'initial_alpha_z0':float(f.alpha(f.w0)*np.pi*T*T/(2*abs(f.b2))),'initial_spectral_loss_factor':x/np.sin(x),'Gordon_final_N_ratio':g['N'][-1]/g['N0'],'Gordon_final_lambda_um':float(wavelength(g['omega'][-1])),'full_response_final_N_ratio':full['N'][-1]/full['N0'],'full_response_final_lambda_um':float(wavelength(full['omega'][-1]))})
dump(Path(__file__).parent/'boundary_predictions.json',out);print(json.dumps(out,indent=2))
