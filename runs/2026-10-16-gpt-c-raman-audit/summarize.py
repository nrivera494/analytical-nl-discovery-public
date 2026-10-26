"""Traceable audit tables from per-case outputs. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
import numpy as np
from independent import write_json
HERE=Path(__file__).resolve().parent
TR=.18*2*(1/32)/((1/32)**2+(1/12.2)**2)
allrows=[]
for path in sorted(HERE.glob('*.json')):
    r=json.loads(path.read_text())
    if not isinstance(r,dict) or 'case' not in r or 'checkpoints' not in r:continue
    c=r['case'];N=c['N'];T=c['T0_fs'];ist=(2*N-1)/N**2
    for cp in r['checkpoints']:
        lead=cp['leading']
        if lead is None:continue
        invalid=[]
        if cp['max_spectral_edge_fraction']>1e-6:invalid.append('spectral_edge')
        if cp['max_time_edge_fraction']>1e-6:invalid.append('temporal_edge')
        if not lead['zs']['success'] or lead['zs']['residual']>1e-8:invalid.append('ZS_root')
        if lead['zs_window_ratio']>1.05:invalid.append('ZS_exceeds_gate')
        if lead['boundary_intensity_ratio']>.02:invalid.append('overlapping_peak_gate')
        if lead['zs_window_ratio']<.90:invalid.append('substantial_nonsoliton_gate_content')
        alpha=c.get('loss_db_km',0)*np.log(10)/10/1000
        row=dict(case=c['id'],N=N,T0_fs=T,raman=c.get('raman','bw'),dispersion=c.get('dispersion','constant'),shock=c.get('shock',False),
           zN=cp['zN'],f1=lead['f_zs'],excess=lead['f_zs']/ist-1,cN=(lead['f_zs']/ist-1)/(TR/T),sqrtN_f1=np.sqrt(N)*lead['f_zs'],
           energy_nJ=lead['energy_zs_nJ'],energy_gate_nJ=lead['f_window']*cp['energy_launch_nJ'],lambda_nm=lead['lambda_nm'],
           f_window=lead['f_window'],width_fs=lead['width_fs'],local_beta2_ratio=lead['local_beta2_ratio'],
           local_gamma_ratio=lead['local_gamma_ratio'],photon_fraction_centroid_proxy=lead['f_zs']/lead['local_gamma_ratio'],
           max_spectral_edge_fraction=cp['max_spectral_edge_fraction'],max_time_edge_fraction=cp['max_time_edge_fraction'],
           mass_drift=cp['mass_drift'],photon_drift_loss_corrected=(1+cp['photon_drift'])*np.exp(alpha*cp['length_m'])-1,
           length_m=cp['length_m'],invalid=invalid,complete=r.get('complete',False))
        for k in ['f_photon_window','spectral_fraction_1200_2300nm','relative_dispersion_variation_one_rms']:
            if k in lead:row[k]=lead[k]
        allrows.append(row)
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',run_id=HERE.name,status='in-progress',rows=allrows)
out['reference_peaks']=[]
for N in [2,3,4,4.5,5,6,7,8,10,12,16]:
    rows=[r for r in allrows if r['case'].startswith('bw_') and r['N']==N and not r['invalid'] and r['zN']>=(2 if N>=10 else 3)]
    if not rows:continue
    byT={}
    for r in sorted(rows,key=lambda x:x['zN']):byT[r['T0_fs']]=r
    peak=max(byT.values(),key=lambda r:r['f1'])
    out['reference_peaks'].append(dict(peak,y=N*N*12.2/peak['T0_fs'],duration_count=len(byT),
        coverage='single candidate point; not a located maximum' if len(byT)==1 else 'maximum among sampled durations'))
out['long_pulse_exponents']=[]
for N in [2,4]:
    chosen=[]
    for T in [800,1600,3200,6400]:
        rows=[r for r in allrows if r['case'] in [f'asym_N{N}_T{T}',f'asym_wide_N{N}_T{T}'] and not r['invalid']]
        wide=[r for r in rows if r['case'].startswith('asym_wide_')]
        if wide:rows=wide
        if rows:
            rows=sorted(rows,key=lambda r:r['zN'])
            selected=dict(rows[-1]);selected['saturation_relative_change']=None
            if len(rows)>1 and rows[-2]['excess']>0:
                selected['saturation_relative_change']=abs(selected['excess']/rows[-2]['excess']-1)
            chosen.append(selected)
    if len(chosen)>1:
        tau=np.array([TR/r['T0_fs'] for r in chosen]);eps=np.array([r['excess'] for r in chosen])
        exponent=float(np.polyfit(np.log(tau),np.log(eps),1)[0]) if np.all(eps>0) else None
        local=(np.diff(np.log(eps))/np.diff(np.log(tau))).tolist() if np.all(eps>0) else []
        saturated=all(r['saturation_relative_change'] is not None and r['saturation_relative_change']<.05 for r in chosen)
        out['long_pulse_exponents'].append(dict(N=N,exponent=exponent,local=local,predicted=1,points=chosen,
            status='saturation_checked' if saturated else 'provisional: not all selected clean checkpoints demonstrate saturation'))
out['peak_fits_at_fixed_zN']=[]
for family in ['bw','constant_hc_s0','smf_hc_s1','measured_hc_s1']:
    for N in [2,3,4,4.5,5,6,7,8,10,12,16]:
        for zn in [3,4,8,16]:
            rows=[r for r in allrows if r['case'].startswith(family+'_') and r['N']==N and r['zN']==zn and not r['invalid']]
            byT={r['T0_fs']:r for r in rows}
            rows=sorted(byT.values(),key=lambda r:r['T0_fs'])
            if len(rows)<3:continue
            j=int(np.argmax([r['f1'] for r in rows]))
            if j==0 or j==len(rows)-1:continue
            nearby=rows[j-1:j+2]
            x=np.array([r['T0_fs'] for r in nearby]);y=np.array([r['f1'] for r in nearby])
            p=np.polyfit(x,y,2);xp=float(-p[1]/(2*p[0]));yp=float(np.polyval(p,xp))
            if p[0]>=0 or not x[0]<xp<x[-1]:continue
            out['peak_fits_at_fixed_zN'].append(dict(family=family,N=N,zN=zn,T0_fs=xp,f1=yp,
               sqrtN_f1=yp*np.sqrt(N),y=N*N*12.2/xp,bracket_fs=x.tolist(),cases=[r['case'] for r in nearby],
               energy_nJ=yp*2*N*N*(20099.330712163866 if family.startswith('measured') else 21700)/(.0013*xp)*1e-6,
               method='local three-point quadratic interpolation; bracket is resolution, not a confidence interval'))
duration_points=[]
for N,zn in [(2,16),(3,8),(4,4),(5,4),(6,4),(8,3)]:
    p=next((r for r in out['peak_fits_at_fixed_zN'] if r['family']=='bw' and r['N']==N and r['zN']==zn),None)
    if p is not None:duration_points.append(p)
if len(duration_points)>2:
    nx=np.array([r['N'] for r in duration_points]);tx=np.array([r['T0_fs'] for r in duration_points])
    fit=np.polyfit(np.log(nx),np.log(tx),1)
    out['reference_duration_scaling']=dict(points=duration_points,fit_exponent=float(fit[0]),
        fit_prefactor_fs=float(np.exp(fit[1])),predicted_exponent=1.62,
        relative_errors_against_21fs_N162=(tx/(21*nx**1.62)-1).tolist(),
        max_absolute_relative_error_against_21fs_N162=float(np.max(abs(tx/(21*nx**1.62)-1))))
out['energy_counterexample']=[r for r in allrows if r['N']==3 and r['T0_fs'] in [25,50,100,140] and r['zN']==4 and not r['invalid'] and (r['case'].startswith('bw_') or r['case'].startswith('measured_') or r['case'].startswith('smf_'))]
out['frozen_largeN_predictions']=[]
for name in sorted(set(r['case'] for r in allrows if r['N'] in [12,16])):
    rows=sorted([r for r in allrows if r['case']==name and not r['invalid']],key=lambda r:r['zN'])
    if not rows:continue
    selected=dict(rows[-1]);selected['predicted_interval']=[1.20,1.38]
    selected['inside_predicted_interval']=bool(1.20<=selected['sqrtN_f1']<=1.38)
    selected['saturation_relative_change']=abs(rows[-1]['excess']/rows[-2]['excess']-1) if len(rows)>1 and rows[-2]['excess']>0 else None
    out['frozen_largeN_predictions'].append(selected)
out['frozen_hc_predictions']=[]
for N in [3,4,6]:
    rows=[r for r in allrows if r['case'].startswith('constant_hc_s0_') and r['N']==N and r['zN']==4 and not r['invalid']]
    if rows:
        selected=dict(max(rows,key=lambda r:r['f1']));selected['predicted_interval']=[1.20,1.38]
        selected['inside_predicted_interval']=bool(1.20<=selected['sqrtN_f1']<=1.38)
        out['frozen_hc_predictions'].append(selected)
out['physical_share_peaks_at_fixed_zN']=[]
out['physical_photon_share_peaks_at_fixed_zN']=[]
for model in ['smf','measured']:
    for N in [3,4,6,8,10]:
        for zn in [2.5,3,4,6]:
            rows=[r for r in allrows if r['case'].startswith(model+'_hc_s1') and r['N']==N and r['zN']==zn and not r['invalid']]
            if rows:
                out['physical_share_peaks_at_fixed_zN'].append(max(rows,key=lambda r:r['f1']))
                out['physical_photon_share_peaks_at_fixed_zN'].append(max(rows,key=lambda r:r['photon_fraction_centroid_proxy']))
write_json(HERE/'summary.json',out)
print('cases',len(set(r['case'] for r in allrows)),'rows',len(allrows))
print('reference peaks',[(r['N'],r['T0_fs'],round(r['sqrtN_f1'],6)) for r in out['reference_peaks']])
print('exponents',[(r['N'],r['exponent'],r['local']) for r in out['long_pulse_exponents']])
print('physical peaks',[(r['dispersion'],r['N'],r['zN'],r['T0_fs'],round(r['energy_nJ'],5)) for r in out['physical_share_peaks_at_fixed_zN']])
