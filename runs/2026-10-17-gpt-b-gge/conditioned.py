#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Conditional shell MCMC."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def diagnostic(chains):
    # Split chains of 10000-step block means; conservative chain-level SE.
    n=chains.shape[1]//2
    split=np.concatenate([chains[:,:n],chains[:,-n:]],axis=0)
    W=split.var(axis=1,ddof=1).mean();B=n*split.mean(axis=1).var(ddof=1)
    rhat=float(np.sqrt(((n-1)*W/n+B/n)/W))
    chain_means=chains.mean(axis=1)
    se=max(float(chain_means.std(ddof=1)/np.sqrt(len(chains))),
           float(np.sqrt(W/chains.size)))
    return dict(mean=float(chains.mean()),se=se,chain_means=chain_means,
                chain_range=float(np.ptp(chain_means)),rhat=rhat,
                resolved=rhat<1.05 and np.ptp(chain_means)<.01)

def main(refine=False):
    memory_gate();m=Model(5)
    shell=json.loads((RUN/'shell_predictions.json').read_text())['rows'];results=[]
    widths=[.1,.05] if refine else [.2,.1,.05]
    steps=4000000 if refine else 1000000
    for j,row in enumerate(shell):
        for include_l in [False,True]:
            if refine and (not include_l or (row['E'],row['seed']) not in
                           [(.6,4103),(.6,4104),(.9,4202),(.9,4204),(.9,0)]):continue
            tag=f'conditional_E{row["E"]:g}_p{row["seed"]}_L{int(include_l)}'
            if refine:tag+='__refined'
            path=DATA/(tag+'.npz')
            if path.exists():
                out=np.load(path);chain_blocks=out['blocks'];accept=out['acceptance']
            else:
                memory_gate();start=time.time();chain_blocks=np.empty((len(widths),4,steps//10000,4));accept=np.empty((len(widths),4,6))
                for chain in range(4):
                    rng=np.random.default_rng(9101+100*j+chain)
                    if chain<2:a=m.launch(row['E'],row['seed'],groups=row['groups'],aligned=row['aligned'])
                    else:a=shell_samples(m,row['E'],1,rng)[0]
                    for w in [.8,.4]:
                        a,_,_=m.mcmc(a,row['E'],row['H'],row['L'],w*row['shell_H_sd'],
                            w*row['shell_L_sd'] if include_l else 0,steps=200000,seed=int(rng.integers(1,2**32)))
                    for wi,w in enumerate(widths):
                        a,_,_=m.mcmc(a,row['E'],row['H'],row['L'],w*row['shell_H_sd'],
                            w*row['shell_L_sd'] if include_l else 0,steps=300000,seed=int(rng.integers(1,2**32)))
                        a,block,diag=m.mcmc(a,row['E'],row['H'],row['L'],w*row['shell_H_sd'],
                            w*row['shell_L_sd'] if include_l else 0,steps=steps,seed=int(rng.integers(1,2**32)))
                        chain_blocks[wi,chain]=block;accept[wi,chain]=diag
                np.savez_compressed(path,blocks=chain_blocks,acceptance=accept)
                print(tag,'seconds',round(time.time()-start,1),flush=True)
            stats=[]
            for wi,w in enumerate(widths):
                d=diagnostic(chain_blocks[wi,:,:,0]);d['width']=w
                d['mean_H']=float(chain_blocks[wi,:,:,1].mean());d['mean_L']=float(chain_blocks[wi,:,:,2].mean())
                d['acceptance_fractions']=accept[wi,:,:2]/(steps/2)
                stats.append(d)
            results.append(dict(E=row['E'],seed=row['seed'],aligned=row['aligned'],held_out=row['held_out'],
                include_L=include_l,target_H=row['H'],target_L=row['L'],widths=stats,
                bandwidth_shift=abs(stats[-1]['mean']-stats[-2]['mean']),raw_file=str(path)))
            print(tag,serializable(stats[-1]),flush=True)
            save_json(RUN/('conditioned_refined_predictions.json' if refine else 'conditioned_predictions.json'),dict(**IDENTITY,rows=results))

if __name__=='__main__':main('--refine' in sys.argv)
