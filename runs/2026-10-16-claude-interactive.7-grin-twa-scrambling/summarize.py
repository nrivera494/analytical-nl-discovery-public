"""Summarize grin_twa.json (raw_location): half-collapse lengths vs n and the slope against the pre-registered prediction."""
import json, os, numpy as np
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-grin-twa-scrambling')
here = os.path.dirname(os.path.abspath(__file__))
o = json.load(open(os.path.join(RAW, 'grin_twa.json'))); z = np.array(o['z'])
rows = []
for j, n in enumerate(o['ncells']):
    cm = np.array([rec[j]['coh'] for rec in o['records']]).mean(1); k = np.argmax(cm < 0.5)
    zh = float(z[k-1] + (0.5-cm[k-1])*(z[k]-z[k-1])/(cm[k]-cm[k-1]))
    rv = np.median(np.array([rec[j]['relvar'] for rec in o['records']])[:, 1:], axis=1); kk = np.argmax(rv > 0.4)
    rows.append(dict(n=n, z_meanfield_half=round(zh, 1), z_median_relvar_0p4=float(z[kk]) if rv[kk] > 0.4 else None))
ns = np.array([r['n'] for r in rows]); zs = np.array([r['z_meanfield_half'] for r in rows])
slope = float(np.polyfit(np.log10(ns), zs, 1)[0])
summary = dict(rows=rows, increment_1e6_to_1e12=round(float(zs[-1]-zs[0]), 1), predicted_increment=377.4, tolerance=[283, 471],
               slope_per_decade=round(slope, 1), predicted_slope=62.9, lambda_eff=round(float(np.log(10)/(2*slope)), 4), lambda_1_shadow=0.0183,
               verdict="PASS" if 283 <= zs[-1]-zs[0] <= 471 else "FAIL")
json.dump(summary, open(os.path.join(here, 'summary.json'), 'w'), indent=1); print(json.dumps(summary, indent=1))
# post-scrambling ensemble statistics vs the Dirichlet law (C-01), z >= 1000 (past z_E for every n)
K = 5; eps = np.concatenate([[k]*(k+1) for k in range(K)]).astype(float); Mm = len(eps); D = Mm-1
S1 = np.sum(1/eps[1:]); S2 = np.sum(1/eps[1:]**2); Ep = o['Eprime']
N0 = 1 - Ep*S1/D; varN0 = (Ep/D)**2*(D*S2 - S1**2)/(D+1)
post = []
sel = z >= 1000
for j, n in enumerate(o['ncells']):
    rv = np.array([rec[j]['relvar'] for rec in o['records']])[sel]
    post.append(dict(n=n, relvar_excited_mean=round(float(rv[:, 1:].mean()), 3), relvar_condensate=round(float(rv[:, 0].mean()), 4)))
summary['post_scrambling_vs_dirichlet'] = dict(dirichlet_relvar_excited=round((D-1)/(D+1), 3), dirichlet_relvar_condensate=round(float(varN0/N0**2), 4), ensemble=post)
json.dump(summary, open(os.path.join(here, 'summary.json'), 'w'), indent=1); print(json.dumps(summary['post_scrambling_vs_dirichlet'], indent=1))
# collapse shape: local slope of ln(-ln coh_bar) vs z in the window 0.02 < -ln coh_bar < 1.5, z > 50
shape = []
for j, n in enumerate(o['ncells']):
    cm = np.array([rec[j]['coh'] for rec in o['records']]).mean(1); y = -np.log(np.clip(cm, 1e-12, 1))
    sel = (y > 0.02) & (y < 1.5) & (z > 50)
    sl = float(np.polyfit(z[sel], np.log(y[sel]), 1)[0]); pw = float(np.polyfit(np.log(z[sel]), np.log(y[sel]), 1)[0])
    shape.append(dict(n=n, window=[float(z[sel].min()), float(z[sel].max())], loglog_slope_in_z=round(sl, 4), power_law_exponent=round(pw, 1)))
summary['collapse_shape'] = dict(two_lambda_1=0.0366, per_n=shape, note="local rate ~0.015 (about lambda_1) for every n; the n-scaling of the crossing gives 2 lambda_eff = 0.034")
json.dump(summary, open(os.path.join(here, 'summary.json'), 'w'), indent=1); print(json.dumps(summary['collapse_shape'], indent=1)[:600])
# dephased-input ensemble (grin_twa_dephased.py): z at which the median excited-mode relative variance first exceeds 0.43
od = json.load(open(os.path.join(RAW, 'grin_twa_dephased.json'))); zd = np.array(od['z']); deph = []
for j, n in enumerate(od['ncells']):
    rv = np.median(np.array([rec[j]['relvar'] for rec in od['records']])[:, 1:], axis=1); k = np.argmax(rv > 0.43)
    deph.append(dict(n=n, z_relvar_0p43=float(zd[k]) if rv[k] > 0.43 else None, relvar_at_10=round(float(rv[np.argmin(abs(zd-10))]), 3)))
summary['dephased_input'] = dict(sampling_step=od['rec'], per_n=deph, note="pre-registered in grin_twa_dephased_predictions.txt; both n reach thermal-level spread within 2-4 L_NL (one sampling step apart), vs coherent z_E 235-511 L_NL")
json.dump(summary, open(os.path.join(here, 'summary.json'), 'w'), indent=1); print(json.dumps(summary['dephased_input']))
