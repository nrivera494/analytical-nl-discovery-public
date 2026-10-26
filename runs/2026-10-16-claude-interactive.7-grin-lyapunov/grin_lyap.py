"""GRIN (exact HG overlaps, S_0000 = 1, so z is in units of L_NL = 1/(g N S_0000)) resonant dynamics:
Lyapunov exponent and long-z statistics, with and without weak intra-group disorder. Dephased launch only."""
import json, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
cases = []
for sig in [0.0, 0.3]:
    for Ep in [0.3, 0.6, 0.9]:
        cases.append(dict(K=5, Eprime=Ep, launch='dephased', sigma=sig))
with open('grin_lyap.jsonl', 'w') as f:
    for c in cases:
        o = gm.run(zmax=10000., zburn=1000., dz=0.05, J=0, seed=0, phase_seed=1, dis_seed=7, **c)
        f.write(json.dumps(o) + '\n'); f.flush()
