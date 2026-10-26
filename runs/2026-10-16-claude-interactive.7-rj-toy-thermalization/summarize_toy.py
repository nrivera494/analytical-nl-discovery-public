"""Summarize final_toy.jsonl and weak_extra.jsonl (raw_location) into summary.json."""
import json, os, numpy as np
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-16-claude-interactive.7-rj-toy-thermalization')
here = os.path.dirname(os.path.abspath(__file__))
pnc = {(r['K'], r['Eprime']): r for r in json.load(open(os.path.join(here, 'polytope_pred_noncondensed.json')))}
rows = []
for fname in ['final_toy.jsonl', 'weak_extra.jsonl']:
    for l in open(os.path.join(RAW, fname)):
        o = json.loads(l)
        K, Ep, M = o['K'], o['Eprime'], o['M']; D = M-1
        eps = np.concatenate([[k]*(k+1) for k in range(K)]).astype(float); groups = eps.astype(int)
        S1 = np.sum(1/eps[1:])
        if Ep <= 1.0:
            pN0, pg2, pcross, pvar = 1-Ep*S1/D, 2-2/M, 1-1/M, o['pred']['var_N0']
            pmeans = Ep/(D*eps[1:])
        else:
            p = pnc[(K, Ep)]; pN0, pvar = p['mean'][0], p['var_N0']; pg2 = float(np.mean(p['g2'][1:])); pcross = None
            pmeans = np.array(p['mean'][1:])
        toy_means = np.array(o['mean_exc_over_RJ'])*(Ep/(D*eps[1:]))
        grp_ratio = [round(float(np.mean(toy_means[groups[1:]==k]/pmeans[groups[1:]==k])), 3) for k in range(1, K)]
        rows.append(dict(source=fname, K=K, M=M, Eprime=Ep, sigma=o['sigma'], launch=o['launch'], lyapunov=round(o['lyapunov'], 5),
            mean_N0=round(o['mean_N0'], 4), se_mean_N0=round(o['block_se']['mean_N0'], 4), pred_mean_N0=round(float(pN0), 4),
            g2_exc_mean=round(o['g2_exc_mean'], 3), se_g2=round(o['block_se']['g2_exc_mean'], 3), pred_g2=round(float(pg2), 3),
            cross_mean=round(o['cross_mean'], 3), se_cross=round(o['block_se']['cross_mean'], 3), pred_cross=None if pcross is None else round(pcross, 3),
            var_N0=float('%.3e' % o['var_N0']), se_var_N0=float('%.2e' % o['block_se']['var_N0']), pred_var_N0=float('%.3e' % pvar),
            group_mean_over_prediction=grp_ratio,
            block_N0=[round(b['N0'], 3) for b in o['blocks']],
            drift=o['drift'], wall_s=round(o['wall_s'])))
json.dump(dict(note="pred_* : Dirichlet closed forms (E' <= 1) or polytope Monte Carlo (E' > 1). Block SEs underestimate errors when populations drift slowly.", cases=rows),
          open(os.path.join(here, 'summary.json'), 'w'), indent=1)
for r in rows:
    print(f"{r['source'][:5]} K={r['K']} E'={r['Eprime']} s={r['sigma']} {r['launch']:8s} lam={r['lyapunov']:.4f} N0={r['mean_N0']:.3f}+-{r['se_mean_N0']:.3f} ({r['pred_mean_N0']:.3f}) "
          f"g2={r['g2_exc_mean']:.3f}+-{r['se_g2']:.3f} ({r['pred_g2']:.3f}) varN0={r['var_N0']:.2e} ({r['pred_var_N0']:.2e}) grp/pred={r['group_mean_over_prediction']}")
