"""Squeezing ensembles Q-dis, Q-launch, Q-strong of predictions.md (run serially): tangent-map Gaussian state (cond_kerr.run, white
disorder), condensate covariance at z = 1, 2, 5, 10, 20, 50, 100, 200, and lambda_best at n0 = 1e10 (shear + crescent curvature,
optimized over Phi, as in best_squeezing.py). Output: ensemble_squeezing.jsonl (appended; resumable)."""
import json, os, sys, numpy as np, warnings
warnings.filterwarnings('ignore')
from scipy.optimize import minimize_scalar
import cond_kerr as ck
OUT = 'ensemble_squeezing.jsonl'; CPS = (1, 2, 5, 10, 20, 50, 100, 200)
def lam(V, Phi, n0):
    Kd = np.array([[1.0, 0.0], [2*Phi, 1.0]]); W = Kd @ V @ Kd.T
    return np.linalg.eigvalsh(W)[0] + W[1, 1]**2/(8*n0)
def lam_best_dB(r, n0=1e10):
    V = np.array([[r['V_X'], r['C']], [r['C'], r['V_P']]])
    grid = np.concatenate([[0.0], np.logspace(-2, 4, 600)]); vals = [lam(V, p, n0) for p in grid]; i = int(np.argmin(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    best = vals[i]
    if hi > lo:
        res = minimize_scalar(lambda p: lam(V, p, n0), bounds=(lo, hi), method='bounded'); best = min(best, res.fun)
    return float(10*np.log10(best))
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['tag'])
jobs = []
for Ep in [0.3, 0.6]:
    for i in range(12): jobs.append(dict(ens='Q-dis', Ep=Ep, sigma=0.3, phase_seed=1, dis_seed=101 + i))
    for i in range(12): jobs.append(dict(ens='Q-launch', Ep=Ep, sigma=0.3, phase_seed=201 + i, dis_seed=7))
for sig in [1.0, 3.0]:
    for i in range(6): jobs.append(dict(ens='Q-strong', Ep=0.3, sigma=sig, phase_seed=1, dis_seed=101 + i))
if len(sys.argv) > 1 and sys.argv[1] == 'smoke':
    o = ck.run(Eprime=0.3, sigma=0.3, dz=0.02, checkpoints=(1, 2), phase_seed=1, dis_seed=7)
    print('smoke (reference: -4.91, -5.74 dB):', [round(r['own_min_quad_dB'], 2) for r in o['records']]); sys.exit()
for j in jobs:
    tag = f"{j['ens']}_E{j['Ep']}_s{j['sigma']}_ph{j['phase_seed']}_dis{j['dis_seed']}"
    if tag in done: continue
    o = ck.run(Eprime=j['Ep'], sigma=j['sigma'], dz=0.02, checkpoints=CPS, phase_seed=j['phase_seed'], dis_seed=j['dis_seed'])
    recs = [dict(z=r['z'], f0=r['f0'], own_dB=r['own_min_quad_dB'], nu=r['nu'], V_X=r['V_X'], V_P=r['V_P'], V_P_given_X=r['V_P_given_X'],
                 Phi_10dB=r['Phi_10dB'], lam_best_1e10_dB=lam_best_dB(r)) for r in o['records']]
    row = dict(tag=tag, **j, records=recs)
    with open(OUT, 'a') as f: f.write(json.dumps(row) + '\n')
    print(tag + ': own ' + ' '.join(f"{x['own_dB']:.1f}" for x in recs) + ' | lam_best ' + ' '.join(f"{x['lam_best_1e10_dB']:.1f}" for x in recs), flush=True)
