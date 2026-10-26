"""Execution and resource ledger. gpt-c / gpt-6-astra / gpt."""
import json,re
from pathlib import Path
from collections import Counter
from independent import write_json,RAW
HERE=Path(__file__).resolve().parent

def main():
    designed={}
    for file in sorted(HERE.glob('*cases.json')):
        cs=json.loads(file.read_text())
        for c in cs:
            if not isinstance(c,dict) or 'id' not in c:continue
            if c['id'] in designed:
                if designed[c['id']]['case']!=c:raise RuntimeError('Case definition changed: '+c['id'])
                designed[c['id']]['design_files'].append(file.name)
            else:designed[c['id']]={'case':c,'design_files':[file.name]}
    for file in HERE.glob('*.json'):
        x=json.loads(file.read_text())
        if not isinstance(x,dict) or 'case' not in x or 'checkpoints' not in x:continue
        c=x['case']
        if c['id'] not in designed:designed[c['id']]={'case':c,'design_files':['case output only; check adaptive manifest history']}
        elif c!=designed[c['id']]['case']:raise RuntimeError('Output differs from case manifest: '+c['id'])
    records=[];rss=[];free=[];wall=[];hashes=Counter();fitcommits=Counter()
    for name,item in sorted(designed.items()):
        file=HERE/(name+'.json');status='unrun';x={}
        if file.exists():
            x=json.loads(file.read_text())
            status='complete' if x.get('complete') else 'edge-terminated' if x.get('terminated_for_edge') else 'error' if x.get('error') else 'partial'
            rss.append(x.get('process_peak_rss_bytes',0));free.append(x['free_percentage_at_start']);wall.append(x.get('wall_seconds',0))
            hashes[x['implementation_sha256']]+=1
            if item['case']['split']=='heldout':fitcommits[str(x.get('holdout_fit_commit'))]+=1
        records.append(dict(id=name,split=item['case']['split'],status=status,design_files=item['design_files'],
                            saved_checkpoints=len(x.get('checkpoints',[])),error=x.get('error')))
    out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',run_id=HERE.name,
             status_counts=dict(Counter(r['status'] for r in records)),records=records,
             maximum_process_rss_bytes=max(rss,default=0),minimum_free_percentage=min(free,default=None),
             total_recorded_case_wall_seconds=sum(wall),implementation_hash_counts=dict(hashes),
             heldout_fit_commit_counts=dict(fitcommits),notes='Serial, single-thread propagations; sparse raw checkpoints stored outside git. Unrun cases are not evidence.')
    manifests=sorted(set(f for r in records for f in r['design_files']))
    out['status_by_design_manifest']={f:dict(Counter(r['status'] for r in records if f in r['design_files'])) for f in manifests}
    out['python_maximum_process_rss_bytes']=out['maximum_process_rss_bytes']
    library=RAW/'library_crosscheck.txt'
    if library.exists():
        match=re.search(r'peak_rss_bytes=(\d+)',library.read_text())
        if match:
            out['julia_maximum_process_rss_bytes']=int(match.group(1))
            out['maximum_process_rss_bytes']=max(out['maximum_process_rss_bytes'],int(match.group(1)))
    write_json(HERE/'inventory.json',out)
    print({k:v for k,v in out.items() if k!='records'})
if __name__=='__main__':main()
