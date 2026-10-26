#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
from independent import *
import subprocess,sys

def safe_case(label,**kw):
    if (RAW/(label+'.json')).exists():
        print('EXISTS',label,flush=True);return json.loads((RAW/(label+'.json')).read_text())
    out=subprocess.check_output(['memory_pressure'],text=True)
    free=int(out.split('free percentage:')[1].split('%')[0])
    if free<35: raise RuntimeError(f'Insufficient free memory: {free}%')
    return run_case(label,**kw)

mode=sys.argv[1]
if mode=='robust':
    for T,m in [(100,'A2'),(200,'B')]:
        for model,kw in [('shock',dict(shock=True)),('tod',dict(d3=.12/(6*21.7*T*.001))),
                         ('loss',dict(loss=.2)),('smf',dict(curve=True,shock=True,loss=.2)),
                         ('published',dict(published=True,shock=True,loss=.2)),
                         ('published_gamma',dict(published=True,gamma_curve=True,loss=.2))]:
            for mask in ['TL',m]:safe_case(f'{model}_{T}_{mask}',N=4,T0=T,mask=mask,**kw)
        for r in [.9,1.1]:
            for mask in ['TL',m]:
                safe_case(f'detuneE_{int(T*r)}_{mask}',N=4*np.sqrt(r),T0=T*r,mask=mask,
                          Tref=T,zfactor=4*r**(-1.5))
elif mode=='converge':
    for T,m in [(100,'A2'),(200,'B')]:
        for mask in ['TL',m]:
            for z in [6,8]:
                safe_case(f'length{z}_{T}_{mask}',N=4,T0=T,mask=mask,zfactor=z,width=320,nt=32768)
            for h in [.5,.25,2.]:safe_case(f'step{h}_{T}_{mask}',N=4,T0=T,mask=mask,hfac=h)
            safe_case(f'grid_{T}_{mask}',N=4,T0=T,mask=mask,nt=32768)
            safe_case(f'window_{T}_{mask}',N=4,T0=T,mask=mask,nt=32768,width=320)
    # Integrable N=1 anchor and shooting convergence are independent known limits.
    t,u,d=propagate(N=1,T0=200,mask='TL',nt=4096,width=80,zfactor=1,hfac=.01,fR=0,
                    save=RAW/'integrable_N1.npz')
    exact=1/np.cosh(t)*np.exp(.5j*d['xi'])
    d['exact_field_relative_error']=float(np.linalg.norm(u-exact)/np.linalg.norm(exact))
    d.update(measure(t,u,d));(RAW/'integrable_N1.json').write_text(json.dumps(d,indent=2));print(d,flush=True)
elif mode=='tl_scan':
    for N,T in [(3,140),(4,200),(5,280)]:
        for r in [.8,.9,1.,1.1,1.2]:safe_case(f'tlscan_N{N}_T{int(T*r)}',N=N,T0=T*r,mask='TL',nt=32768 if T*r>307 else 16384)
else:raise ValueError(mode)
