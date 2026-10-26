"""Continuous cutoff integration of the stored fields. gpt-d/gpt-6-astra/gpt.
CZT evaluates the finite-window Fourier transform without a large dense matrix
or a larger time grid. This separates cutoff-bin error from propagation error.
"""
from independent import *
base=Path(__file__).parent;rows=[]
for slug in ['mask-validation','mask-validation-wide']:
 rid='2026-10-16-gpt-d-'+slug;r=json.loads((ROOT/'runs'/rid/'summary.json').read_text())
 for case in r['cases']:
  ar=np.load(RAW/rid/f"fields_{case['label']}_{case['shaped']}.npz");Q=ar['Qfinal'];Q0=ar['Q0'];w=ar['omega'];n=len(Q);dt=case['dt'];wr=w[0];A=fft(Q);wc=float(omega(2.001));lo=wc-80
  iw=np.where(w>0,1/(HBAR*np.maximum(w,1.)),0.);N0=dt*n*np.sum(abs(Q0)**2*iw)/case['input_photon_fraction']
  vals=[]
  for m in [4097,8193]:
   ww=np.linspace(lo,wc,m);dw=ww[1]-ww[0];F=signal.czt(A,m=m,w=np.exp(1j*dw*dt),a=np.exp(-1j*(lo-wr)*dt))*dt
   vals.append(float(integrate.simpson(abs(F)**2/(HBAR*ww),x=ww)/(2*np.pi*N0)))
  d=2*np.pi/(n*dt);first=-10*d;F=signal.czt(A,m=21,w=np.exp(1j*d*dt),a=np.exp(-1j*first*dt))*dt
  ref=Q[np.arange(-10,11)%n]*n*dt
  row={'run_id':rid,'label':case['label'],'shaped':case['shaped'],'eta_CZT':vals[-1],'quadrature_difference':vals[-1]-vals[0],'CZT_relative_check':float(np.linalg.norm(F-ref)/np.linalg.norm(ref)),'discrete_photons_below_integration_band':float(dt*n*np.sum((abs(Q)**2*iw)[w<lo])/N0)};rows.append(row)
dump(base/'mask_continuous_summary.json',{**IDENTITY,'method':'finite-window continuous Fourier transform using CZT; no propagation refinement inferred','cases':rows});print(json.dumps(rows,indent=2))
