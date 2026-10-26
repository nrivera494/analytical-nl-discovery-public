"""Freeze actual-GNLSE RHS scaling and a second-solver core check."""
from propagate import *
f=Fibre('S28',loss_scale=0.)
for r in [10,20,40,80,160]:
 rid='2026-10-16-gpt-d-c02-rate'+str(r);rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True)
 cfg={'run_id':rid,'identity':IDENTITY,'fibre':{'material':'S28','loss_scale':0.,'dispersion':'quadratic'},'grid':{'n':16384,'dt':.003},'input':{'shape':'sech','E_pJ':100.},'propagation':{'T':f.t1*r,'L':.0001,'h':.00001,'save_every':.0001},'expected':{'long_pulse_exponent':3,'card_exponent':2,'fit_domain_T_over_tau1':[40,160],'source':'Independent derivation frozen in protocol.md before quadrature'}}
 dump(rd/'config.yaml',cfg)
# Matched Python grid and pulse; Julia adds its documented fixed blue window.
rid='2026-10-16-gpt-d-c02-julia-core';rd=ROOT/'runs'/rid;rd.mkdir(exist_ok=True);raw=RAW/rid;raw.mkdir(exist_ok=True)
src=json.loads((ROOT/'runs/2026-10-16-gpt-d-c02-core/config.yaml').read_text());s=BoundSolver(f,**src['grid']);T=src['propagation']['T'];P,_=f.launch(T,3)
A=np.sqrt(P)*sech(s.t/T)*np.exp(-1j*(f.w0-s.wref)*s.t)
ww=np.clip(s.w,omega(4.4),omega(.46));al=np.where(s.valid,0.,1e6)
np.savez(raw/'inputs.npz',A=A,Om=np.fft.fftshift(s.Om),beta=np.fft.fftshift(f.b(ww)),alpha=np.fft.fftshift(al),omega0=s.wref,Aeff=f.A0*1e-12,n2=f.n2,dt=s.dt,window=s.n*s.dt,fR=f.fR,t1=f.t1,t2=f.t2,L=1.,h=.000125,T=T,kappa=s.kappa,E0=2*P*T)
dump(rd/'config.yaml',{**src,'run_id':rid,'implementation':'../2026-10-16-gpt-d-raman-bound-audit/julia_core.jl','method':'RK4IP','precision':'float64','saveat_m':.01,'scope':'Actual agents solver with its fixed blue-edge prefactor window; compare its drift with independent ideal-model Python run.'})
