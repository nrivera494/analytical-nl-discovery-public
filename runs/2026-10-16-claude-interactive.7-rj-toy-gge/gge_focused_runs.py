"""Disorder-free toy runs with the 'focused' launch, to test the pre-registered GGE predictions
(gge_predict_focused.json, written before these runs)."""
import json, warnings
warnings.filterwarnings('ignore')
import resonant_model as r
common = dict(zmax=20000., zburn=2000., dz=0.05, J=400, seed=0, phase_seed=1, dis_seed=7, sigma=0.0)
cases = [dict(K=4, Eprime=0.9, launch='focused'), dict(K=4, Eprime=0.6, launch='focused'), dict(K=5, Eprime=0.9, launch='focused'),
         dict(K=4, Eprime=0.6, launch='dephased')]
with open('gge_focused_runs.jsonl', 'w') as f:
    for c in cases:
        o = r.run(**common, **c); f.write(json.dumps(o) + '\n'); f.flush()
