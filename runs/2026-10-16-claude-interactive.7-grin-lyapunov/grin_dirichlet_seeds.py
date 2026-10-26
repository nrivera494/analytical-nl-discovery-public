"""Robustness of the Dirichlet law (C-01) with the exact GRIN tensor: E'=0.6, sigma=0.3, launch phase seeds 2 and 3 (seed 1 in grin-lyapunov)."""
import json, warnings
warnings.filterwarnings('ignore')
import grin_model as gm
with open('grin_dirichlet_seeds.jsonl', 'w') as f:
    for ps in [2, 3]:
        o = gm.run(K=5, Eprime=0.6, zmax=10000., zburn=1000., dz=0.05, J=0, seed=0, phase_seed=ps, sigma=0.3, launch='dephased', lyap=False)
        f.write(json.dumps(o) + '\n'); f.flush()
        print(f"phase_seed={ps}: N0={o['mean_N0']:.4f}+-{o['block_se']['mean_N0']:.4f} (RJ 0.7393) g2={o['g2_exc_mean']:.3f}+-{o['block_se']['g2_exc_mean']:.3f} (1.867) cross={o['cross_mean']:.3f} (0.933) varN0={o['var_N0']:.2e} (Dir {o['pred']['var_N0']:.2e})", flush=True)
