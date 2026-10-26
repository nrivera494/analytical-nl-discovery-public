"""Disorder-free GRIN dynamics (exact tensor, K=5) for the centre-focused launch, testing the pre-registered GGE predictions
in grin_gge_predict.json (written before this run)."""
import json, numpy as np, warnings
warnings.filterwarnings('ignore')
import grin_model_phases as gm
from grin_overlaps import grin_tensor, hermite_functions
K = 5
modes, groups, S = grin_tensor(K)
psi0 = hermite_functions(K, np.array([0.0]))[:, 0]
centre = np.array([psi0[nx]*psi0[ny] for nx, ny in modes])
with open('grin_focused_runs.jsonl', 'w') as f:
    for Ep in [0.6, 0.9]:
        ph = np.random.default_rng(1).uniform(0, 2*np.pi, len(modes)); nz = np.abs(centre) > 1e-12
        ph[nz] = np.where(centre[nz] > 0, 0.0, np.pi)
        o = gm.run(K=K, Eprime=Ep, zmax=10000., zburn=1000., dz=0.05, J=0, seed=0, phase_seed=1, sigma=0.0, launch='dephased', phases=ph)
        o['launch'] = 'centre-focused'; f.write(json.dumps(o) + '\n'); f.flush()
        print(Ep, 'N0', round(o['mean_N0'], 4), '+-', round(o['block_se']['mean_N0'], 4), 'H0', round(o['H0'], 4), 'lyap', round(o['lyapunov'], 4), 'drift', o['drift'], flush=True)
