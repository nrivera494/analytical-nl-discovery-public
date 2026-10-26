"""POST HOC (not pre-registered): shape test of the Dirichlet law per run. Fraction of (z, mode) samples in the window [1000, 4000] with
excited-mode power above 3x its RJ mean; Dirichlet marginal D Beta(1, D-1) gives (1 - 3/D)^(D-1) = 0.0436 for D = 14.
Uses the raw series (every 2 L_NL). Output posthoc_dirichlet_tail.json and a printed table per ensemble group."""
import json, os, numpy as np
import ens_model as em
RAW = os.path.expanduser('~/analytical-nl-discovery-data/2026-10-17-claude-interactive.7-ensemble-thermalization')
rows = [json.loads(l) for l in open('ensemble_thermalization.jsonl')]
D = 14; pred = (1 - 3/D)**(D - 1); res = {}
for r in rows:
    d = np.load(os.path.join(RAW, r['tag'] + '.npz')); z, I = d['z'], d['I'].astype(float)
    sel = (z >= 1000) & (z <= 4000); X = I[sel][:, 1:]
    T = r['Eprime']/D; mean_rj = T/em.eps[1:]
    frac = float((X > 3*mean_rj[None, :]).mean())
    key = f"{r['ens']}_{r['kind']}_E{round(r['Eprime'], 3)}_s{r['sigma']}"; res.setdefault(key, []).append(frac)
out = {k: dict(n=len(v), mean=float(np.mean(v)), sd=float(np.std(v, ddof=1)) if len(v) > 1 else 0.0, min=float(np.min(v)), max=float(np.max(v))) for k, v in res.items()}
out['_dirichlet_prediction'] = pred
json.dump(out, open('posthoc_dirichlet_tail.json', 'w'), indent=1)
print(f"Dirichlet tail fraction P(I > 3 <I>_RJ) = {pred:.4f}")
for k, v in out.items():
    if not k.startswith('_'): print(f"{k}: n={v['n']} tail fraction {v['mean']:.4f} +- {v['sd']:.4f} [{v['min']:.4f}, {v['max']:.4f}]")
