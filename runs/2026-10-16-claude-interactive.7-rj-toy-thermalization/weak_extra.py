"""Additional cases for run 2026-10-16-claude-interactive.7-rj-toy-thermalization (added after the sigma=1 failures):
weak disorder sigma=0.3, dephased launch. Predictions fixed earlier: non-condensed polytope MC (polytope_pred_noncondensed.json,
computed 15:18) and the Dirichlet values for K=5 (claim C-01, item list)."""
import json, warnings
warnings.filterwarnings('ignore')
import resonant_model as r
common = dict(zmax=20000., zburn=2000., dz=0.05, J=400, seed=0, phase_seed=1, dis_seed=7, sigma=0.3)
cases = [dict(K=4, Eprime=1.5, launch='dephased'), dict(K=4, Eprime=2.0, launch='dephased'), dict(K=5, Eprime=0.6, launch='dephased')]
with open('weak_extra.jsonl', 'w') as f:
    for c in cases:
        o = r.run(**common, **c); f.write(json.dumps(o) + '\n'); f.flush()
