"""Summary and pre-registered checks (predictions.md D1-D5) for disorder_scan.jsonl. White sigma = 0.3 reference: ensemble E1, E' = 0.6,
dis_seed 101-106 of ../2026-10-17-claude-interactive.7-ensemble-thermalization (same code and seeds). Post-hoc metric (labelled): L_rel10,
the same criterion with a 10 L_NL window, from the raw series (every 2 L_NL) in RAW, because the pre-registered 50 L_NL window cannot resolve
relaxation faster than about 50 L_NL. Output summary.json, summary.txt."""
import json, os, numpy as np
RAWS = {'scan': os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-disorder-model-scan'),
        'ens': os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-ensemble-thermalization')}
rows = [json.loads(l) for l in open('disorder_scan.jsonl')]
for r in rows: r['src'] = 'scan'
ref = [json.loads(l) for l in open('../2026-10-17-claude-interactive.7-ensemble-thermalization/ensemble_thermalization.jsonl')]
ref = [r for r in ref if r['ens'] == 'E1' and abs(r['Eprime'] - 0.6) < 1e-6 and r['dis_seed'] in range(101, 107)]
for r in ref: r.update(src='ens', set='S1', model='white', lc=None)
rows += ref
def lrel10(r):
    p = os.path.join(RAWS[r['src']], r['tag'] + '.npz')
    if not os.path.exists(p): return None
    d = np.load(p); z, I0 = d['z'], d['I'][:, 0].astype(float); nw = 5   # 10 L_NL at 2 L_NL spacing
    cs = np.concatenate([[0], np.cumsum(I0)]); rm = (cs[nw:] - cs[:-nw])/nw; hit = np.where(np.abs(rm - r['I0_D']) <= 0.02)[0]
    return float(z[hit[0]]) if len(hit) else None
def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None
settings = {}
for r in rows:
    key = (r['kind'], r['model'], r['sigma'], r['lc']); settings.setdefault(key, []).append(r)
out = dict(settings={}, checks={})
for (kind, model, sig, lc), g in sorted(settings.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], kv[0][3] or 0)):
    name = f"{kind}_{model}_s{sig}" + (f"_lc{lc}" if lc else '')
    L = [r['L_rel'] for r in g]; L10 = [lrel10(r) for r in g]
    out['settings'][name] = dict(n=len(g), I0=[round(r['I0'], 4) for r in g], I0_D=g[0]['I0_D'], g2=[round(r['g2_ex'], 3) for r in g],
                                 VarRatio=[round(r['VarI0']/r['VarI0_D'], 2) for r in g], D_RJ=[round(r['D_RJ'], 3) for r in g],
                                 L_rel=L, L_rel_median=med(L), L_rel10_posthoc=L10, L_rel10_median=med(L10), z_on=[r['z_on'] for r in g], z_on_median=med([r['z_on'] for r in g]))
S = out['settings']; C = out['checks']
def chk(n, ok, d): C[n] = dict(pass_=bool(ok), detail=d)
for name, s in S.items():
    if name.startswith('deph'):
        k = sum(abs(i - s['I0_D']) <= 0.02 and abs(g2 - 1.8667) <= 0.06 for i, g2 in zip(s['I0'], s['g2']))
        chk(f'D1_{name}', k >= 5, f"{k}/{s['n']} with |dI0|<=0.02 and |dg2|<=0.06; <I0> {s['I0']}; g2 {s['g2']}")
def L(name, which='L_rel_median'): return S.get(name, {}).get(which)
a, b = L('deph_white_s3.0'), L('deph_white_s1.0')
chk('D2', a is not None and b is not None and a >= 2*b, f"median L_rel sigma=3: {a}, sigma=1: {b} (post hoc 10-L_NL window: {L('deph_white_s3.0', 'L_rel10_median')}, {L('deph_white_s1.0', 'L_rel10_median')})")
a, b = L('deph_white_s0.1'), L('deph_white_s0.3')
chk('D3', a is not None and b is not None and a >= b, f"median L_rel sigma=0.1: {a}, sigma=0.3: {b} (post hoc: {L('deph_white_s0.1', 'L_rel10_median')}, {L('deph_white_s0.3', 'L_rel10_median')})")
w = L('deph_white_s0.3')
for lc, fac in [(0.1, 2), (1.0, 2), (10.0, 3), (100.0, 3)]:
    x = L(f'deph_piecewise_s0.3_lc{lc}')
    ok = (x is not None and w is not None and ((w == 0 and x <= 50) or (w > 0 and x/fac <= w <= x*fac)))
    if lc >= 10: ok = ok and C.get(f'D1_deph_piecewise_s0.3_lc{lc}', {}).get('pass_', False)
    chk(f'D4_lc{lc}', ok, f"median L_rel l_c={lc}: {x} vs white {w} (factor {fac}; both below the 50 L_NL resolution counts as agreement); post hoc 10-L_NL: {L(f'deph_piecewise_s0.3_lc{lc}', 'L_rel10_median')} vs {L('deph_white_s0.3', 'L_rel10_median')}")
for name, s in S.items():
    if name.startswith('G1'):
        k = sum(z is not None and z <= 4000 and abs(i - 0.5655) <= 0.03 for z, i in zip(s['z_on'], s['I0']))
        chk(f'D5_{name}', k >= 5, f"{k}/{s['n']} condensed; z_on {s['z_on']}; <I0> {s['I0']}")
a, b = S.get('G1_white_s3.0', {}).get('z_on_median'), S.get('G1_white_s1.0', {}).get('z_on_median')
chk('D5_order', a is not None and b is not None and a > b, f"median z_on sigma=3: {a}, sigma=1: {b}")
json.dump(out, open('summary.json', 'w'), indent=1)
lines = [f"{n}: n={s['n']} <I0> {s['I0']} (D {s['I0_D']:.4f}) g2 {s['g2']} Var/D {s['VarRatio']} D_RJ {s['D_RJ']} L_rel med {s['L_rel_median']} (post hoc L_rel10 med {s['L_rel10_median']}) z_on med {s['z_on_median']}" for n, s in S.items()]
lines.append('--- pre-registered checks ---'); lines += [f"{k}: {'PASS' if c['pass_'] else 'FAIL'} | {c['detail']}" for k, c in C.items()]
open('summary.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
