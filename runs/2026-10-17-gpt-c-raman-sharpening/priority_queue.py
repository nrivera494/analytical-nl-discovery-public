"""Order already frozen controls within the wall-clock budget.
gpt-c / gpt-6-astra / gpt. No case parameters or acceptance rules are changed.
"""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def read(name):
    p=HERE/(name+'_cases.json')
    return json.loads(p.read_text()) if p.exists() else []

def main():
    length=read('length_extension');physical=read('physical_control')
    convergence=read('response_control');pr=read('physical_refinement')
    rr=read('response_refinement');bw=read('bw_refinement');damped=read('damped_control')
    ordered=(length+physical+[c for c in convergence if c['id'].endswith('_wide')]
        +[c for c in convergence if c['id'].endswith('_fine')]+pr
        +[c for c in damped if c['N']==4]+[c for c in bw if c['N'] in [3,8,16]]
        +[c for c in rr if c['N']==3]+read('matched_shape')
        +[c for c in rr if c['N']==16 and c['raman']=='as2s3']
        +[c for c in rr if c['N']==16 and c['raman']!='as2s3']
        +[c for c in bw if c['N'] not in [3,8,16]]+[c for c in damped if c['N']!=4])
    unique={}
    for c in ordered:
        if c['id'] in unique and unique[c['id']]!=c:raise RuntimeError('Conflicting case '+c['id'])
        unique[c['id']]=c
    (HERE/'priority_extra_cases.json').write_text(json.dumps(list(unique.values()),indent=2)+'\n')
    print('Priority extras:',len(unique),'(runner skips completed cases and obeys the production cutoff)')

if __name__=='__main__':main()
