"""Summary of shot_stats.json -> summary.json.
Per ensemble and z: median relative variance (g2 - 1 of mode powers across shots) over the 5 launched excited modes (groups 1, 2)
and over the 9 initially empty modes (groups 3, 4); the fundamental's relative variance and Fano factor in photon units for the
quantum-noise ensemble (Fano_0 = n Var(I_0)/<I_0>, n = 1e10); the condensate fraction f0 (mean, relative variance);
Gaussian-scaling check: relvar(q1e6)/relvar(q1e10) and relvar(q1e4)/relvar(q1e6) (expected 1e4 and 1e2 while the noise is linear).
Dirichlet reference (C-20261016-claude-interactive.7-01) for the same N and E'. Sampling error of a variance with B = 128: ~12.5%."""
import json, numpy as np
d = json.load(open('shot_stats.json')); groups = np.array(d['groups']); B = d['B']
launched = np.where((groups == 1) | (groups == 2))[0]; empty = np.where(groups >= 3)[0]
out = dict(dirichlet=d['dirichlet'], B=B, rows=[])
for r in d['records']:
    row = dict(z=r['z'])
    for nm in d['ensembles']:
        e = r[nm]; rv = np.array(e['relvar']); Im = np.array(e['I_mean'])
        row[nm] = dict(relvar_launched_median=float(np.median(rv[launched])), relvar_empty_median=float(np.median(rv[empty])),
                       relvar_I0=float(rv[0]), f0_mean=e['f0_mean'], f0_relvar=e['f0_relvar'], corr_I0_g1=e['corr_I0_g1'],
                       coh_I0=float(e['coh'][0]), coh_median_excited=float(np.median(e['coh'][1:])))
    q10, q6, q4 = row['q1e10'], row['q1e6'], row['q1e4']
    row['Fano_I0_quantum_n1e10'] = float(1e10*q10['relvar_I0']*np.array(r['q1e10']['I_mean'])[0])
    Iq = np.array(r['q1e10']['I_mean']); rq = np.array(r['q1e10']['relvar'])
    row['Fano_launched_median_quantum_n1e10'] = float(np.median(1e10*rq[launched]*Iq[launched]))
    row['I_mean_launched_median_quantum'] = float(np.median(Iq[launched]))
    row['ratio_q1e6_over_q1e10_launched'] = q6['relvar_launched_median']/q10['relvar_launched_median']
    row['ratio_q1e4_over_q1e6_launched'] = q4['relvar_launched_median']/q6['relvar_launched_median']
    row['ratio_q1e6_over_q1e10_I0'] = q6['relvar_I0']/q10['relvar_I0']
    row['ratio_q1e4_over_q1e6_I0'] = q4['relvar_I0']/q6['relvar_I0']
    out['rows'].append(row)
json.dump(out, open('summary.json', 'w'), indent=1)
D = out['dirichlet']
print(f"Dirichlet: excited g2-1 = {D['g2_excited']-1:.3f}, <I0> = {D['I0_mean']:.3f}, relvar(I0) = {D['I0_relvar']:.2e}")
print("Fano (photon units, quantum-limited input n = 1e10), launched excited modes, median:", [(row['z'], round(row['Fano_launched_median_quantum_n1e10'], 1)) for row in out['rows']])
print(" z   | launched-excited relvar: q1e10    q1e6     q1e4     rin1pc   deph  | I0 relvar: q1e10    q1e4     rin1pc   deph   | Fano_I0(q) | ratios 6/10, 4/6 (launched; I0) | f0 deph")
for row in out['rows']:
    g = lambda nm, k: row[nm][k]
    print(f"{row['z']:4d} | {g('q1e10','relvar_launched_median'):.1e} {g('q1e6','relvar_launched_median'):.1e} {g('q1e4','relvar_launched_median'):.1e} "
          f"{g('rin1pc','relvar_launched_median'):.1e} {g('deph','relvar_launched_median'):.3f} | {g('q1e10','relvar_I0'):.1e} {g('q1e4','relvar_I0'):.1e} "
          f"{g('rin1pc','relvar_I0'):.1e} {g('deph','relvar_I0'):.1e} | {row['Fano_I0_quantum_n1e10']:8.2f} | {row['ratio_q1e6_over_q1e10_launched']:.2e} {row['ratio_q1e4_over_q1e6_launched']:.1f}; "
          f"{row['ratio_q1e6_over_q1e10_I0']:.2e} {row['ratio_q1e4_over_q1e6_I0']:.1f} | {g('deph','f0_mean'):.3f}")
