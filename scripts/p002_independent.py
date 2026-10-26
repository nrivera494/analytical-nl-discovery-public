#!/usr/bin/env python3
"""Independent fourth-order split-step capture check; no solver package imports.
agent: gpt-a; model: gpt-6-astra; family: gpt
"""
import json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.fft import fft, ifft, fftfreq

OUT=Path(sys.argv[1]); OUT.mkdir(parents=True,exist_ok=True)
Y1=1/(2-2**(1/3)); Y0=-2**(1/3)*Y1
def c0(d): return 1. if d==0 else (math.pi*d/(2*math.sinh(math.pi*d/2)))**2

def run(label,delta,r=None,window=640.,nt=8192,dz=.02,zmax=40.,b=1.,sigma=1.):
    t=(np.arange(nt)-nt//2)*window/nt;dt=window/nt
    f=1/np.cosh(np.minimum(np.abs(t),700))
    k=2*np.pi*fftfreq(nt,dt)
    if r is None:
        a=f[:,None].astype(complex);D=(-.5j*b*k*k-1j*delta*k)[:,None]
    else:
        assert b==1. and sigma==1., 'Vector control uses the original ideal coefficient matrix'
        a=f[:,None]*np.array([1.,np.sqrt(r)],dtype=complex)
        D=-.5j*k[:,None]**2-1j*k[:,None]*np.array([0.,delta])
    linear={q:np.exp(D*dz*q/2) for q in (Y1,Y0)}
    rows=[]; fields=[];start=time.time()
    def save(z):
        v=a[:,0] if r is None else a[:,1]/np.sqrt(r)
        nu=(np.sqrt(1+8*sigma/b)-1)/2
        psi=f**nu*np.exp(-1j*delta*t/b)
        psi/=np.sqrt(np.sum(abs(psi)**2)*dt)
        d=dict(zeta=z,capture_fixed_5=float(np.sum(abs(v[abs(t)<5])**2)*dt/2),
               capture_fixed_4=float(np.sum(abs(v[abs(t)<4])**2)*dt/2),
               capture_fixed_6=float(np.sum(abs(v[abs(t)<6])**2)*dt/2),
               bound_projection=float(abs(np.vdot(psi,v)*dt)**2/2),
               norm=float(np.sum(abs(v)**2)*dt/2),
               edge=float(np.sum(abs(a[abs(t)>.45*window])**2)/np.sum(abs(a)**2)))
        rows.append(d);fields.append(a.copy())
    save(0.)
    for step in range(1,round(zmax/dz)+1):
        for q in (Y1,Y0,Y1):
            a=ifft(fft(a,axis=0)*linear[q],axis=0)
            if r is None:
                a*=np.exp(1j*q*dz*sigma*f[:,None]**2)
            else:
                n=abs(a)**2;pot=np.column_stack([n[:,0]+n[:,1],n[:,0]+.5*n[:,1]])
                a*=np.exp(1j*q*dz*pot)
            a=ifft(fft(a,axis=0)*linear[q],axis=0)
        if step in {round(z/dz) for z in (10.,20.,30.,40.,80.)}:
            save(step*dz)
    d=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',label=label,delta=delta,r=r,b=b,sigma=sigma,
           window_tau=window,nt=nt,dzeta=dz,rows=rows,C0=c0(delta),elapsed_seconds=time.time()-start)
    (OUT/(label+'.json')).write_text(json.dumps(d,indent=2)+'\n')
    np.savez_compressed(OUT/(label+'.npz'),tau=t,fields=np.array(fields))
    print(label,rows[-1],f'{time.time()-start:.1f}s',flush=True)

if __name__=='__main__':
    material=json.loads(Path('runs/2026-10-04-gpt-a-material/summary.json').read_text())
    ds=[0.,.5,1.,1.5,2.,3.,material['delta_physical']]
    mode=sys.argv[2] if len(sys.argv)>2 else 'passive'
    if mode=='passive':
        for j,d in enumerate(ds,1):run(f'passive_d{j}',d)
    elif mode=='long':
        for j in (2,3,4,6,7):run(f'passive_long_d{j}',ds[j-1],window=1280.,nt=16384,zmax=80.)
    elif mode=='vector':
        for j,r,d in ((1,.01,1.),(2,.1,3.),(3,.01,ds[-1])):
            run(f'vector{j}',d,r,window=320.,nt=4096,zmax=20.)
    elif mode=='refine':
        for j,d in enumerate(ds,1):
            run(f'passive_refined_d{j}',d,window=320.,nt=4096,zmax=20.,dz=.005)
    elif mode=='physical':
        p=json.loads(Path('runs/2026-10-04-gpt-a-material/config_physical_prediction.json').read_text())
        run('passive_physical',p['delta'],b=p['b'],sigma=p['sigma'],window=640.,nt=8192,zmax=40.,dz=.005)
    else:raise ValueError(mode)
