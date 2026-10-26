"""Freeze follow-up predictions, gpt-d/gpt-6-astra/gpt. No forward propagation."""
from independent import *
base=Path(__file__).parent
out={**IDENTITY,'cases':{},'rate_cases':[],'n2_sensitivity':[]}
for slug in ['z75-sourced','z75-cubic','z75-sampled','z75-lossless']:
 cfg=json.loads((ROOT/'runs'/('2026-10-16-gpt-d-'+slug)/'config.yaml').read_text())
 f=Fibre(**cfg['fibre']); p=cfg['propagation']
 r=reduced(f,p['T'],p['L'],full=True,spectral_loss=True,nplanes=321)
 out['cases'][slug]=assess_reduced(f,r,p['cutoffs'])
# Rate scaling at a fixed, small fraction of the dispersion length.
for Tfs in [30,50,80,120,200,300,500]:
 T=Tfs/1000;f=Fibre('S28',dispersion='quadratic',loss_scale=0.)
 L=.1*T*T/abs(f.b2);P,N0=f.launch(T); n=8192;dt=.0015 if Tfs<=50 else .003
 cfg={'run_id':f'2026-10-16-gpt-d-rate{Tfs}','identity':IDENTITY,'fibre':{'material':'S28','dispersion':'quadratic','loss_scale':0.},'grid':{'n':n,'dt':dt},'propagation':{'T':T,'L':L,'h':L/500,'cutoffs':[],'save_every':L/20}}
 rd=ROOT/'runs'/cfg['run_id'];rd.mkdir(exist_ok=True);dump(rd/'config.yaml',cfg)
 r=reduced(f,T,L,full=False,spectral_loss=False,nplanes=21)
 out['rate_cases'].append({'run_id':cfg['run_id'],'T_fs':Tfs,'L_m':L,'Gordon_initial_rate':float(f.K(f.w0)*N0**4),'full_initial_rate':float(-overlap_rate(f,f.w0,N0)),'Gordon_shift':float(f.w0-r['omega'][-1])})
# Sensitivity at fixed photon number differs from retuning a fundamental pulse.
f=Fibre();_,N0=f.launch(.020)
for scale in [.9,1.,1.1,5.4/2.1]:
 ff=Fibre(n2=2.1e-20*scale);_,Nr=ff.launch(.020)
 out['n2_sensitivity'].append({'n2_m2_W':ff.n2,'interpretation':'parameter sensitivity, not a calibration of this fibre','fixed_N0_KN4_ratio':float(ff.K(ff.w0)/f.K(f.w0)),'retuned_fundamental_N_ratio':Nr/N0,'retuned_initial_rate_ratio':float(ff.K(ff.w0)*Nr**4/(f.K(f.w0)*N0**4)),'fixed_N0_Gordon_terminal':terminal(ff,N0),'retuned_Gordon_terminal':terminal(ff,Nr)})
dump(base/'followup_predictions.json',out)
# Shared numerical arrays for an independent Julia API implementation.
for slug in ['cutoff-edge','z75-window']:
 cfg=json.loads((ROOT/'runs'/('2026-10-16-gpt-d-'+slug)/'config.yaml').read_text())
 f=Fibre(**cfg['fibre']);s=GNLSE(f,**cfg['grid']);p=cfg['propagation'];P,_=f.launch(p['T'])
 A=np.sqrt(P)*sech(s.t/p['T'])*np.exp(-1j*(f.w0-s.wref)*s.t)
 ww=np.clip(s.w,omega(7.8 if f.material=='Z75' else 4.4),omega(.66 if f.material=='Z75' else .46))
 al=np.minimum(f.alpha(ww),1e6);al[~s.valid]=1e6
 raw=RAW/('2026-10-16-gpt-d-julia-'+slug);raw.mkdir(exist_ok=True)
 np.savez(raw/'inputs.npz',A=A,Om=np.fft.fftshift(s.Om),beta=np.fft.fftshift(f.b(ww)),alpha=np.fft.fftshift(al),omega0=s.wref,Aeff=f.A0*1e-12,n2=f.n2,dt=s.dt,window=s.dt*s.n,fR=f.fR,t1=f.t1,t2=f.t2,lambda_launch=f.launch_um,cutoff=2.002 if slug=='cutoff-edge' else 3.6,L=20. if slug=='cutoff-edge' else 2.,h=.02 if slug=='cutoff-edge' else .00025)
print('Frozen source, dispersion, n2 and rate predictions; exported Julia inputs.',flush=True)
