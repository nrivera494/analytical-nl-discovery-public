#!/usr/bin/env python3
# agent: gpt-a; model: gpt-6-astra; family: gpt
"""Wait for the serial search, then polish/repropagate training cases only."""
import pathlib,subprocess,json,time,datetime,os,sys
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('~/analytical-nl-discovery-data')/HERE.name
PYTHON='~/agent-work/venv/bin/python'
while True:
    try:state=json.loads((RAW/'queue_status.json').read_text())
    except (FileNotFoundError,json.JSONDecodeError):time.sleep(5);continue
    if state.get('active') is None:break
    time.sleep(5)
counts={3:0,4:0,5:0}
for path in RAW.glob('pyopt_*_summary.json'):
    data=json.loads(path.read_text())
    if not data.get('failed') and not data['start'].startswith('polish'):counts[int(data['N'])]+=1
if any(n<3 for n in counts.values()):
    print('STOP: primary search ended before three completed starts per N',counts,flush=True)
    raise SystemExit(1)
stages=[('polish',[PYTHON,'-u',str(HERE/'polish_queue.py')]),
        ('training_repropagation',[PYTHON,'-u',str(HERE/'qualify.py'),'training']),
        ('TL_duration_peaks',[PYTHON,'-u',str(HERE/'qualify.py'),'tl_peak'])]
for label,cmd in stages:
    while True:
        pressure=subprocess.check_output(['memory_pressure'],text=True)
        free=int(pressure.split('free percentage:')[1].split('%')[0]);print('MEMORY',free,flush=True)
        if free>=35:break
        time.sleep(30)
    state=dict(active=label,started_local=datetime.datetime.now().isoformat(),command=cmd)
    (RAW/'final_training_status.json').write_text(json.dumps(state,indent=2));print('START',label,flush=True)
    with open(RAW/(label+'_pipeline.stdout'),'a') as output:
        result=subprocess.run(cmd,stdout=output,stderr=subprocess.STDOUT,
                              env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1'))
    print('FINISH',label,result.returncode,flush=True)
    if result.returncode!=0:
        state.update(active=None,failed=label,returncode=result.returncode)
        (RAW/'final_training_status.json').write_text(json.dumps(state,indent=2));sys.exit(result.returncode)
(RAW/'final_training_status.json').write_text(json.dumps(dict(active=None,ready_for_selection=True,finished_local=datetime.datetime.now().isoformat())))
print('READY FOR MASK SELECTION AND COMMIT; NO SELECTED-MASK HOLDOUTS HAVE RUN',flush=True)
