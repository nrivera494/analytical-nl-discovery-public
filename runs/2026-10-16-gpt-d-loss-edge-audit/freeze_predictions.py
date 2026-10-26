"""agent=gpt-d, model=gpt-6-astra, family=gpt; predictions before GNLSE."""
from independent import *
pred={'identity':IDENTITY,'cases':{}}
for name,T,L,area in [('main',.020,8,'constant'),('heldout',.030,10,'constant'),('ownheldout',.040,12,'constant'),('variablearea',.020,8,'variable')]:
 f=Fibre(area=area); r=reduced(f,T,L,full=True,spectral_loss=True,nplanes=1+int(L/.025))
 pred['cases'][name]={'T_fs':T*1000,'L_m':L,'area':area,'properties':f.properties(),'prediction':assess_reduced(f,r,[3.3,3.4,3.5,3.6,3.7])}
 cfg={'run_id':'2026-10-16-gpt-d-z75-'+name,'identity':IDENTITY,'fibre':{'material':'Z75','area':area},'grid':{'n':8192,'dt':.003,'carrier_um':3.3},'propagation':{'T':T,'L':L,'h':.00025,'cutoffs':[3.3,3.4,3.5,3.6,3.7],'save_every':.025}}
 rd=ROOT/'runs'/cfg['run_id'];rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
 print(name,pred['cases'][name]['prediction'],flush=True)
f=Fibre('S28',launch_um=2.,dispersion='quadratic',edge_B=92.,edge_ref_um=2.,edge_db=.004342944819)
T=.1; P,N=f.launch(T); tr=terminal(f,N);r=reduced(f,T,1800,full=False,spectral_loss=False,nplanes=361)
pred['cases']['silica_terminal']={'properties':f.properties(),'T_fs':100,'L_m':1800,'terminal':tr,'planes':{'z':r['z'],'N_ratio':r['N']/N,'lambda_um':wavelength(r['omega']),'alpha_z0':f.alpha(r['omega'])*np.pi*r['Ts']**2/(2*np.abs(f.b2at(r['omega'])))}}
cfg={'run_id':'2026-10-16-gpt-d-silica-terminal','identity':IDENTITY,'fibre':{'material':'S28','launch_um':2.,'dispersion':'quadratic','edge_B':92.,'edge_ref_um':2.,'edge_db':.004342944819},'grid':{'n':8192,'dt':.003},'propagation':{'T':T,'L':1800.,'h':.01,'cutoffs':[2.01,2.02,2.04],'save_every':5.}}
rd=ROOT/'runs'/cfg['run_id'];rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
print('silica terminal',tr,'last',r['N'][-1]/N, 'adiabatic',pred['cases']['silica_terminal']['planes']['alpha_z0'][-1],flush=True)
dump(Path(__file__).parent/'predictions.json',pred)
