#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Preregistered follow-up."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from shell import targets
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name
m=Model(5)
for h in [.02,.01]:
    for t in targets():
        selected=(t['E']==.6 and t['seed'] in [4101,4103,4104,0]) or (t['E']==.9 and t['seed'] in [4201,4204,0])
        if h==.01:selected=t['E']==.6 and t['seed'] in [4103,0]
        if not selected:continue
        key=f'extended_E{t["E"]:g}_p{t["seed"]}_s0_d7101_h{h:g}_z240000';path=DATA/(key+'.npz')
        if path.exists():continue
        memory_gate();a=m.launch(t['E'],t['seed'],groups=t['groups'],aligned=t['aligned'])
        out=m.run(a,zmax=240000,dt=h,sigma=0,seed=7101,block=1000,sample=10)
        np.savez_compressed(path,**out)
        row=dict(**IDENTITY,key=key,case=t,sigma=0,disorder_seed=7101,dt=h,zmax=240000,
                 raw_file=str(path),checks=out['checks'],wall_seconds=out['wall_seconds'])
        row['last_window']=unpack(out['moments'][80:],m.M)
        with (DATA/'records.jsonl').open('a') as f:f.write(json.dumps(serializable(row))+'\n')
        print(key,'I0',row['last_window']['mean'][0],'drifts',out['checks'][4:8],flush=True)
# Strong-disorder paired launch follow-up, selected after the initial scan.
from run import one
for dis in range(7101,7105):
    for seed in [4101,0]:
        one(m,dict(E=.6,groups=(1,2),seed=seed,aligned=seed==0,held_out=False),
            sigma=3.,dis=dis,zmax=24000,tag='memory_extended')
