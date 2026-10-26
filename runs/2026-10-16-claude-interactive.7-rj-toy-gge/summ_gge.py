import json, numpy as np
pred = {(o['K'], o['Eprime'], o['launch']): o for o in json.load(open('gge_predict_focused.json'))}
pred.update({(o['K'], o['Eprime'], o['launch']): o for o in json.load(open('gge_predict_dephased_K4E06.json'))})
rows = []
import os
for l in open(os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-rj-toy-gge/gge_focused_runs.jsonl')):
    o = json.loads(l); K, Ep, la = o['K'], o['Eprime'], o['launch']
    groups = np.concatenate([[k]*(k+1) for k in range(K)])
    tg = [round(float(np.mean(np.array(o['mean_exc_over_RJ'])[groups[1:]==k])),3) for k in range(1, K)]
    p = pred[(K, Ep, la)]
    rows.append(dict(K=K, Eprime=Ep, launch=la, sigma=o['sigma'], toy_mean_N0=round(o['mean_N0'],4), se_N0=round(o['block_se']['mean_N0'],4),
                     GGE_pred_N0=round(p['GGE_mean_N0'],4), RJ_N0=round(p['RJ_mean_N0'],4), toy_g2=round(o['g2_exc_mean'],3), GGE_g2=round(p['GGE_g2_exc'],3),
                     toy_groups=tg, GGE_groups=p['GGE_group_over_RJ'], lyapunov=round(o['lyapunov'],4), H0=o['H0'], drift=o['drift']))
    print(rows[-1])
json.dump(rows, open('gge_focused_summary.json','w'), indent=1)
