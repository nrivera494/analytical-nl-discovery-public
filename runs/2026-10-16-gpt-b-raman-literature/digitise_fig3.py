"""Small literature digitisation; no propagation solver.

agent: gpt-b; model: gpt-6-astra; family: gpt.
Input: manually inspected centres of ECE_GNLSE symbols in the 746 x 572
image embedded as xref 66 on page 8 of arXiv:2301.02945v1.
The source image and rendered pages live at the raw_location in meta.yaml.
Uncertainty is a conservative reading tolerance, not a statistical error bar.
"""
import csv
import json
from itertools import product
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
T = np.array([500, 700, 900, 1100, 1500, 1900, 2300, 2700, 3100])
X = [96.5, 141.0, 186.0, 230.0, 319.5, 408.5, 497.5, 586.5, 675.5]
Y = {
    2: [49, 55, 59, 61, 64, 65, 65, 65, 65],
    3: [147, 180, 196, 206, 216, 221, 225, 228, 229],
    4: [175, 215, 243, 265, 288, 299, 307, 312, 316],
    5: [215, 230, 261, 285, 321, 341, 353, 361, 367],
    6: [267, 259, 274, 296, 357, 380, 395, 405, 415],
}
# Tick centres: y=27 -> 80%, y=456 -> 30%. A 3-pixel centre
# ambiguity is 0.35 percentage points; report +/-0.4 points and +/-15 fs.
ece = {n: 80 - (np.array(y) - 27) * 50 / 429 for n, y in Y.items()}
rows = []
for n, ys in Y.items():
    for t, x, y, f in zip(T, X, ys, ece[n]):
        rows.append(dict(N=n, T_FWHM_fs=int(t), ECE_percent=round(float(f), 1),
                         x_pixel=x, y_pixel=y, T_reading_uncertainty_fs=15,
                         ECE_reading_uncertainty_percentage_points=0.4))
with (OUT / 'fig3_digitised.csv').open('w') as f:
    w = csv.DictWriter(f, fieldnames=rows[0]); w.writeheader(); w.writerows(rows)

comparison = []
for n in Y:
    j = int(np.argmax(ece[n])); fv = float(ece[n][j] / 100)
    comparison.append(dict(N=n, largest_sample_T_FWHM_fs=int(T[j]),
        largest_sample_fraction=fv, sample_fraction_times_sqrt_N=fv*np.sqrt(n),
        two_sided_peak_bracket=(n == 6),
        predicted_T0_star_fs=21*n**1.62,
        predicted_T_FWHM_star_fs=1.763*21*n**1.62,
        predicted_fraction_star=(1.29/np.sqrt(n) if n >= 3 else None)))

# Only N=6 has a two-sided sampled maximum; a T*(N) power-law fit is
# unidentifiable. The following two-point fit is explicitly CONDITIONAL on
# treating the left-boundary N=5 sample as its maximum. It is not a measured law.
conditional_exponent = float(np.log(700/500)/np.log(6/5))
conditional_T0_prefactor = float((500/1.763) / 5**conditional_exponent)
conditional_c = [float(max(ece[n])/100*np.sqrt(n)) for n in [5, 6]]
long_pulse = []
for n in [3, 4, 5, 6]:
    t = T[T >= 1900].astype(float)
    f = ece[n][T >= 1900] / 100
    ist = (2*n - 1)/n**2
    eps = f/ist - 1
    exponent = float(np.polyfit(np.log(1/t), np.log(eps), 1)[0])
    # Conservative reading-bound sensitivity, not a statistical confidence
    # interval. Explore all +/-0.4 pp and +/-15 fs corners for four points.
    slopes = []
    for signs in product([-1, 1], repeat=8):
        tc = t + 15*np.array(signs[:4])
        ec = (f + .004*np.array(signs[4:]))/ist - 1
        slopes.append(float(np.polyfit(np.log(1/tc), np.log(ec), 1)[0]))
    long_pulse.append(dict(N=n, T_FWHM_fs=t.tolist(),
        epsilon=eps.tolist(),
        c_estimate=(eps*(t/1.763)/1.462).tolist(),
        log_log_exponent=exponent,
        reading_bound_exponent_range=[min(slopes), max(slopes)],
        warning='Four finite-duration points; no asymptotic extrapolation. N=2 omitted because excess is at the symbol-reading tolerance.'))
summary = dict(agent='gpt-b', model='gpt-6-astra', family='gpt',
    source='arXiv:2301.02945v1; DOI 10.1364/JOSAB.478975',
    access='full text: arXiv preprint and published HTML; published Fig. 3 visually compared',
    calibration=dict(image_pixels=[746,572], y_ticks=[[27,80],[456,30]],
        uncertainty_ECE_percentage_points=0.4, uncertainty_T_reading_fs=15,
        peak_sampling_resolution_fs=100,
        method='manual symbol centres, linear axes; symbols, not analytical lines'),
    comparison=comparison,
    peak_position_fit=dict(identifiable=False,
        reason='Only N=6 is bracketed. N=2-5 maxima are not bracketed by the plotted range.',
        conditional_N5_N6_exponent=conditional_exponent,
        conditional_N5_N6_T0_prefactor_fs=conditional_T0_prefactor),
    conditional_N5_N6_fraction_sqrtN=conditional_c,
    long_pulse_digitised_fits=long_pulse,
    N6_text_values=dict(T_FWHM_fs=[400,700], ECE_percent=[50.0,53.0]),
    no_fibre_simulation=True)
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7.2,4.6), layout='constrained')
for n, style in zip(Y, ['^','o','s','d','*']):
    ax.plot(T, ece[n], marker=style, label=f'N = {n}', linewidth=1.2)
    if n >= 3:
        ax.scatter([1.763*21*n**1.62], [100*1.29/np.sqrt(n)],
                   marker='x', s=60, color=ax.lines[-1].get_color())
ax.axvspan(0,500,color='0.92',zorder=0,label='Outside published Fig. 3')
ax.set(xlim=(0,3200), ylim=(30,82), xlabel='Launch intensity FWHM (fs)',
       ylabel='Leading-soliton energy share (%)',
       title='Kormokar 2023: digitised GNLSE symbols\nCrosses: claim optimum, N = 3-6')
ax.legend(ncol=3,fontsize=8,loc='upper right')
ax.text(.99,.02,'Digitisation tolerance: +/-0.4 percentage points, +/-15 fs',
        transform=ax.transAxes,ha='right',fontsize=8)
fig.savefig(OUT/'fig3_comparison.png',dpi=180)
print(json.dumps(summary,indent=2))
