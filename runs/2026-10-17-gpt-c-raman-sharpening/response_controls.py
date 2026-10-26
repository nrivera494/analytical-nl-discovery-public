"""Deterministic response/shape convergence controls. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'summary.json').read_text());cases=[]
    for response,shape in [('hc','sech'),('as2s3','sech'),('bw','gaussian')]:
        ps=[p for p in s['preferred_peaks'] if p['response']==response and p['shape']==shape and p['N']==16]
        if not ps:
            print('No accepted peak yet:',response,shape);continue
        p=ps[0];base=json.loads((HERE/(p['cases'][1]+'.json')).read_text())['case'];c=dict(base)
        c.update(id=base['id']+'_response_fine',split='control',n=base['n']*2,base_case=base['id'],
                 convergence_justification='Halved dt at the independently bracketed response/shape peak. Larger grid is used only for convergence.')
        cases.append(c)
        if response=='as2s3':
            wide=dict(base);wide.update(id=base['id']+'_response_wide',split='control',n=base['n']*2,width=base['width']*2,base_case=base['id'],
                convergence_justification='Doubled time window at unchanged dt after an observed late As-like N=16 boundary encounter. Larger grid is solely an artefact control.')
            cases.append(wide)
    (HERE/'response_control_cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    print('Response/shape convergence cases:',len(cases))
if __name__=='__main__':main()
