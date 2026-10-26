"""Compact summary of shot_stats_K<K>.json (any subset of ensembles) -> summary_K<K>.json and printed table.
Median relative variance over the launched excited modes (groups 1, 2), the fundamental's relative variance, f0 mean,
and (quantum-limited ensemble) the fundamental's and launched modes' Fano factors in photon units (n = 1e10)."""
import json, sys, numpy as np
fn = sys.argv[1]; d = json.load(open(fn)); groups = np.array(d['groups'])
launched = np.where((groups == 1) | (groups == 2))[0]
rows = []
for r in d['records']:
    row = dict(z=r['z'])
    for nm in d['ensembles']:
        e = r[nm]; rv = np.array(e['relvar']); Im = np.array(e['I_mean'])
        row[nm] = dict(relvar_launched_median=float(np.median(rv[launched])), relvar_I0=float(rv[0]), f0_mean=e['f0_mean'])
        if nm == 'q1e10':
            row[nm]['Fano_I0'] = float(1e10*rv[0]*Im[0]); row[nm]['Fano_launched_median'] = float(np.median(1e10*rv[launched]*Im[launched]))
    rows.append(row)
out = dict(source=fn, K=d['K'], M=len(groups), dirichlet=d['dirichlet'], rows=rows)
json.dump(out, open(fn.replace('shot_stats_', 'summary_'), 'w'), indent=1)
D = d['dirichlet']; print(f"{fn}: M = {len(groups)}; Dirichlet excited g2-1 = {D['g2_excited']-1:.3f}, <I0> = {D['I0_mean']:.3f}, relvar(I0) = {D['I0_relvar']:.2e}")
for row in rows:
    print(f"z={row['z']:4d} | launched relvar " + "  ".join(f"{nm} {row[nm]['relvar_launched_median']:.2e}" for nm in d['ensembles'])
          + " | I0 relvar " + "  ".join(f"{nm} {row[nm]['relvar_I0']:.2e}" for nm in d['ensembles'])
          + (f" | Fano I0 {row['q1e10']['Fano_I0']:.1f}, launched {row['q1e10']['Fano_launched_median']:.1f}" if 'q1e10' in row else '')
          + (f" | f0 deph {row['deph']['f0_mean']:.3f}" if 'deph' in row else ''))
