"""Prioritized deterministic peak refinement. gpt-c / gpt-6-astra / gpt."""
import json,sys
from pathlib import Path
from make_cases import make
HERE=Path(__file__).resolve().parent

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'bw'
    s=json.loads((HERE/'summary.json').read_text());cases=[]
    if mode=='bw':
        peaks=[p for p in s['preferred_peaks'] if p['response']=='bw' and p['shape']=='sech' and p['split']=='calibration']
        priority=[3,8,16,4,6,10,5,7,12,14];peaks.sort(key=lambda p:priority.index(p['N']))
    elif mode=='bw_holdout':
        peaks=sorted([p for p in s['preferred_peaks'] if p['response']=='bw' and p['shape']=='sech' and p['split']=='heldout'],key=lambda p:p['N'])
    elif mode=='response':
        peaks=[p for p in s['preferred_peaks'] if p['dispersion']=='constant' and p['N'] in [3,16]
               and not(p['response']=='bw' and p['shape']=='sech')]
        peaks.sort(key=lambda p:(0 if p['N']==16 else 1,p['response'],p['shape']))
    elif mode=='physical':
        peaks=[p for p in s['peak_fits'] if p.get('bracketed') and p['dispersion']=='measured' and p['zN']==4]
    else:raise ValueError(mode)
    for p in peaks:
        a,b=p['T_bracket_fs'];center=p['sample_T0_fs']
        for T in [round((a+center)/2,3),round((b+center)/2,3)]:
            if mode=='physical':
                c=make(p['N'],T,'hc',split='physical',suffix='_smf',dispersion='measured',shock=True,loss_db_km=.2)
                c['zN']=[3,4,5]
            else:c=make(p['N'],T,p['response'],p['shape'],p['split'])
            c['design_note']='Midpoints of the frozen-policy three-sample local bracket; no training coefficient is refitted.'
            if not (HERE/(c['id']+'.json')).exists():cases.append(c)
    (HERE/(mode+'_refinement_cases.json')).write_text(json.dumps(cases,indent=2)+'\n')
    print(mode,'refinement cases',len(cases))
if __name__=='__main__':main()
