"""POST HOC (not pre-registered): step-size robustness of the strong-disorder result (slow relaxation at sigma = 3, L_d ~ 0.1 L_NL).
(a) Piecewise-constant coupling, sigma_eff = 3, l_c = 0.1 L_NL, dis_seed 101: the disorder path does not depend on dz (one draw per
    segment), so dz = 0.02 and dz = 0.01 integrate the same realization; compare L_rel and the endpoint over z in [1000, 4000].
(b) White noise sigma = 3 at dz = 0.01 (dis_seed 101-103): a different realization than at dz = 0.02 for the same seed, so the comparison
    is statistical (median L_rel 753 L_NL and endpoints 0.705-0.759 at dz = 0.02). Output posthoc_dz_check.json and printed lines."""
import json, numpy as np, warnings
warnings.filterwarnings('ignore')
import ens_model as em
out = []
for dz in (0.02, 0.01):
    r = em.run('deph', 0.6, 1, disorder=em.PiecewiseDisorder(3.0, 0.1, 101, dz), dz=dz)
    out.append(dict(case='piecewise_s3_lc0.1_dis101', dz=dz, I0=r['I0'], g2=r['g2_ex'], L_rel=r['L_rel'], D_RJ=r['D_RJ'], VarRatio=r['VarI0']/r['VarI0_D']))
    print(json.dumps(out[-1]), flush=True)
for seed in (101, 102, 103):
    r = em.run('deph', 0.6, 1, disorder=em.WhiteDisorder(3.0, seed, 0.01), dz=0.01)
    out.append(dict(case=f'white_s3_dis{seed}', dz=0.01, I0=r['I0'], g2=r['g2_ex'], L_rel=r['L_rel'], D_RJ=r['D_RJ'], VarRatio=r['VarI0']/r['VarI0_D']))
    print(json.dumps(out[-1]), flush=True)
json.dump(out, open('posthoc_dz_check.json', 'w'), indent=1)
