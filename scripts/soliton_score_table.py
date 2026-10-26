#!/usr/bin/env python3
"""Assemble the required quartet and gap table from registered run evidence.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=Path('~/analytical-nl-discovery-data')
PREFIX='2026-10-10-gpt-b-soliton-'


def read(run,path):return json.loads((DATA/(PREFIX+run)/path).read_text())


def main():
    kerr=next(r for r in read('kerr','pilot/summary.json')['points'] if abs(r['z_over_LD']-3*np.pi/2)<1e-10)
    cases=[('Kerr fundamental, z/LD=3pi/2','kerr','pilot/summary.json',kerr,kerr['lambda_gen'],'exact Kerr restriction'),
        ('Raman fundamental, T0=0.25 ps, 300 K','solver','pilot_finest/batch.json',None,'pilot','finite output band'),
        ('Held out: T0=0.35 ps, 77 K','solver','held_out/batch.json',None,'held_out','finite output band'),
        ('Held out: T0=0.2 ps, 150 K','solver','held_out_second/batch.json',None,'second','finite output band'),
        ('Held out: T0=0.4 ps, 225 K, refined source','solver','held_out_third/batch.json',None,{'path':'quadratic_held_out_third.json','kind':'quadratic_cutoff'},'finite output band'),
        ('Gaussian N=1.25, Kerr+shock, z/LD=3','gaussian','gaussian_N1.25/batch.json',None,None,'finite output band'),
        ('Gaussian N=1.5, Kerr+shock, z/LD=4','gaussian','gaussian_N1.5/batch.json',None,None,'finite output band'),
        ('Gaussian N=1.25, Raman, z/LD=3','gaussian','gaussian_N1.25_Raman/batch.json',None,None,'finite output band'),
        ('Gaussian N=1.5, Kerr+shock, z/LD=8','gaussian','gaussian_N1.5_late/batch.json',None,None,'Ritz cells of width 0.08'),
        ('Notebook N=1.969 sech, Raman','anchor','native_50ps/batch_cells03.json',None,None,'Ritz cells of width 0.3'),
        ('Gaussian N=2, Raman fission, coarse cells','gaussian','gaussian_N2_Raman_fission/batch_cells03.json',None,None,'Ritz cells of width 0.3'),
        ('Gaussian N=2, Raman fission, finer cells','gaussian','gaussian_N2_Raman_fission/batch_cells015.json',None,None,'Ritz cells of width 0.15')]
    rows=[]
    for name,run,path,result,formula,scope in cases:
        if result is None:
            if not (DATA/(PREFIX+run)/path).exists():continue
            result=read(run,path)
        if isinstance(formula,str):
            mat=read('raman',f'material_{formula}_n256_w40.json')
            formula=next(r['lambda_gen'] for r in mat['points'] if r['source_model']=='linear_coth_cutoff')
        elif isinstance(formula,dict):
            mat=read('raman',formula['path'])
            formula=next(r['lambda_gen'] for r in mat['points'] if r['source_model']==formula['kind'])
        row=dict(case=name,run_id=PREFIX+run,source=path,readout_basis=scope,
            lambda_min=result['lambda_min'],lambda_pass=result['lambda_pass'],lambda_gen=result['lambda_gen'],
            best_binary_found=result['best_binary_found'],formula_lower_value=formula,
            formula_scope='Exact in the declared frozen soliton model; comparison to physical GNLSE is approximate.' if formula is not None else None)
        for key in ['lambda_min','lambda_pass','lambda_gen','best_binary_found']:
            row[key+'_dB']=float(10*np.log10(row[key]))
        for label,key in [('formula','formula_lower_value'),('gen','lambda_gen'),('min','lambda_min')]:
            row['gap_'+label+'_to_binary_dB']=float(10*np.log10(row['best_binary_found']/row[key])) if row[key] is not None else None
        rows.append(row)
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=rows,
        caveat='All eigenvalues are numerical approximations in their declared spaces. Coarse-cell Ritz minima are not lower enclosures for the whole field. Binary search is heuristic; every reported mask is achievable.')
    (DATA/(PREFIX+'solver')/'scored_cases.json').write_text(json.dumps(out,indent=2))
    lines=['---','agent: gpt-b','model: gpt-6-astra','family: gpt','---','',
        '# Scored soliton cases','',out['caveat'],'',
        'All four readout values and all gaps are in dB. Formula refers to the cutoff-source bound for Raman fundamentals and the exact Kerr restriction for the Kerr row. It has no asserted one-sided physical GNLSE remainder.','',
        '| Case | Field minimum | Passive | Amplitude | Best binary | Formula gap | Amplitude gap | Field gap | Run/source |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---|']
    for r in rows:
        values=[r[k] for k in ['lambda_min_dB','lambda_pass_dB','lambda_gen_dB','best_binary_found_dB','gap_formula_to_binary_dB','gap_gen_to_binary_dB','gap_min_to_binary_dB']]
        vals=['—' if v is None else f'{v:.5f}' for v in values]
        lines.append('| '+r['case']+' | '+' | '.join(vals)+' | `'+r['run_id']+'`, `'+r['source']+'` |')
    lines+=['','The notebook row uses 0.3-wide spectral cells, the fission rows use 0.3 and 0.15, and the late Gaussian row uses 0.08. Their quoted eigenvalue gaps are gaps in those restricted readout spaces. Native checks and finer temporal-grid values of their fixed masks are retained separately in the same runs. The third held-out formula uses the quadratic-coth source refinement; the first two use the original linear-coth cutoff.']
    (ROOT/'runs'/(PREFIX+'solver')/'scored_cases.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':main()
