"""Frozen resolution controls at nearest physical peak. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    data=json.loads((HERE/'analysis.json').read_text());out=[]
    for p in data['peaks']:
        if p['model']!='physical' or not p['bracketed']:continue
        row=next(x for x in data['rows'] if x['id']==p['best_sample'] and x['zN']==4)
        base=dict(row['case'])
        changes={'grid':{'n':base['n']*2},'window':{'n':base['n']*2,'width':base['width']*2},
                 'step':{'tol':base['tol']/16},'kernel':{'raman_sampling':'sampled_normalized'}}
        for name,change in changes.items():
            c=dict(base);c.update(change,id=f"control_{name}_N{p['N']}",control_reference=base['id'])
            if c['n']>32768:raise ValueError('control exceeds grid budget')
            out.append(c)
    base=next(c for c in json.loads((HERE/'cases.json').read_text()) if c['id']=='reference_N4_r1')
    for h in [4e-4,2e-4,1e-4,5e-5]:
        c=dict(base);c.update(id=f'control_fixed_h{h:g}',fixed_step=h,zN=[2.])
        out.append(c)
    out.append({'id':'control_library_matched','N':4,'T0_fs':200.,'n':8192,'width':96.,
                'tol':2e-9,'raman':'zblan','shape':'sech','dispersion':'tod','shock':True,
                'loss_db_km':50.,'zN':[2.],'fixed_step':1e-4,'solver_filter':True,
                'raman_sampling':'sampled_normalized','heldout':False})
    (HERE/'control_cases.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(out),'controls; commit before running')
if __name__=='__main__':main()
