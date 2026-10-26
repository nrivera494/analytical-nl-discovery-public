#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Independent shell prediction."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name
DATA.mkdir(parents=True,exist_ok=True)

def targets():
    for E,groups,seeds in [(.6,(1,2),range(4101,4107)),(.9,(1,4),range(4201,4205))]:
        for seed in list(seeds)+[0]:
            yield dict(E=E,groups=groups,seed=seed,aligned=seed==0,held_out=E==.9)

def conditional(values,h,l,sd,width,include_l):
    u=(values[:,1]-h)/(width*sd[0]);v=(values[:,2]-l)/(width*sd[1])
    exponent=-.5*(u*u+(v*v if include_l else 0));exponent-=exponent.max()
    w=np.exp(exponent);w/=w.sum();mu=float(w@values[:,0]);ess=float(1/(w@w))
    se=float(np.sqrt(np.sum(w*w*(values[:,0]-mu)**2)))
    return dict(width=width,mean=mu,se=se,effective_samples=ess,resolved=ess>=200)

def main():
    memory_gate();m=Model(5);rows=[]
    for E in [.6,.9]:
        start=time.time();path=DATA/f'shell_E{E:g}.npy';size=2000000
        if path.exists():raise RuntimeError('Refusing to overwrite shell sample')
        data=np.lib.format.open_memmap(path,mode='w+',dtype='float64',shape=(size,3))
        rng=np.random.default_rng(8101+int(100*E))
        for j in range(0,size,20000):
            a=shell_samples(m,E,min(20000,size-j),rng);inv=m.invariants(a)
            data[j:j+len(a)]=np.column_stack([abs(a[:,0])**2,inv[:,2:4]])
        data.flush();sd=data[:,1:].std(axis=0)
        for target in targets():
            if target['E']!=E:continue
            inv=m.invariants(m.launch(E,target['seed'],groups=target['groups'],aligned=target['aligned']))
            row=dict(target,**IDENTITY,N=float(inv[0]),H=float(inv[2]),L=float(inv[3]),
                RJ=dirichlet_moments(m.q,E)['mean'][0],shell_samples=size,
                shell_H_mean=float(data[:,1].mean()),shell_H_sd=float(sd[0]),
                shell_L_sd=float(sd[1]))
            for name,inc in [('H_only',False),('H_and_L',True)]:
                row[name]=[conditional(data,inv[2],inv[3],sd,w,inc) for w in [.2,.1,.05]]
            rows.append(row)
            print('prediction',E,target['seed'],'H,L',row['H'],row['L'],
                'H-only',row['H_only'][-1],'H,L',row['H_and_L'][-1],flush=True)
        print('shell seconds',time.time()-start,flush=True)
    save_json(RUN/'shell_predictions.json',dict(**IDENTITY,rows=rows))

if __name__=='__main__':main()
