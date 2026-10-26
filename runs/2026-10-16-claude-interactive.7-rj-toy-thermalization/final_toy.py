"""Registered run 2026-10-16-claude-interactive.7-rj-toy-thermalization: all cases, fixed seeds."""
import json, warnings
warnings.filterwarnings('ignore')
import resonant_model as r
common = dict(zmax=20000., zburn=2000., dz=0.05, J=400, seed=0, phase_seed=1, dis_seed=7)
cases = [dict(K=4, Eprime=0.3, launch='dephased', sigma=0.0), dict(K=4, Eprime=0.9, launch='dephased', sigma=0.0),
         dict(K=5, Eprime=0.9, launch='dephased', sigma=0.0)]
for sig in [0.3, 1.0]:
    for Ep in [0.3, 0.6, 0.9]:
        for launch in ['dephased', 'focused']:
            cases.append(dict(K=4, Eprime=Ep, launch=launch, sigma=sig))
cases += [dict(K=4, Eprime=1.5, launch='dephased', sigma=1.0), dict(K=4, Eprime=2.0, launch='dephased', sigma=1.0),
          dict(K=5, Eprime=0.6, launch='dephased', sigma=1.0)]
if __name__ == '__main__':
    with open('final_toy.jsonl', 'w') as f:
        for c in cases:
            o = r.run(**common, **c)
            f.write(json.dumps(o) + '\n'); f.flush()
