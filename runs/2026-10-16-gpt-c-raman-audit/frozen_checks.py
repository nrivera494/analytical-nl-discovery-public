"""Ledger of independently rerun frozen predictions. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json,math

HERE=Path(__file__).resolve().parent
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',rows=[])
def select(name):
    path=HERE/(name+'.json')
    if not path.exists():return None
    r=json.loads(path.read_text());c=r['case']
    ok=[p for p in r['checkpoints'] if p['leading'] is not None and
        max(p['max_spectral_edge_fraction'],p['max_time_edge_fraction'])<1e-6 and
        p['leading']['zs']['success'] and p['leading']['zs']['residual']<1e-8 and
        .9<p['leading']['zs_window_ratio']<1.05 and p['leading']['boundary_intensity_ratio']<.02]
    if not ok:return None
    p=ok[-1];f=p['leading']['f_zs'];N=c['N']
    return dict(case=name,N=N,T0_fs=c['T0_fs'],zN=p['zN'],f1=f,
                excess=f/((2*N-1)/N**2)-1,sqrtN_f1=math.sqrt(N)*f)
specs=[('bw_N5_T100','excess',[.30,.50]),('bw_N5_T200','excess',[.40,.62]),
       ('bw_N5_T280','excess',[.50,.75]),('bw_N7_T500','f1',[.46,.52]),
       ('bw_N8_T600','f1',[.43,.49]),('bw_N8_T800','f1',[.40,.50]),
       ('bw_N10_T870','sqrtN_f1',[1.20,1.38]),
       ('conv_fine_N12_T1176','sqrtN_f1',[1.20,1.38]),
       ('conv_fine_N16_T1875','sqrtN_f1',[1.20,1.38]),
       ('constant_hc_s0_N3_T140','sqrtN_f1',[1.20,1.38]),
       ('constant_hc_s0_N4_T200','sqrtN_f1',[1.20,1.38]),
       ('constant_hc_s0_N6_T400','sqrtN_f1',[1.20,1.38]),
       ('bw_N4.5_T240','sqrtN_f1',[1.20,1.38])]
for name,metric,interval in specs:
    r=select(name)
    if r is None:
        out['rows'].append(dict(case=name,status='no accepted checkpoint'));continue
    out['rows'].append(dict(r,metric=metric,interval=interval,
                           passes=interval[0]<=r[metric]<=interval[1]))
a,b,c=[select(f'bw_N5_T{T}') for T in [340,200,560]]
out['N5_ordering']=dict(points=[a,b,c],passes=a['f1']>b['f1'] and a['f1']>c['f1'])
r=select('rescale_bw_N4_T400_scale2');base=select('bw_N4_T200')
if r is not None:out['time_rescaling']=dict(rescaled=r,reference=base,fraction_difference=r['f1']-base['f1'])
(HERE/'frozen_checks.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2))
