"""Literature unit conversions only; agent gpt-b, model gpt-6-astra, family gpt.

No propagation calculation. Conditional values are not measurements.
For a sech intensity pulse, N^2 = gamma E T0 / (2 abs(beta2)).
The listed ps^2/km, (W km)^-1, nJ and fs units cancel in this formula.
"""
import csv
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
TAU_FS = 12.2
FWHM_FACTOR = 1.763  # same rounded convention as the claim comparison

cases = [
    dict(case='Kormokar 2023', doi='10.1364/JOSAB.478975', access='full text',
         wavelength_nm=1550, FWHM_fs=938, input_nJ=35.4/20,
         leading_nJ=(35.4/20)*.506, reported_share=.506,
         beta2_abs_ps2_km=21.61, gamma_W_inv_km=1.42, N_reported=5.57,
         qualification='EDFA output chirped; duration and N fitted to propagation; fission in 3 m patch before VOA/100 m fibre. Leading energy is only reported share times EDFA pulse energy, not an independent output-energy measurement.'),
    dict(case='Akhoundi 2018 SMF28 reference parameters', doi='10.1364/BOE.9.002326', access='full text',
         wavelength_nm=1560, FWHM_fs=400, input_nJ=5, leading_nJ=2.5,
         reported_share=.5, beta2_abs_ps2_km=21.61, gamma_W_inv_km=1.42,
         qualification='Conditional sech equivalent: beta2 and gamma not reported; borrowed from Kormokar 2023 SMF28 at 1550 nm. Source compressor chirp and true pulse shape not specified sufficiently.'),
    dict(case='Akhoundi 2018 parameter sensitivity', doi='10.1364/BOE.9.002326', access='full text',
         wavelength_nm=1560, FWHM_fs=400, input_nJ=5, leading_nJ=2.5,
         reported_share=.5, beta2_abs_ps2_km=21.7, gamma_W_inv_km=1.3,
         qualification='Sensitivity scenario using the session brief reference-fibre parameters, not measured parameters of this experiment and not a confidence interval.'),
    dict(case='Akhoundi 2020 conditional compressed pulse', doi='10.1364/BOE.389557', access='full text',
         wavelength_nm=1560, FWHM_fs=200, input_nJ=80/37, leading_nJ=40/37,
         reported_share=.5, beta2_abs_ps2_km=21.61, gamma_W_inv_km=1.42,
         qualification='Conditional only: 200 fs is compressed duration, not a separately established transform-limited launch plane for the 11 m SSFS fibre. beta2/gamma borrowed from Kormokar. N<3 outside peak-share law.'),
    dict(case='van Howe 2007 LP02', doi='10.1364/OL.32.000340', access='full text',
         wavelength_nm=1064, FWHM_fs=200, input_nJ=1.39, leading_nJ=.8,
         reported_share=.57, beta2_abs_ps2_km=62.8*1060**2/(2*math.pi*299792.458),
         gamma_W_inv_km=2.2, N_reported=2.1,
         qualification='Beta2 from measured D=62.8 ps/(nm km) at 1060 nm. Gaussian/irregular launch; sech-equivalent N is a diagnostic, not a measured IST order. Compound SMF/LPG/HOM module; N<3 outside peak-share law.'),
    dict(case='Shamim 2023 low reported N', doi='10.1109/JLT.2022.3223802', access='full text',
         wavelength_nm=1940, FWHM_fs=None, input_nJ=None, leading_nJ=None,
         reported_share=None, beta2_abs_ps2_km=74, gamma_W_inv_km=2.2,
         N_reported=2.0,
         qualification='Range endpoint only, not one paired operating point. Launch main lobe 88-536 fs with pedestal and variable chirp; N based on measured peak power/width. ECE denominator is output total energy. Formal extrapolation below N=3.'),
    dict(case='Shamim 2023 high reported N', doi='10.1109/JLT.2022.3223802', access='full text',
         wavelength_nm=1940, FWHM_fs=None, input_nJ=None, leading_nJ=None,
         reported_share=None, beta2_abs_ps2_km=74, gamma_W_inv_km=2.2,
         N_reported=2.3,
         qualification='Other endpoint of reported N range for 8 m DCF configuration; do not pair independently reported range endpoints. Formal extrapolation below N=3.'),
    dict(case='Li 2025 SMF', doi='10.1016/j.optlastec.2024.111769', access='full text',
         wavelength_nm=None, FWHM_fs=None, input_nJ=5.7, leading_nJ=4.8,
         reported_share=.85, beta2_abs_ps2_km=23, gamma_W_inv_km=None,
         qualification='Full text gives nominal beta2=-23 fs^2/mm and MFD=10.5 um, but no paired launch pulse duration or gamma. N and optimum not identifiable. Pulse already shifts in preceding 1.1 m EYDCF; polarization and power optimized. 5.5 m SMF; reported efficiency peak is against output energy, not fixed-N duration.'),
]

for c in cases:
    duration, energy = c['FWHM_fs'], c['input_nJ']
    beta, gamma = c['beta2_abs_ps2_km'], c['gamma_W_inv_km']
    c['N_sech_equivalent'] = (math.sqrt(gamma*energy*(duration/FWHM_FACTOR)/(2*beta))
        if all(x is not None for x in [duration, energy, beta, gamma]) else None)
    n = c.get('N_reported', c['N_sech_equivalent'])
    c['N_used_for_predictions'] = n
    c['peak_share_fit_in_domain_N3_to10'] = bool(n is not None and 3 <= n <= 10)
    c['T0_star_fs'] = 21*n**1.62 if n is not None else None
    c['FWHM_star_fs'] = FWHM_FACTOR*c['T0_star_fs'] if n is not None else None
    c['f_star'] = 1.29/math.sqrt(n) if n is not None else None
    c['E1_at_share_optimum_nJ'] = 1.5*n**(-.12)*beta/(gamma*TAU_FS) if n is not None and beta is not None else None
    c['Einput_at_share_optimum_nJ'] = 2*n*n*beta/(gamma*c['T0_star_fs']) if n is not None and beta is not None else None
    c['T1_at_share_optimum_fs'] = (4/3)*n**.12*TAU_FS if n is not None else None
    c['E1_measured_over_optimum_prediction'] = c['leading_nJ']/c['E1_at_share_optimum_nJ'] if c['leading_nJ'] is not None and c['E1_at_share_optimum_nJ'] is not None else None

summary = dict(agent='gpt-b', model='gpt-6-astra', family='gpt',
    run_id='2026-10-16-gpt-b-raman-literature', tau1_fs=TAU_FS,
    FWHM_factor=FWHM_FACTOR, no_fibre_simulation=True,
    uncertainty='Source rounded numbers retained. Missing fibre parameters explicitly conditional; no invented measurement uncertainty.',
    cases=cases,
    reference_N4=dict(beta2_abs_ps2_km=21.7, gamma_W_inv_km=1.3,
        T0_star_fs=21*4**1.62, FWHM_star_fs=FWHM_FACTOR*21*4**1.62,
        input_nJ=2*4**2*21.7/(1.3*21*4**1.62),
        leading_nJ=1.5*4**(-.12)*21.7/(1.3*TAU_FS),
        f_star=1.29/2),
    width_ratio_over_N3_to10=[(4/3)*n**.12 for n in [3,10]],
    passive_bound_crossing_N=(2/1.29)**2)
(OUT/'experiment_comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
fields = list(dict.fromkeys(k for c in cases for k in c))
with (OUT/'experiment_comparison.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(cases)
print(json.dumps(summary,indent=2))
