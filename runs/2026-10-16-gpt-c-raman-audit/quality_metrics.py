"""Compile numerical controls without discarding failures. gpt-c/gpt-6-astra/gpt."""
import json
from pathlib import Path
from independent import write_json

HERE=Path(__file__).resolve().parent
def read(name):
    p=HERE/(name+'.json')
    return json.loads(p.read_text()) if p.exists() else None
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',convergence=[],alias=[],shock_photon_comparison=[])
pairs=[]
for kind in ['wide','fine','tight']:
    pairs.append(('measured_hc_s1_N3_T80_fixed130cm',f'conv_{kind}_measured_N3_T80_fixed130cm','physical80_'+kind))
pairs.append(('bw_N6_T400','solver_window_N6_T400','exact_repository_window'))
pairs.append(('alias_N8_T400_n16384','solver_window_N8_T400_n16384','exact_repository_window_aliased_control'))
for N,T in [(12,1176),(16,1594),(16,1875),(16,2156)]:
    pairs.append((f'bw_N{N}_T{T}',f'conv_fine_N{N}_T{T}','large_N_grid'))
pairs.append(('bw_N8_T600','conv_wide_N8_T600','large_N_window'))
pairs.append(('measured_hc_s1_N3_T50_fixed130cm','conv_measured_wide_N3_T50_fixed130cm','fixed_length_window'))
pairs.append(('conv_smf_wide_N3_T25','conv_smf_fine_N3_T25_retry','physical_retry_resolution'))
pairs.append(('asym_N4_T6400','asym_fine_N4_T6400','weak_Raman_grid'))
pairs.append(('asym_N4_T6400','asym_wide_N4_T6400','weak_Raman_window'))
for N,T in [(3,25),(4,200),(6,400)]:
    for kind in ['fine','wide','step','halfstep','band']:
        pairs.append((f'bw_N{N}_T{T}',f'conv_{kind}_N{N}_T{T}',kind))
    pairs.append((f'conv_step_N{N}_T{T}',f'conv_halfstep_N{N}_T{T}','step_halving'))
for kind in ['fine','wide','tight']:
    pairs.append(('smf_hc_s1_N3_T25',f'conv_smf_{kind}_N3_T25',kind))
    for N,T in [(3,50),(4,200),(6,400)]:
        pairs.append((f'measured_hc_s1_N{N}_T{T}',f'conv_measured_{kind}_N{N}_T{T}',kind))
for base,test,kind in pairs:
    a,b=read(base),read(test)
    if a is None or b is None:continue
    for p in a['checkpoints']:
        q=next((x for x in b['checkpoints'] if x['zN']==p['zN']),None)
        if q is None or p['leading'] is None or q['leading'] is None:continue
        out['convergence'].append(dict(base=base,test=test,kind=kind,zN=p['zN'],
            fraction_difference=q['leading']['f_zs']-p['leading']['f_zs'],
            relative_fraction_difference=q['leading']['f_zs']/p['leading']['f_zs']-1,
            relative_gate_difference=q['leading']['f_window']/p['leading']['f_window']-1,
            max_spectral_edge_fraction=q['max_spectral_edge_fraction'],max_time_edge_fraction=q['max_time_edge_fraction']))
for p in sorted(HERE.glob('alias_*.json')):
    r=json.loads(p.read_text())
    if not isinstance(r,dict) or 'checkpoints' not in r:continue
    for cp in r['checkpoints']:
        out['alias'].append(dict(case=r['case']['id'],zN=cp['zN'],leading=cp['leading'],
             max_spectral_edge_fraction=cp['max_spectral_edge_fraction'],mass_drift=cp['mass_drift'],
             peak_count=len(cp['peaks']),
             brightest_peak=max(cp['peaks'],key=lambda p:p['peak_power_normalized']) if cp['peaks'] else None,
             brightest_is_leading=bool(cp['leading'] is not None and cp['peaks'] and max(cp['peaks'],key=lambda p:p['peak_power_normalized'])['index']==cp['leading']['index'])))
for N,T in [(3,100),(3,140),(4,200),(6,400)]:
    a,b=read(f'bw_N{N}_T{T}'),read(f'shock_bw_N{N}_T{T}')
    if a is None or b is None:continue
    for p in a['checkpoints']:
        q=next((x for x in b['checkpoints'] if x['zN']==p['zN']),None)
        if q is None or p['leading'] is None or q['leading'] is None:continue
        pa,qa=p['leading'],q['leading']
        photon_zs=qa['f_zs']/qa['local_gamma_ratio']
        out['shock_photon_comparison'].append(dict(N=N,T0_fs=T,zN=p['zN'],
            no_shock_f_zs=pa['f_zs'],shock_f_zs=qa['f_zs'],shock_photon_estimate=photon_zs,
            relative_photon_zs_difference=photon_zs/pa['f_zs']-1,
            relative_photon_gate_difference=qa['f_photon_window']/pa['f_window']-1))
write_json(HERE/'quality_metrics.json',out)
print('comparisons',len(out['convergence']),'alias',len(out['alias']),'photon',len(out['shock_photon_comparison']))
