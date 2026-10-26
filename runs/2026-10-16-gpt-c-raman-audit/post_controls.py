"""Summarize controls completed after the independent verdict. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
TR=.18*2*(1/32)/((1/32)**2+(1/12.2)**2)
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',
         independent_verdict_commit='143cc58cd167f32b4edc88b7f007d23ab2dd641c',
         alias=[],weak_Raman=[],edges=[],fixed_length=[],compression=[],physical80_controls=[])
def read(name):
    p=HERE/(name+'.json')
    return json.loads(p.read_text()) if p.exists() else None
def point(case,cp):
    p=cp.get('leading');N=case['N'];T=case['T0_fs'];f0=(2*N-1)/N**2
    flags=[]
    if cp['max_time_edge_fraction']>1e-6:flags.append('temporal_edge')
    if cp['max_spectral_edge_fraction']>1e-6:flags.append('spectral_edge')
    if p is None:flags.append('no_leading_pulse')
    else:
        if not p['zs']['success'] or p['zs']['residual']>1e-8:flags.append('ZS_root')
        if p['boundary_intensity_ratio']>.02:flags.append('overlapping_peak_gate')
        if not .9<p['zs_window_ratio']<1.05:flags.append('ZS_gate_disagreement')
    return dict(case=case['id'],N=N,T0_fs=T,zN=cp['zN'],length_m=cp['length_m'],
        diagnostic_flags=flags,
        fraction=p['f_zs'] if p else None,
        energy_nJ=p['energy_zs_nJ'] if p else None,
        gated_energy_nJ=p['f_window']*cp['energy_launch_nJ'] if p else None,
        excess=p['f_zs']/f0-1 if p else None,
        cN=(p['f_zs']/f0-1)*T/TR if p else None,
        max_time_edge=cp['max_time_edge_fraction'],max_frequency_edge=cp['max_spectral_edge_fraction'],
        mass_drift=cp['mass_drift'],
        global_fraction_1200_2300=cp.get('global_spectral_fraction_1200_2300nm'),
        leading_fraction_1200_2300=p.get('spectral_fraction_1200_2300nm') if p else None,
        zs_gate_ratio=p['zs_window_ratio'] if p else None)
for p in sorted(HERE.glob('alias_N8*.json')):
    r=json.loads(p.read_text())
    out['alias'] += [point(r['case'],cp) for cp in r['checkpoints']]
for name in ['asym_N4_T6400','asym_wide_N4_T6400','asym_fine_N4_T6400']:
    r=read(name)
    if r:out['weak_Raman'] += [point(r['case'],cp) for cp in r['checkpoints']]
for p in sorted(HERE.glob('edge_N*.json')):
    r=json.loads(p.read_text())
    out['edges'] += [point(r['case'],cp) for cp in r['checkpoints']]
for T in [50,80,100,140]:
    r=read(f'measured_hc_s1_N3_T{T}_fixed130cm')
    if r:out['fixed_length'] += [point(r['case'],cp) for cp in r['checkpoints']]
for kind in ['wide','fine','tight']:
    r=read(f'conv_{kind}_measured_N3_T80_fixed130cm')
    if r:out['physical80_controls'] += [point(r['case'],cp) for cp in r['checkpoints']]
r=read('compression_check')
if r:
    for x in r['rows']:
        a=x.get('first_compression');b=x.get('fine_compression')
        out['compression'].append(dict(N=x['N'],coarse=a,fine=b,
            predicted_amplitude_N_squared=x['N']**2,
            amplitude_ratio_to_prediction=b['peak_amplitude']/x['N']**2 if b else None))
(HERE/'post_controls.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['alias','edges','fixed_length']},indent=2))
