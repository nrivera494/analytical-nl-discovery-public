#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt. Derived audit tables."""
import json
from pathlib import Path

folder=Path(__file__).resolve().parent
data=json.loads((folder/'summary.json').read_text())
lines=['<!-- agent: gpt-a; model: gpt-6-astra; family: gpt -->',
       '# Independent audit data tables',
       '', 'Source run: `2026-10-16-gpt-a-dw-analysis`; underlying run ids are in its config.', '']

def table(headers,rows):
    lines.append('| '+' | '.join(headers)+' |')
    lines.append('|'+'|'.join(['---']*len(headers))+'|')
    lines.extend('| '+' | '.join(map(str,row))+' |' for row in rows)
    lines.append('')

lines.extend(['## Core and held-out law tests','',
    'The three-parameter diagnostic fits c, p, d. The strip is independently computed.', ''])
rows=[]
for name,v in list(data['core'].items())+list(data['heldout'].items()):
    ds=v.get('exact_dstar',v.get('dstar'));f=v['free_fit'];e=v['local_error_scaling']
    rows.append([name,f'{ds:.8f}',f"{f['d']:.8f}",f"{100*(f['d']/ds-1):+.3f}%",
        f"{f['p']:.4f}",f"{e['measured_exponent']:.4f}",f"{f['log_rms']:.3g}"])
table(['Case','Independent d*','Fitted d','Relative error','Fitted p','Slope-error power (prediction 1)','Fit log RMS'],rows)
if data['frozen_p5']['status']=='complete':
    p5=data['frozen_p5']
    lines.extend(['Exact frozen P5 abscissae (source run `2026-10-16-gpt-a-dw-followup`):', ''])
    table(['Independent d*','Fitted d','Relative error','Change from xi=2','Slope-error power'],[[
        f"{p5['dstar']:.9f}",f"{p5['free_fit']['d']:.9f}",f"{100*p5['relative_error']:+.4f}%",
        f"{100*p5['relative_to_length2']:+.4f}%",f"{p5['local_error_scaling']['measured_exponent']:.4f}"]])

lines.extend(['## Roy full model','',
    'Peak ratios use the input spectral maximum. Eq. 6 is parameter free. The fixed-strip curve fits only p,c on delta3=0.010,0.012,0.014. Integrated yields use the isolated resonant band.', ''])
for label,v in data['roy'].items():
    lines.extend(['### '+label,'',f"Independent strip: {v['dstar']:.9f}.",''])
    table(['delta3','Simulation peak dB','Fig. 3b dB','Eq. 6 dB','Strip prediction dB','Energy fraction','Photon fraction'],[
        [f"{r['delta3']:.3f}",f"{r['peak_db']:.3f}",'—' if r['figure_db'] is None else f"{r['figure_db']:.3f}",
         f"{r['eq6_db']:.3f}",f"{r['strip_peak_db']:.3f}",f"{r['eta_resonant']:.6g}",f"{r['eta_photon_resonant']:.6g}"] for r in v['rows']])
    table(['Range','Fixed-strip peak RMSE dB','Eq. 6 peak RMSE dB'],[
        [k,f"{g['strip_peak_rmse_db']:.5f}",f"{g['eq6_peak_rmse_db']:.5f}"] for k,g in v['groups'].items()])

lines.extend(['## Long-fibre attack',''])
table(['Length','Fitted d','Error from exact d*','Fitted p','Slope-error power'],[
    [k,f"{v['free_fit']['d']:.9f}",f"{100*(v['free_fit']['d']/v['dstar']-1):+.3f}%",
     f"{v['free_fit']['p']:.4f}",f"{v['local_error_scaling']['measured_exponent']:.4f}"]
    for k,v in data['length'].items() if k.startswith('xi_')])

numeric=folder/'numerics.json'
lines.extend(['## Finite-yield collapse attack',''])
table(['Case','Actual x','Predicted fraction','Band fraction','Log error','Tolerance'],[
    [r['case'],'pending' if r['actual_x'] is None else f"{r['actual_x']:.5f}",
     f"{r['frozen_prediction']:.5f}",f"{r['eta_band']:.7f}",f"{r['log_error']:+.5f}",r['frozen_log_tolerance']]
    for r in data['collapse']['rows']])
if numeric.exists():
    n=json.loads(numeric.read_text())
    lines.extend(['## Numerical convergence',''])
    table(['Variant','Gate-15 relative change','Gate-20 relative change','Peak change dB','dt fs'],[
        [r['variant'],f"{r['relative_gate15']:+.6g}",f"{r['relative_gate20']:+.6g}",
         '—' if r['peak_delta_db'] is None else f"{r['peak_delta_db']:+.6g}",f"{r['dt_fs']:.6g}"] for r in n['convergence']])

(folder/'tables.md').write_text('\n'.join(lines)+'\n')
