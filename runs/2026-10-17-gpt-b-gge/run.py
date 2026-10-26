#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Frozen GGE dynamics."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from shell import targets
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def one(m,t,sigma=0,dis=7101,dt=.04,zmax=24000,tag='deterministic'):
    key=f'{tag}_E{t["E"]:g}_p{t["seed"]}_s{sigma:g}_d{dis}_h{dt:g}_z{zmax:g}'
    path=DATA/(key+'.npz')
    if path.exists():return
    memory_gate();a=m.launch(t['E'],t['seed'],groups=t['groups'],aligned=t['aligned'])
    out=m.run(a,zmax=zmax,dt=dt,sigma=sigma,seed=dis)
    np.savez_compressed(path,**out)
    t=dict(t);t['groups']=list(t['groups'])
    row=dict(**IDENTITY,key=key,case=t,sigma=sigma,disorder_seed=dis,dt=dt,zmax=zmax,
             raw_file=str(path),checks=out['checks'],wall_seconds=out['wall_seconds'])
    row['last_window']=unpack(out['moments'][40 if zmax==24000 else 20:],m.M)
    with (DATA/'records.jsonl').open('a') as f:f.write(json.dumps(serializable(row))+'\n')
    print(key,'I0',row['last_window']['mean'][0],'drifts',out['checks'][4:8],flush=True)

def main(stage):
    m=Model(5)
    if stage=='deterministic':
        for t in targets():one(m,t)
    elif stage=='convergence':
        for t in targets():
            if t['seed'] in [4101,4103,0,4201]:one(m,t,dt=.02,tag='stepcheck')
    elif stage=='memory':
        for sig in [.003,.01,.03,.1,.3,1.,3.]:
            for dis in range(7101,7105):
                for seed in [4101,0]:
                    one(m,dict(E=.6,groups=(1,2),seed=seed,aligned=seed==0,held_out=False),
                        sigma=sig,dis=dis,zmax=8000,tag='memory')

if __name__=='__main__':main(sys.argv[1])
