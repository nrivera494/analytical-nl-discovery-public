"""gpt-e / gpt-6-astra / gpt: independent weak-dispersion audit."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import argparse,json,time
from pathlib import Path
import numpy as np
from tangent import Flow,kerr_anchor,unpack

HERE=Path(__file__).resolve().parent
RAW=Path('~/analytical-nl-discovery-data')/HERE.name
RAW.mkdir(parents=True,exist_ok=True)

def case(phi,y,power=2,n=1024,window=12.,steps=32,chirp=0.,order=4,shape='gaussian'):
    start=time.time()
    requested_steps=steps
    # Avoid split-step parametric resonances at high frequency. This guard was
    # added after retaining two false minima in initial-main.json.
    steps=max(steps,int(np.ceil(1.703*abs(y/phi)*(np.pi*n/window)**2/2)))
    initial=(lambda t:1/np.cosh(t)*np.exp(-.5j*chirp*t*t)) if shape=='sech' else None
    f=Flow(phi,y/phi,n,window,steps,power,chirp,order,initial=initial)
    values,modes,direct=f.spectrum(k=2)
    excess=values[0]/kerr_anchor(phi)-1
    prediction=(np.sqrt(2/3)*np.sqrt(y) if power==2 else .64226*y**(2/3))*phi/np.sqrt(1+phi*phi)
    mode=unpack(modes[:,0]);width=np.sqrt(np.sum(f.t*f.t*abs(mode)**2))
    row=dict(phi=phi,y=y,power=power,shape=shape,n=n,window=window,steps=steps,chirp=chirp,order=order,
             requested_steps=requested_steps,lambda_min=values[0],lambda_2=values[1],excess=excess,prediction=prediction,
             ratio=excess/prediction,rms_width=width,predicted_width=(y/24)**.25,
             reciprocal_check=float(max(abs(values-direct)/values)),seconds=time.time()-start,**f.diagnostics())
    print(json.dumps(row),flush=True)
    np.savez_compressed(RAW/f'phi{phi}_y{y}_p{power}_n{n}_w{window}_s{steps}_c{chirp}_o{order}_{shape}.npz',t=f.t,mean=f.mean,modes=modes)
    return row

def main():
    p=argparse.ArgumentParser();p.add_argument('--suite',default='pilot');a=p.parse_args()
    if a.suite=='pilot': cases=[dict(phi=7.,y=1e-4),dict(phi=.25,y=1e-4)]
    elif a.suite=='main':
        cases=[dict(phi=phi,y=y) for phi in [.25,1.25,7.,17.] for y in [1e-6,1e-5,1e-4,1e-3,1e-2]]
        cases += [dict(phi=7.,y=y,power=4) for y in [1e-6,1e-5,1e-4,1e-3,1e-2]]
    elif a.suite=='checks':
        cases=[dict(phi=7.,y=1e-5,n=2048),dict(phi=7.,y=1e-5,n=2048,window=24.),
               dict(phi=7.,y=1e-5,steps=64),dict(phi=7.,y=1e-5,steps=256,order=2),
               dict(phi=7.,y=.1),dict(phi=.03,y=1e-4),
               dict(phi=7.,y=1e-3,chirp=.5),dict(phi=7.,y=1e-3,chirp=-.5)]
    elif a.suite=='extra':
        cases=[dict(phi=phi,y=y) for phi in [2.,40.,50.] for y in [1e-6,1e-2]]
        cases += [dict(phi=.03,y=y,n=2048) for y in [1e-8,1e-7,1e-6]]
        cases += [dict(phi=7.,y=y,shape='sech',n=2048,window=24.) for y in [1e-6,1e-5,1e-4]]
        cases += [dict(phi=.25,y=.01,n=512,steps=2048),dict(phi=7.,y=1e-7,n=2048)]
    else: raise ValueError(a.suite)
    rows=[]
    for kwargs in cases:
        rows.append(case(**kwargs));(HERE/f'{a.suite}.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
