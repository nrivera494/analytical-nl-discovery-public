"""Reproducible audit tables. gpt-c / gpt-6-astra / gpt."""
import json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent

def table(lines,head,rows):
    lines.extend(['','| '+' | '.join(head)+' |','|'+'|'.join(['---']*len(head))+'|'])
    lines.extend('| '+' | '.join(str(v) for v in row)+' |' for row in rows)

def main():
    m=json.loads((HERE/'final_metrics.json').read_text())
    lines=['---','agent: gpt-c','model: gpt-6-astra','family: gpt','run_id: '+HERE.name,'---','',
      '# Numerical tables','',f'All numerical entries are from run `{HERE.name}`. Resolution intervals are numerical sensitivity estimates, not statistical confidence intervals. Peaks are bracketed local duration peaks at the stated output checkpoint.','',
      '## Blow–Wood, sech launch']
    bw=sorted([p for p in m['reference_peaks'] if p['response']=='bw' and p['shape']=='sech'],key=lambda p:p['N'])
    table(lines,['N','T0* (fs)','Neighbor bracket (fs)','a = f1* sqrt(N) ± resolution','f1*','y*','zN','Split'],[
       [p['N'],f"{p['T0_fs']:.2f}",f"[{p['T_bracket_fs'][0]:.2f}, {p['T_bracket_fs'][1]:.2f}]",
        f"{p['scaled_share']:.5f} ± {math.ceil(p['scaled_share_resolution_envelope']*1e5)/1e5:.5f}",f"{p['f1']:.6f}",f"{p['y']:.4f}",f"{p['zN']:g}",p['split']] for p in bw])
    pos_path=HERE/'final_position.json'
    if pos_path.exists():
        pos=json.loads(pos_path.read_text())
        lines+=['','## Descriptive position fits by response and shape','',
          'T0* / tau_ref = A N^p, or y* = N^(2-p) / A. All fits here describe the completed data; only training_fit.json supplies the frozen predictive coefficients. Regression intervals use residuals; full-bracket intervals independently vary every peak over its complete neighboring-duration bracket. Neither is a material-parameter confidence interval or a physical asymptotic remainder. HC uses tau_ref = 12.2 fs.']
        table(lines,['Response / shape','N values','A','A residual 95% interval','p','p residual 95% interval','p full-bracket sensitivity','y exponent 2-p','Constant y compatible with all brackets'],[
          [p['response']+' / '+p['shape'],','.join(f'{n:g}' for n in p['N']),f"{p['prefactor_tau1']:.5f}",
           f"[{p['prefactor_OLS_95_interval'][0]:.5f}, {p['prefactor_OLS_95_interval'][1]:.5f}]",f"{p['exponent']:.5f}",
           f"[{p['exponent_OLS_95_interval'][0]:.5f}, {p['exponent_OLS_95_interval'][1]:.5f}]",
           f"[{p['peak_bracket_full_corner_sensitivity'][0]:.5f}, {p['peak_bracket_full_corner_sensitivity'][1]:.5f}]",
           f"{p['y_exponent']:.5f}",p['common_constant_y_allowed_by_all_brackets']]
          for p in pos.get('response_shape_descriptive_fits',[])])
    lines+=['','## Response and launch-shape comparisons','',
      'Each comparison optimizes duration in both models at equal peak-based N. Gaussian launch energy is sqrt(pi) N^2 in soliton units; sech launch energy is 2 N^2.']
    table(lines,['Response / shape','N','Share change vs BW/sech','Resolution interval','Normalized leading-energy change','T0* ratio'],[
       [p['response']+' / '+p['shape'],p['N'],f"{100*p['share_relative_change']:+.3f}%",
        f"[{100*p['share_relative_change_resolution_interval'][0]:+.3f}%, {100*p['share_relative_change_resolution_interval'][1]:+.3f}%]",
        f"{100*p['normalized_leading_energy_relative_change']:+.3f}%",f"{p['duration_ratio']:.4f}"] for p in m['response_shape_comparisons']])
    lines+=['','## Width-selection test','',
      'Widths are sech parameters, not intensity FWHM. Tfit comes from an intensity-profile fit; Tarea is inferred from the total-gamma area relation. Rmax is the independently bracketed overlap maximum.']
    table(lines,['Response / shape','N','Tfit (fs)','Tfit resolution interval (fs)','Tarea (fs)','FWHM / 1.762747 (fs)','Rmax width (fs)','Tfit / Rmax','Tarea / Rmax'],[
      [p['response']+' / '+p['shape'],p['N'],f"{p['fit_width_fs']:.3f}",
       f"[{p['fit_width_resolution_interval_fs'][0]:.3f}, {p['fit_width_resolution_interval_fs'][1]:.3f}]",
       f"{p['area_width_fs']:.3f}",f"{p['fwhm_width_fs']:.3f}",f"{p['overlap_max_width_fs']:.3f}",f"{p['fit_overlap_ratio']:.4f}",f"{p['area_overlap_ratio']:.4f}"]
      for p in m['reference_peaks'] if 'overlap_max_width_fs' in p])
    lines+=['','## Physical SMF-28 model at the ZS-share optimum','',
      'Published dispersion including beta3 and higher orders, HC response, shock, uniform 0.2 dB/km loss, gamma0 = 1.3 / (W km), carrier 1550 nm; zN = 4. Local-ZS soliton content and direct temporal-gate energy are distinct observables. Photon fractions use the full positive-frequency spectral integral and the launch denominator.']
    table(lines,['N','Input T0* / FWHM (fs)','Launch E (nJ)','ZS / gated share','ZS / gated E1 (nJ)','Photon fraction','Length (m)','Centroid wavelength (nm)','Minimum global / leading support in bracket (1200–2300 nm)'],[
      [p['N'],f"{p['T0_fs']:.2f} / {1.762747174039086*p['T0_fs']:.2f}",f"{p['launch_energy_nJ']:.4f}",
       f"{p['f1']:.5f} / {p['f_gate']:.5f}",f"{p['energy_nJ']:.4f} / {p['gate_energy_nJ']:.4f}",
       f"{p['photon_fraction']:.5f}",f"{p['length_m']:.4f}",f"{p['lambda_nm']:.2f}",
       f"{p['global_spectral_support_min_in_bracket']:.8f} / {p['leading_spectral_support_min_in_bracket']:.8f}"] for p in m['physical_share_optima']])
    table(lines,['N','T0* bracket (fs)','Efficient energy resolution interval (nJ)','Entire interval within frozen 1.35–1.55 nJ','tau_R','shock s','delta3','alpha L'],[
      [p['N'],f"[{p['T_bracket_fs'][0]:.3f}, {p['T_bracket_fs'][1]:.3f}]",
       f"[{p['energy_resolution_interval_nJ'][0]:.4f}, {p['energy_resolution_interval_nJ'][1]:.4f}]",p['efficient_energy_prediction_resolved_with_full_bracket'],
       f"{p['tau_R']:.6g}",f"{p['s']:.6g}",f"{p['delta3']:.6g}",f"{p['alpha_L']:.6g}"] for p in m['physical_share_optima']])
    lines+=['','These resolution intervals keep fibre parameters fixed; they do not include spool-to-spool parameter uncertainty.']
    table(lines,['N','Launch peak power (kW)','Input photons','Leading photons'],[
      [p['N'],f"{p['peak_power_kW']:.4f}",f"{p['input_photons']:.6g}",f"{p['leading_photons']:.6g}"] for p in m['physical_share_optima']])
    lines+=['','## Alternative: maximize the directly gated energy fraction','',
      'The temporal-gate energy fraction is maximized independently at the same zN = 4 prescription. Its optimum need not equal the local-ZS-content optimum above. No photon-fraction maximum at a grid edge is accepted.']
    table(lines,['N','T0* (fs)','Neighbor bracket (fs)','Gated fraction','Gated energy (nJ)','Photon fraction','Length (m)'],[
      [p['N'],f"{p['T0_fs']:.3f}",f"[{p['T_bracket_fs'][0]:.3f}, {p['T_bracket_fs'][1]:.3f}]",f"{p['objective_value']:.6f}",
       f"{p['energy_nJ']:.5f}",f"{p['photon_fraction']:.6f}",f"{p['length_m']:.4f}"]
      for p in m['physical_alternative_optima'] if p.get('bracketed') and p['objective']=='f_gate'])
    lines+=['','## Fixed launch constraint','',
      'Transform-limited sech launch, energy 3 nJ, physical length 2 m, peak power <= 10 kW, duration 150–500 fs. This is a finite scan; its largest accepted sample is not a certified continuous global maximum.']
    table(lines,['T0 (fs)','N','ZS energy (nJ)','Gated energy (nJ)','ZS / gated share','Photon fraction'],[
      [p['T0_fs'],f"{p['N']:.5f}",f"{p['energy_nJ']:.5f}",f"{p['gate_energy_nJ']:.5f}",f"{p['f1']:.5f} / {p['f_gate']:.5f}",f"{p['photon_fraction']:.5f}"] for p in sorted(m['constrained_scan'],key=lambda p:p['T0_fs'])])
    lines+=['','## Frozen BW holdout scores']
    table(lines,['N','Predicted / measured a','a error / tolerance','Predicted / measured T0* (fs)','Relative T error','Share / position pass'],[
      [p['N'],f"{p['predicted_scaled_share']:.6f} / {p['observed_scaled_share']:.6f}",f"{p['scaled_share_error']:+.6f} / 0.006",
       f"{p['predicted_T0_fs']:.3f} / {p['observed_T0_fs']:.3f}",f"{100*p['position_relative_error']:+.3f}%",f"{p['share_pass']} / {p['position_pass']}"] for p in m['holdout_scores']])
    lines+=['','The preceding pass flags score central estimates. The following flags additionally require the full numerical resolution envelope or duration bracket to lie within the frozen tolerance.']
    table(lines,['N','Share: envelope inside 0.006','Fitted position: full bracket inside 5%','Original position: full bracket inside 10%'],[
      [p['N'],p['share_prediction_resolved_with_resolution_envelope'],p['position_prediction_resolved_with_full_bracket'],p['original_10pct_position_prediction_resolved_with_full_bracket']] for p in m['holdout_scores']])
    (HERE/'tables.md').write_text('\n'.join(lines)+'\n')
    print('Wrote tables.md')
if __name__=='__main__':main()
