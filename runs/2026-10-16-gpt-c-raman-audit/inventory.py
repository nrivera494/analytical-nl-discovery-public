"""Execution inventory, including unrun configurations. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
planned={};outputs={};rss=[]
for p in HERE.glob('*.json'):
    r=json.loads(p.read_text())
    if isinstance(r,list):
        for c in r:
            if isinstance(c,dict) and 'id' in c and 'N' in c:
                planned.setdefault(c['id'],[]).append(p.name)
    elif isinstance(r,dict) and 'case' in r and 'checkpoints' in r:
        if r.get('complete'):status='complete'
        elif r.get('measurement_failed'):status='measurement_failed'
        elif r.get('terminated_for_edge'):status='edge_stopped'
        elif r.get('intentionally_interrupted'):status='intentionally_interrupted'
        else:status='unfinished_without_stop_marker'
        outputs[r['case']['id']]=dict(file=p.name,status=status,checkpoints=len(r['checkpoints']),
            zN=[x['zN'] for x in r['checkpoints']])
        rss += [x['process_peak_rss_bytes'] for x in r['checkpoints'] if 'process_peak_rss_bytes' in x]
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',run_id=HERE.name,
         scope='Per-case run_audit.py reports; calibration, compression and the pinned-solver cross-check have separate reports.',
         case_count=len(outputs),counts={s:sum(v['status']==s for v in outputs.values()) for s in set(v['status'] for v in outputs.values())},
         peak_recorded_python_rss_bytes=max(rss) if rss else None,
         not_executed=[dict(case=k,configuration_files=v) for k,v in sorted(planned.items()) if k not in outputs],
         cases=outputs)
(HERE/'execution_inventory.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
