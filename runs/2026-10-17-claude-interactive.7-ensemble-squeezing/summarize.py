"""Summary and pre-registered checks (predictions.md Q1-Q5) for ensemble_squeezing.jsonl -> summary.json, summary.txt.
(Q6 is evaluated in ../2026-10-17-claude-interactive.7-ensemble-thermalization/summarize.py.)"""
import json, numpy as np
rows = [json.loads(l) for l in open('ensemble_squeezing.jsonl')]
REF_OWN = {1: -4.91, 2: -5.74, 5: -5.69}
def grp(ens, Ep, sig): return [r for r in rows if r['ens'] == ens and abs(r['Ep'] - Ep) < 1e-9 and r['sigma'] == sig]
def at(r, z, key): return [x[key] for x in r['records'] if abs(x['z'] - z) < 1e-6][0]
out = dict(groups={}, checks={})
for ens, Ep, sig in [('Q-dis', 0.3, 0.3), ('Q-dis', 0.6, 0.3), ('Q-launch', 0.3, 0.3), ('Q-launch', 0.6, 0.3), ('Q-strong', 0.3, 1.0), ('Q-strong', 0.3, 3.0)]:
    g = grp(ens, Ep, sig)
    if not g: continue
    d = {}
    for z in (1, 2, 5, 10, 20, 50, 100, 200):
        o = np.array([at(r, z, 'own_dB') for r in g]); lb = np.array([at(r, z, 'lam_best_1e10_dB') for r in g]); nu = np.array([at(r, z, 'nu') for r in g])
        f0 = np.array([at(r, z, 'f0') for r in g])
        d[z] = dict(own_mean=float(o.mean()), own_sd=float(o.std(ddof=1)), own_min=float(o.min()), own_max=float(o.max()), own_median=float(np.median(o)),
                    lam_mean=float(lb.mean()), lam_sd=float(lb.std(ddof=1)), lam_min=float(lb.min()), lam_max=float(lb.max()),
                    nu_geomean=float(np.exp(np.log(nu).mean())), nu_geosd=float(np.exp(np.log(nu).std(ddof=1))), f0_mean=float(f0.mean()), own=o.round(2).tolist(), lam=lb.round(1).tolist())
    out['groups'][f'{ens}_E{Ep}_s{sig}'] = dict(n=len(g), z=d)
G = out['groups']; C = out['checks']
def chk(n, ok, det): C[n] = dict(pass_=bool(ok), detail=det)
g = G.get('Q-dis_E0.3_s0.3')
if g:
    z = g['z']
    ok1 = all(max(abs(x - REF_OWN[zz]) for x in z[zz]['own']) <= 0.5 for zz in (1, 2, 5))
    ok2 = all(-7.5 <= z[zz]['own_mean'] <= -4.5 and z[zz]['own_max'] < -2 for zz in (10, 20, 50))
    chk('Q1', ok1 and ok2, '; '.join(f"z={zz}: mean {z[zz]['own_mean']:.2f} sd {z[zz]['own_sd']:.2f} [{z[zz]['own_min']:.2f}, {z[zz]['own_max']:.2f}]" for zz in (1, 2, 5, 10, 20, 50)))
    okq4 = (-25 <= z[10]['lam_mean'] <= -19) and (-14 <= z[50]['lam_mean'] <= -8) and (-8.5 <= z[100]['lam_mean'] <= -0.5) and (sum(x > -1 for x in z[200]['lam']) >= 9) \
           and all(z[zz]['nu_geosd'] <= 2 for zz in (1, 2, 5, 10, 20, 50))
    chk('Q4', okq4, '; '.join(f"z={zz}: lam_best {z[zz]['lam_mean']:.1f} +- {z[zz]['lam_sd']:.1f} [{z[zz]['lam_min']:.1f}, {z[zz]['lam_max']:.1f}], nu geomean {z[zz]['nu_geomean']:.3g} x/{z[zz]['nu_geosd']:.2f}" for zz in (10, 50, 100, 200)))
g = G.get('Q-launch_E0.3_s0.3')
if g:
    z = g['z']
    chk('Q2', all(-9 <= z[zz]['own_mean'] <= -4 and sum(x < -3 for x in z[zz]['own']) >= 9 for zz in (10, 20, 50)),
        '; '.join(f"z={zz}: mean {z[zz]['own_mean']:.2f} [{z[zz]['own_min']:.2f}, {z[zz]['own_max']:.2f}], below -3 dB: {sum(x < -3 for x in z[zz]['own'])}/{g['n']}" for zz in (10, 20, 50)))
ok3 = True; det3 = []
for k in ('Q-dis_E0.6_s0.3', 'Q-launch_E0.6_s0.3'):
    if k in G:
        for zz in (5, 10, 20):
            m = G[k]['z'][zz]['own_median']; ok3 &= m > -3; det3.append(f"{k} z={zz}: median {m:.2f}")
if det3: chk('Q3', ok3, '; '.join(det3))
base = G.get('Q-dis_E0.3_s0.3')
for sig in (1.0, 3.0):
    g = G.get(f'Q-strong_E0.3_s{sig}')
    if g and base:
        ok = all(abs(g['z'][zz]['own_mean'] - base['z'][zz]['own_mean']) <= 3 for zz in (10, 20, 50)) and abs(g['z'][50]['lam_mean'] - base['z'][50]['lam_mean']) <= 4
        chk(f'Q5_sigma{sig}', ok, '; '.join(f"z={zz}: own mean {g['z'][zz]['own_mean']:.2f} vs {base['z'][zz]['own_mean']:.2f}" for zz in (10, 20, 50)) + f"; lam_best(50) {g['z'][50]['lam_mean']:.1f} vs {base['z'][50]['lam_mean']:.1f}")
json.dump(out, open('summary.json', 'w'), indent=1)
lines = []
for k, g in G.items():
    lines.append(f"{k} (n={g['n']}): " + ' | '.join(f"z={zz}: own {d['own_mean']:.1f}+-{d['own_sd']:.1f} [{d['own_min']:.1f},{d['own_max']:.1f}], lam {d['lam_mean']:.1f}+-{d['lam_sd']:.1f}, nu {d['nu_geomean']:.3g}x/{d['nu_geosd']:.2f}" for zz, d in g['z'].items()))
lines.append('--- pre-registered checks ---'); lines += [f"{k}: {'PASS' if c['pass_'] else 'FAIL'} | {c['detail']}" for k, c in C.items()]
open('summary.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines[-6:]))
