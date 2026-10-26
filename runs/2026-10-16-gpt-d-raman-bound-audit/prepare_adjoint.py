"""Freeze a phase-only adjoint attack on the integrated rate bound."""
from propagate import *
import hashlib
rid='2026-10-16-gpt-d-c02-adjoint';rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True);raw=RAW/rid;raw.mkdir(exist_ok=True)
f=Fibre('S28',loss_scale=0.,dispersion='quadratic');n=4096;dt=.00025;T=.002;E=200.;L=.0005;h=.000005
s=BoundSolver(f,n=n,dt=dt,carrier_um=.4);valid=s.w>.1*s.wref;Q=ifft(sech(s.t/T))*valid;Q*=np.sqrt(E/(dt*n*np.sum(abs(Q)**2)));A=fft(Q)
al=np.where(valid,0.,1e6)
np.savez(raw/'inputs.npz',A=A,Om=np.fft.fftshift(s.Om),beta=np.zeros(n),alpha=np.fft.fftshift(al),omega0=s.wref,Aeff=f.A0*1e-12,n2=f.n2,dt=dt,window=n*dt,fR=f.fR,t1=f.t1,t2=f.t2,L=L,h=h,T=T,kappa=s.kappa,E0=E)
cfg={**IDENTITY,'run_id':rid,'claim':'C-20261016-claude-interactive.6-02','source_script':'../2026-10-16-gpt-d-raman-bound-audit/adjoint_bound.jl','n':n,'dt_ps':dt,'T_ps':T,'carrier_um':.4,'E0_pJ':E,'L_m':L,'dz_m':h,'adjoint_dz_m':h,'adjoint_mode':'discrete_rk4ip','precision':'float64','method':'RK4IP','optimizer':'LBFGS','max_iterations':12,'seeds':[101,305,707],'mask':'exp(i B phi); five spectral phase coefficients, unit magnitude','objective':'(E0-Eout)/(kappa E0^2 L)','expected_ceiling':1/(1+s.kappa*E*L),'scope':'Formal zero-dispersion constant-area model. Positive frequency carrier chosen to suppress near-zero spectral mass; not a calibrated ultraviolet fibre prediction. Absorber below 0.1 carrier must be negligible in independent validation.','raw_input_sha256':hashlib.sha256((raw/'inputs.npz').read_bytes()).hexdigest()}
dump(rd/'config.yaml',cfg)
