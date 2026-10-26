"""Physical-model peak resolution controls. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'summary.json').read_text());cases=[]
    for n in [3,6]:
        peaks=[p for p in s['peak_fits'] if p.get('bracketed') and p['dispersion']=='measured' and p['zN']==4 and p['N']==n]
        if not peaks:continue
        p=peaks[0];base=json.loads((HERE/(p['cases'][1]+'.json')).read_text())['case']
        c=dict(base,id=base['id']+'_physical_fine',split='control',n=base['n']*2,base_case=base['id'],
            convergence_justification='Halved dt at the winning physical-model duration, selected by the frozen policy. Any grid above 32768 is only a convergence control.')
        cases.append(c)
    (HERE/'physical_control_cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    print('Physical convergence cases:',len(cases))

if __name__=='__main__':main()
