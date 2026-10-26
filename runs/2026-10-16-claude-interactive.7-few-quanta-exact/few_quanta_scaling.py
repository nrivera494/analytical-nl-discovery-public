"""Scaling of the freeze-out of few quanta above a condensate with condensate size N (Q = 6, K = 4 toy, two Fock initial states)."""
import json, numpy as np, warnings
warnings.filterwarnings('ignore')
import resonant_model as rm
from few_quanta_exact import analyze
K = 4; groups = list(rm.build(K, 400, 0)[0].astype(int)); M = len(groups); exc = [m for m in range(M) if groups[m] > 0]
Q = 6
cfg1 = [0]*len(exc); cfg1[0] = Q
g2idx = [i for i, m in enumerate(exc) if groups[m] == 2][0]; cfg2 = [0]*len(exc); cfg2[g2idx] = Q//2
out = []
for N in [8, 12, 20, 50, 100, 300, 1000, 3000]:
    o = analyze(K=K, N=N, Q=Q, inits=[('Q photons in one group-1 mode', cfg1), ('photons in one group-2 mode', cfg2)])
    row = dict(N=N, dim=o['dim'], uniform_Nex_var=o['uniform_Nex_var'], uniform_Nex_mean=o['uniform_Nex_mean'],
               inits=[dict(name=d['name'], PR=d['participation_ratio'], Nex_mean=d['Nex_mean'], Nex_var=d['Nex_var']) for d in o['inits']])
    out.append(row)
    print(f"N={N:5d}: " + "; ".join(f"{d['name'][:16]}: PR={d['PR']:.2f} <Nex>={d['Nex_mean']:.3f} Var={d['Nex_var']:.4f}" for d in row['inits']) + f" | uniform <Nex>={o['uniform_Nex_mean']:.3f} Var={o['uniform_Nex_var']:.3f}", flush=True)
json.dump(out, open('few_quanta_scaling.json', 'w'), indent=1)
