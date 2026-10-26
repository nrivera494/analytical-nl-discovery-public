"""How much intra-group disorder erases the input-phase memory (C-03)? GRIN exact tensor, K=5, E'=0.6, centre-focused launch,
sigma in {0.03, 0.1, 0.3} (decorrelation length L_d = 1/sigma^2 = 1111, 100, 11 L_NL); compare <I_0> with GGE (0.695) and RJ (0.739)."""
import json, numpy as np, warnings
warnings.filterwarnings('ignore')
import grin_model_phases as gm
from grin_overlaps import grin_tensor, hermite_functions
K = 5; modes, groups, S = grin_tensor(K)
psi0 = hermite_functions(K, np.array([0.0]))[:, 0]; centre = np.array([psi0[nx]*psi0[ny] for nx, ny in modes])
ph = np.random.default_rng(1).uniform(0, 2*np.pi, len(modes)); nz = np.abs(centre) > 1e-12; ph[nz] = np.where(centre[nz] > 0, 0.0, np.pi)
with open('grin_gge_disorder.jsonl', 'w') as f:
    for sig in [0.03, 0.1, 0.3]:
        o = gm.run(K=K, Eprime=0.6, zmax=10000., zburn=1000., dz=0.05, J=0, seed=0, phase_seed=1, sigma=sig, launch='dephased', phases=ph, lyap=False)
        o['launch'] = 'centre-focused'; f.write(json.dumps(o) + '\n'); f.flush()
        print(f"sigma={sig} (L_d={1/sig**2:.0f} L_NL): <I_0>={o['mean_N0']:.4f} +- {o['block_se']['mean_N0']:.4f}  (GGE 0.695, RJ 0.739); H drift {o['drift']['H']:.3e}", flush=True)
