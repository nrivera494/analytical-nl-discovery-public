"""Mode-count robustness of the linearized-state results: K = 4 (10 modes) and K = 6 (21 modes), E' = 0.6, sigma = 0.3."""
import json, warnings, time
warnings.filterwarnings('ignore')
import gauss_state as gs
out = []
t0 = time.time()
for K in [4, 6]:
    o = gs.run(K=K, Eprime=0.6, sigma=0.3, zmax=400.)
    out.append(o)
    for r in o['records']:
        m0 = r['modes'][0]
        print(f"K={K} z={r['z']:.0f} mm={r['multimode_min_quad_dB']:.1f} lam_gen_dB={r['lambda_gen_dB']:.1f} FN={r['Fano_N']:.3f} cond_quad_dB={m0['min_quad_dB']:.1f} cond_S={m0['S_ent']:.2f}", flush=True)
json.dump(out, open('gauss_modecount.json', 'w'), indent=1); print('wall', time.time()-t0)
