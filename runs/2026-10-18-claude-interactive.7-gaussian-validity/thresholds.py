"""G4 of predictions.md and the regime boundaries quoted in the claims (no new dynamics; reads earlier runs).
(a) Own squeezing: per realization of runs/2026-10-17-claude-interactive.7-ensemble-squeezing, n0* = V_P^2/(0.8 lam_own) (curvature term = 10% of
    the squeezed variance; lam_own = 10^(own_dB/10)), at z = 5, 10, 20, 50, 100.
(b) Multimode squeezing (runs/2026-10-16-claude-interactive.7-grin-gaussian-state): n0* = sigma_max^6/0.8.
(c) Photon counting: n0* = V_P,0^2/(0.8 lam_gen) with V_P,0 from runs/2026-10-17-claude-interactive.7-condensate-kerr-squeezability (same case).
Output thresholds.json and printed tables."""
import json, numpy as np
out = {}
qs = [json.loads(l) for l in open('../2026-10-17-claude-interactive.7-ensemble-squeezing/ensemble_squeezing.jsonl')]
for ens, Ep, sig in [('Q-dis', 0.3, 0.3), ('Q-launch', 0.3, 0.3), ('Q-dis', 0.6, 0.3), ('Q-strong', 0.3, 1.0), ('Q-strong', 0.3, 3.0)]:
    g = [r for r in qs if r['ens'] == ens and abs(r['Ep'] - Ep) < 1e-9 and r['sigma'] == sig]; d = {}
    for z in (5, 10, 20, 50, 100):
        th = []
        for r in g:
            x = [x for x in r['records'] if abs(x['z'] - z) < 1e-6][0]; lam = 10**(x['own_dB']/10)
            th.append(x['V_P']**2/(0.8*lam) if lam < 1 else np.nan)
        th = np.array(th); ok = th[np.isfinite(th)]
        d[z] = dict(n_squeezed=int(len(ok)), n0star_median=float(np.median(ok)) if len(ok) else None, n0star_max=float(np.max(ok)) if len(ok) else None)
    out[f'own_{ens}_E{Ep}_s{sig}'] = d
gs = json.load(open('../2026-10-16-claude-interactive.7-grin-gaussian-state/summary.json'))['cases']
for c in gs:
    out[f"multimode_E{c['Eprime']}_s{c['sigma']}"] = {int(r['z']): dict(lam_lin_dB=r['multimode_min_quad_dB'], sigma_max2=float(np.exp(2*r['log_sigma_max'])),
                                                                         n0star=float(np.exp(6*r['log_sigma_max'])/0.8)) for r in c['records']}
ck = json.load(open('../2026-10-17-claude-interactive.7-condensate-kerr-squeezability/cond_kerr.json'))['cases']
for c in gs:
    m = [x for x in ck if x['Eprime'] == c['Eprime'] and x['sigma'] == c['sigma']]
    if not m: continue
    vp = {int(round(r['z'])): r['V_P'] for r in m[0]['records']}
    out[f"photon_counting_E{c['Eprime']}_s{c['sigma']}"] = {int(r['z']): dict(lam_gen_dB=r['lambda_gen_dB'], V_P0=vp[int(r['z'])],
                                                                               n0star=float(vp[int(r['z'])]**2/(0.8*10**(r['lambda_gen_dB']/10))))
                                                              for r in c['records'] if int(r['z']) in vp}
json.dump(out, open('thresholds.json', 'w'), indent=1)
for k, d in out.items():
    if k.startswith('own'):
        print(k, ' | '.join(f"z={z}: n0* median {v['n0star_median']:.2g} max {v['n0star_max']:.2g} ({v['n_squeezed']} squeezed)" if v['n0star_median'] else f"z={z}: none squeezed" for z, v in d.items()))
    else:
        print(k, ' | '.join(f"z={z}: n0* {v['n0star']:.2g}" for z, v in d.items()))
