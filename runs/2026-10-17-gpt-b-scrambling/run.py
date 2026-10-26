#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Independent TWA/Fock tests."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from scipy.special import gammaln
from scipy.optimize import brentq
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name
DATA.mkdir(parents=True,exist_ok=True)

def exact():
    memory_gate();rows=[]
    for n in [16,64,256,1024,4096]:
        cutoff=int(n+16*np.sqrt(n)+100);k=np.arange(cutoff+1)
        psi=np.exp((-n+k*np.log(n)-gammaln(k+1))/2).astype(complex)
        captured_norm=float(np.vdot(psi,psi).real)
        psi/=np.sqrt(captured_norm)
        def moments(s):
            v=psi*np.exp(-.5j*s/n*k*(k-1));norm=np.vdot(v,v).real
            a=np.sum(np.conj(v[:-1])*v[1:]*np.sqrt(k[1:]))
            a2=np.sum(np.conj(v[:-2])*v[2:]*np.sqrt(k[2:]*(k[2:]-1)))
            ni=float(np.sum(k*abs(v)**2));C=abs(a)**2/ni
            det=(.5+ni-abs(a)**2)**2-abs(a2-a*a)**2
            return C,det,norm
        crossing=brentq(lambda s:moments(s)[0]-.5,.1,2*np.sqrt(n))
        analytic=2*n*np.arcsin(np.sqrt(np.log(2)/(4*n)))
        probes=[]
        for s in [1.,2.,n**(1/6),.1*np.sqrt(n)]:
            C,det,norm=moments(s)
            am=np.sqrt(n)*np.exp(n*np.expm1(-1j*s/n))
            a2=n*np.exp(-1j*s/n+n*np.expm1(-2j*s/n))
            analytic_det=(.5+n-abs(am)**2)**2-abs(a2-am*am)**2
            probes.append(dict(s=s,coherence=C,det=det,analytic_det=float(analytic_det),
                asymptotic_excess=(2*s**6+4.5*s**4)/n,norm=norm))
        rows.append(dict(n=n,cutoff=cutoff,captured_norm_before_normalizing=captured_norm,
                         held_out=n in [256,4096],crossing=crossing,
                         predicted_crossing=float(analytic),probes=probes))
    exp=float(np.polyfit(np.log([r['n'] for r in rows]),np.log([r['crossing'] for r in rows]),1)[0])
    exps=[]
    for i,s in enumerate([1.,2.]):
        r=rows[1:];exps.append(dict(s=s,exponent=float(np.polyfit(np.log([1/x['n'] for x in r]),
            np.log([x['probes'][i]['det']-.25 for x in r]),1)[0])))
    save_json(RUN/'exact_summary.json',dict(**IDENTITY,rows=rows,ballistic_exponent=exp,
                                         covariance_error_exponents=exps))
    print('exact exponents',exp,exps,flush=True)

def lyapunov():
    m=Model(5);a=m.launch(.6,4101);rows=[]
    for seed in [7501,7502]:
        for ep in [1e-6,1e-7,1e-8]:
            path=DATA/f'lyapunov_d{seed}_eps{ep:g}.npy'
            if path.exists():g=np.load(path)
            else:
                memory_gate();g=m.lyapunov(a,epsilon=ep,seed=seed);np.save(path,g)
            blocks=g[2000:].reshape(-1,500).mean(axis=1)
            rows.append(dict(seed=seed,epsilon=ep,lambda1=float(g[2000:].mean()),
                se=float(blocks.std(ddof=1)/np.sqrt(len(blocks))),blocks=blocks,
                predicted_slope=float(1/(2*g[2000:].mean()))))
            print('Lyapunov',rows[-1],flush=True)
    save_json(RUN/'lyapunov_summary.json',dict(**IDENTITY,rows=rows))

def one(m,n,dis,dt=.04,dephased=False):
    tag=f'{"dephased" if dephased else "coherent"}_n{n:g}_d{dis}_h{dt:g}'
    path=DATA/(tag+'.npz')
    if path.exists():return
    memory_gate();rng=np.random.default_rng(9301)
    a=m.launch(.6,4101);outputs=[];finals=[];start=time.time()
    for b in range(8):
        if dephased:initial=abs(a)*np.exp(2j*np.pi*rng.random((32,m.M)))
        else:initial=np.broadcast_to(a,(32,m.M)).copy()
        initial+=(rng.normal(size=initial.shape)+1j*rng.normal(size=initial.shape))/(2*np.sqrt(n))
        o,af=m.ensemble(initial,n,zmax=200 if dephased else 1200,dt=dt,
                       sample=.2 if dephased else 1,seed=dis)
        outputs.append(o);finals.append(af)
    np.savez_compressed(path,moments=np.array(outputs),final=np.array(finals))
    record=dict(**IDENTITY,n=n,disorder_seed=dis,dt=dt,dephased=dephased,shots=256,
                sample=.2 if dephased else 1,zmax=200 if dephased else 1200,
                raw_file=str(path),wall_seconds=time.time()-start)
    with (DATA/'records.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
    print(tag,'seconds',round(record['wall_seconds'],1),flush=True)

def coherent():
    m=Model(5)
    for dis in [7501,7502]:
        for n in [1e4,1e6,1e7,1e8,1e10,1e12]:one(m,n,dis)

def convergence():one(Model(5),1e8,7501,dt=.02)
def dephased():
    m=Model(5)
    for n in [1e4,1e8,1e12]:one(m,n,7501,dephased=True)

if __name__=='__main__':getattr(sys.modules[__name__],sys.argv[1])()
