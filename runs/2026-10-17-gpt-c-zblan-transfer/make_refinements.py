"""Predeclared geometric localization controls. gpt-c / gpt-6-astra / gpt."""
import json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

def main():
    iteration=int(sys.argv[1]); out=[]
    unresolved_only='--unresolved-only' in sys.argv
    data=json.loads((HERE/'analysis.json').read_text())
    for p in data['peaks']:
        if unresolved_only and p['bracketed'] and all(s['verdict']!='unresolved bracket' for s in p['scores'].values()):continue
        if not p['bracketed']:
            row=next(x for x in data['rows'] if x['id']==p['best'] and x['zN']==4)
            T=row['T0_fs']*(1.5 if p['edge']=='upper' else 1/1.5)
            c=dict(row['case']);c.update(id=f"extend{iteration}_{p['model']}_N{p['N']}",T0_fs=T,
                n=2**int(np.ceil(np.log2(max(8192,96*T/2.5)))))
            if c['n']>32768:raise ValueError('extension exceeds grid budget')
            out.append(c);continue
        tri=[next(x for x in data['rows'] if x['id']==i and x['zN']==4) for i in p['bracket_ids']]
        for k in [0,1]:
            T=np.sqrt(tri[k]['T0_fs']*tri[k+1]['T0_fs'])
            width=120. if p['model']=='reference' and p['N']==6 else 96.
            c=dict(tri[1]['case']);c.update(id=f"refine{iteration}_{p['model']}_N{p['N']}_{k}",T0_fs=float(T),width=width,
                n=2**int(np.ceil(np.log2(max(8192,width*T/2.5)))),zN=[2.,3.,4.])
            if c['n']>32768:raise ValueError('refinement exceeds grid budget')
            out.append(c)
    path=HERE/f'refinement{iteration}_cases.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(path.name,len(out),'cases; commit before running')
if __name__=='__main__':main()
