"""Dimensionless physical-regime ledger. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json,math

HERE=Path(__file__).resolve().parent
cal=json.loads((HERE/'physics_calibration.json').read_text())
tr=next(r['TR_quad_fs'] for r in cal['raman_quadrature'] if r['model']=='hc')
disp=cal['dispersion'];b=abs(disp['measured_beta2_ps2_km'])*1000
b3=disp['measured_beta3_ps3_km']*1e6;w0=2*math.pi*299.792458/1550
occ=json.loads((HERE/'physical_occupancy.json').read_text())['rows']
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',HC_first_moment_fs=tr,rows=[])
for N,T in [(3,130),(4,210),(6,375),(3,50),(8,600),(10,870)]:
    name=f'measured_hc_s1_N{N}_T{T}'
    path=HERE/(name+'.json')
    if not path.exists():continue
    r=json.loads(path.read_text());cp=next((p for p in r['checkpoints'] if p['zN']==4),None)
    if cp is None:continue
    p=cp['leading'];o=next((v for v in occ if v['case']==name and v['zN']==4),{})
    out['rows'].append(dict(case=name,N=N,T0_fs=T,zN=4,tau_R_HC=tr/T,
        x_HC=N*N*tr/T,y_using_BW_tau1=N*N*12.2/T,s=1/(w0*T),delta3=b3/(6*b*T),
        alpha_L=.2*math.log(10)/10/1000*cp['length_m'],local_beta2_ratio=p['local_beta2_ratio'],
        relative_carrier_redshift=1-p['local_gamma_ratio'],
        local_ZS_over_gate_minus_one=p['zs_window_ratio']-1,energy_nJ=p['energy_zs_nJ'],
        gate_energy_nJ=p['f_window']*cp['energy_launch_nJ'],**{k:v for k,v in o.items() if k not in ['case','zN']}))
(HERE/'regime_metrics.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2))
