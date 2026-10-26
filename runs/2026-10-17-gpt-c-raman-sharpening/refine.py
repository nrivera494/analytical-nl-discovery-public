"""Deterministic peak refinement, never retunes predictions. gpt-c / gpt-6-astra / gpt."""
import json,sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from make_cases import make
HERE=Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'summary.json').read_text());split=sys.argv[1] if len(sys.argv)>1 else 'calibration'
    rows=[r for r in s['rows'] if r['split']==split and r['dispersion']=='constant'];gs=defaultdict(list)
    for r in rows:gs[(r['response'],r['shape'],r['N'])].append(r)
    new=[]
    for key,rs in gs.items():
        peaks=[p for p in s['preferred_peaks'] if (p['response'],p['shape'],p['N'])==key and p['split']==split]
        Ts=sorted(set(r['T0_fs'] for r in rs));present=set(Ts)
        if peaks:
            p=peaks[0];a,b=p['T_bracket_fs'];center=p['sample_T0_fs']
            targets=[(a+center)/2,(b+center)/2]
        else:
            valid=[r for r in rs if not r['invalid'] and r['plateau_relative_change'] is not None and r['plateau_relative_change']<.005]
            if not valid:
                print('UNRESOLVED',key,'no plateau');continue
            best=max(valid,key=lambda r:r['f1'])
            if best['T0_fs']==Ts[0]:targets=[Ts[0]/1.3,Ts[0]/1.3**2]
            elif best['T0_fs']==Ts[-1]:targets=[Ts[-1]*1.3,Ts[-1]*1.3**2]
            else:
                print('UNRESOLVED',key,'interior points require common-length/quality control');continue
        for T in targets:
            T=round(T,3)
            if T in present:continue
            c=make(key[2],T,key[0],key[1],split)
            c['design_note']='Deterministic local bracket midpoint or geometric edge extension under original frozen policy.'
            new.append(c)
    out=HERE/(sys.argv[2] if len(sys.argv)>2 else split+'_refinement_cases.json')
    out.write_text(json.dumps(new,indent=2)+'\n');print(out.name,len(new))
if __name__=='__main__':main()
