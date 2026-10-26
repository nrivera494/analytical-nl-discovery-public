"""Direct dispersionless signed momentum check; gpt-a, gpt-6-astra, gpt."""
import json,time
from pathlib import Path
import numpy as np
out=dict(provenance=dict(agent='gpt-a',model='gpt-6-astra',family='gpt'),rows=[])
for shape in ('gaussian','quartic','sech'):
 for phi in (1.,5.,10.):
  start=time.time();nt=2048;window=32.;dt=window/nt;t=(np.arange(nt)-nt//2)*dt;w=2*np.pi*np.fft.fftfreq(nt,dt)
  e={'gaussian':lambda:np.exp(-t*t/2),'quartic':lambda:np.exp(-t**4/2),'sech':lambda:1/np.cosh(t)}[shape]()
  phase=phi*e*e;rot=np.exp(1j*phase);u=e*rot;alpha=np.fft.fft(u,norm='ortho');alpha0=np.fft.fft(e,norm='ortho')
  q=np.fft.ifft(w*alpha,norm='ortho');a=rot*(1+1j*phase);b=rot*1j*phi*e*e
  back=a.conj()*q+b*q.conj();shot=np.sum(w*w*abs(alpha)**2);F=np.sum(abs(back)**2)/shot
  pp=np.fft.ifft(1j*w*np.fft.fft(e*e)).real;ep=np.fft.ifft(1j*w*np.fft.fft(e)).real
  I1=np.sum(ep*ep);I2=np.sum(e*e*pp*pp);formula=I1/(I1+phi*phi*I2)
  out['rows'].append(dict(shape=shape,Phi=phi,nt=nt,window=window,physical_weight='omega, signed post-detection weighting',F_momentum=float(F),bandwidth_ratio=float(np.sum(w*w*abs(alpha0)**2)/shot),formula=float(formula),relative_error=float(F/formula-1),wall_seconds=time.time()-start))
Path(__file__).with_name('momentum.json').write_text(json.dumps(out,indent=2)+'\n')
print('Maximum relative error:',max(abs(r['relative_error']) for r in out['rows']))
