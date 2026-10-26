"""Serial memory-gated launch helper. gpt-d / gpt-6-astra / gpt."""
import json,os,pathlib,subprocess,sys,time
log=pathlib.Path(sys.argv[1]);log.parent.mkdir(exist_ok=True,parents=True)
while True:
 text=subprocess.check_output(['memory_pressure'],text=True)
 line=next(x for x in text.splitlines() if 'free percentage' in x);print(line,flush=True)
 if int(line.split(':')[1].strip().rstrip('%'))>=35:break
 time.sleep(15)
start=time.monotonic()
with log.open('w') as f:
 p=subprocess.run(sys.argv[2:],stdout=f,stderr=subprocess.STDOUT)
result={'agent':'gpt-d','model':'gpt-6-astra','family':'gpt','returncode':p.returncode,'wall_s':time.monotonic()-start,'command':sys.argv[2:]}
log.with_suffix('.exit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
sys.exit(p.returncode)
