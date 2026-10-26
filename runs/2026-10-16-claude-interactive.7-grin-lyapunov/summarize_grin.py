"""Summarize grin_lyap.jsonl and the cw_sidebands*.json files (raw_location) into summary.json."""
import json, os, numpy as np
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-grin-lyapunov')
here = os.path.dirname(os.path.abspath(__file__))
rows = []
for l in open(os.path.join(RAW, 'grin_lyap.jsonl')):
    o = json.loads(l); K = o['K']; M = o['M']; D = M-1
    groups = np.concatenate([[k]*(k+1) for k in range(K)]); eps = groups.astype(float); S1 = np.sum(1/eps[1:])
    rows.append(dict(K=K, M=M, Eprime=o['Eprime'], sigma=o['sigma'], lyapunov_per_LNL=round(o['lyapunov'], 5),
        mean_N0=round(o['mean_N0'], 4), se_N0=round(o['block_se']['mean_N0'], 4), RJ_N0=round(float(1-o['Eprime']*S1/D), 4),
        g2_exc=round(o['g2_exc_mean'], 3), se_g2=round(o['block_se']['g2_exc_mean'], 3), dirichlet_g2=round(2-2/M, 3),
        cross=round(o['cross_mean'], 3), dirichlet_cross=round(1-1/M, 3),
        var_N0=float('%.3e' % o['var_N0']), dirichlet_var_N0=float('%.3e' % o['pred']['var_N0']),
        group_mean_over_RJ=[round(float(np.mean(np.array(o['mean_exc_over_RJ'])[groups[1:]==k])), 3) for k in range(1, K)],
        drift=o['drift']))
cw = {}
for name in ['cw_sidebands.json', 'cw_sidebands_wide.json', 'cw_sidebands_normal.json']:
    f = os.path.join(RAW, name)
    if os.path.exists(f):
        for o in json.load(open(f)):
            key = o['mode']; cw.setdefault(key, {})
            for x, lam in zip(o['xs'], o['lam']):
                cw[key][str(x)] = round(lam, 5)
note = ("cw growth rates are field-amplitude growth rates per L_NL along the K=5, E'=0.6, sigma=0.3 trajectory; "
        "walkoff x=16 is a numerical artefact (RK4 step stability: x*k_max*dz = 3.2) and must not be used; gvd x >= 8 is affected by RK4 numerical damping at dz = 0.05 (x*dz >= 0.4), so use x <= 4.")
json.dump(dict(grin_cases=rows, cw_lambda_vs_x=cw, note=note), open(os.path.join(here, 'summary.json'), 'w'), indent=1)
for r in rows: print(r)
print(json.dumps(cw, indent=1))
