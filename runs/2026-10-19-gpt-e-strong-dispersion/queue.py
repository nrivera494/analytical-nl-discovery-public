"""gpt-e / gpt-6-astra / gpt. Serial, memory-gated audit launcher."""
import os,re,json,time,subprocess,datetime,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
PY='~/agent-work/venv/bin/python'
weak='runs/2026-10-19-gpt-e-weak-dispersion/'
strong='runs/2026-10-19-gpt-e-strong-dispersion/'
sim='runs/2026-10-19-gpt-e-similariton/'
raw='~/analytical-nl-discovery-data/'
jobs=[
    ('strong-edges',[PY,'-W','ignore',strong+'run.py','--suite','edges']),
    ('strong-rk4ip1024',['julia','--project=solver',weak+'solver_crosscheck.jl',raw+'2026-10-19-gpt-e-strong-dispersion/crosscheck.npz','1024']),
    ('strong-rk4ip2048',['julia','--project=solver',weak+'solver_crosscheck.jl',raw+'2026-10-19-gpt-e-strong-dispersion/crosscheck.npz','2048']),
    ('sim-reduced-main',[PY,'-W','ignore',sim+'reduced.py','--suite','main']),
    ('sim-reduced-checks',[PY,'-W','ignore',sim+'reduced.py','--suite','checks']),
    ('sim-fullfield-main',[PY,'-W','ignore',sim+'fullfield.py','--suite','main']),
    ('sim-fullfield-checks',[PY,'-W','ignore',sim+'fullfield.py','--suite','checks']),
    ('sim-prepare-crosscheck',[PY,'-W','ignore',sim+'prepare_crosscheck.py']),
    ('sim-rk4ip1024',['julia','--project=solver',weak+'solver_crosscheck.jl',raw+'2026-10-19-gpt-e-similariton/crosscheck.npz','1024']),
    ('sim-rk4ip2048',['julia','--project=solver',weak+'solver_crosscheck.jl',raw+'2026-10-19-gpt-e-similariton/crosscheck.npz','2048']),
]
extra='--extra' in sys.argv
if extra:
    jobs=[
        ('hydro256',[PY,'-W','ignore',strong+'hydro.py','--n','256']),
        ('hydro512',[PY,'-W','ignore',strong+'hydro.py','--n','512']),
        ('hydro512-window',[PY,'-W','ignore',strong+'hydro.py','--n','512','--window','24']),
        ('weak-optimize',[PY,'-W','ignore',weak+'optimize.py']),
        ('strong-optimize',[PY,'-W','ignore',strong+'optimize.py']),
        ('sim-optimize',[PY,'-W','ignore',sim+'optimize.py']),
        ('sim-fullfield-main-discrete',[PY,'-W','ignore',sim+'fullfield.py','--suite','main']),
        ('sim-fullfield-checks-discrete',[PY,'-W','ignore',sim+'fullfield.py','--suite','checks']),
        ('sim-edge-resolution',[PY,'-W','ignore',sim+'fullfield.py','--suite','edge-resolution']),
        ('sim-short',[PY,'-W','ignore',sim+'fullfield.py','--suite','short']),
    ]
env=os.environ.copy();env.update(JULIA_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
deadline=datetime.datetime(2026,10,19,12,48,tzinfo=datetime.timezone.utc).timestamp()
records=[]
for label,command in jobs:
    while True:
        if time.time()>deadline:raise SystemExit('Numerical-launch deadline reached; reserve finishing time')
        message=subprocess.check_output(['memory_pressure'],text=True)
        free=int(re.search(r'free percentage:\s*(\d+)',message).group(1))
        print(f'MEMORY {label}: {free}% free',flush=True)
        if free>=35:break
        time.sleep(15)
    start=time.time();dest=Path('/private/tmp')/('gpt-e-'+label+'.txt')
    print(f'START {label} -> {dest}',flush=True)
    with dest.open('w') as output:
        result=subprocess.run(command,cwd=ROOT,env=env,stdout=output,stderr=subprocess.STDOUT)
    row=dict(agent='gpt-e',model='gpt-6-astra',family='gpt',label=label,command=command,
             free_percentage_before=free,seconds=time.time()-start,returncode=result.returncode,output=str(dest))
    records.append(row);(HERE/('queue-extra-summary.json' if extra else 'queue-summary.json')).write_text(json.dumps(records,indent=2)+'\n')
    print(f'FINISH {label}: code={result.returncode}, seconds={row["seconds"]:.2f}',flush=True)
    if result.returncode:raise SystemExit('Stop serial queue on failure; inspect and resume explicitly')
