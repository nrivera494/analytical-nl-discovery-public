"""Summarize the TWA ensembles (raw JSON in raw_location) into summary.json."""
import json, os, numpy as np
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-rj-toy-twa-scrambling')
pred = {1e5: 297, 1e7: 2048, 1e9: 2757, 1e11: 3380}
rows = []
for part, fname in [(1, 'twa_scramble.json'), (2, 'twa_scramble2.json')]:
    o = json.load(open(os.path.join(RAW, fname))); z = np.array(o['z'])
    for j, (l, n) in enumerate(o['cols']):
        co = np.array([rec[j]['coh'] for rec in o['records']]); cm = co.mean(1)
        rv = np.array([rec[j]['relvar'] for rec in o['records']])[:, 1:]; rvm = np.median(rv, axis=1)
        def cross(y, thr, below=True):
            idx = np.where(y < thr)[0] if below else np.where(y > thr)[0]
            if len(idx) == 0: return None
            k = idx[0]
            if k == 0: return float(z[0])
            return float(z[k-1] + (thr - y[k-1])*(z[k]-z[k-1])/(y[k]-y[k-1]))
        r = dict(part=part, launch=l, n_cell_total=n, B=o['B'], zmax=o['zmax'], rec=o['rec'],
                 z_meanfield_half=None if l != 'coherent' else cross(cm, 0.5),
                 z_median_relvar_0p4=cross(rvm, 0.4, below=False),
                 prediction_z_meanfield_half=pred.get(n) if part == 2 else None,
                 relvar_exc_median_at=dict((int(zz), float(rvm[np.argmin(abs(z-zz))])) for zz in [20, 100, 500, 1000, 2000, 3000, 4000, 5000] if zz <= o['zmax']),
                 meanfield_frac_at=dict((int(zz), float(cm[np.argmin(abs(z-zz))])) for zz in [20, 100, 500, 1000, 2000, 3000, 4000, 5000] if zz <= o['zmax']))
        if 'relcoh' in o['records'][0][j]:
            rc = np.array([rec[j]['relcoh'] for rec in o['records']])[:, 1:].mean(1); r['z_relcoh_half'] = cross(rc, 0.5)
        rows.append(r)
# scaled dephasing collapse check (part 1, coherent): n*(-ln coh_bar) at fixed z
o = json.load(open(os.path.join(RAW, 'twa_scramble.json'))); z = np.array(o['z']); collapse = {}
for j, (l, n) in enumerate(o['cols']):
    if l != 'coherent': continue
    cm = np.array([rec[j]['coh'] for rec in o['records']]).mean(1)
    collapse[f'{n:.0e}'] = dict((int(zz), float(n*(-np.log(max(cm[np.argmin(abs(z-zz))], 1e-300))))) for zz in [200, 400, 600, 800, 1000, 1200])
json.dump(dict(rows=rows, scaled_dephasing_n_times_minus_ln_coh=collapse), open('summary.json', 'w'), indent=1)
for r in rows: print(r['part'], r['launch'], f"{r['n_cell_total']:.0e}", 'z_mf_half', r['z_meanfield_half'], 'pred', r['prediction_z_meanfield_half'], 'z_relvar0.4', r['z_median_relvar_0p4'], 'z_relcoh', r.get('z_relcoh_half'))
print(json.dumps(collapse, indent=0)[:600])
