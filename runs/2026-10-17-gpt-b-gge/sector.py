#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Symmetry-controlled follow-up."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from conditioned import diagnostic
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def shell():
    memory_gate();full=Model(5);m,U=reflection_sector(full);rows=[]
    rng=np.random.default_rng(9621)
    for E,groups in [(.6,(1,2)),(.9,(1,4))]:
        initial=U.T@full.launch(E,0,groups=groups,aligned=True);H=m.invariants(initial)[2]
        aa=shell_samples(m,E,200000,rng);hs=m.invariants(aa)[:,2];sd=hs.std()
        blocks=np.empty((3,4,200,4));diags=np.empty((3,4,6))
        for chain in range(4):
            a=initial.copy() if chain<2 else shell_samples(m,E,1,rng)[0]
            for width in [.8,.4]:
                a,_,_=m.mcmc(a,E,H,0,width*sd,0,steps=200000,seed=9631+chain+round(E*100))
            for wi,width in enumerate([.2,.1,.05]):
                a,_,_=m.mcmc(a,E,H,0,width*sd,0,steps=300000,seed=9641+chain+100*wi+round(E*100))
                a,b,d=m.mcmc(a,E,H,0,width*sd,0,steps=2000000,seed=9651+chain+100*wi+round(E*100))
                blocks[wi,chain]=b;diags[wi,chain]=d
        path=DATA/f'reflection_shell_E{E:g}.npz';np.savez_compressed(path,blocks=blocks,diagnostics=diags,U=U)
        stats=[dict(diagnostic(blocks[wi,:,:,0]),width=w) for wi,w in enumerate([.2,.1,.05])]
        row=dict(E=E,groups=list(groups),M=m.M,target_H=H,H_sd=sd,widths=stats,
                 bandwidth_shift=abs(stats[-1]['mean']-stats[-2]['mean']),raw_file=str(path))
        rows.append(row);print(serializable(row),flush=True)
    save_json(RUN/'reflection_predictions.json',dict(**IDENTITY,rows=rows))

def dynamics():
    full=Model(5);m,U=reflection_sector(full);rows=[]
    for E,groups in [(.6,(1,2)),(.9,(1,4))]:
        for variant in ['exact_sector','perturbed_1e-6','perturbed_1e-4']:
            path=DATA/f'reflection_dynamics_E{E:g}_{variant}.npz'
            initial=full.launch(E,0,groups=groups,aligned=True)
            if variant=='exact_sector':
                used=m;a=U.T@initial
            else:
                used=full;a=initial.copy();eps=float(variant.split('_')[1]);a[1]*=np.exp(1j*eps)
            if not path.exists():
                memory_gate();out=used.run(a,zmax=240000,dt=.02,sigma=0,block=1000,sample=10)
                np.savez_compressed(path,**out)
            else:out=np.load(path)
            v=out['moments'][80:,1]/out['moments'][80:,0]
            batch=v.reshape(-1,10).mean(axis=1)
            rows.append(dict(E=E,variant=variant,initial_invariants=used.invariants(a),
                mean=float(v.mean()),se=float(batch.std(ddof=1)/np.sqrt(len(batch))),
                half_shift=float(v[-80:].mean()-v[:80].mean()),checks=out['checks'],raw_file=str(path)))
            print(rows[-1],flush=True)
    save_json(RUN/'reflection_summary.json',dict(**IDENTITY,rows=rows))

if __name__=='__main__':globals()[sys.argv[1]]()
