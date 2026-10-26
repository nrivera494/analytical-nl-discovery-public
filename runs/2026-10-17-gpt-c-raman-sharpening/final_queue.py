"""Prioritize frozen production and distinct controls before repeated checks.
gpt-c / gpt-6-astra / gpt. Ordering only: no scientific acceptance rule changes.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def read(name):
    p=HERE/(name+'_cases.json')
    return json.loads(p.read_text()) if p.exists() else []

def main():
    controls=read('essential_control');responses=read('response_control')
    n4=[c for c in controls if c['N']==4]
    n16=[c for c in controls if c['N']==16]
    first16=[c for c in n16 if c['id'].endswith(('_baseline','_fine'))]
    rest16=[c for c in n16 if c not in first16]
    damped=read('damped_control');bw=read('bw_refinement');rr=read('response_refinement')
    if '--post-holdout' in sys.argv:
        # Full-bracket uncertainty tests take priority over repeated interior-N
        # controls and optional matched-shape scans. Original manifests remain.
        ordered=(read('heldout_response')+read('length_extension')+n4
            +read('physical_control')+read('physical_refinement')+first16
            +[c for c in responses if c['id'].endswith('_wide')]
            +[c for c in responses if c['id'].endswith('_fine')]
            +[c for c in damped if c['N']==4]+[c for c in bw if c['N']==3]
            +sorted(read('bw_holdout_refinement'),key=lambda c:-c['N'])+rest16+[c for c in controls if c['N']==8]
            +read('matched_shape')+[c for c in bw if c['N'] in [8,16]]+rr
            +[c for c in bw if c['N'] not in [3,8,16]]+[c for c in damped if c['N']!=4])
        filename='post_holdout_queue_cases.json'
    else:
        ordered=(read('heldout_response')+read('length_extension')+n4+first16
            +[c for c in responses if c['id'].endswith('_wide')]+read('physical_control')
            +[c for c in responses if c['id'].endswith('_fine')]+read('physical_refinement')
            +[c for c in damped if c['N']==4]+rest16
            +[c for c in controls if c['N']==8]+[c for c in bw if c['N'] in [3,8,16]]
            +[c for c in rr if c['N']==3]+read('matched_shape')
            +[c for c in rr if c['N']==16]+[c for c in bw if c['N'] not in [3,8,16]]
            +[c for c in damped if c['N']!=4])
        filename='final_queue_cases.json'
    unique={}
    for c in ordered:
        if c['id'] in unique and unique[c['id']]!=c:raise RuntimeError('Conflicting case '+c['id'])
        unique[c['id']]=c
    (HERE/filename).write_text(json.dumps(list(unique.values()),indent=2)+'\n')
    print('Final ordered queue:',len(unique),'cases; completed cases are skipped, unrun cases retained at cutoff.')

if __name__=='__main__':main()
