#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
# Lightweight serial launcher; each child is the only heavy process of this agent.
import os,sys,time,datetime,subprocess,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('~/analytical-nl-discovery-data')/HERE.name
PYTHON='~/agent-work/venv/bin/python'
if os.environ.get('WAIT_FOR_CONVERGENCE'):
    while not (RAW/'integrable_N1.json').exists():
        print('Waiting for preceding convergence sweep',flush=True);time.sleep(10)
commands=[('robust',[PYTHON,'-u',str(HERE/'suite.py'),'robust']),
          ('tl_scan',[PYTHON,'-u',str(HERE/'suite.py'),'tl_scan'])]
# Establish an independently optimized candidate at each N before additional starts.
for N,T,start,it in [(3,140,'TL',180),(4,200,'B',180),(5,280,'TL',180),
                      (3,140,'r1',120),(4,200,'TL',120),(5,280,'r1',120),
                      (3,140,'r2',120),(4,200,'r1',120),(5,280,'r2',120),
                      (3,140,'r3',120),(4,200,'r2',120),(5,280,'r3',120)]:
    commands.append((f'pyopt_N{N}_T{T}_{start}',[PYTHON,'-u',str(HERE/'adjoint.py'),str(N),str(T),start,
                     '--maxiter',str(it),'--hfac','2','--mode','checkopt' if start in ['TL','B'] else 'opt']))
    failure=RAW/(f'pyopt_N{N}_T{T}_{start}_summary.json')
    if failure.exists() and json.loads(failure.read_text()).get('failed'):
        commands.append((f'pyopt_N{N}_T{T}_{start}resume',[PYTHON,'-u',str(HERE/'adjoint.py'),str(N),str(T),start+'resume',
                         '--warm',str(RAW/(f'pyopt_N{N}_T{T}_{start}_bestcoef.csv')),
                         '--maxiter',str(it),'--hfac','2','--mode','checkopt']))
for name,cmd in commands:
    # Reserve time for final independent readout and documentation.
    if datetime.datetime.now().hour>=20:
        print('QUEUE STOP: 20:00 local, reserve qualification/finalization',flush=True);break
    while True:
        out=subprocess.check_output(['memory_pressure'],text=True)
        pct=int(out.split('free percentage:')[1].split('%')[0]);print('MEMORY',pct,flush=True)
        if pct>=35:break
        time.sleep(30)
    if (RAW/(name+'_summary.json')).exists():print('COMPLETE',name,flush=True);continue
    status={'active':name,'started_local':datetime.datetime.now().isoformat(),'command':cmd}
    (RAW/'queue_status.json').write_text(json.dumps(status,indent=2));print('START',name,flush=True)
    with open(RAW/(name+'.stdout'),'a') as f:
        result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,
                              env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1'))
    status.update(returncode=result.returncode,finished_local=datetime.datetime.now().isoformat())
    with open(RAW/'queue_completed.jsonl','a') as f:f.write(json.dumps(status)+'\n')
    print('FINISH',name,result.returncode,flush=True)
    if result.returncode!=0:break
(RAW/'queue_status.json').write_text(json.dumps({'active':None,'finished_local':datetime.datetime.now().isoformat()}))
