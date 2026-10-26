#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Serial training-only refinement of the best completed start at each N."""
import os,sys,time,datetime,subprocess,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('~/analytical-nl-discovery-data')/HERE.name
PYTHON='~/agent-work/venv/bin/python'
for N,T in [(3,140),(4,200),(5,280)]:
    tag=f'pyopt_N{N}_T{T}_polish'
    if (RAW/(tag+'_summary.json')).exists():continue
    choices=[]
    for p in RAW.glob(f'pyopt_N{N}_T{T}_*_summary.json'):
        d=json.loads(p.read_text());choices.append((d['best_f_zs'],p.stem.replace('_summary','')))
    if not choices:raise RuntimeError(f'No completed start for N={N}')
    best,source=max(choices)
    while True:
        pressure=subprocess.check_output(['memory_pressure'],text=True)
        free=int(pressure.split('free percentage:')[1].split('%')[0]);print('MEMORY',free,flush=True)
        if free>=35:break
        time.sleep(30)
    cmd=[PYTHON,'-u',str(HERE/'adjoint.py'),str(N),str(T),'polish','--warm',str(RAW/(source+'_bestcoef.csv')),
         '--hfac','1','--zs-refine','4','--method','BFGS','--precondition','--maxiter','180','--stop-gradient','1e-6','--mode','checkopt',
         '--max-seconds',str({3:420,4:600,5:1200}[N])]
    record=dict(agent='gpt-a',model='gpt-6-astra',family='gpt',source=source,source_objective=best,
                command=cmd,started_local=datetime.datetime.now().isoformat())
    (RAW/'polish_status.json').write_text(json.dumps(dict(active=tag,**record),indent=2))
    (RAW/(tag+'_launch.json')).write_text(json.dumps(record,indent=2))
    print('START',tag,'from',source,flush=True)
    with open(RAW/(tag+'.stdout'),'a') as f:
        result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,
                              env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1'))
    print('FINISH',tag,result.returncode,flush=True)
    if result.returncode!=0:
        (RAW/'polish_status.json').write_text(json.dumps(dict(active=None,failed=tag,returncode=result.returncode)))
        sys.exit(result.returncode)
(RAW/'polish_status.json').write_text(json.dumps(dict(active=None,finished_local=datetime.datetime.now().isoformat())))
