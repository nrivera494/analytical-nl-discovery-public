#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt.

Post-production correction of the variance definition; no new trajectories.
The frozen predictions said relative intensity variance, while the original
analysis used the normally ordered excess g2-1. Keep both and distinguish
undefined initial vacuum-mode ratios from occupied-mode diagnostics.
"""
from pathlib import Path
import json
import numpy as np
from summarize import crossing

RUN = Path(__file__).resolve().parent
DATA = Path.home()/'analytical-nl-discovery-data'/RUN.name

def curves(blocks, n):
    o = blocks.mean(axis=0)
    m = o.shape[1]//6
    intensity = o[:, 2*m:3*m]
    square = o[:, 3*m:4*m]
    photons = intensity-.5/n
    with np.errstate(divide='ignore', invalid='ignore'):
        return {
            'normally_ordered_excess': (square-2*intensity/n+.5/n**2)/photons**2-1,
            'photon_number_relative_variance': (square-intensity**2-.25/n**2)/photons**2,
            'wigner_intensity_relative_variance': square/intensity**2-1,
        }

def main():
    rows = []
    for line in (DATA/'records.jsonl').read_text().splitlines():
        r = json.loads(line)
        if not r['dephased']:
            continue
        blocks = np.load(r['raw_file'])['moments']
        cc = curves(blocks, r['n'])
        z = np.arange(len(next(iter(cc.values()))))*r['sample']
        diagnostics = {}
        for name, modal in cc.items():
            all_modes = np.median(modal[:, 1:], axis=1)
            occupied = np.median(modal[:, 1:6], axis=1)
            jk = []
            for j in range(len(blocks)):
                y = np.median(curves(np.delete(blocks, j, axis=0), r['n'])[name][:, 1:6], axis=1)
                value = crossing(z, y, 13/30, start=.2, down=False)
                if value is not None:
                    jk.append(value)
            diagnostics[name] = {
                'all_excited_initial_estimate': float(all_modes[0]),
                'all_excited_at_first_nonzero_sample': float(all_modes[1]),
                'all_excited_numerical_upcrossing': crossing(z, all_modes, 13/30, start=.2, down=False),
                'all_excited_first_sample_above_target': bool(all_modes[1]>=13/30),
                'all_excited_valid_onset_clock': False,
                'initially_occupied_onset': crossing(z, occupied, 13/30, start=.2, down=False),
                'initially_occupied_onset_jackknife_se': float(np.sqrt((len(jk)-1)*np.var(jk))) if len(jk)>1 else None,
            }
        rows.append(dict(n=r['n'], dt=r['dt'], sample=r['sample'], disorder_seed=r['disorder_seed'], diagnostics=diagnostics))
    result = dict(agent='gpt-b', model='gpt-6-astra', family='gpt',
        role='post-production analysis correction, not a replacement frozen test',
        photon_variance_formula='(mean_Wigner_I2-mean_Wigner_I**2-1/(4*n**2))/(mean_Wigner_I-1/(2*n))**2',
        identity='photon_relative_variance = normally_ordered_g2_minus_1 + 1/(n*mean_photon_intensity)',
        initial_support='five occupied excited modes, nine exactly empty excited modes',
        caveat='The all-mode photon ratio is undefined on initial vacuum modes. Wigner vacuum intensity has relative variance one. First-cell crossings cannot establish a kinetic clock. Occupied-mode restriction is post hoc.',
        rows=rows)
    (RUN/'variance_clocks.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    for r in rows:
        print(r['n'], r['diagnostics']['photon_number_relative_variance'])

if __name__ == '__main__':
    main()
