"""Independent GNLSE energy-budget implementation. gpt-d/gpt-6-astra/gpt."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'2026-10-16-gpt-d-loss-edge-audit'))
from independent import *

class BoundSolver(GNLSE):
 def __init__(self,f,**kw):
  super().__init__(f,**kw);self.integral_identity=0.;self.integral_rhs=0.
  self.pref=f.g0*f.fR/f.w0;self.hp=1/f.t1**2+1/f.t2**2;self.kappa=self.pref*self.hp/2
 def nl(self,Q):
  B=fft(self.s*Q);I=abs(B)**2;Fi=ifft(I)
  R=(1-self.f.fR)*I+self.f.fR*fft(self.H*Fi).real
  dq=1j*self.gamma_out*ifft(B*R)
  self.current_identity=-self.pref*self.dt*self.n*np.sum(self.Om*self.H.imag*abs(Fi)**2)
  self.current_rhs=2*self.dt*self.n*np.real(np.sum(np.conj(Q)*dq))
  return dq
 def step(self,Q,h):
  ep=np.exp(self.D*h/2);U=ep*Q
  k1=ep*self.nl(Q);r1=self.current_identity;e1=self.current_rhs
  k2=self.nl(U+h*k1/2);r2=self.current_identity;e2=self.current_rhs
  k3=self.nl(U+h*k2/2);r3=self.current_identity;e3=self.current_rhs
  k4=self.nl(ep*(U+h*k3));r4=self.current_identity;e4=self.current_rhs
  self.integral_identity+=h*(r1+2*r2+2*r3+r4)/6
  self.integral_rhs+=h*(e1+2*e2+2*e3+e4)/6
  return ep*(U+h*(k1+2*k2+2*k3)/6)+h*k4/6
 def measure(self,Q,N0,cutoffs,isolated=True):
  factor=self.dt*self.n;p=abs(Q)**2;iw=np.zeros(self.n);iw[self.valid]=1/(HBAR*self.w[self.valid]);E=factor*np.sum(p);N=factor*np.sum(p*iw);w=E/(HBAR*N);A=fft(Q);I=abs(A)**2;B=fft(self.s*Q);EB=self.dt*np.sum(abs(B)**2)
  dn=self.nl(Q);dN=2*factor*np.sum(np.real(np.conj(Q)*dn)*iw);dE=float(self.current_rhs);ident=float(self.current_identity);k=self.kappa
  shift=self.n//2-int(np.argmax(I));Ir=np.roll(I,shift);edge=Ir[abs(self.t)>.45*self.n*self.dt].sum()/I.sum()
  return {'E_pJ':float(E),'N':float(N),'N_ratio':float(N/N0),'omega':float(w),'lambda_um':float(wavelength(w)),'peak_W':float(I.max()),'dN_dz':float(dN),'dE_rhs':dE,'dE_identity':ident,'integral_identity':float(self.integral_identity),'integral_rhs':float(self.integral_rhs),'rate_over_bound':float(-dE/(k*E*E)) if k else 0.,'identity_rate_over_bound':float(-ident/(k*E*E)) if k else 0.,'weighted_rate_over_bound':float(-ident/(k*EB*EB)) if k else 0.,'weighted_energy_over_energy':float(EB/E),'identity_residual_over_bound':float((dE-ident)/(k*E*E)) if k else 0.,'time_edge_fraction':float(edge),'spectral_outer_fraction':float(p[abs(self.Om)>.8*np.pi/self.dt].sum()/p.sum()),'eta':{str(l):float(factor*np.sum((p*iw)[(self.w<omega(l))&self.valid])/N0) for l in cutoffs}}

def execute_bound(config_path):
 while True:
  try:memory_ok();break
  except SystemExit:time.sleep(15)
 cfg=json.loads(Path(config_path).read_text());rid=cfg['run_id'];rd=ROOT/'runs'/rid;raw=RAW/rid;raw.mkdir(exist_ok=True)
 f=Fibre(**cfg['fibre']);s=BoundSolver(f,**cfg['grid']);pr=cfg['propagation'];Q0=None
 if cfg.get('positive_frequency_model'):
  s.valid=s.w>cfg.get("omega_min_fraction",.1)*s.wref;s.s=np.ones(s.n);s.gamma_out=f.g0*(s.w/f.w0)*s.valid;s.D=np.zeros(s.n,dtype=complex);s.D[~s.valid]=-1e6
 if cfg.get('input'):
  inp=cfg['input'];T=pr['T'];tt=s.t;typ=inp['shape']
  if typ=='pair':A=np.exp(-.5*((tt-inp['gap_ps']/2)/T)**2)+np.exp(1j*inp['phase'])*np.exp(-.5*((tt+inp['gap_ps']/2)/T)**2)
  else:A=sech(tt/T)
  # Custom short-pulse inputs are centred on the grid carrier.
  Q0=ifft(A)*s.valid;Q0*=np.exp(.5j*inp.get('GDD_fs2',0)*1e-6*s.Om**2);Q0*=np.sqrt(inp['E_pJ']/(s.dt*s.n*np.sum(abs(Q0)**2)))
  if 'phase_coefficients' in inp:
   x=np.clip(s.Om*T,-5.,5.);v=inp['phase_coefficients'];basis=[x*x/2,x**3/6,x**4/24,np.exp(-((x-1.5)/.8)**2),np.exp(-((x+1.5)/.8)**2)]
   Q0*=np.exp(1j*sum(vv*bb for vv,bb in zip(v,basis)))
 out,arr=s.run(**pr,Q0=Q0,progress=False);rr=out['records'];E0=rr[0]['E_pJ'];k=s.kappa
 for r in rr:r['retention_bound']=1/(1+k*E0*r['z']);r['retention_ratio']=r['E_pJ']/E0;r['retention_margin']=r['retention_ratio']-r['retention_bound']
 idx=int(np.argmax([r['rate_over_bound'] for r in rr]));pk=np.array([r['peak_W'] for r in rr]);peaks,_=signal.find_peaks(pk,prominence=.03*pk.max())
 delta=rr[-1]['E_pJ']-E0
 stats={'kappa_pJinv_minv':k,'E0_pJ':E0,'E_L_over_E0':rr[-1]['retention_ratio'],'retention_bound_at_L':rr[-1]['retention_bound'],'min_retention_margin':min(r['retention_margin'] for r in rr),'max_rate_over_bound':rr[idx]['rate_over_bound'],'z_at_max_m':rr[idx]['z'],'first_compression_m':rr[int(peaks[0])]['z'] if len(peaks) else None,'max_abs_identity_residual_over_bound':max(abs(r['identity_residual_over_bound']) for r in rr),'identity_relative_integrated_mismatch':abs(delta-s.integral_identity)/max(abs(delta),1e-30),'rhs_relative_integrated_mismatch':abs(delta-s.integral_rhs)/max(abs(delta),1e-30),'max_photon_drift':max(abs(r['N_ratio']-1) for r in rr),'max_saved_energy_increase_pJ':max(np.diff([r['E_pJ'] for r in rr])),'max_time_edge_fraction':max(r['time_edge_fraction'] for r in rr),'max_spectral_outer_fraction':max(r['spectral_outer_fraction'] for r in rr),'max_weighted_rate_over_bound':max(r['weighted_rate_over_bound'] for r in rr)}
 out.update(IDENTITY);out.update({'run_id':rid,'config':cfg,'statistics':stats});dump(rd/'summary.json',out);np.savez_compressed(raw/'fields.npz',**arr)
 (rd/'meta.yaml').write_text(f'run_id: {rid}\nagent: gpt-d\nmodel: gpt-6-astra\nfamily: gpt\nclaim: C-20261016-claude-interactive.6-02\nsolver_commit: {SOLVER}\nsolver_dirty: false\nimplementation: Independent Python RK4IP with stage-wise identity integration\nhardware: {socket.gethostname()}\nwall_time_s: {out["wall_s"]}\nraw_location: {raw}\n')
 print(json.dumps({'run_id':rid,**stats}),flush=True)
if __name__=='__main__':
 for p in sys.argv[1:]:execute_bound(p)
