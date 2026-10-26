#!/usr/bin/env python3
"""gpt-b / gpt-6-astra / gpt. Lightweight serial child resource recorder."""
import subprocess,sys,time,resource,json,datetime
command=sys.argv[1:];deadline=None
if command[:1]==['--deadline-utc']:
    deadline=datetime.datetime.fromisoformat(command[1].replace('Z','+00:00'))
    command=command[2:]
timeout=max(0.,(deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds()) if deadline else None
start=time.time();timed_out=False
try:
    result=subprocess.run(command,timeout=timeout);returncode=result.returncode
except subprocess.TimeoutExpired:
    # subprocess.run kills and reaps this wrapper's own child before raising.
    returncode=124;timed_out=True
r=resource.getrusage(resource.RUSAGE_CHILDREN)
print(json.dumps({'agent':'gpt-b','model':'gpt-6-astra','family':'gpt','command':command,
 'wall_seconds':time.time()-start,'child_peak_rss_bytes':r.ru_maxrss if sys.platform=='darwin' else r.ru_maxrss*1024,
 'user_seconds':r.ru_utime,'system_seconds':r.ru_stime,'returncode':returncode,'timed_out':timed_out,
 'deadline_UTC':deadline.isoformat() if deadline else None}),flush=True)
sys.exit(returncode)
