"""Audit tables and scored predictions. gpt-c / gpt-6-astra / gpt."""
import json,math
from pathlib import Path
import numpy as np
from independent import write_json,shape_integral,W0,GAMMA,carrier_beta2
from analyze import peakfit
HERE=Path(__file__).resolve().parent
IDENT={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt'}

def main():
    s=json.loads((HERE/'summary.json').read_text());peaks=s['preferred_peaks'];over=json.loads((HERE/'overlap.json').read_text()) if (HERE/'overlap.json').exists() else {'rows':[]}
    acc=json.loads((HERE/'accuracy.json').read_text()) if (HERE/'accuracy.json').exists() else {'grid_window_tolerance':[]}
    rmax={r['response']:r['overlap_max_width_fs'] for r in over['rows'] if r['time_scale']==1}
    # Conservative numerical envelope from controlled peak-adjacent runs, plus
    # interpolation and output-checkpoint sensitivity. Not a probabilistic CI.
    conv=max([abs(r['scaled_share_difference']) for r in acc['grid_window_tolerance']+acc.get('response_specific',[]) if r['max_edge']<1e-6]+[0.0002])
    reference=[]
    for p in peaks:
        if p['dispersion']!='constant' or p['shock'] or p['split']=='matched_shape':continue
        q=dict(p)
        prior=[v for v in s['peak_fits'] if v.get('bracketed') and (v['N'],v['response'],v['shape'],v['dispersion'],v['shock'])==(p['N'],p['response'],p['shape'],p['dispersion'],p['shock']) and v.get('plateau_complete',False) and v['max_plateau_relative_change']<=.005]
        spread=max([abs(v['scaled_share']-p['scaled_share']) for v in prior]+[0])
        q['scaled_share_resolution_envelope']=conv+spread+np.sqrt(p['N'])*max(p['interpolation_share_difference'],abs(p['f1']-p['sample_f1']))
        q['peak_position_half_bracket_fs']=(p['T_bracket_fs'][1]-p['T_bracket_fs'][0])/2
        width_numerical=max([abs(r['fit_width_difference_fs']) for r in acc['grid_window_tolerance'] if r['max_edge']<1e-6]+[.02])
        width_numerical=max([abs(r['relative_fit_width_change'])*p['fit_width_fs'] for r in acc.get('response_specific',[]) if r['max_edge']<1e-6]+[width_numerical])
        for kind in ['fit','area']:
            spread_w=max([abs(v[kind+'_width_fs']-p[kind+'_width_fs']) for v in prior]+[0])
            values=[v[kind+'_width_fs'] for v in p['bracket_values']]
            q[kind+'_width_resolution_interval_fs']=[min(values)-spread_w-width_numerical,max(values)+spread_w+width_numerical]
        if p['response'] in rmax:
            q['overlap_max_width_fs']=rmax[p['response']]
            fr=next(r['fR'] for r in over['rows'] if r['response']==p['response'] and r['time_scale']==1)
            q['electronic_area_width_fs']=p['area_width_fs']/(1-fr)
            q['electronic_area_overlap_ratio']=q['electronic_area_width_fs']/rmax[p['response']]
            for kind in ['fit','area','fwhm']:
                q[kind+'_overlap_ratio']=p[kind+'_width_fs']/rmax[p['response']]
                q[kind+'_selection_pass_15pct']=abs(q[kind+'_overlap_ratio']-1)<=.15
                if kind in ['fit','area']:
                    interval=q[kind+'_width_resolution_interval_fs']
                    q[kind+'_selection_15pct_excluded_by_resolution_interval']=interval[0]>1.15*rmax[p['response']] or interval[1]<.85*rmax[p['response']]
        reference.append(q)
    bw={p['N']:p for p in reference if p['response']=='bw' and p['shape']=='sech'}
    compares=[]
    for p in reference:
        if p['N'] not in bw or (p['response']=='bw' and p['shape']=='sech'):continue
        b=bw[p['N']]
        compares.append(dict(N=p['N'],response=p['response'],shape=p['shape'],
                share_relative_change=p['f1']/b['f1']-1,
                normalized_leading_energy_relative_change=shape_integral(p['shape'])*p['f1']/(2*b['f1'])-1,
                physical_eff_energy_relative_change=shape_integral(p['shape'])*p['f1']*b['T0_fs']/(2*b['f1']*p['T0_fs'])-1,
                duration_ratio=p['T0_fs']/b['T0_fs']))
        ap,ab=p['scaled_share'],b['scaled_share'];ep=p['scaled_share_resolution_envelope'];eb=b['scaled_share_resolution_envelope']
        lo=(ap-ep)/(ab+eb);hi=(ap+ep)/(ab-eb)
        compares[-1]['share_relative_change_resolution_interval']=[lo-1,hi-1]
        factor=shape_integral(p['shape'])/2
        compares[-1]['normalized_energy_relative_change_resolution_interval']=[factor*lo-1,factor*hi-1]
        compares[-1]['duration_ratio_bracket_interval']=[p['T_bracket_fs'][0]/b['T_bracket_fs'][1],p['T_bracket_fs'][1]/b['T_bracket_fs'][0]]
        compares[-1]['split']=p['split']
        if p['shape']=='sech' and p['response'] in ['hc','as2s3']:
            compares[-1]['frozen_response_8pct_pass']=abs(compares[-1]['share_relative_change'])<=.08
            compares[-1]['original_4pct_extension_pass']=abs(compares[-1]['share_relative_change'])<=.04
        if p['shape']=='gaussian':
            compares[-1]['frozen_normalized_energy_6pct_pass']=bool(abs(compares[-1]['normalized_leading_energy_relative_change'])<=.06)
            if p['N'] in [4,6]:
                tol={4:.04,6:.025}[p['N']]
                compares[-1]['original_shape_tolerance']=tol
                compares[-1]['original_shape_prediction_pass']=bool(abs(compares[-1]['normalized_leading_energy_relative_change'])<=tol)
    physical=[p for p in s['peak_fits'] if p.get('bracketed') and p['dispersion']=='measured' and p['zN']==4]
    for p in physical:
        # Exact constant-N launch normalization at the interpolated optimum.
        sample=next(r for r in s['rows'] if r['case']==p['cases'][1] and r['zN']==4)
        ein=sample['launch_energy_nJ']*sample['T0_fs']/p['T0_fs']
        p['launch_energy_nJ']=ein;p['energy_nJ']=p['f1']*ein;p['gate_energy_nJ']=p['f_gate']*ein
        p['efficient_energy_interval_test_pass']=1.35<=p['energy_nJ']<=1.55
        ef=conv/np.sqrt(p['N'])+max(p['interpolation_share_difference'],abs(p['f1']-p['sample_f1']))
        lo,hi=p['T_bracket_fs'];constant=ein*p['T0_fs']
        p['energy_resolution_interval_nJ']=[constant/hi*(p['f1']-ef),constant/lo*(p['f1']+ef)]
        p['efficient_energy_prediction_resolved_with_full_bracket']=bool(p['energy_resolution_interval_nJ'][0]>=1.35 and p['energy_resolution_interval_nJ'][1]<=1.55)
        p['s']=1/(W0*p['T0_fs']);p['delta3']=.12466969933575454e6/(6*carrier_beta2('measured')*p['T0_fs'])
        p['alpha_L']=.2*np.log(10)/10/1000*p['length_m']
        p['tau_R']=next((r['first_moment_fs'] for r in over['rows'] if r['response']=='hc'),2.463955525270499)/p['T0_fs']
        p['peak_power_kW']=500*ein/p['T0_fs']
        p['input_intensity_FWHM_fs']=2*np.arccosh(np.sqrt(2))*p['T0_fs']
        p['input_photons']=ein*1e-9/(1.054571817e-34*W0*1e15)*p['launch_photon_energy_equivalent_ratio']
        p['leading_photons']=p['photon_fraction']*p['input_photons']
    matched=[]
    k=np.arccosh(np.sqrt(2))/np.sqrt(np.log(2));g=np.sqrt(2*k/np.sqrt(np.pi))
    for p in peaks:
        if p['split']!='matched_shape':continue
        ns=int(round(p['N']/g));b=bw.get(ns)
        if b is not None:
            matched.append(dict(reference_sech_N=ns,gaussian_peak_N=p['N'],gaussian_T0_fs=p['T0_fs'],equivalent_sech_T0_fs=p['T0_fs']/k,
                gaussian_share=p['f1'],sech_share=b['f1'],share_gain=p['f1']/b['f1']-1,predicted_gain_interval=[.03,.13],
                prediction_pass=.03<=p['f1']/b['f1']-1<=.13,T_bracket_gaussian_fs=p['T_bracket_fs'],cases=p['cases']))
            rr=sorted([r for r in s['rows'] if r['split']=='matched_shape' and r['N']==p['N'] and r['zN']==p['zN'] and not r['invalid']],key=lambda r:r['T0_fs'])
            target=k*b['T0_fs']
            if rr and rr[0]['T0_fs']<=target<=rr[-1]['T0_fs']:
                fg=float(np.interp(target,[r['T0_fs'] for r in rr],[r['f1'] for r in rr]))
                matched[-1]['pointwise_at_sech_optimum']={'gaussian_T0_fs':target,'gaussian_share_linear_interpolation':fg,
                    'sech_share':b['f1'],'share_gain':fg/b['f1']-1,
                    'note':'Same launch energy, intensity FWHM and physical length at this point. Separate family optima above do not have equal launch energies.'}
    physical_alternative=[]
    for n in [3,4,6]:
        vals=[r for r in s['rows'] if r['split']=='physical' and r['N']==n and r['zN']==4 and not r['invalid']]
        if len(vals)<3:continue
        for observable in ['f_gate','photon_fraction']:
            modified=[dict(r,f1=r[observable],scaled_share=np.sqrt(n)*r[observable]) for r in vals]
            p=peakfit(modified);p['objective']=observable
            if p.get('bracketed'):
                T=p['T0_fs'];ein=vals[0]['launch_energy_nJ']*vals[0]['T0_fs']/T
                p['launch_energy_nJ']=ein;p['objective_value']=p['f1'];p['energy_nJ']=p['f_gate']*ein
                p['s']=1/(W0*T);p['delta3']=.12466969933575454e6/(6*carrier_beta2('measured')*T)
                p['alpha_L']=.2*np.log(10)/10/1000*p['length_m']
                p['tau_R']=next((r['first_moment_fs'] for r in over['rows'] if r['response']=='hc'),2.463955525270499)/T
                if observable=='f_gate':
                    p['energy_nJ']=p['objective_value']*ein
                    p['efficient_energy_interval_test_pass']=1.35<=p['energy_nJ']<=1.55
                    p['input_photons']=ein*1e-9/(1.054571817e-34*W0*1e15)*p['launch_photon_energy_equivalent_ratio']
                    p['leading_photons']=p['photon_fraction']*p['input_photons']
            physical_alternative.append(p)
    constrained=[r for r in s['rows'] if r['split']=='constrained' and not r['invalid']]
    for r in constrained:
        r['peak_power_kW']=500*r['launch_energy_nJ']/r['T0_fs']
        r['input_photons']=r['launch_energy_nJ']*1e-9/(1.054571817e-34*W0*1e15)*r['launch_photon_energy_equivalent_ratio']
        r['leading_photons']=r['photon_fraction']*r['input_photons']
    constrained_best=max(constrained,key=lambda r:r['energy_nJ']) if constrained else None
    hold=[]
    if (HERE/'training_fit.json').exists():
        fit=json.loads((HERE/'training_fit.json').read_text())
        for h in fit['holdout_predictions']:
            if h['N'] not in bw:continue
            p=bw[h['N']]
            hold.append(dict(N=p['N'],predicted_scaled_share=h['scaled_share'],observed_scaled_share=p['scaled_share'],
                scaled_share_error=p['scaled_share']-h['scaled_share'],share_pass=abs(p['scaled_share']-h['scaled_share'])<=h['scaled_share_absolute_tolerance'],
                predicted_T0_fs=h['T0_fs'],observed_T0_fs=p['T0_fs'],position_relative_error=p['T0_fs']/h['T0_fs']-1,
                position_pass=abs(p['T0_fs']/h['T0_fs']-1)<=h['T0_relative_tolerance']))
            hold[-1]['share_prediction_resolved_with_resolution_envelope']=bool(abs(p['scaled_share']-h['scaled_share'])+p['scaled_share_resolution_envelope']<=h['scaled_share_absolute_tolerance'])
            hold[-1]['position_prediction_resolved_with_full_bracket']=bool(p['T_bracket_fs'][0]>=h['T0_fs']*(1-h['T0_relative_tolerance']) and p['T_bracket_fs'][1]<=h['T0_fs']*(1+h['T0_relative_tolerance']))
            hold[-1]['T_bracket_fs']=p['T_bracket_fs']
            original=21*p['N']**1.62
            hold[-1]['original_10pct_position_prediction_resolved_with_full_bracket']=bool(p['T_bracket_fs'][0]>=.9*original and p['T_bracket_fs'][1]<=1.1*original)
    out=dict(IDENT,run_id=HERE.name,status=s['status'],reference_peaks=reference,response_shape_comparisons=compares,physical_share_optima=physical,
             matched_shape_comparisons=matched,physical_alternative_optima=physical_alternative,constrained_scan=constrained,constrained_best_sample=constrained_best,constrained_best_gate_sample=max(constrained,key=lambda r:r['gate_energy_nJ']) if constrained else None,holdout_scores=hold,
             numerical_scaled_share_envelope=conv,overlap=over['rows'],number_of_cases=len(set(r['case'] for r in s['rows'])),
             number_of_invalid_checkpoints=sum(bool(r['invalid']) for r in s['rows']),
             excluded_checkpoints=[dict(case=r['case'],zN=r['zN'],reasons=r['invalid']) for r in s['rows'] if r['invalid']])
    out['physical_model']={'carrier_wavelength_nm':1550,'beta2_ps2_per_km':-carrier_beta2('measured')/1000,
        'beta3_ps3_per_km':.12466969933575454,'gamma_per_W_km':1000*GAMMA,'loss_dB_per_km':.2,
        'response':'13-mode Hollenbeck-Cantrell','raman_fraction':.18,'shock':True,
        'dispersion_note':'Full published Boilard SMF-28 fit is propagated; beta2 and beta3 are carrier derivatives, not a truncated propagation model.',
        'source_DOI':'10.1038/s41598-022-08329-3','source_access':'full text in prior independent audit',
        'limitations':['uniform loss','constant mode area','not a calibration of a particular spool']}
    small=[p for p in reference if p['response']=='bw' and p['shape']=='sech' and 3<=p['N']<=10]
    if small:
        out['small_order_constant_summary']={'orders':[p['N'] for p in sorted(small,key=lambda p:p['N'])],
            'coefficient':1.29,'scaled_share_envelope':[min(p['scaled_share']-p['scaled_share_resolution_envelope'] for p in small),max(p['scaled_share']+p['scaled_share_resolution_envelope'] for p in small)],
            'maximum_relative_deviation_including_numerical_envelope':max((abs(p['scaled_share']-1.29)+p['scaled_share_resolution_envelope'])/1.29 for p in small),
            'scope':'Finite sampled orders and declared output checkpoints; numerical envelope, not a proved physical remainder.'}
    def bounds(vals):
        return [float(min(vals)),float(max(vals))] if vals else None
    accepted=[r for r in s['rows'] if not r['invalid'] and r['split'] in ['calibration','heldout','physical','constrained','matched_shape']]
    out['accepted_diagnostic_bounds']={key:bounds([r[key] for r in accepted if r[key] is not None]) for key in
        ['dt_fs','max_time_edge_fraction','max_spectral_edge_fraction','mass_drift','photon_drift','local_beta2_ratio','local_gamma_ratio','relative_dispersion_variation_one_rms']}
    out['reference_peak_regimes']=[]
    for response in ['bw','hc','as2s3','bw_damped']:
        for shape in ['sech','gaussian']:
            ps=[p for p in reference if p['response']==response and p['shape']==shape]
            if not ps:continue
            tr=next((r['first_moment_fs'] for r in over['rows'] if r['response']==response and r['time_scale']==1),None)
            out['reference_peak_regimes'].append(dict(response=response,shape=shape,
                N=bounds([p['N'] for p in ps]),T0_fs=bounds([p['T0_fs'] for p in ps]),y=bounds([p['y'] for p in ps]),
                zN=bounds([p['zN'] for p in ps]),tau_R=bounds([tr/p['T0_fs'] for p in ps]) if tr else None))
    out['original_and_frozen_peak_scores']=[]
    for p in reference:
        if p['shape']!='sech':continue
        q=dict(N=p['N'],response=p['response'],split=p['split'],scaled_share=p['scaled_share'],T0_fs=p['T0_fs'])
        if p['response']=='bw':
            q.update(broad_scaled_share_pass=1.20<=p['scaled_share']<=1.38,
                     original_constant_3pct_pass=abs(p['scaled_share']/1.29-1)<=.03,
                     original_position_relative_error=p['T0_fs']/(21*p['N']**1.62)-1,
                     original_position_10pct_pass=abs(p['T0_fs']/(21*p['N']**1.62)-1)<=.10,
                     original_position_10pct_full_bracket_pass=bool(p['T_bracket_fs'][0]>=.9*21*p['N']**1.62 and p['T_bracket_fs'][1]<=1.1*21*p['N']**1.62))
        elif p['response'] in ['as2s3','bw_damped']:
            tau=15.5 if p['response']=='as2s3' else 12.2
            q.update(single_oscillator_position_relative_error=p['T0_fs']/(1.7*tau*p['N']**1.62)-1,
                     single_oscillator_position_20pct_pass=abs(p['T0_fs']/(1.7*tau*p['N']**1.62)-1)<=.20)
        out['original_and_frozen_peak_scores'].append(q)
    write_json(HERE/'final_metrics.json',out)
    print('Reference peaks:',len(reference),'Physical:',len(physical),'Holdouts:',len(hold),'Convergence envelope:',conv)
    for p in sorted([v for v in reference if v['response']=='bw' and v['shape']=='sech'],key=lambda v:v['N']):
        print(p['N'],p['T0_fs'],p['scaled_share'],p['scaled_share_resolution_envelope'])
if __name__=='__main__':main()
