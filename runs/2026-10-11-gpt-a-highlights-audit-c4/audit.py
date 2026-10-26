"""Bounded alternate check, independent XPM tangent transpose.
gpt-a, gpt-6-astra, gpt. Physical filter vacuum is included.
"""
import json,time,gc
from pathlib import Path
import numpy as np
PROV=dict(agent='gpt-a',model='gpt-6-astra',family='gpt')
def run(p,C,z=2.,delta=None,nt=256,window=40.,step=.002,beta=None):
 start=time.time();p=np.array(p);C=np.array(C);nm=len(p);delta=np.zeros(nm) if delta is None else np.array(delta);beta=np.ones(nm) if beta is None else np.array(beta)
 t=(np.arange(nt)-nt//2)*window/nt;w=2*np.pi*np.fft.fftfreq(nt,window/nt);sigma=float(p@C@p)
 steps=max(int(np.ceil(z/step)),int(np.ceil(z*max(w*w)/2/.5)));h=z/steps
 lin=np.exp((-1j*w[:,None]**2*beta[None,:]/2-1j*w[:,None]*delta[None,:])*h/2)
 u=np.sqrt(p)[None,:]/np.sqrt(sigma)/np.cosh(t[:,None]);u=u.astype(complex);E0=float(np.sum(abs(u)**2));saved=[]
 def linear(v,adj=False):
  ll=lin.conj() if adj else lin
  return np.fft.ifft(ll.reshape(ll.shape+(1,)*(v.ndim-2))*np.fft.fft(v,axis=0),axis=0)
 for _ in range(steps):
  v=linear(u);saved.append(v);u=linear(v*np.exp(1j*h*(abs(v)**2@C.T)))
 f=np.fft.fft(u,axis=0,norm='ortho');bins=np.fft.fftfreq(nt)*nt
 T=np.column_stack([(abs(bins)<=k).astype(float) for k in range(1,15)]+[np.ones(nt),.6*(abs(bins)<=5),((bins>=-2)&(bins<=7)).astype(float)])
 q=np.fft.ifft(T[:,None,:]*f[:,:,None],axis=0,norm='ortho')
 for v in saved[::-1]:
  q=linear(q,True);rot=np.exp(1j*h*(abs(v)**2@C.T));qq=rot.conj()[:,:,None]*q
  mix=np.einsum('mn,tmf->tnf',C,np.imag(v.conj()[:,:,None]*qq),optimize=False)
  q=linear(qq+2*h*v[:,:,None]*mix,True)
 means=np.sum(T[:,None,:]*abs(f[:,:,None])**2,axis=(0,1));vac=np.sum((T*(1-T))[:,None,:]*abs(f[:,:,None])**2,axis=(0,1))
 factors=(np.sum(abs(q)**2,axis=(0,1))+vac)/means
 c=np.sqrt(p);r=delta*c-c*np.dot(c,delta*c);v=c*((C-np.ones_like(C))@p);qdef=v-c*np.dot(c,v)
 return dict(p=p.tolist(),C=C.tolist(),z=z,delta=delta.tolist(),beta=beta.tolist(),nt=nt,window=window,steps=steps,
  hard_band_F=factors[:14].tolist(),best_kmax=int(np.argmin(factors[:14])+1),best_F=float(min(factors[:14])),
  all_count_F=float(factors[14]),fractional_F=float(factors[15]),asymmetric_F=float(factors[16]),q_squared=float(qdef@qdef),r_squared=float(r@r),
  energy_error=float(np.sum(abs(u)**2)/E0-1),edge_energy=float(np.sum(abs(u[abs(t)>.4*window])**2)/E0),wall_seconds=time.time()-start)
if __name__=='__main__':
 out=dict(provenance=PROV,rows=[])
 cases=[dict(p=[1.],C=[[1.]]),dict(p=[.25,.75],C=[[1,1],[1,.5]]),dict(p=[.25,.75],C=np.ones((2,2))),
  dict(p=[1.],C=[[1.]],nt=512,step=.001),dict(p=[.25,.75],C=[[1,1],[1,.5]],nt=512,step=.001)]
 for e in [.02,.04,.08]:
  for sign in [-1,1]:cases.append(dict(p=[.7,.3],C=[[1,1],[1,1+sign*e]]))
 cases += [dict(p=[.25,.75],C=[[1,1],[1,.5]],delta=[0,.6]),dict(p=[.25,.75],C=[[1,1],[1,.5]],beta=[1,1.02])]
 for case in cases:
  row=run(**case);out['rows'].append(row);Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2));print(row['best_F'],row['q_squared'],row['wall_seconds'],flush=True);gc.collect()
