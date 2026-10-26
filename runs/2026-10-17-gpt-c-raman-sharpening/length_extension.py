"""Resolve missing plateau brackets without retuning laws. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'summary.json').read_text());done=set((p['response'],p['shape'],p['N']) for p in s['preferred_peaks'] if p['dispersion']=='constant')
    groups=defaultdict(list)
    for p in s['peak_fits']:
        if p.get('bracketed') and p['dispersion']=='constant' and p['split'] in ['calibration','heldout']:
            groups[(p['response'],p['shape'],p['N'])].append(p)
    cases=[]
    for key,ps in groups.items():
        if key in done:continue
        p=max(ps,key=lambda p:p['zN'])
        for name in p['cases']:
            base=json.loads((HERE/(name+'.json')).read_text())
            if not base.get('complete'):continue
            c=dict(base['case']);last=max(c['zN']);c['id']+='_long';c['zN']=sorted(set(c['zN']+[round(last*f,8) for f in [1.25,1.5,2]]))
            c['design_note']='Length extension because no fully qualified plateau bracket was available. Same launch and numerical tolerance; original short run retained.'
            if not (HERE/(c['id']+'.json')).exists():cases.append(c)
    path=HERE/'length_extension_cases.json'
    old=json.loads(path.read_text()) if path.exists() else []
    combined={c['id']:c for c in old}
    for c in cases:
        if c['id'] in combined and combined[c['id']]!=c:raise RuntimeError('Changed extension case '+c['id'])
        combined[c['id']]=c
    path.write_text(json.dumps(list(combined.values()),indent=2)+'\n');print('Length extensions:',len(combined))
if __name__=='__main__':main()
